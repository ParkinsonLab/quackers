#!/bin/bash
#SBATCH --cpus-per-task=40
#SBATCH --nodes=1
#SBATCH --time=4:00:00
#SBATCH --job-name=day7_metaWRAP_metabat_ind_ass
#SBATCH --error=metaWRAP_metabat_ind_ass.err
#SBATCH --out=metaWRAP_metabat_ind_ass.out

module load autotools	
module load gcc/13.2.0
# conda activate python3.7
PATH=$PATH:/project/j/jparkin/Lab_Tools/BWA
PATH=$PATH:/project/j/jparkin/Lab_Tools/metaWRAP/bin
PATH=$PATH:$SCRATCH/bin

for SAMPLE in `awk '{print $1}' SRR_AccessionList_day7.txt`; do
        echo "SAMPLE metaBAT2:  $SAMPLE"
	metawrap binning -o INITIAL_BINNING_metaBAT2_individual/${SAMPLE} -t 96 -a day7_megahit_separate_out/output_${SAMPLE}/final.contigs.fa --metabat2 --single-end day7_chicken_fastq_preprocessed_trimmed_forMetaBAT/${SAMPLE}_1.fastq
done
