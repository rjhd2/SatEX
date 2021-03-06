# -*- coding: iso-8859-1 -*-
import numpy as np
import iris
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import iris.quickplot as qplt
import matplotlib.cm as mpl_cm
#import iris.plot as iplt
import cartopy.crs as ccrs
#import cartopy.feature as cfeature
import glob
#from iris.util import unify_time_units
#import datetime
#import numpy.ma as ma
import sys
#import requests

def plot_map_of_cube(data, date):
    '''Plot map of cube with qplt.'''
    plt.close()
    qplt.contourf(data)
    plt.gca().coastlines() #add coastlines
    plt.title('CM SAF map of LST of some hour on '+date)
    plt.savefig('/home/h01/vportge/CM_SAF/plots/CM_SAF/CM_SAF_map_LST'+date+'.png')

def pcolormesh_map(data, lons, lats, cbar_label, titlestring, filename, outpath):
    '''Plot annual average on a map.'''
    plt.close()
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    #This takes some time, I think the average gets calculated now
    #lst_map = plt.pcolormesh(lons, lats, data, transform=ccrs.PlateCarree())
    lst_map = plt.pcolormesh(lons, lats, data, transform=ccrs.PlateCarree(), cmap = mpl_cm.get_cmap('brewer_RdBu_11'), vmin = 0.0001, vmax = 100)
    lst_map.cmap.set_under('white') #set 0 percent values to white. 

    cbar = plt.colorbar(lst_map, orientation='horizontal', extend='both')
    cbar.set_label(cbar_label)

    ax1.coastlines()
    plt.title(titlestring+str(YEAR))
    plt.savefig(outpath+filename+str(YEAR)+'.png')
    return


def load_min_max_LST(season_filepath):
    lst_warm_max = iris.load(season_filepath, 'Maximum Land Surface Temperature in Warm Window (PMW)')
    lst_warm_max = lst_warm_max.concatenate_cube()

    lst_cold_max = iris.load(season_filepath, 'Maximum Land Surface Temperature in Cold Window (PMW)')
    lst_cold_max = lst_cold_max.concatenate_cube()

    lst_cold_min = iris.load(season_filepath, 'Minimum Land Surface Temperature in Cold Window (PMW)')
    lst_cold_min = lst_cold_min.concatenate_cube()

    average_lst_warm_max = lst_warm_max.collapsed('time', iris.analysis.MEAN)
    average_lst_cold_max = lst_cold_max.collapsed('time', iris.analysis.MEAN)
    average_lst_cold_min = lst_cold_min.collapsed('time', iris.analysis.MEAN)


    return lst_warm_max, lst_cold_max, lst_cold_min, average_lst_warm_max, average_lst_cold_max, average_lst_cold_min


