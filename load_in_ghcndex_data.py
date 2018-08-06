# -*- coding: iso-8859-1 -*-
import numpy as np
import iris
import matplotlib.pyplot as plt
import iris.quickplot as qplt
import matplotlib.cm as mpl_cm
import iris.plot as iplt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import glob
import iris
from iris.util import unify_time_units
import numpy as np
import matplotlib.pyplot as plt
import iris.quickplot as qplt
import matplotlib.cm as mpl_cm
import iris.plot as iplt
import cartopy.crs as ccrs
import copy
import datetime
import netCDF4
import cf_units

def line(x,t,m):
    '''Plot a line. '''
    return m*x+t


def plot_figure(data, gridlons, gridlats, title):
    """Plot map of index for some day."""
    plt.close()
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    lst_map = plt.pcolormesh(gridlons, gridlats, data, transform=ccrs.PlateCarree(), cmap = 'RdBu_r')
    cbar = plt.colorbar(lst_map, orientation='horizontal', extend='both')
    ax.coastlines()
    gl = ax.gridlines(draw_labels=True)
    plt.title(title, y=1.08, size=22)
    cbar.set_label(UNITS_DICT[indexname]+' per decade', size=20)
    plt.tight_layout()
    plt.savefig(OUTPATH+indexname+'_map_of_trend_'+REGION+'png')
    return

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

    mpw=np.ma.median(np.ma.array(slopes))
    y_intercept_point = np.ma.median(np.array(y_intercepts))

    # copied from median_pairwise.pro methodology (Mark McCarthy)
    slopes.sort()

    if calc_with_mdi == True:
        good_data = np.where(mdi == False)#good_data=np.where(ydata == False)[0]
        n=len(ydata[good_data])

    elif calc_with_mdi == False:
        n=len(ydata)

    try:

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

    except:
        if mult10:
            return 10. * mpw, 'test', 'test', y_intercept_point      # MedianPairwiseSlopes
        else:
            return  mpw, 'test', 'test', y_intercept_point      # MedianPairwiseSlopes



UNITS_DICT = {'CSDI': 'days', 'DTR': u'\u00B0C', 'FD': 'days', 'ID': 'days', 'SU': 'days', 'TN10p': '%', 'TN90p': '%',
              'TNm': u'\u00B0C', 'TNn': u'\u00B0C', 'TNx': u'\u00B0C', 
              'TR': 'days', 'TX10p': '%', 'TX90p': '%', 'TXn': u'\u00B0C', 'TXx': u'\u00B0C', 'WSDI': 'days' }
#'HW': 'days', 'TMGE10': 'days', 'TMGE5': 'days', 'TMLT10': 'days', 'TMLT10': 'days', 'TMm': u'\u00B0C','TMLT5': 'days', 'TX95T': u'\u00B0C', 'TXGE30': 'days', 'TXGE35': 'days', 'TXGT50P': '%',
#'TNLT2': 'days', 'TNLTM2': 'days', 'TNLTM20': 'days',
# gibt es, aber nicht bei climpact:  'GSL': 'days',
#UNITS_DICT = {'CSDI': 'days'}

REGIONS = {'SPAIN': [-7.5, 37.5, 0.0, 42.5], 'GERMANY': [5.0, 47.5, 15.0, 52.5], 'MOROCCO': [-5.0, 30.0, 5.0, 35.0]}  #westerly longitude, southerly latitude, easterly longitude, northerly latitude


