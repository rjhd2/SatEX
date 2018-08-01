# -*- coding: iso-8859-1 -*-
import numpy as np
import datetime as dt
import iris
import os
import copy
import cf_units
import glob
# data location

MIN_OR_MAX = 'max'

#OUTDIR = '/scratch/vportge/concatenated_yearly_files/'
#OUTDIR = '/scratch/vportge/concatenated_yearly_files/max_LST_in_cold_window/'
OUTDIR = '/scratch/vportge/concatenated_yearly_files/'+MIN_OR_MAX+'_LST_in_cold_window/TILES/'
#OUTDIR = '/scratch/vportge/concatenated_yearly_files/min_LST_in_cold_window/TILES/'

YEARS = np.arange(1991,2016)

#max LST in cold window
'''
FILEPATHS = ['/scratch/vportge/concatenated_yearly_files/max_LST_in_cold_window/1991_1992_missing_value_1e20_time_in_hours.nc', 
             '/scratch/vportge/concatenated_yearly_files/max_LST_in_cold_window/1993_1995_missing_value_1e20_time_in_hours.nc',
             '/scratch/vportge/concatenated_yearly_files/max_LST_in_cold_window/1996_1998_missing_value_1e20_time_in_hours.nc',
             '/scratch/vportge/concatenated_yearly_files/max_LST_in_cold_window/1999_2001_missing_value_1e20_time_in_hours.nc', 
             '/scratch/vportge/concatenated_yearly_files/max_LST_in_cold_window/2002_2004_missing_value_1e20_time_in_hours.nc', 
             '/scratch/vportge/concatenated_yearly_files/max_LST_in_cold_window/2005_2007_missing_value_1e20_time_in_hours.nc', 
             '/scratch/vportge/concatenated_yearly_files/max_LST_in_cold_window/2008_2010_missing_value_1e20_time_in_hours.nc', 
             '/scratch/vportge/concatenated_yearly_files/max_LST_in_cold_window/2011_2013_missing_value_1e20_time_in_hours.nc', 
             '/scratch/vportge/concatenated_yearly_files/max_LST_in_cold_window/2014_2015_missing_value_1e20_time_in_hours.nc']
'''
#min LST in cold window
FILEPATHS = glob.glob('/scratch/vportge/concatenated_yearly_files/'+MIN_OR_MAX+'_LST_in_cold_window/*.nc')
#FILEPATHS = ['/scratch/vportge/concatenated_yearly_files/max_LST_in_cold_window/north_africa/1991_2015_north_africa_missing_value_1e20_hours_as_time_coord.nc']
FILEPATHS.sort()


#define the indices of the certain regions/tiles
TILES_SHAPES = []
for i in range(4):
    for j in range(3):
        TILES_SHAPES.append(str(154*i)+','+str(154*(i+1))+','+str(520*j)+','+str(520*(j+1)))

        #TILES_SHAPES.append(str(154*i)+':'+str(154*(i+1))+','+str(520*j)+':'+str(520*(j+1)))




#for climpact_var in ["tmax", "tmin", "precip"]:
for climpact_var in ["tmin"]: #if tmax and precip were already calculated

    for TILENUM in range(len(TILES_SHAPES)):
        print(TILENUM)
        tileshape = TILES_SHAPES[TILENUM].split(',')

        final_cubes = iris.cube.CubeList()

        data = iris.load(FILEPATHS, climpact_var)
        # concatenate down time axis
        merged = data.concatenate_cube()
        #take only a certain region 
        merged = merged[:,int(tileshape[0]):int(tileshape[1]),int(tileshape[2]):int(tileshape[3])]

        #The order of the input cubes does not affect the concatenate process according to Iris Documentation.
        final_cubes.append(merged)

        print("saving "+str(climpact_var))
        iris.save(final_cubes, OUTDIR+str(TILENUM)+'/'+str(YEARS[0])+'_'+str(YEARS[-1])+"_"+str(climpact_var)+"_tile_"+str(TILENUM)+"_"+MIN_OR_MAX+"_LST_in_cold_window.nc", zlib = True)

        print("done")
