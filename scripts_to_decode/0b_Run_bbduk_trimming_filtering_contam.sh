PATH=$PATH:$SCRATCH/bbmap
cd day7_chicken_fastq_rawdata
# loop through raw fastq files:
for file in *; do
 # Filter out contaminant reads placing them in their own file
 # $SCRATCH/bbmap/bbduk.sh in=$file out=../day7_chicken_fastq_preprocessed_trimmed/${file}_unmatched.fq outm=../day7_chicken_fastq_preprocessed_trimmed/${file}_matched.fq \
 # k=31 \
 # hdist=1 \
 # ftm=5 \
 # ref=$SCRATCH/bbmap/resources/sequencing_artifacts.fa.gz \
 # stats=../day7_chicken_fastq_preprocessed_trimmed/${file}_contam_stats.txt

  # Trim the adapters using the reference file adaptors.fa (provided by bbduk)
  # Force-Trim Modulo: The right end so that the read’s length is equal to zero modulo 5 (ftm=5). The reason for this is that with Illumina sequencing, normal runs are usually a multiple of 5 in length (50bp, 75bp, 100bp, etc), but sometimes they are generated with an extra base (51bp, 76bp, 151bp, etc). This last base is very inaccurate and has badly calibrated quality as well, so it’s best to trim it before doing anything else. But you don’t want to simply always trim the last base, because sometimes the last base will already be clipped by Illumina’s software. “ftm=5” will, for example, convert a 151bp read to 150bp, but leave a 150bp read alone.
  $SCRATCH/bbmap/bbduk.sh in=../day7_chicken_fastq_preprocessed_trimmed/${file}_unmatched.fq \
  out=../day7_chicken_fastq_preprocessed_trimmed/${file}_woChick.fastq \
  outm=../day7_chicken_fastq_preprocessed_trimmed/${file}_matchedChick.fastq \
  k=25 \
  hdist=1 \
  ref=$SCRATCH/ncbi_rawdata/GCA_000002315.5_GRCg6a_genomic.fna
done
