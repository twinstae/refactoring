from pydantic_models import ArticleOut, ArticleIn
from services import ABService, AioSqliteService, TortoiseService, DatabasesService
from typing import List
from fastapi import FastAPI


app = FastAPI()
my_service: ABService.__class__ = AioSqliteService

name_to_service = {
    service.name: service
    for service in [
        AioSqliteService,
        TortoiseService,
        DatabasesService
    ]
}


@app.post("/setup/{service_name}")
async def setup_request(service_name: str):
    global my_service
    my_service = name_to_service[service_name]
    await my_service.setup()


@app.get("/articles/", response_model=List[ArticleOut])
async def read_articles():
    return await my_service.read_articles()


@app.post("/articles/")
async def create_article(article: ArticleIn):
    await my_service.create_article(article)


@app.delete("/articles/")
async def delete_all_articles():
    await my_service.delete_all_articles()


@app.delete("/teardown/")
async def teardown():
    await my_service.teardown()
