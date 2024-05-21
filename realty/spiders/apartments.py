import scrapy


class ApartmentsSpider(scrapy.Spider):
    name = "apartments"
    allowed_domains = ["realtylink.org"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.driver = webdriver.Chrome()

    def start_requests(self) -> Iterable[Request]:
        urls = []
        start_url = "https://realtylink.org/en/properties~for-rent"

        additional_urls = self._get_urls(start_url)
        urls.extend(additional_urls)

        for url in urls:

            url = urljoin(start_url, url)

            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        pass
