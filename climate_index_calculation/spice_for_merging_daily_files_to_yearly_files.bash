#!/bin/bash

for year in $(seq 1991 2015); do
    spice_script=spice_lst_max_${year}.bash
    echo "#!/bin/bash -l" > ${spice_script}
    echo "#SBATCH --mem=20G" >> ${spice_script} # memory in MB
    echo "#SBATCH --ntasks=4" >> ${spice_script}
    echo "#SBATCH --output=/scratch/vportge/satex/slurm_log_lst_max_${year}.txt" >> ${spice_script}
    echo "#SBATCH --time=15" >> ${spice_script} # time in minutes
    echo "#SBATCH --qos=normal" >> ${spice_script} # queue
    echo "module load scitools/experimental-current" >> ${spice_script}
    echo "python /home/h01/vportge/CM_SAF/python_analysis/climate_index_calculation/merge_daily_files_to_yearly_files.py ${year}" >> ${spice_script} 
    chmod +x ${spice_script}
    sbatch ${spice_script}
    # if there are too many files in the queue, wait for a minute before submitting some more.
    n_jobs=`squeue -l | grep vportge | wc -l`
    while [ $n_jobs -gt 75 ]; do # which is a silly limit, but to demonstrate!
            echo `date` "  SPICE queue for user hadobs maxed out - sleeping 200s"
            sleep 200s| tr -d '\r'
            n_jobs=`squeue -l | grep vportge | wc -l`
    done

done
