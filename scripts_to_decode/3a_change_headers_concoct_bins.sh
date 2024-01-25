


for SAMPLE in `awk '{print $1}' SRR_AccessionList_day7.txt`; do
	cd concoct_output_c800_individual/${SAMPLE}/

	mkdir concoct_bins_headersRenamed
	cd fasta_bins

	for file in *fa; do
    		awk '/^>/ {print $1} !/^>/ {print}' "$file" > ../concoct_bins_headersRenamed/"$file"
	done
	
	cd ../../../

	cd concoct_output_c400_individual/${SAMPLE}/

        mkdir concoct_bins_headersRenamed
        cd fasta_bins

        for file in *fa; do
                awk '/^>/ {print $1} !/^>/ {print}' "$file" > ../concoct_bins_headersRenamed/"$file"
        done

        cd ../../../
done
