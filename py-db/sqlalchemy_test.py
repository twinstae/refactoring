from sqlalchemy import create_engine, Column, Integer, String, select, delete
from typing import List, Tuple
from unittest import TestCase
from sqlalchemy.orm import Session, declarative_base

ARTICLES = "ARTICLES"
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
Base = declarative_base()


class Articles(Base):
    __tablename__ = "ARTICLES"

    id = Column(Integer, primary_key=True)
    title = Column(String(128), nullable=False)
    body = Column(String(512), nullable=False)

    def __repr__(self):
        return f"Article(id={self.id!r}, title={self.title!r}, body={self.body!r})"


class SqlAlchemyTest(TestCase):
    session: Session = Session(engine)

    @classmethod
    def setUpClass(cls) -> None:
        Base.metadata.create_all(engine)

    def tearDown(self) -> None:
        self.session.execute(delete(Articles))

    @classmethod
    def tearDownClass(cls) -> None:
        cls.session.close()

    def write_articles(self, articles: List[Articles]):
        self.session.add_all(articles)
        self.session.flush()

    def get_articles(self) -> List[Articles]:
        return self.session.query(Articles).all()

    def test_write_article(self):
        articles = [
            Articles(title="제목", body="내용")
        ]
        self.write_articles(articles)

        result = self.get_articles()
        assert result == articles

    def test_write_many_article(self):
        articles = [
            Articles(title="제목", body="내용"),
            Articles(title="title", body="body")
        ]
        self.write_articles(articles)

        result = self.get_articles()
        assert result == articles