for indexname in UNITS_DICT.keys():
    print(indexname)
    ######################################################################################
    #load in data with constraints to correct region defined by longitudes and latitudes #
    ######################################################################################

    #indexname='TXx' #Decide which index should be used:
    filepath='/project/hadobs2/hadex3/ghcndex/GHCND_'+indexname+'_1951-2018_RegularGrid_global_2.5x2.5deg_LSmask.nc'
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
            print(indexname)
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
                ANN_data_avg=ANN_data.collapsed('latitude', iris.analysis.MEAN)
                ANN_data_avg=ANN_data_avg.collapsed('longitude', iris.analysis.MEAN)
                ANN_index = i*1.

            else:
                month_avg=month_data.collapsed('latitude', iris.analysis.MEAN)
                month_avg=month_avg.collapsed('longitude', iris.analysis.MEAN)
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

        plt.close()
        fig = plt.figure(figsize=(10, 5))
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        #ax.set_extent([ -30., 65., 30, 65. ], crs=ccrs.PlateCarree())
        cont = iplt.pcolormesh(ANN_data.collapsed('time', iris.analysis.MEAN), cmap = 'CMRmap')
        ax.coastlines()
        cb=fig.colorbar(cont, ax=ax, orientation='horizontal')
        cb.set_label(indexname+' Index Value')
        plt.title('Map of averaged '+indexname+' values (GHCNDEX) '+REGION)
        plt.savefig(OUTPATH+indexname+'_GHCNDEX_map_averaged_'+REGION+'.png')

        #########################################
        #Plot years 1991 - 2015 with trend line #
        #########################################
        if len(original_data)>1:
            plt.close()
            YDATA = values_spat_avg
            XDATA = times_spat_avg
            #convert to datetime object so that it can be plotted easily.
            times_datetime = [netCDF4.num2date(i, units = 'days since 1970-01-01 00:00', calendar = 'standard') for i in times_spat_avg]

            trendanalysis = MedianPairwiseSlopes(XDATA,YDATA,10,mult10 = False, sort = False, calc_with_mdi=False)
            slope = trendanalysis[0]
            slope_lower_uncrty = trendanalysis[1]
            slope_upper_uncrty = trendanalysis[2]
            Y_INTERCEPTION = trendanalysis[3]


            trendline=line(np.array(XDATA), np.array(Y_INTERCEPTION), slope)
            plt.plot(times_datetime, YDATA)
            plt.plot(times_datetime, trendline, label='trend: '+str(round(slope*365*10.,2))+ ' ' + UNITS_DICT[indexname]+' per decade')
            plt.grid()
            plt.title(indexname + ' GHCNDEX '+REGION, size=22)
            plt.xlabel('years', size=20)
            plt.ylabel(UNITS_DICT[indexname], size=20)

            plt.legend(fontsize = 16)
            plt.tight_layout()
            plt.tick_params(axis='both', which='major', labelsize=16)
            plt.savefig(OUTPATH+indexname+'_GHCNDEX_with_trend_'+REGION+'png')



        #####################################################
        #Plot map of trend for each gridpoint using ANN_data#
        #####################################################
        GRIDLONS = ANN_data.coord('longitude').points
        GRIDLATS = ANN_data.coord('latitude').points
        TRENDS_ANN = np.ma.zeros(ANN_data.shape[1:3]) # lat, lon
        XDATA_ANN = ANN_data.coord('time').points

        for lat in range(len(GRIDLATS)):
            for lon in range(len(GRIDLONS)):

                YDATA_GRIDPOINT = ANN_data[:, lat, lon]
                if np.isnan(YDATA_GRIDPOINT.data).any() == False:
                    #no missing values
                    TRENDS_ANN[lat,lon] = MedianPairwiseSlopes(XDATA_ANN,YDATA_GRIDPOINT.data,10,mult10 = False, sort = False, calc_with_mdi = False)[0]*365*10.

                else:
                    MDI = YDATA_GRIDPOINT.data.mask
                    TRENDS_ANN[lat,lon] = MedianPairwiseSlopes(XDATA_ANN,YDATA_GRIDPOINT.data,MDI,mult10 = False, sort = False, calc_with_mdi = True)[0]*365*10.

        TRENDS_ANN = np.ma.masked_where(np.isnan(TRENDS_ANN), TRENDS_ANN)
        plot_figure(TRENDS_ANN, GRIDLONS, GRIDLATS, 'Trend of '+ indexname+' '+REGION)











