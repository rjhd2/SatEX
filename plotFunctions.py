# -*- coding: iso-8859-1 -*-
import numpy as np
import iris
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import iris.quickplot as qplt
import iris.plot as iplt
import cartopy.crs as ccrs
import cartopy.feature as cfeat



def line(x,t,m):
    '''Plot a line. '''
    return m*x+t


def plot_figure(data, gridlons, gridlats, title, units_dict, indexname, outpath, region):
    """Plot map of index for some day."""
    plt.close()
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    cbar_value = np.amax(abs(data))
    lst_map = plt.pcolormesh(gridlons, gridlats, data, transform=ccrs.PlateCarree(), cmap = 'RdBu_r', vmin = -cbar_value, vmax = cbar_value)
    cbar = plt.colorbar(lst_map, orientation='horizontal', extend='both')
    ax.set_extent((np.amin(gridlons)-2, np.amax(gridlons)+2, np.amin(gridlats)-2, np.amax(gridlats)+2), crs = ccrs.PlateCarree())

    political_bdrys = cfeat.NaturalEarthFeature(category='cultural',
                                                name='admin_0_countries',
                                                scale='50m')
    ax.add_feature(political_bdrys, edgecolor='b', facecolor='none', zorder=2)
    gl = ax.gridlines(draw_labels=True)
    plt.title(title, y=1.08, size=22)
    cbar.set_label(units_dict[indexname]+' per decade', size=20)
    plt.savefig(outpath+indexname+'_map_of_trend_'+region+'.png')
    return

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
    y_intercepts = []
    for i in range(len(xdata)):
        for j in range(i+1,len(xdata)):
            if calc_with_mdi == True:
                if mdi[j] == False and mdi[i] == False: #changed from: if ydata[j]!=mdi and ydata[i]!=mdi:
                    slopes += [(ydata[j]-ydata[i])/(xdata[j]-xdata[i])]
                    y_intercepts += [(xdata[j]*ydata[i]-xdata[i]*ydata[j])/(xdata[j]-xdata[i])]
            elif calc_with_mdi == False:
                slopes += [(ydata[j]-ydata[i])/(xdata[j]-xdata[i])]
                y_intercepts += [(xdata[j]*ydata[i]-xdata[i]*ydata[j])/(xdata[j]-xdata[i])]

    mpw=np.ma.median(np.ma.array(slopes))
    y_intercept_point = np.ma.median(np.array(y_intercepts))

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

