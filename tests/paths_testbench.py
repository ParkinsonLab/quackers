import os
import sys
import time
from datetime import datetime as dt
sys.path.insert(1, '../')
import quackers_path as q_path


if __name__ == "__main__":
    out_path = sys.argv[1]
    config_path = sys.argv[2]
    path_obj = q_path(out_path, config_path)