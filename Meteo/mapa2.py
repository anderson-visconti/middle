def make_map():

    fig, ax = plt.subplots()
    m = Basemap(projection='merc',
                llcrnrlat=-35,
                urcrnrlat=12,
                llcrnrlon=-85,
                urcrnrlon=-30
                )
    m.ax = ax
    m.drawcoastlines()
    m.drawcountries()
    return fig, m


def draw_states(ax, shapefile):
        shp = m.readshapefile(shapefile, 'states', drawbounds=True)
        for nshape, seg in enumerate(m.states):
            poly = Polygon(seg, facecolor='1', edgecolor='k')
            ax.add_patch(poly)


if __name__ == '__main__':
    import pandas as pd
    import numpy as np
    from mpl_toolkits.basemap import Basemap
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon
    from matplotlib.colors import LinearSegmentedColormap


    df_teste = pd.read_fwf(
        filepath_or_buffer=r'C:\Users\ander\Desktop\Eta40_precipitacao10d_11_06\ETA40_p110617a140617.dat',
        delim_whitespace =True, decimal=',',
        names=['lon', 'lat', 'precip'], dtype={'lon':np.float, 'lat':np.float, 'precip':np.float})

    df_teste.head()
    lons, lats = df_teste.lon.unique(), df_teste.lat.unique()
    x, y = np.meshgrid(lons, lats)
    precip = df_teste.pivot(index='lat', columns='lon', values='precip').values

    print np.amin(lons), np.amax(lons)
    print np.amin(lats), np.amax(lats)

    sub_set = {
        'llcrnrlat': float(np.amin(lats)),
        'urcrnrlat': float(np.amax(lats)),
        'llcrnrlon': float(np.amin(lons)),
        'urcrnrlon': float(np.amin(lons))
    }

    for i in sub_set.values():
        print i

    fig, m = make_map()
    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()
    m.drawrivers(linewidth=0.1)
    xx, yy = m(x, y)
    levels = np.arange(0, 210, 10)
    cores_ons = ['paleturquoise', 'mediumturquoise', 'dodgerblue',
                 'steelblue', 'springgreen', 'limegreen', 'forestgreen',
                 'yellow', 'gold', 'orangered', 'red', 'salmon', 'lightgray'
                 ]

    custom_map = LinearSegmentedColormap.from_list('my_cmap', colors=cores_ons)
    plt.register_cmap(cmap=custom_map)
    cs = m.contourf(xx, yy, precip, levels=levels, cmap='my_cmap', extend='both')
    cbar = m.colorbar(cs, location='bottom')
    plt.show()


    pass


