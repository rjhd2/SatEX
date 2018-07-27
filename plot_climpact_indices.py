# -*- coding: iso-8859-1 -*-
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

def plot_daily_cycle(data, outpath):
    """"Plot a daily cycle for some specific gridpoint."""
    plt.close()
    fig = plt.figure()
    plt.plot(data)
    plt.grid()
    plt.title('CM SAF daily cycle for specific gridpoint')
    plt.xlabel('UTC hour of the day')
    plt.ylabel('LST in K')
    plt.savefig(outpath+'CM_SAF_time_series_LST'+day_yyyymmdd+'.png')

def plot_map(data, outpath):
    """"Plot filled contour map of LST for some hour."""
    plt.close()
    qplt.contourf(data)
    plt.gca().coastlines() #add coastlines
    plt.title('CM SAF map of LST of some hour')
    plt.savefig(outpath+'CM_SAF_map_LST'+day_yyyymmdd+'.png')

def plot_years(y, indexname):
    plt.close()
    fig=plt.figure()
    iplt.plot(y)
    plt.grid()
    plt.title('Time series of averaged '+indexname+' values ('+TIMERANGE+')')
    plt.savefig(OUTPATH+indexname+'_'+TIMERANGE+'.png')


def plot_figure(data, gridlons, gridlats, title, outname, outpath):
    """Plot min/max LST for some day."""
    plt.close()
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    lst_map = plt.contourf(gridlons, gridlats, data, transform=ccrs.PlateCarree())
    cbar = plt.colorbar(lst_map, orientation='horizontal', extend='both')
    ax.coastlines()
    plt.title('CM SAF '+title)
    plt.show()
    #plt.savefig(outpath+'CM_SAF_map_LST_'+title[0:3]+'_'+outname+'.png')
    return


INDIR = '/scratch/vportge/satex/calculated_indices_small_region/'
FILEPATHS = glob.glob(INDIR+'*.nc')
OUTPATH = '/scratch/vportge/plots/Climpact/'

INDICES_NAMES = []

for i in range(len(FILEPATHS)):
    INDICES_NAMES.append(FILEPATHS[i][55:].split('_')[0])

INDICES_NAMES = list(set(INDICES_NAMES))

YEARS=np.arange(1991,2016)


for INAME in (INDICES_NAMES):

    if INAME == 'wsdi' or INAME == 'csdi' or INAME == 'hw': #those are annual indices.
        possible_times = ['ANN']
    elif INAME == 'tx95t':
        possible_times = ['DAY']

    else:
        possible_times = ['MON', 'ANN']



    for TIMERANGE in possible_times:
        indexpath = glob.glob(INDIR+INAME+'_'+TIMERANGE+'*.nc')
        data = iris.load(indexpath)

        global_mean=data[0].collapsed('latitude', iris.analysis.MEAN)
        global_mean=global_mean.collapsed('longitude', iris.analysis.MEAN)

        try:

            plt.close()
            plot_years(global_mean, INAME)
        except:
            print('doesnt work')
            print(INAME)




