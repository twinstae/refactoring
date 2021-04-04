from typing import List
from unittest import TestCase
import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.testclient import TestClient

DATABASE_URL = "sqlite:///./test.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

articles_table = sqlalchemy.Table(
    "articles",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("body", sqlalchemy.String),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


class ArticleIn(BaseModel):
    title: str
    body: str


class ArticleOut(BaseModel):
    id: int
    title: str
    body: str


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/articles/", response_model=List[ArticleOut])
async def read_notes():
    query = articles_table.select()
    return await database.fetch_all(query)


@app.post("/articles/", response_model=ArticleOut)
async def create_note(article: ArticleIn):
    query = articles_table.insert()
    last_record_id = await database.execute(query, article.dict())
    return {**article.dict(), "id": last_record_id}


@app.delete("/articles/")
async def delete_all_notes():
    query = articles_table.delete()
    await database.execute(query)


class SqlAlchemyTest(TestCase):
    client = TestClient(app)

    def tearDown(self) -> None:
        self.client.delete("/articles/")

    def test_write_article(self):
        self.client.post("/articles/", json={"title": "제목", "body": "내용"})

        response = self.client.get("/articles/")
        assert response.json() == [{"id": 1, "title": "제목", "body": "내용"}]

    def test_write_many_articles(self):
        self.client.post("/articles/", json={"title": "제목", "body": "내용"})
        self.client.post("/articles/", json={"title": "title", "body": "body"})

        response = self.client.get("/articles/")
        assert response.json() == [
            {"id": 1, "title": "제목", "body": "내용"},
            {"id": 2, "title": "title", "body": "body"}
        ]
