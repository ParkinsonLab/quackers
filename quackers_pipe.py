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


def run_pipe(path_obj, args_pack):
    #-------------------------------------------------------
    #step 1: hosts
    dir_obj = q_path.dir_structure(args_pack, path_obj)
    mp_obj = mpu.mp_util(args_pack["out"])#, path_obj.bypass_log)
    stage_obj = q_stage.q_stage(args_pack["out"], path_obj, dir_obj, args_pack)

    stage_obj.check_host_bypass()

    if(mp_obj.check_bypass_log(path_obj.bypass_log, path_obj.host_dir)):
        
        stage_obj.host_filter()
    
    if(mp_obj.check_bypass_log(path_obj.bypass_log, path_obj.assembly_dir)):
        stage_obj.megahit_assembly()

    if(mp_obj.check_bypass_log(path_obj.bypass_log, path_obj.cct_bin_dir)):
        stage_obj.concoct_binning()    

    if(mp_obj.check_bypass_log(path_obj.bypass_log, path_obj.mwrap_bin_dir)):
        stage_obj.metawrap_binning()
    print(dt.today(), "DONE!")

def parse_inputs():
    parser = ArgumentParser(description="Quackers: a metagenomic processing pipeline <and maybe more>. 2024. "
                            "Version 1.0.0")
    parser.add_argument("-o", "-O", "--output_dir", "--Output_dir", type=str, help="Path to the output directory")
    parser.add_argument("-c", "-C", "--config", type=str, help="Path to a configuration file")
    parser.add_argument("-1", "--forward", "--f", type=str, help="Used only for paired-end reads: Path to the forward-end data")
    parser.add_argument("-2", "--reverse", "--r", type=str, help="Used only for paired-end reads: Path to the reverse-end data")
    parser.add_argument("-s", "-S", "--single", type=str, help="For single-ended reads:, Path to the single-end data")

    args = parser.parse_args()

    output_dir  = args.output_dir
    config_path = args.config
    p1_path     = args.forward
    p2_path     = args.reverse
    s_path      = args.single

    operating_mode = ""

    if(p1_path is None):
        if(s_path is None):
            sys.exit("ERROR: expecting at least 1 set of input data: single OR forward + reverse")
        else:
            
            if(not p2_path is None):
                sys.exit("ERROR: Single and Reverse-end can't both be present. typo?")
            else:
                operating_mode = "single"
                print("Pipe running in SINGLE mode")

    if(s_path is None):
        if(not p1_path is None):
            if(not p2_path is None):
                operating_mode = "paired"
                print("Pipe running in PAIRED mode")
            else:
                sys.exit("ERROR: Reverse-end data missing")
    else:
        if(not p1_path is None):
            if(not p2_path is None):
                sys.exit("ERROR: all 3 fields filled. single OR forward + reverse. Not all 3")

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
    args_pack["op_mode"] = operating_mode

    if(args_pack["s_path"] is None):
        args_pack["s_path"] = "empty"
    if(args_pack["p1_path"] is None):
        args_pack["p1_path"] = "empty"
    if(args_pack["p2_path"] is None):
        args_pack["p2_path"] = "empty"

    print("S:", args_pack["s_path"])
    print("P1:", args_pack["p1_path"])
    print("P2:", args_pack["p2_path"])
    

    return args_pack



if __name__ == "__main__":
    args_pack = parse_inputs()
    for item in args_pack:
        print("[" + item + "]", args_pack[item])

    
    path_obj = q_path.path_obj(args_pack["out"], args_pack["config"])
    path_obj.operating_mode = args_pack["op_mode"]
    
    #mp_util = mpu.mp_util(args_pack["out"], path_obj.bypass_log_name)

    run_pipe(path_obj, args_pack)



