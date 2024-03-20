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
    def __init__(self, out_path, path_obj):
        os.umask(0)
        self.output_dir = out_path

        self.host_dir_top   = os.path.join(self.output_dir, path_obj.host_dir)
        self.host_dir_data  = os.path.join(self.host_dir_top, "data")
        self.host_dir_end   = os.path.join(self.host_dir_top, "export")
        self.host_final_f  = os.path.join(self.host_dir_end, "forward.fastq")
        self.host_final_r  = os.path.join(self.host_dir_end, "reverse.fastq")
        self.host_final_s   = os.path.join(self.host_dir_end, "single.fastq")

        self.host_mkr = os.path.join(self.host_dir_top, "host_filter")

        make_folder(self.host_dir_top)
        make_folder(self.host_dir_data)
        make_folder(self.host_dir_end)
        
        self.assembly_dir_top   = os.path.join(self.output_dir, path_obj.assemble_dir)
        self.assembly_dir_data  = os.path.join(self.assembly_dir_top, "data")
        self.assembly_dir_end   = os.path.join(self.assembly_dir_top, "export")
        self.assembly_dir_temp  = os.path.join(self.assembly_dir_top, "temp")
        self.assembly_contigs   = os.path.join(self.assembly_dir_data, "assembled.contigs.fa")
        self.assembly_bwa       = os.path.join(self.assembly_dir_data, "bwa_out.sam")
        self.assembly_final_c   = os.path.join(self.assembly_dir_data, "assembled_contigs.fa")
        self.assembly_final_s   = os.path.join(self.assembly_dir_end, "single.fastq")
        self.assembly_final_f   = os.path.join(self.assembly_dir_end, "forward.fastq")
        self.assembly_final_r   = os.path.join(self.assembly_dir_end, "reverse.fastq")



        self.assembly_mkr        = os.path.join(self.assembly_dir_top, "assembly_megahit")
        self.assembly_pp_mkr     = os.path.join(self.assembly_dir_top, "assembly_bwa_pp")
        self.assembly_reconcile_mkr = os.path.join(self.assembly_dir_top, "assembly_reconcile")
        self.cct_top            = os.path.join(self.output_dir, path_obj.contig_binning)
        self.cct_data           = os.path.join(self.cct_top, "data")
        self.cct_bed            = os.path.join(self.cct_data, "contigs.bed")
        self.cct_cut_contig     = os.path.join(self.cct_data, "cut_contgs.fa")
        self.contig_h_fixed     = os.path.join(self.cct_data, "assembled_contigs_header_patch.fa")

        make_folder(self.assembly_dir_top)
        make_folder(self.assembly_dir_temp)
        #make_folder(self.assembly_dir_data)
        make_folder(self.assembly_dir_end)

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

        self.megahit_path       = os.path.join(self.tool_install_path, "megahit", "bin", "megahit")
        self.samtools_path      = "samtools"
        self.bowtie2_path       = os.path.join(self.tool_install_path, "bowtie2", "bowtie2")
        self.bowtie2_index      = os.path.join(self.tool_install_path, "bowtie2", "bowtie2-build")
        self.concoct_path       = "concoct"
        self.checkm_path        = "checkm"
        self.ar_path            = os.path.join(self.tool_install_path, "adapterremoval", "AdapterRemoval")
        self.cdhit_path         = os.path.join(self.tool_install_path, "cdhit_dup", "cd-hit-dup")
        self.bbduk_path         = os.path.join(self.tool_install_path, "bbmap", "bbduk.sh")
        self.py_path            = "python3"
        self.BWA_path           = os.path.join(self.tool_install_path, "BWA", "bwa")
        self.cct_cut_up_fasta   = "python3" + " " + os.path.join(self.tool_install_path, "concoct", "scripts", "cut_up_fasta.py")
        self.cct_cov_table      = "python3" + " " + os.path.join(self.tool_install_path, "concoct", "scripts", "concoct_coverage_table.py")
        


        #---------------------------------------------------------------------------
        #Assign paths for scripts
        self.bowtie2_sift       = self.assign_value("scripts", "bowtie2_sift", "str", "scripts/bowtie2_sift.py")
        self.bowtie2_reconcile  = self.assign_value("scripts", "bowtie2_reconcile", "str", "scripts/clean_reads_reconcile.py")

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
        

        #--------------------------------------------------------------
        #directory structure

        self.host_dir       = self.assign_value("directory", "host_filter", "str", "1_host_filter")
        self.assemble_dir   = self.assign_value("directory", "contig_assembly", "str", "2_megahit_assemble")
        self.contig_binning = self.assign_value("directory", "contig_binning", "str", "3_contig_binning")

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

        




