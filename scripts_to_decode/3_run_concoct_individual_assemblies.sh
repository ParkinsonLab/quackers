#!/bin/bash
#SBATCH --cpus-per-task=40
#SBATCH --nodes=1
#SBATCH --time=2:00:00
#SBATCH --job-name=day7_ind_ass_concoct1.1.0_c400
#SBATCH --error=concoct_run_individ_c400_3.err
#SBATCH --out=concoct_individ_c400_3.out

conda activate concoct_env
# mkdir concoct_output_c400_individual

for SAMPLE in `awk '{print $1}' SRR_AccessionList_day7_1.txt`; do
	echo "SAMPLE concoct:  $SAMPLE"
	mkdir concoct_output_c400_individual/${SAMPLE}/

	# cut contigs into smaller parts, with a maximum length of 10,000 base pairs, which is aimed at mitigating the effect of potential local assembly errors:
	cut_up_fasta.py day7_megahit_separate_out/output_${SAMPLE}/final.contigs.fa -c 10000 -o 0 --merge_last -b concoct_output_c400_individual/${SAMPLE}/day7_contigs_10K.bed > concoct_output_c400_individual/${SAMPLE}/day7_contigs_10K.fa

	# get the coverage of these new, cut up contigs in our samples:
	concoct_coverage_table.py concoct_output_c400_individual/${SAMPLE}/day7_contigs_10K.bed day7_bam_files_individual_assembly/${SAMPLE}.bam > concoct_output_c400_individual/${SAMPLE}/day7_coverage_table.tsv

	# Run_concoct:
	concoct --composition_file concoct_output_c400_individual/${SAMPLE}/day7_contigs_10K.fa --coverage_file concoct_output_c400_individual/${SAMPLE}/day7_coverage_table.tsv -b concoct_output_c400_individual/${SAMPLE}/ -c 400 --threads 96

	# Now that we have information on all of the bins/clusters, we can merge the cut up contig clustering back into the original, potentially longer, contigs:
	merge_cutup_clustering.py concoct_output_c400_individual/${SAMPLE}/clustering_gt1000.csv > concoct_output_c400_individual/${SAMPLE}/clustering_merged.csv
	# use this clustering information to take the contig sequences and group together those that should be in the same bin/MAG:
	mkdir concoct_output_c400_individual/${SAMPLE}/fasta_bins 
	extract_fasta_bins.py day7_megahit_separate_out/output_${SAMPLE}/final.contigs.fa concoct_output_c400_individual/${SAMPLE}/clustering_merged.csv --output_path concoct_output_c400_individual/${SAMPLE}/fasta_bins
done
