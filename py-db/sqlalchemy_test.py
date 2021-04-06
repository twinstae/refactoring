from sqlalchemy import create_engine, Column, Integer, String, delete, ForeignKey, Text
from typing import List
from unittest import TestCase
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
Base = declarative_base()


class User(Base):
    __tablename__ = "USERS"

    id = Column(Integer, primary_key=True)
    name = Column(String(16), nullable=False)
    my_articles = relationship("Article", back_populates="author")

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r})"


class Article(Base):
    __tablename__ = "ARTICLES"

    id = Column(Integer, primary_key=True)
    title = Column(String(128), nullable=False)
    body = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey('USERS.id'))  # 테이블 명
    author = relationship("User", back_populates="my_articles")  # 클래스 명

    def __repr__(self):
        return f"Article(id={self.id!r}, title={self.title!r}, body={self.body!r}, author={self.author!r})"


class SqlAlchemyTest(TestCase):
    session: Session = Session(engine)

    @classmethod
    def setUpClass(cls) -> None:
        Base.metadata.create_all(engine)
        cls.user_1 = User(name="테스트유저", my_articles=[])
        cls.session.add(cls.user_1)

    def tearDown(self) -> None:
        self.session.execute(delete(Article))

    @classmethod
    def tearDownClass(cls) -> None:
        cls.session.close()

    def write_articles(self, articles: List[Article]):
        self.session.add_all(articles)
        self.session.flush()

    def get_articles(self) -> List[Article]:
        return self.session.query(Article).all()

    def test_write_article(self):
        articles = [
            Article(title="제목", body="내용", author=self.user_1)
        ]
        self.write_articles(articles)

        result = self.get_articles()
        print(result)
        assert result == articles

    def test_write_many_article(self):
        articles = [
            Article(title="제목", body="내용", author=self.user_1),
            Article(title="title", body="body", author=self.user_1)
        ]
        self.write_articles(articles)

        result = self.get_articles()
        print(result)
        assert result == articles
