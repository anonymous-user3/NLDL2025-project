#!/bin/bash

#SBATCH --job-name=prediction_summary_ESOL_and_Mutagenicity
#SBATCH --output=job_logs/prediction_summary_ESOL_and_Mutagenicity-%A-%a.out
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --time=23:00:00
#SBATCH --mem=16gb
#SBATCH --gres=gpu
#SBATCH --mail-user=ANONYMOUS
#SBATCH --mail-type=END,FAIL
#SBATCH --partition=titans
#SBATCH --export=ALL

## INFO
echo "Node: $(hostname)"
echo "Start: $(date +%F-%R:%S)"
echo -e "Working dir: $(pwd)\n"

SCRATCH=/scratch/$USER
if [[ ! -d $SCRATCH ]]; then
    mkdir $SCRATCH
fi

source ~/.bashrc
source activate SME_GPU_pip
cd MaskGNN_interpretation
python prediction_summary.py

echo "Done: $(date +%F-%R:%S)"
