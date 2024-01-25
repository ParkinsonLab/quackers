#!/bin/bash
#SBATCH --cpus-per-task=40
#SBATCH --nodes=1
#SBATCH --time=19:00:00
#SBATCH --job-name=day7_megahit_sep2_3
#SBATCH --error=megahit_separate2_3.err
#SBATCH --out=megahit_separate2_3.out


PATH=$PATH:$SCRATCH/2023_MG_chicken_cecal_data_BenWilling/MEGAHIT-1.2.9-Linux-x86_64-static/bin
# fq_files=$( ls day7_chicken_fastq_preprocessed_trimmed/*_unmatched.fq | tr '\n' ',' | sed 's/,$//' )

file_path="day7_chicken_fastq_preprocessed_trimmed/"

# Iterate over the files in the specified path
# for file in "$file_path"*.fastq_unmatched.fq; do
for file in day7_chicken_fastq_preprocessed_trimmed/SRR22360844_1.fastq_unmatched.fq day7_chicken_fastq_preprocessed_trimmed/SRR22360845_1.fastq_unmatched.fq day7_chicken_fastq_preprocessed_trimmed/SRR22360846_1.fastq_unmatched.fq day7_chicken_fastq_preprocessed_trimmed/SRR22360829_1.fastq_unmatched.fq day7_chicken_fastq_preprocessed_trimmed/SRR22360830_1.fastq_unmatched.fq; do
    # Extract the desired part of the file name
    file_name=$(basename "$file")
    identifier="${file_name%%_*}"
    # Create the name of the output directory
    output_dir="output_$identifier"

    megahit -r $file \
       	 --min-contig-len 1000 \
         --num-cpu-threads 80 \
         --verbose \
         -o "day7_megahit_separate_out/$output_dir"

done
## round 2:
# megahit --continue -o day7_megahit_out
