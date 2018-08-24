import numpy as np
import iris
import matplotlib
matplotlib.use('Agg')
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
from plotFunctions import line, plot_figure, MedianPairwiseSlopes, plot_time_series_with_trend, plot_map_of_time_average

#select whether the minimum or the maximum LST in the cold window should be used
MIN_OR_MAX = 'max'
#The trend value coming from the median pairwise trend calculation has to be calculated by this factor to
#derive a trend per decade
TIME_FACTOR = 365*10.*24.

#A dictionary containing all the different indices with their unit.
UNITS_DICT = {'CSDI': 'days', 'DTR': u'\u00B0C', 'FD': 'days', 'ID': 'days', 'SU': 'days',
              'TN10p': '%', 'TN90p': '%', 'TNm': u'\u00B0C', 'TNn': u'\u00B0C', 'TNx': u'\u00B0C', 
              'TR': 'days', 'TX10p': '%', 'TX90p': '%', 'TXn': u'\u00B0C', 'TXx': u'\u00B0C',
              'WSDI': 'days' }

#The indices that were calculated using the python code
python_indices = ['TXx', 'TNx', 'TXn', 'TNn', 'DTR', 'FD', 'TR']
#python_indices = ['TR']

#python_indices = ['TR', 'FD' ]

#This are the extents of the regions which are used for GHCNDEX data:
'''REGIONS = {'SPAIN': [-7.5, 37.5, 0.0, 42.5], 'GERMANY': [5.0, 45.0, 15.0, 50.0], 
'MOROCCO': [-5.0, 30.0, 5.0, 35.0]}  #westerly longitude, southerly latitude, easterly longitude, 
#northerly latitude'''

'''The satellite data has a much higher resolution than the station data. The satellite data has to 
cover the whole region of the station data up to the boundaries of their
gridboxes. This is why the extent of the different regions of the satellite data is a bit higher.
the values correspond to the center values of a gridbox, not to their boundary.
westerly longitude, southerly latitude, easterly longitude, northerly latitude'''
REGIONS = {'SPAIN': [-8.75, 36.25, 1.25, 43.75], 'GERMANY': [5.0-1.25, 45.0-1.25, 15.0+1.25, 50.0+1.25],
           'MOROCCO': [-5.0-1.25, 30.0-1.25, 5.0+1.25, 35.0+1.25]}  

'''cbar_extent_XXX are dictionaries which are used to save the lowest and highest values
of a map which shows the trends in the indices. Those dictionaries are saved to .txt files after plotting
and they can be used to load in the extents (lowest/highest value) when plotting the GHCNDEX data.'''
#for whole time period (1991-2015)
cbar_extent_GERMANY = {}
cbar_extent_MOROCCO = {}
cbar_extent_SPAIN = {}
#for period 1991-2004
cbar_extent_GERMANY_period1 = {}
cbar_extent_MOROCCO_period1 = {}
cbar_extent_SPAIN_period1 = {}
#for period 2005-2015
cbar_extent_GERMANY_period2 = {}
cbar_extent_MOROCCO_period2 = {}
cbar_extent_SPAIN_period2 = {}

