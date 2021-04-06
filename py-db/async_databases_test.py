from typing import List
import databases
import pytest
import sqlalchemy as sa
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import select
from starlette.testclient import TestClient

USER_1 = {"name": "테스트유저"}
ARTICLE_1 = {"title": "제목", "body": "내용", "author_id": 1}
ARTICLE_2 = {"title": "title", "body": "body", "author_id": 1}
ARTICLE_1_WITH_AUTHOR = {'author': {'id': 1, 'name': '테스트유저'}, 'id': 1, 'body': '내용', 'title': '제목'}
ARTICLE_2_WITH_AUTHOR = {'author': {'id': 1, 'name': '테스트유저'}, 'id': 2, 'title': 'title', 'body': 'body'}

DATABASE_URL = "sqlite:///./test.db"
database = databases.Database(DATABASE_URL)
metadata = sa.MetaData()

users_table = sa.Table(
    "USERS",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String(16)),
)

articles_table = sa.Table(
    "ARTICLES",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("title", sa.String(128)),
    sa.Column("body", sa.Text),
    sa.Column("author_id", sa.Integer, sa.ForeignKey('USERS.id'))
)

engine = sa.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)
pytestmark = pytest.mark.asyncio


class UserIn(BaseModel):
    name: str


class UserOut(BaseModel):
    id: int
    name: str


class ArticleIn(BaseModel):
    title: str
    body: str
    author_id: int


class ArticleOut(BaseModel):
    id: int
    title: str
    body: str
    author: UserOut


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/articles/", response_model=List[ArticleOut])
async def read_articles():
    j = articles_table.join(users_table, users_table.c.id == articles_table.c.author_id)
    query = select([articles_table, users_table]).select_from(j)
    result = await database.fetch_all(query)
    return [ArticleOut(
        id=row[0], title=row[1], body=row[2],
        author=UserOut(id=row[4], name=row[5])
    ) for row in result]


@app.post("/articles/")
async def create_article(article: ArticleIn):
    query = articles_table.insert()
    await database.execute(query, article.dict())


@app.delete("/articles/")
async def delete_all_articles():
    query = articles_table.delete()
    await database.execute(query)


@app.post("/users/")
async def create_user(user: UserIn):
    query = users_table.insert()
    await database.execute(query, user.dict())


@app.delete("/users/")
async def delete_all_users():
    query = users_table.delete()
    await database.execute(query)


class TestDatabases:
    client = TestClient(app)

    @classmethod
    def setup_class(cls):
        cls.client.post("/users/", json=USER_1)

    @classmethod
    def teardown_class(cls):
        cls.client.delete("/users/")

    def teardown_method(self, method) -> None:
        self.client.delete("/articles/")

    def test_write_article(self):
        self.client.post("/articles/", json=ARTICLE_1).json()

        response = self.client.get("/articles/")
        result = response.json()
        print(result)
        assert result == [ARTICLE_1_WITH_AUTHOR]

    def test_write_many_articles(self):
        self.client.post("/articles/", json=ARTICLE_1)
        self.client.post("/articles/", json=ARTICLE_2)

        response = self.client.get("/articles/")
        result = response.json()
        print(result)
        assert result == [ARTICLE_1_WITH_AUTHOR, ARTICLE_2_WITH_AUTHOR]
