import os, sys, glob, dask
import pandas as pd
import cdsapi
from datetime import datetime, timedelta
reqStartDate = (pd.to_datetime(sys.argv[1],format="%Y-%m-%d") - timedelta(days=0)).strftime('%Y-%m-%d')
reqEndDate = (pd.to_datetime(sys.argv[2],format="%Y-%m-%d") + timedelta(days=0)).strftime('%Y-%m-%d')
#data_dir = '/mnt/data/sateesh/realtimeECMWFanlSink/'
data_dir = sys.argv[3]
#for stamp in pd.date_range(arcStartDate, arcEndDate,freq='3H'):
def SFCdownload(data_dir, stamp):
    print(stamp.strftime('Processing for %Y-%b-%d at: ' + data_dir))
    data_dirr = data_dir + stamp.strftime('/%Y/%m/%d/')
    os.makedirs(data_dirr, exist_ok=True)
    print('Checking for ' + data_dirr + stamp.strftime('download-WrfEraSurface_%Y%m%d%H.grib'))
    if (len(glob.glob(data_dirr + stamp.strftime('download-WrfEraSurface_%Y%m%d%H.grib'))) == 0):
        print('##################################################################')
        print('##################################################################')
        print('Downloading now: ' + data_dirr + stamp.strftime('download-WrfEraSurface_%Y%m%d%H.grib'))
        c = cdsapi.Client()
        c.retrieve( 'reanalysis-era5-single-levels',
            {
                'product_type': 'reanalysis',
                'format': 'grib',
                'variable': ['10m_u_component_of_wind', '10m_v_component_of_wind', '2m_dewpoint_temperature',
                            '2m_temperature', 'land_sea_mask', 'mean_sea_level_pressure',
                            'sea_surface_temperature', 'skin_temperature', 'snow_depth', 'soil_temperature_level_1',
                            'soil_temperature_level_2', 'soil_temperature_level_3', 'soil_temperature_level_4',
                            'surface_pressure', 'total_precipitation', 'volumetric_soil_water_layer_1',
                            'volumetric_soil_water_layer_2', 'volumetric_soil_water_layer_3', 'volumetric_soil_water_layer_4',],
                'year': stamp.strftime('%Y'),
                'month': stamp.strftime('%m'),
                'day': stamp.strftime('%d'),
                'time': stamp.strftime('%H'),
                }, data_dirr + stamp.strftime('download-WrfEraSurface_%Y%m%d%H.grib'))
    return(print('Download file: ', stamp.strftime('%Y/')))

#########
def main_work():
    from dask.distributed import Client, as_completed
    client = Client(n_workers=8, threads_per_worker=1)
    print('hello',client)
    futures=list()
    for stamp in pd.date_range(reqStartDate, reqEndDate, freq='3h'):
        futures.append(client.submit(SFCdownload,data_dir,stamp))
    for future in as_completed(futures):
        print(future.status)

##############
if __name__ == '__main__':
    main_work()
