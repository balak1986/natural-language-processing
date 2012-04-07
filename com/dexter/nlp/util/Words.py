
'''
Created on Apr 6, 2012

@author: Bala
'''



from nltk.corpus import stopwords, names, swadesh, wordnet
from string import punctuation
import nltk
import os
import en
import re

'''
Frequency of words in a file.
'''    
def get_frequncy_dist(dir_path):
    files = os.listdir(dir_path)
    file_handlers = []    
    for filename in files:
        if (filename.endswith('.srt')):
            file_handlers.append(open(dir_path + '\\' + filename, 'r'))

    '''get words'''
    all_words = [word.strip(punctuation).lower() for file_hd in file_handlers for line in file_hd for word in line.strip().split()]
    words_wt_freq = {}

    ''' get count and ignore stop words'''
    for word in all_words:
        if (word.isalpha()):
            words_wt_freq[word.lower()] = words_wt_freq.get(word.lower(), 0) + 1
    all_size = len(words_wt_freq.keys()) 
    print ('#words:' + str (all_size))
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
    print ('#words after lemmatized:' + str (lemmatized_size) + " diff: " + str (all_size - lemmatized_size))
    lexical_diversity_for_freq(lemmatized_words_wt_freq.values())
        
            
    #english_vocab = set(w.lower() for w in words.words())
    #usual_words = set(words_wt_freq.keys()).intersection(english_vocab)
    #print (set(words_wt_freq.keys()).difference(english_vocab))
    #print ('Total number of words after removing unusual:' + str (len(usual_words)))   
    
    '''wordnet has 155k'''                                 
    usual_words = []
    for word in  lemmatized_words_wt_freq.keys():
        if (len(wordnet.synsets(word)) != 0):
            usual_words.append(word)
    print ('#words after filtering unused words:' + str (len(usual_words)) + " diff: " + str (lemmatized_size - len(usual_words)))
    
    stopwords_en = stopwords.words('english')
    male_names = names.words('male.txt')
    female_names = names.words('female.txt')
    comparative = swadesh.words('en')
    ignore_list = [] ;
    ignore_list.extend(stopwords_en)
    ignore_list.extend(male_names)
    ignore_list.extend(female_names)
    ignore_list.extend(comparative)            
    filtered_words = [ word for word in usual_words if len(word) > 3 and word.lower() not in ignore_list]  
    print ('#words after filtering stop words:' + str (len(filtered_words)) + " diff: " + str (len(usual_words) - len(filtered_words)))
    
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
    print ('#words after filtering unwanted pos tags:' + str (len(tag_filtered_words_wt_freq.keys())) + " diff: " + str (len(filtered_words) - len(tag_filtered_words_wt_freq.keys())))
    lexical_diversity_for_freq(tag_filtered_words_wt_freq.values())


    basic_english_vocab = en.basic.words
    non_basic_words = set(tag_filtered_words_wt_freq.keys()).difference(basic_english_vocab)
    non_basic_words_wt_freq = {}
    for non_basic_word in non_basic_words:
        non_basic_words_wt_freq[non_basic_word] = tag_filtered_words_wt_freq[non_basic_word] 
    print ('#words after filtering basic words:' + str (len(non_basic_words_wt_freq.keys())) + " diff: " + str (len(tag_filtered_words_wt_freq.keys()) - len(non_basic_words_wt_freq.keys())))
    lexical_diversity_for_freq(non_basic_words_wt_freq.values())
    

    fh = open('C:\\Users\\Tyler\\workspace\\python\\etc\\iknew.csv', 'r')
    my_words = [word.lower() for line in fh for word in line.strip().split()]
    new_words = set(non_basic_words).difference(my_words)
    new_words_wt_freq = {}
    for new_word in new_words:
        new_words_wt_freq[new_word] = non_basic_words_wt_freq[new_word] 
    print ('#words after filtering my words:' + str (len(new_words_wt_freq.keys())) + " diff: " + str (len(non_basic_words_wt_freq.keys()) - len(new_words_wt_freq.keys())))
    lexical_diversity_for_freq(new_words_wt_freq.values())
        
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
        print ('Lexical Diversity : ' + str(round ((uniq_words / total_words) * 100, 2)))
        
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
