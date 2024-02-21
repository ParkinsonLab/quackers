import os
import sys
import re

def get_match_score(cigar_segment):
    CIGAR = re.split("([MIDNSHPX=])", cigar_segment) # Split CIGAR string into list, placing
    CIGAR = CIGAR[:-1]                      #lop off the empty char artifact from the split
    position_count = 0                      #position counter, because the CIGAR string is split into alternating segments of <length><Label>, 
    length = 0
    matched = 0
    segment_length = 0
    for item in CIGAR:
        if((position_count %2) == 0):       #every even position (starting from 0) is going to be a length
            segment_length = int(item)
        elif((position_count %2) == 1):     #every odd position is going to be a label
            length += segment_length
            if(item == "M"):
                matched += segment_length
        position_count += 1
    if(length == 0):
        return 0
        
    match_score = 100 * (matched / length)
    
    return match_score



if __name__ == "__main__":
    sam_file = sys.argv[1]
    export_file = sys.argv[2]
    with open(export_file, "w") as out_file:
        with open(sam_file, "r") as sam_in:
            for line in sam_in:
                if(line.startswith("@")):
                    continue
                else:
                    line_split = line.split("\t")
                    read_ID = line_split[0]
                    read_quality = line_split[5]
                    match_score = get_match_score(read_quality)
                    if(match_score  != 0):
                        #print("quality[", read_quality, "]:", line)
                        out_line = read_ID + "\t" + match_score + "\n"
                        out_file.write(line)
