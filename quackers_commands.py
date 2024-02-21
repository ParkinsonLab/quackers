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


    def __init__(self, path_obj):
        #self.path_obj = q_path.path_obj(output_path)
        self.path_obj = path_obj
        self.op_mode = self.path_obj.operating_mode

    

    def clean_reads_single_command(self, ref_path, in_path, out_path):
        #to be called on for each host/adapter cluster
        command = self.path_obj.bowtie2_path
        command += " -x " + ref_path
        command += " -U " + in_path 
        command += " -b " + out_path
        command += " -q "


        return [command]
    
    def clean_reads_paired_command(self, ref_path, in1_path, in2_path, out1_path, out2_path):
        #to be called on for each host/adapter cluster
        command = self.path_obj.bowtie2_path
        command += " -x " + ref_path
        command += " -1 " + in1_path
        command += " -2 " + in2_path
        #command += " -b " + out1_path 
        command += " -q "
        command += "-S " + out1_path
        #command += " --align-paired-reads " 

        return [command]

    def megahit_command(self):
        command = self.path_obj.megahit_path + " "
        command += "-r" + " "
        

    def bowtie2_index_command(self, lib_path):
        command = self.path_obj.bowtie2_path + "-build" + " "
        command += lib_path + " "

    

        