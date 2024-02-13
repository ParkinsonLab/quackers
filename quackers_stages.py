import os
import re
import sys
import time
from weakref import ref
import quackers_paths as q_path
import quackers_commands as q_com
import MetaPro_utilities as mp_util


class q_stage:
    def __init__(self, out_path, path_obj):
        self.path_obj = path_obj
        self.command_obj = q_com.command_obj()
        self.job_control = mp_util.mp_util(out_path, self.path_obj.bypass_log_path)
        self.operating_mode = self.path_obj.operating_mode

    def trim_adapters(self, ref_path):
        
        ref_basename = os.path.basename(ref_path)
        ref_basename = ref_basename.split(".")[0]
        command = ""
        if(self.operating_mode == "single"):
            command = self.command_obj.clean_reads_single_command(ref_path)
        else:
            command = self.command_obj.clean_reads_command_paired(ref_path)

        script_path = os.path.join(self.path_obj.trim_dir, "trim_adapaters_" + ref_basename + ".sh")
        self.job_control.launch_and_create_v2(script_path, command)

    def host_filter(self, ref_path, path_obj, args_pack, dir_obj):
        #launch for each new ref path

        list_of_hosts = sorted(path_obj.config["hosts"].keys())
        for host_key in list_of_hosts:
            
            s_host_export_path = None
            p1_host_export_path = None
            p2_host_export_path = None
            host_ref_path = path_obj.hosts_path_dict[host_key]
            if(args_pack["op_mode"] == "single"):
                s_host_export_path = os.path.join(dir_obj.host_dir_data, host_key + "_free_s.fastq")
            elif(args_pack["op_mode"] == "paired"):
                p1_host_export_path = os.path.join(dir_obj.host_dir_data, host_key + "_free_p1.fastq")
                p2_host_export_path = os.path.join(dir_obj.host_dir_data, host_key + "_free_p2.fastq")


            ref_basename = os.path.basename(ref_path)
            ref_basename = ref_basename.split(".")[0]
            command = ""
            if(self.operating_mode == "single"):
                command = self.command_obj.clean_reads_single_command(ref_path, args_pack["s_path"], s_host_export_path)
            else:
                command = self.command_obj.clean_reads_command_paired(ref_path, args_pack["p1_path"], args_pack["p2_path"], p1_host_export_path, p2_host_export_path)

            script_path = os.path.join(self.path_obj.host_dir, "host_filter" + ref_basename + ".sh")
            self.job_control.launch_and_create_v2_with_mp_store(script_path, command)

        self.job_control.wait_for_mp_store()

    