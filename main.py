import argparse

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from eximapro.eximapro.spiders.rostender import RostenderSpider


def run_scrapy(max_items: int, output: str):
    settings = get_project_settings()
    settings.set(
        "FEEDS",
        {
            output: {
                "format": "csv" if output.endswith(".csv") else "json",
                "overwrite": True,
                "encoding": "utf-8",
            },
        },
    )
    settings.set("ROBOTSTXT_OBEY", False)

    process = CrawlerProcess(settings)
    process.crawl(RostenderSpider, max_tenders=max_items)
    process.start()


def main():
    parser = argparse.ArgumentParser(description="Сбор тендеров с сайта")
    parser.add_argument(
        "--max", type=int, default=100, help="Максимум тендеров"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="tenders.csv",
        help="Файл вывода (csv или json)",
    )
    parser.add_argument(
        "--domain",
        type=str,
        choices=["rostender.info", "b2bcenter"],
        default="rostender.info",
        help="Источник тендеров",
    )

    args = parser.parse_args()

    try:
        run_scrapy(args.max, args.output)
    except ValueError as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
