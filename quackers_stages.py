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
        self.dir_obj = dir_obj
        self.command_obj = q_com.command_obj(path_obj, dir_obj)
        self.job_control = mp_util.mp_util(out_path)#, self.path_obj.bypass_log_name)
        self.operating_mode = self.path_obj.operating_mode
        
        self.op_mode = args_pack["op_mode"]

        self.start_s_path   = args_pack["s_path"]
        self.start_f_path  = args_pack["p1_path"]
        self.start_r_path  = args_pack["p2_path"]

        self.hosts_bypassed = False

    def check_host_bypass(self):
        #checks if there are hosts. if not, trigger the bypass
        list_of_hosts = sorted(self.path_obj.config["hosts"].keys())

        if(len(list_of_hosts) == 0):
            #skip host-cleaning. move data
            self.hosts_bypassed = True 
            print(dt.today(), "no hosts used: bypassing host filter")
            if(self.op_mode == "single"):
                self.dir_obj.host_final_s = self.start_s_path
            elif(self.op_mode == "paired"):
                self.dir_obj.host_final_f = self.start_f_path
                self.dir_obj.host_final_r = self.start_r_path


    def host_filter(self):
        #launch for each new ref path

        list_of_hosts = sorted(self.path_obj.config["hosts"].keys())

        if(len(list_of_hosts) == 0):
            #skip host-cleaning. move data
            self.hosts_bypassed = True 
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
                        command = self.command_obj.clean_reads_bwa_command_s(host_ref_path, self.start_s_path, s_host_export_path, self.host_pp_)
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

        self.job_control.write_to_bypass_log(self.path_obj.bypass_log, self.path_obj.host_dir)

        



    def megahit_assembly(self):
        command = ""
        script_path = ""

        
        if(not os.path.exists(self.dir_obj.assembly_mkr)):
            if(self.op_mode == "single"):
                print("[S] using data from:", self.dir_obj.host_final_s)
                command = self.command_obj.megahit_command_s(self.dir_obj.host_final_s, self.dir_obj.assembly_dir_data, self.dir_obj.assembly_dir_temp)
                self.job_control.launch_and_create_v2_with_mp_store(self.dir_obj.assembly_megahit_s_job, command)

            elif(self.op_mode == "paired"):
                print("[F] using data from:", self.dir_obj.host_final_f)
                print("[R] using data from:", self.dir_obj.host_final_r)
                command = self.command_obj.megahit_command_p(self.dir_obj.host_final_f, self.dir_obj.host_final_r, self.dir_obj.assembly_dir_data, self.dir_obj.assembly_dir_temp)
                self.job_control.launch_and_create_v2_with_mp_store(self.dir_obj.assembly_megahit_p_job, command)
            
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
                self.job_control.launch_and_create_v2_with_mp_store(self.dir_obj.assembly_bwa_idx_job, command)
                self.job_control.wait_for_mp_store()

                if(self.op_mode == "paired"):
                    command = self.command_obj.clean_reads_bwa_command_p(self.dir_obj.assembly_contigs, self.dir_obj.assembly_sam, self.dir_obj.host_final_f, self.dir_obj.host_final_r, self.dir_obj.assembly_pp_mkr)
                    

                elif(self.op_mode == "single"):
                    command = self.command_obj.clean_reads_bwa_command_s(self.dir_obj.assembly_contigs, self.dir_obj.assembly_sam, self.dir_obj.host_final_s, self.dir_obj.assembly_pp_mkr)
                self.job_control.launch_and_create_v2_with_mp_store(self.dir_obj.assembly_bwa_job, command)
                self.job_control.wait_for_mp_store()

        if(not os.path.exists(self.dir_obj.assembly_sam_convert_mkr)):
            command = self.command_obj.sam_convert_command(self.dir_obj.assembly_sam, self.dir_obj.assembly_bam, self.dir_obj.assembly_s_bam)
            self.job_control.launch_and_create_v2_with_mp_store(self.dir_obj.assembly_sam_convert_job, command)

        if(not os.path.exists(self.dir_obj.assembly_reconcile_mkr)):

            command = self.command_obj.clean_reads_reconcile(self.dir_obj.assembly_dir_data, self.dir_obj.assembly_dir_end, self.dir_obj.host_final_s, self.dir_obj.host_final_f, self.dir_obj.host_final_r )
            script_path = os.path.join(self.dir_obj.assembly_dir_top, "contig_reconcile.sh")
            self.job_control.launch_and_create_v2_with_mp_store(script_path, command)
            self.job_control.wait_for_mp_store()

        else:
            print(dt.today(), "skipping assembly reconcile")
            #print(dt.today(), "WARNING: NO contigs formed from this sample")
        self.job_control.write_to_bypass_log(self.path_obj.bypass_log, self.path_obj.assembly_dir)
        

    def concoct_binning(self):
        #print(dt.today(), "temp holder")
        #requires adjusting headers and junk before sending off to concoct.
        #code just removes the dangling portion of the ID in each contig
        if(not os.path.exists(self.dir_obj.cct_prep_mkr)):
            command = self.command_obj.concoct_prep_command(self.dir_obj.cct_prep_mkr)
            self.job_control.launch_and_create_v2_with_mp_store(self.dir_obj.cct_prep_job_path, command)
            self.job_control.wait_for_mp_store()

        if(not os.path.exists(self.dir_obj.cct_mkr)):
            command = self.command_obj.concoct_command(self.dir_obj.cct_mkr)
            self.job_control.launch_and_create_v2_with_mp_store(self.dir_obj.cct_job_path, command)
            self.job_control.wait_for_mp_store()

        if(not os.path.exists(self.dir_obj.cct_checkm_mkr)):
            print(dt.today(), "running checkm")
            command = self.command_obj.checkm_command(self.dir_obj.cct_checkm_mkr)
            self.job_control.launch_and_create_v2_with_mp_store(self.dir_obj.cct_checkm_job_path, command)
            self.job_control.wait_for_mp_store()
        else:
            print(dt.today(), "bypassing checkm")
            print(self.dir_obj.cct_checkm_mkr)
        self.job_control.write_to_bypass_log(self.path_obj.bypass_log, self.path_obj.cct_bin_dir)
            
    def metawrap_binning(self):
        print(dt.today(), "running metawrap-binning")
        command = self.command_obj.metawrap_bin_command(self.op_mode, self.hosts_bypassed, self.dir_obj.mwrap_mkr)
        self.job_control.launch_and_create_v2_with_mp_store(self.dir_obj.mwrap_job, command)
        self.job_control.wait_for_mp_store()
        self.job_control.write_to_bypass_log(self.path_obj.bypass_log, self.path_obj.mwrap_bin_dir)

    def metawrap_bin_refine(self):
        print("running metawrap bin_refinement")
        command = self.command_obj.metawrap_bin_refinement_command(self.dir_obj.mwrap_bin_r_mkr)
        self.job_control.launch_and_create_v2_with_mp_store(self.dir_obj.mwrap_bin_r_job, command)
        self.job_control.wait_for_mp_store()
        self.job_control.write_to_bypass_log(self.path_obj.bypass_log, self.path_obj.mwrap_bin_r_dir)

    def gtdbtk_classify(self):
        print("running GTDB-tk classify")
        command = self.command_obj.gtdbtk_command(self.dir_obj.gtdbtk_mkr)
        self.job_control.launch_and_create_v2_with_mp_store(self.dir_obj.gtdbtk_job, command)
        #self.job_control.wait_for_mp_store()
        #self.job_control.write_to_bypass_log(self.path_obj.bypass_log, self.path_obj.gtdbtk_class_dir)

    def metawrap_quant(self):
        print(dt.today(), "running metawrap quant bin")
        command = self.command_obj.metawrap_quantify_command(self.dir_obj.mwrap_quant_mkr)
        self.job_control.launch_and_create_v2_with_mp_store(self.dir_obj.mwrap_quant_job, command)