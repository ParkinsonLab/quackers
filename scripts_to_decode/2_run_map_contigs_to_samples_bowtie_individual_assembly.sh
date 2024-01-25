#!/bin/bash
#SBATCH --cpus-per-task=40
#SBATCH --nodes=1
#SBATCH --time=7:00:00
#SBATCH --job-name=day7_map_contigs1_ind_ass
#SBATCH --error=day7_map_contigs1_ind_ass.err
#SBATCH --out=day7_map_contigs1_ins_ass.out


./Map_contigs_to_samples_bowtie_individual_assembly.sh
