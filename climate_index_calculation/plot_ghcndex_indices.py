# -*- coding: iso-8859-1 -*-
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as mpl_cm
import iris
import iris.quickplot as qplt
import iris.plot as iplt
from iris.util import unify_time_units
import cartopy.crs as ccrs
import cartopy.feature as cfeat
import glob
import copy
import datetime
import netCDF4
import cf_units
from plotFunctions import line, plot_figure, MedianPairwiseSlopes, open_file_with_cbar_extents, plot_map_of_time_average


UNITS_DICT = {'CSDI': 'days', 'DTR': u'\u00B0C', 'FD': 'days', 'ID': 'days', 'SU': 'days',
              'TN10p': '%', 'TN90p': '%', 'TNn': u'\u00B0C', 'TNx': u'\u00B0C', 'TR': 'days',
              'TX10p': '%', 'TX90p': '%', 'TXn': u'\u00B0C', 'TXx': u'\u00B0C', 'WSDI': 'days' }
#'HW': 'days', 'TMGE10': 'days', 'TMGE5': 'days', 'TMLT10': 'days', 'TMLT10': 'days', 'TMm': u'\u00B0C','TMLT5': 'days', 'TX95T': u'\u00B0C', 'TXGE30': 'days', 'TXGE35': 'days', 'TXGT50P': '%',
#'TNLT2': 'days', 'TNLTM2': 'days', 'TNLTM20': 'days',
# gibt es, aber nicht bei climpact:  'GSL': 'days',
#UNITS_DICT = {'CSDI': 'days'}

#List of the indices which were calculated using python/climpact
python_indices = ['TXx', 'TNx', 'TXn', 'TNn', 'DTR', 'FD', 'TR']
climpact_indices = ['CSDI', 'ID', 'SU', 'TN10p', 'TN90p', 'TX10p', 'TX90p', 'WSDI']


REGIONS = {'SPAIN': [-7.5, 37.5, 0.0, 42.5], 'GERMANY': [5.0, 45.0, 15.0, 50.0], 'MOROCCO': [-5.0, 30.0, 5.0, 35.0]}  #westerly longitude, southerly latitude, easterly longitude, northerly latitude

TIME_FACTOR = 365*10.

cbar_extent_GERMANY = {}
cbar_extent_MOROCCO = {}
cbar_extent_SPAIN = {}

