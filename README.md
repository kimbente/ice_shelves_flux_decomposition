# Ice shelf flux decomposition

- “In the absence of vertical shear on floating ice, the surface-derived velocity is equivalent to a depth-averaged velocity.” ([Rignot et al. 2013](https://www.science.org/doi/epdf/10.1126/science.1235798))
- And we have relatively dense ice thickness measurements from Operation Ice Bridge
- Decomposition into curl-free and divergence-free components with [dfNN](https://arxiv.org/abs/2201.10085)

Contribution:
- See if we can attain better ice shelf thickness interpolation than Bedmap3 (which has small mean bias for Ross but strong spatial patterns and thus needs bias correction)
    - Bedmap3 applied (1) hydrostatic equilibrium and then (2) bias corrects.
- Sea level rise attribution / basal melt estimates: interpret flux. Flux (arrising just from the curl-free term) can be subtrated by smb models to estimate basal melt.

Idea:
- Pretrain on hydrostatic equilibrium for better start?


Proprocessing:
- Ice shelf mask from Bedmap3
- Erode mask edge by 5 km like in Bedmap3 paper