for INAME in python_indices:
    print(INAME)

    if INAME == 'WSDI' or INAME == 'CSDI' or INAME == 'HW': #those are annual indices.
        possible_times = ['ANN']

    else:
        possible_times = ['MON', 'ANN']

    for REGION in REGIONS:
        print(REGION)
        #coordinates of the corners of the region
        left_lon = float(REGIONS[REGION][0])
        right_lon = float(REGIONS[REGION][2])
        lower_lat = float(REGIONS[REGION][1])
        upper_lat = float(REGIONS[REGION][3])

        lat_constraint = iris.Constraint(latitude=lambda c: lower_lat <= c.point <= upper_lat)
        lon_constraint = iris.Constraint(longitude=lambda c: left_lon <= c.point <= right_lon)


        #FPATH = glob.glob('/scratch/vportge/indices/python_created_indices/'+MIN_OR_MAX+'_LST_in_cold_window/*/'+INAME+'*.nc')
        #OUTPATH = '/scratch/vportge/plots/Python_Indices/'+MIN_OR_MAX+'_LST_in_cold_window/'+REGION+'/'

        FPATH = glob.glob('/scratch/vportge/indices/python_created_indices/warm_window_10_3/'+MIN_OR_MAX+'_LST_in_cold_window/*/'+INAME+'*.nc')
        OUTPATH = '/scratch/vportge/plots/warm_window_10_3/Python_Indices/'+MIN_OR_MAX+'_LST_in_cold_window/'+REGION+'/'


        #Load in the data for the index.
        data = iris.load(FPATH)
        #concatenate data so that all tiles are sticked together!
        data = data.concatenate_cube()

        #Extract only a subregion of the whole region.
        data = data.extract(lat_constraint)
        data = data.extract(lon_constraint)

        #needed for collapsing the data
        data.coord('latitude').guess_bounds()
        data.coord('longitude').guess_bounds()

        #In case the data is in Kelvin it has to be converted to Degree Celsius. 
        cube_name = data.name()
        if UNITS_DICT[INAME] != '%' and UNITS_DICT[INAME] != 'days':
            if INAME != 'DTR':
                data = data - 273.15
                data.rename(cube_name)

        ###############################################################################
        #Add a new time coordinate ('year') so that an annual average can be computed.#
        ###############################################################################
        iris.coord_categorisation.add_year(data, 'time', name='year')

        #'TXx', 'TNx', 'TXn', 'TNn', 'DTR', 'FD', 'TR'
        if INAME == 'TXx' or INAME == 'TNx':
            #The data of those indices is the maximum value per month. To get the annual value
            #of this index the maximum of the monthly maximum has to be found. 
            ann_data = data.aggregated_by('year', iris.analysis.MAX)

        elif INAME == 'TXn' or INAME == 'TNn':
            #The data of those indices is the minimum value per month. To get the annual value
            #of this index the minimum of the monthly minimum has to be found. 
            ann_data = data.aggregated_by('year', iris.analysis.MIN)

        elif INAME == 'DTR':
            #The data of those indices is the mean value per month. To get the annual value
            #of this index the mean of the monthly mean has to be found. 
            ann_data = data.aggregated_by('year', iris.analysis.MEAN)

        elif INAME == 'FD' or INAME == 'TR':
            #The data of those indices is the number of days per month. To get the annual value
            #of this index the number of days for each month have to be summed up.
            ann_data = data.aggregated_by('year', iris.analysis.SUM)

        ann_data.rename(cube_name[:-3]+'ANN' )

        #Possible are either annual indices or monthly indices
        for TIMERANGE in possible_times:
            if TIMERANGE == 'ANN':
                TITLE_TIME = 'annually'
                analyse_data = ann_data

            elif TIMERANGE == 'MON':
                TITLE_TIME = 'monthly'
                analyse_data = data


            #####################################################################################
            #Plot a time series of spatially averaged values weighted by the area of the gridbox#
            #First: Do spatial average, then: Compute the trend 
            #Is done in function plot_time_series_with_trend#
            #####################################################################################

            global_mean_areas = iris.analysis.cartography.area_weights(analyse_data)
            global_mean=analyse_data.collapsed(['latitude', 'longitude'], iris.analysis.MEAN, weights=global_mean_areas)
            CUBEINFO = [TITLE_TIME, INAME, REGION, TIMERANGE, OUTPATH, 'CM SAF', TIME_FACTOR] 
            slopes = plot_time_series_with_trend(global_mean, CUBEINFO, UNITS_DICT)

            ####################################################
            #Plot map of calculated trends for every gridpoint #
            ####################################################
            if TIMERANGE == 'ANN':
                print('Begin calculation of trends for map')

                index_values = ann_data.data
                TRENDS_ANN = np.zeros(index_values.shape[1:3]) # lat, lon
                XDATA_ANN = ann_data.coord('time').points #in hours!
                for lat in range(TRENDS_ANN.shape[0]):
                    for lon in range(TRENDS_ANN.shape[1]):
                        YDATA_GRIDPOINT = index_values[:, lat, lon]
                        TRENDS_ANN[lat,lon] = MedianPairwiseSlopes(XDATA_ANN,YDATA_GRIDPOINT)[0]*TIME_FACTOR

                if ann_data.coord('longitude').has_bounds() == False:
                    ann_data.coord('latitude').guess_bounds()
                    ann_data.coord('longitude').guess_bounds()

                #for pcolormesh the bounds have to be used. 
                GRIDLONS = np.append(ann_data.coord('longitude').bounds[:,0], ann_data.coord('longitude').bounds[-1,1])
                GRIDLATS = np.append(ann_data.coord('latitude').bounds[:,0], ann_data.coord('latitude').bounds[-1,1])

                TRENDS_ANN = np.ma.masked_where(np.isnan(TRENDS_ANN), TRENDS_ANN)
                OUTNAME = OUTPATH+INAME+'_map_of_trend_'+REGION+'.png'

                FIG_INFO =  ['Trend of annually CM SAF ' + INAME, UNITS_DICT[INAME], OUTPATH, REGION, OUTNAME, False]

                if REGION == 'GERMANY':
                    cbar_extent_GERMANY[INAME] = plot_figure(TRENDS_ANN, GRIDLONS, GRIDLATS, FIG_INFO)

                elif REGION == 'SPAIN':
                    cbar_extent_SPAIN[INAME] = plot_figure(TRENDS_ANN, GRIDLONS, GRIDLATS, FIG_INFO)

                elif REGION == 'MOROCCO':
                    cbar_extent_MOROCCO[INAME] = plot_figure(TRENDS_ANN, GRIDLONS, GRIDLATS, FIG_INFO)

                ###########################################################
                # Calculation for trends for first time period: 1991 -2004#
                ###########################################################

                time_constraint1 = iris.Constraint(time=lambda c: c.point.year < 2005)
                period1 = ann_data.extract(time_constraint1)

                index_values = period1.data
                TRENDS_ANN = np.zeros(period1.shape[1:3]) # lat, lon
                XDATA_ANN = period1.coord('time').points #in hours!
                for lat in range(TRENDS_ANN.shape[0]):
                    for lon in range(TRENDS_ANN.shape[1]):
                        YDATA_GRIDPOINT = index_values[:, lat, lon]
                        TRENDS_ANN[lat,lon] = MedianPairwiseSlopes(XDATA_ANN,YDATA_GRIDPOINT)[0]*TIME_FACTOR

                TRENDS_ANN = np.ma.masked_where(np.isnan(TRENDS_ANN), TRENDS_ANN)
                OUTNAME = OUTPATH+INAME+'_1991-2004_map_of_trend_'+REGION+'.png'

                FIG_INFO =  ['Trend of annually CM SAF ' + INAME +' (1991-2004)', UNITS_DICT[INAME], OUTPATH, REGION, OUTNAME, False]

                if REGION == 'GERMANY':
                    cbar_extent_GERMANY_period1[INAME] = plot_figure(TRENDS_ANN, GRIDLONS, GRIDLATS, FIG_INFO)

                elif REGION == 'SPAIN':
                    cbar_extent_SPAIN_period1[INAME] = plot_figure(TRENDS_ANN, GRIDLONS, GRIDLATS, FIG_INFO)

                elif REGION == 'MOROCCO':
                    cbar_extent_MOROCCO_period1[INAME] = plot_figure(TRENDS_ANN, GRIDLONS, GRIDLATS, FIG_INFO)




                #begin Calculation for trends for first time period: 1991 -2004
                time_constraint2 = iris.Constraint(time=lambda c: c.point.year > 2004)
                period2 = ann_data.extract(time_constraint2)


                index_values = period2.data
                TRENDS_ANN = np.zeros(period2.shape[1:3]) # lat, lon
                XDATA_ANN = period2.coord('time').points #in hours!
                for lat in range(TRENDS_ANN.shape[0]):
                    for lon in range(TRENDS_ANN.shape[1]):
                        YDATA_GRIDPOINT = index_values[:, lat, lon]
                        TRENDS_ANN[lat,lon] = MedianPairwiseSlopes(XDATA_ANN,YDATA_GRIDPOINT)[0]*TIME_FACTOR

                TRENDS_ANN = np.ma.masked_where(np.isnan(TRENDS_ANN), TRENDS_ANN)
                OUTNAME = OUTPATH+INAME+'_2005-2015_map_of_trend_'+REGION+'.png'
                FIG_INFO =  ['Trend of annually CM SAF ' + INAME +' (2005-2015)', UNITS_DICT[INAME], OUTPATH, REGION, OUTNAME, False]

                if REGION == 'GERMANY':
                    cbar_extent_GERMANY_period2[INAME] = plot_figure(TRENDS_ANN, GRIDLONS, GRIDLATS, FIG_INFO)

                elif REGION == 'SPAIN':
                    cbar_extent_SPAIN_period2[INAME] = plot_figure(TRENDS_ANN, GRIDLONS, GRIDLATS, FIG_INFO)

                elif REGION == 'MOROCCO':
                    cbar_extent_MOROCCO_period2[INAME] = plot_figure(TRENDS_ANN, GRIDLONS, GRIDLATS, FIG_INFO)


                #Plot map of averaged values
                CUBEINFO = [TITLE_TIME, INAME, REGION, TIMERANGE, OUTPATH, 'CM SAF', TIME_FACTOR, UNITS_DICT[INAME]]
                plot_map_of_time_average(ann_data, CUBEINFO)



