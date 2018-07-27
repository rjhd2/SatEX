# -*- coding: iso-8859-1 -*-
import numpy as np
import datetime as dt
import iris
import os
import copy
import cf_units

# data location
DATALOC = "/scratch/vportge/CM_SAF_LST_MIN_MAX/"

OUTDIR = '/scratch/vportge/concatenated_yearly_files/'

# conversion between Climpact and SEVERI names
IN_VARIABLE_NAMES = {"tmax" : "Maximum Land Surface Temperature in Warm Window (PMW)", "tmin" : "Maximum Land Surface Temperature in Cold Window (PMW)", "precip" : ""}

final_cubes = iris.cube.CubeList()

YEARS = np.arange(2014,2016)

for climpact_var in ["tmax", "tmin", "precip"]:
    severi_var = IN_VARIABLE_NAMES[climpact_var]

    print("{:s} {:s}".format(climpact_var, severi_var))

    if climpact_var == "precip":
        # doing precip last, and mock up some dummy data
        precip = copy.deepcopy(final_cubes[-1])

        precip.rename(climpact_var)

        # remove data and mask
        precip.data[:] = -99.9
        precip.data.fill_value = -99.9
        try:
            precip.data.mask[:] = True
        except:
            #do nothing
            d = 0.
        precip.units = "kg m-2 d-1"
        precip.axis = None

        final_cubes.append(precip)

    else:
        # empty container
        cubelist = iris.cube.CubeList()

        for year in YEARS:
            # list the files
            year_path = "/".join([DATALOC, str(year)])

            months = os.listdir(year_path)
            months.sort()

            for month in months:
                print(month)

                month_path = "/".join([year_path, month])

                daily_files = os.listdir(month_path)
                daily_files.sort()

                # spin through each file
                for dfile in daily_files:

                    cube = iris.load_cube("/".join([month_path, dfile]), severi_var)
                    #take sahara
                    #cube = cube.extract(iris.Constraint(coord_values={'longitude':lambda cell: 18 < cell < 20}))
                    #cube = cube.extract(iris.Constraint(coord_values={'latitude':lambda cell: 28 < cell < 30}))

                    #remove missing values, mock up
                    #try:
                        #cube.data[np.where(cube.data.mask == True)] = 270.0
                        #cubelist.append(cube)

                    #except:
                        #print(dfile)
                        #cubelist.append(cube)
                    cubelist.append(cube)

        # concatenate down time axis
        merged = cubelist.concatenate()[0]
        #merged.data.fill_value = -99.9
        merged.data.fill_value = 1e20

        # rename & other bits
        merged.rename(climpact_var)
        merged.axis = None

        # time coordinates - in case that helps!
        times = merged.coord("time")
        cube_start = dt.datetime.strptime(times.units.origin.split()[2] + " 00:00","%Y-%m-%d %H:%M")
        hours = times.points/(60.*60.)

        time_unit = cf_units.Unit('hours since ' + dt.datetime.strftime(cube_start, "%Y-%m-%d %H:%M"), calendar=cf_units.CALENDAR_GREGORIAN)   
        timecoord = iris.coords.DimCoord(hours, standard_name = 'time', units = time_unit, var_name = "time") # add bounds?
        timecoord.guess_bounds()

        merged.remove_coord('time')
        merged.add_dim_coord(timecoord,0)

        # store
        final_cubes.append(merged)

print("saving")
iris.save(final_cubes, OUTDIR+str(YEARS[0])+'_'+str(YEARS[-1])+"_missing_value_1e20_time_in_hours.nc", zlib = True)

print("done")
