import numpy as np
import iris
import matplotlib.pyplot as plt
import iris.quickplot as qplt
import matplotlib.cm as mpl_cm
import iris.plot as iplt
import cartopy.crs as ccrs
import cartopy.feature as cfeature


def plot_figure(data):
	fig=plt.figure()
	plt.imshow(data[::-1]) #imshow mirrors the image somehow. 
	plt.colorbar()
	plt.show()
	return

filepath='/home/h01/vportge/CM_SAF/test_data/ORD28974_europe/ORD28974/LTPin201511010100001UD1000101UD.nc'
testdata=iris.load(filepath, 'Land Surface Temperature (PMW)')
LST=testdata[0]

LST1=LST.data[0,:,:]

plot_figure(LST1)


#or use quickplot for plotting:
contour=qplt.contour(LST[0,:,:]) #take first hour of something
plt.clabel(contour,inline=False) #label contour lines

plt.show()
#plt.close()
#new plot with filled contours
qplt.contourf(LST[0,:,:])
plt.gca().coastlines() #add coastlines
plt.show()
#plt.close()
# Draw the block plot.
brewer_cmap = mpl_cm.get_cmap('brewer_OrRd_09') #colormap, see http://colorbrewer2.org/
qplt.pcolormesh(LST[0,:,:],cmap=brewer_cmap)
iplt.citation(iris.plot.BREWER_CITE)


#interpolate to specific sample point:
sample_points=[('latitude', 48.0), ('longitude', 11.5)]
print(LST[0,:,:].interpolate(sample_points, iris.analysis.Linear()))#.data


#plot daily cycle:
daily_cycle=LST[:,179,1592] #some random location
fig=plt.figure()
plt.plot(daily_cycle.data)
plt.grid()
plt.title('daily cycle for lat 179 lon 1592 gridpoints')

#calculate daily mean
daily_mean = LST.collapsed('time', iris.analysis.MEAN)
print(daily_mean)

fig=plt.figure()
plt.contourf(daily_mean.data, cmap='jet')
plt.title('Daily mean land surface temperature') 
#plt.gca().coastlines() #add coastlines
plt.show()

plt.close()

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.coastlines()
ax.gridlines()
