import os
import sys
import time
from datetime import datetime as dt
from wsgiref.util import shift_path_info
import MetaPro_utilities as mpu
import quackers_paths as q_path
import quackers_commands as q_comm
import quackers_stages as q_stage
from argparse import ArgumentParser


def run_pipe(path_obj, stage_obj, output_dir, mp_util):
    #-------------------------------------------------------
    #step 1: hosts
    list_of_hosts = sorted(path_obj.config["hosts"].keys())
    
    for host_entry in list_of_hosts:
        print(host_entry)
        #stage_obj.host_filter(host_entry)



def parse_inputs():
    parser = ArgumentParser(description="Quackers: a metagenomic processing pipeline <and maybe more>. 2024. "
                            "Version 1.0.0")
    parser.add_argument("-o", "-O", "--output_dir", "--Output_dir", type=str, help="Path to the output directory")
    parser.add_argument("-c", "-C", "--config", type=str, help="Path to a configuration file")
    parser.add_argument("-1", "--forward", "--f", type=str, help="Used only for paired-end reads: Path to the forward-end data")
    parser.add_argument("-2", "--reverse", "--r", type=str, help="Used only for paired-end reads: Path to the reverse-end data")
    parser.add_argument("-s", "--single", type=str, help="For single-ended reads:, Path to the single-end data")

    args = parser.parse_args()

    output_dir  = args.output_dir
    config_path = args.config
    p1_path     = args.forward
    p2_path     = args.reverse
    s_path      = args.single

    if(p1_path is None):
        if(s_path is None):
            sys.exit("expecting at least 1 set of input data: single OR forward + reverse")
    if(not s_path is None):
        if(not p1_path is None):
            sys.exit("expecting either single-end OR both paired-end data. not both")
    if(config_path is None):
        sys.exit("expecting a config file. Use the < -c/C > or < --config > flag" )
    if(output_dir is None):
        sys.exit("expecting an output directory. Use the < -o/O > or < --output_dir > flag")

    if not(os.path.exists(output_dir)):
        os.mkdir(output_dir)

    args_pack = dict()
    args_pack["out"] = output_dir
    args_pack["config"] = config_path
    args_pack["p1_path"] = p1_path
    args_pack["p2_path"] = p2_path
    args_pack["s_path"] = s_path

    return args_pack



if __name__ == "__main__":
    args_pack = parse_inputs()
    for item in args_pack:
        print("[" + item + "]", args_pack[item])

    
    path_obj = q_path.path_obj(args_pack["out"], args_pack["config"])
    stage_obj = q_stage.q_stage(args_pack["out"], path_obj)
    mp_util = mpu.mp_util(args_pack["out"], path_obj.bypass_log_name)

    run_pipe(path_obj, stage_obj, args_pack["out"], mp_util)



