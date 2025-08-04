import scrapy

from eximapro.eximapro.items import RostenderItem


class RostenderSpider(scrapy.Spider):
    name = "rostender"
    allowed_domains = ["rostender.info"]
    start_urls = ["https://rostender.info/extsearch"]

    def __init__(self, max_tenders=100, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_tenders = int(max_tenders)
        self.total_parsed = 0

    def parse(self, response):
        if self.total_parsed >= self.max_tenders:
            return

        for tender in response.css("article.tender-row"):
            if self.total_parsed >= self.max_tenders:
                break

            tender_id = tender.css(".tender__number::text").re_first(
                r"№\s*(\d+)"
            )
            date_start = tender.css(".tender__date-start::text").get()
            title = tender.css(".tender-info__description::text").get()
            url = tender.css(".tender-info__description::attr(href)").get()
            date_end_date = tender.css(
                ".tender__countdown-text .black::text"
            ).get()
            date_end_time = tender.css(
                ".tender__countdown-container::text"
            ).get()
            price = tender.css(".starting-price--price::text").get()
            location = tender.css(".tender-address .line-clamp::text").getall()
            categories = tender.css(".list-branches__link::text").getall()

            self.total_parsed += 1

            yield RostenderItem(
                {
                    "tender_id": tender_id,
                    "title": title.strip() if title else None,
                    "url": response.urljoin(url) if url else None,
                    "date_start": date_start.strip() if date_start else None,
                    "date_end": (
                        f"{date_end_date.strip()} {date_end_time.strip()}"
                        if date_end_date and date_end_time
                        else None
                    ),
                    "price": price.strip() if price else None,
                    "location": " ".join(
                        [l.strip() for l in location if l.strip()]
                    ),
                    "categories": [
                        cat.strip() for cat in categories if cat.strip()
                    ],
                }
            )

        if self.total_parsed < self.max_tenders:
            next_page = response.css(
                "ul.pagination li.last a::attr(href)"
            ).get()
            if next_page:
                yield response.follow(next_page, callback=self.parse)
