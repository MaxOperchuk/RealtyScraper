import os
import time
from typing import Iterable
from urllib.parse import urljoin

import scrapy
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from scrapy import Request
from scrapy.http import Response
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


load_dotenv()

APARTMENT_SCRAPE_LIMIT = int(os.getenv("APARTMENT_SCRAPE_LIMIT"))


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

    def close(self, reason: str) -> None:
        self.driver.close()

    def parse(self, response: Response, **kwargs):

        yield {
            "title": self._get_title(response),
            "link": response.url,
            "region": self._get_region(response),
            "address": self._get_address(response),
            "description": self._get_description(response),
            "photos_links": self._get_photos_links(response),
            "price": self._get_price(response),
            "number_of_bedrooms": self._get_number_of_bedrooms(response),
            "floor_area": self._get_floor_area(response),
        }

    @staticmethod
    def _get_floor_area(response: Response) -> str | float:
        floor_area = response.css(
            "div.carac-value span::text"
        ).get()

        if not floor_area:
            return "Floor area not provided"

        floor_area = floor_area.split(" sqft")[0].strip().replace(",", ".")

        return float(floor_area)

    @staticmethod
    def _get_number_of_bedrooms(response: Response) -> int | str:
        number_of_bedrooms = response.css(
            "div.col-lg-3.col-sm-6.cac::text"
        ).get()

        if number_of_bedrooms:
            number_of_bedrooms = number_of_bedrooms.strip().split(" ")[0]
            return int(number_of_bedrooms)

        return "Number of bedrooms not provided"

    @staticmethod
    def _get_price(response: Response) -> float | str:
        price = response.css("span.text-nowrap::text").get()

        if not price:
            return "Price not provided"

        price = price.strip().replace("$", "").replace(",", ".")

        return float(price)

    @staticmethod
    def _get_photos_links(response: Response) -> str:
        photos_links = response.css(
            "div.thumbnail.last-child.first-child script::text"
        ).get()

        if photos_links:
            photos_links = photos_links.split(" = ")[1]
            return photos_links.split(";\r\n")[0]

        return "No photos provided"

    @staticmethod
    def _get_description(response: Response) -> str:
        description = response.css(
            "div.property-description div[itemprop='description']::text"
        ).get()

        if description:
            return description.strip()

        return "No description provided"

    @staticmethod
    def _get_location_text(response: Response) -> str:
        return response.css("div.d-flex.mt-1 h2::text").get()

    def _get_region(self, response: Response) -> str:
        location_text = self._get_location_text(response)

        if location_text:
            return "".join(location_text.split(",")[1:]).strip()

        return "Unknown address"

    def _get_address(self, response: Response) -> str:
        location_text = self._get_location_text(response)

        if location_text:
            return location_text.split(",")[0].strip()

        return "Unknown region"

    @staticmethod
    def _get_title(response: Response) -> str:
        title = response.css("span[data-id='PageTitle']::text").get()

        if title:
            return title.strip()

        return "No title provided"

    def _get_urls(self, url: str) -> list[str]:

        urls_set = set()

        self.driver.get(url)

        while True:

            page_source = self.driver.page_source
            time.sleep(2)
            self._click_next_button()

            urls_set.update(self._parse_detail_links(page_source))

            if len(urls_set) >= APARTMENT_SCRAPE_LIMIT:
                break

        return list(urls_set)[:APARTMENT_SCRAPE_LIMIT]

    @staticmethod
    def _parse_detail_links(page_source: str) -> list[str]:
        soup = BeautifulSoup(page_source, "html.parser")
        detail_links = [
            link.get("href")
            for link in soup.select(".property-thumbnail-summary-link")
        ]

        return detail_links

    def _click_next_button(self) -> None:

        try:
            next_button = WebDriverWait(
                self.driver, 10
            ).until(EC.element_to_be_clickable(
                (By.CLASS_NAME, "next"))
            )

            next_button.find_element(By.TAG_NAME, "a").click()
        except Exception as e:
            print(f"An error occurred: {e}")
