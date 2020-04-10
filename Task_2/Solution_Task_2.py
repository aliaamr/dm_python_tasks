#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Name : Alia Amr | Track : Data Management | Mail : aliaamr2110@gmail.com


# ### Problem Descripition 
# 
# In 2012, URL shortening service Bitly partnered with the US government website USA.gov to provide a feed of anonymous data gathered from users who shorten links ending with .gov or .mil.
# 
# The text file comes in JSON format and here are some keys and their description. They are only the most important ones for this task.

# In[2]:


import os
import sys
import json
import fnmatch
import pandas as pd
from os import listdir
from datetime import datetime
from os.path import isfile, join
from subprocess import PIPE, Popen
from pandas.io.json import json_normalize

# calcuate the execution time
startTime = datetime.now() 

args = sys.argv
args.pop(0)

UNIX_format = False
# check arguments
if '-u' in args :
    UNIX_format = True
    args.remove('-u')

directory_path = args[0]
if(directory_path[0] != '/'):
    directory_path = os.getcwd()+'/'+directory_path
    
checksums = {}
duplicated_files = []

file_list = [os.path.join(directory_path, f) for f in listdir(directory_path) if isfile(os.path.join(directory_path, f))]

for file_name in file_list:
    if fnmatch.fnmatch(file_name, '*.json'):
        with Popen(["md5sum", file_name], stdout=PIPE) as proc:
            checksum, _ = proc.stdout.read().split()
            print(checksum)
            if checksum in checksums.values():
                duplicated_files.append(file_name)
            checksums[file_name] = checksum
            
print("duplicated_files " , len(duplicated_files) )
print("------------------------")
print("checksums " , (checksums) )


# In[ ]:





# In[3]:


def open_json_file_fun (file_path):
    try:
        data_records = [json.loads(record) for record in open(file_path)]
    except IOError:
        print("[File Not Found.]")
    return data_records;


# In[4]:


from collections import defaultdict
def filtered_data_records_fun (data_records):
    # required columns
    columns = ['a', 'c', 'r', 'u', 't', 'hc', 'cy', 'll']
    filtered_data_records = []

    for record in data_records: 
        record = {k:v for (k,v) in record.items() if k in columns}

        # add missed columns with None as a default value
        # then check None values and delet them
        [record.setdefault(c, None) for c in columns]
        if (None not in record.values()): 
            filtered_data_records.append(record)
    return filtered_data_records


# In[5]:


# function to retutn the url in short format
def short_format_url(url):
  return (url.replace('http://', '').replace('https://', '')).split("/")[0]


# In[6]:


def clear_data_records_fun(filtered_data_records):

    clear_data_records = []
    for record in filtered_data_records: 
        # new empty record
        new_data_record = {}

        # browser and operating_system
        splitted_record = record['a'].split(" ")
        # browser
        new_data_record['web_browser'] = splitted_record[0]

        # operating_system
        if len(splitted_record) > 1:
            # remove special characters like '(|,|;|)'
            new_data_record['operating_system'] = "".join([character for character in splitted_record[1] if character.isalnum()])            
        else:
            continue # skip record if the operating_system is missed

        # merge 
        new_data_record = {**new_data_record,**record}
        del new_data_record['a']

        # update url
        new_data_record['r'] = short_format_url(record['u'])
        new_data_record['u'] = short_format_url(record['r'])

        # add longitude and latitude

        new_data_record['long'] = new_data_record['ll'][0]
        new_data_record['lat'] = new_data_record['ll'][1]
        del new_data_record['ll']

        # check UNIX_format option and update the dates  
        if (UNIX_format == False):
            if 't' in new_data_record:
                ts = int(new_data_record['hc'])
                new_data_record['hc'] = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                ts = int(new_data_record['t'])
                new_data_record['t'] = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        clear_data_records.append(new_data_record)
    return clear_data_records


# In[7]:


def reordered_data_records_fun (clear_data_records):
    # rearranging dictionary order
    desired_order_list = ['web_browser', 'operating_system', 'r', 'u', 'cy', 'long', 'lat', 'c', 't', 'hc']
    reordered_data_records = []

    for record in clear_data_records:
        reordered_data_records.append([record[key] for key in desired_order_list if key in record])
    return reordered_data_records;


# In[8]:


import csv
import errno
from pathlib import Path    

def save_file_fun (reordered_data_records, input_file_name):
    input_file_name = Path(input_file_name).name
    # remove the extension from the input file name
    input_file_name = ''.join(input_file_name.rsplit('.',1)[:-1])

    output_file_name = input_file_name + "_output.csv"
    output_base_dir = directory_path+"/transformed_files"
    output_file_path = os.path.join(output_base_dir, output_file_name)

    # check and create the directory for the output
    if not os.path.exists(os.path.dirname(output_file_path)):
        try:
            os.makedirs(os.path.dirname(output_file_path))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(output_file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(reordered_data_records)
    
    print('-'*40)
    print('File : ', output_file_name, ' generated successfully')
    print('-'*40)
    print('Output : ', len(reordered_data_records), 'row(s).')
    print('_'*40)


# In[9]:


for file in file_list :
    if file in duplicated_files:
        print ("Duplicated file : " , file, " checksum : ", checksums[file])
    else:
        r1 = open_json_file_fun (file)
        r2 = filtered_data_records_fun (r1)
        r3 = clear_data_records_fun (r2)
        r4 = reordered_data_records_fun (r3)
        r5 = save_file_fun (r4, file)
print('Task done successfully!')
print("Execution time : ", datetime.now() - startTime)

