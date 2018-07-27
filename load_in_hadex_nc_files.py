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

def plot_years(x,y):
    plt.close()
    fig=plt.figure()
    plt.plot(x,y)
    plt.grid()
    plt.title('Time series of global average '+indexname+' values (HadEX2)')
    plt.savefig('/home/h01/vportge/CM_SAF/plots/hadex_time_series_'+indexname+'.png')

def plot_map(data, lons, lats):
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent([ -30., 65., 30, 65. ], crs=ccrs.PlateCarree())

    cont = ax.contourf(lons, lats, year,transform=ccrs.PlateCarree(),cmap='nipy_spectral')
    ax.coastlines()
    cb=fig.colorbar(cont, ax=ax, orientation='horizontal')
    cb.set_label(indexname+' Index Value')
    plt.title('Map of '+indexname+' values (HadEX2) '+ str(CHOOSE_YEAR))
    plt.savefig('/home/h01/vportge/CM_SAF/plots/hadex_map_index_'+indexname+'_'+str(CHOOSE_YEAR)+'.png')


##############
#load in data#
##############

indexname='CDD' #Decide which index should be used:
CHOOSE_YEAR=2007
filepath='/project/hadobs2/hadex2/dataset/HadEX2_'+indexname+'_1901-2010_h2_mask_m4.nc'
data=iris.load(filepath)

data_values=data[0].data
LONS = data[0].coord('lon').points
LATS = data[0].coord('lat').points

years=np.arange(1901,2010+1)	
year=data[0].data[0,:,:]

##########################################
#compute the global average for some year#
##########################################
global_mean=data[0].collapsed('lat', iris.analysis.MEAN)
global_mean=global_mean.collapsed('lon', iris.analysis.MEAN)

######################################################
#Plot the data: Time Series and map of global average#
######################################################
plot_years(years, global_mean.data)
plot_map(data_values[CHOOSE_YEAR-1901, :, :], LONS, LATS)





