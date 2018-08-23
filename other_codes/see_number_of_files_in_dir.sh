#!/bin/bash

for i in /scratch/vportge/ECA_D/*.zip; do
	echo "$i"
	zipinfo "$i" | grep ^-| wc -l
done

echo "Numbers of files in dirs"

for j in /scratch/vportge/ECA_D/*/; do
	echo "$j"
	ls "$j" -F | grep -v / | wc -l
done

