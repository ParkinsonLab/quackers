#!/bin/bash
#SBATCH --cpus-per-task=40
#SBATCH --nodes=1
#SBATCH --time=12:00:00
#SBATCH --job-name=day7_metaWRAP_refine_ind
#SBATCH --error=metaWRAP_refine_50_10_c400_c800_ind_4.err
#SBATCH --out=metaWRAP_refine_50_10_c400_c800_ind_4.out

module load autotools	
module load gcc/13.2.0
module load python/3.7.9
# conda activate python3.7
# PATH=$PATH:/project/j/jparkin/Lab_Tools/BWA
# PATH=$PATH:/project/j/jparkin/Lab_Tools/metaWRAP/bin
PATH=$PATH:$SCRATCH/metaWRAP/bin
PATH=$PATH:/home/j/jparkin/utkinair/.local/bin
PATH=$PATH:$SCRATCH/bin
#metawrap binning -o INITIAL_BINNING_2 -t 96 -a day7_megahit_out/final.contigs.fa --metabat2 --single-end day7_chicken_fastq_preprocessed_trimmed_forMetaBAT/*fastq

for SAMPLE in `awk '{print $1}' SRR_AccessionList_day7_4.txt`; do
        echo "SAMPLE metaBAT2:  $SAMPLE"
        # metawrap binning -o INITIAL_BINNING_metaBAT2_individual/${SAMPLE} -t 96 -a day7_megahit_separate_out/output_${SAMPLE}/final.contigs.fa --metabat2 --single-end day7_chicken_fastq_preprocessed_trimmed_forMetaBAT/${SAMPLE}_1.fastq

	metawrap bin_refinement -o BIN_REFINEMENT_50_10_individual_assemblies/${SAMPLE} -t 96 -A INITIAL_BINNING_metaBAT2_individual/${SAMPLE}/metabat2_bins/ -B concoct_output_c400_individual/${SAMPLE}/concoct_bins_headersRenamed -C concoct_output_c800_individual/${SAMPLE}/concoct_bins_headersRenamed -c 50 -x 10
done
