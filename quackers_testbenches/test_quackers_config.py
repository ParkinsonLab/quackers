import os
import sys
import time
sys.path.append("/home/billy/alt_storage")
from datetime import datetime as dt
import quackers_paths as q_p

if __name__ == "__main__":
    output_folder_path = sys.argv[1]
    if(os.path.exists(output_folder_path)):
        print("path exists")
    else:
        os.makedirs(output_folder_path)
    config_path = sys.argv[2]
    path_obj = q_p.path_obj(output_folder_path, config_path)