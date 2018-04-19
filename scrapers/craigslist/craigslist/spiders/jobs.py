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
			#ad_response = Request(link)
			yield Request(link, callback=self.parse_ad, meta={ 'title': title })

	def parse_ad(self, response):
		description = "".join(line for line in response.css('section#postingbody::text').extract())
		yield {
			'description': description,
			'title': response.meta['title']
		}
