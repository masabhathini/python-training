import os, sys, glob
from matplotlib import pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import LogNorm
import numpy as np
import xarray as xr
import pandas as pd
import rioxarray

########
variable = 'sulfurdioxide_total_vertical_column'
ss = xr.open_mfdataset(glob.glob(variable + '_202511*.nc'), combine='nested', concat_dim='time', parallel=True)

for data in ss.groupby('time.date'):
    t = data[0].strftime('%Y-%^b-%d')
    outputnc = data[0].strftime('merged_' + variable + '_%Y-%^b-%d.nc')
    outputpng = data[0].strftime('merged_' + variable + '_%Y-%^b-%d.png')
    print('Processing for: ', t)
    da = data[1][variable].max(dim='time')
    da = da.expand_dims(time=[pd.to_datetime(data[0])])
    da_pos = da.where(da > 0)
    # Compute safe vmin/vmax
    vmax = float(da_pos.max())
    vmin = max(float(da_pos.min()), 1e-6)   # avoid LogNorm errors
    # Setup map projection (data is lon/lat so PlateCarree)
    proj = ccrs.PlateCarree()
    plt.figure(figsize=(12, 8))
    ax = plt.axes(projection=proj)
    # Plot data
    pcm = da_pos.plot(
        ax=ax,
        x='lon',
        y='lat',
        transform=proj,
        norm=LogNorm(vmin=vmin, vmax=vmax),
        cmap='viridis',
        cbar_kwargs={'label': data[1][variable].units}
    )
    # Add coastlines and borders
    ax.coastlines(resolution='10m', linewidth=1, color='black')
    ax.add_feature(cfeature.BORDERS, linewidth=0.7)
    ax.add_feature(cfeature.LAND, facecolor='lightgray', alpha=0.5)
    ax.add_feature(cfeature.OCEAN, facecolor='white')
    ax.set_extent([
        float(da.lon.min()), float(da.lon.max()),
        float(da.lat.min()), float(da.lat.max())
    ], crs=proj)
    # Title
    plt.title(data[1].title + f"\nTime: {t}")
    plt.tight_layout()
    plt.savefig(outputpng)
    plt.close()
    plt.clf()
    da_pos.to_netcdf(outputnc)
