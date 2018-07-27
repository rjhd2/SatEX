# -*- coding: iso-8859-1 -*-
import numpy as np
import iris
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import iris.quickplot as qplt
#import matplotlib.cm as mpl_cm
#import iris.plot as iplt
import cartopy.crs as ccrs
#import cartopy.feature as cfeature
import glob
#from iris.util import unify_time_units
#import datetime
#import numpy.ma as ma
import sys
#import requests

def load_min_max_LST(season_filepath):
    lst_warm_max = iris.load(season_filepath, 'Coverage of Maximum Land Surface Temperature in Warm Window (PMW)')
    lst_cold_max = iris.load(season_filepath, 'Coverage of Maximum Land Surface Temperature in Cold Window (PMW)')
    lst_cold_min = iris.load(season_filepath, 'Coverage of Minimum Land Surface Temperature in Cold Window (PMW)')

    num_of_years = len(lst_warm_max)

    lst_warm_max_data = np.zeros((num_of_years, 856, 2171))
    lst_cold_max_data = np.zeros((num_of_years, 856, 2171))
    lst_cold_min_data = np.zeros((num_of_years, 856, 2171))

    for i in range(num_of_years):
        lst_warm_max_data[i, :] = lst_warm_max[i].data
        lst_cold_max_data[i, :] = lst_cold_max[i].data
        lst_cold_min_data[i, :] = lst_cold_min[i].data

    average_lst_warm_max = np.mean(lst_warm_max_data, axis = 0)
    average_lst_cold_max = np.mean(lst_cold_max_data, axis = 0)
    average_lst_cold_min = np.mean(lst_cold_min_data, axis = 0)

    return lst_warm_max_data, lst_cold_max_data, lst_cold_min_data, average_lst_warm_max, average_lst_cold_max, average_lst_cold_min


def pcolormesh_map(data, lons, lats, cbar_label, titlestring, filename, outpath):
    '''Plot annual average on a map.'''

    if SEASON=='DJF':
        divide_days = 90.25
    elif SEASON == 'MAM':
        divide_days = 92.
    elif SEASON == 'JJA':
        divide_days = 92.
    elif SEASON == 'SON':
        divide_days = 91.

    plt.close()
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    #This takes some time, I think the average gets calculated now
    lst_map = plt.pcolormesh(lons, lats, data*100./divide_days, transform=ccrs.PlateCarree(), vmin=0.0001, vmax=100)
    lst_map.cmap.set_under('white')


    cbar = plt.colorbar(lst_map, orientation='horizontal', extend='both')
    cbar.set_label(cbar_label)
    ax1.coastlines()
    plt.title(titlestring)
    plt.savefig(outpath+filename+'.png')
    return


DATADIR = '/scratch/vportge/CM_SAF_LST_MIN_MAX/COVERAGE/'
OUTPATH = '/scratch/vportge/plots/CM_SAF/'



GET_COORDINATES_PATH = '/scratch/vportge/CM_SAF_LST_MIN_MAX/1991/01/LST_max_and_min_19910101.nc'
GET_COORDINATES_DATA = iris.load(GET_COORDINATES_PATH)
LONS = GET_COORDINATES_DATA[0].coord('longitude').points
LATS = GET_COORDINATES_DATA[0].coord('latitude').points


DJF_YEARS = []
MAM_YEARS = []
JJA_YEARS = []
SON_YEARS = []

for YEAR in range(1992, 2016):
    for i in range(4):
        if i == 0:
            SEASON = 'DJF'
            DJF = glob.glob(DATADIR+str(YEAR)+'/*_DJF*.nc')


        elif i == 1:
            SEASON = 'MAM'
            MAM = glob.glob(DATADIR+str(YEAR)+'/*_MAM*.nc')

        elif i == 2:
            SEASON = 'JJA'
            JJA = glob.glob(DATADIR+str(YEAR)+'/*_JJA*.nc')


        elif i == 3:
            SEASON = 'SON'
            SON = glob.glob(DATADIR+str(YEAR)+'/*_SON*.nc')


    DJF_YEARS = DJF_YEARS + DJF
    MAM_YEARS = MAM_YEARS + MAM
    JJA_YEARS = JJA_YEARS + JJA
    SON_YEARS = SON_YEARS + SON

