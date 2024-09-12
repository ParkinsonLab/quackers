#---------------------------------------------------------------
#Reconcile all various host/adapter filters to one coherent file <or 2 in paired>
#reconciliation based on match score.
#export the reads for the next stage

#note: redo this part. just walk through each SAM, and have a running top-hit.  no need for double-for-loop.
#note2: too slow. use multithreading to finish this faster
#note3: reconstituted to be just-for-contigs.  Just for 1 file.

#note4: multithreading didn't do anything.  removed checks on scorefile.  Assuming there will only be 1 hit.
#multi-hit check was holdover from host-filter days.

import os
import sys
from datetime import datetime as dt
import multiprocessing as mp

import time


def import_fastq(fastq_file):

    walk_count = 0
    with open(fastq_file, "r") as fastq_in:
        line_count = 0
        read_dict = dict()
        read_ID = ""
        seq = ""
        true_ID = ""
        qual = ""
        inner_dict = dict()
        for line in fastq_in:
            
            if(line_count ==  0):
                read_ID = line.strip("\n")
                true_ID = read_ID
                read_ID = read_ID.split("\t")[0]
                read_ID = read_ID.split(" ")[0]
                read_ID = read_ID.strip("@")
                line_count += 1
                
            elif(line_count ==  1):
                seq = line.strip("\n")
                line_count += 1
            elif(line_count == 2):
                line_count += 1
            
            elif(line_count == 3):
               
                qual = line.strip("\n")
                inner_dict["seq"] = seq
                inner_dict["qual"] = qual
                inner_dict["ID"] = true_ID
                read_dict[read_ID] = inner_dict

                line_count = 0
    
    print("line count:", line_count)
    print("dict keys:", len(read_dict.keys()))
    return read_dict




def sort_samfiles(sam_path):
    #opening one score_bt2/bwa.out
    #going low-tech here. assuming there's only valid entries.  
  
    sam_hits_set = set()
    
    #print("sam score path:", sam_path)
    with open(sam_path, "r") as sam_in:
        for line in sam_in:
            line_split = line.split("\t")
            read_ID = line_split[0]
            sam_hits_set.add(read_ID)

    return sam_hits_set


def sort_reads(raw_read_keys, sam_hits_keys, clean_reads_dict, work_ID):
    
    #clean_reads = list()
    if(work_ID == "0_1"):
        print("[" + work_ID + "] raw keys:", len(raw_read_keys))
        print("[" + work_ID + "] sam hits keys:", len(sam_hits_keys))
    count = 0
    start_time = time.time()
    full_count = len(raw_read_keys)
    for read in raw_read_keys:
        if(work_ID == "0_1"):

            
            count += 1
            now_time = time.time()
            time_diff = int(now_time - start_time)
            #print(dt.today(), "[" + work_ID + "] on:", count)
            if(count == 10):
                
                print(dt.today(), "[" + work_ID + "] first 10 done:", time_diff)
            elif(count == 100):
                print(dt.today(), "[" + work_ID + "] first 100 done:", time_diff)
            elif(count == 1000):
                print(dt.today(), "[" + work_ID + "] first 1000 done", time_diff)

            elif(count == int(full_count / 10)):
                print(dt.today(), "[" + work_ID + "] 10% done", time_diff)

            elif(count == int(full_count / 4)):
                print(dt.today(), "[" + work_ID + "] 25% done", time_diff)

            elif(count == int(full_count /2)):
                print(dt.today(), "[" + work_ID + "] 50% done", time_diff)

            elif(count == int(full_count * 0.75)):
                print(dt.today(), "[" + work_ID + "] 75% done", time_diff)


        hit_reads = set(sorted(sam_hits_keys))
        if(not read in hit_reads):
            continue
        else:
            clean_reads_dict[read] = 1
            #print(dt.today(), "work ID:", work_ID, read, clean_reads_dict[read])
            
    print("[" + str(work_ID) + "] clean reads dict: " + str(len(clean_reads_dict.keys())))
    #return clean_reads

