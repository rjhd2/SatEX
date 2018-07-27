# -*- coding: iso-8859-1 -*-
#analyse hourly indices
def plot_figure(data, gridlons, gridlats):
    """Plot min/max LST for some day."""
    plt.close()
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    v = np.arange(int(np.amin(data)-1), int(np.amax(data)+1), 1)
    lst_map = plt.contourf(gridlons, gridlats, data, levels = v, transform=ccrs.PlateCarree())
    cbar = plt.colorbar(lst_map, orientation='horizontal', extend='both')
    ax.coastlines()
    plt.title('CM SAF ')
    plt.show()
    #plt.savefig(outpath+'CM_SAF_map_LST_'+title[0:3]+'_'+outname+'.png')
    return
