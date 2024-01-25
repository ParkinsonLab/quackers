#!/bin/bash
#SBATCH --cpus-per-task=40
#SBATCH --nodes=1
#SBATCH --time=2:00:00
#SBATCH --job-name=day7_checkm
#SBATCH --error=checkm_concoctc500.err
#SBATCH --out=checkm_concoctc500.out

# conda activate checkm
# checkm lineage_wf concoct_output_run2/fasta_bins/ -x .fa -t 40 day7_MAGs-CHECKM-WF_concoct
# checkm lineage_wf INITIAL_BINNING_2_metaBAT2/metabat2_bins -x .fa -t 40 day7_MAGs-CHECKM-WF_metaBAT2
checkm lineage_wf concoct_output_c800_schellackia/fasta_bins/ -x .fa -t 40 day7_MAGs-CHECKM-WF_concoct_c800_schellackia
