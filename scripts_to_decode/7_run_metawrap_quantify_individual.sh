#!/bin/bash
#SBATCH --cpus-per-task=40
#SBATCH --nodes=1
#SBATCH --time=4:00:00
#SBATCH --job-name=day7_metaWRAP_quantify_individual
#SBATCH --error=metaWRAP_quantify_50_individ.err
#SBATCH --out=metaWRAP_quantify_50_individ.out

module load autotools	
#module load gcc/13.2.0
module load python/3.7.9

PATH=$PATH:$SCRATCH/metaWRAP/bin
PATH=$PATH:/home/j/jparkin/utkinair/.local/bin
PATH=$PATH:$SCRATCH/bin
export PATH=$SCRATCH/salmon-1.4.0_linux_x86_64/bin:$PATH


for SAMPLE in `awk '{print $1}' SRR_AccessionList_day7.txt`; do
        echo "SAMPLE quant:  $SAMPLE"
        metawrap quant_bins -b BIN_REFINEMENT_50_10_individual_assemblies/${SAMPLE}/metawrap_50_10_bins -o day7_QUANT_BINS_50_10_individual_assemblies/${SAMPLE} -a day7_megahit_separate_out/output_${SAMPLE}/final.contigs.fa day7_chicken_fastq_preprocessed_trimmed_forMetaBAT/${SAMPLE}_1.fastq -t 96
done


#metawrap quant_bins -b BIN_REFINEMENT_50_10_concoct_c800_c400/metawrap_50_10_bins -o day7_QUANT_BINS_50_10_v2_v4_concoct_c400_c800 -a day7_megahit_out/final.contigs.fa day7_chicken_fastq_preprocessed_trimmed_forMetaBAT/*fastq -t 96
