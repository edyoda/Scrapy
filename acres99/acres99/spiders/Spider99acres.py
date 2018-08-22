import scrapy
from acres99.items import PropertyItem
class Spider99acres(scrapy.Spider):
	name = "99acres"
	host_url = "https://www.99acres.com"

	start_urls = ['https://www.99acres.com/property-in-bangalore-ffid']

	item_count = 0
	page_count = 0
	def parse(self,response):
		Spider99acres.page_count +=1
		cards = response.xpath(".//div[@title='View Property Details']")     
		for card in cards[:10]:
			property_detail = PropertyItem()
		    
			title_1 = card.xpath(".//th/a/span/text()").extract_first()
			title_2 = card.xpath(".//th/a/span/b/text()").extract_first()
			property_title = title_1.strip(" ")+title_2.strip(" ")

			builder_name = card.xpath(".//a[@class='sName']/b/text()").extract_first()
			price = card.xpath(".//span[contains(@class,'srpNw_price')]/text()").extract_first()
			price_per_sq = card.xpath(".//td[@class='_auto_ppu_area']/text()").extract_first()
			super_area = card.xpath(".//td[@class='_auto_areaValue']/b/text()").extract_first()
			bd_room = card.xpath(".//td[@class='_auto_bedroom']/b/text()").extract_first()
			
			possession_raw = card.xpath(".//td[@class='_auto_possesionLabel']/text()").extract_first()
			possession = possession_raw.replace("\n","").strip(" ")
			
			# print("{} {} {} {} {} {} {}".format(property_title,price,price_per_sq,super_area,bd_room,builder_name,possession))

			## Loading Items

			property_detail['title'] = property_title
			property_detail['builder'] = builder_name
			property_detail['price'] = price
			property_detail['price_per_sqft'] = price_per_sq
			property_detail['super_area'] = super_area
			property_detail['bed_room'] = bd_room
			property_detail['posession'] = possession

			Spider99acres.item_count+=1
			print("Current item count",Spider99acres.item_count)
			yield property_detail

		next_page = response.xpath("//a[@name='nextbutton']/@href").extract_first()
		
		next_page_url = Spider99acres.host_url + next_page
	
		
		if Spider99acres.page_count <= 5:		
			yield scrapy.Request(url=next_page_url,callback = self.parse,dont_filter=True)
	