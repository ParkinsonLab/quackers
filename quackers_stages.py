import os
import sys
import time
import quackers_paths as q_path
import quackers_commands as q_com
import MetaPro_utilities as mp_util


class q_stage:
    def __init__(self, out_path, config_path):
        self.path_obj = q_path.path_obj(out_path, config_path)
        self.command_obj = q_com.command_obj()
        self.job_control = mp_util.mp_util(out_path, self.path_obj.bypass_log_path)
        self.operating_mode = self.path_obj.operating_mode

    def trim_adapters(self, ref_path):
        command = ""
        if(self.operating_mode == "single"):
            command = self.command_obj.clean_reads_single_command(ref_path)
        else:
            command = self.command_obj.clean_reads_command_paired(ref_path)

        script_path = os.path.join(self.path_obj.trim_dir, "launch_job.sh")
        self.job_control.launch_and_create_v2(script_path, command)
        




    def host_filter(self):
