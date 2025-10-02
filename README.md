# Ice shelf flux decomposition

In this repository we are learning the decomposition of Ross ice shelf flux vector fields into its divergence-free and curl-free vector field components with the help of a Helmholtz Neural Network (analog in architecture to the Dissipative Hamiltionian Neural Network, the DHNN, see [this Sosanya et al. 2022](https://arxiv.org/abs/2201.10085).) We thereby aim to provide a new (ML learned) estimate of mass loss representing the observational status-quo, and also a mesh-free and interpretable ice thickness model for Ross ice shelf.

# Output

![DHNN predicted basal melt over Ross Ice Shelf](figures/basal_melt_ross.png)

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

# Equation

∂t∂H ​+ ∇⋅(Hu) - SMB = Basal Melt

https://polar-iceshelf.org/news/ 

# Inputs

## Ice thickenss

We use the Bedmap collection of ice thickness measurements. We combine all standardised .csv files from the Bedmap1, Bedmap2 and Bedmap3 collections from the [UK Polar Data Centre](https://www.bas.ac.uk/data/uk-pdc/). The lists of .csv files are visible on [this Bristish Antarctic Survey (BAS) webpage](https://www.bas.ac.uk/project/bedmap/#data).

Bedmap(3) references:
- *Pritchard, Hamish D., et al. "Bedmap3 updated ice bed, surface and thickness gridded datasets for Antarctica." Scientific data 12.1 (2025): 414.*
- *Frémand, Alice C., et al. "Antarctic Bedmap data: Findable, Accessible, Interoperable, and Reusable (FAIR) sharing of 60 years of ice bed, surface, and thickness data." Earth System Science Data 15.7 (2023): 2695-2710.*

![Ice thickess observations from Bedmap 1+2+3](figures/ice_thickness_points_onshelf.png)

## Ice velocity

We use [MEaSUREs Phase-Based Antarctica Ice Velocity Map, Version 1](https://nsidc.org/data/nsidc-0754/versions/1)

Reference:
- *Mouginot, J., Rignot, E. & Scheuchl, B. (2019). MEaSUREs Phase-Based Antarctica Ice Velocity Map. (NSIDC-0754, Version 1). [Data Set]. Boulder, Colorado USA. NASA National Snow and Ice Data Center Distributed Active Archive Center. https://doi.org/10.5067/PZ3NJ5RXRH10. Date Accessed 10-02-2025.*

![Ice velocity (phase-based)](figures/ice_velocity_phase_oshelf.png)

## Surface mass balance (smb)

We use interpolated [Monthly RACMO2.4p1 data for Greenland (11 km) and Antarctica (27 km) for SMB, SEB, near-surface temperature and wind speed (2006-2015) Version 2](https://zenodo.org/records/13773130)

Reference:
- *Van Dalum, Christiaan T., Willem Jan van de Berg, Srinidhi N. Gadde, Maurice Van Tiggelen, Tijmen van der Drift, Erik van Meijgaard, Lambertus H. van Ulft, and Michiel R. Van Den Broeke. "First results of the polar regional climate model RACMO2. 4." The Cryosphere 18, no. 9 (2024): 4065-4088.*

![SMB estimates from RACMO2.4pw](figures/smb_ross_racmo.png)