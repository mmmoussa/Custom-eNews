import requests
import re
import time
import cPickle as pickle
import html5lib
from bs4 import BeautifulSoup
from news_settings import *


# Start of news reader
storageFile = 'storage.data'
serverStorageFile = '/share/mohamed/news_scraper/storage.data'
try:
	fd = open(storageFile)
except:
	fd = open(serverStorageFile)
try:
	seenHeadlines = pickle.load(fd)
except:
	seenHeadlines = []
fd.close()

link = ""
currentTime = time.localtime(time.time())

def findWholeWord(word):
    return re.compile(r'\b({0}s?)\b'.format(word), flags=re.IGNORECASE).search

def scanPage(url):
	global seenHeadlines, link

	headlines = []
	smallTopStoriesDiv1 = []
	smallTopStoriesDiv2 = []
	smallTopStories1 = []
	smallTopStories2 = []

	r = requests.get(url)
	if r.status_code == 200:
		print "Got page: " + url
		try:
			soup = BeautifulSoup(r.text)
		except:
			soup = BeautifulSoup(r.text, 'html5')
		#print soup.prettify()

		# Major headlines
		bigTopStoriesDiv = soup.select('.topstories-primarylist')
		bigTopStories = bigTopStoriesDiv[0].find_all('h2')

		for story in bigTopStories:
			headlines.append(story.find_all('a', limit=1, text=True))

		# Minor headlines
		try:
			smallTopStoriesDiv1 = soup.select('.moreheadlines-body')
			smallTopStories1 = smallTopStoriesDiv1[0].find_all('li')
		except:
			pass
		try:
			smallTopStoriesDiv2 = soup.select('.topstories-secondarylist')
			smallTopStories2 = smallTopStoriesDiv2[0].find_all('li')
		except:
			pass

		if len(smallTopStories1) > 0:
			for story in smallTopStories1:
				headlines.append(story.find_all('a', limit=1, text=True))
		if len(smallTopStories2) > 0:
			for story in smallTopStories2:
				headlines.append(story.find_all('a', limit=1, text=True))

		if len(headlines[-1]) == 0:
			print "\n\n\nSaved!\n\n\n"
			headlines.pop()

		# Act on list of headlines
		for headline in headlines:
			# print "- " + headline[0].text
			for word in flaggedWords:
				if findWholeWord(word)(headline[0].text):
					if headline[0].text not in seenHeadlines:
						link += "Headline: " + headline[0].text + "\n\nLink: " + "http://www.cbc.ca" + headline[0]['href'] + "\n\nFlagged word: " + word.title() + "\n\n\n\n"
						print headline[0].text + "\n"
						seenHeadlines.append(headline[0].text)

	else:
		print "Failed request"

if currentTime[3] >= 7 and currentTime[3] <= 22:
	scanPage('http://www.cbc.ca/news')
	scanPage('http://www.cbc.ca/news/world')
	scanPage('http://www.cbc.ca/news/canada')
	scanPage('http://www.cbc.ca/news/politics')
	scanPage('http://www.cbc.ca/news/business')
	scanPage('http://www.cbc.ca/news/health')
	scanPage('http://www.cbc.ca/news/arts')
	scanPage('http://www.cbc.ca/news/technology')


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
