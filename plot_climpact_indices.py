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
    plt.ylabel(UNITS_DICT[INAME])
    #plt.show()
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



#***************************************
def MedianPairwiseSlopes(xdata,ydata,mdi,mult10 = True, sort = False):
    '''
    Calculate the median of the pairwise slopes

    :param array xdata: x array
    :param array ydata: y array
    :param float mdi: missing data indicator
    :param bool mult10: multiply output trends by 10 (to get per decade)
    :param bool sort: sort the Xdata first
    :returns: float of slope
    '''
    
    import numpy as np
    
    # sort xdata
    if sort:
        sort_order = np.argsort(xdata)

        xdata = xdata[sort_order]
        ydata = ydata[sort_order]

    slopes=[]
    for i in range(len(xdata)):
        for j in range(i+1,len(xdata)):
            if mdi[j] == False and mdi[i] == False: #changed from: if ydata[j]!=mdi and ydata[i]!=mdi:
                slopes+=[(ydata[j]-ydata[i])/(xdata[j]-xdata[i])]


    mpw=np.median(np.array(slopes))

    # copied from median_pairwise.pro methodology (Mark McCarthy)
    slopes.sort()

    good_data=np.where(ydata != mdi)[0]

    n=len(ydata[good_data])

    dof=n*(n-1)/2
    w=np.sqrt(n*(n-1)*((2.*n)+5.)/18.)

    rank_upper=((dof+1.96*w)/2.)+1
    rank_lower=((dof-1.96*w)/2.)+1

    if rank_upper >= len(slopes): rank_upper=len(slopes)-1
    if rank_upper < 0: rank_upper=0
    if rank_lower < 0: rank_lower=0

    upper=slopes[int(rank_upper)]
    lower=slopes[int(rank_lower)]

    if mult10:
        return 10. * mpw, 10. * lower, 10. * upper      # MedianPairwiseSlopes
    else:
        return  mpw, lower, upper      # MedianPairwiseSlopes




INDIR = '/scratch/vportge/satex/calculated_indices_small_region/'
FILEPATHS = glob.glob(INDIR+'*.nc')
OUTPATH = '/scratch/vportge/plots/Climpact/'

INDICES_NAMES = []

for i in range(len(FILEPATHS)):
    INDICES_NAMES.append(FILEPATHS[i][55:].split('_')[0])

INDICES_NAMES = list(set(INDICES_NAMES))

YEARS=np.arange(1991,2016)


#degree = u'Temp (\u00B0C)'

UNITS_DICT = {'csdi': 'days', 'dtr': u'\u00B0C', 'fd': 'days', 'hw': 'days', 'id': 'days', 'su': 'days', 'tmge10': 'days',
              'tmge5': 'days', 'tmlt10': 'days', 'tmlt10': 'days', 'tmlt5': 'days', 'tmm': u'\u00B0C', 'tn10p': '%', 'tn90p': '%',
              'tnlt2': 'days', 'tnltm2': 'days', 'tnltm20': 'days', 'tnm': u'\u00B0C', 'tnn': u'\u00B0C', 'tnx': u'\u00B0C',
              'tr': 'days', 'tx10p': '%', 'tx90p': '%', 'tx95t': u'\u00B0C', 'txge30': 'days', 'txge35': 'days', 'txgt50p': '%',
              'txn': u'\u00B0C', 'txx': u'\u00B0C', 'wsdi': 'days'}


not_working = []

SLOPES = {}

slopes = []

for INAME in (INDICES_NAMES):
    print(INAME)
    if INAME == 'wsdi' or INAME == 'csdi' or INAME == 'hw': #those are annual indices.
        possible_times = ['ANN']
    elif INAME == 'tx95t':
        possible_times = ['DAY']

    else:
        possible_times = ['MON', 'ANN']



    for TIMERANGE in possible_times:
        indexpath = glob.glob(INDIR+INAME+'_'+TIMERANGE+'*.nc')
        data = iris.load(indexpath)
        data[0].coord('latitude').guess_bounds()
        data[0].coord('longitude').guess_bounds()
        global_mean_areas = iris.analysis.cartography.area_weights(data[0])
        global_mean=data[0].collapsed(['latitude', 'longitude'], iris.analysis.MEAN, weights=global_mean_areas)
        #global_mean=global_mean.collapsed('longitude', iris.analysis.MEAN)

        try:

            plt.close()
            plot_years(global_mean, INAME)

            YDATA = global_mean.data
            XDATA = global_mean.coord('time').points
            MDI  = YDATA.mask

            slopes.append(MedianPairwiseSlopes(XDATA,YDATA,MDI,mult10 = True, sort = False))



        except:
            not_working.append(INAME)
print(not_working)




