# -*- coding: iso-8859-1 -*-
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

try:
    YEAR_N_MONTH = sys.argv[1] #has format: 1991/01/
except:
    YEAR_N_MONTH = '1997/03/'


OUTPATH_PLOTS = '/home/h01/vportge/CM_SAF/plots/CM_SAF/'

#filepaths of all hourly files of one month to be analysed:
FILES = glob.glob('/scratch/vportge/CM_SAF_data_metadata_changed/'+YEAR_N_MONTH+'*.nc')

#OUTPATH = "/scratch/vportge/CM_SAF_LST_MIN_MAX/"
OUTPATH = "/scratch/vportge/CM_SAF_LST_MIN_MAX_COLD_WINDOW_10_3/"


#filepaths of all hourly files of all days to be analysed.
#FILES=glob.glob('/scratch/vportge/CM_SAF_data_metadata_changed/*/*.nc')
FILES.sort()

GET_COORDINATES_PATH = FILES[0:24]
GET_COORDINATES_DATA = iris.load(GET_COORDINATES_PATH, 'Land Surface Temperature (PMW)')
#concatenate the hourly data into one cube with dims (time: 24; latitude: 856; longitude: 2171)
GET_COORDINATES_DATA = GET_COORDINATES_DATA.concatenate_cube()

LONS = GET_COORDINATES_DATA.coord('longitude').points
LATS = GET_COORDINATES_DATA.coord('latitude').points

###############################################################################
#Calculate the local time of each gridpoint. This depends on the longitude of #
#the gridpoint. +/- 1 degree longitude means: +/- 4 minutes to UTC time       #
#'OFFSET' is the time period that has to be added/subtracted from the UTC time#
#and can be negative or positive. It is an array with dim(LONS) as dimension. #
###############################################################################

#datetime(-1, 2281) means: go -1 day back and then plus 2281 seconds into the future,
#LONS/360 gives the time in days which has to be added or subtracted from UTC time.
#OFFSET is the same for all files.
OFFSET = np.array([datetime.timedelta(i) for i in LONS/360.])

TIME_DATA = GET_COORDINATES_DATA.coord('time').points
#those are the dates and times of each hourly file of one date.
TIME_DATA_DATETIME = np.array([datetime.datetime.utcfromtimestamp(i) for i in TIME_DATA])
#make datetime object  out of timestamp

#################################################################################
#Calculate the local times for each gridpoint for determining which hourly      #
#files lie within the time intervals 11 am to 3 pm and 4 am to 9 am where the   #
#maximum and minimum LST shall be analysed. The index/location of the hourly    #
#files inside the time array won't change when analysing different days and     #
#therefore the indices of the suitable hourly files must only be calculated once#
#The local times which are calculated here are only used to find the indices:   #
#LOCAL_TIMES_TO_FIND_INDICES							#
#################################################################################

#compute local time for each longitude and each UTC hour
#timediff[0].__str__() #to see date and time in readable way
LOCAL_TIMES_TO_FIND_INDICES = np.array([i+OFFSET for i in TIME_DATA_DATETIME])


#TIME11 = TIME_DATA_DATETIME[11] #11 am
TIME11 = TIME_DATA_DATETIME[10] #10 am


TIME15 = TIME_DATA_DATETIME[15] #get the data and time of 3 pm, datetime object.
TIME4 = TIME_DATA_DATETIME[4]   #4 am
TIME9 = TIME_DATA_DATETIME[9]   #9 am

