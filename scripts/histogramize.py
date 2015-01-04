# This script accepts a list of sorted timestamps, one each line.
# Outputs a list of histogram intervals in csv format (separated by commas).

import codecs
import json
import sys
import time
from pprint import pprint

# start_timestamp = 1413910800000 # wto, 21 paz 2014, 19:00:00 CEST
# end_timestamp =   1413928800000 # sro, 22 paz 2014, 00:00:00 CEST
start_timestamp = 1413997200000 # sro, 22 paz 2014, 19:00:00 CEST
end_timestamp =   1414015200000 # czw, 23 paz 2014, 00:00:00 CEST
interval_width  = 120000

def main():    
    if len(sys.argv) < 2:
        print "Usage: python histogramize.py <file_name>"
        return

    with codecs.open(sys.argv[1], 'r', 'utf-8') as f:
        current_lower_bound = start_timestamp
        current_count = 0
        for line in f:
            timestamp_int = int(line)
            if timestamp_int > current_lower_bound:
                if timestamp_int > current_lower_bound + interval_width:
                    # print "%d: %d\n" % (current_lower_bound, current_count)
                    timestr = time.strftime("%H:%M", time.localtime(int(current_lower_bound / 1000)))
                    with open("histogram.csv", "a") as myfile:
                        myfile.write("%s,%d\n" % (timestr, current_count))
                    current_count = 1
                    current_lower_bound += interval_width
                else:
                    current_count += 1
            if timestamp_int > end_timestamp:
                return




if __name__ == '__main__':
    main()