def analyse_coverage(lst_warm_max, lst_cold_max, lst_cold_min, lons, lats, season, outpath):


    if season=='DJF':
        divide_days = 90.25
    elif season == 'MAM':
        divide_days = 92.
    elif season == 'JJA':
        divide_days = 92.
    elif season == 'SON':
        divide_days = 91.

    latdim = lst_warm_max[0].coord('latitude')
    londim = lst_warm_max[0].coord('longitude')

    lst_warm_max_data = lst_warm_max.data
    lst_cold_max_data = lst_cold_max.data
    lst_cold_min_data = lst_cold_min.data

    coverage_lst_warm_max = np.ma.MaskedArray.count(lst_warm_max_data, axis=0)
    coverage_lst_cold_max = np.ma.MaskedArray.count(lst_cold_max_data, axis=0)
    coverage_lst_cold_min = np.ma.MaskedArray.count(lst_cold_min_data, axis=0)

    pcolormesh_map(coverage_lst_warm_max*100./divide_days, lons, lats,
                '% of possible days that could have been observed',
                season+' coverage - LST in warm window ', season+'_coverage_LST_warm_', outpath)
    #pcolormesh_map(coverage_lst_cold_max, lons, lats,
                #'% of possible days that could have been observed',
                #season+' coverage - max LST in cold window ', season+'_coverage_LST_max_cold_', outpath)
    pcolormesh_map(coverage_lst_cold_min*100./divide_days, lons, lats,
                '% of possible days that could have been observed',
                season+' coverage - LST in cold window ', season+'_coverage_LST_cold_', outpath)
    

    #Save seasonal coverage for each year to a netcdf file so that coverage can be calculated faster.
    '''
    attri = {"creator_name": "Veronika Portge", "creator_email": "veronika.portge@metoffice.gov.uk", "summary": "This file contains processed time-space aggregated Thematic Climate Data Records (TCDR) produced by geosatclim within the Satellite Application Facility on Climate Monitoring (CM SAF). It was processed to determine the coverage of the maximum land surface temperature in the warm window from 11 am - 3 pm local time and the coverage of the maximum and minimum land surface temperature in the cold window from 4 am - 9 am local time for " + SEASON + " of "+YEAR +"."}
    coverage_lst_warm_max_cube = iris.cube.Cube(coverage_lst_warm_max, long_name="Coverage of Maximum Land Surface Temperature in Warm Window (PMW)", var_name='COV_LST_MAX_WARM', units="K", attributes=attri, dim_coords_and_dims=[(latdim, 0), (londim, 1)])
    coverage_lst_cold_max_cube = iris.cube.Cube(coverage_lst_cold_max, long_name="Coverage of Maximum Land Surface Temperature in Cold Window (PMW)", var_name='COV_LST_MAX_COLD', units="K", attributes=attri, dim_coords_and_dims=[(latdim, 0), (londim, 1)])
    coverage_lst_cold_min_cube = iris.cube.Cube(coverage_lst_cold_min, long_name="Coverage of Minimum Land Surface Temperature in Cold Window (PMW)", var_name='COV_LST_MIN_COLD', units="K", attributes=attri, dim_coords_and_dims=[(latdim, 0), (londim, 1)])

    cubelist = iris.cube.CubeList([coverage_lst_warm_max_cube, coverage_lst_cold_max_cube, coverage_lst_cold_min_cube])
    iris.save(cubelist, "/scratch/vportge/CM_SAF_LST_MIN_MAX/COVERAGE/"+str(YEAR)+"/"+str(YEAR)+"_"+str(SEASON)+"_coverage_LST_max_and_min.nc", zlib = True)
    '''

    return



#first argument gives the year to be analysed
try:
    YEAR = sys.argv[1]
except:
    YEAR = '1993'

print(YEAR)

OUTPATH = '/scratch/vportge/plots/CM_SAF/'

DATADIR = '/scratch/vportge/CM_SAF_LST_MIN_MAX/'

######################################
#Seasonal analysis DJF, MAM, JJA, SON#
######################################