#OUTPATH_trends = '/scratch/vportge/plots/textfiles_with_cbar_extent/'
OUTPATH_trends = '/scratch/vportge/plots/warm_window_10_3/textfiles_with_cbar_extent/'



with open(OUTPATH_trends+MIN_OR_MAX+'_LST_in_cold_window_CMSAF_python_cbar_GERMANY.txt', 'w') as f:
    for key, value in cbar_extent_GERMANY.items():
        f.write('%s, %s\n' % (key, value))

with open(OUTPATH_trends+MIN_OR_MAX+'_LST_in_cold_window_CMSAF_python_cbar_SPAIN.txt', 'w') as f:
    for key, value in cbar_extent_SPAIN.items():
        f.write('%s, %s\n' % (key, value))

with open(OUTPATH_trends+MIN_OR_MAX+'_LST_in_cold_window_CMSAF_python_cbar_MOROCCO.txt', 'w') as f:
    for key, value in cbar_extent_MOROCCO.items():
        f.write('%s, %s\n' % (key, value))


with open(OUTPATH_trends+MIN_OR_MAX+'_LST_in_cold_window_CMSAF_python_cbar_GERMANY_period1.txt', 'w') as f:
    for key, value in cbar_extent_GERMANY_period1.items():
        f.write('%s, %s\n' % (key, value))