LST_WARM_INDICES = []
LST_COLD_INDICES = []
for i in range(len(LONS)):
    if i%100 == 0:
        print(i)

    #compute for each local time the difference to 3pm, 11am, 4am, 9am
    #to decide whether it lies within the two time intervals.

    TIMEDIFF15 = (LOCAL_TIMES_TO_FIND_INDICES[:, i] - TIME15)
    TIMEDIFF11 = (LOCAL_TIMES_TO_FIND_INDICES[:, i] - TIME11)

    TIMEDIFF4 = (LOCAL_TIMES_TO_FIND_INDICES[:, i] - TIME4)
    TIMEDIFF9 = (LOCAL_TIMES_TO_FIND_INDICES[:, i] - TIME9)

    #get the 'day' values of the timedifference arrays (datetime objects)
    #if the considered local time is earlier than the compared time: the 'day' value is -1
    #if the considered local time is later than the compared time: the 'day' value is 0

    DIFFDAYS15 = np.array([i.days for i in TIMEDIFF15])
    DIFFDAYS11 = np.array([i.days for i in TIMEDIFF11])

    DIFFDAYS4 = np.array([i.days for i in TIMEDIFF4])
    DIFFDAYS9 = np.array([i.days for i in TIMEDIFF9])


    #LST_WARM_indices contains for each longitude the indices in time coordinate where the
    #local time is between 11 am and 3 pm. (warm window) np.intersect1d(11am, 3pm)
    #LST_COLD_INDICES contains for each longitude the indices in time coordinate where the
    #local time is between 4 am and 9 am. (cold window)

    LST_WARM_INDICES.append(np.intersect1d(np.where(DIFFDAYS11 >= 0)[0], np.where(DIFFDAYS15 < 0)[0]))
    LST_COLD_INDICES.append(np.intersect1d(np.where(DIFFDAYS4 >= 0)[0], np.where(DIFFDAYS9 < 0)[0]))



##############################################################################
#Start of the analysis of each day. 'files' contain the filepaths.           #
##############################################################################

