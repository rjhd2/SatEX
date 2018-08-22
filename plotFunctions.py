# -*- coding: iso-8859-1 -*-
import numpy as np
import iris
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as mpl_cm
import iris.quickplot as qplt
import iris.plot as iplt
import cartopy.crs as ccrs
import cartopy.feature as cfeat
import copy
from mpl_toolkits.axes_grid1 import AxesGrid
from numpy import ma
from matplotlib import cbook
from matplotlib.colors import Normalize
import matplotlib.colors as mcolors
def line(x,t,m):
    '''Plot a line. '''
    return m*x+t


def plot_figure(data, gridlons, gridlats, figure_info):
    """Plot map of index for some day.
    figure_info = [title, unit, outpath, region, outname, cbar_dict]
    """
    title = figure_info[0]
    unit = figure_info[1]
    outpath = figure_info[2]
    region = figure_info[3]
    outname = figure_info[4]
    cbar_dict = figure_info[5]

    plt.close()
    fig = plt.figure(figsize = (10, 8))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    cbar_value = np.amax(abs(data))
    vmin = np.amin(data)
    vmax = np.amax(data)

    colors1 = plt.cm.ocean(np.linspace(0, 1, 256))
    colors2 = plt.cm.gist_heat_r(np.linspace(0, 1, 256))
    colors = np.vstack((colors1, colors2))
    my_cmap = mcolors.LinearSegmentedColormap.from_list('colormap', colors)



    if cbar_dict == False:
        if vmin <=0. and vmax >=0:
            lst_map = plt.pcolormesh(gridlons, gridlats, data, transform=ccrs.PlateCarree(), cmap=my_cmap, vmin = -cbar_value, vmax = cbar_value)
        elif vmin <=0 and vmax<=0:
            lst_map = plt.pcolormesh(gridlons, gridlats, data, transform=ccrs.PlateCarree(), cmap = 'ocean', vmin = vmin, vmax = 0.)
        elif vmin >=0 and vmax>=0:
            lst_map = plt.pcolormesh(gridlons, gridlats, data, transform=ccrs.PlateCarree(), cmap = 'gist_heat_r', vmin = 0, vmax = vmax)

    else:
        vmin_cbar = float(cbar_dict[0])
        vmax_cbar = float(cbar_dict[1])

        max_vmax = np.amax([abs(vmin_cbar), vmax_cbar])

        if vmin <=0. and vmax >=0:
            lst_map = plt.pcolormesh(gridlons, gridlats, data, transform=ccrs.PlateCarree(), cmap=my_cmap, vmin = -max_vmax, vmax = max_vmax)
            #lst_map.cmap.set_under('blue')
            #lst_map.cmap.set_over('red')

        elif vmin <=0 and vmax<=0:
            lst_map = plt.pcolormesh(gridlons, gridlats, data, transform=ccrs.PlateCarree(), cmap = my_cmap, vmin = vmin_cbar, vmax = -vmin_cbar)
            #lst_map.cmap.set_under('blue')
            #lst_map.cmap.set_over('red')
        elif vmin >=0 and vmax>=0:
            lst_map = plt.pcolormesh(gridlons, gridlats, data, transform=ccrs.PlateCarree(), cmap = my_cmap, vmin = -vmax_cbar, vmax = vmax_cbar)
            #lst_map.cmap.set_under('blue')
            #lst_map.cmap.set_over('red')
    #plt.show()
    cbar = plt.colorbar(lst_map, orientation='horizontal', extend='both')

    #cbar = plt.colorbar(lst_map, orientation='horizontal')
    ax.set_extent((np.amin(gridlons)-0.5, np.amax(gridlons)+0.5, np.amin(gridlats)-0.5, np.amax(gridlats)+0.5), crs = ccrs.PlateCarree())
    ax.add_feature(cfeat.LAND)
    ax.add_feature(cfeat.OCEAN)

    political_bdrys = cfeat.NaturalEarthFeature(category='cultural',
                                                name='admin_0_countries',
                                                scale='50m')
    ax.add_feature(political_bdrys, edgecolor='b', facecolor='none', zorder=2)
    gl = ax.gridlines(draw_labels=True)
    plt.title(title, y=1.08, size=22)
    cbar.set_label(unit+' per decade', size=20)
    #plt.show()
    plt.savefig(outname)
    return [vmin, vmax]