def export_reads(final_out_file, raw_read_dict, keys_to_write):
    with open(final_out_file, "w") as s_out:
        for read_ID in keys_to_write:
            selected_read = raw_read_dict[read_ID]
            seq = selected_read["seq"]
            qual = selected_read["qual"]
            true_ID = selected_read["ID"]
            out_line = true_ID + "\n" + seq + "\n" + "+" + "\n" + qual + "\n"

            print("Writing:", true_ID)
            s_out.write(out_line)






if __name__ == "__main__":
    print(dt.today(), "RUNNING contig reconcile mod")
    sam_score_file = sys.argv[1]
    export_dir = sys.argv[2]
    raw_s_read = sys.argv[3]
    raw_p1_read = sys.argv[4]
    raw_p2_read = sys.argv[5]
    
    is_single = False
    is_paired = False
    s_raw_dict = ""
    p1_raw_dict = ""
    p2_raw_dict = ""
    final_s_reads = os.path.join(export_dir, "singles.fastq")
    final_p1_reads  = os.path.join(export_dir, "remaining_forward.fastq")
    final_p2_reads  = os.path.join(export_dir, "remaining_reverse.fastq")

    print("export destination:", final_p1_reads)

    
    print(dt.today(), "starting samfile sort+merge")
    sam_hits_set = sort_samfiles(sam_score_file)

 
    

    if(os.path.exists(raw_s_read)):
        is_single = True
        print(dt.today(), "sample is SINGLE-ended")
    else:
        is_paired = True
        print(dt.today(), "sample is PAIRED-ended")

    if(os.path.exists(raw_p1_read) and (os.path.exists(raw_p2_read))):
        is_paired = True
    if(is_paired and is_single):
        sys.exit("Exit at reconciliation.  Single and paired-reads detected")
    print(dt.today(), "starting host sort")        
    #for read_ID in sam_hits_dict:

    

    cpu_count = mp.cpu_count() * 2
    cpu_count = cpu_count - 1
    manager = mp.Manager()
    


    mp_jobs = []


    print(dt.today(), "starting clean read extract")
    if(is_single):
        s_raw_dict = import_fastq(raw_s_read)
        s_keys_set = set(s_raw_dict.keys())
        s_clean_keys = list(s_keys_set - sam_hits_set)


        print(dt.today(), "S extraction jobs done. Starting export")
        s_export_process = mp.Process(target = export_reads, args = (final_s_reads, s_raw_dict, s_clean_keys))
        s_export_process.start()
        print(dt.today(), "waiting for export S process to finish")
        s_export_process.join()
        print(dt.today(), "DONE!")
        #----------------------------------------

        
    elif(is_paired):
        p1_raw_dict = import_fastq(raw_p1_read)
        p2_raw_dict = import_fastq(raw_p2_read)

        
        p1_keys_set = set(p1_raw_dict.keys())
        p2_keys_set = set(p2_raw_dict.keys())

        p1_clean_keys = list(p1_keys_set - sam_hits_set)
        p2_clean_keys = list(p2_keys_set - sam_hits_set)


        print("clean keys to write[P1]:", len(p1_clean_keys))
        print("clean keys to write[P2]:", len(p2_clean_keys))


        p1_export_process = mp.Process(target = export_reads, args = (final_p1_reads, p1_raw_dict, p1_clean_keys))
        p2_export_process = mp.Process(target = export_reads, args = (final_p2_reads, p2_raw_dict, p2_clean_keys))

        p1_export_process.start()
        p2_export_process.start()
        mp_jobs.append(p1_export_process)
        mp_jobs.append(p2_export_process)
        print(dt.today(), "export processes launched. waiting")
        for item in mp_jobs:
            item.join()
        mp_jobs.clear()
        print(dt.today(), "done!")
        


        


