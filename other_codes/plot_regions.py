import numpy as np
import iris
import iris.quickplot as qplt
import iris.plot as iplt
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
from   cartopy.mpl.gridliner import LATITUDE_FORMATTER


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

def plot_years(y, indexname):

    if TIMERANGE == 'ANN':
        title_time = 'annually'
    elif TIMERANGE == 'MON':
        title_time = 'monthly'
    elif TIMERANGE == 'DAY':
        title_time = 'daily'

    plt.close()
    fig=plt.figure()
    iplt.plot(y)
    plt.grid()
    plt.title(indexname+' ('+title_time+')', size=22)
    plt.ylabel(UNITS_DICT[INAME], size=20)
    plt.xlabel('years', size=20)
    plt.tick_params(axis='both', which='major', labelsize=16)

    #plt.show()
    #iplt.plot(trendcube)
    plt.savefig(OUTPATH+indexname+'_'+TIMERANGE+'.png')


def plot_figure(data, gridlons, gridlats, title):
    """Plot map of index for some day."""
    plt.close()
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    lst_map = plt.contourf(gridlons, gridlats, data, transform=ccrs.PlateCarree())
    cbar = plt.colorbar(lst_map, orientation='horizontal', extend='both')
    ax.coastlines()
    gl = ax.gridlines(draw_labels=True)
    plt.title(title, y=1.08, size=22)
    cbar.set_label(UNITS_DICT[INAME]+' per decade', size=20)
    plt.tight_layout()
    plt.savefig(OUTPATH+INAME+'_map_of_trend_'+TIMERANGE+'.png')
    return



INDIR = '/scratch/vportge/satex/calculated_indices_small_region/'
FILEPATHS = glob.glob(INDIR+'*.nc')
OUTPATH = '/scratch/vportge/plots/Climpact/'

#define the indices of the certain regions/tiles
TILES_SHAPES = []
for i in range(8): #latitudes
    for j in range(12): #longitudes
        TILES_SHAPES.append(str(77*i)+','+str(77*(i+1))+','+str(522+130*j)+','+str(522+130*(j+1))) #lower_lat, upper_lat, lower_lon, upper_lon

        #TILES_SHAPES.append(str(154*i)+':'+str(154*(i+1))+','+str(520*j)+':'+str(520*(j+1)))

testfile = iris.load_cube('/scratch/vportge/CM_SAF_LST_MIN_MAX/1991/01/LST_max_and_min_19910101.nc', "Maximum Land Surface Temperature in Warm Window (PMW)")
lon = testfile.coord('longitude')
lat = testfile.coord('latitude')


lat_tiles = lat[0:616][::77]
lon_tiles = lon[522+130::130]


lat_points = lat_tiles.points
lon_points = lon_tiles.points

coord_sys = ccrs.PlateCarree()

ax = plt.axes(projection=coord_sys)
ax.coastlines()
gl = ax.gridlines(draw_labels=True)
#ax.set_extent([np.amin(lon_tiles.points), np.amax(lon_tiles.points), np.amin(lat_tiles.points), np.amax(lat_tiles.points)], crs=coord_sys)
gl.xlocator = mticker.FixedLocator(lon_tiles.points)
gl.ylocator = mticker.FixedLocator(lat_tiles.points)
#tileshape = TILES_SHAPES[10].split(',')
#ax.scatter(lon_points[10], lat_points[10],color = 'red', s = 10)

for i in range(len(TILES_SHAPES)):
    tileshape = TILES_SHAPES[i].split(',')
    lat1 = float(lat[tileshape[0]].points)+0.5
    lon1 = float(lon[tileshape[2]].points)+0.5
    plt.text(lon1, lat1, i, color = 'red')



plt.show()





