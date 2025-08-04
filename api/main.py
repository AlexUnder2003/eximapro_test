from fastapi import FastAPI, Query

from parser import fetch_tenders
from schemas import Tender

app = FastAPI()


@app.get("/tenders", response_model=list[Tender])
async def get_tenders(
    max_items: int = Query(100, ge=1),
):
    tenders = await fetch_tenders(max_items=max_items)
    return tenders
