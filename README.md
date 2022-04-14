# afr-rss-feed-generator
Creates a personal RSS feed for the AFR website. 

* I use an RSS reader (Feedly) to keep track of the content of many web sources, including a number of news websites. 
AFR.com did not have an accessible RSS feed which I could integrate into the reader, and so I developed a Cloud Function in Python that is scheduled to run on a daily basis (via cron/Cloud Scheduler) to scrape the homepage of the website and generate an XML file in RSS feed format, which is hosted in a Cloud Storage bucket. 
* I then use the publicly accessible URL of the feed file to integrate into the RSS reader. 
* This is provided for reference & demonstration purposes only. 

# System Design

<img width="790" alt="Screen Shot 2022-04-14 at 12 31 42 pm" src="https://user-images.githubusercontent.com/19522573/163302305-b79d1957-5d7e-4ed5-80f0-5ff000a41a8a.png">

# Screenshots

##### Example output once integrated in an RSS aggregator 
<img width="750" alt="Screen Shot 2022-04-12 at 3 12 18 pm" src="https://user-images.githubusercontent.com/19522573/163301958-46f29cf4-3ecc-49d9-9cb5-21424d7b5c20.png">

##### Example logging within Google Cloud Platform

<img width="750" alt="Screen Shot 2022-04-12 at 3 10 05 pm" src="https://user-images.githubusercontent.com/19522573/163302157-d4228c81-8af8-456a-a959-2815978f8a0d.png">
