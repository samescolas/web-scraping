import scrapy
from scrapy.http import Request

cities = ['newyork', 'boston', 'seattle', 'sanfrancisco', 'austin', 'providence', 'chicago', 'detroit', 'denver']

class CLSpider(scrapy.Spider):
	name = 'job-spider'
	#start_urls = ['https://{}.craigslist.org/d/jobs/search/jjj'.format(city) for city in cities]
	start_urls = ['https://boston.craigslist.org/d/jobs/search/jjj']

	def parse(self, response):
		for job in response.css('p.result-info'):
			title = job.css('a.result-title::text').extract_first()
			link = job.css('a.result-title::attr(href)').extract_first()
			ad_response = Request(link)
			yield { 
				'title': title,
				'link': link,
				'response': ad_response
			}

	def parse_ad(self, response):
		print("IM INSIDE PARSE_AD!!!! ", response)
		return {'biznatch': response}
