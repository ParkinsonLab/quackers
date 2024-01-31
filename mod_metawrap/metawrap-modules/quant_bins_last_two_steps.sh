#!/usr/bin/env bash


help_message () {
        echo ""
        echo "Usage: metaWRAP quant_bins [options] -b bins_folder -o output_dir -a assembly.fa readsA_1.fastq readsA_2.fastq ... [readsX_1.fastq readsX_2.fastq]"
        echo "Options:"
        echo ""
        echo "  -b STR          folder containing draft genomes (bins) in fasta format"
        echo "  -o STR          output directory"
        echo "  -a STR          fasta file with entire metagenomic assembly (strongly recommended!)"
        echo "  -t INT          number of threads"
        echo ""
        echo "";}

comm () { ${SOFT}/print_comment.py "$1" "-"; }
error () { ${SOFT}/print_comment.py "$1" "*"; exit 1; }
warning () { ${SOFT}/print_comment.py "$1" "*"; }
announcement () { ${SOFT}/print_comment.py "$1" "#"; }

########################################################################################################
########################               LOADING IN THE PARAMETERS                ########################
########################################################################################################


# setting scripts and databases from config file (should be in same folder as main script)
config_file=$(which config-metawrap)
source $config_file


# default params
threads=4; out=false; bin_folder=false; assembly=false
# long options defaults

# load in params
OPTS=`getopt -o ht:o:b:a: --long help -- "$@"`
# make sure the params are entered correctly
if [ $? -ne 0 ]; then help_message; exit 1; fi

# loop through input params
while true; do
        case "$1" in
                -t) threads=$2; shift 2;;
                -o) out=$2; shift 2;;
                -b) bin_folder=$2; shift 2;;
                -a) assembly=$2; shift 2;;
                -h | --help) help_message; exit 1; shift 1;;
                --) help_message; exit 1; shift; break ;;
                *) break;;
        esac
done





########################################################################################################
########################        EXTRACTING AVERAGE ABUNDANCE OF EACH BIN        ########################
########################################################################################################
announcement "EXTRACTING AVERAGE ABUNDANCE OF EACH BIN"

n=$(ls ${out}/quant_files/ | grep counts | wc -l)
if [[ $n -lt 1 ]]; then error "There were no files found in ${out}/quant_files/"; fi
comm "There were $n samples detected. Making abundance table!"

${SOFT}/split_salmon_out_into_bins.py ${out}/quant_files/ $bin_folder $assembly > ${out}/bin_abundance_table.tab
if [[ $? -ne 0 ]]; then error "something went wrong with making summary abundance table. Exiting..."; fi
comm "Average bin abundance table stored in ${out}/abundance_table.tab"




########################################################################################################
########################            MAKING GENOME ABUNDANCE HEATMAP             ########################
########################################################################################################
if [[ $n -gt 1 ]]; then
        announcement "MAKING GENOME ABUNDANCE HEATMAP WITH SEABORN"

        comm "making heatmap with Seaborn"
        ${SOFT}/make_heatmap.py ${out}/bin_abundance_table.tab ${out}/bin_abundance_heatmap.png
        if [[ $? -ne 0 ]]; then error "something went wrong with making the heatmap. Exiting..."; fi

        comm "cleaning up..."
        rm -r ${out}/alignment_files/ 
else
        warning "Cannot make clustered heatmap with just one sample... Skipping heatmap"
fi

########################################################################################################
########################     QUANT_BINS PIPELINE SUCCESSFULLY FINISHED!!!       ########################
########################################################################################################
announcement "QUANT_BINS PIPELINE SUCCESSFULLY FINISHED!!!"




