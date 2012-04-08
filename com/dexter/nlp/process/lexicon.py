'''
Created on Apr 6, 2012

com.dexter.nlp.script.Lexicon - Generate lexicons from distinct subtitle (srt) files from the given dir after lemmatized, removing unusual, filtering stop words, filtering unwanted part-of-speech tags, and filtering basic words

@author: Bala
'''
from com.dexter.nlp.util.files import get_distinct_files, copy_files, \
    unzip_files
from com.dexter.nlp.util.words import get_frequncy_dist
from time import strftime, gmtime, time
import base
import logging


logger = logging.getLogger('script.Lexicon')
base.init_logger(logger)

startTime = time()

logger.info('Started')   
key_pattern = '(\w+ \w* - [0-9]x[0-9]{2})'   
fp = unzip_files('C:\\Lab\\temp') 
distinct_files = get_distinct_files (fp, key_pattern)   
dest_dir_path = fp + '\\distinct'  
copy_files(fp, dest_dir_path, distinct_files)
dest_dir_path = 'C:\\Lab\\out\\nlp\\all_tv_subtitles'
#dest_dir_path = 'C:\\Lab\\ip\\test\\distinct'
words = get_frequncy_dist(dest_dir_path)
logger.debug("Finished. Total time: " + strftime('%H:%M:%S', gmtime(time() - startTime)))

