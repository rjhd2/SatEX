# -*- coding: iso-8859-1 -*-
import numpy as np
import numpy.ma as ma
import glob
import matplotlib.pyplot as plt
import iris.quickplot as qplt
import matplotlib.cm as mpl_cm
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def plot_years(x,y, title):
    fig=plt.figure()
    plt.plot(x,y)
    plt.grid()
    plt.title(indexname+' values for each year '+title+' (ECA&D)')
    plt.savefig('/home/h01/vportge/CM_SAF/plots/ECA_D_time_series_'+indexname+'_'+title[-4:]+'.png')
    return 0


def plot_station_data_on_map(full_dataset, lon, lat, year_for_map, season_for_map):
    '''Plot a scatterplot of the stations with their measurements indicated by size and color of scatterpoint.'''
    fig = plt.figure()  # create a figure object
    ax = plt.axes(projection=ccrs.PlateCarree()) 
    ax.stock_img()
    ax.add_feature(cfeature.LAND) 
    ax.add_feature(cfeature.LAKES)
    ax.add_feature(cfeature.RIVERS)
    ax.coastlines()
    season_index = SEASONS_POSSIBLE.index(season_for_map)
    locations=np.where(full_dataset[:, year_for_map - MIN_YEAR, season_index]!=0)[0]
    values=np.array(full_dataset[locations, year_for_map - MIN_YEAR, season_index])

    #ax.set_extent([ np.amin(lon[locations])-0.5, np.amax(lon[locations])+0.5, np.amin(lat[locations])-0.5, np.amax(lat[locations])+0.5 ], crs=ccrs.PlateCarree())
    ax.set_extent([ -30., 65., 30, 65. ], crs=ccrs.PlateCarree())

    s=ax.scatter(lon[locations],lat[locations],c=values,transform=ccrs.PlateCarree(), s=80.*values/np.amax(values), alpha=0.7, cmap='jet', zorder=10) 
    cb=fig.colorbar(s, ax=ax, orientation='horizontal')
    cb.set_label(indexname+' Index Value')
    plt.title(indexname+' Index in '+season_for_map+' '+str(year_for_map)+' (ECA&D)')
    #plt.show()
    plt.savefig('/home/h01/vportge/CM_SAF/plots/ECA_D_map_'+indexname+'_'+season_for_map.replace(" ", "")+'_'+str(year_for_map)+'.png')
    return 0


def DMS2DD(D,M,S): 
    '''Convert longitude/latitude data from Degree:Minutes:Seconds to Decimal Degrees.'''
    if D >= 0:
            DD = D+(float(M)*60.+float(S))/3600.
    else:
            DD = D-(float(M)*60.+float(S))/3600.
    return DD




def get_station_data(filepath):
    '''Get ID, latitude, longitude, height of the stations and return them.'''

    ############################################
    #Read in Station Data: ID, Lat, Lon, height#
    ############################################
    #01-05 STAID       : Station identifier
    #07-46 STATIONNAME : Station Name
    #48-87 COUNTRYNAME : Country Name
    #89-97 LAT         : Latitude in degrees:minutes:seconds (+:North, -:South)
    #99-109 LON        : Longitude in degrees:minutes:seconds (+:East, -:West)
    #111-115 HGT       : Station elevation in meters 
    with open(filepath) as f:
        lines = f.readlines()
    station_data = np.zeros((len(lines[17:]), 4)) #the first 17 lines are part of the header. 

    for i in range(len(lines[17:])):
            station_data[i, 0] = lines[17+i][0:5]
            D_lat = float(lines[17+i][88:91])
            M_lat = float(lines[17+i][92:94])
            S_lat = float(lines[17+i][95:97])

            D_lon = float(lines[17+i][98:102])
            M_lon = float(lines[17+i][103:105])
            S_lon = float(lines[17+i][106:108])

            station_data[i, 1] = DMS2DD(D_lat, M_lat, S_lat) #lat, to convert from DMS to DD
            station_data[i, 2] = DMS2DD(D_lon, M_lon, S_lon) #lon
            station_data[i, 3] = str(lines[17+i][110:115])
    return station_data




'''
#######################################################################################################
#Check Scaling for each index file (data values get often scaled by 0.01, but is it always like this?)#
#######################################################################################################
see_scaling_parameter = glob.glob('/scratch/vportge/ECA_D/*/index*000001.txt')
for files in see_scaling_parameter:
	with open(files) as f:
    		print(f.readlines()[15])
#every index is scaled by 0.01 apparently.
'''


##########################################################################
#Read in Data: all stations files will be put together in one numpy array#
##########################################################################

