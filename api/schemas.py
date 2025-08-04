from pydantic import BaseModel


class Tender(BaseModel):
    tender_id: str
    title: str
    url: str
    date_start: str | None = None
    date_end: str | None = None
    categories: list[str] | None = None
    price: str | None = None
    location: str | None = None
