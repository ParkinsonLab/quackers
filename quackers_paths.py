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
        return False
    
    

    def __init__(self, output_folder_path, config_path = None):
        config = ConfigParser()
        if(config_path is None):
            print("No config: Using default")
        else:
            config.read(config_path)
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


        #---------------------------------------------------------------
        #libraries
        
        print("categories in config:", len(config.keys()))
        for item in config.keys():
            print(item)

        if("hosts" in config):
            number_of_hosts = len(config["hosts"])

            print("number of hosts:", number_of_hosts)
            for host_entry in config["hosts"]:
                #print(host_entry)
                self.check_lib_integrity(host_entry)
        
        else:
            print("no hosts section found in Config")

        




