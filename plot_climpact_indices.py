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

    if TIMERANGE == 'ANN':
        title_time = 'annually'
    elif TIMERANGE == 'MON':
        title_time = 'monthly'
    elif TIMERANGE == 'DAY':
        title_time = 'daily'

    plt.close()
    fig=plt.figure()
    iplt.plot(y)
    plt.grid()
    plt.title(indexname+' ('+title_time+')', size=22)
    plt.ylabel(UNITS_DICT[INAME], size=20)
    plt.xlabel('years', size=20)
    plt.tick_params(axis='both', which='major', labelsize=16)

    #plt.show()
    #iplt.plot(trendcube)
    plt.savefig(OUTPATH+indexname+'_'+TIMERANGE+'.png')


def plot_figure(data, gridlons, gridlats, title):
    """Plot map of index for some day."""
    plt.close()
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    lst_map = plt.contourf(gridlons, gridlats, data, transform=ccrs.PlateCarree())
    cbar = plt.colorbar(lst_map, orientation='horizontal', extend='both')
    ax.coastlines()
    gl = ax.gridlines(draw_labels=True)
    plt.title(title, y=1.08, size=22)
    cbar.set_label(UNITS_DICT[INAME]+' per decade', size=20)
    plt.tight_layout()
    plt.savefig(OUTPATH+INAME+'_map_of_trend_'+TIMERANGE+'.png')
    return

def line(x,t,m):
    return m*x+t



#***************************************
def MedianPairwiseSlopes(xdata,ydata,mdi,mult10 = False, sort = False, calc_with_mdi = False):
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
    y_intercepts = []
    for i in range(len(xdata)):
        for j in range(i+1,len(xdata)):
            if calc_with_mdi == True:
                if mdi[j] == False and mdi[i] == False: #changed from: if ydata[j]!=mdi and ydata[i]!=mdi:
                    slopes += [(ydata[j]-ydata[i])/(xdata[j]-xdata[i])]
                    y_intercepts += [(xdata[j]*ydata[i]-xdata[i]*ydata[j])/(xdata[j]-xdata[i])]
            elif calc_with_mdi == False:
                slopes += [(ydata[j]-ydata[i])/(xdata[j]-xdata[i])]
                y_intercepts += [(xdata[j]*ydata[i]-xdata[i]*ydata[j])/(xdata[j]-xdata[i])]

    mpw=np.median(np.array(slopes))
    y_intercept_point = np.median(np.array(y_intercepts))

    # copied from median_pairwise.pro methodology (Mark McCarthy)
    slopes.sort()

    good_data=np.where(ydata == False)[0]

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
        return 10. * mpw, 10. * lower, 10. * upper, y_intercept_point      # MedianPairwiseSlopes
    else:
        return  mpw, lower, upper, y_intercept_point      # MedianPairwiseSlopes




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

#INDICES_NAMES = ['tn10p']

