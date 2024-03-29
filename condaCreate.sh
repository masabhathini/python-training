#!/usr/bin/bash
## Python env using Conda.
## Author: Dr. M. Sateesh
## Date: 2022-04-16
## sateesh.masabathini@kaust.edu.sa/masabhathini@gmail.com
######################
wget  https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh
sh Anaconda3-2022.05-Linux-x86_64.sh
conda create -n envPy38Sat -c conda-forge python=3.8  -y
###
conda install  -n envPy38Sat -c conda-forge satpy -y       ## for meteorological, satellite data
conda install  -n envPy38Sat -c conda-forge pygrib pyhdf   -y
conda install  -n envPy38Sat -c conda-forge wrf-python  -y
conda install  -n envPy38Sat -c conda-forge metpy    -y
conda install  -n envPy38Sat -c conda-forge xmitgcm  -y
### Big Data parallel computing 
conda install  -n envPy38Sat -c conda-forge dask distributed  dask-jobqueue  -y
####  Tools 
conda install  -n envPy38Sat -c conda-forge python-cdo  -y
## plotting
conda install  -n envPy38Sat -c conda-forge matplotlib   -y
## Shape files
conda install  -n envPy38Sat -c conda-forge basemap   -y
conda install  -n envPy38Sat -c conda-forge cartopy   -y
conda install  -n envPy38Sat -c conda-forge basemap-data-hires   -y
conda install  -n envPy38Sat -c conda-forge geopandas   -y
conda install  -n envPy38Sat -c conda-forge rioxarray   -y
conda install  -n envPy38Sat -c conda-forge gdal -y
conda install  -n envPy38Sat -c conda-forge pycrs -y
conda install  -n envPy38Sat -c conda-forge climpred   -y
conda install  -n envPy38Sat -c conda-forge xclim   -y
conda install  -n envPy38Sat -c conda-forge windrose -y
conda install  -n envPy38Sat -c anaconda jinja2 
conda install  -n envPy38Sat -c conda-forge folium
conda install  -n envPy38Sat -c conda-forge qgis
conda install  -n envPy38Sat -c conda-forge f90nml
conda install  -n envPy38Sat -c anaconda pysal
conda install  -n envPy38Sat -c mzh pypdf4   ## pip install PyPDF4
###
pip install geog
pip install salem
pip install python-dotenv
pip install motionless
pip install scikit-image
pip install pycryptodome  # Encrypt / decrypt data in python with salt
#######################################
#######################################
source /home/$HOME/anaconda3/bin/activate envPy38Sat
