import numpy as np
import iris
import iris.quickplot as qplt
import iris.plot as iplt
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
from   cartopy.mpl.gridliner import LATITUDE_FORMATTER
import glob
import cartopy.feature as cfeat


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

lat_tiles.guess_bounds()
lon_tiles.guess_bounds()

lat_all = np.append(lat_points, lat_points[-1]+3.85)
lon_all = np.append(lon_points[0]-6.5, lon_points)



coord_sys = ccrs.PlateCarree()

ax = plt.axes(projection=coord_sys)
ax.coastlines()
ax.add_feature(cfeat.LAND)
ax.add_feature(cfeat.OCEAN)
gl = ax.gridlines(draw_labels=True, linestyle='-')
ax.set_extent([np.amin(lon_tiles.points)-8, np.amax(lon_tiles.points)+3, np.amin(lat_tiles.points)-3, np.amax(lat_tiles.points)+8], crs=coord_sys)
#gl.xlocator = mticker.FixedLocator(lon_tiles.points)
#gl.ylocator = mticker.FixedLocator(lat_tiles.points)

gl.xlocator = mticker.FixedLocator(lon_all)
gl.ylocator = mticker.FixedLocator(lat_all)

#tileshape = TILES_SHAPES[10].split(',')
#ax.scatter(lon_points[10], lat_points[10],color = 'red', s = 10)

for i in range(len(TILES_SHAPES)):
    tileshape = TILES_SHAPES[i].split(',')
    lat1 = float(lat[tileshape[0]].points)+0.5
    lon1 = float(lon[tileshape[2]].points)+0.5
    plt.text(lon1, lat1, i, color = 'indianred', fontsize = 16)

plt.title('Map of the region split up into 96 different tiles', y=1.08, fontsize=18)

plt.show()





