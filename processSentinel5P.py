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
##################
inputfiles = sorted(glob.glob('/home/masabas/workSentinel5P/data/S5P_NRTI_L2__SO2____202511*.nc')) #sys.argv[2]
###############
variable = 'sulfurdioxide_total_vertical_column'
##########################
for inputfile in inputfiles:
    print(inputfile)
    data = xr.open_dataset(inputfile,group = 'PRODUCT')
    lon = data.longitude.compute().data
    lat = data.latitude.compute().data
    time_dt = datetime.strptime(inputfile.split('_')[-6], '%Y%m%dT%H%M%S')
    #start_date = data.start_time.strftime('%Y-%b-%d %H:%M:%S')
    mask = ((lon >= wrfoutgrid.lon.min().item()) & (lon <= wrfoutgrid.lon.max().item()) &
            (lat >= wrfoutgrid.lat.min().item()) & (lat <= wrfoutgrid.lat.max().item()))
    if mask.any():
        # ---------------------------
        # 3) Build xarray Dataset
        # ---------------------------
        da_var = data['sulfurdioxide_total_vertical_column']
        da = xr.DataArray(
            da_var.squeeze('time'),
            dims=("y", "x"),
            coords={
                "lat": (("y", "x"), lat.squeeze()),
                "lon": (("y", "x"), lon.squeeze()),
                "time": time_dt
            },
            name=variable
        )
        dataset = xr.Dataset({variable: da})
        regridder = xe.Regridder(dataset, wrfoutgrid, method='bilinear', periodic=False)
        das = regridder(dataset)
        das[variable] = das[variable].where(das[variable] > 0)
        das[variable].attrs = dataset[variable].attrs
        ds = das.copy()
        # Global attributes
        ds.attrs["title"] = str(variable)
        ds.attrs["source_file"] = str(inputfile)
        ds.attrs["history"] = f"Converted to NetCDF on {datetime.now(UTC)} UTC"
        ds.attrs["time_extracted_from_filename"] = time_dt.isoformat()
        outputnc = ds.time.dt.strftime(variable + '_%Y%m%dT%H%M%S.nc').item()
        outputpng = ds.time.dt.strftime(variable + '_%Y%m%dT%H%M%S.png').item()
        ds.to_netcdf(outputnc)
        ds[variable].plot(x='lon',y='lat', cmap='viridis')
        plt.savefig(outputpng)
        plt.close()
        plt.clf()
        print("Saved with time:", outputnc)
        print("Time extracted:", time_dt)
    else:
        print('This file is not in RS boudary')