for INAME in UNITS_DICT.keys():
    print(INAME)
    ######################################################################################
    #load in data with constraints to correct region defined by longitudes and latitudes #
    ######################################################################################

    #INAME='TXx' #Decide which index should be used:
    filepath='/project/hadobs2/hadex3/ghcndex/GHCND_'+INAME+'_1951-2018_RegularGrid_global_2.5x2.5deg_LSmask.nc'
    time_constraint = iris.Constraint(time=lambda c: 20160101 > c.point > 19910100)
    #longitude_constraint = iris.Constraint(longitude=lambda c: 0<=c.point<=60 or 360.>=c.point>=342)
    latitude_constraint = iris.Constraint(latitude=lambda c: 22< c.point<60) 


    '''
    original_data = original_data.extract(latitude_constraint)
    data = iris.cube.CubeList()
    for i in range(len(original_data)):
        #cube.intersection changes longitudes from 0-360 degree to -180 - +180 degree. 
        data.append(original_data[i].intersection(longitude=(-18, 60)))
    '''


    for REGION in REGIONS:
        print(REGION)
        OUTPATH = '/scratch/vportge/plots/GHCNDEX/'+REGION+'/'

        original_data=iris.load(filepath, time_constraint) #Data has name of the months. 
        if len(original_data) == 0:
            print(INAME)
            continue



        left_lon = float(REGIONS[REGION][0])
        right_lon = float(REGIONS[REGION][2])
        lower_lat = float(REGIONS[REGION][1])
        upper_lat = float(REGIONS[REGION][3])

        lat_constraint = iris.Constraint(latitude=lambda c: lower_lat <= c.point <= upper_lat)
        #lon_constraint = iris.Constraint(longitude=lambda c: left_lon <= c.point <= right_lon)


        original_data = original_data.extract(lat_constraint)

        data = iris.cube.CubeList()
        for i in range(len(original_data)):
            #cube.intersection changes longitudes from 0-360 degree to -180 - +180 degree. 
            data.append(original_data[i].intersection(longitude=(left_lon, right_lon)))



        ######################################################################################
        #Change time coordinate of data as it only contains the month via .name() of the cube#
        ######################################################################################

        spat_avg_month = iris.cube.CubeList()

        for i in range(len(data)):
            month_data = data[i]
            month_time = month_data.coord('time')
            month_datetime = []

            for j in range(len(month_time.points)):
                yyyy = datetime.datetime.strptime(str(int(month_time.points[j])), '%Y%m%d').year
                if month_data.name() == 'Ann':
                    mm = '01'
                elif month_data.name() == 'Jan':
                    mm = '01'
                elif month_data.name() == 'Feb':
                    mm = '02'
                elif month_data.name() == 'Mar':
                    mm = '03'
                elif month_data.name() == 'Apr':
                    mm = '04'
                elif month_data.name() == 'May':
                    mm = '05'
                elif month_data.name() == 'Jun':
                    mm = '06'
                elif month_data.name() == 'Jul':
                    mm = '07'
                elif month_data.name() == 'Aug':
                    mm = '08'
                elif month_data.name() == 'Sep':
                    mm = '09'
                elif month_data.name() == 'Oct':
                    mm = '10'
                elif month_data.name() == 'Nov':
                    mm = '11'
                elif month_data.name() == 'Dec':
                    mm = '12'
                month_datetime.append(datetime.datetime.strptime(str(yyyy)+str(mm)+'01', '%Y%m%d'))


            times_nums_units = netCDF4.date2num(month_datetime, units = 'days since 1970-01-01 00:00', calendar = 'standard')
            time_unit = cf_units.Unit( 'days since 1970-01-01 00:00', calendar='standard')
            new_timecoord = iris.coords.DimCoord(times_nums_units, standard_name = 'time', units = time_unit, var_name = "time") 
            month_data.remove_coord('time')
            month_data.add_dim_coord(new_timecoord,0)
            #calculate spatial average#
            if month_data.name() == 'Ann':
                ANN_data = copy.deepcopy(month_data)
                #calculate spatial average#
                ANN_data.coord('latitude').guess_bounds()
                ANN_data.coord('longitude').guess_bounds()
                ANN_data_areas = iris.analysis.cartography.area_weights(ANN_data)

                ANN_data_avg = ANN_data.collapsed(['latitude', 'longitude'], iris.analysis.MEAN, weights=ANN_data_areas)
                #ANN_data_avg = ANN_data_avg.collapsed('longitude', iris.analysis.MEAN)
                ANN_index = i*1.

            else:
                month_data.coord('latitude').guess_bounds()
                month_data.coord('longitude').guess_bounds()

                month_data_areas = iris.analysis.cartography.area_weights(month_data)

                month_avg = month_data.collapsed(['latitude', 'longitude'], iris.analysis.MEAN, weights=month_data_areas)
                #month_avg = month_avg.collapsed('longitude', iris.analysis.MEAN)
                spat_avg_month.append(month_avg)
        del(data[int(ANN_index)])





        #######################################################################################
        #cubelist.concatenate_cube() doesn't work so get the values and save them into a list.#
        #Leading to a list consisting of 12 lists (one for each month.) Sort the dates so that#
        #a time series can be plotted. times_spat_avg are the sorted dates (as numbers) and   #
        #values_spat_avg are the corresponding values of the index. (Spatially averaged!).    #
        #######################################################################################


        if len(original_data)>1:
            times_spat_avg = []
            values_spat_avg = []

            for i in spat_avg_month:
                time_month = i.coord('time')
                times_spat_avg.append(time_month.points)
                values_spat_avg.append(i.data)
            #flatten the lists
            times_spat_avg = [item for sublist in times_spat_avg for item in sublist]
            values_spat_avg = [item for sublist in values_spat_avg for item in sublist]
            #sort list by time coordinate
            times_spat_avg, values_spat_avg = (list(t) for t in zip(*sorted(zip(times_spat_avg, values_spat_avg))))


        ###################################################################
        #Plot map of averaged values over whole time period using ANN_data#
        ###################################################################
        '''
        plt.close()
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        #ax.set_extent([ -30., 65., 30, 65. ], crs=ccrs.PlateCarree())

        ANN_data.coord('time').guess_bounds()

        ANN_data_time_avg = ANN_data.collapsed('time', iris.analysis.MEAN)
        ANN_data_lon = ANN_data_time_avg.coord('longitude').points
        ANN_data_lat = ANN_data_time_avg.coord('latitude').points

        cont = iplt.pcolormesh(ANN_data_time_avg, cmap = 'CMRmap')


        ax.set_extent((np.amin(ANN_data_lon)-2, np.amax(ANN_data_lon)+2, np.amin(ANN_data_lat)-2, np.amax(ANN_data_lat)+2), crs = ccrs.PlateCarree())

        political_bdrys = cfeat.NaturalEarthFeature(category='cultural',
                                                    name='admin_0_countries',
                                                    scale='50m')
        ax.add_feature(political_bdrys, edgecolor='b', facecolor='none', zorder=2)
        cb=fig.colorbar(cont, ax=ax, orientation='horizontal')
        cb.set_label(INAME+' Index Value')
        plt.title('Map of averaged '+INAME+' values (GHCNDEX)')
        plt.savefig(OUTPATH+INAME+'_GHCNDEX_map_averaged_'+REGION+'.png')
        '''
        ########################################################
        #Plot time series of years 1991 - 2015 with trend line #
        ########################################################
        if len(original_data)>1: #Then it's monthly data.
            plt.close()
            YDATA = values_spat_avg
            XDATA = times_spat_avg
            #convert to datetime object so that it can be plotted easily.
            times_datetime = [netCDF4.num2date(i, units = 'days since 1970-01-01 00:00', calendar = 'standard') for i in times_spat_avg]

            trendanalysis = MedianPairwiseSlopes(XDATA,YDATA)
            slope = trendanalysis[0]
            slope_lower_uncrty = trendanalysis[1]
            slope_upper_uncrty = trendanalysis[2]
            Y_INTERCEPTION = trendanalysis[3]

            trendline=line(np.array(XDATA), np.array(Y_INTERCEPTION), slope)

            fig = plt.figure(figsize = (10, 8))
            plt.plot(times_datetime, YDATA)
            plt.plot(times_datetime, trendline, label='trend: '+str(round(slope*TIME_FACTOR,2))+ ' ' + UNITS_DICT[INAME]+' per decade')
            plt.grid()
            plt.title('Time series of monthly GHCNDEX ' + INAME + ' in ' + REGION , size=22)
            plt.xlabel('years', size=20)
            plt.ylabel(UNITS_DICT[INAME], size=20)

            plt.legend(fontsize = 16)
            plt.tight_layout()
            plt.tick_params(axis='both', which='major', labelsize=16)
            plt.savefig(OUTPATH+INAME+'_time_series_GHCNDEX_with_trend_monthly_'+REGION+'.png')





        YDATA = ANN_data_avg.data
        XDATA = ANN_data_avg.coord('time').points
        #convert to datetime object so that it can be plotted easily.
        times_datetime = [netCDF4.num2date(i, units = 'days since 1970-01-01 00:00', calendar = 'standard') for i in ANN_data_avg.coord('time').points]

        YDATA1 = YDATA[0:14]
        YDATA2 = YDATA[14:]
        XDATA1 = XDATA[0:14]
        XDATA2 = XDATA[14:]
        times_datetime1 = times_datetime[0:14]
        times_datetime2 = times_datetime[14:]




        trendanalysis = MedianPairwiseSlopes(XDATA,YDATA)
        slope = trendanalysis[0]
        Y_INTERCEPTION = trendanalysis[3]


        trendanalysis1 = MedianPairwiseSlopes(XDATA1,YDATA1)
        slope1 = trendanalysis1[0]
        Y_INTERCEPTION1 = trendanalysis1[3]

        trendanalysis2 = MedianPairwiseSlopes(XDATA2,YDATA2)
        slope2 = trendanalysis2[0]
        Y_INTERCEPTION2 = trendanalysis2[3]


        trendline=line(np.array(XDATA), np.array(Y_INTERCEPTION), slope)
        trendline1=line(np.array(XDATA1), np.array(Y_INTERCEPTION1), slope1)
        trendline2=line(np.array(XDATA2), np.array(Y_INTERCEPTION2), slope2)


        plt.close()
        fig=plt.figure(figsize = (10, 8))
        plt.plot(times_datetime, YDATA)
        plt.plot(times_datetime, trendline, label='trend: '+str(round(slope*TIME_FACTOR,2))+ ' ' + UNITS_DICT[INAME]+' per decade'+ ' (1991-2015)')
        plt.plot(times_datetime1, trendline1, label='trend: '+str(round(slope1*TIME_FACTOR,2))+ ' ' + UNITS_DICT[INAME]+' per decade'+ ' (1991-2004)')
        plt.plot(times_datetime2, trendline2, label='trend: '+str(round(slope2*TIME_FACTOR,2))+ ' ' + UNITS_DICT[INAME]+' per decade'+ ' (2005-2015)')

        plt.grid()
        plt.title('Time series of annually GHCNDEX ' + INAME + ' in ' + REGION , size=22)
        plt.xlabel('years', size=20)
        plt.ylabel(UNITS_DICT[INAME], size=20)

        plt.legend(fontsize = 16)
        plt.tight_layout()
        plt.tick_params(axis='both', which='major', labelsize=16)
        plt.savefig(OUTPATH+INAME+'_time_series_GHCNDEX_with_trend_annually_'+REGION+'.png')



        #####################################################
        #Plot map of trend for each gridpoint using ANN_data#
        #####################################################
        min_or_max = ['min', 'max']

        for cold_win in min_or_max:

            '''Read in the files which contain the lowest and highest values of CLIMPACT/PYTHON created indices.
               Those values can be used to set the extent of the GHCNDEX plots so that the colorbars show the same range.'''
            cbar_path_python = '/scratch/vportge/plots/textfiles_with_cbar_extent/'+cold_win+'_LST_in_cold_window_CMSAF_python_cbar_'+REGION+'.txt'
            cbar_path_climpact = '/scratch/vportge/plots/textfiles_with_cbar_extent/'+cold_win+'_LST_in_cold_window_CMSAF_climpact_cbar_'+REGION+'.txt'

            cbar_dict_python = open_file_with_cbar_extents(cbar_path_python)
            cbar_dict_climpact = open_file_with_cbar_extents(cbar_path_climpact)

            #Pcolormesh will be used for plotting which uses the boundarie points.
            GRIDLONS = np.append(ANN_data.coord('longitude').bounds[:,0], ANN_data.coord('longitude').bounds[-1,1])
            GRIDLATS = np.append(ANN_data.coord('latitude').bounds[:,0], ANN_data.coord('latitude').bounds[-1,1])
            TRENDS_ANN = np.ma.zeros(ANN_data.shape[1:3]) # lat, lon
            XDATA_ANN = ANN_data.coord('time').points

            for lat in range(ANN_data.shape[1]):
                for lon in range(ANN_data.shape[2]):
                    YDATA_GRIDPOINT = ANN_data[:, lat, lon]
                    TRENDS_ANN[lat,lon] = MedianPairwiseSlopes(XDATA_ANN,YDATA_GRIDPOINT.data)[0]*TIME_FACTOR

            TRENDS_ANN = np.ma.masked_where(np.isnan(TRENDS_ANN), TRENDS_ANN)
            OUTNAME = OUTPATH+INAME+'_map_of_trend_'+REGION+'_'+cold_win+'.png'

            if INAME in python_indices:
                FIG_INFO =  ['Trend of annually GHCNDEX ' + INAME , UNITS_DICT[INAME], OUTPATH, REGION, OUTNAME, cbar_dict_python[INAME]]

                if REGION == 'GERMANY':
                    cbar_extent_GERMANY[INAME] = plot_figure(TRENDS_ANN, GRIDLONS, GRIDLATS, FIG_INFO)

                elif REGION == 'SPAIN':
                    cbar_extent_SPAIN[INAME] = plot_figure(TRENDS_ANN, GRIDLONS, GRIDLATS, FIG_INFO)

                elif REGION == 'MOROCCO':
                    cbar_extent_MOROCCO[INAME] = plot_figure(TRENDS_ANN, GRIDLONS, GRIDLATS, FIG_INFO)

            elif INAME in climpact_indices:
                FIG_INFO =  ['Trend of annually GHCNDEX ' + INAME , UNITS_DICT[INAME], OUTPATH, REGION, OUTNAME, cbar_dict_climpact[INAME.lower()]]
                if REGION == 'GERMANY':
                    cbar_extent_GERMANY[INAME] = plot_figure(TRENDS_ANN, GRIDLONS, GRIDLATS, FIG_INFO)

                elif REGION == 'SPAIN':
                    cbar_extent_SPAIN[INAME] = plot_figure(TRENDS_ANN, GRIDLONS, GRIDLATS, FIG_INFO)

                elif REGION == 'MOROCCO':
                    cbar_extent_MOROCCO[INAME] = plot_figure(TRENDS_ANN, GRIDLONS, GRIDLATS, FIG_INFO)


            else:
                FIG_INFO =  ['Trend of annually GHCNDEX ' + INAME , UNITS_DICT[INAME], OUTPATH, REGION, OUTNAME, False]
                plot_figure(TRENDS_ANN, GRIDLONS, GRIDLATS, FIG_INFO)



            ################################################################
            #begin Calculation for trends for first time period: 1991 -2004#
            ################################################################
            cbar_path_python = '/scratch/vportge/plots/textfiles_with_cbar_extent/'+cold_win+'_LST_in_cold_window_CMSAF_python_cbar_'+REGION+'_period1.txt'
            cbar_path_climpact = '/scratch/vportge/plots/textfiles_with_cbar_extent/'+cold_win+'_LST_in_cold_window_CMSAF_climpact_cbar_'+REGION+'_period1.txt'

            cbar_dict_python = open_file_with_cbar_extents(cbar_path_python)
            cbar_dict_climpact = open_file_with_cbar_extents(cbar_path_climpact)

            TRENDS_ANN = np.ma.zeros(ANN_data.shape[1:3]) # lat, lon
            XDATA_ANN = ANN_data.coord('time').points[0:14]
            for lat in range(ANN_data.shape[1]):
                for lon in range(ANN_data.shape[2]):
                    YDATA_GRIDPOINT = ANN_data[0:14, lat, lon]
                    TRENDS_ANN[lat,lon] = MedianPairwiseSlopes(XDATA_ANN,YDATA_GRIDPOINT.data)[0]*TIME_FACTOR

            TRENDS_ANN = np.ma.masked_where(np.isnan(TRENDS_ANN), TRENDS_ANN)
            OUTNAME = OUTPATH+INAME+'_1991-2004_map_of_trend_'+REGION+'_'+cold_win+'.png'

            if INAME in python_indices:
                FIG_INFO =  ['Trend of annually GHCNDEX ' + INAME +' (1991-2004)', UNITS_DICT[INAME], OUTPATH, REGION, OUTNAME, cbar_dict_python[INAME]] 
                plot_figure(TRENDS_ANN, GRIDLONS, GRIDLATS, FIG_INFO)

            elif INAME in climpact_indices:
                FIG_INFO =  ['Trend of annually GHCNDEX ' + INAME +' (1991-2004)', UNITS_DICT[INAME], OUTPATH, REGION, OUTNAME, cbar_dict_climpact[INAME.lower()]]
                plot_figure(TRENDS_ANN, GRIDLONS, GRIDLATS, FIG_INFO)

            else:
                FIG_INFO =  ['Trend of annually GHCNDEX ' + INAME +' (1991-2004)', UNITS_DICT[INAME], OUTPATH, REGION, OUTNAME, False]
                plot_figure(TRENDS_ANN, GRIDLONS, GRIDLATS, FIG_INFO)

            ################################################################
            #begin Calculation for trends for second time period: 2005-2015#
            ################################################################
            cbar_path_python = '/scratch/vportge/plots/textfiles_with_cbar_extent/'+cold_win+'_LST_in_cold_window_CMSAF_python_cbar_'+REGION+'_period2.txt'
            cbar_path_climpact = '/scratch/vportge/plots/textfiles_with_cbar_extent/'+cold_win+'_LST_in_cold_window_CMSAF_climpact_cbar_'+REGION+'_period2.txt'

            cbar_dict_python = open_file_with_cbar_extents(cbar_path_python)
            cbar_dict_climpact = open_file_with_cbar_extents(cbar_path_climpact)

            TRENDS_ANN = np.ma.zeros(ANN_data.shape[1:3]) # lat, lon
            XDATA_ANN = ANN_data.coord('time').points[14:]
            for lat in range(ANN_data.shape[1]):
                for lon in range(ANN_data.shape[2]):
                    YDATA_GRIDPOINT = ANN_data[14:, lat, lon]
                    TRENDS_ANN[lat,lon] = MedianPairwiseSlopes(XDATA_ANN,YDATA_GRIDPOINT.data)[0]*TIME_FACTOR

            TRENDS_ANN = np.ma.masked_where(np.isnan(TRENDS_ANN), TRENDS_ANN)
            OUTNAME = OUTPATH+INAME+'_2005-2015_map_of_trend_'+REGION+'_'+cold_win+'.png'


            if INAME in python_indices:
                FIG_INFO =  ['Trend of annually GHCNDEX ' + INAME +' (2005-2015)', UNITS_DICT[INAME], OUTPATH, REGION, OUTNAME, cbar_dict_python[INAME]] 
                plot_figure(TRENDS_ANN, GRIDLONS, GRIDLATS, FIG_INFO)

            elif INAME in climpact_indices:
                FIG_INFO =  ['Trend of annually GHCNDEX ' + INAME +' (2005-2015)', UNITS_DICT[INAME], OUTPATH, REGION, OUTNAME, cbar_dict_climpact[INAME.lower()]]
                plot_figure(TRENDS_ANN, GRIDLONS, GRIDLATS, FIG_INFO)

            else:
                FIG_INFO =  ['Trend of annually GHCNDEX ' + INAME +' (2005-2015)', UNITS_DICT[INAME], OUTPATH, REGION, OUTNAME, False]
                plot_figure(TRENDS_ANN, GRIDLONS, GRIDLATS, FIG_INFO)

            #Plot map of averaged values
            CUBEINFO = ['annually', INAME, REGION, 'ANN', OUTPATH, 'GHCNDEX', TIME_FACTOR, UNITS_DICT[INAME]]
            plot_map_of_time_average(ANN_data, CUBEINFO)



OUTPATH_trends = '/scratch/vportge/plots/GHCNDEX/'

with open(OUTPATH_trends+'cbar_GERMANY.txt', 'w') as f:
    for key, value in cbar_extent_GERMANY.items():
        f.write('%s, %s\n' % (key, value))

with open(OUTPATH_trends+'cbar_SPAIN.txt', 'w') as f:
    for key, value in cbar_extent_SPAIN.items():
        f.write('%s, %s\n' % (key, value))

with open(OUTPATH_trends+'cbar_MOROCCO.txt', 'w') as f:
    for key, value in cbar_extent_MOROCCO.items():
        f.write('%s, %s\n' % (key, value))

