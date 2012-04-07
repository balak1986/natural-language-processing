'''
Created on Apr 6, 2012

@author: Tyler
'''

# super-complicated, time-consuming code

import re,os,zipfile
import base 
from urllib2 import urlopen, URLError, HTTPError
z = zipfile.ZipFile('C:\\Lab\\temp\\download-38-1-en.html.zip')
for f in z.namelist():
    if f.endswith('/'):
        os.makedirs(f)
z.extractall('C:\\Lab\\temp\\')

