import os
import sys
import time
from datetime import datetime as dt
import MetaPro_utilities as mpu
import quackers_paths as q_path

class quackers_command:
    def make_folder(folder_path):
        if(not os.path.exists(folder_path)):
            os.mkdir(folder_path)


    def __init__(self):
        self.path_obj = q_path.quackers_path()
        self.op_mode = self.path_obj.operating_mode

    def adapterremoval_command(self):
        command = self.path_obj.ar_path + " "
        command += 

    def cleaning_trim_reads_command(self, host_path):
        #to be called on for each host
        command = self.path_obj.bbduk_path + " "
        if(self.op_mode == "single"):

            command += "in=" + 
            command += "out=" +
            
        else:
            command += "in1=" + 
            command += "in2=" + 
            command += "out1=" + 
            command += "out2=" + 

        command += "k=" + self.BBMAP_k + " "
        command += "ftm=" + self.BBMAP_ftm + " "
        command += "hdist=" + self.BBMAP_hdist + " "
        command += "ref=" + host_path
        

    def megahit_command(self):
        command = self.path_obj.megahit_path + " "
        command += 

    def bowtie2_index_command(self, lib_path):
        command = self.path_obj.bowtie2_path + "-build" + " "
        command += lib_path + " "

    def cleaning_trim_reads_command(self):
        command = self.path_obj.bbduk_path + " "
        if(self.op_mode == "single"):

            command += "in=" + 
            command += "out=" +
            
        else:
            command += "in1=" + 
            command += "in2=" + 
            command += "out1=" + 
            command += "out2=" + 

        command += "k=" + self.BBMAP_k + " "
        command += "ftm=" + self.BBMAP_ftm + " "
        command += "hdist=" + self.BBMAP_hdist + " "
        command += "ref"

        