import scrapy


class ApartmentsSpider(scrapy.Spider):
    name = "apartments"
    allowed_domains = ["realtylink.org"]
    start_urls = ["https://realtylink.org/en/properties~for-rent"]
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.driver = webdriver.Chrome()


    def parse(self, response):
        pass
