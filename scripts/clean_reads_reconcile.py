#---------------------------------------------------------------
#Reconcile all various host/adapter filters to one coherent file <or 2 in paired>
#reconciliation based on match score.
#export the reads for the next stage

#note: redo this part. just walk through each SAM, and have a running top-hit.  no need for double-for-loop.
#note2: too slow. use multithreading to finish this faster

#weak, 
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
    return read_dict, read_dict.keys()

def export_hosts(sam_hits_dict, export_dir):
    #sort all reads by host
    hosts_dict = dict()
    for read_ID in sam_hits_dict:
        entry = sam_hits_dict[read_ID]
        samfile = entry.split("|")[0]
        if(samfile in hosts_dict):
            hosts_dict[samfile].append(read_ID)
        else:
            hosts_dict[samfile] = [read_ID]

    for host in hosts_dict:
        host_reads = hosts_dict[host]
        host_basename = host.split(".sam")[0]
        host_export_file = os.path.join(export_dir, host_basename + "_reads.txt")
        
        with open(host_export_file, "w") as host_out:
            for read in host_reads:
                out_line = read + "\n"
                host_out.write(out_line)

def sort_samfiles(sam_dir):
    list_of_samfiles = os.listdir(sam_dir)
    unique_hosts = set()
    sam_hits_dict = dict()
    list_of_reads = list()
    for samfile in list_of_samfiles:
        
        
        if(samfile.endswith("score_bwa.out")):
            unique_hosts.add(samfile)
            sam_path = os.path.join(sam_dir, samfile)
            print("sam path:", sam_path)
            with open(sam_path, "r") as sam_in:
                
                for line in sam_in:
                    line_split = line.strip("\n").split("\t")
                    read_ID = line_split[0]
                    #print("whole line:", line)
                    
                    list_of_reads.append(read_ID)
                    score = float(line_split[1])
                    
                    #note: paired-hits will get a double-chance to act.
                    if(read_ID in sam_hits_dict):
                        old_hit = sam_hits_dict[read_ID]
                        #print("old hit:", old_hit)
                        old_score = float(old_hit.split("|")[1])
                        if(old_score < score):
                            sam_hits_dict[read_ID] = samfile + "|" + str(score)
                    else:
                        sam_hits_dict[read_ID] = samfile + "|" + str(score)

    return sam_hits_dict, unique_hosts


def sort_reads(raw_read_keys, sam_hits_keys, hits_reads_dict, work_ID):
    #ranks hits.
    #clean_reads = list()
    print("[" + work_ID + "] raw keys:", len(raw_read_keys))
    print("[" + work_ID + "] sam hits keys:", len(sam_hits_keys))
    for read in raw_read_keys:
        hit_reads = set(sorted(sam_hits_keys))
        old_size = len(hit_reads)
        hit_reads.add(read)
        new_size = len(hit_reads)
        if(old_size < new_size):
            continue
        else:
            hits_reads_dict[read] = 1
            #print(dt.today(), "work ID:", work_ID, read, clean_reads_dict[read])
            
    print("[" + str(work_ID) + "] hits reads dict: " + str(len(hits_reads_dict.keys())))
    #return clean_reads

def export_reads(final_out_file, raw_read_dict, keys_to_write):
    with open(final_out_file, "w") as s_out:
        for read_ID in keys_to_write:
            selected_read = raw_read_dict[read_ID]
            seq = selected_read["seq"]
            qual = selected_read["qual"]
            out_line = "@" + read_ID + "\n" + seq + "\n" + "+" + "\n" + qual + "\n"
            s_out.write(out_line)


def sort_host_hits(sam_hits_dict):
    #separate the reads into samfiles
    host_bin_dict = dict()
    for read_id in sam_hits_dict.keys():
        sam_hit = sam_hits_dict[read_id].split("|")[0]
        if(sam_hit in host_bin_dict):
            host_bin_dict[sam_hit].append(read_id)
        else:
            host_bin_dict[sam_hit] = [read_id]
    return host_bin_dict

def export_host_list(export_dir, host_bins_dict, host_name):
    #export all host lists
    #for host_sam in host_bins_dict.keys():
    host_sam = host_bins_dict[host_name]
    short_host_name = host_name.split(".")[0]
    #print("using:", host_name)
    host_bin_file = os.path.join(export_dir, short_host_name + "_hits.txt")
    with open(host_bin_file, "w") as out_file:
        for read in host_bins_dict[host_name]:
            out_line = read + "\n"
            out_file.write(out_line)