def plot_time_series_with_trend(cube, infos, units_dict):
    ''' Plot a time series with trends for the whole time period, the first period
        from 1991-2004 and the second period from 2005-2015 using the MedianPairwiseSlopes function
        cube should be a cube of the annual values along the time axis
        infos is a list of different infos which can be used for plotting the title or the filename
        units_dict: the unit of the index.'''

    #infos = [TITLE_TIME, INAME, REGION, TIMERANGE, OUTPATH, instrument]

    #extract some information for the title or the filename.
    title_time = infos[0]
    iname = infos[1]
    region = infos[2]
    timerange = infos[3]
    outpath = infos[4]
    instrument = infos[5]
    time_factor = infos[6]

    #The 2006 value is biased due to Dec 14th 2006 where extremely high LST values
    #were measured. This excludes the year 2006 from the plot. But actually it shouldn't be extracted. 
    exclude_2006_constraint = iris.Constraint(time = lambda c: c.point.year != 2006)
    cube = cube.extract(exclude_2006_constraint)

    #First period where MVIRI was measuring was until end of 2004
    time_constraint1 = iris.Constraint(time=lambda c: c.point.year < 2005)
    cube1 = cube.extract(time_constraint1)

    #Second period where SEVIRI measured began in 2005
    time_constraint2 = iris.Constraint(time=lambda c: c.point.year > 2004)
    cube2 = cube.extract(time_constraint2)

    #compute the trend for the whole time period
    ydata = cube.data
    xdata = cube.coord('time').points
    mdi  = ydata.mask
    trendanalysis = MedianPairwiseSlopes(xdata,ydata)
    slope = trendanalysis[0]
    y_interception = trendanalysis[3]
    trendcube = copy.deepcopy(cube)
    trendcube.rename('Trend')
    trendcube.data=line(xdata, y_interception, slope)

    #compute the trend for the first time period
    ydata1 = cube1.data
    xdata1 = cube1.coord('time').points
    mdi1  = ydata1.mask
    trendanalysis1 = MedianPairwiseSlopes(xdata1,ydata1)
    slope1 = trendanalysis1[0]
    y_interception1 = trendanalysis1[3]
    trendcube1 = copy.deepcopy(cube1)
    trendcube1.rename('Trend')
    trendcube1.data=line(xdata1, y_interception1, slope1)

    #compute the trend for the second time period
    ydata2 = cube2.data
    xdata2 = cube2.coord('time').points
    mdi2  = ydata2.mask
    trendanalysis2 = MedianPairwiseSlopes(xdata2,ydata2)
    slope2 = trendanalysis2[0]
    y_interception2 = trendanalysis2[3]
    trendcube2 = copy.deepcopy(cube2)
    trendcube2.rename('Trend')
    trendcube2.data=line(xdata2, y_interception2, slope2)


    #Begin plot#
    plt.close()
    fig=plt.figure(figsize = (10, 8))
    iplt.plot(cube)
    plt.grid()
    plt.title('Time series of '+title_time+' '+instrument+' ' + iname + ' in ' + region , size=22)
    plt.ylabel(units_dict[iname], size=20)
    plt.xlabel('years', size=20)

    iplt.plot(trendcube, label='trend: '+str(round(slope*time_factor,2))+' '+units_dict[iname]+' per decade' + ' (1991-2015)')
    iplt.plot(trendcube1, label='trend: '+str(round(slope1*time_factor,2))+' '+units_dict[iname]+' per decade' +  ' (1991-2004)')
    iplt.plot(trendcube2, label='trend: '+str(round(slope2*time_factor,2))+' '+units_dict[iname]+' per decade' + ' (2005-2015)')

    plt.legend(fontsize = 16, loc = 'best')
    plt.tight_layout()
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.savefig(outpath+iname+'_with_trend_'+timerange+'_'+region+'.png')

    return [str(round(slope*time_factor,2)), str(round(slope1*time_factor,2)), str(round(slope2*time_factor,2))]



