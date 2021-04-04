from sqlalchemy import create_engine, Table, Column, Integer, String, insert, select, delete
from typing import List, Any, Tuple
from unittest import TestCase
from sqlalchemy.orm import Session
from typing_extensions import TypedDict
from sqlalchemy import MetaData


class Article(TypedDict):
    title: str
    body: str


ARTICLES = "ARTICLES"
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
metadata = MetaData()

article_table = Table(
    "ARTICLES",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(128), nullable=False),
    Column('body', String(512), nullable=False)
)


class SqlAlchemyTest(TestCase):
    session: Session = Session(engine)

    @classmethod
    def setUpClass(cls) -> None:
        metadata.create_all(engine)

    def tearDown(self) -> None:
        self.session.execute(article_table.delete())

    @classmethod
    def tearDownClass(cls) -> None:
        cls.session.close()

    def write_articles(self, articles: List[Article]):
        self.session.execute(article_table.insert(), articles)
        self.session.commit()

    def get_articles(self) -> List[Tuple[int, str, str]]:
        cursor = self.session.execute(article_table.select())
        return cursor.fetchall()

    def test_write_article(self):
        self.write_articles([{"title": "제목", "body": "내용"}])

        articles = self.get_articles()

        assert articles == [(1, "제목", "내용")]

    def test_write_many_article(self):
        self.write_articles([
            {"title": "제목", "body": "내용"},
            {"title": "title", "body": "body"}
        ])

        articles = self.get_articles()

        assert articles == [(1, "제목", "내용"), (2, "title", "body")]
