#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 10:24:37 2017

@author: jonathan
"""
from __future__ import print_function
from collections import defaultdict
import os
from shutil import copyfile
import csv

buffer_path = '/media/jonathan/D3C7-4043/sdsDatabase/buffer/'
sds_path = '/media/jonathan/D3C7-4043/sdsDatabase/'
from datetime import datetime
from glob import glob 
def pdf_spread(filename, buffer_path, sds_path):
    buffer_path = buffer_path
    d = defaultdict(list)
    failed = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            #makes a directory path and checks for its existence, creates it if
            #it does not exist
            directory = sds_path+ '{}'.format(row[0])
            if not os.path.exists(directory):
                os.makedirs(directory)
            #makes a dictionary with Room:Chemical_CAS list
            if not row[1] in d[row[0]]:
                d[row[0]].append('{}_{}'.format(row[1],row[2]))
    for room in d.keys():
        #Starts setting room paths
        room_path = sds_path+'{}/'.format(room)
        #Tries to copy file from buffer, if fails will log the failed Room/Chemical
        #for manual lookup
        for chemical in d[room]:
           
            if glob(buffer_path+'*'+chemical.split('_')[-1]):
                if not glob(room_path+'*'+chemical.split('_')[1]):
                    print (chemical)
                    replaced_room_path=(room_path + (chemical).replace('*','')\
                               .replace('/', '').replace('<','').replace('>','')+)
                    print (room_path)
                    copyfile(glob(buffer_path+'*'+chemical.split('_')[1])[0],replaced_room_path)
            else:
                failed.append((room,chemical))
                
    with open('failed_lookups.txt','w') as e:
        for chemical in failed:
            e.write((chemical[0]+','+chemical[1]+'\n'))

    
pdf_spread('inventory.csv', buffer_path, sds_path)

