import urllib.request
import ssl # To get HTTPS using urllib 
from bs4 import BeautifulSoup
import re # regex
import feedgenerator
from google.cloud import storage
import os

# Set creds for GCS upload
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="gcs_secrets.json"

# Generate cert for the HTTPS call
ssl._create_default_https_context = ssl._create_unverified_context

def feedgen(request, payload):
	"""
	Main function which makes a HTTP request to the
	AFR.com. The response is parsed using
	BeautifulSoup and then formatted into 
	an RSS feed format with the below attributes: 

	title
	link
	description
	unique_id

	This is saved as an XML feed in a Cloud Storage
	Bucket. The URL can be publically accessed as
	an RSS feed, for integrations in readers. 

	The script is intended to be ran as a sheduled 
	Cloud Function. 

	Args:
	  request: generated from the PubSub topic
	  payload: generated from the PubSub topic

	Returns:
	  True 

	"""

	# Make HTTP call
	response = urllib.request.urlopen("https://www.afr.com/")#
	html = response.read()

	# Soupify
	soup = BeautifulSoup(html, features="html.parser")
	results = soup.select('[data-pb-type="st"]')

	feed = feedgenerator.Rss201rev2Feed(title="AFR.com.au",
			link="https://www.afr.com",
			description="Created by Joe",
			language="en")

	for x in results:
		# Headline
		article_info = x.select('[data-pb-type="hl"]')
		final_article_title = article_info[0].getText()
		print(final_article_title)

		# ID
		article_url = article_info[0].find('a')['href']
		final_article_article_id = '-'.join(article_url.split('-')[-2:])
		print(final_article_article_id)

		# Description 
		article_description = x.select('[data-pb-type="ab"]')
		if len(article_description) == 1:
			final_article_description = article_description[0].getText()
			print(final_article_description) 
		else:
			final_article_description = "No description"
			print(final_article_description)

		# URL 
		afr_url_append = "https://www.afr.com"
		final_article_url = afr_url_append + article_url
		print(final_article_url)

		print('-----\n')

		feed.add_item(
			title=final_article_title,
			link=final_article_url,
			description=final_article_description,
			unique_id=final_article_article_id
		)

	# Console logging
	print("Completed feed generation....\n---")
	print(feed.writeString('utf-8'))
	print("Uploading to cloud....\n---")

	# Cloud storage
	storage_client = storage.Client()
	bucket = storage_client.get_bucket("afr-rss-feed-bucket")
	blob = bucket.blob('feed.xml')
	blob.upload_from_string(feed.writeString('utf-8').encode())

	print("Complete! Exiting..")