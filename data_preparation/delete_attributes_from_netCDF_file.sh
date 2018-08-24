#!/bin/bash
#for i in *.nc; do
    	#echo item: $i
	#ncatted -h -a date_created,global,d,, $i
	#ncatted -h -a history,global,d,, $i
#done

#for i in /scratch/vportge/test_data_CM_SAF/*/*/*.nc; do
    	#echo item: $i
 	#echo $(basename "$i")
 	#echo $(dirname "$i")
	#ncatted -h -a date_created,global,d,, $i $(dirname "$i")/test$(basename "$i")
	#ncatted -h -a history,global,d,, $(dirname "$i")/test$(basename "$i") 
#done

#Delete Attributes history and date created 
#for i in /scratch/vportge/CM_SAF_data/*/*/*.nc; do
for i in /scratch/vportge/CM_SAF_data_2/*/*/*.nc; do

    	echo item: $i
	folderpath="$(dirname $i)"
	folderpath="$(dirname $folderpath)"
	foldername="$(basename $folderpath)"

	#echo $foldername #name of folder, ORD.....


 	#echo $(basename "$i") #filename
 	#echo $(dirname "$i")

	ncatted -h -a date_created,global,d,, $i /scratch/vportge/CM_SAF_data_metadata_changed/$(basename "$i")
	ncatted -h -a history,global,d,, /scratch/vportge/CM_SAF_data_metadata_changed/$(basename "$i")
done


for year in $(seq 1991 2015); do
    for month in $(seq -w 1 12); do


        mv /scratch/vportge/CM_SAF_data_metadata_changed/LTPin${year}${month}*.nc /scratch/vportge/CM_SAF_data_metadata_changed/${year}/${month}/

    done
done


#for i in /scratch/vportge/CM_SAF_data/*/*/; do
 	#echo $(basename "$i")
	#mkdir /scratch/vportge/CM_SAF_data_metadata_changed/$(basename "$i")/
	#echo item: $i
#done


#for i in /scratch/vportge/CM_SAF_data/*/*/*.nc; do
 	#echo $(basename "$i")
	#echo item: $i
#done


