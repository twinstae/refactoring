from sqlalchemy import create_engine, Column, Integer, String, delete, ForeignKey
from typing import List
from unittest import TestCase
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
Base = declarative_base()


class Users(Base):
    __tablename__ = "USERS"

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    my_articles = relationship("Articles", back_populates="author")

    def __repr__(self):
        return f"Users(id={self.id!r}, name={self.name!r})"


class Articles(Base):
    __tablename__ = "ARTICLES"

    id = Column(Integer, primary_key=True)
    title = Column(String(128), nullable=False)
    body = Column(String(512), nullable=False)
    author_id = Column(Integer, ForeignKey('USERS.id'))  # 테이블 명
    author = relationship("Users", back_populates="my_articles")  # 클래스 명

    def __repr__(self):
        return f"Articles(id={self.id!r}, title={self.title!r}, body={self.body!r})"


class SqlAlchemyTest(TestCase):
    session: Session = Session(engine)

    @classmethod
    def setUpClass(cls) -> None:
        Base.metadata.create_all(engine)
        cls.user_1 = Users(name="테스트유저", my_articles=[])
        cls.session.add(cls.user_1)

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
            Articles(title="제목", body="내용", author=self.user_1)
        ]
        self.write_articles(articles)

        result = self.get_articles()
        assert result == articles

    def test_write_many_article(self):
        articles = [
            Articles(title="제목", body="내용", author=self.user_1),
            Articles(title="title", body="body", author=self.user_1)
        ]
        self.write_articles(articles)

        result = self.get_articles()
        assert result == articles
