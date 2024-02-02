import os
import sys
import time
from datetime import datetime as dt
import MetaPro_utilities as mpu
import quackers_paths as q_path

class quackers_command:
    
    def __init__(self):
        self.path_obj = q_path.quackers_path()

    def megahit_command(self):
        command = self.path_obj.megahit_path + " "
        command += 
