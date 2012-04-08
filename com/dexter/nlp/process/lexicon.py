'''
Created on Apr 6, 2012

com.dexter.nlp.script.Lexicon - Generate lexicons from distinct subtitle (srt) files from the given dir after lemmatized, removing unusual, filtering stop words, filtering unwanted part-of-speech tags, and filtering basic words

@author: Bala
'''
from com.dexter.nlp.util.files import get_distinct_files, copy_files, \
    unzip_files
from com.dexter.nlp.util.words import get_frequncy_dist
from operator import itemgetter
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

out_file = open(dest_dir_path + '\\lexicon.csv', 'w')
out_file.write ('Word, Frequency \n')
words = get_frequncy_dist(dest_dir_path)
sorted_words = sorted(words.items(), key=itemgetter(1, 0))
for (word, frequency) in sorted_words:
    out_file.write (word + ',' + str(frequency) + '\n')

logger.debug( "Finished. Total time: " + strftime('%H:%M:%S', gmtime(time() - startTime)))

