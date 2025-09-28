# Ice shelf flux decomposition

In this repository we are learning the decomposition of Ross ice shelf flux vector fields into its divergence-free and curl-free vector field components with the help of a Helmholtz Neural Network (analog in architecture to the Dissipative Hamiltionian Neural Network, the DHNN, see [this Sosanya et al. 2022](https://arxiv.org/abs/2201.10085).) We thereby aim to provide a new (ML learned) estimate of mass loss representing the observational status-quo, and also a mesh-free and interpretable ice thickness model for Ross ice shelf.

## Contributions
- Sea level rise attribution / **basal melt estimates**/ melt water production: 
    - Based on the work by [Rignot et al. 2013](https://www.science.org/doi/epdf/10.1126/science.1235798) **Ice-Shelf Melting Around Antarctica**.
        - InSAR velocities from 2007/2008.
        - RACMO smb long-term average between 1979 and 2010.
        - thinning rates (and steady-state)
    - "ice shelf basal melting is the largest ablation process in Antarctica"
    - They state “In the absence of vertical shear on floating ice, the surface-derived velocity is equivalent to a depth-averaged velocity.” Hence, our flux observations are much more trusthworthy in this area. Ice thickness observations are rather dense over Ross.
    - Calculate the flux divergence from the curl-free vector field component.
    - flux divergence = smb (net surfac mass balance) - bmb (basal mass balance i.e. basal melt) "the rate of ice-shelf thickening ∂H/∂t equals the sum of net surface mass balance SMB minus net basal melting B minus the lateral divergence in volume flux Hv"
    - ∂H/∂t = SMB – B - ∇ (H v)
    - B_ss (B steady state) is ∂H/∂t = 0
    - We have surface mass balance estimates from the regional climate model [RACMO 2.4](https://tc.copernicus.org/articles/18/4065/2024/) so that bmb (i.e. basal mass balance) can be inferred.
- See if we can attain better **ice shelf thickness interpolation** than Bedmap3 (which has small mean bias for Ross but strong spatial patterns and thus needs bias correction)
    - Bedmap3 applied (1) hydrostatic equilibrium and then (2) bias corrects.

# Ideas for future work
- Pretrain model on hydrostatic equilibrium, as done in Bedmap3
- Use ice shelf thinning data

## Proprocessing:
- Ice shelf mask from Bedmap3
- Erode mask edge by 5 km like in Bedmap3 paper

- directional guidance data set
    - get velocities on native 450 m grid
    - subset values on shelf (without edges) with mask
    - calculate unit velocity components 
    - export tensor with 2M data

# Region - Ross ice shelf
- 1000 x 1000 km region
- Ross ice shelf itself: ~ 500,000 km² (about the size of Spain)
- cold cavity
- ice shelves generally have high snowfall i.e. surface accumulation
- important role with regards to buttressing i.e. stability of the ice sheet
- Ross East and West are vey different: East looses half its mass through basal melting whilte the West doesn't have any basal melt water.
    - smb are similar but basal melt not
- Bedmap3 grid has ~ 2M points over the shelf

# Key words
- ice-ocean interactions
- climate attribution
- XAI (Explainable AI)
- meltwater production
