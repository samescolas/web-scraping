from scraper import AmazonScraper as Scraper
from sys import argv

scraper = Scraper(
	[],
	verbose=False,
	image_dir='./images')

def get_first(q):
	page = scraper.search(q)
	if page:
		try:
			result = page.find(class_="s-item-container").find('h2')['data-attribute']
		except:
			result = None
	else:
		return None
	return result

if len(argv) > 1:
	print(get_first(argv[1]))
