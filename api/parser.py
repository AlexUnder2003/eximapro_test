import requests
from bs4 import BeautifulSoup


def fetch_tenders(max_items=100):
    url = "https://rostender.info/extsearch"
    tenders = []
    page = 1

    while len(tenders) < max_items:
        response = requests.get(url, params={"page": page})
        soup = BeautifulSoup(response.text, "html.parser")

        articles = soup.select("article.tender-row")
        if not articles:
            break

        for tender in articles:
            if len(tenders) >= max_items:
                break

            tender_id = tender.select_one(".tender__number")
            date_start = tender.select_one(".tender__date-start")
            title = tender.select_one(".tender-info__description")
            url_tag = tender.select_one(".tender-info__description")
            date_end_date = tender.select_one(".tender__countdown-text .black")
            date_end_time = tender.select_one(".tender__countdown-container")
            price = tender.select_one(".starting-price--price")
            location = [
                loc.get_text(strip=True)
                for loc in tender.select(".tender-address .line-clamp")
            ]
            categories = [
                cat.get_text(strip=True)
                for cat in tender.select(".list-branches__link")
            ]

            tenders.append(
                {
                    "tender_id": (
                        tender_id.get_text(strip=True).replace("№", "")
                        if tender_id
                        else None
                    ),
                    "title": title.get_text(strip=True) if title else None,
                    "url": (
                        "https://rostender.info" + url_tag["href"]
                        if url_tag and url_tag.has_attr("href")
                        else None
                    ),
                    "date_start": (
                        date_start.get_text(strip=True) if date_start else None
                    ),
                    "date_end": (
                        f"{date_end_date.get_text(strip=True)} {date_end_time.get_text(strip=True)}"
                        if date_end_date and date_end_time
                        else None
                    ),
                    "price": price.get_text(strip=True) if price else None,
                    "location": " ".join(location),
                    "categories": categories,
                }
            )

        page += 1

    return tenders
