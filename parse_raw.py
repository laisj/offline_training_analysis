# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 15:28:30 2015

@author: laisijia
"""

import os
import sys
import gzip
import collections

workdir = "/Users/laisijia/data/ctrpredict/in/"
outdir = "/Users/laisijia/data/ctrpredict/in/"
listfiles = os.listdir(workdir)
dims = ['display', 'click']
for filename in listfiles:
    for dim in dims:
        clickdict = collections.defaultdict(int)
        if not os.path.isdir(workdir+filename) and filename.startswith(dim + "-"):
            countdict = collections.defaultdict(int)
            print filename
            time_bucket = filename.split(".")[2]
            for line in gzip.open(workdir+filename, "rb"):
                linearr = line.split("|")
                countdict[(linearr[5], linearr[10])] += 1
                #print line
                #break
            
            with open(outdir + time_bucket + "bin_" + dim + ".tsv", "w") as fw:
                for k,v in countdict.items():
                    print "\t".join([time_bucket, k[0], k[1], str(v)])
                    fw.write("\t".join([time_bucket, k[0], k[1], str(v)]))
                    fw.write("\n")