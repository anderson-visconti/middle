def make_map():

    fig, ax = plt.subplots()
    m = Basemap(projection='merc',
                llcrnrlat=-35,
                urcrnrlat=9.0,
                llcrnrlon=-78,
                urcrnrlon=-30,
                resolution='i'
                )
    m.ax = ax
    m.drawcoastlines(linewidth=0.15)
    m.drawcountries(linewidth=0.15)
    m.drawrivers(linewidth=0.3)
    return m, ax


def draw_states(ax, shapefile):
        shp = m.readshapefile(shapefile, 'states', drawbounds=True)
        for nshape, seg in enumerate(m.states):
            poly = Polygon(seg, facecolor='none', edgecolor='none', alpha=1.0)
            ax.add_patch(poly)

        return

if __name__ == '__main__':
    import pandas as pd
    import numpy as np
    from mpl_toolkits.basemap import Basemap
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon


    df_teste = pd.read_fwf(
        filepath_or_buffer=r'C:\OneDrive\Middle Office\Middle\Hidrologia\Previsao de Vazao\Chuva\ETA\20170614\ETA40_p140617a150617.dat',
        delim_whitespace =True, decimal=',',
        names=['lon', 'lat', 'precip'], dtype={'lon':np.float, 'lat':np.float, 'precip':np.float})

    df_teste.head()
    lons, lats = df_teste.lon.unique(), df_teste.lat.unique()
    x, y = np.meshgrid(lons, lats)
    df_teste['precip']  = df_teste['precip'].apply(lambda x: x * 100.0)
    precip = df_teste.pivot(index='lat', columns='lon', values='precip').values
    sub_set = {
        'llcrnrlat': float(np.amin(lats)),
        'urcrnrlat': float(np.amax(lats)),
        'llcrnrlon': float(np.amin(lons)),
        'urcrnrlon': float(np.amin(lons))
    }

    m, ax = make_map()
    draw_states(ax, shapefile=r'C:\OneDrive\Middle Office\Middle\Hidrologia\ShapeFiles\brasil\BRA_adm1')
    xx, yy = m(x, y)
    levels = [1, 5, 10, 15, 20, 25, 30, 40, 50, 75, 100, 150, 200]
    cores_ons = [(255.0/255.0, 255.0/255.0, 255.0/255.0),
                 (225.0/255.0, 255.0/255.0, 255.0/255.0),
                 (180.0/255.0, 240.0/255.0, 250.0/255.0),
                 (40.0/255.0, 130.0/255.0, 240.0/255.0),
                 (20.0/255.0, 100.0/255.0, 210.0/255.0),
                 (103.0/255.0, 254.0/255.0, 133.0/255.0),
                 (24.0/255.0, 215.0/255.0, 6.0/255.0),
                 (30.0/255.0, 180.0/255.0, 30.0/255.0),
                 (255.0/255.0, 232.0/255.0, 120.0/255.0),
                 (255.0/255.0, 192.0/255.0, 60.0/255.0),
                 (255.0/255.0, 96.0/255.0, 0.0/255.0),
                 (225.0/255.0, 20.0/255.0, 0.0/255.0),
                 (251.0/255.0, 94.0/255.0, 107.0/255.0),
                 (170.0/255.0, 170.0/255.0, 170.0/255.0)
                 ]
    plt.title('Modelo ETA')
    cs = m.contourf(xx, yy, precip, levels=levels, colors=cores_ons, extend='both')
    cbar = m.colorbar(cs, location='bottom', label='Preciptacao [mm]')
    cbar.set_ticks(levels)
    cbar.ax.tick_params(labelsize=8)
    #plt.savefig(r'C:\OneDrive\Middle Office\Middle\Hidrologia\teste.png')
    plt.show()


    pass
