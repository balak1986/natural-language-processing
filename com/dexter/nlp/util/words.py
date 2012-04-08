
'''
Created on Apr 6, 2012

com.dexter.nlp.util.Words - Finds frequency distribution of words after lemmatized, removing unusual, filtering stop words, filtering unwanted part-of-speech tags, and filtering basic words

@author: Bala
'''



from nltk.corpus import stopwords, names, swadesh, wordnet
from operator import itemgetter
from string import punctuation
import base
import en
import logging
import nltk
import os
import re

logger = logging.getLogger('util.Words')
base.init_logger(logger)

'''
Frequency of words in a file.
'''    
def get_frequncy_dist(dir_path):
    files = os.listdir(dir_path)
    out_file = open(dir_path + '\\wfd.csv', 'w')
    out_file.write ('Word, Type, Frequency \n')
    all_words = 0
    words_wt_freq = {}   
    '''get words'''
    for filename in files:
        if (filename.endswith('.srt')):
            file_handler = open(dir_path + '\\' + filename, 'r')
            for line in file_handler :
                for word in line.strip().split():
                    sword = word.strip(punctuation)
                    if (sword.isalpha()):
                        lword = sword.lower()
                        words_wt_freq[lword] = words_wt_freq.get(lword, 0) + 1
                        all_words += 1
            file_handler.close()
    logger.debug('# all words: ' + str (all_words - 1))
    logger.debug('# unique words: ' + str (len(words_wt_freq.keys())))
    lexical_diversity_for_freq(words_wt_freq.values())
    
    lemmatized_words_wt_freq = {}
    for word in words_wt_freq.keys():
        lemmatized_word = nltk.WordNetLemmatizer().lemmatize(word)
        if (word != lemmatized_word and lemmatized_word != None):
            lemmatized_words_wt_freq[lemmatized_word] = lemmatized_words_wt_freq.get(lemmatized_word, 0) + words_wt_freq.get(word)
            #print(lemmatized_word, word)
        else:
            lemmatized_words_wt_freq[word] = words_wt_freq.get(word)
    lemmatized_size = len(lemmatized_words_wt_freq.keys())            
    logger.debug ('# words after lemmatized: ' + str (lemmatized_size) + " diff: " + str (len(words_wt_freq.keys()) - lemmatized_size))
    lexical_diversity_for_freq(lemmatized_words_wt_freq.values())
    words_wt_freq = {} # Save memory


    '''wordnet has 155k'''                                 
    usual_words = []
    for word in  lemmatized_words_wt_freq.keys():
        if (len(wordnet.synsets(word)) != 0):
            usual_words.append(word)
        else:
            out_file.write(word + ',not in wordnet,' + str(lemmatized_words_wt_freq.get(word)) + '\n')
    logger.debug ('# words after filtering unused words: ' + str (len(usual_words)) + " diff: " + str (lemmatized_size - len(usual_words)))
    
    
    stopwords_en = stopwords.words('english')
    male_names = names.words('male.txt')
    female_names = names.words('female.txt')
    comparative = swadesh.words('en')
    ignore_list = [] ;
    ignore_list.extend(stopwords_en)
    ignore_list.extend(male_names)
    ignore_list.extend(female_names)
    ignore_list.extend(comparative)            
    filtered_words = []
    for word in usual_words:
        if len(word) > 3 and word not in ignore_list:
            filtered_words.append(word)   
        else:
            out_file.write(word + ',stop words,' + str(lemmatized_words_wt_freq.get(word)) + '\n')
    logger.debug ('# words after filtering stop words: ' + str (len(filtered_words)) + " diff: " + str (len(usual_words) - len(filtered_words)))
    usual_words = [] #save memory
    ignore_list = [] #save memory


    tag_filtered_words_wt_freq = {}
    words_wt_tags = nltk.pos_tag(filtered_words)
    for (word, tag) in words_wt_tags:
        if (tag not in ['EX', 'DET', 'CNJ', 'FW', 'MD', 'NP', 'NUM', 'PRO', 'P', 'TO', 'UH', 'WH', 'WP', 'NNP', 'MOD']):
            if(en.is_adverb(word)):
                tag_filtered_words_wt_freq[word] = lemmatized_words_wt_freq[word]  
                #print ('ADV,' + word)
            elif (en.is_adjective(word)):
                tag_filtered_words_wt_freq[word] = lemmatized_words_wt_freq[word]  
                #print ('ADJ,' + word)
            elif (en.is_verb(word)):
                tag_filtered_words_wt_freq[word] = lemmatized_words_wt_freq[word]  
                #print ('VB,' + word)
            elif (en.is_noun(word)):
                tag_filtered_words_wt_freq[word] = lemmatized_words_wt_freq[word]  
                #print ('N,' + word) 
            else:
                if (tag in ['VBZ', 'NNS']):
                    if word.endswith('s'):
                        new_word = word[:-1]
                        tag_filtered_words_wt_freq[new_word] = lemmatized_words_wt_freq[word] + tag_filtered_words_wt_freq.get(new_word, 0)
                        #print (word , new_word,tag)    
                elif (tag == 'VBG'):
                    new_word = en.verb.infinitive(word)
                    if new_word != None and word != new_word:
                        tag_filtered_words_wt_freq[new_word] = lemmatized_words_wt_freq[word] + tag_filtered_words_wt_freq.get(new_word, 0)
                elif (tag == 'JJS'):
                    if word.endswith('est'):
                        new_word = word[:-3]
                        tag_filtered_words_wt_freq[new_word] = lemmatized_words_wt_freq[word] + tag_filtered_words_wt_freq.get(new_word, 0)     
                else:
                    tag_filtered_words_wt_freq[word] = lemmatized_words_wt_freq[word]        
                    #print (word,tag)   
        else:
            out_file.write(word + ',unwanted pos,' + str(lemmatized_words_wt_freq.get(word)) + '\n')
    logger.debug ('# words after filtering unwanted pos:' + str (len(tag_filtered_words_wt_freq.keys())) + " diff: " + str (len(filtered_words) - len(tag_filtered_words_wt_freq.keys())))
    lexical_diversity_for_freq(tag_filtered_words_wt_freq.values())
    lemmatized_words_wt_freq = {} # save memory


    basic_english_vocab = en.basic.words
    non_basic_words = set(tag_filtered_words_wt_freq.keys()).difference(basic_english_vocab)
    non_basic_words_wt_freq = {}
    for non_basic_word in non_basic_words:
        non_basic_words_wt_freq[non_basic_word] = tag_filtered_words_wt_freq[non_basic_word] 
    words_in_both = set(tag_filtered_words_wt_freq.keys()).intersection(basic_english_vocab)
    for word in words_in_both:
        out_file.write(word + ',en.basic.words,' + str(tag_filtered_words_wt_freq.get(word)) + '\n')
    logger.debug ('# words after filtering basic words: ' + str (len(non_basic_words_wt_freq.keys())) + " diff: " + str (len(tag_filtered_words_wt_freq.keys()) - len(non_basic_words_wt_freq.keys())))
    lexical_diversity_for_freq(non_basic_words_wt_freq.values())
    tag_filtered_words_wt_freq = {} #save memory


    fh = open(os.path.join(base.app_root(), 'etc\\basic_words.csv'), 'r')
    my_words = [word.lower() for line in fh for word in line.strip().split()]
    fh.close()
    new_words = set(non_basic_words).difference(my_words)
    words_in_both = set(non_basic_words).intersection(my_words)
    for word in words_in_both:
        out_file.write(word + ',en.basic.words.mine,' + str(non_basic_words_wt_freq.get(word)) + '\n')    
    new_words_wt_freq = {}
    for new_word in new_words:
        new_words_wt_freq[new_word] = non_basic_words_wt_freq[new_word] 
    logger.debug ('# words after filtering my words: ' + str (len(new_words_wt_freq.keys())) + " diff: " + str (len(non_basic_words_wt_freq.keys()) - len(new_words_wt_freq.keys())))
    lexical_diversity_for_freq(new_words_wt_freq.values())
    
    sorted_words = sorted(new_words_wt_freq.items(), key=itemgetter(1, 0))
    for (word, frequency) in sorted_words:
        out_file.write (word + ',lexicon,' + str(frequency) + '\n')
    out_file.close()
    
    return new_words_wt_freq


def lexical_diversity(dir_path):
    total_words = 0
    uniq_words = 0.0
    for value in get_frequncy_dist(dir_path).values():
        total_words += value
        uniq_words += 1
    return round ((uniq_words / total_words) * 100, 2)

def lexical_diversity_for_freq(values):
    total_words = 0
    uniq_words = 0.0
    for value in values:
        total_words += value
        uniq_words += 1
    if total_words != 0 :
        logger.debug ('Lexical Diversity : ' + str(round ((uniq_words / total_words) * 100, 2)))
        
def long_words (words, size):
    long_words = [w for w in words if len(w) > size]
    return sorted(long_words)
    
    
if __name__ == '__main__':   
    dir_path = 'C:\Lab\ip\\dexter\distinct\\'
    #out_file = open(dir_path + 'words.csv', 'w')
    #out_file.write (' Word , Frequency \n')
    get_frequncy_dist(dir_path)
    #print ('Lexical Diversity : ' + str (lexical_diversity (dir_path)))
    #  print ('Long Words' + str (long_words(get_frequncy_dist(dir_path), 10)))
    # for (word, frequency) in get_frequncy_dist(dir_path).items():
    #     out_file.write (word + ',' + str(frequency) + '\n')
