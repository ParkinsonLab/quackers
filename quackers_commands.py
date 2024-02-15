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


    def __init__(self, output_path):
        self.path_obj = q_path.path_obj(output_path)
        self.op_mode = self.path_obj.operating_mode

    

    def clean_reads_single_command(self, ref_path, in_path, out_path):
        #to be called on for each host/adapter cluster
        command = self.path_obj.bbduk_path + " "
        command += "in=" + in_path + " "
        command += "out=" + out_path + " "
    
        command += "k=" + str(self.path_obj.BBMAP_k) + " "
        command += "ftm=" + str(self.path_obj.BBMAP_ftm) + " "
        command += "hdist=" + str(self.path_obj.BBMAP_hdist) + " "
        command += "ref=" + ref_path

        return [command]
    
    def clean_reads_paired_command(self, ref_path, in1_path, in2_path, out1_path, out2_path):
        #to be called on for each host/adapter cluster
        command = self.path_obj.bbduk_path + " "
        
        command += "in1=" + in1_path + " "
        command += "in2=" + in2_path + " "
        command += "out1=" + out1_path + " "
        command += "out2=" + out2_path + " "

        command += "k=" + str(self.path_obj.BBMAP_k) + " "
        command += "ftm=" + str(self.path_obj.BBMAP_ftm) + " "
        command += "hdist=" + str(self.path_obj.BBMAP_hdist) + " "
        command += "ref=" + ref_path
        
        return [command]

    def megahit_command(self):
        command = self.path_obj.megahit_path + " "
        command += "-r" + " "
        

    def bowtie2_index_command(self, lib_path):
        command = self.path_obj.bowtie2_path + "-build" + " "
        command += lib_path + " "

    

        