## Ref: https://docs.conda.io/projects/miniconda/en/latest/
#mkdir -p ~/miniconda3
#wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
#bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
#rm -rf ~/miniconda3/miniconda.sh
#~/miniconda3/bin/conda init bash
#~/miniconda3/bin/conda init zsh
########################## After this reopen the terminal ##############
## conda create -n envPy311Sat -c conda-forge  -y
############################################################
conda create  -n envPy311Sat -c conda-forge wrf-python -y
conda activate envPy311Sat
conda install -n envPy311Sat -c conda-forge xesmf -y
conda install  -n envPy311Sat -c conda-forge metpy    -y
### Big Data parallel computing 
conda install  -n envPy311Sat -c conda-forge dask distributed  dask-jobqueue  -y
####  Tools 
conda install  -n envPy311Sat -c conda-forge python-cdo  -y
## plotting
conda install  -n envPy311Sat -c conda-forge matplotlib   -y
## Shape files
conda install  -n envPy311Sat -c conda-forge basemap   -y
## conda install  -n envPy311Sat -c conda-forge cartopy   -y
## conda install  -n envPy311Sat -c conda-forge basemap-data-hires   -y
conda install  -n envPy311Sat -c conda-forge geopandas   -y
conda install  -n envPy311Sat -c conda-forge rioxarray   -y
## conda install  -n envPy311Sat -c conda-forge gdal -y
## pip install geog
pip install salem
pip install python-dotenv
pip install motionless
pip install scikit-image
pip install pycryptodome
