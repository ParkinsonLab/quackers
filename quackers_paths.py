from xml.dom.pulldom import default_bufsize
from distutils.core import extension_keywords
import os
import sys
import time
from datetime import datetime as dt
from configparser import ConfigParser



def make_folder(dir):
    if(not os.path.exists(dir)):
        os.makedirs(dir, mode=0o777, exist_ok=False)

class dir_structure:
    def __init__(self, args_pack, path_obj):
        os.umask(0)
        self.output_dir = args_pack["out"]

        self.start_f = args_pack["p1_path"] 
        self.start_r = args_pack["p2_path"]
        self.start_s = args_pack["s_path"]

        self.clean_dir_top = os.path.join(self.output_dir, path_obj.clean_dir)
        self.clean_dir_data = os.path.join(self.clean_dir_top, "data")
        self.clean_dir_end = os.path.join(self.clean_dir_top, "export")

        self.clean_dir_AR_s0 = os.path.join(self.clean_dir_data, "s0.fastq")
        self.clean_dir_AR_sf = os.path.join(self.clean_dir_data, "sf.fastq")
        self.clean_dir_AR_sr = os.path.join(self.clean_dir_data, "sr.fastq")
        self.clean_dir_AR_f = os.path.join(self.clean_dir_data, "AR_f.fastq")
        self.clean_dir_AR_r = os.path.join(self.clean_dir_data, "AR_r.fastq")
        self.clean_dir_AR_s = os.path.join(self.clean_dir_data, "AR_s.fastq")
        self.clean_dir_final_s = os.path.join(self.clean_dir_end, "single.fastq")
        #specifically-named for metawrap binning.
        self.clean_dir_final_f = os.path.join(self.clean_dir_end, "pair_1.fastq")
        self.clean_dir_final_r = os.path.join(self.clean_dir_end, "pair_2.fastq")
        self.clean_dir_job = os.path.join(self.clean_dir_top, "AR.sh")
        self.clean_dir_mkr = os.path.join(self.clean_dir_top, "clean_AR")
        
        make_folder(self.clean_dir_top)
        make_folder(self.clean_dir_data)
        make_folder(self.clean_dir_end)

        self.host_dir_top   = os.path.join(self.output_dir, path_obj.host_dir)
        self.host_dir_data  = os.path.join(self.host_dir_top, "data")
        self.host_dir_sam   = os.path.join(self.host_dir_data, "sam")
        self.host_dir_end   = os.path.join(self.host_dir_top, "export")
        
        self.host_final_f  = os.path.join(self.host_dir_end, "pair_1.fastq")
        self.host_final_r  = os.path.join(self.host_dir_end, "pair_2.fastq")
        self.host_final_s   = os.path.join(self.host_dir_end, "single.fastq")

        self.host_mkr = os.path.join(self.host_dir_top, "host_filter")
        self.host_bwa_mkr = os.path.join(self.host_dir_top, "host_filter_bwa")
        self.host_pp_mkr = os.path.join(self.host_dir_top, "host_filter_reconcile")

        self.host_recon_job = os.path.join(self.host_dir_top, "reconcile.sh")
        self.host_clean_bwa_p_job = os.path.join(self.host_dir_top, "host_clean_bwa_p.sh")
        self.host_clean_bwa_s_job = os.path.join(self.host_dir_top, "host_clean_bwa_s.sh")

        make_folder(self.host_dir_top)
        make_folder(self.host_dir_data)
        make_folder(self.host_dir_sam)
        make_folder(self.host_dir_end)
        
        self.assembly_dir_top   = os.path.join(self.output_dir, path_obj.assembly_dir)
        self.assembly_dir_data  = os.path.join(self.assembly_dir_top, "data")
        self.assembly_dir_end   = os.path.join(self.assembly_dir_top, "export")
        self.assembly_dir_temp  = os.path.join(self.assembly_dir_top, "temp")
        self.assembly_contigs   = os.path.join(self.assembly_dir_data, "contigs.fasta")
        self.assembly_dir_bt2_idx   = os.path.join(self.assembly_dir_data, "bt2_idx")
        self.assembly_bt2_idx   = os.path.join(self.assembly_dir_bt2_idx, "contigs")
        self.assembly_raw_sam   = os.path.join(self.assembly_dir_data, "raw_bt2_out.sam")
        self.assembly_raw_bam   = os.path.join(self.assembly_dir_data, "raw_bt2_out.bam")
        self.assembly_sort_bam  = os.path.join(self.assembly_dir_data, "bt2_sort.bam")
        
        self.assembly_score_out = os.path.join(self.assembly_dir_data, "score_bt2.out") 
        self.assembly_final_c   = os.path.join(self.assembly_dir_data, "contigs.fasta")
        self.assembly_final_s   = os.path.join(self.assembly_dir_end, "single.fastq")
        self.assembly_final_f   = os.path.join(self.assembly_dir_end, "forward.fastq")
        self.assembly_final_r   = os.path.join(self.assembly_dir_end, "reverse.fastq")

        self.assembly_mspades_s_job = os.path.join(self.assembly_dir_top, "assemble_s.sh")
        self.assembly_mspades_p_job = os.path.join(self.assembly_dir_top, "assemble_p.sh")
        self.assembly_bwa_idx_job = os.path.join(self.assembly_dir_top, "index_contigs.sh")
        self.assembly_pp_job = os.path.join(self.assembly_dir_top, "clean_reads.sh")
        self.assembly_recon_job = os.path.join(self.assembly_dir_top, "clean_reads_reconcile.sh")
        self.assembly_scan_sam_job = os.path.join(self.assembly_dir_top, "scan_sam.sh")

        self.assembly_sam_convert_job = os.path.join(self.assembly_dir_top, "sam_convert.sh")

        self.assembly_mkr                       = os.path.join(self.assembly_dir_top, "assembly_mspades")
        self.assembly_bt2_idx_mkr               = os.path.join(self.assembly_dir_top, "assembly_bt2_idx")
        self.assembly_bwa_idx_mkr               = os.path.join(self.assembly_dir_top, "assembly_bwa_idx")
        self.assembly_scan_sam_mkr              = os.path.join(self.assembly_dir_top, "assembly_scan_sam")

        self.assembly_pp_mkr                    = os.path.join(self.assembly_dir_top, "assembly_bwa_pp")

        self.assembly_reconcile_mkr             = os.path.join(self.assembly_dir_top, "assembly_reconcile")
        self.assembly_sam_convert_mkr   = os.path.join(self.assembly_dir_top, "assembly_sam_convert")

        make_folder(self.assembly_dir_top)
        make_folder(self.assembly_dir_temp)
        make_folder(self.assembly_dir_data)
        make_folder(self.assembly_dir_end)
        make_folder(self.assembly_dir_bt2_idx)

        self.cct_dir_top            = os.path.join(self.output_dir, path_obj.cct_bin_dir)
        self.cct_dir_data           = os.path.join(self.cct_dir_top, "data")
        self.cct_dir_checkm     = os.path.join(self.cct_dir_top, "checkm_data")
        self.cct_dir_bins       = os.path.join(self.cct_dir_top, "bins")
        self.cct_dir_export     = os.path.join(self.cct_dir_top, "export")
        self.cct_bed            = os.path.join(self.cct_dir_data, "contigs.bed")
        self.cct_cut_contig     = os.path.join(self.cct_dir_data, "cut_contgs.fa")
        self.cct_cov_table      = os.path.join(self.cct_dir_data, "coverage_table.tsv")
        self.contig_h_fixed     = os.path.join(self.cct_dir_data, "assembled_contigs_header_patch.fa")
        self.cct_clust          = os.path.join(self.cct_dir_data, "concoct_run_clustering_gt1000.csv")
        self.cct_clust_merge    = os.path.join(self.cct_dir_data, "concoct_merged_cluster.csv")
        
        self.cct_prep_mkr       = os.path.join(self.cct_dir_top, "concoct_prep")
        self.cct_mkr            = os.path.join(self.cct_dir_top, "concoct_binning")
        self.cct_checkm_mkr     = os.path.join(self.cct_dir_top, "checkm")

        self.cct_prep_job_path  = os.path.join(self.cct_dir_top, "cct_prep.sh")
        self.cct_job_path  = os.path.join(self.cct_dir_top, "cct.sh")
        self.cct_checkm_job_path = os.path.join(self.cct_dir_top, "cct_checkm.sh")

        self.mbat2_bin_dir_top = os.path.join(self.output_dir, path_obj.mbat2_bin_dir)
        self.mbat2_bin_dir_data = os.path.join(self.mbat2_bin_dir_top, "data")
        self.mbat2_bin_dir_work = os.path.join(self.mbat2_bin_dir_top, "metabat2")
        self.mbat2_fastq = os.path.join(self.mbat2_bin_dir_export, "mwrap_mbat_bin_contigs.fastq")
        
        self.mbat2_bins_dir = os.path.join(self.mbat2_bin_dir_mbat, "metabat2_bins")
        self.mbat2_mkr = os.path.join(self.mbat2_bin_dir_top, "mbat2_bin")
        self.mbat2_job = os.path.join(self.mbat2_bin_dir_top, "mbat2.sh")



        self.mbin2_bin_dir_top = os.path.join(self.output_dir, path_obj.mbin2_bin_dir)
        self.mbin2_bin_dir_work = os.path.join(self.mbin2_bin_dir_top, "maxbin2")
        self.mbin2_bins_dir     = os.path.join(self.mbin2_bin_dir_work, "maxbin2_bins")
        self.mbin2_mkr = os.path.join(self.mbin2_bin_dir_top, "mbin2_bin")
        self.mbin2_job  = os.path.join(self.mbin2_bin_dir_top, "mbin2.sh")


        self.mwrap_bin_r_dir_top    = os.path.join(self.output_dir, path_obj.mwrap_bin_r_dir)
        self.mwrap_bin_r_dir_data   = os.path.join(self.mwrap_bin_r_dir_top, "data")
        self.mwrap_bin_r_job = os.path.join(self.mwrap_bin_r_dir_top, "mwrap_bin_r.sh")
        self.mwrap_bin_r_mkr = os.path.join(self.mwrap_bin_r_dir_top, "mwrap_bin_r")

        self.gtdbtk_dir_top = os.path.join(self.output_dir, path_obj.gtdbtk_class_dir)
        self.gtdbtk_dir_data = os.path.join(self.gtdbtk_dir_top, "data")
        self.gtdbtk_job = os.path.join(self.gtdbtk_dir_top, "gtdbtk_classify.sh")
        self.gtdbtk_mkr = os.path.join(self.gtdbtk_dir_top, "gtdbtk_run")

        self.mwrap_quant_dir_top    = os.path.join(self.output_dir, path_obj.mwrap_quant_dir)
        self.mwrap_quant_dir_data   = os.path.join(self.mwrap_quant_dir_top, "data")
        self.mwrap_quant_job = os.path.join(self.mwrap_quant_dir_top, "mwrap_quant.sh")
        self.mwrap_quant_mkr = os.path.join(self.mwrap_quant_dir_top, "")


        


        make_folder(self.cct_dir_top)
        make_folder(self.cct_dir_data)
        make_folder(self.cct_dir_bins)
        make_folder(self.cct_dir_checkm)
        make_folder(self.cct_dir_export)

        make_folder(self.mwrap_bin_dir_top)
        make_folder(self.mwrap_bin_dir_data)
        make_folder(self.mwrap_bin_dir_prep)
        make_folder(self.mwrap_bin_dir_mbat)
        make_folder(self.mwrap_bin_dir_export)

        make_folder(self.mwrap_bin_r_dir_top)
        make_folder(self.mwrap_bin_r_dir_data)

        make_folder(self.gtdbtk_dir_top)
        make_folder(self.gtdbtk_dir_data)

        make_folder(self.mwrap_quant_dir_top)
        make_folder(self.mwrap_quant_dir_data)