for INAME in (INDICES_NAMES):
    print(INAME)
    if INAME == 'wsdi' or INAME == 'csdi' or INAME == 'hw': #those are annual indices.
        possible_times = ['ANN']
    elif INAME == 'tx95t':
        possible_times = ['DAY']

    else:
        possible_times = ['MON', 'ANN']



    for TIMERANGE in possible_times:
        if TIMERANGE == 'ANN':
            TITLE_TIME = 'annually'
        elif TIMERANGE == 'MON':
            TITLE_TIME = 'monthly'
        elif TIMERANGE == 'DAY':
            TITLE_TIME = 'daily'


        indexpath = glob.glob(INDIR+INAME+'_'+TIMERANGE+'*.nc')
        data = iris.load(indexpath)
        data[0].coord('latitude').guess_bounds()
        data[0].coord('longitude').guess_bounds()
        global_mean_areas = iris.analysis.cartography.area_weights(data[0])
        global_mean=data[0].collapsed(['latitude', 'longitude'], iris.analysis.MEAN, weights=global_mean_areas)
        #global_mean=global_mean.collapsed('longitude', iris.analysis.MEAN)

        if INAME in ['hw', 'tnx', 'txx', 'tx95t', 'tnm', 'tmm']:

            try:
                plot_years(global_mean, INAME)
            except:
                d = 0

        if INAME not in ['hw', 'tnx', 'txx', 'tx95t', 'tnm', 'tmm']:

            #try:
            #####################################################################
            #Plot time series of spatially averaged data with trend calculation #
            #####################################################################




            plt.close()
            #plot_years(global_mean, INAME)
            YDATA = global_mean.data
            XDATA = global_mean.coord('time').points
            MDI  = YDATA.mask

            trendanalysis = MedianPairwiseSlopes(XDATA,YDATA,MDI,mult10 = False, sort = False, calc_with_mdi=True)

            slope = trendanalysis[0]
            slope_lower_uncrty = trendanalysis[1]
            slope_upper_uncrty = trendanalysis[2]
            #Y_INTERCEPTION = np.median(YDATA)-slope*np.median(XDATA)
            Y_INTERCEPTION = trendanalysis[3]
            slopes.append(slope)

            trendcube = copy.deepcopy(global_mean)
            trendcube.rename('Trend')
            trendcube.data=line(XDATA, Y_INTERCEPTION, slope)
            '''
            trendcube_upper = copy.deepcopy(global_mean)
            trendcube_upper.rename('Upper Trend')
            trendcube_upper.data=line(XDATA, Y_INTERCEPTION, slope_upper_uncrty)

            trendcube_lower = copy.deepcopy(global_mean)
            trendcube_lower.rename('Upper Trend')
            trendcube_lower.data=line(XDATA, Y_INTERCEPTION, slope_lower_uncrty)       
            '''

            plt.close()
            fig=plt.figure(figsize = (10, 8))
            iplt.plot(global_mean)
            plt.grid()
            plt.title(INAME+' ('+TITLE_TIME+')', size=22)
            plt.ylabel(UNITS_DICT[INAME], size=20)
            plt.xlabel('years', size=20)

            iplt.plot(trendcube, label='trend: '+str(round(slope*365*10.,2))+' '+UNITS_DICT[INAME]+' per decade')
            #iplt.plot(trendcube_lower, label='lower trend: '+str(round(slope*365*10.,2))+' '+UNITS_DICT[INAME]+' per decade')
            #iplt.plot(trendcube_upper, label='upper trend: '+str(round(slope*365*10.,2))+' '+UNITS_DICT[INAME]+' per decade')

            plt.legend(fontsize = 16)
            plt.tight_layout()
            plt.tick_params(axis='both', which='major', labelsize=16)

            #plt.xlim( 728294. - 5*365, 735599.)
            plt.savefig(OUTPATH+INAME+'_with_trend_'+TIMERANGE+'.png')


            ####################################################
            #Plot map of calculated trends for every gridpoint #
            ####################################################
            if TIMERANGE == 'ANN':
                try:
                    index_values = data[0].data
                    trends = np.zeros(index_values.shape[1:3]) # lat, lon
                    for lat in range(trends.shape[0]):
                        for lon in range(trends.shape[1]):
                            YDATA_GRIDPOINT = index_values[:, lat, lon]
                            trends[lat,lon] = MedianPairwiseSlopes(XDATA,YDATA_GRIDPOINT,mdi=False,mult10 = False, sort = False, calc_with_mdi = False)[0]*365*10.

                    GRIDLONS = data[0].coord('longitude').points
                    GRIDLATS = data[0].coord('latitude').points
                    plot_figure(trends, GRIDLONS, GRIDLATS, 'Trend of '+ INAME+' ('+TITLE_TIME+')')
                except:
                    d=0.

            #except:
                #not_working.append(INAME)
print(not_working)






