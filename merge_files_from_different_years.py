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


YEARS = np.arange(1991,2016)

FILEPATHS = ['/scratch/vportge/concatenated_yearly_files/1991_1992_missing_value_1e20_time_in_hours.nc', 
             '/scratch/vportge/concatenated_yearly_files/1993_1995_missing_value_1e20_time_in_hours.nc',
             '/scratch/vportge/concatenated_yearly_files/1996_1998_missing_value_1e20_time_in_hours.nc',
             '/scratch/vportge/concatenated_yearly_files/1999_2001_missing_value_1e20_time_in_hours.nc', 
             '/scratch/vportge/concatenated_yearly_files/2002_2004_missing_value_1e20_time_in_hours.nc', 
             '/scratch/vportge/concatenated_yearly_files/2005_2007_missing_value_1e20_time_in_hours.nc', 
             '/scratch/vportge/concatenated_yearly_files/2008_2010_missing_value_1e20_time_in_hours.nc', 
             '/scratch/vportge/concatenated_yearly_files/2011_2013_missing_value_1e20_time_in_hours.nc', 
             '/scratch/vportge/concatenated_yearly_files/2014_2015_missing_value_1e20_time_in_hours.nc']



for climpact_var in ["tmax", "tmin", "precip"]:
    final_cubes = iris.cube.CubeList()

    data = iris.load(FILEPATHS, climpact_var)
    # concatenate down time axis
    merged = data.concatenate_cube()
    #The order of the input cubes does not affect the concatenate process according to Iris Documentation.
    final_cubes.append(merged)

    print("saving "+str(climpact_var))
    iris.save(final_cubes, OUTDIR+str(YEARS[0])+'_'+str(YEARS[-1])+"_"+str(climpact_var)+".nc", zlib = True)

    print("done")
