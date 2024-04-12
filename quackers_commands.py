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


    def __init__(self, path_obj, dir_obj):
        #self.path_obj = q_path.path_obj(output_path)
        self.path_obj = path_obj
        self.dir_obj = dir_obj
        self.op_mode = self.path_obj.operating_mode

    def bwa_index_ref(self, ref_path):
        command = self.path_obj.BWA_path
        command += " index " + ref_path
        return [command]

    def clean_reads_bwa_command_s(self, ref_path, in_path, out_path, marker_path):
        command = self.path_obj.BWA_path 
        command += " mem "
        command += ref_path + " "
        command += in_path + " "
        command += ">" + " " + out_path


        sifting_command = self.path_obj.py_path + " "
        sifting_command += self.path_obj.bowtie2_sift + " "
        sifting_command += out_path + " "
        sifting_command += out_path

        make_marker = "touch" + " " + marker_path

        return [command + " && " + sifting_command + " && " + make_marker]


    def clean_reads_command_s(self, ref_path, in_path, out_path, marker_path):
        #to be called on for each host/adapter cluster
        command = self.path_obj.bowtie2_path
        command += " -x " + ref_path
        command += " -q "
        command += " -U " + in_path 
        command += " -S " + out_path
        

        sifting_command = self.path_obj.py_path + " "
        sifting_command += self.path_obj.bowtie2_sift + " "
        sifting_command += out_path + " "
        sifting_command += out_path

        make_marker = "touch"  + " " + marker_path
        return [command + " && " + sifting_command + " && " +  make_marker]
    
    def clean_reads_bwa_command_p(self, ref_path, export_path, in1_path, in2_path, marker_path):
        command = self.path_obj.BWA_path
        command += " mem "
        command += ref_path + " "
        command += in1_path + " "
        command += in2_path + " "
        command += ">" + " " + export_path

        sifting_command = self.path_obj.py_path + " "
        sifting_command += self.path_obj.bowtie2_sift + " "
        sifting_command += export_path + " "#bowtie2_out_path + " "
        sifting_command += export_path #bowtie2_out_path #os.path.join(export_path, "host_only_" + ref_basename + "_paired_out.sam")

        make_marker = "touch" + " " + marker_path

        return [command + " && " + sifting_command + " && " + make_marker]
    
    def clean_reads_command_p(self, ref_path, export_path, in1_path, in2_path, marker_path):
        #to be called on for each host/adapter cluster
        ref_basename = os.path.basename(ref_path)
        #export_path = os.path.dirname(out1_path)
        #bowtie2_out_path = os.path.join(export_path, ref_basename + "_paired_out.sam")
        command = self.path_obj.bowtie2_path
        command += " -x " + ref_path
        command += " -q "
        command += " -1 " + in1_path
        command += " -2 " + in2_path
        command += " -S " + export_path #bowtie2_out_path
        
        sifting_command = self.path_obj.py_path + " "
        sifting_command += self.path_obj.bowtie2_sift + " "
        sifting_command += export_path + " "#bowtie2_out_path + " "
        sifting_command += export_path #bowtie2_out_path #os.path.join(export_path, "host_only_" + ref_basename + "_paired_out.sam")
        
        make_marker = "touch" + " " + marker_path
        return [command + " && " + sifting_command + " && " + make_marker]

    def clean_reads_reconcile(self, sam_path, export_path, s_reads, p1_reads, p2_reads):
        command = self.path_obj.py_path + " "
        command += self.path_obj.bowtie2_reconcile + " "
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

        make_marker = "touch" + " " + self.dir_obj.host_pp_mkr

        return [command + " && " + make_marker]


    def megahit_command_p(self, forward_path, reverse_path, export_path, temp_path):
        command = self.path_obj.megahit_path + " "
        command += "-1" + " " + forward_path + " "
        command += "-2" + " " + reverse_path + " "
        command += "-o" + " " + export_path + " "
        command += "--out-prefix" + " " + "assembled" + " "
        command += "-t" + " " + str(os.cpu_count()) + " "
        command += "-m" + " " + str(0.8) + " "
        command += "--continue" + " "
        command += "--tmp-dir" + " " + temp_path

        make_marker = "touch"  + " "
        make_marker += self.dir_obj.assembly_mkr
        
        return [command + " && " + make_marker]

    def megahit_command_s(self, single_path, export_path, temp_path):
        command = self.path_obj.megahit_path + " "
        command += "-r" + " " + single_path + " "
        command += "-o" + " " + export_path + " "
        command += "--out-prefix" + " " + "assembled" + " "
        command += "-t" + " " + str(os.cpu_count()) + " "
        command += "-m" + " " + str(0.8) + " "
        command += "--continue" + " "
        command += "--tmp-dir" + " " + temp_path

        make_marker = "touch"  + " "
        make_marker += self.dir_obj.assembly_mkr
        
        return [command + " && " + make_marker]
    
    def megahit_pp_command_s(self, single_path, export_path):

        command = self.path_obj.bowtie2_index + " "
        command += self.dir_obj.assembly_contigs + " "
        command += "-c" + " "
        command += "--threads" + " " + str(os.cpu_count())


        scan_for_hits = self.path_obj.bowtie2_path + " "
        scan_for_hits += "-x" + " " + self.dir_obj.assembly_contigs + " "
        scan_for_hits += "-U" + " " + single_path + " "
        scan_for_hits += "-S" + " " + export_path


        return [command + " && " + scan_for_hits]

    def sam_convert_command(self, sam_path, bam_path, sorted_bam_path):
        sam_convert = self.path_obj.samtools_path + " "
        sam_convert += "view" + " " + "-F" + " " + "4" + " " + "-bS" + " "
        sam_convert += sam_path + " "
        sam_convert += ">" + " " + bam_path

        sam_sort = self.path_obj.samtools_path + " "
        sam_sort += "sort" + " "
        sam_sort += bam_path + " "
        sam_sort += "-o" + " " + sorted_bam_path

        sam_index = self.path_obj.samtools_path + " "
        sam_index += "index" + " "
        sam_index += sorted_bam_path

        return [sam_convert + " && "+ sam_sort + " && " + sam_index]


    def bowtie2_index_command(self, ref_path):

        command = self.path_obj.bowtie2_index + " "
        command += ref_path + " "
        command += "-c" + " "
        command += "--threads" + " " + str(os.cpu_count())
        
        return [command]
    
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
        concoct_table_prep += self.dir_obj.assembly_s_bam + " "
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
        get_bins += self.dir_obj.cct_dir_bins

        make_marker = "touch" + " " + marker_path

        return [run_concoct + " && " + merge_cutup + " && " + get_bins + " && " + make_marker]

    def checkm_command(self, marker_path):
        run_checkm = self.path_obj.checkm_path + " "
        run_checkm += "lineage_wf" + " "
        run_checkm += self.dir_obj.cct_dir_bins + " "
        run_checkm += "-x" + " " + ".fa" + " " + "-t" + " " + str(os.cpu_count()) + " "
        run_checkm += self.dir_obj.cct_dir_checkm

        make_marker = "touch" + " " + marker_path

        return [run_checkm + " && " +  make_marker]
    
    def metawrap_bin_command(self, op_mode, hosts_bypassed, marker_path):

        #metawrap needs specifically-named files for paired
        change_f_name = "cp" + " "
        change_r_name = "cp" + " "
        change_s_name = "cp" + " "
        
        if(hosts_bypassed):
            change_f_name += self.dir_obj.start_f + " " + self.dir_obj.mwrap_prep_f
            change_r_name += self.dir_obj.start_r + " " + self.dir_obj.mwrap_prep_r
            change_s_name += self.dir_obj.start_s + " " + self.dir_obj.mwrap_prep_s
        else:
            change_f_name += self.dir_obj.host_final_f + " " + self.dir_obj.mwrap_prep_f
            change_r_name += self.dir_obj.host_final_r + " " + self.dir_obj.mwrap_prep_r
            change_f_name += self.dir_obj.host_final_s + " " + self.dir_obj.mwrap_prep_s
        
        
        metawrap_bin = self.path_obj.mwrap_bin_tool + " "
        metawrap_bin += "-o" + " " + self.dir_obj.mwrap_bin_dir_mbat + " "
        metawrap_bin += "-t" + " " + str(os.cpu_count()) + " "
        metawrap_bin += "-a" + " " + self.dir_obj.assembly_contigs + " "
        
        if(op_mode == "single"):
            metawrap_bin += "--metabat2" + " " + "--single-end" + " "
            if(hosts_bypassed):
                metawrap_bin += self.dir_obj.start_s
            else:
                metawrap_bin += self.dir_obj.host_final_s

        else:
            metawrap_bin += "--metabat2" + " "
            metawrap_bin += self.dir_obj.mwrap_prep_f + " " + self.dir_obj.mwrap_prep_r
            
        make_marker = "touch" + " " + marker_path

        if(op_mode == "paired"):
            return [change_f_name + " && " + change_r_name + " && " + metawrap_bin + " && " + make_marker]
        else:
            return [change_s_name + " && "  + metawrap_bin + " && " + make_marker]
        
    def metawrap_bin_refinement_command(self, marker_path):
        refine = self.path_obj.mwrap_bin_r_tool + " "
        refine += "-o" + " " + self.dir_obj.mwrap_bin_r_dir_data + " "
        refine += "-t" + " " + str(os.cpu_count()) + " "
        refine += "-A" + " " + self.dir_obj.mwrap_bins_dir + " "
        refine += "-c" + " " + str(50) + " "
        refine += "-x" + " " + str(10)

        make_marker = "touch" + " " + marker_path

        return [refine + " && " + marker_path]
    
    def gtdbtk_command(self, marker_path):
        classify = self.path_obj.gtdbtk_path + " " + "classify_wf" + " "
        classify += "--skip_ani_screen" + " "
        classify += "--genome_dir" + " " + self.dir_obj.mwrap_bin_r_dir_data + " "
        classify += "--extension" + " " + "fa" + " "
        classify += "--out_dir" + " " + self.dir_obj.gtdbtk_dir_data + " "
        classify += "--cpus" + " " + str(os.cpu_count())

        make_marker = "touch" + " " + marker_path

        return [classify + " && " + make_marker]