#classes that store all tool paths for Quackers.
#also classes that store all datapaths.

class data_paths:
    #A series of dictionaries to track all output locations.
    #Used as a way to track the paths of multiple host filters.
    
    def __init__(self):
        #reminder/note: these aren't supposed to store sequential paths.  They should all be run in parallel
        #and be reconciled before moving on.    


        self.p1_host_out_path_dict = dict()
        self.p2_host_out_path_dict = dict()
        self.s_host_out_path_dict = dict()


class path_obj:


    def check_if_indexed(self, lib_path):
        print("looking at:", lib_path)
        if os.path.exists(lib_path):
            list_of_files = os.listdir(lib_path)
            bt2_count = 0
            for item in list_of_files:
                if(item.endswith(".bt2")):
                    file_path = os.path.join(lib_path, item)
                    if(os.path.getsize(file_path)>0):
                        bt2_count += 1

            if(bt2_count > 0):
                return True
            else:
                sys.exit("no bowtie2 indexed files found")


    def check_if_indexed_bwa(self, lib_file):
        lib_path = os.path.dirname(lib_file)

        print("looking at:", lib_path)
        if os.path.exists(lib_path):
            list_of_files = os.listdir(lib_path)
            ok_count = 0
            for item in list_of_files:
                if(item.endswith(".bwt")):
                    file_path = os.path.join(lib_path, item)
                    if(os.path.getsize(file_path)>0):
                        ok_count += 1

                elif(item.endswith(".amb")):
                    file_path = os.path.join(lib_path, item)
                    if(os.path.getsize(file_path)>0):
                        ok_count += 1
                elif(item.endswith(".ann")):
                    file_path = os.path.join(lib_path, item)
                    if(os.path.getsize(file_path)>0):
                        ok_count += 1
                elif(item.endswith(".pac")):
                    file_path = os.path.join(lib_path, item)
                    if(os.path.getsize(file_path)>0):
                        ok_count += 1
                elif(item.endswith(".sa")):
                    file_path = os.path.join(lib_path, item)
                    if(os.path.getsize(file_path)>0):
                        ok_count += 1
            if(ok_count >= 5):
                print("LIB is BWA-INDEXED")
                return True
            else:
                print("NOT INDEXED")
                sys.exit("not enough BWA index files found")
        else:
            print("lib path does not exist")
            sys.exit("not valid library")
    
    def check_lib_integrity(self, lib_path):
        print("looking at:", lib_path)
        if os.path.exists(lib_path):
            if(os.path.getsize(lib_path) > 0):
                if((lib_path.endswith(".fasta")) or (lib_path.endswith(".fa")) or (lib_path.endswith(".fna"))):
                    print("library check: OK!")
                    return True
                else:
                    print("library not a fasta/fa/fna file", lib_path)
            else:
                print("library points to empty file:", lib_path)
        else:
            print("library path doesn't exist:", lib_path)
        exit_statement = "bad library: " + lib_path 
        sys.exit(exit_statement)
    

    def assign_value(self, key0, key1, type, default_value):
        #looks for dual-layered keys off config map
        export_value = default_value
        if(key0 in self.config):
            settings_map = self.config[key0]
            if(key1 in settings_map):
                export_value = settings_map[key1]
        else:
            print(key0 + " not found in config: default used:", default_value)
            
        
        if(type == "str"):
            export_value = str(export_value)
        elif(type == "int"):
            export_value = int(export_value)
        elif(type == "float"):
            export_value = float(export_value)
        elif(type == "flag"):
            if((export_value == "yes") or (export_value == "Yes") or (export_value == "y") or (export_value == "Y")):
                export_value = True
            else:
                export_value = False
        
        return export_value

    def __init__(self, output_folder_path, config_path = None):
        self.config = ConfigParser()
        if(not config_path):
            print("No config: Using default")
        else:
            self.config.read(config_path)
            print("Config found: using custom args")
        self.output_path = output_folder_path   


        

        self.tool_install_path = "/quackers_tools"
        self.temp_internal_scripts_path = "/home/billy/storage/quackers"
        #self.mwrap_temp_path = os.path.join(self.temp_internal_scripts_path, "modded_scripts")

        self.megahit_path       = os.path.join(self.tool_install_path, "megahit", "bin", "megahit")
        self.samtools_path      = "samtools"
        self.bowtie2_path       = os.path.join(self.tool_install_path, "bowtie2", "bowtie2")
        self.bowtie2_idx_path   = os.path.join(self.tool_install_path, "bowtie2", "bowtie2-build")
        self.concoct_path       = "concoct"
        self.checkm_path        = "checkm"
        self.ar_path            = os.path.join(self.tool_install_path, "adapterremoval", "AdapterRemoval")
        self.cdhit_path         = os.path.join(self.tool_install_path, "cdhit_dup", "cd-hit-dup")
        self.bbduk_path         = os.path.join(self.tool_install_path, "bbmap", "bbduk.sh")
        self.py_path            = "python3"
        self.BWA_path           = "bwa"
        self.mspades_path       = "metaspades.py"
        #self.mwrap_bin_tool     = os.path.join(self.mwrap_temp_path, "binning.sh")
        #print("TEST")
        #time.sleep(10)
        self.gtdbtk_path        = "gtdbtk"
        self.mwrap_bin_tool     = "metawrap binning"
        self.mwrap_bin_r_tool   = "metawrap bin_refinement"
        self.mwrap_quant_tool   = "metawrap quant_bins"
        self.cct_cut_up_fasta   = "python3" + " " + os.path.join(self.tool_install_path, "concoct", "scripts", "cut_up_fasta.py")
        self.cct_cov_table      = "python3" + " " + os.path.join(self.temp_internal_scripts_path, "modded_scripts", "concoct_coverage_table.py")
        self.cct_merge_cutup    = "python3" + " " + os.path.join(self.temp_internal_scripts_path, "modded_scripts", "merge_cutup_clustering.py")
        self.cct_get_bins       = "python3" + " " + os.path.join(self.temp_internal_scripts_path, "modded_scripts", "extract_fasta_bins.py")



        #---------------------------------------------------------------------------
        #Assign paths for scripts
        self.sam_sift               = self.assign_value("scripts", "sam_sift", "str", "scripts/sam_sift.py")
        self.clean_reads_reconcile  = self.assign_value("scripts", "clean_reads_reconcile", "str", "scripts/clean_reads_reconcile.py")
        self.AR_reconcile           = self.assign_value("scripts", "AR_reconcile", "str", "scripts/AR_reconcile.py")
        self.contig_reconcile       = self.assign_value("scripts", "contig_reconcile", "str", "scripts/contig_reconcile.py")

        #------------------------------------------------------------------
        #Assign singular values for settings

        self.bypass_log         = self.assign_value("settings", "bypass_log_name", "str", "bypass_log.txt")
        self.bypass_log         = os.path.join(self.output_path, self.bypass_log)
        self.operating_mode     = self.assign_value("settings", "operating_mode", "str", "single")
        self.BBMAP_k            = self.assign_value("BBMAP_settings", "k", "int", 25)
        self.BBMAP_hdist        = self.assign_value("BBMAP_settings", "hdist", "int", 1)
        self.BBMAP_ftm          = self.assign_value("BBMAP_settings", "ftm", "int", 5)

        self.megahit_contig_len = self.assign_value("MEGAHIT_settings", "contig_len", "int", 1000)
        self.megehit_threads    = self.assign_value("settings", "threads", "int", 64)
        self.AR_minlength       = self.assign_value("settings", "AdapterRemoval_minlength", "int", 30)
        

        #--------------------------------------------------------------
        #directory structure

        self.clean_dir          = self.assign_value("directory", "clean_reads", "str", "0_clean_reads")
        self.host_dir           = self.assign_value("directory", "host_filter", "str", "1_host_filter")
        self.assembly_dir       = self.assign_value("directory", "contig_assembly", "str", "2_contig_assemble")
        self.cct_bin_dir        = self.assign_value("directory", "contig_binning", "str", "3a_conconct_binning")
        self.mbin2_bin_dir       = self.assign_value("directory", "maxbin2_binning", "str", "3b_maxbin2_binning")
        self.mbat2_bin_dir      = self.assign_value("directory", "metabat2_binning", "str", "3c_metabat2_binning")
        self.mwrap_bin_r_dir    = self.assign_value("directory", "metawrap_bin_refinement", "str", "4_mwrap_bin_r")
        self.gtdbtk_class_dir   = self.assign_value("directory", "gtdbtk_classify", "str", "5_gtdbtk_classify")
        self.mwrap_quant_dir    = self.assign_value("directory", "metawrap_quant_bin", "str", "6_metawrap_quant_bins")

        #-----------------------------------------------------------
        #keep flags
        self.keep_all       = self.assign_value("keep_options", "all", "flag", "yes")
        self.keep_trim      = self.assign_value("keep_options", "trim", "flag", "yes")
        self.keep_host      = self.assign_value("keep_options", "host", "flag", "yes")
        self.keep_bin       = self.assign_value("keep_options", "bin", "flag", "yes")
        

 
        #---------------------------------------------------------------
        #libraries

        #multi-host support:
        #expecting to loop over all hosts.
        self.hosts_path_dict = dict()

        if(not "hosts" in self.config):
            print("no hosts section found in Config")
        else:
            number_of_hosts = len(self.config["hosts"])
            print("number of hosts:", number_of_hosts)
            for host_entry in self.config["hosts"]:
                #print(host_entry)
                #self.check_lib_integrity(self.config["hosts"][host_entry])
                #self.check_if_indexed(self.config["hosts"][host_entry])
                self.check_if_indexed_bwa(self.config["hosts"][host_entry])
                
                self.hosts_path_dict[str(host_entry)] = self.assign_value("hosts", host_entry, "str", "none")
                print("check host:", "key:", host_entry, "value:", self.hosts_path_dict[str(host_entry)])
                
        
        if("artifacts" in self.config):
            for artifact_entry in self.config["artifacts"]:
                self.check_lib_integrity(artifact_entry)

        self.gtdbtk_ref = self.assign_value("databases", "gtdbtk", "str", "databases/gtdbtk_placeholder")
        if(os.path.getsize(self.gtdbtk_ref) > 0):
            print("GTDBTK db OK")
        else:
            sys.exit("GTDBTK db empty. Exiting.")
        




