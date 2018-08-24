#!/bin/bash

for TILENUM in $(seq 0 95); do
        echo ${TILENUM}
        spice_script=calculate_indices_${TILENUM}.bash
        echo "#!/bin/bash -l" > ${spice_script}
        echo "#SBATCH --mem=10G" >> ${spice_script} # memory in MB
        echo "#SBATCH --ntasks=6" >> ${spice_script}
        echo "#SBATCH --output=/scratch/vportge/spice_logs/calculate_indices_${TILENUM}.txt" >> ${spice_script}
        echo "#SBATCH --time=200" >> ${spice_script} # time in minutes
        echo "#SBATCH --qos=normal" >> ${spice_script} # queue
        echo "module load scitools/experimental-current" >> ${spice_script}
        echo "python /home/h01/vportge/CM_SAF/python_analysis/climate_index_calculation/compute_indices.py ${TILENUM}" >> ${spice_script} 
        chmod +x ${spice_script}
        sbatch ${spice_script}
        #sbatch spice_internal_1991_10.bash
        # if there are too many files in the queue, wait for a minute before submitting some more.
        n_jobs=`squeue -l | grep vportge | wc -l`
        while [ $n_jobs -gt 25 ]; do # which is a silly limit, but to demonstrate!
                echo `date` "  SPICE queue for user hadobs maxed out - sleeping 200s"
                sleep 200s| tr -d '\r'
                n_jobs=`squeue -l | grep vportge | wc -l`
        done

done
