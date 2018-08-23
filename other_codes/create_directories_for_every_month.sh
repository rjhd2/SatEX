#!/bin/bash
#create directories
#for i in $(seq 1991 2015); do
for i in $(seq 0 95); do
    echo $i
    #mkdir /scratch/vportge/concatenated_yearly_files/cold_window_10_3/$i/
    mkdir /scratch/vportge/concatenated_yearly_files/warm_window_10_3/max_LST_in_cold_window/TILES/$i/
    mkdir /scratch/vportge/concatenated_yearly_files/warm_window_10_3/min_LST_in_cold_window/TILES/$i/
    #for month in $(seq -w 1 12); do

        #mkdir /scratch/vportge/CM_SAF_LST_MIN_MAX_WINDOW_CHANGED/$i/${month}/
        #mkdir /scratch/vportge/CM_SAF_LST_MIN_MAX/COVERAGE/$i/
        #mkdir /scratch/vportge/concatenated_yearly_files/max_LST_in_cold_window/CORRECT_TILES/$i/
        #mkdir /scratch/vportge/concatenated_yearly_files/min_LST_in_cold_window/CORRECT_TILES/$i/
        #mkdir /scratch/vportge/indices/python_created_indices/min_LST_in_cold_window/$i/
        #mkdir /scratch/vportge/indices/python_created_indices/max_LST_in_cold_window/$i/
        #moo mkdir moose:/adhoc/users/veronika.portge/SatEX/data/CM_SAF_LST_MIN_MAX/daily_files/$i/${month}/
        #moo put -v /scratch/vportge/CM_SAF_LST_MIN_MAX/$i/${month}/*.nc moose:/adhoc/users/veronika.portge/SatEX/data/CM_SAF_LST_MIN_MAX/daily_files/$i/${month}/


        #for k in $(seq 1 9); do
                #mkdir /scratch/vportge/CM_SAF_LST_MIN_MAX/COVERAGE/$i/0$k/
        #done
        #for k in $(seq 10 12); do
                #mkdir /scratch/vportge/CM_SAF_LST_MIN_MAX/COVERAGE/$i/$k/
    #done
done

