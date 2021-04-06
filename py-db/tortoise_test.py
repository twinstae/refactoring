from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.testclient import TestClient
from tortoise.models import Model
from tortoise import fields, Tortoise

USER_1 = {"name": "테스트유저"}
ARTICLE_1 = {"title": "제목", "body": "내용", "author_name": "테스트유저"}
ARTICLE_2 = {"title": "title", "body": "body", "author_name": "테스트유저"}
ARTICLE_1_WITH_AUTHOR = {'author': {'name': '테스트유저'}, 'title': '제목', 'body': '내용'}
ARTICLE_2_WITH_AUTHOR = {'author': {'name': '테스트유저'}, 'title': 'title', 'body': 'body'}

DATABASE_URL = "sqlite://test.db"


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(16)


class Article(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(128)
    body = fields.TextField()
    author = fields.ForeignKeyField('models.User')


class UserIn(BaseModel):
    name: str


class UserOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class ArticleIn(BaseModel):
    title: str
    body: str
    author_name: str


class ArticleOut(BaseModel):
    id: int
    title: str
    body: str
    author: UserOut

    class Config:
        orm_mode = True


app = FastAPI()


@app.post("/setup/")
async def setup_request():
    await Tortoise.init(
        db_url='sqlite://:memory:',
        modules={'models': ['tortoise_test']}
    )
    await Tortoise.generate_schemas()

    await User.create(**USER_1)


@app.get("/articles/", response_model=List[ArticleOut])
async def read_articles():
    return await Article.all().prefetch_related('author')


@app.post("/articles/")
async def create_article(article: ArticleIn):
    user = await User.get_or_none(name=article.author_name)
    await Article.create(**article.dict(), author=user)


@app.delete("/articles/")
async def delete_all_articles():
    await Article.all().delete()


@app.delete("/teardown/")
async def teardown():
    await User.all().delete()
    await Tortoise.close_connections()


def consistency_check(result, expected):
    print(result)
    for r, e in zip(result, expected):
        for key in ['title', 'body']:
            assert r[key] == e[key]
        assert r['author']['name'] == e['author']['name']


class TestTortoise:
    client = TestClient(app)

    @classmethod
    def setup_class(cls):
        cls.client.post("/setup/")

    @classmethod
    def teardown_class(cls):
        cls.client.delete("/teardown/")

    def teardown_method(self, method) -> None:
        self.client.delete("/articles/")

    def test_write_article(self):
        self.client.post("/articles/", json=ARTICLE_1)

        response = self.client.get("/articles/")
        result = response.json()
        consistency_check(result, [ARTICLE_1_WITH_AUTHOR])

    def test_write_many_articles(self):
        self.client.post("/articles/", json=ARTICLE_1)
        self.client.post("/articles/", json=ARTICLE_2)

        response = self.client.get("/articles/")
        result = response.json()
        consistency_check(result, [ARTICLE_1_WITH_AUTHOR, ARTICLE_2_WITH_AUTHOR])
