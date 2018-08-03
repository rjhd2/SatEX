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


def plot_years(x,y):
    plt.close()
    fig=plt.figure()
    plt.plot(x,y)
    plt.grid()
    plt.title('Time series of global average '+indexname+' values (GHCNDEX)')
    plt.savefig(OUTPATH+indexname+'_time_series_GHCNDEX.png')

def plot_map(data, lons, lats):
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent([ -30., 65., 30, 65. ], crs=ccrs.PlateCarree())

    cont = ax.contourf(lons, lats, year,transform=ccrs.PlateCarree(),cmap='nipy_spectral')
    ax.coastlines()
    cb=fig.colorbar(cont, ax=ax, orientation='horizontal')
    cb.set_label(indexname+' Index Value')
    plt.title('Map of '+indexname+' values (GHCNDEX) '+ str(CHOOSE_YEAR))
    plt.savefig(OUTPATH+indexname+'_GHCNDEX_map_'+str(CHOOSE_YEAR)+'.png')

def line(x,t,m):
    '''Plot a line. '''
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

    if calc_with_mdi == True:
        good_data=np.where(ydata == False)[0]
        n=len(ydata[good_data])

    elif calc_with_mdi == False:
        n=len(ydata)

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



OUTPATH = '/scratch/vportge/plots/GHCNDEX/'


######################################################################################
#load in data with constraints to correct region defined by longitudes and latitudes #
######################################################################################

indexname='TXx' #Decide which index should be used:
CHOOSE_YEAR=2015
filepath='/project/hadobs2/hadex3/ghcndex/GHCND_'+indexname+'_1951-2018_RegularGrid_global_2.5x2.5deg_LSmask.nc'
time_constraint = iris.Constraint(time=lambda c: 20160101 > c.point > 19910100)
longitude_constraint = iris.Constraint(longitude=lambda c: 0<=c.point<=60 or 360.>=c.point>=342)
latitude_constraint = iris.Constraint(latitude=lambda c: 22< c.point<60) 

data=iris.load(filepath, time_constraint) #Data has name of the months. 
data = data.extract(longitude_constraint)
data = data.extract(latitude_constraint)


######################################################################################
#Change time coordinate of data as it only contains the month via .name() of the cube#
######################################################################################

spat_avg_month = iris.cube.CubeList()

for i in range(len(data)):
    month_data = data[i]
    month_time = month_data.coord('time')
    month_datetime = []

    if month_data.name() == 'Ann':
        ANN_data = copy.deepcopy(month_data)
        #calculate spatial average#
        ANN_data_avg=ANN_data.collapsed('latitude', iris.analysis.MEAN)
        ANN_data_avg=ANN_data_avg.collapsed('longitude', iris.analysis.MEAN)
        ANN_index = i*1.
    else:
        for j in range(len(month_time.points)):
            yyyy = datetime.datetime.strptime(str(int(month_time.points[j])), '%Y%m%d').year
            if month_data.name() == 'Jan':
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
        month_avg=month_data.collapsed('latitude', iris.analysis.MEAN)
        month_avg=month_avg.collapsed('longitude', iris.analysis.MEAN)
        spat_avg_month.append(month_avg)
del(data[int(ANN_index)])


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


##############################################################
#Plot map of averaged values over whole time period: ANN_data#
##############################################################
plt.close()
fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
#ax.set_extent([ -30., 65., 30, 65. ], crs=ccrs.PlateCarree())
cont = iplt.contourf(ANN_data.collapsed('time', iris.analysis.MEAN))
ax.coastlines()
cb=fig.colorbar(cont, ax=ax, orientation='horizontal')
cb.set_label(indexname+' Index Value')
plt.title('Map of averaged '+indexname+' values (GHCNDEX) ')
plt.savefig(OUTPATH+indexname+'_GHCNDEX_map_averaged.png')

#########################################
#Plot years 1991 - 2015 with trend line #
#########################################
plt.close()
YDATA = values_spat_avg
XDATA = times_spat_avg
times_datetime = [netCDF4.num2date(i, units = 'days since 1970-01-01 00:00', calendar = 'standard') for i in times_spat_avg]

trendanalysis = MedianPairwiseSlopes(XDATA,YDATA,10,mult10 = False, sort = False, calc_with_mdi=False)
slope = trendanalysis[0]
slope_lower_uncrty = trendanalysis[1]
slope_upper_uncrty = trendanalysis[2]
Y_INTERCEPTION = trendanalysis[3]


trendline=line(np.array(XDATA), np.array(Y_INTERCEPTION), slope)
plt.plot(times_datetime, YDATA)
plt.plot(times_datetime, trendline, label='trend: '+str(round(slope*365*10.,2))+' per decade')
plt.grid()
plt.title(indexname + ' GHCNDEX', size=22)
plt.xlabel('years', size=20)
plt.legend(fontsize = 16)
plt.tight_layout()
plt.tick_params(axis='both', which='major', labelsize=16)
plt.savefig(OUTPATH+indexname+'_GHCNDEX_with_trend.png')











