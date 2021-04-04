from sqlalchemy import create_engine, text
from typing import List, Any, Optional
from unittest import TestCase

from sqlalchemy.engine.base import Connection
from typing_extensions import TypedDict


class Article(TypedDict):
    title: str
    body: str


ARTICLES = "ARTICLES"
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)


class SqlAlchemyTest(TestCase):
    conn: Connection = engine.connect()

    @classmethod
    def setUpClass(cls) -> None:
        print(type(cls.conn))
        cls.conn.execute(text(f'''CREATE TABLE {ARTICLES} (title text, body text);'''))

    def tearDown(self) -> None:
        self.conn.execute(text(f'''DELETE FROM {ARTICLES}'''))

    @classmethod
    def tearDownClass(cls) -> None:
        cls.conn.close()

    def write_article(self, article: Article):
        self.conn.execute(f"INSERT INTO {ARTICLES} VALUES (:title, :body);", article)

    def get_articles(self) -> List[Any]:
        cursor = self.conn.execute(f"SELECT * FROM {ARTICLES};")
        return cursor.fetchall()

    def test_write_article(self):
        self.write_article({"title": "제목", "body": "내용"})

        article = self.get_article_by_title("제목")
        print(type(article))

        assert article == ("제목", "내용")

    def write_many_articles(self, articles: List[Article]):
        self.conn.execute(text(f"INSERT INTO {ARTICLES} VALUES (:title, :body);"), articles)

    def test_write_many_article(self):
        self.write_many_articles([
            {"title": "제목", "body": "내용"},
            {"title": "title", "body": "body"}
        ])

        articles = self.get_articles()
        print(type(articles))

        assert articles == [("제목", "내용"), ("title", "body")]

    def get_article_by_title(self, title) -> Optional[Any]:
        cursor = self.conn.execute(f"SELECT * FROM {ARTICLES} WHERE title=:title;", {"title": title})
        return cursor.fetchone()