DJF_YEARS.sort()

for i in range(4):
    if i == 0:
        SEASON = 'DJF'
        LST_WARM_MAX, LST_COLD_MAX, LST_COLD_MIN, AVERAGE_LST_WARM_MAX, AVERAGE_LST_COLD_MAX, AVERAGE_LST_COLD_MIN = load_min_max_LST(DJF_YEARS)
        AVERAGE_LST_WARM_DJF = AVERAGE_LST_WARM_MAX*1
        AVERAGE_LST_COLD_DJF = AVERAGE_LST_COLD_MIN*1

    elif i == 1:
        SEASON = 'MAM'
        LST_WARM_MAX, LST_COLD_MAX, LST_COLD_MIN, AVERAGE_LST_WARM_MAX, AVERAGE_LST_COLD_MAX, AVERAGE_LST_COLD_MIN = load_min_max_LST(MAM_YEARS)
        AVERAGE_LST_WARM_MAM = AVERAGE_LST_WARM_MAX*1
        AVERAGE_LST_COLD_MAM = AVERAGE_LST_COLD_MIN*1

    elif i == 2:
        SEASON = 'JJA'
        LST_WARM_MAX, LST_COLD_MAX, LST_COLD_MIN, AVERAGE_LST_WARM_MAX, AVERAGE_LST_COLD_MAX, AVERAGE_LST_COLD_MIN = load_min_max_LST(JJA_YEARS)
        AVERAGE_LST_WARM_JJA = AVERAGE_LST_WARM_MAX*1
        AVERAGE_LST_COLD_JJA = AVERAGE_LST_COLD_MIN*1

    elif i == 3:
        SEASON = 'SON'
        LST_WARM_MAX, LST_COLD_MAX, LST_COLD_MIN, AVERAGE_LST_WARM_MAX, AVERAGE_LST_COLD_MAX, AVERAGE_LST_COLD_MIN = load_min_max_LST(SON_YEARS)
        AVERAGE_LST_WARM_SON = AVERAGE_LST_WARM_MAX*1
        AVERAGE_LST_COLD_SON = AVERAGE_LST_COLD_MIN*1

    pcolormesh_map(AVERAGE_LST_WARM_MAX, LONS, LATS, '% of possible days that could have been observed', SEASON+' coverage - LST in warm window ', SEASON+'_coverage_LST_max_warm_', OUTPATH)
    #pcolormesh_map(AVERAGE_LST_COLD_MAX, LONS, LATS, '% of possible days that could have been observed', SEASON+' coverage - max LST in cold window ', SEASON+'_coverage_LST_max_cold_', OUTPATH)
    pcolormesh_map(AVERAGE_LST_COLD_MIN, LONS, LATS, '% of possible days that could have been observed', SEASON+' coverage -  LST in cold window ', SEASON+'_coverage_LST_min_cold_', OUTPATH)







fig = plt.figure(figsize=(16,12))
ax1 = fig.add_subplot(2, 2, 1, projection=ccrs.PlateCarree())
ax2 = fig.add_subplot(2, 2, 2, projection=ccrs.PlateCarree())
ax3 = fig.add_subplot(2, 2, 3, projection=ccrs.PlateCarree())
ax4 = fig.add_subplot(2, 2, 4, projection=ccrs.PlateCarree())

