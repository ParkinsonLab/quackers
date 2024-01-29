# make a Bowtie2 database with the contigs for each sample:
#for SAMPLE in `awk '{print $1}' SRR_AccessionList_day7.txt`; do
#	bowtie2-build day7_megahit_separate_out/output_${SAMPLE}/final.contigs.fa day7_megahit_separate_out/output_${SAMPLE}/final.contigs
#done


cd day7_chicken_fastq_rawdata
# for SAMPLE in `awk '{print $1}' ../SRR_AccessionList_day7.txt`; do
for SAMPLE in `awk '{print $1}' ../SRR_AccessionList_day7.txt`; do
	echo "Sample "$SAMPLE

	# do the bowtie mapping to get the SAM file:
	bowtie2 --threads 40 \
            -x ../day7_megahit_separate_out/output_${SAMPLE}/final.contigs \
	    -U "../day7_chicken_fastq_preprocessed_trimmed/"$SAMPLE"_1.fastq_unmatched.fq" \
	    --no-unal \
            -S ../day7_bam_files_individual_assembly/$SAMPLE.sam

	 # convert the resulting SAM file to a BAM file:
	samtools view -F 4 -bS ../day7_bam_files_individual_assembly/$SAMPLE.sam > ../day7_bam_files_individual_assembly/$SAMPLE-RAW.bam

	# sort and index the BAM file:
	samtools sort ../day7_bam_files_individual_assembly/$SAMPLE-RAW.bam -o ../day7_bam_files_individual_assembly/$SAMPLE.bam
	samtools index ../day7_bam_files_individual_assembly/$SAMPLE.bam

	# remove temporary files:
	rm ../day7_bam_files_individual_assembly/$SAMPLE.sam ../day7_bam_files_individual_assembly/$SAMPLE-RAW.bam

done




