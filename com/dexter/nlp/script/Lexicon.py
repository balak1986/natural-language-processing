'''
Created on Apr 6, 2012

@author: Bala
'''
from com.dexter.nlp.util.Files import get_distinct_files, copy_files
from com.dexter.nlp.util.Words import get_frequncy_dist
from operator import itemgetter
from time import strftime, gmtime, time


startTime = time()

src_dir_path = 'C:\\Lab\\ip\\dexter\\'     
key_pattern = '([0-9]x[0-9]{2})'   
distinct_files = get_distinct_files (src_dir_path, key_pattern)   

dest_dir_path = src_dir_path + 'distinct'  
copy_files(src_dir_path, dest_dir_path, distinct_files)

out_file = open(dest_dir_path + '\\lexicon.csv', 'w')
out_file.write (' Word , Frequency \n')
words = get_frequncy_dist(dest_dir_path)
sorted_words = sorted(words.items(), key=itemgetter(1, 0))
for (word, frequency) in sorted_words:
    out_file.write (word + ',' + str(frequency) + '\n')

elapsed = time() - startTime
print "Finished. Total time: " + strftime('%H:%M:%S', gmtime(elapsed))
    