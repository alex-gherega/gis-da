# data representation and ops
import numpy as np
import pandas as pd
import rioxarray
import xarray as xr

# date/time
from datetime import datetime, date

def open_rdf(columns=['PRECTOT','PRECTOTCORR']):
    rain_xr = xr.open_zarr('data/nasa/rainfall/').load()[columns]

    # rainfall units in kg m-2 h-1
    rain_xr = rain_xr * 3600
    rain_xr.attrs['units'] = f'kg m-2 h-1'  
    
    return rain_xr

def sel_dailybox(rain_xr,
                 lats=slice(47.,47.5), lons=slice(16., 17.),
                 withdrop=True): #TODO: parameterize with corse (e.g. 2) and time-aggregation (e.g. 24)
    
    # select a 60km x 60km ~ 30' x 30' (1' = 1NM = 1.852)
    rdf_box = rain_xr.sel(lat=lats, lon=lons)

    rdf_box = rdf_box.coarsen(lat=2).sum().coarsen(lon=2).sum() * 24 
    rdf_box.attrs['units'] = 'kg m-2 24h'
    rdf_box = rdf_box.to_dataframe()
    
    # a complicated way of dropping levels
    # rdf_box = rdf_box.xs((slice(None),slice(None)), level=['lat','lon'], axis=0, drop_level=True) 

    if withdrop:
        rdf_box.index = rdf_box.index.droplevel(['lat','lon'])

    rdf_box.rename_axis('date', inplace=True)
    rdf_box.rename(columns={'PRECTOT':'rainfall'}, inplace=True)

    return rdf_box
