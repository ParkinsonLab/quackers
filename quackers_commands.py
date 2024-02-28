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

    

    def clean_reads_command_s(self, ref_path, in_path, out_path):
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

        return [command + " && " + sifting_command]
    
    def clean_reads_command_p(self, ref_path, export_path, in1_path, in2_path, ):
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
        
        
        return [command + " && " + sifting_command]

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



        return [command]


    def megahit_command_p(self, forward_path, reverse_path, export_path):
        command = self.path_obj.megahit_path + " "
        command += "-1" + " " + forward_path + " "
        command += "-2" + " " + reverse_path + " "
        command += "-o" + " " + export_path + " "
        command += "--out-prefix" + " " + "assembled_contigs" + " "
        command += "-t" + " " + str(os.cpu_count()) + " "
        command += "-m" + " " + 0.8
        
        return [command]

    def megahit_command_s(self, single_path, export_path):
        command = self.path_obj.megahit_path + " "
        command += "-r" + " " + single_path + " ""
        command += "-o" + " " + export_path + " "
        command += "--out-prefix" + " " + "assembled_contigs" + " "
        command += "-t" + " " + str(os.cpu_count()) + " "
        command += "-m" + " " + 0.8
        
        return [command]

        