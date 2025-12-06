import os, sys, glob
from datetime import datetime, timedelta, UTC
import xarray as xr
import xesmf as xe
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
import cartopy.crs as ccrs
## Operational RS boundaries ###
wrfoutgrid = xr.open_dataset('/home/masabas/workMsgNative/etc/operRS_wrf_latlongrid.nc')
## Define custom regular grid
#lat_new = np.arange(10, 30+0.01, 0.01)
#lon_new = np.arange(20, 50+0.01, 0.01)
#outgrid = xr.Dataset({'lat': (['lat', 'lon'], np.meshgrid(lat_new, lon_new)[0].T),
#    'lon': (['lat', 'lon'], np.meshgrid(lat_new, lon_new)[1].T)})

#import h5py
#def walk(name, obj):
#    if isinstance(obj, h5py.Dataset):
#        print("DATASET:", name)
#    elif isinstance(obj, h5py.Group):
#        print("GROUP:   ", name)
#
#with h5py.File(inputfile, "r") as f:
#    f.visititems(walk)
##################
inputfiles = sorted(glob.glob('/home/masabas/workSentinel5P/dataMLS/MLS-Aura_L2GP-H2O_*.he5')) #sys.argv[2]
###############
variable = 'H2O' # HDFEOS/SWATHS/H2O

##########################
for inputfile in inputfiles:
    print(inputfile)
    datalatlon = xr.open_dataset(inputfile,group = '/HDFEOS/SWATHS/H2O')
    #data = xr.open_dataset(inputfile,group = '/HDFEOS/SWATHS/H2O/Data Fields').H2O.data
    data = xr.open_dataset(inputfile,group = '/HDFEOS/SWATHS/H2O/Data Fields').L2gpValue.data
    lon = xr.open_dataset(inputfile,group = '/HDFEOS/SWATHS/H2O/Geolocation Fields/').Longitude.data
    lat = xr.open_dataset(inputfile,group = '/HDFEOS/SWATHS/H2O/Geolocation Fields/').Latitude.data
    nlevels = xr.open_dataset(inputfile,group = '/HDFEOS/SWATHS/H2O-APriori').nLevels.data
    pressure = xr.open_dataset(inputfile,group = '/HDFEOS/SWATHS/H2O/Geolocation Fields/').Pressure.data
    time_dt = datetime.strptime(inputfile.split('_')[-1], '%Yd%j.he5')
    #start_date = data.start_time.strftime('%Y-%b-%d %H:%M:%S')
    mask = ((lon >= wrfoutgrid.lon.min().item()) & (lon <= wrfoutgrid.lon.max().item()) &
            (lat >= wrfoutgrid.lat.min().item()) & (lat <= wrfoutgrid.lat.max().item()))
    if mask.any():
        # ---------------------------
        # 3) Build xarray Dataset
        # ---------------------------
        da_var = data[variable]
        ds = xr.Dataset({
            "H2O": (["obs","lev"], data),
            "Pressure": (["lev"], pressure),
            "lat": (["obs"], lat),
            "lon": (["obs"], lon),
        })
        dataset = ds
        ds.H2O.plot(x='obs', 'lev')
        sys.quit() # incomplete and complex.
