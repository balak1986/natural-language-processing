'''
Created on Apr 7, 2012

com.dexter.nlp.util.TVSubtitles - Downloads TV Show subtitles from tvsubtitles.com

@author: Bala
'''

from lxml.html import fromstring
from time import strftime, gmtime, time, sleep
from urllib2 import urlopen
import base
import logging
import os
import re

logger = logging.getLogger('util.Files')
base.init_logger(logger)
                 
HOME_URL = 'http://www.tvsubtitles.net'
dl_links = {}

def cache_dl_links():
    logger.debug( "caching... ")
    startTime = time()
    # Get document from URL 
    url_handler = urlopen(HOME_URL + '/tvshows.html')
    tvsubtitles_html = url_handler.read()
    url_handler.close()
    my_search_tree = fromstring(tvsubtitles_html)
    
    # Collect hyper links
    href_links = []
    for a in my_search_tree.cssselect('td a'):
        href_links.append(a.get('href'))
    
    # Map HyperLink with its meaning
    href_link_map = {}
    expr = ".//tr/*/a[@href = $name]/b"
    for href_link in href_links:    
        for element in my_search_tree.xpath(expr, name=href_link):
            href_link_map[str(element.text).lstrip().lower().replace("'", "")] = href_link
    
    # Make it as downloadale links
    for (name, link) in href_link_map.items():
        match = re.match('tvshow-(\d+)-(\d+).html', link)
        show = match.group(1)
        seasons = match.group(2)
        dl_links[name] = [HOME_URL + '/download-' + show + '-' + str(n) + '-en.html' for n in range(1, int(seasons))]
    logger.debug("caching is done TT: " + strftime('%M:%S', gmtime(time() - startTime)))

def download_tvsubtitles(show_name, des_dir):
    startTime = time()
    urls = dl_links.get(show_name.lstrip().lower())
    if urls == None:
        logger.debug( "Found no subtitles for " + show_name)
        return
    for  url in urls: 
        logger.debug("downloading subtitles for " + show_name + " : " + os.path.basename(url))
        f = urlopen(url)
        # Open our local file for writing
        with open(des_dir + os.path.basename(url) + '.zip', "wb") as local_file:
            local_file.write(f.read())
    logger.debug("downloading for " + show_name + " is done TT: " + strftime('%M:%S', gmtime(time() - startTime)))
    
if __name__ == '__main__':
    startTime = time()
    cache_dl_links()
    fav_shows = ['The O.C.', '24', 'Alias', 'Band of Brothers', 'Breaking Bad', 'Chuck', 'Dexter', 'Doctor Who', 'FlashForward', 'Friends', 'Fringe', 'Heroes', 'House M.D.', 'How I Met Your Mother', 'Lost', 'Modern Family', 'Persons Unknown', 'Prison Break', 'Six Feet Under', 'Supernatural', 'Seinfeld', 'Scrubs', 'The Big Bang Theory', 'The IT Crowd', 'The Killing', 'The Mentalist', 'The Office', 'Two and a Half Men', 'Justified', 'Jericho', 'One Tree Hill', 'Workaholics', 'Suits', 'True Blood', 'Mad Men', 'Game of Thrones','Batman','Family Guy','Futurama','South Park','The Simpsons','Tom and Jerry','Scooby Doo, Where Are You!','The Mask','Avatar: The Last Airbender','The Adventures of Tintin']
    all_shows = ['The O.C.','24','Alias','Band of Brothers','Breaking Bad','Chuck','Dexter','Doctor Who','FlashForward','Friends','Fringe','Heroes','House M.D.','How I Met Your Mother','Lost','Modern Family','Persons Unknown','Prison Break','Six Feet Under','Supernatural','Seinfeld','Scrubs','The Big Bang Theory','The IT Crowd','The Killing','The Mentalist','The Office','Justified','Jericho','One Tree Hill','Workaholics','Suits','True Blood','Mad Men','Game of Thrones','Aliens in America','Arrested Development','Spartacus: Vengeance','Boardwalk Empire','Bored to Death','Californication','Castle','Childrens Hospital','Cougar Town','Deadwood','Defying Gravity','Dollhouse','Eastbound & Down','Episodes','Firefly','Freaks and Geeks','Gossip Girl','Harpers Island','Its Always Sunny in Philadelphia','John Adams','Lie to Me','Lights Out','Louie','Luther','Misfits','Monty Pythons Flying Circus','Parks and Recreation','Peep Show','The Pillars of the Earth','Spartacus: Gods of the Arena','Rome','Rubicon','Shameless','Skins','Sons of Anarchy','Spaced','Tell Me You Love Me','The Big C','The Kill Point','The Lost Room','The Pacific','The Shadow Line','The Walking Dead','Twin Peaks','Two and a Half Men','United States of Tara','Weeds','Wilfred']
    for show in sorted(dl_links.keys()):
        if re.match('^[U-Z]', show.upper()):
            download_tvsubtitles(show, base.temp_dir())
            sleep(5) 
    logger.debug("Total time taken: " + strftime('%H:%M:%S', gmtime(time() - startTime)))
    
