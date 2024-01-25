#!/bin/bash
#SBATCH --cpus-per-task=40
#SBATCH --nodes=1
#SBATCH --time=9:00:00
#SBATCH --job-name=day7_gtdbtk_4
#SBATCH --error=day7_gtdbtk_classify_50_10_ind_4.err
#SBATCH --out=day7_gtdbtk_classify_50_10_ind_4.out

# conda activate checkm
# checkm lineage_wf concoct_output_run2/fasta_bins/ -x .fa -t 40 day7_MAGs-CHECKM-WF_concoct
export GTDBTK_DATA_PATH=$SCRATCH/GTDBtk_Reference/release214
# export GTDBTK_DATA_PATH=$SCRATCH/gtdbtk_data.tar.gz

# gtdbtk classify_wf --mash_db ~/miniconda/bin/mash --genome_dir BIN_REFINEMENT_comp75_contam10/metawrap_75_10_bins --extension fa --out_dir day7_GTDBtk_out_75_10 --cpus 40
for SAMPLE in `awk '{print $1}' SRR_AccessionList_day7_4.txt`; do
        echo "SAMPLE gtdbtk:  $SAMPLE"	
	gtdbtk classify_wf --skip_ani_screen --genome_dir BIN_REFINEMENT_50_10_individual_assemblies/${SAMPLE}/metawrap_50_10_bins --extension fa --out_dir day7_GTDBtk_out_50_10_individual_assemblies/${SAMPLE} --cpus 40
done
