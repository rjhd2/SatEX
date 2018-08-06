import numpy as np
import iris
import matplotlib.pyplot as plt
import iris.quickplot as qplt
#import matplotlib.cm as mpl_cm
#import iris.plot as iplt
import cartopy.crs as ccrs
#import cartopy.feature as cfeature
import glob
#from iris.util import unify_time_units
import datetime
import numpy.ma as ma
import sys
#import requests
import netCDF4
import iris.plot as iplt
#from median_pairwise_slopes import MedianPairwiseSlopes
import copy

MIN_OR_MAX = 'max'
YEARS = np.arange(1991, 2016)
MONTHS = ["%.2d" % i for i in range(1,13)]
try:
    TILENUM = int(sys.argv[1]) #has format: '1'
except:
    TILENUM = 7

INDIR = '/scratch/vportge/indices/python_created_indices/'+MIN_OR_MAX+'_LST_in_cold_window/'+str(TILENUM)+'/'
tmax = glob.glob(INDIR+'CORRECT_TILES/'+str(TILENUM)+'/*_tmax*.nc')
tmin = glob.glob(INDIR+'CORRECT_TILES/'+str(TILENUM)+'/*_tmin*.nc')

OUTDIR = '/scratch/vportge/indices/python_created_indices/'+MIN_OR_MAX+'_LST_in_cold_window/'+str(TILENUM)+'/'


fname1 = '/scratch/vportge/indices/python_created_indices/max_LST_in_cold_window/0/DTR_MON_0.nc'
fname2 = '/scratch/vportge/indices/python_created_indices/max_LST_in_cold_window/1/DTR_MON_1.nc'


TXx_MON = iris.cube.CubeList()
TNx_MON = iris.cube.CubeList()
TXn_MON = iris.cube.CubeList()
TNn_MON = iris.cube.CubeList()
DTR_MON = iris.cube.CubeList()
FD_MON  = iris.cube.CubeList()
TR_MON  = iris.cube.CubeList()



indices = ['TXx', 'TNx', 'TXn', 'TNn', 'DTR', 'FD', 'TR']

for INDEX in indices:
    FPATH = glob.glob('/scratch/vportge/indices/python_created_indices/max_LST_in_cold_window/*/'+INDEX+'*.nc')
    data = iris.load(FPATH)
    #concatenate data so that all tiles are sticked together!
    data = data.concatenate_cube()