#calculate number of days to be analysed from number of files in directory, as there are only the hourly files
number_of_days = int(len(FILES)/24)
print(number_of_days)
for d in range(0, number_of_days):
    #one day consists of 24 hours. So take the first 24 files for the first day,
    #the next 24 files for the second day and so on.
    hourly_data_path = FILES[d*24:d*24+24]
    hourly_data = iris.load(hourly_data_path, 'Land Surface Temperature (PMW)')

    SATID = iris.load(hourly_data_path[0], 'Spacecraft ID (unique number defined by MSGGS or GSDS or NORAD or COSPAR)')
    SATID = SATID[0].data

    hourly_uncertainty = iris.load(hourly_data_path, 'Land Surface Temperature Uncertainty PMW')

    #concatenate hourly data into one cube with dims (time: 24; latitude: 856; longitude: 2171)
    day_cube = hourly_data.concatenate_cube()
    day_data = day_cube.data

    day_uncrty_cube = hourly_uncertainty.concatenate_cube()
    day_uncrty = day_uncrty_cube.data


    day_yyyymmdd = hourly_data_path[0][59:67]
    #day_yyyymmdd=hourly_data_path[0][60:68]
    print(day_yyyymmdd)

    #if the local times are whished then do:

    #those are the dates and times of each hourly file of the day:
    #times_day=day_cube.coord('time').points

    #make datetime object  out of times:
    #times_day_datetime=np.array([datetime.datetime.utcfromtimestamp(i) for i in times_day])

    #compute local time for each longitude and each UTC hour:
    #local_times=np.array([i+OFFSET for i in times_day_datetime])

    ####################################################################################
    #Compute the minimum/maximum LST: LST_COLD_INDICES contains for each longitude     #
    #an array of the indices of the times that lie within the appropriate time interval#
    #Go through each longitude (for i in range(len(LONS))) and read out the data inside#
    #the time interval (LST_COLD_INDICES[i]) for each latitude (':' at second place).  #
    #Then find for each latitude the minimum of the LST inside the time interval.      #
    #np.amin(..., axis=0). During this process the masked_values from day_data change  #
    #their fill_value to 1.e20. Therefore: mask these values again. 		       #
    ####################################################################################

    LSTwarm_max = np.array([np.amax(day_data[LST_WARM_INDICES[i], :, i], axis=0) for i in range(len(LONS))])
    LSTcold_min = np.array([np.amin(day_data[LST_COLD_INDICES[i], :, i], axis=0) for i in range(len(LONS))])

    #compute maximum value in cold window (in LST_COLD_INDICES time interval),
    #as LST_COLD_INDICES is often affected by clouds.
    LSTcold_max = np.array([np.amax(day_data[LST_COLD_INDICES[i], :, i], axis=0) for i in range(len(LONS))])

    LSTwarm_max = ma.masked_values(LSTwarm_max, 1.e20)
    LSTcold_min = ma.masked_values(LSTcold_min, 1.e20) #mask fill values
    LSTcold_max = ma.masked_values(LSTcold_max, 1.e20)

    #longitude and latitude coordinates were inverted compared to all other datasets -> Transpose
    LSTwarm_max = LSTwarm_max.T
    LSTcold_min = LSTcold_min.T
    LSTcold_max = LSTcold_max.T

    #find uncertainty values:
    #result is the index of the hour-index in LST_WARM_indices, result = 1 means: first element
    #of hour_indices_array LST_WARM_indices. If LST_WARM_indices = [12, 13, 14, 15]
    #then result = 1 means: first value -> 13, take hour = 13, python indexing starts with 0.
    LST_warm_max_uncrty_index = np.array([np.argmax(day_data[LST_WARM_INDICES[i], :, i], axis=0) for i in range(len(LONS))])
    LST_cold_min_uncrty_index = np.array([np.argmin(day_data[LST_COLD_INDICES[i], :, i], axis=0) for i in range(len(LONS))])
    LST_cold_max_uncrty_index = np.array([np.argmax(day_data[LST_COLD_INDICES[i], :, i], axis=0) for i in range(len(LONS))])


    #array of hourly indices shape:(856,2171): 
    #which hour has maximum LST in warm window -> take this uncertainty value then
    hourly_index_warm_max = np.array([LST_WARM_INDICES[i][LST_warm_max_uncrty_index[i, :]] for i in range(len(LONS))])
    hourly_index_warm_max = hourly_index_warm_max.T

    hourly_index_cold_min = np.array([LST_COLD_INDICES[i][LST_cold_min_uncrty_index[i, :]] for i in range(len(LONS))])
    hourly_index_cold_min = hourly_index_cold_min.T

    hourly_index_cold_max = np.array([LST_COLD_INDICES[i][LST_cold_max_uncrty_index[i, :]] for i in range(len(LONS))])
    hourly_index_cold_max = hourly_index_cold_max.T


    #Convert hourly_indices into datetime objects. so that for each gridpoint the observation time can be seen.
    DATE_N_TIME = np.array([datetime.datetime.utcfromtimestamp(i) for i in day_cube.coord('time').points]) #to save the time of observations.
    OBS_TIMES_WARM_MAX = DATE_N_TIME[hourly_index_warm_max]
    OBS_TIMES_COLD_MIN = DATE_N_TIME[hourly_index_cold_min]
    OBS_TIMES_COLD_MAX = DATE_N_TIME[hourly_index_cold_max]


    uncrty_warm_max = np.zeros(hourly_index_warm_max.shape)
    uncrty_warm_max = ma.masked_values(uncrty_warm_max, 1.e20)

    uncrty_cold_min = np.zeros(hourly_index_cold_min.shape)
    uncrty_cold_min = ma.masked_values(uncrty_cold_min, 1.e20)

    uncrty_cold_max = np.zeros(hourly_index_cold_max.shape)
    uncrty_cold_max = ma.masked_values(uncrty_cold_max, 1.e20)

    for i in range(len(LATS)):
        for j in range(len(LONS)):
            uncrty_warm_max[i, j] = (day_uncrty[hourly_index_warm_max[i, j], i, j])
            uncrty_cold_min[i, j] = (day_uncrty[hourly_index_cold_min[i, j], i, j])
            uncrty_cold_max[i, j] = (day_uncrty[hourly_index_cold_max[i, j], i, j])


    #################################################################
    #Uncomment this if a plots are wished. Is 'Agg' environment set?#
    #################################################################

    #plot with filled contours
    #plot_map(day_cube[0,:,:], OUTPATH_PLOTS)

    #plot daily cycle:
    #plot=plot_daily_cycle(day_data[:,179,1592], OUTPATH_PLOTS)

    #plot LST max and min
    #plot_figure(LSTwarm_max, LONS, LATS, 'max LST '+str(day_yyyymmdd), str(day_yyyymmdd), OUTPATH_PLOTS)
    #plot_figure(LSTcold_min, LONS, LATS, 'min LST '+str(day_yyyymmdd), str(day_yyyymmdd), OUTPATH_PLOTS)


    ####################################################################
    #Create the netCDF file for LST max and LST min and uncertainties  #
    #For this: Create Cubes out of the np.arrays with metadata and then#
    #save the cubes to netCDF files using the iris.save method.        #
    ####################################################################

    timedim = hourly_data[0].coord('time')
    latdim = hourly_data[0].coord('latitude')
    londim = hourly_data[0].coord('longitude')
    attri = {"creator_name": "Veronika Portge", "creator_email": "veronika.portge@metoffice.gov.uk", "summary": "This file contains time-space aggregated Thematic Climate Data Records (TCDR) produced by geosatclim within the Satellite Application Facility on Climate Monitoring (CM SAF). It was processed to determine the maximum land surface temperature in the warm window from 10 am - 3 pm local time and the maximum and minimum land surface temperature in the cold window from 4 am - 9 am local time."}




    #reshape arrays so that they've got a time dimension
    LSTwarm_max = np.reshape(LSTwarm_max, (1, LSTwarm_max.shape[0], LSTwarm_max.shape[1]))
    LSTcold_min = np.reshape(LSTcold_min, (1, LSTcold_min.shape[0], LSTcold_min.shape[1]))
    LSTcold_max = np.reshape(LSTcold_max, (1, LSTcold_max.shape[0], LSTcold_max.shape[1]))

    uncrty_warm_max = np.reshape(uncrty_warm_max, (1, uncrty_warm_max.shape[0], uncrty_warm_max.shape[1]))
    uncrty_cold_min = np.reshape(uncrty_cold_min, (1, uncrty_cold_min.shape[0], uncrty_cold_min.shape[1]))
    uncrty_cold_max = np.reshape(uncrty_cold_max, (1, uncrty_cold_max.shape[0], uncrty_cold_max.shape[1]))

    OBS_TIMES_WARM_MAX = np.reshape(OBS_TIMES_WARM_MAX, (1, OBS_TIMES_WARM_MAX.shape[0], OBS_TIMES_WARM_MAX.shape[1]))
    OBS_TIMES_COLD_MIN = np.reshape(OBS_TIMES_COLD_MIN, (1, OBS_TIMES_COLD_MIN.shape[0], OBS_TIMES_COLD_MIN.shape[1]))
    OBS_TIMES_COLD_MAX = np.reshape(OBS_TIMES_COLD_MAX, (1, OBS_TIMES_COLD_MAX.shape[0], OBS_TIMES_COLD_MAX.shape[1]))


    


    #now: create Cubes out of the arrays
    LSTwarm_max_cube = iris.cube.Cube(LSTwarm_max, long_name="Maximum Land Surface Temperature in Warm Window (PMW)", var_name='LST_MAX_WARM', units="K", attributes=attri, dim_coords_and_dims=[(timedim, 0), (latdim, 1), (londim, 2)])
    LSTcold_min_cube = iris.cube.Cube(LSTcold_min, long_name="Minimum Land Surface Temperature in Cold Window (PMW)", var_name='LST_MIN_COLD', units="K", attributes=attri, dim_coords_and_dims=[(timedim, 0), (latdim, 1), (londim, 2)])
    LSTcold_max_cube = iris.cube.Cube(LSTcold_max, long_name="Maximum Land Surface Temperature in Cold Window (PMW)", var_name='LST_MAX_COLD', units="K", attributes=attri, dim_coords_and_dims=[(timedim, 0), (latdim, 1), (londim, 2)])

    uncrty_warm_max_cube = (iris.cube.Cube(uncrty_warm_max,
                                           long_name="Uncertainty of Maximum Land Surface"+
                                           " Temperature in Warm Window (PMW)", var_name='LSTERROR_MAX_WARM', units="K",
                                           attributes=attri, dim_coords_and_dims=[(timedim, 0),
                                           (latdim, 1), (londim, 2)]))

    uncrty_cold_min_cube = (iris.cube.Cube(uncrty_cold_min,
                                           long_name="Uncertainty of Minimum Land Surface"+
                                           " Temperature in Cold Window (PMW)", var_name='LSTERROR_MIN_COLD', units="K",
                                           attributes=attri, dim_coords_and_dims=[(timedim, 0),
                                           (latdim, 1), (londim, 2)]))

    uncrty_cold_max_cube = iris.cube.Cube(uncrty_cold_max, long_name="Uncertainty of Maximum Land Surface Temperature in Cold Window (PMW)", var_name='LSTERROR_MAX_COLD', units="K", attributes=attri, dim_coords_and_dims=[(timedim, 0), (latdim, 1), (londim, 2)])

    #import netCDF4
    #to read it back into python: 
    #import netCDF4
    #netCDF4.num2date(zeit[0].data, units='days since 1970-01-01 00:00', calendar='standard')

    #PRECIP = np.zeros(LSTwarm_max_cube.shape)
    #PRECIP_CUBE = iris.cube.Cube(PRECIP, long_name="Precipitation", var_name='PRECIP', units="kg m-2 d-1", attributes=attri, dim_coords_and_dims=[(timedim, 0), (latdim, 1), (londim, 2)])

    OBS_TIMES_WARM_MAX = netCDF4.date2num(OBS_TIMES_WARM_MAX, units = 'days since 1970-01-01 00:00', calendar = 'standard')
    OBS_TIMES_COLD_MIN = netCDF4.date2num(OBS_TIMES_COLD_MIN, units = 'days since 1970-01-01 00:00', calendar = 'standard')
    OBS_TIMES_COLD_MAX = netCDF4.date2num(OBS_TIMES_COLD_MAX, units = 'days since 1970-01-01 00:00', calendar = 'standard')


    OBS_TIMES_WARM_MAX_CUBE = iris.cube.Cube(OBS_TIMES_WARM_MAX, long_name="Date and Time (UTC) of Observation of Maximum Land Surface Temperature in Warm Window (PMW)", var_name='OBS_TIME_MAX_WARM', units = 'days since 1970-01-01 00:00', attributes=attri, dim_coords_and_dims=[(timedim, 0), (latdim, 1), (londim, 2)])
    OBS_TIMES_COLD_MIN_CUBE = iris.cube.Cube(OBS_TIMES_COLD_MIN, long_name="Date and Time (UTC) of Observation of Minimum Land Surface Temperature in Cold Window (PMW)", var_name='OBS_TIME_MIN_COLD', units = 'days since 1970-01-01 00:00', attributes=attri, dim_coords_and_dims=[(timedim, 0), (latdim, 1), (londim, 2)])
    OBS_TIMES_COLD_MAX_CUBE = iris.cube.Cube(OBS_TIMES_COLD_MAX, long_name="Date and Time (UTC) of Observation of Maximum Land Surface Temperature in Cold Window (PMW)", var_name='OBS_TIME_MAX_COLD', units = 'days since 1970-01-01 00:00', attributes=attri, dim_coords_and_dims=[(timedim, 0), (latdim, 1), (londim, 2)])

    SATID = ma.masked_values(SATID, -2147483647)
    SATID_CUBE = iris.cube.Cube(SATID, long_name="Spacecraft ID (unique number defined by MSGGS or GSDS or NORAD or COSPAR)", var_name="SATID", attributes=attri, units="1")


    #make CubeList out of different cubes
    cubelist = iris.cube.CubeList([LSTwarm_max_cube, LSTcold_min_cube, LSTcold_max_cube, uncrty_warm_max_cube, uncrty_cold_min_cube, uncrty_cold_max_cube, OBS_TIMES_WARM_MAX_CUBE, OBS_TIMES_COLD_MIN_CUBE, OBS_TIMES_COLD_MAX_CUBE, SATID_CUBE])

    #save cubes, zlib = True will compress the data
    iris.save(cubelist, OUTPATH+str(day_yyyymmdd[0:4])+"/"+str(day_yyyymmdd[4:6])+"/LST_max_and_min_"+day_yyyymmdd+".nc", zlib = True)

    print('Finished day')





