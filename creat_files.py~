#!/usr/local/sci/bin/python2.7
# -*- coding: iso-8859-1 -*-
import numpy as np
import datetime as dt
import iris
import os
import copy
import cf_units

# data location
DATALOC = "/scratch/vportge/satex/"

OUTDIR = '/scratch/vportge/indices/'

# conversion between Climpact and SEVERI names
IN_VARIABLE_NAMES = {"tmax" : "Maximum Land Surface Temperature in Warm Window (PMW)", "tmin" : "Minimum Land Surface Temperature in Cold Window (PMW)", "precip" : ""}

START = dt.datetime(1970,1,1)

final_cubes = iris.cube.CubeList()

YEARS = np.arange(2003,2005)

for climpact_var in ["tmax", "tmin", "precip"]:
    severi_var = IN_VARIABLE_NAMES[climpact_var]

    print "{:s} {:s}".format(climpact_var, severi_var)

    if climpact_var == "precip":
        # doing precip last, and mock up some dummy data
        precip = copy.deepcopy(final_cubes[-1])

        precip.rename(climpact_var)

        # remove data and mask
        precip.data[:] = 10
        precip.data.fill_value = -99.9        
        precip.data.mask[:] = True
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
                print month

                month_path = "/".join([year_path, month])

                daily_files = os.listdir(month_path)
                daily_files.sort()

                # spin through each file
                for dfile in daily_files:
                    print dfile

                    cube = iris.load_cube("/".join([month_path, dfile]), severi_var)
                    cube.data[:] = 270
                    cube.data.fill_value = -99.9        
                    cube.data.mask[:] = True
                    cube.units = "kg m-2 d-1"
                    cube.axis = None
                    cubelist.append(cube)

        # concatenate down time axis
        merged = cubelist.concatenate()[0]
        merged.data.fill_value = -99.9        

        # rename & other bits
        merged.rename(climpact_var)
        merged.axis = None

        # time coordinates - in case that helps!
        times = merged.coord("time")
        cube_start = dt.datetime.strptime(times.units.origin.split()[2] + " 00:00","%Y-%m-%d %H:%M")
        hours = times.points/60.

        time_unit = cf_units.Unit('hours since ' + dt.datetime.strftime(cube_start, "%Y-%m-%d %H:%M"), calendar=cf_units.CALENDAR_GREGORIAN)   
        timecoord = iris.coords.DimCoord(hours, standard_name = 'time', units = time_unit, var_name = "time") # add bounds?
    
        merged.remove_coord('time')
        merged.add_dim_coord(timecoord,0)

        # store
        final_cubes.append(merged)

print "saving"
iris.save(final_cubes, OUTDIR+str(year)+"_file_created_without_fill_values.nc", zlib = True)

print "done"
