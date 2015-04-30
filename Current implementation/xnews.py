import requests
import re
import time
import cPickle as pickle
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from news_settings import *



# Start of news reader
storageFile = 'articles.data'
serverStorageFile = '/share/mohamed/news_scraper/articles.data'
try:
	fd = open(storageFile)
except:
	fd = open(serverStorageFile)
try:
	seenHeadlines = pickle.load(fd)
except:
	seenHeadlines = []
fd.close()



# Required global variables
link = ""
currentTime = time.localtime(time.time())



# Function for cleanly viewing xml while testing
def prettify(elem):
    # Return a pretty-printed XML string for the Element.
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

# Function for testing if word is in text
def findWholeWord(word):
    return re.compile(r'\b({0}s?)\b'.format(word), flags=re.IGNORECASE).search

# Main function
def scanPage(url):
	global seenHeadlines, link

	r = requests.get(url)
	if r.status_code == 200:
		try:
			print "Got page: " + url

			root = ET.fromstring(r.content)
			# print prettify(root)
			# print "\n\n\n\n\n"

			topic = re.search('http://www.cbc.ca/cmlink/rss-(.+)', url).group(1).title()

			headlines = root.findall('.//item')
			# print len(headlines)

			for headline in headlines:
				title = headline.find('title').text
				source = headline.find('link').text[:-8]
				allDescription = headline.find('description').text
				description = re.search('<p>(.+?)</p>', allDescription).group(1)

				for word in flaggedWords:
					if (findWholeWord(word)(title)) or (findWholeWord(word)(description)):
						if source not in seenHeadlines:
							article = "Headline: " + title + "\n\nDescription: " + description + "\n\nTopic: " + topic + "\n\nFlagged word: " + word.title() + "\n\nLink: " + source + "\n\n\n\n"
							link += article
							seenHeadlines.append(source)
		except:
			with open("errors.txt", "a") as myfile:
				month = str(currentTime[1])
				day = str(currentTime[2])
				year = str(currentTime[0])
				if currentTime[3] > 12:
					hour = str(currentTime[3] - 12)
					meridian = "pm"
				else:
					hour = str(currentTime[3])
					meridian = "am"
				if str(currentTime[4]) < 10:
					minute = "0" + str(currentTime[4])
				else:
					minute = str(currentTime[4])
				minute = str(currentTime[4])
				time = hour + ":" + minute + meridian + ", " + month + "/" + day + "/" + year + ": "
				log = time + url + "\n"
				print log
				myfile.write(log)
	else:
		print "Failed request"

if currentTime[3] >= 7 and currentTime[3] <= 22:
	scanPage('http://www.cbc.ca/cmlink/rss-topstories')
	scanPage('http://www.cbc.ca/cmlink/rss-world')
	scanPage('http://www.cbc.ca/cmlink/rss-canada')
	scanPage('http://www.cbc.ca/cmlink/rss-politics')
	scanPage('http://www.cbc.ca/cmlink/rss-business')
	scanPage('http://www.cbc.ca/cmlink/rss-health')
	scanPage('http://www.cbc.ca/cmlink/rss-arts')
	scanPage('http://www.cbc.ca/cmlink/rss-technology')
	# scanPage('http://www.cbc.ca/cmlink/rss-offbeat')
	scanPage('http://www.cbc.ca/cmlink/rss-cbcaboriginal')
	# scanPage('http://www.cbc.ca/cmlink/rss-canada-kitchenerwaterloo')

	print link

	if link != "":
		# Send myself email
		print "Sending email!"

		link += "This is the end of your custom news update. So far, you have been notified about " + str(len(seenHeadlines)) + " headlines."

		payload_send = {"api_user":api_user,
		           		"api_key":api_key,
		           		"to":user_email,
		           		"from":user_email,
		           		"subject":"Custom News Update",
		           		"text":link}

		m = requests.post('https://api.sendgrid.com/api/mail.send.json',
		                  params=payload_send)

		print m.text
else:
	print currentTime


fw = open(storageFile, 'w')
pickle.dump(seenHeadlines, fw)
fw.close()
