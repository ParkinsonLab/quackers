import os
import sys
import time
from datetime import datetime as dt
import MetaPro_utilities as mpu
import quackers_paths as q_path
import quackers_commands as q_comm
if __name__ == "__main__":

    output_dir = sys.argv[1]

    mp_util = mpu.init()
    
    print("test import check")