if __name__ == "__main__":
    sam_dir = sys.argv[1]
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
    final_p1_reads  = os.path.join(export_dir, "pair_1.fastq")
    final_p2_reads  = os.path.join(export_dir, "pair_2.fastq")
    host_p1_reads = os.path.join(export_dir, "host_p1.fastq")
    host_p2_reads = os.path.join(export_dir, "host_p2.fastq")
    host_s_reads = os.path.join(export_dir, "host_s.fastq")

    
    print(dt.today(), "starting samfile sort+merge")
    sam_hits_dict, unique_hosts = sort_samfiles(sam_dir)

    
    print(dt.today(), "exporting host lists")
    export_hosts(sam_hits_dict, export_dir)
    

    if(os.path.exists(raw_s_read)):
        is_single = True

    if(os.path.exists(raw_p1_read) and (os.path.exists(raw_p2_read))):
        is_paired = True
    if(is_paired and is_single):
        sys.exit("Exit at reconciliation.  Single and paired-reads detected")
    print(dt.today(), "starting host sort")        
    #for read_ID in sam_hits_dict:

    

    cpu_count = mp.cpu_count()
    cpu_count = cpu_count - 1
    manager = mp.Manager()
    sam_hits_keys = sam_hits_dict.keys()

    count = 0
    for test_sam_key in sam_hits_keys:
        print("sam hits keys:", test_sam_key)
        count += 1
        if(count > 10):
            break



    mp_jobs = []
    #--------------------------------------------
    #deal with host lists
    host_bin_dict = sort_host_hits(sam_hits_dict)
    print(dt.today(), "starting host export")
    for unique_host in unique_hosts:
        host_export_process = mp.Process(target = export_host_list, args = (export_dir, host_bin_dict, unique_host))
        host_export_process.start()
        mp_jobs.append(host_export_process)
    print(dt.today(), "all host export jobs launched. waiting")
    for item in mp_jobs:
        item.join()
    mp_jobs.clear()

    print(dt.today(), "starting clean read extract")
    if(is_single):
        s_raw_dict, s_raw_keys = import_fastq(raw_s_read)

        cpu_count = int(cpu_count)
        split_size = int(len(p1_raw_dict.keys())/cpu_count)
        s_keys = list(sorted(s_raw_dict.keys()))
        hits_s_reads_dict = manager.dict()
        for i_cpu in range(0, cpu_count):
            start_index = i_cpu * split_size
            end_index = ((i_cpu + 1) * split_size)-1
            s_selection = s_keys[start_index:end_index]
            if(i_cpu >= cpu_count - 1):
                s_selection = s_keys[start_index:]

            s_process = mp.Process(target = sort_reads, args = (s_selection, sam_hits_keys, hits_s_reads_dict))
            s_process.start()
            mp_jobs.append(s_process)
        print(dt.today(), "S jobs launched. waiting")
        for item in mp_jobs:
            item.join()
        mp_jobs.clear()
        print(dt.today(), "S extraction jobs done. Starting export")
        s_export_process = mp.Process(target = export_reads, args = (final_s_reads, s_raw_dict, hits_s_reads_dict.keys()))
        s_export_process.start()
        print(dt.today(), "waiting for export S process to finish")
        s_export_process.join()
        print(dt.today(), "DONE!")
        #----------------------------------------

        
    elif(is_paired):
        p1_raw_dict, p1_raw_keys = import_fastq(raw_p1_read)
        p2_raw_dict, p2_raw_keys = import_fastq(raw_p2_read)

        

        cpu_count = int(cpu_count / 2)
        split_size = int(len(p1_raw_dict.keys())/cpu_count)

        print("cpu count:", cpu_count)
        print("full reads:", len(p1_raw_dict.keys()))
        p1_keys = list(sorted(p1_raw_dict.keys()))
        p2_keys = list(sorted(p2_raw_dict.keys()))
        
        
        print("split size:", split_size)
        
        hits_p1_reads_dict = manager.dict()
        hits_p2_reads_dict = manager.dict()
        


        for i_cpu in range(0, cpu_count):
            start_index = i_cpu * split_size
            end_index = ((i_cpu + 1) * split_size)-1
            p1_selection = p1_keys[start_index:end_index]
            p2_selection = p2_keys[start_index:end_index]

            start_selection = p1_selection[0]
            end_selection = p1_selection[-1]
            start_main = p1_keys[start_index]
            end_main = p1_keys[end_index-1]


            if(i_cpu >= cpu_count -1):
                end_index = len(p1_keys)
                p1_selection = p1_keys[start_index:end_index]
                p2_selection = p2_keys[start_index:end_index]
                #print("LAST bin")
                #print("start:", start_index, "end:", end_index)
                end_main = p1_keys[end_index-1]
                end_selection = p1_selection[-1]

            work_ID = str(i_cpu) + "_1"
            work_ID2 = str(i_cpu) + "_2"
            p1_process = mp.Process(target = sort_reads, args = (p1_selection, sam_hits_keys, hits_p1_reads_dict, work_ID))
            p2_process = mp.Process(target = sort_reads, args = (p2_selection, sam_hits_keys, hits_p2_reads_dict, work_ID2))

            p1_process.start()
            p2_process.start()
            mp_jobs.append(p1_process)
            mp_jobs.append(p2_process)

        print(dt.today(), "P extraction jobs launched. waiting")
        for item in mp_jobs:
            item.join()
        mp_jobs.clear()
    
        print(dt.today(), "paired extraction jobs done! Starting export")
        
        final_hits_p1_reads_dict = dict(hits_p1_reads_dict)
        final_hits_p2_reads_dict = dict(hits_p2_reads_dict)

        p1_keys_to_export = p1_raw_keys - hits_p1_reads_dict.keys()
        p2_keys_to_export = p2_raw_keys - hits_p2_reads_dict.keys()

        count = 0
        for key in p1_keys_to_export:
            count += 1
            print("keys to write:", key)
            if(count > 10):
                break

        p1_export_process = mp.Process(target = export_reads, args = (final_p1_reads, p1_raw_dict, p1_keys_to_export))
        p2_export_process = mp.Process(target = export_reads, args = (final_p2_reads, p2_raw_dict, p2_keys_to_export))

        p1_export_process.start()
        p2_export_process.start()
        mp_jobs.append(p1_export_process)
        mp_jobs.append(p2_export_process)
        print(dt.today(), "export processes launched. waiting")
        for item in mp_jobs:
            item.join()
        mp_jobs.clear()
        print(dt.today(), "done!")
        


        


