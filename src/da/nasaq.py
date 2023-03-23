# data APIs
from scipy.io import netcdf
import numpy as np
import pandas as pd

# plots
import matplotlib
import matplotlib.pyplot as plt

# data formats
import netCDF4
import numpy as np
import rioxarray
import xarray as xr

import pprint

# access APIs
from pydap.client import open_url
from pydap.cas.urs import setup_session
import requests

# overloading
from multipledispatch import dispatch

# logs
import src.logging as log

# ... query data sources
QUERY_SRCS = {'dap': {'daily': {'prefix':'https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2/M2T1NXSLV.5.12.4/',
                                'infix':'MERRA2_400.tavg1_2d_slv_Nx.'},
                      'monthly':{'prefix':'https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2_MONTHLY/M2TMNXFLX.5.12.4',
                                 'infix':'MERRA2_400.tavgM_2d_flx_Nx.'}},
              'dat': {'daily':{'prefix':'https://goldsmr4.gesdisc.eosdis.nasa.gov/data/MERRA2/M2T1NXSLV.5.12.4',
                               'infix':'MERRA2_400.tavg1_2d_slv_Nx.'},
                      'monthly':{'prefix':'https://goldsmr4.gesdisc.eosdis.nasa.gov/data/MERRA2_MONTHLY/M2TMNXFLX.5.12.4/',
                                 'infix':'MERRA2_400.tavgM_2d_flx_Nx.'}}}



# ... build query URLs sets
@dispatch(str, str, list, list)
def build_urls(url_prefix, url_infix, years, months): # Clojure multimethod
    return [f'{url_prefix}/{y}/{url_infix}{y}{mon:02d}.nc4'
            for y in years for mon in months] # good case for a macro

@dispatch(str, str, list, list, list)
def build_urls(url_prefix, url_infix, years, months, days): # Clojure multimethod
    return [f'{url_prefix}/{y}/{mon:02d}/{url_infix}{y}{mon:02d}{day:02d}.nc4'
            for y in years for mon in months for day in days] # good case for a macro

# ... using PyDap API to query NASA's data
def _dap_query(session, url):
    log.info(f'Query NSA at {url}')
    store = xr.backends.PydapDataStore.open(url, session=session)
    log.info(store)
    return xr.open_dataset(store)
    

@dispatch(str, str, list, list)
def query(username, password, URLs, keys):
    datasets = []

    session = None
    for url in URLs:
        try:
            session = setup_session(username, password, check_url=url)
            datasets.append(_dap_query(session, url)[keys])
        except:
            continue
        
    log.info(f'Queried data: {len(datasets)}')
    return xr.concat(datasets,dim='time')
    
# ... uring requests API to query NASA's data
@dispatch(list, str)
def query(URLs, key):

    # Set the FILENAME string to the data file name, the LABEL keyword value, or any customized name. 
    FILENAME = 'data/nasa/tmp-230318.nc4'

    for url in URLs:
        result = requests.get(url)
        try:
            result.raise_for_status()
            f = open(FILENAME,'wb')
            f.write(result.content)
            f.close()
            print('contents of URL written to '+FILENAME)
        except:
            print('requests.get() returned an error code '+str(result.status_code))
