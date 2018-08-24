#!/bin/bash
#SBATCH --mail-user=veronika.portge@metoffice.gov.uk
#SBATCH --mail-type=ALL
#SBATCH --mem=5G
#SBATCH --ntasks=10
#SBATCH --output="/scratch/vportge/satex/spice_plot_maps_of_regions_python.txt"
#SBATCH --time=200
#SBATCH --qos=normal

module load scitools/experimental-current
python /home/h01/vportge/CM_SAF/python_analysis/climate_index_calculation/plot_indices/plot_python_indices.py