indexname = 'CDD' #Decide which index should be used:
YEAR_FOR_MAP = 2007 #Decide from which year a map of the values is made. 
SEASON_FOR_MAP = 'DJF'
SEASONS_POSSIBLE=['SOUID', 'YEAR', 'ANNUAL', 'WINTER HALF YEAR', 'SUMMER HALF YEAR', 'DJF', 'MAM', 'JJA', 'SON', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']



FILEPATH='/scratch/vportge/ECA_D/ECA_index'+indexname

fnames = glob.glob(FILEPATH+'/index*.txt')
fnames.sort()
#LIST_OF_STATION_DATA is a list where each element is the data of one station which is an array. 
#Each element has dimensions: number_of_years x 21 where 21: different seasons, months, ...
LIST_OF_STATION_DATA = [np.loadtxt(f, skiprows=30) for f in fnames]

#find earliest (MIN_YEAR) and latest measurement in all files
MAX_YEAR = 0
MIN_YEAR = 2018

for station in range(len(LIST_OF_STATION_DATA)): 
    if LIST_OF_STATION_DATA[station].ndim == 1:
        #stations with only one year of data have dimensions: (21,), but for putting them
        #together with the other stations it's better to have dimension (1,21)
        LIST_OF_STATION_DATA[station] = LIST_OF_STATION_DATA[station].reshape((1, 21))

    #find earliest and latest measurement: [:, 1] is a list of all the years in which
    #measurements at this station were made. 
    if np.amax(LIST_OF_STATION_DATA[station][:,1]) > MAX_YEAR:
        MAX_YEAR = np.amax(LIST_OF_STATION_DATA[station][:, 1])
    if np.amin(LIST_OF_STATION_DATA[station][:,1]) < MIN_YEAR:
        MIN_YEAR = np.amin(LIST_OF_STATION_DATA[station][:, 1])

MAX_NUMBER_OF_YEARS = MAX_YEAR - MIN_YEAR + 1
years = np.arange(MIN_YEAR, MAX_YEAR+1)


#Not every station measures same time period, but do they at least measure continously each year
#beginning from first measuring year?
for station in range(len(LIST_OF_STATION_DATA)):
    if LIST_OF_STATION_DATA[station].shape[0] > 1:
        for j in range(1, LIST_OF_STATION_DATA[station].shape[0]):
            #if they don't measure continuously then the difference between two measurements is not 1 year. 
            if (LIST_OF_STATION_DATA[station][j, 1]-LIST_OF_STATION_DATA[station][j-1, 1])!= 1:
                print(LIST_OF_STATION_DATA[station][j, 1]-LIST_OF_STATION_DATA[station][j-1, 1])
                print('The time series is not continuously')
                sys.exit()



#FULL_DATASET will contain the data for all stations, for all years and all different months. 
#has therefore dimensions: Stations x years x seasons/months
FULL_DATASET = np.ones((len(LIST_OF_STATION_DATA), MAX_NUMBER_OF_YEARS, LIST_OF_STATION_DATA[0].shape[1]))*(-999999.0) 
#-999999.0 is the fill value of the data.

for station in range(len(LIST_OF_STATION_DATA)):
    #first year of station's dataset, to decide where to put the data in the big array
    FIRST_YEAR = LIST_OF_STATION_DATA[station][0, 1] 
    LAST_YEAR = LIST_OF_STATION_DATA[station][-1, 1] #last year of station's dataset

    START_INDEX = FIRST_YEAR - MIN_YEAR
    END_INDEX = LAST_YEAR - MAX_YEAR

    FULL_DATASET[station, int(START_INDEX):int(START_INDEX)+(int(LAST_YEAR)-int(FIRST_YEAR))+1, :] = LIST_OF_STATION_DATA[station]


FULL_DATASET = ma.masked_where(FULL_DATASET == -999999., FULL_DATASET )
FULL_DATASET[:, :, 2:] = FULL_DATASET[:, :, 2:]*0.01 #Values are scaled by factor 0.01

global_mean = np.mean(FULL_DATASET, axis=0)

station_data_path = FILEPATH+'/stations.txt'

STATION_DATA = get_station_data(station_data_path)

lon = STATION_DATA[:,2]
lat = STATION_DATA[:,1]


if YEAR_FOR_MAP >= MAX_YEAR or YEAR_FOR_MAP <= MIN_YEAR:
    print('Chosen year is out of range, take last possible year instead.')
    YEAR_FOR_MAP = MAX_YEAR


plot_years(global_mean[:,1], global_mean[:,5], 'for global mean') #[x,x,1]: years, [x,x,5]: some season, [-35,x,x]: station number
plot_years(FULL_DATASET[-35, :, 1], FULL_DATASET[-35, :, 5], 'for specific station') #[x,x,1]: years, [x,x,5]: some season, [-35,x,x]: station number
plot_station_data_on_map(FULL_DATASET, lon, lat, YEAR_FOR_MAP, SEASON_FOR_MAP)

#FULL_DATASET contains now first dimension: stations, second: years, third: different variables
#for i in range(len(arrays)):
	#if arrays[i].shape[0]==MAX_NUMBER_OF_YEARS:
		#station_with_longest_record = i
		#years=arrays[i][:,1]
		#break
#final_array = np.concatenate(arrays)

#MAX_NUMBER_OF_YEARS=max([a.shape[0] for a in arrays])

#np.dstack

#filename='/home/h01/vportge/CM_SAF/test_data/ECA_indexCSDI/indexCSDI000001.txt'
#data=np.loadtxt(filename, skiprows=30)