for i in range(4):
    if i == 0:
        SEASON = 'DJF'
        if int(YEAR) == 1991:
            JAN = glob.glob(DATADIR+str(YEAR)+'/01/*.nc')
            FEB = glob.glob(DATADIR+str(YEAR)+'/02/*.nc')
            SEASON_FILEPATH =  JAN + FEB
            DJF = SEASON_FILEPATH * 1
            print(DJF)
        else:
            DEC = glob.glob(DATADIR+str(int(YEAR)-1)+'/12/*.nc')
            JAN = glob.glob(DATADIR+str(YEAR)+'/01/*.nc')
            FEB = glob.glob(DATADIR+str(YEAR)+'/02/*.nc')
            SEASON_FILEPATH = DEC + JAN + FEB
            DJF = SEASON_FILEPATH * 1

    elif i == 1:
        SEASON = 'MAM'
        MAR = glob.glob(DATADIR+str(YEAR)+'/03/*.nc')
        APR = glob.glob(DATADIR+str(YEAR)+'/04/*.nc')
        MAY = glob.glob(DATADIR+str(YEAR)+'/05/*.nc')
        SEASON_FILEPATH = MAR + APR + MAY
        MAM = SEASON_FILEPATH * 1

    elif i == 2:
        SEASON = 'JJA'
        JUN = glob.glob(DATADIR+str(YEAR)+'/06/*.nc')
        JUL = glob.glob(DATADIR+str(YEAR)+'/07/*.nc')
        AUG = glob.glob(DATADIR+str(YEAR)+'/08/*.nc')
        SEASON_FILEPATH = JUN + JUL + AUG
        JJA = SEASON_FILEPATH * 1

    elif i == 3:
        SEASON = 'SON'
        SEP = glob.glob(DATADIR+str(YEAR)+'/09/*.nc')
        OCT = glob.glob(DATADIR+str(YEAR)+'/10/*.nc')
        NOV = glob.glob(DATADIR+str(YEAR)+'/11/*.nc')
        SEASON_FILEPATH = SEP + OCT + NOV
        SON = SEASON_FILEPATH * 1


    SEASON_FILEPATH.sort()
    #SEASON_FILEPATH = SEASON_FILEPATH[0:4]

    LST_WARM_MAX, LST_COLD_MAX, LST_COLD_MIN, AVERAGE_LST_WARM_MAX, AVERAGE_LST_COLD_MAX, AVERAGE_LST_COLD_MIN = load_min_max_LST(SEASON_FILEPATH)

    #get longitudes and latitudes of grid
    LONS = LST_WARM_MAX.coord('longitude').points
    LATS = LST_WARM_MAX.coord('latitude').points

    #Plot averaged data:

    
    pcolormesh_map(AVERAGE_LST_WARM_MAX.data, LONS, LATS, 'LST in K',
                SEASON+' average of max LST in warm window ', SEASON+'_average_LST_max_warm_', OUTPATH+'seasons/')
    pcolormesh_map(AVERAGE_LST_COLD_MAX.data, LONS, LATS, 'LST in K',
                SEASON+' average of max LST in cold window ', SEASON+'_average_LST_max_cold_', OUTPATH+'seasons/')
    pcolormesh_map(AVERAGE_LST_COLD_MIN.data, LONS, LATS, 'LST in K',
                SEASON+' average of min LST in cold window ', SEASON+'_average_LST_min_cold_', OUTPATH+'seasons/')
    
    #analyse_coverage(LST_WARM_MAX, LST_COLD_MAX, LST_COLD_MIN, LONS, LATS, SEASON, OUTPATH+'seasons/')






