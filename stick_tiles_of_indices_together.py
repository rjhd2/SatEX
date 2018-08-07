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
import datetime
import numpy.ma as ma
import sys
import netCDF4
import iris.plot as iplt
import copy
import iris.coord_categorisation
from plotFunctions import line, plot_figure, MedianPairwiseSlopes, plot_time_series_with_trend



MIN_OR_MAX = 'max'
YEARS = np.arange(1991, 2016)
MONTHS = ["%.2d" % i for i in range(1,13)]

'''
UNITS_DICT = {'CSDI': 'days', 'DTR': u'\u00B0C', 'FD': 'days', 'ID': 'days', 'SU': 'days', 'TN10P': '%', 'tn90p': '%',
              'TNLT2': 'days', 'TNLTM2': 'days', 'TNLTM20': 'days', 'TNm': u'\u00B0C', 'TNn': u'\u00B0C', 'TNx': u'\u00B0C',
              'TR': 'days', 'TX10P': '%', 'TX90P': '%', 'TX95T': u'\u00B0C', 'TXGE30': 'days', 'TXGE35': 'days', 'TXGT50P': '%',
              'TXn': u'\u00B0C', 'TXx': u'\u00B0C', 'WSDI': 'days'}
'''

UNITS_DICT = {'CSDI': 'days', 'DTR': u'\u00B0C', 'FD': 'days', 'ID': 'days', 'SU': 'days', 'TN10p': '%', 'TN90p': '%',
              'TNm': u'\u00B0C', 'TNn': u'\u00B0C', 'TNx': u'\u00B0C', 
              'TR': 'days', 'TX10p': '%', 'TX90p': '%', 'TXn': u'\u00B0C', 'TXx': u'\u00B0C', 'WSDI': 'days' }


python_indices = ['TXx', 'TNx', 'TXn', 'TNn', 'DTR', 'FD', 'TR']


not_working = []
REGIONS = {'SPAIN': [-7.5, 37.5, 0.0, 42.5], 'GERMANY': [5.0, 45.0, 15.0, 50.0], 'MOROCCO': [-5.0, 30.0, 5.0, 35.0]}  #westerly longitude, southerly latitude, easterly longitude, northerly latitude


slopes_ANN_GERMANY = {}
slopes_MON_GERMANY = {}

slopes_ANN_SPAIN = {}
slopes_MON_SPAIN = {}

slopes_ANN_MOROCCO = {}
slopes_MON_MOROCCO = {}

for INAME in python_indices:
    print(INAME)

    if INAME == 'WSDI' or INAME == 'CSDI' or INAME == 'HW': #those are annual indices.
        possible_times = ['ANN']
    elif INAME == 'TX95T':
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


        FPATH = glob.glob('/scratch/vportge/indices/python_created_indices/'+MIN_OR_MAX+'_LST_in_cold_window/*/'+INAME+'*.nc')
        OUTPATH = '/scratch/vportge/plots/Python_Indices/'+MIN_OR_MAX+'_LST_in_cold_window/'+REGION+'/'


        data = iris.load(FPATH)
        #concatenate data so that all tiles are sticked together!
        data = data.concatenate_cube()

        data = data.extract(lat_constraint)
        data = data.extract(lon_constraint)

        data.coord('latitude').guess_bounds()
        data.coord('longitude').guess_bounds()

        cube_name = data.name()
        if UNITS_DICT[INAME] != '%' and UNITS_DICT[INAME] != 'days':
            if INAME != 'DTR':
                data = data - 273.15
                data.rename(cube_name)

        ###############################################################################
        #Add a new time coordinate ('year') so that an annual average can be computed.#
        ###############################################################################
        iris.coord_categorisation.add_year(data, 'time', name='year')
        ann_data = data.aggregated_by('year', iris.analysis.MEAN)
        ann_data.rename(cube_name[:-3]+'ANN' )

        for TIMERANGE in possible_times:
            if TIMERANGE == 'ANN':
                TITLE_TIME = 'annually'
                analyse_data = ann_data

            elif TIMERANGE == 'MON':
                TITLE_TIME = 'monthly'
                analyse_data = data

            elif TIMERANGE == 'DAY':
                TITLE_TIME = 'daily'
                analyse_data = data

            #####################################################################################
            #Plot a time series of spatially averaged values weighted by the area of the gridbox#
            #First: Do spatial average, then: Compute the trend 
            #Is done in function plot_time_series_with_trend#
            #####################################################################################

            print('calculate weights')
            global_mean_areas = iris.analysis.cartography.area_weights(analyse_data)
            print('calculate spatial average')
            global_mean=analyse_data.collapsed(['latitude', 'longitude'], iris.analysis.MEAN, weights=global_mean_areas)
            CUBEINFO = [TITLE_TIME, INAME, REGION, TIMERANGE, OUTPATH, 'CM SAF', 365*10.*24.] 

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
                index_values = ann_data.data
                trends = np.zeros(index_values.shape[1:3]) # lat, lon
                XDATA_ANN = ann_data.coord('time').points #in hours!
                for lat in range(trends.shape[0]):
                    for lon in range(trends.shape[1]):
                        YDATA_GRIDPOINT = index_values[:, lat, lon]
                        trends[lat,lon] = MedianPairwiseSlopes(XDATA_ANN,YDATA_GRIDPOINT,10,mult10 = False, sort = False, calc_with_mdi = False)[0]*365*10.*24.

                GRIDLONS = ann_data.coord('longitude').points
                GRIDLATS = ann_data.coord('latitude').points

                trends = np.ma.masked_where(np.isnan(trends), trends)
                plot_figure(trends, GRIDLONS, GRIDLATS, 'Trend of annually CM SAF ' + INAME, UNITS_DICT, INAME, OUTPATH, REGION)

                    #except:
                        #not_working.append(INAME)
print(not_working)

OUTPATH_trends = '/scratch/vportge/plots/Python_Indices/'+MIN_OR_MAX+'_LST_in_cold_window/'

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

