from typing import Union
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from scraper import get_url

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount('/static', StaticFiles(directory="static"), name="static")

class UrlModel(BaseModel):
    url: str

@app.get("/")
def home(request: Request, response_class=HTMLResponse):
    return templates.TemplateResponse(
        request=request,
        name="home.html"
    )

# https://en.wikipedia.org/wiki/Gavin_King



@app.post("/crawl")
def crawl_url(body: UrlModel):
    # kick off crawling here
    r = get_url(body.url)

    return {"url": r}
# async def read_item(item_id: int, q: Union[str, None] = None):
    # return {"item_id": item_id, "q": q}