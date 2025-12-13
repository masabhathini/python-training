## mamba activate /home/masabas/miniconda3/envs/envPy38Sat
import os, sys, glob, dask
import pandas as pd
import cdsapi
from datetime import datetime, timedelta
reqStartDate = (pd.to_datetime(sys.argv[1],format="%Y-%m-%d") - timedelta(days=0)).strftime('%Y-%m-%d')
reqEndDate = (pd.to_datetime(sys.argv[2],format="%Y-%m-%d") + timedelta(days=0)).strftime('%Y-%m-%d')
#data_dir = '/mnt/data/sateesh/realtimeECMWFanlSink/'
data_dir = sys.argv[3]

def UPLdownload(data_dir, stamp):
    print(stamp.strftime('Processing for %Y-%b-%d at: ' + data_dir))
    data_dirr = data_dir + stamp.strftime('/%Y/%m/%d/')
    os.makedirs(data_dirr, exist_ok=True)
    print('Checking for ' + data_dirr + stamp.strftime('download-WrfEraPressure_%Y%m%d%H.grib'))
    if (len(glob.glob(data_dirr + stamp.strftime('download-WrfEraPressure_%Y%m%d%H.grib'))) == 0):
        print('Downloading now: ' + data_dirr + stamp.strftime('download-WrfEraPressure_%Y%m%d%H.grib'))
        c = cdsapi.Client()
        c.retrieve( 'reanalysis-era5-pressure-levels',
            {
                'product_type': 'reanalysis',
                'format': 'grib',
                'variable': ['geopotential', 'relative_humidity', 'specific_humidity', 'temperature',
                    'u_component_of_wind', 'v_component_of_wind', 'vertical_velocity',],
                    'pressure_level': [ '10', '20', '50', '70', '100', '150', '200', '250',
                        '300', '350', '400', '450', '500', '550', '600', '650', '700', '750',
                        '775', '800', '825', '850', '875', '900', '925', '950', '975', '1000',],
                'year': stamp.strftime('%Y'),
                'month': stamp.strftime('%m'),
                'day': stamp.strftime('%d'),
                'time': stamp.strftime('%H'),
                }, data_dirr + stamp.strftime('download-WrfEraPressure_%Y%m%d%H.grib'))
    return(print('Download UPL file: ', stamp.strftime('%Y/')))

#########
def main_work():
    from dask.distributed import Client, as_completed
    client = Client(n_workers=8, threads_per_worker=1)
    print('hello',client)
    futures=list()
    for stamp in pd.date_range(reqStartDate, reqEndDate, freq='3h'):
        futures.append(client.submit(UPLdownload,data_dir,stamp))
    for future in as_completed(futures):
        print(future.status)

##############
if __name__ == '__main__':
    main_work()
