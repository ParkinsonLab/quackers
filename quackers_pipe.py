import os
import sys
import time
from datetime import datetime as dt
import MetaPro_utilities as mpu
import quackers_paths as q_path
import quackers_commands as q_comm
if __name__ == "__main__":

    output_dir  = sys.argv[1]
    config_path = sys.argv[2]
    mp_util = mpu.init()
    path_obj = q_path.path_obj(output_dir, config_path)
    print("test import check")