import torch
import torch.nn as nn

##################################################
### Helmholtz decomposition network, no ResNet ###
##################################################
class HelmholtzNN(nn.Module):
    """
    2D Helmholtz decomposition network
    """
    def __init__(self, coordinate_dims = 2, hidden_dim = 256, n_hidden_layers = 6):
        super().__init__()
        assert coordinate_dims == 2
        self.coordinate_dims = coordinate_dims
        self.hidden_dim = hidden_dim

        # Shared trunk (stack of fully connected layers)
        layers = [nn.Linear(coordinate_dims, hidden_dim), nn.SiLU()]
        for _ in range(n_hidden_layers - 1):
            layers += [nn.Linear(hidden_dim, hidden_dim), nn.SiLU()]
        self.trunk = nn.Sequential(*layers)

        # Two scalar heads: Psi and Phi
        self.head_df_psi   = nn.Linear(hidden_dim, 1) 
        self.head_cf_phi = nn.Linear(hidden_dim, 1)

    def _grad_scalar(self, s, x):
        # gradient of scalar s(x) w.r.t. x -> shape [batch, 2]
        return torch.autograd.grad(
            outputs = s.sum(),
            inputs = x,
            create_graph = True,
        )[0]

    def forward(self, x, return_parts = False, return_potentials = False):
        """
        x: [N, 2] with requires_grad set (we set it if not)
        returns: v = J∇H + ∇Φ  (shape [N, 2])
        """
        if not x.requires_grad:
            x = x.requires_grad_()

        h = self.trunk(x)
        psi = self.head_df_psi(h) # [N, 1]
        phi = self.head_cf_phi(h) # [N, 1]

        # ∇ psi and ∇ phi
        grad_psi = self._grad_scalar(psi, x) # [N, 2]
        grad_phi = self._grad_scalar(phi, x) # [N, 2]

        # J∇H in 2D: (∂H/∂y, -∂H/∂x)
        J_grad_psi = grad_psi.flip(-1) * torch.tensor([1.0, -1.0], device = x.device, dtype = x.dtype)

        # Combine 
        v = J_grad_psi + grad_phi

        if return_parts or return_potentials:
            out = (v,)
            if return_parts:
                out += (J_grad_psi, grad_phi)
            if return_potentials:
                out += (psi, phi)
            return out

        return v
    
####################################################
### Helmholtz decomposition network, with ResNet ###
####################################################

import torch
import torch.nn as nn

class _ResBlock(nn.Module):
    def __init__(self, hidden_dim):
        super().__init__()
        self.lin1 = nn.Linear(hidden_dim, hidden_dim)
        self.lin2 = nn.Linear(hidden_dim, hidden_dim)
        self.act  = nn.SiLU()

    def forward(self, h):
        # residual: h -> lin1 -> act -> lin2 -> +h -> act
        out = self.lin2(self.act(self.lin1(h)))
        return self.act(h + out)

class HelmholtzResNN(nn.Module):
    """
    2D Helmholtz decomposition network
    """
    def __init__(self, coordinate_dims = 2, hidden_dim = 256, n_hidden_layers = 6):
        super().__init__()
        assert coordinate_dims == 2
        self.coordinate_dims = coordinate_dims
        self.hidden_dim = hidden_dim

        # Shared trunk (stack of fully connected layers with residual blocks)
        # First projection (as in your code)
        self.inp = nn.Sequential(
            nn.Linear(coordinate_dims, hidden_dim),
            nn.SiLU()
        )
        # Then n_hidden_layers residual blocks
        # e.g. 6 residual blocks
        self.trunk = nn.ModuleList([_ResBlock(hidden_dim) for _ in range(n_hidden_layers)])

        # Two scalar heads: Psi and Phi
        self.head_df_psi = nn.Linear(hidden_dim, 1)
        self.head_cf_phi = nn.Linear(hidden_dim, 1)

    def _grad_scalar(self, s, x):
        # gradient of scalar s(x) w.r.t. x -> shape [batch, 2]
        return torch.autograd.grad(
            outputs = s.sum(),
            inputs  = x,
            create_graph = True,
        )[0]

    def forward(self, x, return_parts = False, return_potentials = False):
        """
        x: [N, 2] with requires_grad set (we set it if not)
        returns: v = J∇ψ + ∇φ  (shape [N, 2])
        """
        if not x.requires_grad:
            # safer: make x a leaf with grad
            x = x.clone().detach().requires_grad_(True)

        h = self.inp(x)
        for blk in self.trunk:
            h = blk(h)

        psi = self.head_df_psi(h)  # [N, 1]
        phi = self.head_cf_phi(h)  # [N, 1]

        # ∇psi and ∇phi
        grad_psi = self._grad_scalar(psi, x)  # [N, 2]
        grad_phi = self._grad_scalar(phi, x)  # [N, 2]

        # J∇ψ in 2D: (∂ψ/∂y, -∂ψ/∂x)
        J_grad_psi = grad_psi.flip(-1) * torch.tensor([1.0, -1.0], device = x.device, dtype = x.dtype)

        # Combine
        v = J_grad_psi + grad_phi

        if return_parts or return_potentials:
            out = (v,)
            if return_parts:
                out += (J_grad_psi, grad_phi)
            if return_potentials:
                out += (psi, phi)
            return out

        return v
