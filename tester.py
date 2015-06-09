# -*- coding: utf-8 -*-
import os
import re
import urllib2
import json
import pickle

# srcDir = os.path.dirname(os.path.abspath(__file__))
# print("Change workind directory to:", srcDir)
# os.chdir( srcDir )

def download_url(url):
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
	       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
	       'Accept-Encoding': 'none',
	       'Accept-Language': 'en-US,en;q=0.8',
	       'Connection': 'keep-alive'}

	req = urllib2.Request(url, headers=hdr)
	
	try:
	    page = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
	    print ("fail to get page")
	    print e.fp.read()

	return page.read();


def exract_episodes(content, re_episode, re_url, re_number):
 	matches = re.finditer(re_episode, content, re.DOTALL)

 	episodes = list()

 	for match in matches:
 		episode = dict()
 		episode_area = match.groups('')[0]
 		url_match = re.search(re_url, episode_area)
 		if url_match: 
			episode['url'] = url_match.groups('')[0]; 
 		
 		number_match = re.search(re_number, episode_area)
		if number_match:
			episode['number'] = number_match.groups('')[0]

 		episodes.append(episode)

 	return episodes;

site_config = json.load(open("skai-gr.json","r"))

print "Start scraping at %s" % (site_config['domain'], )

seiries = site_config['seiries'];

print "Found %i seiries in %s " % ( len(seiries), site_config['domain'])

for s in seiries:
	print "now checking: %s" % ( s['title'], )
	url = s['url']
	print "Downloading \"%s\"" % (url, )
	page = download_url(url)
	print "Extract episodes"

	episodes = exract_episodes(page, s['episode'], s['episode-url'], s['episode-number'])

	print "Found:"
	for episode in episodes:
		print "%s - %s in %s" % (s['title'], episode['number'], episode['url'])