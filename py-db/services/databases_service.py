import databases
import sqlalchemy as sa
from sqlalchemy import select
from pydantic_models import ArticleIn, ArticleOut, UserOut, UserIn
from services import ABService

DATABASE_URL = "sqlite:///./test.db"
metadata = sa.MetaData()

user_table = sa.Table(
    "USER",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String(16)),
)

article_table = sa.Table(
    "ARTICLE",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("title", sa.String(128)),
    sa.Column("body", sa.Text),
    sa.Column("author_id", sa.Integer, sa.ForeignKey('USER.id'))
)

engine = sa.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)


class DatabasesService(ABService):
    name = "databases"
    database = databases.Database(DATABASE_URL)
    
    @classmethod
    async def setup(cls):
        metadata.create_all(engine)
        await cls.database.connect()

    @classmethod
    async def teardown(cls):
        await cls.database.disconnect()
        await cls.database.execute(user_table.delete())

    @classmethod
    async def create_user(cls, user_in: UserIn) -> None:
        await cls.database.execute(user_table.insert(), user_in.dict())

    @classmethod
    async def get_user_articles(cls, user_name: str):
        j = user_table.join(article_table, user_table.c.id == article_table.c.author_id)
        query = select([article_table, user_table]).select_from(j)
        result = await cls.database.fetch_all(query)
        return [ArticleOut(
            id=row[0], title=row[1], body=row[2],
            author=UserOut(id=row[4], name=row[5])
        ) for row in result]

    @classmethod
    async def read_articles(cls):
        j = article_table.join(user_table, user_table.c.id == article_table.c.author_id)
        query = select([article_table, user_table]).select_from(j)
        result = await cls.database.fetch_all(query)
        return [ArticleOut(
            id=row[0], title=row[1], body=row[2],
            author=UserOut(id=row[4], name=row[5])
        ) for row in result]

    @classmethod
    async def create_article(cls, article: ArticleIn):
        author = await cls.database.fetch_one(user_table.select())
    
        query = article_table.insert()
    
        values = article.dict()
        del values['author_name']
        values['author_id'] = author["id"]
        await cls.database.execute(query, values)

    @classmethod
    async def delete_all_articles(cls):
        query = article_table.delete()
        await cls.database.execute(query)
