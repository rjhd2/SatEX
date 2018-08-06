import numpy as np
import iris
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import iris.quickplot as qplt
#import matplotlib.cm as mpl_cm
#import iris.plot as iplt
import cartopy.crs as ccrs
import cartopy.feature as cfeat
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
    lst_map = plt.pcolormesh(gridlons, gridlats, data, transform=ccrs.PlateCarree(), cmap = 'RdBu_r')
    cbar = plt.colorbar(lst_map, orientation='horizontal', extend='both')
    ax.coastlines()
    ax.set_extent((np.amin(gridlons)-2, np.amax(gridlons)+2, np.amin(gridlats)-2, np.amax(gridlats)+2), crs = ccrs.PlateCarree())

    political_bdrys = cfeat.NaturalEarthFeature(category='cultural',
                                                name='admin_0_countries',
                                                scale='50m')
    ax.add_feature(political_bdrys,
                edgecolor='b', facecolor='none', zorder=-1)

    gl = ax.gridlines(draw_labels=True)
    plt.title(title, y=1.08, size=22)
    cbar.set_label(UNITS_DICT[INAME]+' per decade', size=20)
    #plt.tight_layout()
    plt.show()
    #plt.savefig(OUTPATH+INAME+'_map_of_trend_'+TIMERANGE+'.png')
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




INDIR = '/scratch/rdunn/satex/tiles/*/'
OUTPATH = '/scratch/vportge/plots/Climpact/'
MIN_OR_MAX = 'max'



#degree = u'Temp (\u00B0C)'

UNITS_DICT = {'csdi': 'days', 'id': 'days', 'su': 'days', 'tn10p': '%', 'tn90p': '%', 'tnn': u'\u00B0C', 'tnx': u'\u00B0C',
              'tx10p': '%', 'tx90p': '%', 'txn': u'\u00B0C', 'txx': u'\u00B0C', 'wsdi': 'days'}

#python_indices = ['TXx', 'TNx', 'TXn', 'TNn', 'DTR', 'FD', 'TR']

not_working = []

slopes = []
REGIONS = {'SPAIN': [-7.5, 37.5, 0.0, 42.5], 'GERMANY': [5.0, 47.5, 15.0, 52.5], 'MOROCCO': [-5.0, 30.0, 5.0, 35.0]}  #westerly longitude, southerly latitude, easterly longitude, northerly latitude

#UNITS_DICT = {'hw': 'days'}

for INAME in UNITS_DICT:
    print(INAME)
    if INAME == 'wsdi' or INAME == 'csdi' or INAME == 'hw': #those are annual indices.
        possible_times = ['ANN']
    elif INAME == 'tx95t':
        possible_times = ['DAY']

    else:
        possible_times = ['MON', 'ANN']

    for REGION in REGIONS:
        print(REGION)

        left_lon = float(REGIONS[REGION][0])
        right_lon = float(REGIONS[REGION][2])
        lower_lat = float(REGIONS[REGION][1])
        upper_lat = float(REGIONS[REGION][3])

        lat_constraint = iris.Constraint(latitude=lambda c: lower_lat <= c.point <= upper_lat)
        lon_constraint = iris.Constraint(longitude=lambda c: left_lon <= c.point <= right_lon)
        OUTPATH = '/scratch/vportge/plots/Climpact/'+MIN_OR_MAX+'_LST_in_cold_window/'+REGION+'/'

        for TIMERANGE in possible_times:
            if TIMERANGE == 'ANN':
                TITLE_TIME = 'annually'
            elif TIMERANGE == 'MON':
                TITLE_TIME = 'monthly'
            elif TIMERANGE == 'DAY':
                TITLE_TIME = 'daily'


            indexpath = glob.glob(INDIR+INAME+'_'+TIMERANGE+'*-'+MIN_OR_MAX+'*.nc')

            data = iris.load(indexpath)
            for i in range(len(data)):
                del data[i].attributes['file_created']

            data = data.concatenate_cube()

            data = data.extract(lat_constraint)
            data = data.extract(lon_constraint)

            data.coord('latitude').guess_bounds()
            data.coord('longitude').guess_bounds()
            global_mean_areas = iris.analysis.cartography.area_weights(data)
            global_mean=data.collapsed(['latitude', 'longitude'], iris.analysis.MEAN, weights=global_mean_areas)
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
                        index_values = data.data
                        trends = np.zeros(index_values.shape[1:3]) # lat, lon
                        for lat in range(trends.shape[0]):
                            for lon in range(trends.shape[1]):
                                YDATA_GRIDPOINT = index_values[:, lat, lon]
                                trends[lat,lon] = MedianPairwiseSlopes(XDATA,YDATA_GRIDPOINT,mdi=False,mult10 = False, sort = False, calc_with_mdi = False)[0]*365*10.

                        GRIDLONS = data.coord('longitude').points
                        GRIDLATS = data.coord('latitude').points
                        plot_figure(trends, GRIDLONS, GRIDLATS, 'Trend of '+ INAME+' ('+TITLE_TIME+')')
                    except:
                        d=0.

                #except:
                    #not_working.append(INAME)
print(not_working)






