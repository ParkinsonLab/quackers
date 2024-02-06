from xml.dom.pulldom import default_bufsize
from distutils.core import extension_keywords
import os
import sys
import time
from datetime import datetime as dt
from configparser import ConfigParser

#class that stores all tool paths for Quackers.


class path_obj:

    def check_lib_integrity(self, lib_path):
        if os.path.exists(lib_path):
            if(os.path.getsize(lib_path) > 0):
                if((lib_path.endswith(".fasta")) or (lib_path.endswith(".fa")) or (lib_path.endswith(".fna"))):
                    return True
                else:
                    print("library not a fasta/fa/fna file", lib_path)
            else:
                print("library points to empty file:", lib_path)
        else:
            print("library path doesn't exist:", lib_path)
        exit_statement = "bad library: " + lib_path 
        sys.exit(exit_statement)
    

    def assign_value(self, key0, key1, default_value):
        #looks for dual-layered keys off config map
        if(key0 in self.config):
            settings_map = self.config[key0]
            if(key1 in settings_map):
                return settings_map[key1]
        else:
            print(key0 + " not found in config: default used:", default_value)
        
        return default_value

    def __init__(self, output_folder_path, config_path = None):
        self.config = ConfigParser()
        if(config_path is None):
            print("No config: Using default")
        else:
            self.config.read(config_path)
            print("Config found: using custom args")
        self.output_path = output_folder_path   

        self.tool_install_path = "/quackers_tools"

        self.megahit_path   = os.path.join(self.tool_install_path, "megahit", "bin", "megahit")
        self.samtools_path  = "samtools"
        self.bowtie2_path   = os.path.join(self.tool_install_path, "bowtie2", "bowtie2")
        self.concoct_path   = "concoct"
        self.checkm_path    = "checkm"
        self.ar_path        = os.path.join(self.tool_install_path, "adapterremoval", "AdapterRemoval")
        self.cdhit_path     = os.path.join(self.tool_install_path, "cdhit_dup", "cd-hit-dup")
        self.bbduk_path     = os.path.join(self.tool_install_path, "bbmap", "bbduk.sh")


        #------------------------------------------------------------------
        #Assign singular values for settings


        self.operating_mode = self.assign_value("settings", "operating_mode", "single")
        self.BBMAP_k        = self.assign_value("BBMAP_settings", "k", 25)
        self.BBMAP_hdist    = self.assign_value("BBMAP_settings", "hdist", 1)
        self.BBMAP_ftm      = self.assign_value("BBMAP_settings", "ftm", 5)

        #--------------------------------------------------------------
        #directory structure



        #---------------------------------------------------------------
        #libraries

        #multi-host support:
        #expecting to loop over all hosts.
        self.hosts_path_dict = dict()
        if("hosts" in self.config):
            number_of_hosts = len(self.config["hosts"])

            print("number of hosts:", number_of_hosts)
            for host_entry in self.config["hosts"]:
                #print(host_entry)
                self.check_lib_integrity(host_entry)
                self.hosts_path_dict[str(host_entry)] = self.assign_value("hosts", host_entry, "none")
        
        else:
            print("no hosts section found in Config")

        if("artifacts" in self.config):
            for artifact_entry in self.config["artifacts"]):
                self.check_lib_integrity(artifact_entry)

        




