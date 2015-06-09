# -*- coding: utf-8 -*-
import os
import re
import urllib2
import sendgrid
import pickle
import conf #for this to work rename the example.conf.py to conf.py

srcDir = os.path.dirname(os.path.abspath(__file__))
print("Change workind directory to:", srcDir)
os.chdir( srcDir )


sendgrid_password = conf.sendgrid_password
mail = conf.mail
address = conf.address
sendgrid_username = conf.sendgrid_username
site= conf.url
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

req = urllib2.Request(site, headers=hdr)

try:
    page = urllib2.urlopen(req)
except urllib2.HTTPError, e:
    
    print e.fp.read()

content = page.read()

match = re.finditer(u"<p>\s*<time>\s*([0-3][0-9]\.(0[0-9]|1(0|1|2))\.20\d{0,2})\s*</time>", content)
print match
dates = ""
try:
	datesFile = pickle.load(open("backedup_dates","rb"))
except IOError:
	datesFile = set()

print dateFile


for m in match:
	
	
	time = m.groups('0')[0]
	print time
	
	if time not in dateFile:
		dateFile.add(time)
		dates += time + "\n"

if len(dates) != 0:
	
	sg = sendgrid.SendGridClient(sendgrid_username, sendgrid_password)

	message = sendgrid.Mail()
	message.add_to([mail])
	message.set_subject('New Episode is Here!')

	message.set_text(dates)
	message.set_from(address)
	status, msg = sg.send(message)

	print ("email sent")


pickle.dump(dateFile,open("backedup_dates","wb"))


























