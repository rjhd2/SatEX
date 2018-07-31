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


YEARS = np.arange(1991, 2016)
INDIR = '/scratch/vportge/CM_SAF_LST_MIN_MAX/'

MONTHS = ["%.2d" % i for i in range(1,13)]

MONTHLY_AVERAGED = []
MONTHLY_AVERAGED_DATA = []

ANNUAL_AVERAGED = []
ANNUAL_AVERAGED_DATA = []

MONTHLY_AVERAGE = iris.cube.CubeList()
ANNUAL_AVERAGE = iris.cube.CubeList()
for i in range(len(YEARS)):
    #MONTHLY_MAX = np.ma.zeros((12, 856, 2171), fill_value = 1e+20) #25 years, 856 latitude, 2171 longitude
    FINAL_MONTHS = iris.cube.CubeList()

    print(YEARS[i])

    for MONTH in MONTHS:
        print(MONTH)
        FPATH = glob.glob(INDIR+str(YEARS[i])+'/'+str(MONTH)+'/*.nc')
        tmax = iris.load(FPATH, 'Maximum Land Surface Temperature in Warm Window (PMW)')
        tmax = tmax.concatenate_cube()

        FINAL_MONTHS.append(tmax.collapsed('time', iris.analysis.MAX))

        #tmax_data = tmax.data
        #MONTHLY_MAX[int(MONTH)-1,:,:] = ma.max(tmax_data, axis = 0)

    FINAL_MONTHS = FINAL_MONTHS.merge_cube()
    MEAN_MONTHLY_MAX = FINAL_MONTHS.collapsed(('longitude', 'latitude'), iris.analysis.MEAN)
    MEAN_ANNUALLY_MAX = MEAN_MONTHLY_MAX.collapsed('time', iris.analysis.MEAN)

    MONTHLY_AVERAGE.append(MEAN_MONTHLY_MAX)
    ANNUAL_AVERAGE.append(MEAN_ANNUALLY_MAX)


MONTHLY_AVERAGE = MONTHLY_AVERAGE.concatenate_cube()
ANNUAL_AVERAGE = ANNUAL_AVERAGE.concatenate_cube()

qplt.plot(MONTHLY_AVERAGE)
plt.savefig('MONTHLY.png')

plt.close()
qplt.plot(ANNUAL_AVERAGE)
plt.savefig('ANNUALLY.png')


'''
    MEAN_MONTHLY_MAX = ma.mean(MONTHLY_MAX, axis = (1,2))
    MONTHLY_AVERAGED.append(MEAN_MONTHLY_MAX)
    MONTHLY_AVERAGED_DATA.append(MEAN_MONTHLY_MAX.data)

    MEAN_ANNUAL_MAX = ma.mean(MEAN_MONTHLY_MAX)
    ANNUAL_AVERAGED.append(MEAN_ANNUAL_MAX)
    ANNUAL_AVERAGED_DATA.append(MEAN_ANNUAL_MAX.data)
    '''

'''
MONTHLY_AVERAGED_DATA = np.concatenate(MONTHLY_AVERAGED_DATA).ravel()
ANNUAL_AVERAGED_DATA = np.concatenate(ANNUAL_AVERAGED_DATA).ravel()



fig = plt.figure()
plt.plot(MONTHLY_AVERAGED_DATA)
plt.ylabel('K')
plt.savefig('test_monthly.png')

plt.close()
fig = plt.figure()
plt.plot(ANNUAL_AVERAGED_DATA)
plt.savefig('test_annual.png')

'''











