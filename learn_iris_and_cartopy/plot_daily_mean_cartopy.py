import numpy as np
import iris
import matplotlib.pyplot as plt
import iris.quickplot as qplt
import matplotlib.cm as mpl_cm
import iris.plot as iplt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

filepath='/scratch/vportge/test_data_CM_SAF/ORD28977/ORD28977_1/LTPin199201010000001UD1000101UD.nc'
testdata=iris.load(filepath, 'Land Surface Temperature (PMW)')
LST=testdata[0]
daily_mean = LST.collapsed('time', iris.analysis.MEAN)

 
# turn the iris Cube data structure into numpy arrays
gridlons = daily_mean.coord('longitude').contiguous_bounds()
gridlats = daily_mean.coord('latitude').contiguous_bounds()
daily_mean_data = daily_mean.data

#plot daily mean data
plt.interactive(True)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1,projection=ccrs.PlateCarree())
plt.contourf(gridlons[:-1], gridlats[:-1], daily_mean_data, transform=ccrs.PlateCarree())
ax.coastlines()
plt.close()

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1,projection=ccrs.PlateCarree())
lst_map=iplt.pcolormesh(daily_mean)
ax.coastlines()
plot_title='Daily Mean LST'
bar = plt.colorbar(lst_map, orientation='horizontal', extend='both')
plt.title(plot_title)