#***************************************
def MedianPairwiseSlopes(xdata,ydata):
    '''
    Calculate the median of the pairwise slopes

    :param array xdata: x array
    :param array ydata: y array
    :param float mdi: missing data indicator
    :param bool mult10: multiply output trends by 10 (to get per decade)
    :returns: float of slope
    '''
    # sort xdata

    slopes=[]
    for i in range(len(xdata)):
        for j in range(i+1,len(xdata)):
            slopes += [(ydata[j]-ydata[i])/(xdata[j]-xdata[i])]

    mpw=np.ma.median(np.ma.array(slopes))
    y_intercept_point = np.median(ydata)-mpw*np.median(xdata)
    # copied from median_pairwise.pro methodology (Mark McCarthy)
    slopes.sort()
    n=len(ydata)

    try:

        dof=n*(n-1)/2
        w=np.sqrt(n*(n-1)*((2.*n)+5.)/18.)

        rank_upper=((dof+1.96*w)/2.)+1
        rank_lower=((dof-1.96*w)/2.)+1

        if rank_upper >= len(slopes): rank_upper=len(slopes)-1
        if rank_upper < 0: rank_upper=0
        if rank_lower < 0: rank_lower=0

        upper=slopes[int(rank_upper)]
        lower=slopes[int(rank_lower)]
        return  mpw, lower, upper, y_intercept_point      # MedianPairwiseSlopes

    except:
        return  mpw, 'test', 'test', y_intercept_point      # MedianPairwiseSlopes


def open_file_with_cbar_extents(cbar_path):
    ''' Opens a file which contains the extents (lowest and highest values) of Climpact or Python Indices and saves
    values to a dictionary so that colors of GHCNDEX maps are adjusted to Climpact/Python. Better comparison possible.'''
    cbar_dict = {}
    with open(cbar_path) as f:
        cbar_extents = f.read().splitlines()

    for i in range(len(cbar_extents)):
        val = cbar_extents[i].split(',')
        cbar_dict[val[0]] = [val[1][2:], val[2][1:-1]]
    return cbar_dict


def plot_map_of_time_average(ann_data, infos):
    '''' Plot a map of the average values over the whole time period'''
    #CUBEINFO = [TITLE_TIME, INAME, REGION, TIMERANGE, OUTPATH, 'CM SAF', time_factor, UNITS_DICT[INAME]]
    
    title_time = infos[0]
    iname = infos[1]
    region = infos[2]
    timerange = infos[3]
    outpath = infos[4]
    instrument = infos[5]
    time_factor = infos[6]
    unit = infos[7]
 
    if ann_data.coord('time').has_bounds() == False:
        ann_data.coord('time').guess_bounds()

    ann_data_time_avg = ann_data.collapsed('time', iris.analysis.MEAN)
    ann_data_lon = ann_data_time_avg.coord('longitude').bounds
    ann_data_lat = ann_data_time_avg.coord('latitude').bounds


    plt.close()
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.add_feature(cfeat.LAND)
    ax.add_feature(cfeat.OCEAN)
    gl = ax.gridlines(draw_labels=True)
    ax.set_extent((np.amin(ann_data_lon)-0.5, np.amax(ann_data_lon)+0.5, np.amin(ann_data_lat)-0.5, np.amax(ann_data_lat)+0.5), crs = ccrs.PlateCarree())

    political_bdrys = cfeat.NaturalEarthFeature(category='cultural',
                                                name='admin_0_countries',
                                                scale='50m')
    ax.add_feature(political_bdrys, edgecolor='b', facecolor='none', zorder=2)

    if iname == 'TR':
        vmax = 170
    else:
        vmax = np.amax(ann_data_time_avg.data)

    cont = iplt.pcolormesh(ann_data_time_avg, cmap = mpl_cm.get_cmap('YlOrRd'), vmax = vmax)

    cb=fig.colorbar(cont, ax=ax, orientation='horizontal')
    cb.set_label(unit, size=22)

    plt.title('Map of averaged '+iname+' values '+'('+instrument+')', y=1.08, size=22)
    plt.savefig(outpath+iname+'_'+instrument+'_map_averaged_'+region+'.png')
    return