'''


##############################################################
#Analysis of annual values - annual average, annual coverage #
##############################################################



#filepaths of all daily LST min/max files of one year to be analysed
FILEPATH = glob.glob('/scratch/vportge/CM_SAF_LST_MIN_MAX/'+str(YEAR)+'/*/*.nc')
FILEPATH.sort()


#load LST data
LST_WARM_MAX = iris.load(FILEPATH, 'Maximum Land Surface Temperature in Warm Window (PMW)')
LST_WARM_MAX = LST_WARM_MAX.concatenate_cube()

LST_COLD_MAX = iris.load(FILEPATH, 'Maximum Land Surface Temperature in Cold Window (PMW)')
LST_COLD_MAX = LST_COLD_MAX.concatenate_cube()

LST_COLD_MIN = iris.load(FILEPATH, 'Minimum Land Surface Temperature in Cold Window (PMW)')
LST_COLD_MIN = LST_COLD_MIN.concatenate_cube()

#get longitudes and latitudes of grid
LONS = LST_WARM_MAX.coord('longitude').points
LATS = LST_WARM_MAX.coord('latitude').points


#Compute annual average and plot it
ANNUAL_AVERAGE_LST_WARM_MAX = LST_WARM_MAX.collapsed('time', iris.analysis.MEAN)
ANNUAL_AVERAGE_LST_COLD_MAX = LST_COLD_MAX.collapsed('time', iris.analysis.MEAN)
ANNUAL_AVERAGE_LST_COLD_MIN = LST_COLD_MIN.collapsed('time', iris.analysis.MEAN)


pcolormesh_map(ANNUAL_AVERAGE_LST_WARM_MAX.data, LONS, LATS, 'LST in K',
               'Annual average of max LST in warm window ', 'annual_average_LST_max_warm_', OUTPATH)
pcolormesh_map(ANNUAL_AVERAGE_LST_COLD_MAX.data, LONS, LATS, 'LST in K',
               'Annual average of max LST in cold window ', 'annual_average_LST_max_cold_', OUTPATH)
pcolormesh_map(ANNUAL_AVERAGE_LST_COLD_MIN.data, LONS, LATS, 'LST in K',
               'Annual average of min LST in cold window ', 'annual_average_LST_min_cold_', OUTPATH)

#Analyse Coverage and plot it
print('start coverage analysis')
LST_WARM_MAX_DATA = LST_WARM_MAX.data
LST_COLD_MAX_DATA = LST_COLD_MAX.data
LST_COLD_MIN_DATA = LST_COLD_MIN.data

COVERAGE_LST_WARM_MAX = np.ma.MaskedArray.count(LST_WARM_MAX_DATA, axis=0)
COVERAGE_LST_COLD_MAX = np.ma.MaskedArray.count(LST_COLD_MAX_DATA, axis=0)
COVERAGE_LST_COLD_MIN = np.ma.MaskedArray.count(LST_COLD_MIN_DATA, axis=0)


pcolormesh_map(COVERAGE_LST_WARM_MAX, LONS, LATS,
               'Number of days per year where LST measurement was possible',
               'Coverage - max LST in warm window ', 'coverage_LST_max_warm_', OUTPATH)
pcolormesh_map(COVERAGE_LST_COLD_MAX, LONS, LATS,
               'Number of days per year where LST measurement was possible',
               'Coverage - max LST in cold window ', 'coverage_LST_max_cold_', OUTPATH)
pcolormesh_map(COVERAGE_LST_COLD_MIN, LONS, LATS,
               'Number of days per year where LST measurement was possible',
               'Coverage - min LST in cold window ', 'coverage_LST_min_cold_', OUTPATH)

'''



'''
for YEAR in range(1991,1992):
    filepath=glob.glob('/scratch/vportge/CM_SAF_LST_MIN_MAX/'+str(YEAR)+'/*/*.nc') #filepaths of all daily LST min/max files of one year to be analysed.
    LST_warm_max=iris.load(filepath, 'Maximum Land Surface Temperature in Warm Window (PMW)')
    LST_warm_max=LST_warm_max.concatenate_cube()
    LONS=LST_warm_max.coord('longitude').points 
    LATS=LST_warm_max.coord('latitude').points 


    #Compute annual average and plot it
    annual_average_LST_warm_max = LST_warm_max.collapsed('time', iris.analysis.MEAN)
    plt.close()
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1,projection=ccrs.PlateCarree())
    lst_map=plt.pcolormesh(LONS, LATS, annual_average_LST_warm_max.data, transform=ccrs.PlateCarree()) #This takes some time, I think the average gets calculated now
    bar = plt.colorbar(lst_map, orientation='horizontal', extend='both')
    ax.coastlines()
    plt.title('Annual average LST max warm window')
    plt.savefig('/scratch/vportge/plots/CM_SAF/annual_average_LST_max_warm_'+str(YEAR)+'.png')



    #Analyse Coverage and plot it
    print('start coverage analysis')
    LST_warm_max_data=LST_warm_max.data
    COVERAGE_LST_WARM_MAX=np.ma.MaskedArray.count(LST_warm_max_data, axis=0)
    plt.close()
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1,projection=ccrs.PlateCarree())
    lst_map=plt.pcolormesh(LONS, LATS, COVERAGE_LST_WARM_MAX, transform=ccrs.PlateCarree()) #This takes some time, I think the average gets calculated now
    bar = plt.colorbar(lst_map, orientation='horizontal', extend='both')
    ax.coastlines()
    plt.title('Coverage LST max warm window')
    plt.savefig('/scratch/vportge/plots/CM_SAF/coverage_LST_max_warm_'+str(YEAR)+'.png')
    print('end coverage analysis')

'''

