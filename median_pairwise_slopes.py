#!/usr/local/sci/bin/python2.7

#***************************************
def MedianPairwiseSlopes(xdata,ydata,mdi,mult10 = True, sort = False):
    '''
    Calculate the median of the pairwise slopes

    :param array xdata: x array
    :param array ydata: y array
    :param float mdi: missing data indicator
    :param bool mult10: multiply output trends by 10 (to get per decade)
    :param bool sort: sort the Xdata first
    :returns: float of slope
    '''
    
    import numpy as np
    
    # sort xdata
    if sort:
        sort_order = np.argsort(xdata)

        xdata = xdata[sort_order]
        ydata = ydata[sort_order]

    slopes=[]
    for i in range(len(xdata)):
        for j in range(i+1,len(xdata)):
            if ydata[j] != mdi and ydata[i] != mdi:
                slopes+=[(ydata[j]-ydata[i])/(xdata[j]-xdata[i])]


    mpw=np.median(np.array(slopes))

    # copied from median_pairwise.pro methodology (Mark McCarthy)
    slopes.sort()

    good_data=np.where(ydata != mdi)[0]

    n=len(ydata[good_data])

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
        return 10. * mpw, 10. * lower, 10. * upper      # MedianPairwiseSlopes
    else:
        return  mpw, lower, upper      # MedianPairwiseSlopes


