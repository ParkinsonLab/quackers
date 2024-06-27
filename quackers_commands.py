import os
import sys
import time
from datetime import datetime as dt
import MetaPro_utilities as mpu
import quackers_paths as q_path

class command_obj:
    def make_folder(folder_path):
        if(not os.path.exists(folder_path)):
            os.mkdir(folder_path)


    def __init__(self, path_obj, dir_obj, encoding):
        #self.path_obj = q_path.path_obj(output_path)
        self.path_obj = path_obj
        self.dir_obj = dir_obj
        self.op_mode = self.path_obj.operating_mode
        self.phred_encoding = encoding

    def adapterremoval_command(self, quality_encoding, marker_path):
        remove_lq = self.path_obj.ar_path + " "
        if(self.op_mode == "single"):
            remove_lq += "--file1" + " " + self.dir_obj.start_s + " '"
        elif(self.op_mode == "paired"):
            remove_lq += "--file1" + " " + self.dir_obj.start_f + " "
            remove_lq += "--file2" + " " + self.dir_obj.start_r + " "
        
        remove_lq += "--qualitybase" + " " + str(quality_encoding) + " "
        if(quality_encoding == 33):
            remove_lq += "--qualitymax" + " " + "75" + " "
        remove_lq += "--threads" + " " + str(os.cpu_count()) + " "
        remove_lq += "--minlength" + " " + str(self.path_obj.AR_minlength) + " "
        #remove_lq += "--basename" + " " + self.dir_obj.clean_dir_data + "_AR" + " "
        remove_lq += "--trimqualities" + " "
        
        if(self.op_mode == "single"):
            remove_lq += "--output1" + " " + self.dir_obj.clean_dir_final_s
        else:
            remove_lq += "--output1" + " " + self.dir_obj.clean_dir_final_f + " " 
            remove_lq += "--output2" + " " + self.dir_obj.clean_dir_final_r + " "
            remove_lq += "--singleton" + " " + self.dir_obj.clean_dir_AR_s0

        
        AR_reconcile = self.path_obj.py_path + " "
        AR_reconcile += self.path_obj.AR_reconcile + " "
        AR_reconcile += self.dir_obj.clean_dir_final_f + " "
        AR_reconcile += self.dir_obj.clean_dir_final_r + " "
        AR_reconcile += self.dir_obj.clean_dir_AR_sf + " "
        AR_reconcile += self.dir_obj.clean_dir_AR_sr + " "
        AR_reconcile += self.dir_obj.clean_dir_final_f + " "
        AR_reconcile += self.dir_obj.clean_dir_final_r

        combine_singles = "cat" + " "
        combine_singles += self.dir_obj.clean_dir_AR_s0 + " "
        combine_singles += self.dir_obj.clean_dir_AR_sf + " "
        combine_singles += self.dir_obj.clean_dir_AR_sr + " "
        combine_singles += ">>" + " "
        combine_singles += self.dir_obj.clean_dir_final_s
        
        
        
        make_marker = "touch" + " " + marker_path

        #if(self.op_mode == "single"):
        return [remove_lq +  " && " + make_marker]
        #else:
        #    return [remove_lq + " && " + AR_reconcile + " && " + combine_singles + " && " + make_marker ]

    def bwa_index_ref_command(self, ref_path, marker_path):
        command = self.path_obj.BWA_path
        command += " index " + ref_path

        make_marker = "touch" + " " + marker_path 
        return [command + " && " + make_marker]
    
    def bowtie2_index_ref_command(self, ref_path, out_path, marker_path):
        command = self.path_obj.bowtie2_idx_path + " "
        command += ref_path  + " "
        command += out_path

        make_marker = "touch " + marker_path

        return [command + " && " + make_marker]
    

    def clean_reads_bwa_simple_s(self, ref_path, sam_name, in_path, marker_path):
        #for a single host.
        sam_path = os.path.join(self.dir_obj.host_dir_sam, sam_name + ".sam")
        score_out_path = os.path.join(self.dir_obj.host_dir_sam, sam_name + "_s_score_bwa.out")
        command = self.path_obj.BWA_path + " mem "
        command += ref_path + " "
        command += in_path + " | " 
        command += self.path_obj.samtools_path + " view -F 4 > " + sam_path

   

        make_marker = "touch " + marker_path

        return [command + " && " + make_marker]

    def clean_reads_bwa_simple_p(self, ref_path, sam_name, f_path, r_path, marker_path):
        #for a single host. expected to be called per-host
        sam_path = os.path.join(self.dir_obj.host_dir_sam, sam_name + ".sam")
        score_out_path = os.path.join(self.dir_obj.host_dir_sam, sam_name + "_p_score_bwa.out")
        command = self.path_obj.BWA_path + " mem "
        command += ref_path + " "
        command += f_path + " "
        command += r_path + " "
        command += "|" + " " + self.path_obj.samtools_path + " view -F 4 > " + sam_path

        

        make_marker = "touch " + marker_path

        return [command + " && " + make_marker]
    
    def sift_bwa_sam_command(self, sam_path, score_out_path, marker_path):
        sifting_command = self.path_obj.py_path + " "
        sifting_command += self.path_obj.sam_sift + " "
        sifting_command += sam_path + " "
        sifting_command += score_out_path

        make_marker = "touch " + marker_path

        return [sifting_command + " && " + make_marker]

    def clean_reads_bowtie2_command_s(self, ref_path, in_path, marker_path):
        #used for contigs only
        command = self.path_obj.bowtie2_path 
        command += " -x "
        command += ref_path + " "
        command += "-U" + " " + in_path + " " 
        #command += "--phred" + str(self.phred_encoding) + " "
        command += "-S " + " " + self.dir_obj.assembly_raw_sam


        make_marker = "touch" + " " + marker_path

        return [command + " && " + make_marker]


    
    def clean_reads_bowtie2_command_p(self, ref_path, in1_path, in2_path, marker_path):
        #used for contigs only
        command = self.path_obj.bowtie2_path + " "
        command += "-p " + str(os.cpu_count()) + " "
        command += "-q" + " "
        command += "-x" + " "
        command += ref_path + " "
        command += "-1" + " " + in1_path + " "
        command += "-2" + " " + in2_path + " "
        #command += "--phred" + str(self.phred_encoding) + " "
        command += "-S " + self.dir_obj.assembly_raw_sam

        make_marker = "touch" + " " + marker_path

        return [command + " &&  " + make_marker]

    def bt2_scan_sam(self, marker_path):

        convert_sam = self.path_obj.samtools_path + " " + "view -bS " + self.dir_obj.assembly_raw_sam + " > " + self.dir_obj.assembly_raw_bam 

        sort_bam = self.path_obj.samtools_path + " " + "sort" + " " 
        sort_bam += self.dir_obj.assembly_raw_bam + " " 
        sort_bam += "-o" + " " + self.dir_obj.assembly_sort_bam

        index_bam = self.path_obj.samtools_path + " " + "index" + " "
        index_bam += self.dir_obj.assembly_sort_bam

        sifting_command = self.path_obj.py_path + " "
        sifting_command += self.path_obj.sam_sift + " "
        sifting_command += self.dir_obj.assembly_raw_sam + " "
        sifting_command += self.dir_obj.assembly_score_out

        make_marker = "touch" + " " + marker_path

        return [convert_sam + " && " + sort_bam + " && " + index_bam + " && " + sifting_command + " && " + make_marker]
    
    def contig_reconcile(self, sam_score_file, export_path, s_reads, f_reads, r_reads, marker_path):

        command = self.path_obj.py_path + " "
        command += self.path_obj.contig_reconcile + " "
        command += sam_score_file + " "
        command += export_path + " "
        command += s_reads + " "
        command += f_reads + " "
        command += r_reads

        make_marker = "touch " + marker_path

        return [command + " && " + make_marker]
    

    def clean_reads_reconcile(self, sam_path, export_path, s_reads, p1_reads, p2_reads, marker_path):
        command = self.path_obj.py_path + " "
        command += self.path_obj.clean_reads_reconcile + " "
        command += sam_path + " "
        command += export_path + " "
        if(not s_reads):
            command += "none" + " "
        else:
            command += s_reads + " "
        
        if(not p1_reads):
            command += "none" + " "
        else:
            command += p1_reads + " "
        
        if(not p2_reads):
            command += "none"
        else:
            command += p2_reads

        make_marker = "touch" + " " + marker_path

        return [command + " && " + make_marker]
        
    def metaspades_command_p(self, forward_path, reverse_path, quality_encoding, export_dir, marker_path):
        command = self.path_obj.mspades_path + " "
        command += "-1" + " " + forward_path + " "
        command += "-2" + " " + reverse_path + " "
        
        command += "-o" + " " + export_dir  + " "
        command += "-t" + " " + str(os.cpu_count()) + " "
        command += "--phred-offset" + " " + str(quality_encoding) + " "
        command += "--only-assembler"

        make_marker = "touch" + " " + marker_path
        return [command + " && " + make_marker]
    
    def metaspades_command_s(self, single_path, quality_encoding, export_dir, marker_path):
        command = self.path_obj.mspades_path + " " 
        command += "-s" + " " + single_path + " "
        command += "-t" + " " + str(os.cpu_count()) + " "
        command += "--only-assembler" + " "
        command += "--phread-offset" + " " + str(quality_encoding) + " " 
        command += "-o" + " " + export_dir 

        make_marker = "touch" + " " + marker_path

        return [command + " && " + make_marker]
    




    
    
    def concoct_prep_command(self, marker_path):

        concoct_prep = self.path_obj.cct_cut_up_fasta + " "
        concoct_prep += self.dir_obj.assembly_contigs + " "
        concoct_prep += "-c" + " " + "10000" + " "
        concoct_prep += "-o" + " " + "0" + " "
        concoct_prep += "--merge_last" + " " 
        concoct_prep += "-b" + " " + self.dir_obj.cct_bed + " "
        concoct_prep += ">" + " " + self.dir_obj.cct_cut_contig

        concoct_table_prep  = self.path_obj.cct_cov_table + " "
        concoct_table_prep += self.dir_obj.cct_bed + " "
        concoct_table_prep += self.dir_obj.assembly_sort_bam + " "
        concoct_table_prep +=">" + " " + self.dir_obj.cct_cov_table
        #concoct_table_prep += 

        prep_header = "awk" + " " + "'/^>/ {print $1} !/^>/ {print}'" + " "
        prep_header += self.dir_obj.assembly_contigs + " "
        prep_header += ">" + " " 
        prep_header += self.dir_obj.contig_h_fixed

        make_marker = "touch" + " " + marker_path

        return [concoct_prep + " && " + concoct_table_prep + " && " + prep_header + " && " + make_marker]
    

    def concoct_command(self, marker_path):
        run_concoct = self.path_obj.concoct_path + " "
        run_concoct += "--composition_file" + " "
        run_concoct += self.dir_obj.cct_cut_contig + " "
        run_concoct += "--coverage_file" + " "
        run_concoct += self.dir_obj.cct_cov_table + " "
        run_concoct += "-c" + " " + "400" + " "
        run_concoct += "-t" + " " + str(os.cpu_count()) + " "
        run_concoct += "-b" + " " + os.path.join(self.dir_obj.cct_dir_data, "concoct_run")

        merge_cutup = self.path_obj.cct_merge_cutup + " "
        merge_cutup += self.dir_obj.cct_clust + " "
        merge_cutup += ">" + " " 
        merge_cutup += self.dir_obj.cct_clust_merge

        get_bins = self.path_obj.cct_get_bins + " "
        get_bins += self.dir_obj.assembly_contigs + " "
        get_bins += self.dir_obj.cct_clust_merge + " "
        get_bins += "--output_path" + " "
        get_bins += self.dir_obj.cct_bins_dir

        make_marker = "touch" + " " + marker_path

        return [run_concoct + " && " + merge_cutup + " && " + get_bins + " && " + make_marker]

    def checkm_command(self, marker_path):
        set_env = "export" + " "
        set_env += "CHECKM_DATA_PATH="
        set_env += self.path_obj.checkm_ref

        run_checkm = self.path_obj.checkm_path + " "
        run_checkm += "lineage_wf" + " "
        run_checkm += self.dir_obj.cct_bins_dir + " "
        run_checkm += "-x" + " " + ".fa" + " " + "-t" + " " + str(os.cpu_count()) + " "
        run_checkm += self.dir_obj.cct_dir_checkm

        make_marker = "touch" + " " + marker_path

        return [set_env, run_checkm + " && " +  make_marker]
    
    def metabat2_bin_command(self, op_mode, hosts_bypassed, marker_path):

        #metawrap needs specifically-named files for paired
        metabat2_bin = self.path_obj.mwrap_bin_tool + " "
        metabat2_bin += "-o" + " " + self.dir_obj.mbat2_bin_dir_work + " "
        metabat2_bin += "-t" + " " + str(os.cpu_count()) + " "
        metabat2_bin += "-a" + " " + self.dir_obj.assembly_contigs + " "
        
        if(op_mode == "single"):
            metabat2_bin += "--metabat2" + " " + "--single-end" + " "
            if(hosts_bypassed):
                metabat2_bin += self.dir_obj.clean_dir_final_s
            else:
                metabat2_bin += self.dir_obj.host_final_s

        else:
            metabat2_bin += "--metabat2" + " "
            if(hosts_bypassed):
                metabat2_bin += self.dir_obj.clean_dir_final_f + " " + self.dir_obj.clean_dir_final_r
            else:
                metabat2_bin += self.dir_obj.host_final_f + " " + self.dir_obj.host_final_r
        make_marker = "touch" + " " + marker_path

        return [metabat2_bin + " && " + make_marker]
        

    def maxbin2_bin_command(self, op_mode, hosts_bypassed, marker_path):
        maxbin2_command = self.path_obj.mwrap_bin_tool + " "
        maxbin2_command += "-o" + " " + self.dir_obj.mbin2_bin_dir_work + " "
        maxbin2_command += "-t" + " " + str(os.cpu_count()) + " "
        maxbin2_command += "-a" + " " + self.dir_obj.assembly_contigs + " "
        if(op_mode == "single"):
            maxbin2_command += "--maxbin2" + " " + "--single-end" + " "
            if(hosts_bypassed):
                maxbin2_command += self.dir_obj.clean_dir_final_s
            else:
                maxbin2_command += self.dir_obj.host_final_s
        else:
            maxbin2_command += "--maxbin2" + " "
            if(hosts_bypassed):
                maxbin2_command += self.dir_obj.clean_dir_final_f + " " + self.dir_obj.clean_dir_final_r
            else:
                maxbin2_command += self.dir_obj.host_final_f + " " + self.dir_obj.host_final_r

        make_marker = "touch" + " " + marker_path

        return[maxbin2_command + " && " + make_marker]


        
    def metawrap_bin_refinement_command(self, marker_path):
        refine = self.path_obj.mwrap_bin_r_tool + " "
        refine += "-o" + " " + self.dir_obj.mwrap_bin_r_dir_data + " "
        refine += "-t" + " " + str(os.cpu_count()) + " "
        refine += "-A" + " " + self.dir_obj.cct_bins_dir + " "
        refine += "-B" + " " + self.dir_obj.mbat2_bins_dir + " "
        refine += "-C" + " " + self.dir_obj.mbin2_bins_dir + " "
        refine += "-c" + " " + str(50) + " "
        refine += "-x" + " " + str(10)

        make_marker = "touch" + " " + marker_path
        return [refine + " && " + make_marker]
    
    def gtdbtk_command(self, bin_choice, marker_path):
        bin_select = ""
        out_dir = ""
        if(bin_choice == "cct"):
            bin_select = self.dir_obj.cct_bins_dir
            out_dir = self.dir_obj.gtdbtk_dir_cct
        elif(bin_choice == "mbat2"):
            bin_select = self.dir_obj.mbat2_bins_dir
            out_dir = self.dir_obj.gtdbtk_dir_mbat2
        elif(bin_choice == "mbin2"):
            bin_select = self.dir_obj.mbin2_bins_dir
            out_dir = self.dir_obj.gtdbtk_dir_mbin2

        set_env = "export" + " "
        set_env += "GTDBTK_DATA_PATH="
        set_env += self.path_obj.gtdbtk_ref

        classify = self.path_obj.gtdbtk_path + " " + "classify_wf" + " "
        classify += "--skip_ani_screen" + " "
        classify += "--genome_dir" + " " + bin_select + " "
        classify += "--extension" + " " + "fa" + " "
        classify += "--out_dir" + " " + out_dir + " "
        classify += "--cpus" + " " + str(os.cpu_count())

        make_marker = "touch" + " " + marker_path

        return [set_env, classify + " && " + make_marker]
    
    def metawrap_quantify_command(self, bin_choice, forward, reverse, single, marker_path):

        bin_select = ""
        out_dir = ""
        reads_selection = ""
        if(self.op_mode == "single"):
            reads_selection = single
        elif(self.op_mode == "paired"):
            reads_selection = forward + " " + reverse
        
        if(bin_choice == "cct"):
            out_dir = self.dir_obj.mwrap_quant_cct_dir 
            bin_select = self.dir_obj.cct_bins_dir
        elif(bin_choice == "mbat2"):
            out_dir = self.dir_obj.mwrap_quant_mbat2_dir
            bin_select = self.dir_obj.mbat2_bins_dir
        
        elif(bin_choice == "mbin2"):
            out_dir = self.dir_obj.mwrap_quant_mbin2_dir
            bin_select = self.dir_obj.mbin2_bins_dir

        quant = self.path_obj.mwrap_quant_tool + " "
        quant += "-b" + " " + bin_select + " "
        quant += "-o" + " " + out_dir + " "
        quant += "-a" + " " + self.dir_obj.assembly_contigs + " "
        quant += reads_selection + " "
        quant += "-t" + " " + str(os.cpu_count()) 
        make_marker = "touch" + " " + marker_path

        return [quant + " && " + make_marker]