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

filepaths = ['/scratch/vportge/2003_test.nc', '/scratch/vportge/2004_test.nc']


# conversion between Climpact and SEVERI names
IN_VARIABLE_NAMES = {"tmax" : "Maximum Land Surface Temperature in Warm Window (PMW)", "tmin" : "Minimum Land Surface Temperature in Cold Window (PMW)", "precip" : ""}

final_cubes = iris.cube.CubeList()

for climpact_var in ["tmax", "tmin", "precip"]:
    severi_var = IN_VARIABLE_NAMES[climpact_var]

    #print "{:s} {:s}".format(climpact_var, severi_var)

    # empty container
    cubelist = iris.cube.CubeList()

    cube = iris.load(filepaths, climpact_var)


    # concatenate down time axis
    merged = cube.concatenate()[0]

    final_cubes.append(merged)

iris.save(final_cubes, OUTDIR+"2003_2004_test.nc", zlib = True)
