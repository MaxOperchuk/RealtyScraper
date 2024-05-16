import scrapy


class ApartmentsSpider(scrapy.Spider):
    name = "apartments"
    allowed_domains = ["realtylink.org"]
    start_urls = ["https://realtylink.org/en/properties~for-rent"]

    def parse(self, response):
        pass