with open(OUTPATH_trends+MIN_OR_MAX+'_LST_in_cold_window_CMSAF_python_cbar_SPAIN_period1.txt', 'w') as f:
    for key, value in cbar_extent_SPAIN_period1.items():
        f.write('%s, %s\n' % (key, value))

with open(OUTPATH_trends+MIN_OR_MAX+'_LST_in_cold_window_CMSAF_python_cbar_MOROCCO_period1.txt', 'w') as f:
    for key, value in cbar_extent_MOROCCO_period1.items():
        f.write('%s, %s\n' % (key, value))


with open(OUTPATH_trends+MIN_OR_MAX+'_LST_in_cold_window_CMSAF_python_cbar_GERMANY_period2.txt', 'w') as f:
    for key, value in cbar_extent_GERMANY_period2.items():
        f.write('%s, %s\n' % (key, value))

with open(OUTPATH_trends+MIN_OR_MAX+'_LST_in_cold_window_CMSAF_python_cbar_SPAIN_period2.txt', 'w') as f:
    for key, value in cbar_extent_SPAIN_period2.items():
        f.write('%s, %s\n' % (key, value))

with open(OUTPATH_trends+MIN_OR_MAX+'_LST_in_cold_window_CMSAF_python_cbar_MOROCCO_period2.txt', 'w') as f:
    for key, value in cbar_extent_MOROCCO_period2.items():
        f.write('%s, %s\n' % (key, value))