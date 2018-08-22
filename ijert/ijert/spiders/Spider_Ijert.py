import scrapy
from ijert.items import IjertItem
class SpiderIJERT(scrapy.Spider):
	name ="IEEE digital Library"
	start_urls = ["https://www.ijert.org/browse/volume-7-2018/january-2018-edition"]

	def parse(self,response):
		print(response.url)

		links = response.xpath("//a[contains(@class,'btn-success')]/@href")

		for link in links:
			item  = IjertItem()
			item['file_urls'] = [link.extract()]
			yield item