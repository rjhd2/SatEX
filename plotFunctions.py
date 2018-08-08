# -*- coding: iso-8859-1 -*-
import numpy as np
import iris
import matplotlib.pyplot as plt
import iris.quickplot as qplt
import iris.plot as iplt
import cartopy.crs as ccrs
import cartopy.feature as cfeat
import copy


def line(x,t,m):
    '''Plot a line. '''
    return m*x+t


def plot_figure(data, gridlons, gridlats, title, units_dict, indexname, outpath, region):
    """Plot map of index for some day."""
    plt.close()
    fig = plt.figure(figsize = (10, 8))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    cbar_value = np.amax(abs(data))
    lst_map = plt.pcolormesh(gridlons, gridlats, data, transform=ccrs.PlateCarree(), cmap = 'RdBu_r', vmin = -cbar_value, vmax = cbar_value)
    cbar = plt.colorbar(lst_map, orientation='horizontal', extend='both')
    ax.set_extent((np.amin(gridlons)-0.5, np.amax(gridlons)+0.5, np.amin(gridlats)-0.5, np.amax(gridlats)+0.5), crs = ccrs.PlateCarree())

    political_bdrys = cfeat.NaturalEarthFeature(category='cultural',
                                                name='admin_0_countries',
                                                scale='50m')
    ax.add_feature(political_bdrys, edgecolor='b', facecolor='none', zorder=2)
    gl = ax.gridlines(draw_labels=True)
    plt.title(title, y=1.08, size=22)
    cbar.set_label(units_dict[indexname]+' per decade', size=20)
    plt.savefig(outpath+indexname+'_map_of_trend_'+region+'.png')
    return

def plot_time_series_with_trend(cube, infos, units_dict):
    ###############################################################
    #Compute the Trend for the 1991/01/01 - 2004/12/31 time period#
    ###############################################################

    #infos = [TITLE_TIME, INAME, REGION, TIMERANGE, OUTPATH, instrument]

    title_time = infos[0]
    iname = infos[1]
    region = infos[2]
    timerange = infos[3]
    outpath = infos[4]
    instrument = infos[5]
    time_factor = infos[6]

    time_constraint1 = iris.Constraint(time=lambda c: c.point.year < 2005)
    cube1 = cube.extract(time_constraint1)

    time_constraint2 = iris.Constraint(time=lambda c: c.point.year > 2004)
    cube2 = cube.extract(time_constraint2)

    ydata = cube.data
    xdata = cube.coord('time').points
    mdi  = ydata.mask
    trendanalysis = MedianPairwiseSlopes(xdata,ydata,mdi,mult10 = False, sort = False, calc_with_mdi=True)
    slope = trendanalysis[0]
    y_interception = trendanalysis[3]
    trendcube = copy.deepcopy(cube)
    trendcube.rename('Trend')
    trendcube.data=line(xdata, y_interception, slope)


    ydata1 = cube1.data
    xdata1 = cube1.coord('time').points
    mdi1  = ydata1.mask
    trendanalysis1 = MedianPairwiseSlopes(xdata1,ydata1,mdi1,mult10 = False, sort = False, calc_with_mdi=True)
    slope1 = trendanalysis1[0]
    y_interception1 = trendanalysis1[3]
    trendcube1 = copy.deepcopy(cube1)
    trendcube1.rename('Trend')
    trendcube1.data=line(xdata1, y_interception1, slope1)


    ydata2 = cube2.data
    xdata2 = cube2.coord('time').points
    mdi2  = ydata2.mask
    trendanalysis2 = MedianPairwiseSlopes(xdata2,ydata2,mdi2,mult10 = False, sort = False, calc_with_mdi=True)
    slope2 = trendanalysis2[0]
    y_interception2 = trendanalysis2[3]
    trendcube2 = copy.deepcopy(cube2)
    trendcube2.rename('Trend')
    trendcube2.data=line(xdata2, y_interception2, slope2)

    print(xdata1)
    print(xdata2)

    print(trendcube1.summary)
    print(trendcube2.summary)

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
def MedianPairwiseSlopes(xdata,ydata,mdi,mult10 = False, sort = False, calc_with_mdi = False):
    '''
    Calculate the median of the pairwise slopes

    :param array xdata: x array
    :param array ydata: y array
    :param float mdi: missing data indicator
    :param bool mult10: multiply output trends by 10 (to get per decade)
    :param bool sort: sort the Xdata first
    :returns: float of slope
    '''
    # sort xdata
    if sort:
        sort_order = np.argsort(xdata)

        xdata = xdata[sort_order]
        ydata = ydata[sort_order]

    slopes=[]
    #y_intercepts = []
    for i in range(len(xdata)):
        for j in range(i+1,len(xdata)):
            if calc_with_mdi == True:
                if mdi[j] == False and mdi[i] == False: #changed from: if ydata[j]!=mdi and ydata[i]!=mdi:
                    slopes += [(ydata[j]-ydata[i])/(xdata[j]-xdata[i])]
                    #y_intercepts += [(xdata[j]*ydata[i]-xdata[i]*ydata[j])/(xdata[j]-xdata[i])]
            elif calc_with_mdi == False:
                slopes += [(ydata[j]-ydata[i])/(xdata[j]-xdata[i])]
                #y_intercepts += [(xdata[j]*ydata[i]-xdata[i]*ydata[j])/(xdata[j]-xdata[i])]

    mpw=np.ma.median(np.ma.array(slopes))
    #y_intercept_point = np.ma.median(np.array(y_intercepts))
    y_intercept_point = np.median(ydata)-mpw*np.median(xdata)
    # copied from median_pairwise.pro methodology (Mark McCarthy)
    slopes.sort()

    if calc_with_mdi == True:
        good_data = np.where(mdi == False)#good_data=np.where(ydata == False)[0]
        n=len(ydata[good_data])

    elif calc_with_mdi == False:
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

        if mult10:
            return 10. * mpw, 10. * lower, 10. * upper, y_intercept_point      # MedianPairwiseSlopes
        else:
            return  mpw, lower, upper, y_intercept_point      # MedianPairwiseSlopes

    except:
        if mult10:
            return 10. * mpw, 'test', 'test', y_intercept_point      # MedianPairwiseSlopes
        else:
            return  mpw, 'test', 'test', y_intercept_point      # MedianPairwiseSlopes

