'''
Created on Apr 6, 2012

@author: Bala
'''
import os,zipfile
import re
import shutil
import logging
import base

logger = logging.getLogger('util.Files')
base.init_logger(logger)
        
def get_distinct_files(dir_path, key_pattern):
    files = os.listdir(dir_path)
    keyed_files = {}
    for filename in files:
        if (filename.endswith('.srt')):
            result = re.search(key_pattern, filename)
            if result != None:
                keyed_files [result.group(0)] = filename 
    logger.debug('Keys for finding distinct files : ' + str(sorted(keyed_files.keys())))                
    return keyed_files.values()

def copy_files (src, dest, file_names):
    ''' Setup destination folder '''
    if (os.path.isdir(dest)):
        shutil.rmtree(dest)
        logger.debug('Removed ' + dest) 
    os.makedirs(dest)
    logger.debug('Created ' + dest) 
    src_files = os.listdir(src)
    for file_name in src_files:
        if file_name in file_names:
            full_file_name = os.path.join(src, file_name)
            if (os.path.isfile(full_file_name)):
                shutil.copy(full_file_name, dest)

def unzip_files(dir_path):
    logger.debug('Unzipping files from ' + dir_path)
    files = os.listdir(dir_path)
    for filename in files:
        if (filename.endswith('.zip')):
            try:
                z = zipfile.ZipFile(os.path.join(dir_path, filename))
                for f in z.namelist():
                    if f.endswith('/'):
                        os.makedirs(f)
                z.extractall(dir_path + '\\unzipped')
                logger.debug('Extracted : ' + filename)
            except zipfile.BadZipfile:
                logger.debug('BadZipfile : ' + filename)
    return dir_path + '\\unzipped'

def main():
    logger.info('Started')   
    key_pattern = '(\w+ \w* - [0-9]x[0-9]{2})'   
    fp = unzip_files('C:\\Lab\\temp') 
    distinct_files = get_distinct_files (fp, key_pattern)   
    dest_dir_path = fp + '\\distinct'  
    copy_files(fp, dest_dir_path, distinct_files)
    logger.info('Finished')

if __name__ == '__main__':  
    main()