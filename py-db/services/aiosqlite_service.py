import aiosqlite
from aiosqlite import Connection
from pydantic_models import ArticleOut, ArticleIn, UserOut, UserIn
from services.ab_service import ABService

ARTICLE = "ARTICLE"
USER = "USER"


class AioSqliteService(ABService):
    name = "aiosqlite"
    con: Connection

    @classmethod
    async def setup(cls):
        cls.con = await aiosqlite.connect(':memory:')
        await cls.con.execute(f'''
                CREATE TABLE {USER} (
                    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    "name" VARCHAR(16) NOT NULL
                );''')

        await cls.con.execute(f'''
                CREATE TABLE {ARTICLE} (
                    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    "title" VARCHAR(128) NOT NULL,
                    "body" TEXT NOT NULL,
                    "author_id" INT NOT NULL REFERENCES "{USER}" ("id") ON DELETE CASCADE
                );''')

    @classmethod
    async def teardown(cls):
        await cls.con.execute(f'''DELETE FROM {USER}''')
        await cls.con.close()

    @classmethod
    async def create_user(cls, user_in: UserIn) -> None:
        await cls.con.execute(f"INSERT INTO {USER}(name) VALUES (:name);", user_in.dict())

    @classmethod
    async def get_user_articles(cls, user_name: str):
        cursor = await cls.con.execute(f"""
                SELECT * FROM {USER}
                INNER JOIN {ARTICLE}
                ON {ARTICLE}.author_id={USER}.id;
            """)
        result = await cursor.fetchall()
        return [ArticleOut(
            id=row[2], title=row[3], body=row[4],
            author=UserOut(id=row[0], name=row[1])
        ) for row in result]

    @classmethod
    async def read_articles(cls):
        cursor = await cls.con.execute(f"""
                SELECT * FROM {ARTICLE}
                INNER JOIN {USER}
                ON {ARTICLE}.author_id={USER}.id;
            """)
        result = await cursor.fetchall()
        return [ArticleOut(
            id=row[0], title=row[1], body=row[2],
            author=UserOut(id=row[4], name=row[5])
        ) for row in result]

    @classmethod
    async def create_article(cls, article: ArticleIn):
        cur = await cls.con.execute(f"SELECT id FROM {USER};")
        author_id = await cur.fetchone()
        query = f"INSERT INTO {ARTICLE}(title, body, author_id) VALUES (?, ?, ?);"
        await cls.con.execute(query, (
            article.title, article.body, author_id[0]
        ))

    @classmethod
    async def delete_all_articles(cls):
        await cls.con.execute(f'''DELETE FROM {ARTICLE}''')
