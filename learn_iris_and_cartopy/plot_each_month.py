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

def plot_map(data, date):
    #new plot with filled contours
    plt.close()
    qplt.contourf(data)
    plt.gca().coastlines() #add coastlines
    plt.title('2006, month: '+date)
    plt.savefig('/home/h01/vportge/CM_SAF/plots/CM_SAF/2006_month_'+date+'.png')


for i in range(1,13):
    if i<10:
        f=glob.glob('/scratch/vportge/CM_SAF_data_metadata_changed/2006/0'+str(i)+'/*.nc')
    else:
        f=glob.glob('/scratch/vportge/CM_SAF_data_metadata_changed/2006/'+str(i)+'/*.nc')
 

    f=f[0]

    data=iris.load(f)[1][0]


    plot_map(data, str(i))

    