'''

    #now: create Cubes out of the arrays
    LSTwarm_max_cube = iris.cube.Cube(LSTwarm_max, long_name="Maximum Land Surface Temperature in Warm Window (PMW)", units="K", attributes=attri, dim_coords_and_dims=[(timedim, 0), (latdim, 1), (londim, 2)])
    LSTcold_min_cube = iris.cube.Cube(LSTcold_min, long_name="Minimum Land Surface Temperature in Cold Window (PMW)", units="K", attributes=attri, dim_coords_and_dims=[(timedim, 0), (latdim, 1), (londim, 2)])
    LSTcold_max_cube = iris.cube.Cube(LSTcold_max, long_name="Maximum Land Surface Temperature in Cold Window (PMW)", units="K", attributes=attri, dim_coords_and_dims=[(timedim, 0), (latdim, 1), (londim, 2)])

    uncrty_warm_max_cube = (iris.cube.Cube(uncrty_warm_max,
                                           long_name="Uncertainty of Maximum Land Surface"+
                                           " Temperature in Warm Window (PMW)", units="K",
                                           attributes=attri, dim_coords_and_dims=[(timedim, 0),
                                           (latdim, 1), (londim, 2)]))

    uncrty_cold_min_cube = (iris.cube.Cube(uncrty_cold_min,
                                           long_name="Uncertainty of Minimum Land Surface"+
                                           " Temperature in Cold Window (PMW)", units="K",
                                           attributes=attri, dim_coords_and_dims=[(timedim, 0),
                                           (latdim, 1), (londim, 2)]))

    uncrty_cold_max_cube = iris.cube.Cube(uncrty_cold_max, long_name="Uncertainty of Maximum Land Surface Temperature in Cold Window (PMW)", units="K", attributes=attri, dim_coords_and_dims=[(timedim, 0), (latdim, 1), (londim, 2)])
'''





