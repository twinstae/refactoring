import aiosqlite
from typing import List, Optional
from aiosqlite import Connection
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.testclient import TestClient

TEST_USER_NAME = "테스트유저"

ARTICLES = "ARTICLES"
USERS = "USERS"
USER_1 = {"name": "테스트유저"}
ARTICLE_1 = {"title": "제목", "body": "내용", "author_id": 1}
ARTICLE_2 = {"title": "title", "body": "body", "author_id": 1}
ARTICLE_1_WITH_AUTHOR = {'author': {'id': 1, 'name': '테스트유저'}, 'id': 1, 'body': '내용', 'title': '제목'}
ARTICLE_2_WITH_AUTHOR = {'author': {'id': 1, 'name': '테스트유저'}, 'id': 2, 'title': 'title', 'body': 'body'}


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
con = Optional[Connection]


@app.post("/setup/")
async def setup_request():
    global con
    con = await aiosqlite.connect(':memory:')
    await con.execute(f'''
        CREATE TABLE {USERS} (
            id integer primary key,
            name varchar
        );''')

    await con.execute(f"INSERT INTO {USERS}(name) VALUES (?);", (TEST_USER_NAME, ))
    await con.execute(f'''
        CREATE TABLE {ARTICLES} (
            id integer primary key,
            title text,
            body text,
            author_id integer,
            FOREIGN KEY(author_id) REFERENCES {USERS}(id)
        );''')


@app.get("/articles/", response_model=List[ArticleOut])
async def read_articles():
    cursor = await con.execute(f"""
        SELECT * FROM {ARTICLES}
        INNER JOIN {USERS}
        ON {ARTICLES}.author_id={USERS}.id;
    """)
    result = await cursor.fetchall()
    return [ArticleOut(
        id=row[0], title=row[1], body=row[2],
        author=UserOut(id=row[4], name=row[5])
    ) for row in result]


@app.post("/articles/")
async def create_article(article: ArticleIn):
    query = f"INSERT INTO {ARTICLES}(title, body, author_id) VALUES (?, ?, ?);"
    await con.execute(query, (
        article.title,
        article.body,
        article.author_id
    ))


@app.delete("/articles/")
async def delete_all_articles():
    await con.execute(f'''DELETE FROM {ARTICLES}''')


@app.delete("/teardown/")
async def teardown():
    await con.execute(f'''DELETE FROM {USERS}''')
    await con.close()


class TestAioSqlite:
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
        print(result)
        assert result == [ARTICLE_1_WITH_AUTHOR]

    def test_write_many_articles(self):
        self.client.post("/articles/", json=ARTICLE_1)
        self.client.post("/articles/", json=ARTICLE_2)

        response = self.client.get("/articles/")
        result = response.json()
        print(result)
        assert result == [ARTICLE_1_WITH_AUTHOR, ARTICLE_2_WITH_AUTHOR]
