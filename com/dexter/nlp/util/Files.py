'''
Created on Apr 6, 2012

@author: Bala
'''
import os
import re
import shutil
    
def get_distinct_files(dir_path, key_pattern):
    files = os.listdir(dir_path)
    keyed_files = {}
    for file in files:
        if (file.endswith('.srt')):
            result = re.search(key_pattern, file)
            if result != None:
                keyed_files [result.group(0)] = file 
    return keyed_files.values()

def copy_files (src, dest, file_names):
    ''' Setup destination folder '''
    if (os.path.isdir(dest)):
        shutil.rmtree(dest)
    os.makedirs(dest)
    src_files = os.listdir(src)
    for file_name in src_files:
        if file_name in file_names:
            full_file_name = os.path.join(src, file_name)
            if (os.path.isfile(full_file_name)):
                shutil.copy(full_file_name, dest)

if __name__ == '__main__':        
    src_dir_path = 'C:\Lab\dexter\\'     
    key_pattern = '([0-9]x[0-9]{2})'   
    distinct_files = get_distinct_files (src_dir_path, key_pattern)   
    
    dest_dir_path = src_dir_path + 'distinct'  
    copy_files(src_dir_path, dest_dir_path, distinct_files)
