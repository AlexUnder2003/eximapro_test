from fastapi import FastAPI, Query

from parser import fetch_tenders
from schemas import Tender

app = FastAPI()


@app.get("/tenders", response_model=list[Tender])
def get_tenders(
    max_items: int = Query(100, ge=1),
):
    result = fetch_tenders(max_items)
    return result
