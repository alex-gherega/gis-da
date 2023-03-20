## How to access NASA satelite data

(For the purposes of this project)

### Data source

[Monthly mean,Time-Averaged,Single-Level,Assimilation,Surface Flux Diagnostics V5.12.4](https://disc.gsfc.nasa.gov/datasets/M2TMNXFLX_5.12.4/summary)

### Data access

The actual data files can be found at: [Online Archive](https://goldsmr4.gesdisc.eosdis.nasa.gov/data/MERRA2_MONTHLY/M2TMNXFLX.5.12.4/) 

Follow this instructions set to gain access to the data via `wget`:
[How to access data via wget](https://disc.gsfc.nasa.gov/information/howto?title=How%20to%20Download%20Data%20Files%20from%20HTTPS%20Service%20with%20wget)

> Access to GES DISC data requires all users to be registered with the Earthdata Login system. Data continue to be free of charge and accessible via HTTPS. Access to data via anonymous FTP is no longer available. Detailed instructions on how to register and receive authorization to access GES DISC data are provided [here](https://disc.gsfc.nasa.gov/data-access).


### Pydap access

One can follow this instructions set to gain access via pydap API:
[How to Access GES DISC Data Using Python](https://disc.gsfc.nasa.gov/information/howto?title=How%20to%20Access%20GES%20DISC%20Data%20Using%20Python) via NASA's [How-to's](https://disc.gsfc.nasa.gov/information/howto)

Or follow this basic code:
```
from pydap.client import open_url
from pydap.cas.urs import setup_session

URL = 'https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2_MONTHLY/M2TMNXFLX.5.12.4/2023/MERRA2_400.tavgM_2d_flx_Nx.202301.nc4'
username= 'yourusernamehere'
password ='yourpasswordhere'

session = setup_session(username, password, check_url=url) 
store = xr.backends.PydapDataStore.open(url, session=session)
data = xr.open_dataset(store)
```
