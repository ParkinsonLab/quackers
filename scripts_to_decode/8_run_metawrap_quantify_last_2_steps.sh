#!/bin/bash
#SBATCH --cpus-per-task=40
#SBATCH --nodes=1
#SBATCH --time=0:20:00
#SBATCH --job-name=day7_metaWRAP_quantify_last2steps
#SBATCH --error=metaWRAP_quantify_last2steps.err
#SBATCH --out=metaWRAP_quantify_last2steps.out

module load autotools	
module load python/2.7.15 

PATH=$PATH:$SCRATCH/metaWRAP/bin
PATH=$PATH:/home/j/jparkin/utkinair/.local/bin
PATH=$PATH:$SCRATCH/bin
export PATH=$SCRATCH/salmon-1.4.0_linux_x86_64/bin:$PATH
PATH=$PATH:/gpfs/fs1/scinet/niagara/software/2019b/opt/base/python/2.7.15/lib/python2.7/site-packages



for SAMPLE in `awk '{print $1}' SRR_AccessionList_day7.txt`; do
        echo "SAMPLE quant:  $SAMPLE"
        metawrap quant_bins_last_two_steps -b BIN_REFINEMENT_50_10_individual_assemblies/${SAMPLE}/metawrap_50_10_bins -o day7_QUANT_BINS_50_10_individual_assemblies/${SAMPLE} -a day7_megahit_separate_out/output_${SAMPLE}/final.contigs.fa day7_chicken_fastq_preprocessed_trimmed_forMetaBAT/${SAMPLE}_1.fastq -t 96
done

