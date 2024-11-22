import os
import sys
sys.path.append("/home/billy/alt_storage")
from datetime import datetime as dt
import quackers_paths as qp

if __name__ == "__main__":
    output_dir = sys.argv[1]

    config_path = sys.argv[2]
    args_pack = dict()
    args_pack["out"] = output_dir


    path_obj = qp.path_obj(output_dir, config_path)
    dir_obj = qp.dir_structure(args_pack, path_obj)

    list_of_hosts = sorted(path_obj.config["hosts"].keys())
    list_of_mkrs = list()

    for host_key in list_of_hosts:
                                
        host_ref_path = path_obj.hosts_path_dict[host_key]
        ref_basename = os.path.basename(host_ref_path)
        ref_basename = ref_basename.split(".")[0]

        host_bwa_marker_path = os.path.join(dir_obj.host_dir_top, ref_basename + "_host_bwa_mkr")
        list_of_mkrs.append(host_bwa_marker_path)
    for host_key in list_of_hosts:
        host_ref_path = path_obj.hosts_path_dict[host_key]
        ref_basename = os.path.basename(host_ref_path)
        ref_basename = ref_basename.split(".")[0]
        sam_sift_marker_path = os.path.join(dir_obj.host_dir_top, ref_basename + "_sift_mkr")    
        list_of_mkrs.append(sam_sift_marker_path)
    
    if(dir_obj.check_mkr_host(list_of_mkrs)):
        print(dt.today(), "everything's fine")