'''
lat = 48.871236 ## your latitude
lon = 2.77928 ## your longitude

url = "http://api.geonames.org/timezoneJSON?formatted=true&lat={}&lng={}&username=demo".format(lat,lon)

r = requests.get(url) ## Make a request
return r.json()['timezoneId'] 

from datetime import datetime
from dateutil import tz

from_zone = tz.gettz('UTC')
to_zone = tz.gettz('America/New_York')

# utc = datetime.utcnow()
utc = datetime.strptime('2011-01-21 02:37:21', '%Y-%m-%d %H:%M:%S')

# Tell the datetime object that it's in UTC time zone since 
# datetime objects are 'naive' by default
utc = utc.replace(tzinfo=from_zone)

# Convert time zone
central = utc.astimezone(to_zone)
get_timezones_data_path=FILES[0:24]
get_timezones_data=iris.load(get_timezones_data_path, 'Land Surface Temperature (PMW)') 
get_timezones_data=get_timezones_data.concatenate_cube() #concatenate the hourly data into one cube with dimensions (time: 24; latitude: 856; longitude: 2171)

LONS=get_timezones_data.coord('longitude').points
LATS=get_timezones_data.coord('latitude').points

#timezones_array=np.chararray((LATS.shape[0], LONS.shape[0]))
timezones_array=[]

for i in range(500,len(LATS)):
    for j in range(1000,len(LONS)):
        lat=LATS[i]
        lon=LONS[j]
        url = "http://api.geonames.org/timezoneJSON?formatted=true&lat={}&lng={}&username=VPORTGE".format(lat,lon)
        r = requests.get(url) ## Make a request
        
        print(r.json()['timezoneId'])
        #timezones_array[i, j]=r.json()['timezoneId']
        timezones_array.append(r.json()['timezoneId'])
        #except:
                #continue


'''

#day_array=np.zeros((24, 856, 2171))
#for i in range(0,24):
	#day_array[i,:,:]=hourly_data[i].data
#np.ma.masked_where(day_array==-32767. , day_array)
#day=str('{:02}'.format(d))
#print(day)
#filepath='/net/home/h01/vportge/CM_SAF/test_data/ORD28974_europe/ORD28974/LTPin201511'+day+'*.nc'
#print(filepath)
