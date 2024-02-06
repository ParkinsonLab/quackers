#!/bin/bash
#SBATCH --cpus-per-task=40
#SBATCH --nodes=1
#SBATCH --time=1:00:00
#SBATCH --job-name=day7_bbduk
#SBATCH --error=day7_bbduk.err
#SBATCH --out=day7_bbduk.out

module load gnu-parallel
# raw data:
# find day7_chicken_fastq_rawdata/*fastq | parallel -j 33 "fastqc {} --outdir day7_fastqc/"
# data with contaminants removed:
# find day7_chicken_fastq_preprocessed_trimmed/*unmatched* | parallel -j 33 "fastqc {} --outdir day7_fastqc/"


# remove chicken genome-associated reads:
./Run_bbduk_trimming_filtering_contam.sh
