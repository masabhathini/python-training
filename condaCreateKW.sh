wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
conda create -n envwgrib -c conda-forge wgrib wgrib2
conda install -n envwgrib -c conda-forge cdo eccodes netcdf4 hdf5
