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
from plotFunctions import line, plot_figure, MedianPairwiseSlopes, plot_time_series_with_trend, plot_map_of_time_average

#INDIR = '/scratch/rdunn/satex/tiles/*/'
INDIR = '/scratch/rdunn/satex/tiles_longer_max_window/*/'
MIN_OR_MAX = 'min'
#Multiply trends by this factor to get trend per decade
TIME_FACTOR = 365*10.

UNITS_DICT = {'csdi': 'days', 'id': 'days', 'su': 'days', 'tn10p': '%', 'tn90p': '%',
              'tnn': u'\u00B0C', 'tnx': u'\u00B0C', 'tx10p': '%', 'tx90p': '%',
              'txn': u'\u00B0C', 'txx': u'\u00B0C', 'wsdi': 'days'}
#UNITS_DICT = {'tx10p': '%'}
#python_indices = ['TXx', 'TNx', 'TXn', 'TNn', 'DTR', 'FD', 'TR']

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

for INAME in UNITS_DICT:
    print(INAME)

    if INAME == 'wsdi' or INAME == 'csdi' or INAME == 'hw': #those are annual indices.
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
        #OUTPATH = '/scratch/vportge/plots/Climpact/'+MIN_OR_MAX+'_LST_in_cold_window/'+REGION+'/'
        OUTPATH = '/scratch/vportge/plots/warm_window_10_3/Climpact/'+MIN_OR_MAX+'_LST_in_cold_window/'+REGION+'/'

        for TIMERANGE in possible_times:
            if TIMERANGE == 'ANN':
                TITLE_TIME = 'annually'
            elif TIMERANGE == 'MON':
                TITLE_TIME = 'monthly'
            elif TIMERANGE == 'DAY':
                TITLE_TIME = 'daily'

            FPATH = glob.glob(INDIR+INAME+'_'+TIMERANGE+'*-'+MIN_OR_MAX+'*.nc')
            #Load in the data for the index and delete 'file_created' attribute.
            data = iris.load(FPATH)
            for i in range(len(data)):
                del data[i].attributes['file_created']

            #concatenate data so that all tiles are sticked together.
            data = data.concatenate_cube()
            #Extract only a subregion of the whole region.
            data = data.extract(lat_constraint)
            data = data.extract(lon_constraint)
        
            #needed for collapsing the data
            data.coord('latitude').guess_bounds()
            data.coord('longitude').guess_bounds()


            #Those indices had problems due to thresholds.
            if INAME not in ['hw', 'tnx', 'txx', 'tx95t', 'tnm', 'tmm']:

                #####################################################################
                #Plot time series of spatially averaged data with trend calculation #
                #####################################################################
                #Compute an area average.
                global_mean_areas = iris.analysis.cartography.area_weights(data)
                global_mean = data.collapsed(['latitude', 'longitude'], iris.analysis.MEAN, weights=global_mean_areas)
                CUBEINFO = [TITLE_TIME, INAME, REGION, TIMERANGE, OUTPATH, 'CM SAF', TIME_FACTOR] 
                slopes = plot_time_series_with_trend(global_mean, CUBEINFO, UNITS_DICT)


                ####################################################
                #Plot map of calculated trends for every gridpoint #
                ####################################################
                if TIMERANGE == 'ANN':
                    index_values = data.data
                    XDATA_ANN = data.coord('time').points
                    TRENDS_ANN = np.zeros(index_values.shape[1:3]) # lat, lon
                    for lat in range(TRENDS_ANN.shape[0]):
                        for lon in range(TRENDS_ANN.shape[1]):
                            YDATA_GRIDPOINT = index_values[:, lat, lon]
                            TRENDS_ANN[lat,lon] = MedianPairwiseSlopes(XDATA_ANN,YDATA_GRIDPOINT)[0]*TIME_FACTOR

                    if data.coord('longitude').has_bounds() == False:
                        data.coord('latitude').guess_bounds()
                        data.coord('longitude').guess_bounds()
                        

                    GRIDLONS = np.append(data.coord('longitude').bounds[:,0], data.coord('longitude').bounds[-1,1])
                    GRIDLATS = np.append(data.coord('latitude').bounds[:,0], data.coord('latitude').bounds[-1,1])
                    TRENDS_ANN = np.ma.masked_where(np.isnan(TRENDS_ANN), TRENDS_ANN)
                    OUTNAME = OUTPATH+INAME+'_map_of_trend_'+REGION+'.png'

                    #save maximum and minimum values of the maps.
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
                    period1 = data.extract(time_constraint1)

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
                    period2 = data.extract(time_constraint2)

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

                    #############################
                    #Plot map of averaged values#
                    #############################
                    CUBEINFO = [TITLE_TIME, INAME, REGION, TIMERANGE, OUTPATH, 'CM SAF', TIME_FACTOR, UNITS_DICT[INAME]]
                    plot_map_of_time_average(data, CUBEINFO)





#OUTPATH_trends = '/scratch/vportge/plots/textfiles_with_cbar_extent/'
OUTPATH_trends = '/scratch/vportge/plots/warm_window_10_3/textfiles_with_cbar_extent/'


with open(OUTPATH_trends+MIN_OR_MAX+'_LST_in_cold_window_CMSAF_climpact_cbar_GERMANY.txt', 'w') as f:
    for key, value in cbar_extent_GERMANY.items():
        f.write('%s, %s\n' % (key, value))

with open(OUTPATH_trends+MIN_OR_MAX+'_LST_in_cold_window_CMSAF_climpact_cbar_SPAIN.txt', 'w') as f:
    for key, value in cbar_extent_SPAIN.items():
        f.write('%s, %s\n' % (key, value))

with open(OUTPATH_trends+MIN_OR_MAX+'_LST_in_cold_window_CMSAF_climpact_cbar_MOROCCO.txt', 'w') as f:
    for key, value in cbar_extent_MOROCCO.items():
        f.write('%s, %s\n' % (key, value))


with open(OUTPATH_trends+MIN_OR_MAX+'_LST_in_cold_window_CMSAF_climpact_cbar_GERMANY_period1.txt', 'w') as f:
    for key, value in cbar_extent_GERMANY_period1.items():
        f.write('%s, %s\n' % (key, value))

with open(OUTPATH_trends+MIN_OR_MAX+'_LST_in_cold_window_CMSAF_climpact_cbar_SPAIN_period1.txt', 'w') as f:
    for key, value in cbar_extent_SPAIN_period1.items():
        f.write('%s, %s\n' % (key, value))

with open(OUTPATH_trends+MIN_OR_MAX+'_LST_in_cold_window_CMSAF_climpact_cbar_MOROCCO_period1.txt', 'w') as f:
    for key, value in cbar_extent_MOROCCO_period1.items():
        f.write('%s, %s\n' % (key, value))


with open(OUTPATH_trends+MIN_OR_MAX+'_LST_in_cold_window_CMSAF_climpact_cbar_GERMANY_period2.txt', 'w') as f:
    for key, value in cbar_extent_GERMANY_period2.items():
        f.write('%s, %s\n' % (key, value))

with open(OUTPATH_trends+MIN_OR_MAX+'_LST_in_cold_window_CMSAF_climpact_cbar_SPAIN_period2.txt', 'w') as f:
    for key, value in cbar_extent_SPAIN_period2.items():
        f.write('%s, %s\n' % (key, value))

with open(OUTPATH_trends+MIN_OR_MAX+'_LST_in_cold_window_CMSAF_climpact_cbar_MOROCCO_period2.txt', 'w') as f:
    for key, value in cbar_extent_MOROCCO_period2.items():
        f.write('%s, %s\n' % (key, value))
