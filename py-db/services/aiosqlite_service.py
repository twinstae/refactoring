import aiosqlite
from aiosqlite import Connection
from pydantic_models import ArticleOut, ArticleIn, UserOut
from services.ab_service import ABService

ARTICLES = "ARTICLES"
USERS = "USERS"
USER_1 = {"name": "테스트유저"}


class AioSqliteService(ABService):
    name = "aiosqlite"
    con: Connection

    @classmethod
    async def setup(cls):
        cls.con = await aiosqlite.connect(':memory:')
        await cls.con.execute(f'''
                CREATE TABLE {USERS} (
                    id integer primary key,
                    name varchar
                );''')

        await cls.con.execute(f'''
                CREATE TABLE {ARTICLES} (
                    id integer primary key,
                    title text,
                    body text,
                    author_id integer,
                    FOREIGN KEY(author_id) REFERENCES {USERS}(id)
                );''')

        await cls.con.execute(f"INSERT INTO {USERS}(name) VALUES (:name);", USER_1)

    @classmethod
    async def teardown(cls):
        await cls.con.execute(f'''DELETE FROM {USERS}''')
        await cls.con.close()

    @classmethod
    async def read_articles(cls):
        cursor = await cls.con.execute(f"""
                SELECT * FROM {ARTICLES}
                INNER JOIN {USERS}
                ON {ARTICLES}.author_id={USERS}.id;
            """)
        result = await cursor.fetchall()
        return [ArticleOut(
            id=row[0], title=row[1], body=row[2],
            author=UserOut(id=row[4], name=row[5])
        ) for row in result]

    @classmethod
    async def create_article(cls, article: ArticleIn):
        cur = await cls.con.execute(f"SELECT id FROM {USERS};")
        author_id = await cur.fetchone()
        query = f"INSERT INTO {ARTICLES}(title, body, author_id) VALUES (?, ?, ?);"
        await cls.con.execute(query, (
            article.title, article.body, author_id[0]
        ))

    @classmethod
    async def delete_all_articles(cls):
        await cls.con.execute(f'''DELETE FROM {ARTICLES}''')
