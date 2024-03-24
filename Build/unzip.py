# The data package is a directory of directories containing zip files.
# This function will open a given data source path and unzip the datasets from each folder.
# Then it will transfer them to a new temporary folder called "Data_Unzipped" and output the coressponding path.

import zipfile
import os

def extract_zipfiles (source_path, debug) :
    
    if debug : 
        unzip_path = './Testing/DataUnzipped'
    else : 
        unzip_path = './Output/DataUnzipped'
    
    # Check if the output folder has been created
    isExist = os.path.exists(unzip_path)

    # Creates a an output folder if needed
    if not isExist: 
        os.makedirs(unzip_path)
    
    # Iterates through the data source directory and unzips wanted files
    for folder in os.listdir(source_path):

        # Avoid certain hidden files that show up on Mac OS
        if folder == ".DS_Store" : 
            continue

        for item in os.listdir(f'{source_path}/{folder}') :
            if item.endswith('.xml.zip'):
                with zipfile.ZipFile(f'{source_path}/{folder}/{item}', 'r') as zip_ref:
                    zip_ref.extractall(unzip_path)
    
    return unzip_path