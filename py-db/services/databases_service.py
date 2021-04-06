import databases
import sqlalchemy as sa
from sqlalchemy import select
from pydantic_models import ArticleIn, ArticleOut, UserOut
from services import ABService

DATABASE_URL = "sqlite:///./test.db"
metadata = sa.MetaData()
USER_1 = {"name": "테스트유저"}

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


class DatabasesService(ABService):
    name = "databases"
    database = databases.Database(DATABASE_URL)
    
    @classmethod
    async def setup(cls):
        metadata.create_all(engine)
        await cls.database.connect()
        await cls.database.execute(users_table.insert(), USER_1)

    @classmethod
    async def teardown(cls):
        await cls.database.disconnect()
        await cls.database.execute(users_table.delete())

    @classmethod
    async def read_articles(cls):
        j = articles_table.join(users_table, users_table.c.id == articles_table.c.author_id)
        query = select([articles_table, users_table]).select_from(j)
        result = await cls.database.fetch_all(query)
        return [ArticleOut(
            id=row[0], title=row[1], body=row[2],
            author=UserOut(id=row[4], name=row[5])
        ) for row in result]

    @classmethod
    async def create_article(cls, article: ArticleIn):
        author = await cls.database.fetch_one(users_table.select())
    
        query = articles_table.insert()
    
        values = article.dict()
        del values['author_name']
        values['author_id'] = author["id"]
        await cls.database.execute(query, values)

    @classmethod
    async def delete_all_articles(cls):
        query = articles_table.delete()
        await cls.database.execute(query)
