import marimo

__generated_with = "0.20.4"
app = marimo.App()


@app.cell
def _():
    import cartopy.crs as ccrs # module to work with coordinate reference systems for mapping
    import cartopy.feature as cfeature # module to add details like country and state outlines to maps
    import matplotlib.pyplot as plt # major plotting module
    import metpy # library for working with meteorological data
    import xarray as xr # library for working with labeled higher-dimensional data

    return ccrs, cfeature, metpy, plt, xr


@app.cell
def _(xr):
    # You will need to open a terminal from your current working directory (the directory with this
    # notebook) and run the command: cp /data/metr1313/kis/graphcastgfs.t00z.pgrb2.0p25_251029.f000 .
    # This will copy the data file into your current working directory
    # The period is part of the command and stands for the current working directory!

    ds = xr.open_dataset('graphcastgfs.t00z.pgrb2.0p25_251029.f000', # data file
                          engine='cfgrib', # data file is in GRIB2 format
                          decode_timedelta=False, # to avoid a User Warning
                          backend_kwargs={'filter_by_keys':{'typeOfLevel':'isobaricInhPa'}}) # to avoid a User Warning
    return (ds,)


@app.cell
def _(ds):
    # Let's view the dataset!
    # Please explore it by clicking on its icons to expand its metadata and values
    ds
    return


@app.cell
def _(ds):
    variables = ['gh', 'u', 'v'] # We only want to plot geopotential height, u, and v
    ds_subset = ds.sel(
        isobaricInhPa=500, # We only will plot data on the 500 hPa surface
        latitude=slice(70,20),
        longitude=slice(200,300))[variables]
    return (ds_subset,)


@app.cell
def _(ds_subset):
    ds_subset
    return


@app.cell
def _(ds_subset):
    time = str(ds_subset['time'].values)
    time
    return (time,)


@app.cell
def _(ds_subset, metpy):
    speed = metpy.calc.wind_speed(ds_subset['u'], ds_subset['v'])
    return (speed,)


@app.cell
def _(ds_subset, metpy):
    ug, vg = metpy.calc.geostrophic_wind(ds_subset['gh'])
    return ug, vg


@app.cell
def _(ug):
    ug.shape
    return


@app.cell
def _(ds_subset, metpy):
    ua, va = metpy.calc.ageostrophic_wind(ds_subset['gh'], ds_subset['u'], ds_subset['v'])
    return


@app.cell
def _(ccrs):
    transform = ccrs.PlateCarree()
    projection = ccrs.PlateCarree()
    return projection, transform


@app.cell
def _(cfeature, ds_subset, plt, projection, speed, time, transform, ug, vg):
    fig, ax = plt.subplots(
        figsize=(10,10),
        layout='constrained',
        subplot_kw={'projection':projection}
    )

    ax.add_feature(cfeature.BORDERS, edgecolor='gray', zorder=1)
    ax.add_feature(cfeature.COASTLINE, edgecolor='gray', zorder=1)
    ax.add_feature(cfeature.STATES, edgecolor='gray', zorder=1)

    gh_levels = range(4800, 6060, 60)
    gh_contours = ax.contour(
        ds_subset['longitude'],
        ds_subset['latitude'],
        ds_subset['gh'],
        transform=transform,
        levels=gh_levels,
        colors='brown',
        linewidths=2,
        zorder=3,
    )
    ax.clabel(gh_contours)

    quiver_step = 10
    mask = slice(None, None, quiver_step)
    geo_vectors = ax.quiver(
        ds_subset['longitude'][mask],
        ds_subset['latitude'][mask],
        ug[mask,mask],
        vg[mask,mask],
        transform=transform,
        #scale=800,
        color='blue',
        zorder=5,
    )

    wind_vectors = ax.quiver(
        ds_subset['longitude'][mask],
        ds_subset['latitude'][mask],
        ds_subset['u'][mask,mask],
        ds_subset['v'][mask,mask],
        transform=transform,
        #scale=geo_vectors.scale,
        color='black',
        zorder=4,           
    )

    #ageo_vectors = ax.quiver(
    #    ds_subset['longitude'][mask],
    #    ds_subset['latitude'][mask],
    #    ua[mask,mask],
    #    va[mask,mask],
    #    transform=transform,
    #    scale=geo_vectors.scale,
    #    color='red',
    #    zorder=4,           
    #)

    isotach_levels = range(25, 50, 5)
    isotachs = ax.contourf(
        ds_subset['longitude'],
        ds_subset['latitude'],
        speed,
        transform=transform,
        levels=isotach_levels,
        cmap='cool',
        alpha=0.5,
        extend='max',
        zorder=2,
    )
    cbar = fig.colorbar(
        isotachs,
        location='bottom',
        orientation='horizontal',
        #drawedges=True,
        label='Wind speed (m/s)',
    )

    ax.set_title(f'500 hPa geopotential height (m) and wind (m/s) @ {time[:10]} {time[11:13]}Z')

    fig.savefig(
        'my_500-hPa_plot.png',
        format='png',
        bbox_inches='tight',
    )

    plt.show()
    return


if __name__ == "__main__":
    app.run()
