#!/usr/local/bin/python3

# This is our main script. It utilizes our custom made functions and some other general libraries.
# The program first takes a path for our dataset.
# It will then iterate through all the .xml.zip files and unzip them with our extract_zipfiles function.
# Then it will take the path with all the unzipped data, and iterate through all files.
# For each file, it will create an iterparse object, that will be processed by create_txtfile.
# It will redo this process until all the files in our dataset have been processed.

# Import general libraries
from alive_progress import alive_bar
import xml.etree.cElementTree as ET
import os

# Import our custom made functions
from scraper import create_txtfile
from unzip import extract_zipfiles

debug = 1 # Set to 1 for debugging
 
if debug : 
    source_path = './Data/Tests'
else :
    source_path = './Data/Lake'
 
data_path = extract_zipfiles(source_path, debug)
 
with alive_bar(len(os.listdir(data_path)) - 1 , force_tty = True) as bar:
    print(f"Loading datasets...")
    
    for filename in os.listdir(data_path):
        
        # Avoid certain hidden files that show up on Mac OS
        if filename == "__MACOSX" or filename == ".DS_Store" : 
            continue
        
        print(f"The file named '{filename}' is being processed.")
        fullname = os.path.join(data_path, filename)
        
        # Events tell whether it's an opening or closing tag
        context = ET.iterparse(fullname, events = ('start', 'end'))
        context = iter(context)
        
        create_txtfile(context, filename, debug)
        
        print(f"The file named '{filename}' has successfully been processed.")
        bar()