lst_map1=ax1.pcolormesh(LONS, LATS, AVERAGE_LST_COLD_DJF*100./90.25, transform=ccrs.PlateCarree(), cmap='jet', vmin=0.0001, vmax=100)
lst_map2=ax2.pcolormesh(LONS, LATS, AVERAGE_LST_COLD_MAM*100./92., transform=ccrs.PlateCarree(), cmap='jet', vmin=0.0001, vmax=100)
lst_map3=ax3.pcolormesh(LONS, LATS, AVERAGE_LST_COLD_JJA*100./92., transform=ccrs.PlateCarree(), cmap='jet', vmin=0.0001, vmax=100)
lst_map4=ax4.pcolormesh(LONS, LATS, AVERAGE_LST_COLD_SON*100./91., transform=ccrs.PlateCarree(), cmap='jet', vmin=0.0001, vmax=100)

lst_map1.cmap.set_under('white')
lst_map2.cmap.set_under('white')
lst_map3.cmap.set_under('white')
lst_map4.cmap.set_under('white')

ax1.set_title('DJF', size=20)
ax2.set_title('MAM', size=20)
ax3.set_title('JJA', size=20)
ax4.set_title('SON', size=20)

ax1.coastlines()
ax2.coastlines()
ax3.coastlines()
ax4.coastlines()

cbar_ax = fig.add_axes([0.15, 0.07,  0.7, 0.04])
cbar = fig.colorbar(lst_map1, orientation='horizontal', extend='both', cax=cbar_ax)
cbar.ax.tick_params(labelsize = 20)
cbar.set_label('% of possible days that could have been observed', size=20)

fig.suptitle('Average coverage of LST in cold window', size=24)
plt.tight_layout()

plt.savefig(OUTPATH+'coverage_LST_cold.png')


plt.close()
fig = plt.figure(figsize=(16,12))
ax1 = fig.add_subplot(2, 2, 1, projection=ccrs.PlateCarree())
ax2 = fig.add_subplot(2, 2, 2, projection=ccrs.PlateCarree())
ax3 = fig.add_subplot(2, 2, 3, projection=ccrs.PlateCarree())
ax4 = fig.add_subplot(2, 2, 4, projection=ccrs.PlateCarree())

lst_map1=ax1.pcolormesh(LONS, LATS, AVERAGE_LST_WARM_DJF*100./90.25, transform=ccrs.PlateCarree(), cmap='jet', vmin=0.0001, vmax=100)
lst_map2=ax2.pcolormesh(LONS, LATS, AVERAGE_LST_WARM_MAM*100./92., transform=ccrs.PlateCarree(), cmap='jet', vmin=0.0001, vmax=100)
lst_map3=ax3.pcolormesh(LONS, LATS, AVERAGE_LST_WARM_JJA*100./92., transform=ccrs.PlateCarree(), cmap='jet', vmin=0.0001, vmax=100)
lst_map4=ax4.pcolormesh(LONS, LATS, AVERAGE_LST_WARM_SON*100./91., transform=ccrs.PlateCarree(), cmap='jet', vmin=0.0001, vmax=100)

lst_map1.cmap.set_under('white')
lst_map2.cmap.set_under('white')
lst_map3.cmap.set_under('white')
lst_map4.cmap.set_under('white')

ax1.set_title('DJF', size=20)
ax2.set_title('MAM', size=20)
ax3.set_title('JJA', size=20)
ax4.set_title('SON', size=20)

ax1.coastlines()
ax2.coastlines()
ax3.coastlines()
ax4.coastlines()

cbar_ax = fig.add_axes([0.15, 0.07,  0.7, 0.04])
cbar = fig.colorbar(lst_map1, orientation='horizontal', extend='both', cax=cbar_ax)
cbar.ax.tick_params(labelsize = 20)
cbar.set_label('% of possible days that could have been observed', size=20)

fig.suptitle('Average coverage of LST in warm window', size=24)
plt.tight_layout()
plt.savefig(OUTPATH+'coverage_LST_warm.png')


#DJF: 90 / 91, MAM: 92, JJA: 92, SON: 91 