#uncomment for doing comparison with Lizzie's Plots

'''
dates= ['20100705', '20100710', '20100730', '20100801']


#hourly_data=iris.load(hourly_data_path,


for date in dates:
	data_path='/scratch/vportge/CM_SAF_LST_MIN_MAX/2010/'+date[4:6]+'/LST_max_and_min_'+date+'.nc'
	print(data_path)
	data=iris.load(data_path)
	print(data)
	LSTcoldmax=data[4]
	LSTcoldmin=data[2]
	LSTwarmmax=data[0]
	
	time=LSTcoldmax[0].coord('time').points
	lat=LSTcoldmax[0].coord('latitude').points
	lon=LSTcoldmax[0].coord('longitude').points

	LSTcoldmax_deg_C=LSTcoldmax[0].data-273.15
	LSTcoldmin_deg_C=LSTcoldmin[0].data-273.15
	LSTwarmmax_deg_C=LSTwarmmax[0].data-273.15

	np.clip(LSTcoldmax_deg_C, 10, 50, LSTcoldmax_deg_C)
	np.clip(LSTcoldmin_deg_C, 10, 50, LSTcoldmin_deg_C)
	np.clip(LSTwarmmax_deg_C, 10, 50, LSTwarmmax_deg_C)

	#compare_with_lizzies_figures(LSTcoldmax_deg_C, lon, lat, 'maximum LST in cold window', date+'_cold_max' )
	#compare_with_lizzies_figures(LSTcoldmin_deg_C, lon, lat, 'minimum LST in cold window', date+ '_cold_min' )
	#compare_with_lizzies_figures(LSTwarmmax_deg_C, lon, lat, 'maximum LST in warm window', date+ '_warm_max' )
	

	plt.close()
	fig = plt.figure(figsize=(16,9))
	ax1 = fig.add_subplot(2,2,  1,projection=ccrs.PlateCarree())
	ax2 = fig.add_subplot(2,2,  2,projection=ccrs.PlateCarree())
	ax3 = fig.add_subplot(2,2,  3,projection=ccrs.PlateCarree())

	lst_map1=ax1.pcolormesh(lon, lat, LSTcoldmin_deg_C, transform=ccrs.PlateCarree(), cmap='spectral', vmin=10, vmax=50)
	lst_map2=ax2.pcolormesh(lon, lat, LSTcoldmax_deg_C, transform=ccrs.PlateCarree(), cmap='spectral', vmin=10, vmax=50)
	lst_map3=ax3.pcolormesh(lon, lat, LSTwarmmax_deg_C, transform=ccrs.PlateCarree(), cmap='spectral', vmin=10, vmax=50)

	ax1.set_title('LST minimum in cold window')
	ax2.set_title('LST maximum in cold window')
	ax3.set_title('LST maximum in warm window')



	ax1.coastlines()
	ax2.coastlines()
	ax3.coastlines()

	cbar_ax = fig.add_axes([0.15, 0.05,  0.7, 0.02])
	fig.colorbar(lst_map1, orientation='horizontal', extend='both', cax=cbar_ax)
	plt.title('CM SAF (clipped to 10 - 50 deg C) '+date)

	fig.tight_layout()
	plt.savefig('/home/h01/vportge/CM_SAF/plots/compare_with_lizzies_plots/CM_SAF_map_LST_'+date+'.png')


'''


#plot with filled contours
#plot_map_of_cube(day_cube[0,:,:])	

#plot daily cycle:
#plot=plot_daily_cycle(day_data[:,179,1592])

#plot LST max and min
#plot_figure(LSTwarm_max, LONS, LATS, 'max LST '+str(day_yyyymmdd),  str(day_yyyymmdd))
#plot_figure(LSTcold_min, LONS, LATS, 'min LST '+str(day_yyyymmdd),  str(day_yyyymmdd))
