#!/bin/bash

for year in $(seq 1991 2015); do
		echo ${year}
		spice_script=plot_coverage_${year}.bash
		echo "#!/bin/bash -l" > ${spice_script}
		echo "#SBATCH --mem=40000" >> ${spice_script} # memory in MB
		echo "#SBATCH --ntasks=6" >> ${spice_script}
		echo "#SBATCH --output=/scratch/vportge/spice_logs/example_${year}_internal.txt" >> ${spice_script}
		echo "#SBATCH --time=15" >> ${spice_script} # time in minutes, seasonal analysis takes less than 5 mins.
		echo "#SBATCH --qos=normal" >> ${spice_script} # queue
		echo "module load scitools/experimental-current" >> ${spice_script}
		echo "python /home/h01/vportge/CM_SAF/python_analysis/plot_CM_SAF_LST_min_max.py ${year}" >> ${spice_script} 
		chmod +x ${spice_script}		
		sbatch ${spice_script}
		#sbatch spice_internal_1991_10.bash
		# if there are too many files in the queue, wait for a minute before submitting some more.
		n_jobs=`squeue -l | grep vportge | wc -l`
		while [ $n_jobs -gt 9 ]; do # which is a silly limit, but to demonstrate!
			echo `date` "  SPICE queue for user hadobs maxed out - sleeping 200s"
			sleep 200s| tr -d '\r'
			n_jobs=`squeue -l | grep vportge | wc -l`
	done
done
