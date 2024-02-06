PATH=$PATH:$SCRATCH/bbmap
cd day7_chicken_fastq_rawdata
# loop through raw fastq files:
for file in *; do
  # Filter out contaminant reads placing them in their own file
  $SCRATCH/bbmap/bbduk.sh in=$file out=../day7_chicken_fastq_preprocessed_trimmed/${file}_unmatched.fq outm=../day7_chicken_fastq_preprocessed_trimmed/${file}_matched.fq \
  k=31 \
  hdist=1 \
  ftm=5 \
  ref=$SCRATCH/bbmap/resources/sequencing_artifacts.fa.gz \
  stats=../day7_chicken_fastq_preprocessed_trimmed/${file}_contam_stats.txt
done
