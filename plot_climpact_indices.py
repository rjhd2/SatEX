import numpy as np
import iris
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import iris.quickplot as qplt
import cartopy.crs as ccrs
import cartopy.feature as cfeat
import glob
import datetime
import numpy.ma as ma
import sys
import netCDF4
import iris.plot as iplt
import copy
from plotFunctions import line, plot_figure, MedianPairwiseSlopes, plot_time_series_with_trend


INDIR = '/scratch/rdunn/satex/tiles/*/'
OUTPATH = '/scratch/vportge/plots/Climpact/'
MIN_OR_MAX = 'max'



#degree = u'Temp (\u00B0C)'

UNITS_DICT = {'csdi': 'days', 'id': 'days', 'su': 'days', 'tn10p': '%', 'tn90p': '%', 'tnn': u'\u00B0C', 'tnx': u'\u00B0C',
              'tx10p': '%', 'tx90p': '%', 'txn': u'\u00B0C', 'txx': u'\u00B0C', 'wsdi': 'days'}

#python_indices = ['TXx', 'TNx', 'TXn', 'TNn', 'DTR', 'FD', 'TR']

not_working = []

REGIONS = {'SPAIN': [-7.5, 37.5, 0.0, 42.5], 'GERMANY': [5.0, 45.0, 15.0, 50.0], 'MOROCCO': [-5.0, 30.0, 5.0, 35.0]}  #westerly longitude, southerly latitude, easterly longitude, northerly latitude

slopes_ANN_GERMANY = {}
slopes_MON_GERMANY = {}

slopes_ANN_SPAIN = {}
slopes_MON_SPAIN = {}

slopes_ANN_MOROCCO = {}
slopes_MON_MOROCCO = {}

#UNITS_DICT = { 'su': 'days',}

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


            if INAME not in ['hw', 'tnx', 'txx', 'tx95t', 'tnm', 'tmm']:

                #####################################################################
                #Plot time series of spatially averaged data with trend calculation #
                #####################################################################
                CUBEINFO = [TITLE_TIME, INAME, REGION, TIMERANGE, OUTPATH, 'CM SAF', 365*10.] 
                slopes = plot_time_series_with_trend(global_mean, CUBEINFO, UNITS_DICT)

                if TIMERANGE == 'MON':
                    if REGION == 'GERMANY':
                        slopes_MON_GERMANY[INAME] = slopes
                    elif REGION == 'SPAIN':
                        slopes_MON_SPAIN[INAME] = slopes
                    elif REGION == 'MOROCCO':
                        slopes_MON_MOROCCO[INAME] = slopes

                elif TIMERANGE == 'ANN':
                    if REGION == 'GERMANY':
                        slopes_ANN_GERMANY[INAME] = slopes
                    elif REGION == 'SPAIN':
                        slopes_ANN_SPAIN[INAME] = slopes
                    elif REGION == 'MOROCCO':
                        slopes_ANN_MOROCCO[INAME] = slopes




                ####################################################
                #Plot map of calculated trends for every gridpoint #
                ####################################################
                if TIMERANGE == 'ANN':
                    index_values = data.data
                    XDATA_ANN = data.coord('time').points
                    trends = np.zeros(index_values.shape[1:3]) # lat, lon
                    for lat in range(trends.shape[0]):
                        for lon in range(trends.shape[1]):
                            YDATA_GRIDPOINT = index_values[:, lat, lon]
                            trends[lat,lon] = MedianPairwiseSlopes(XDATA_ANN,YDATA_GRIDPOINT,mdi=False,mult10 = False, sort = False, calc_with_mdi = False)[0]*365*10.

                    GRIDLONS = data.coord('longitude').points
                    GRIDLATS = data.coord('latitude').points
                    trends = np.ma.masked_where(np.isnan(trends), trends)

                    plot_figure(trends, GRIDLONS, GRIDLATS,  'Trend of annually CM SAF ' + INAME, UNITS_DICT, INAME, OUTPATH, REGION)


                #except:
                    #not_working.append(INAME)
print(not_working)





OUTPATH_trends = '/scratch/vportge/plots/Climpact/'+MIN_OR_MAX+'_LST_in_cold_window/'

with open(OUTPATH_trends+'trends_MON_MOROCCO.txt', 'w') as f:
    for key, value in slopes_MON_MOROCCO.items():
        f.write('%s, %s\n' % (key, value))


with open(OUTPATH_trends+'trends_ANN_MOROCCO.txt', 'w') as f:
    for key, value in slopes_ANN_MOROCCO.items():
        f.write('%s, %s\n' % (key, value))

with open(OUTPATH_trends+'trends_MON_SPAIN.txt', 'w') as f:
    for key, value in slopes_MON_SPAIN.items():
        f.write('%s, %s\n' % (key, value))

with open(OUTPATH_trends+'trends_ANN_SPAIN.txt', 'w') as f:
    for key, value in slopes_ANN_SPAIN.items():
        f.write('%s, %s\n' % (key, value))

with open(OUTPATH_trends+'trends_MON_GERMANY.txt', 'w') as f:
    for key, value in slopes_MON_GERMANY.items():
        f.write('%s, %s\n' % (key, value))

with open(OUTPATH_trends+'trends_ANN_GERMANY.txt', 'w') as f:
    for key, value in slopes_ANN_GERMANY.items():
        f.write('%s, %s\n' % (key, value))


