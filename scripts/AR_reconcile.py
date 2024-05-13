#cleans up stray reads that lost its pair from the AR process
#puts everything else to a separate singletons file

import os
import sys
import time
from datetime import datetime as dt

def import_fastq(fastq_file):

    walk_count = 0
    with open(fastq_file, "r") as fastq_in:
        line_count = 0
        read_dict = dict()
        read_ID = ""
        seq = ""
        qual = ""
        inner_dict = dict()
        for line in fastq_in:
            
            if(line_count % 4 ==  0):
                read_ID = line.strip("\n")
                read_ID = read_ID.split("\t")[0]
                read_ID = read_ID.split(" ")[0]
                read_ID = read_ID.strip("@")
                walk_count += 1
                
            elif(line_count % 4 ==  1):
                seq = line.strip("\n")
                
            
            elif(line_count % 4 == 3):
               
                qual = line.strip("\n")
                inner_dict["seq"] = seq
                inner_dict["qual"] = qual
                read_dict[read_ID] = inner_dict

            line_count += 1
    
    print("walk:", walk_count)
    print("line count:", line_count)
    print("dict keys:", len(read_dict.keys()))
    return read_dict

def export_reads(out_path, keys_to_write, reads_dict):

    with open(out_path, "w") as out_file:
        first_line = True
        for item in keys_to_write:
            if(first_line):
                first_line = False
                
            else:
                out_line = "\n"
                out_file.write(out_line)
            out_line = "@" + item + "\n"
            line_choice = reads_dict[item]
            out_line += line_choice["seq"] + "\n"
            out_line += "+\n"
            out_line += line_choice["qual"]
            out_file.write(out_line)

if __name__ == "__main__":
    f_file_in = sys.argv[1]
    r_file_in = sys.argv[2]
    s0_file_out = sys.argv[3]
    s1_file_out = sys.argv[4]
    f_file_out = sys.argv[5]
    r_file_out = sys.argv[6]
    print(dt.today(), "begin import")
    f_reads_dict = import_fastq(f_file_in)
    r_reads_dict = import_fastq(r_file_in)
    print(dt.today(), "finished import")
    f_keys = set(f_reads_dict.keys())
    r_keys = set(r_reads_dict.keys())

    common_keys = f_keys.intersection(r_keys)
    f_only_keys = f_keys - r_keys
    r_only_keys = r_keys - f_keys
    print("common keys:", len(common_keys))
    print("f-only:", len(f_only_keys))
    print("r-only:", len(r_only_keys))


    print(dt.today(), "exporting")
    export_reads(f_file_out, common_keys, f_reads_dict)
    export_reads(r_file_out, common_keys, r_reads_dict)
    export_reads(s0_file_out, f_only_keys, f_reads_dict)
    export_reads(s1_file_out, r_only_keys, r_reads_dict)
    
    print(dt.today(), "finished export")




    
