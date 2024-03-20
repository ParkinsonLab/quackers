import os
import re
import sys
import time
from datetime import datetime as dt
import quackers_commands as q_com
import MetaPro_utilities as mp_util


class q_stage:
    def __init__(self, out_path, path_obj, dir_obj, args_pack):
        self.path_obj = path_obj
        self.command_obj = q_com.command_obj(path_obj)
        self.job_control = mp_util.mp_util(out_path)#, self.path_obj.bypass_log_name)
        self.operating_mode = self.path_obj.operating_mode
        self.dir_obj = dir_obj
        self.op_mode = args_pack["op_mode"]

        self.start_s_path   = args_pack["s_path"]
        self.start_f_path  = args_pack["p1_path"]
        self.start_r_path  = args_pack["p2_path"]


    def host_filter(self):
        #launch for each new ref path

        list_of_hosts = sorted(self.path_obj.config["hosts"].keys())

        if(len(list_of_hosts) == 0):
            #skip host-cleaning. move data 
            print(dt.today(), "no hosts used: bypassing host filter")
            if(self.op_mode == "single"):
                self.dir_obj.host_final_s = self.start_s_path
            elif(self.op_mode == "paired"):
                self.dir_obj.host_final_f = self.start_f_path
                self.dir_obj.host_final_r = self.start_r_path

        else:
            for host_key in list_of_hosts:
                
                s_host_export_path = None
                p_host_export_path = None
                marker_exists = False
                
                host_ref_path = self.path_obj.hosts_path_dict[host_key]
                
                if(self.op_mode == "single"):
                    s_host_export_path = os.path.join(self.dir_obj.host_dir_data, host_key + "_s.sam")
                    print("using s host export path:", s_host_export_path)
                    if(os.path.exists(s_host_export_path)):
                        marker_exists = True
                elif(self.op_mode == "paired"):
                    p_host_export_path = os.path.join(self.dir_obj.host_dir_data, host_key + "_p.sam")
                    print("using p host export path:", p_host_export_path)
                    if(os.path.exists(p_host_export_path)):
                        marker_exists = True
                

                if(marker_exists):
                    print("skipping Host filter")
                else:
                    ref_basename = os.path.basename(host_ref_path)
                    ref_basename = ref_basename.split(".")[0]
                    command = ""
                    if(self.operating_mode == "single"):
                        #command = self.command_obj.clean_reads_command_s(host_ref_path, self.start_s_path, s_host_export_path)
                        #command = self.command_obj.clean_reads_command_s(host_ref_path, self.start_s_path, s_host_export_path)
                        command = self.command_obj.clean_reads_bwa_command_s(host_ref_path, self.start_s_path, s_host_export_path)
                    else:
                        #command = self.command_obj.clean_reads_command_p(host_ref_path, p_host_export_path, self.start_f_path, self.start_r_path)
                        command = self.command_obj.clean_reads_bwa_command_p(host_ref_path, p_host_export_path, self.start_f_path, self.start_r_path)

                    script_path = os.path.join(self.dir_obj.host_dir_top, "host_filter_" + ref_basename + ".sh")
                    self.job_control.launch_and_create_v2_with_mp_store(script_path, command)

            self.job_control.wait_for_mp_store()


            command = self.command_obj.clean_reads_reconcile(self.dir_obj.host_dir_data, self.dir_obj.host_dir_end, self.start_s_path, self.start_f_path, self.start_r_path)
            script_path = os.path.join(self.dir_obj.host_dir_top, "reconcile.sh")
            self.job_control.launch_and_create_v2_with_mp_store(script_path, command)
            self.job_control.wait_for_mp_store()

        



    def megahit_assembly(self):
        command = ""
        script_path = ""

        
        if(not os.path.exists(self.dir_obj.assembly_mkr)):
            if(self.op_mode == "single"):
                print("[S] using data from:", self.dir_obj.host_final_s)
                command = self.command_obj.megahit_command_s(self.dir_obj.host_final_s, self.dir_obj.assembly_dir_data, self.dir_obj.assembly_dir_temp)
                script_path = os.path.join(self.dir_obj.assembly_dir_top, "assemble_s.sh")

            elif(self.op_mode == "paired"):
                print("[F] using data from:", self.dir_obj.host_final_f)
                print("[R] using data from:", self.dir_obj.host_final_r)
                command = self.command_obj.megahit_command_p(self.dir_obj.host_final_f, self.dir_obj.host_final_r, self.dir_obj.assembly_dir_data, self.dir_obj.assembly_dir_temp)
                script_path = os.path.join(self.dir_obj.assembly_dir_top, "assemble_p.sh")

            self.job_control.launch_and_create_v2_with_mp_store(script_path, command)
            self.job_control.wait_for_mp_store()
        else:
            print(dt.today(), "skipping: megahit")

        print("path to contigs:", self.dir_obj.assembly_contigs)
        if(self.job_control.check_file_integrity(self.dir_obj.assembly_contigs)):
            if(not os.path.exists(self.dir_obj.assembly_pp_mkr)):
                #post-process.  Index the contigs. rescan the reads to extract consumed reads.
                #print(dt.today(), "todo: finish megahit PP")
                #command = self.command_obj.bowtie2_index_command(self.dir_obj.assembly_contigs)
                command = self.command_obj.bwa_index_ref(self.dir_obj.assembly_contigs)
                script_path = os.path.join(self.dir_obj.assembly_dir_top, "index_contigs.sh")
                self.job_control.launch_and_create_v2_with_mp_store(script_path, command)

                self.job_control.wait_for_mp_store()

                if(self.op_mode == "paired"):
                    command = self.command_obj.clean_reads_bwa_command_p(self.dir_obj.assembly_contigs, self.dir_obj.assembly_bwa, self.dir_obj.host_final_f, self.dir_obj.host_final_r)
                    

                elif(self.op_mode == "single"):
                    command = self.command_obj.clean_reads_bwa_command_s(self.dir_obj.assembly_contigs, self.dir_obj.assembly_bwa, self.dir_obj.host_final_s)
                script_path = os.path.join(self.dir_obj.assembly_dir_top, "clean_reads.sh")
                self.job_control.launch_and_create_v2_with_mp_store(script_path, command)
                self.job_control.wait_for_mp_store()

        if(not os.path.exists(self.dir_obj.assembly_reconcile_mkr)):

            command = self.command_obj.clean_reads_reconcile(self.dir_obj.assembly_dir_data, self.dir_obj.assembly_dir_end, self.dir_obj.host_final_s, self.dir_obj.host_final_f, self.dir_obj.host_final_r )
            script_path = os.path.join(self.dir_obj.assembly_dir_top, "contig_reconcile.sh")
            self.job_control.launch_and_create_v2_with_mp_store(script_path, command)
            self.job_control.wait_for_mp_store()

        else:
            print(dt.today(), "WARNING: NO contigs formed from this sample")

    #def concoct_binning(self):
        #requires adjusting headers and junk before sending off to concoct.
        #code just removes the dangling portion of the ID in each contig



