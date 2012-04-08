'''
Created on Apr 7, 2012

@author: Bala
'''

import os
import logging

def app_root():
    return os.path.dirname(__file__)

def temp_dir():
    return 'C:\\Lab\\temp\\'

def init_logger(logger):
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('C:\\Lab\\log\\files.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter) 
    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)    
