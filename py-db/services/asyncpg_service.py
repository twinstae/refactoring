import asyncpg
from asyncpg import Connection
from pydantic_models import ArticleOut, ArticleIn, UserOut, UserIn
from services.ab_service import ABService

ARTICLE = "articles"
USER = "users"


class AsyncpgService(ABService):
    name = "asyncpg"
    con: Connection

    @classmethod
    async def setup(cls):
        cls.con = await asyncpg.connect(
            user='docker', password='docker',
            database='docker', host='127.0.0.1',
            port=49153
        )

        await cls.con.execute(f'''
                CREATE TABLE IF NOT EXISTS "{USER}"(
                "id" SERIAL NOT NULL PRIMARY KEY,
                "name" VARCHAR(16) NOT NULL
            );''')

        await cls.con.execute(f'''
                CREATE TABLE IF NOT EXISTS "{ARTICLE}" (
                "id" SERIAL NOT NULL PRIMARY KEY,
                "title" VARCHAR(128) NOT NULL,
                "body" TEXT NOT NULL,
                "author_id" INT NOT NULL REFERENCES "{USER}" ("id") ON DELETE CASCADE
            );''')

    @classmethod
    async def teardown(cls):
        await cls.con.execute(f'''DELETE FROM {USER}''')
        await cls.con.execute(f'''DROP TABLE {ARTICLE}''')
        await cls.con.execute(f'''DROP TABLE {USER}''')
        await cls.con.close()

    @classmethod
    async def create_user(cls, user_in: UserIn) -> None:
        await cls.con.execute(f"INSERT INTO {USER}(name) VALUES ($1)", user_in.name)

    @classmethod
    async def get_user_articles(cls, user_name: str):
        async with cls.con.transaction():
            result = await cls.con.fetch(f"""
                    SELECT * FROM {USER}
                    INNER JOIN {ARTICLE}
                    ON {ARTICLE}.author_id={USER}.id
                """)
            return [ArticleOut(
                id=record[2], title=record[3], body=record[4],
                author=UserOut(id=record[0], name=record[1])
            ) for record in result]

    @classmethod
    async def read_articles(cls):
        async with cls.con.transaction():
            result = await cls.con.fetch(f"""
                    SELECT * FROM {ARTICLE}
                    INNER JOIN {USER}
                    ON {ARTICLE}.author_id={USER}.id
                """)
            print(result[0])
            return [ArticleOut(
                id=record[0], title=record[1], body=record[2],
                author=UserOut(id=record[4], name=record[5])
            ) for record in result]

    @classmethod
    async def create_article(cls, article: ArticleIn):
        async with cls.con.transaction():
            author_record = await cls.con.fetchrow(f"SELECT id FROM {USER};")

            query = f"INSERT INTO {ARTICLE}(title, body, author_id) VALUES ($1, $2, $3)"
            await cls.con.execute(query, article.title, article.body, author_record['id'])

    @classmethod
    async def delete_all_articles(cls):
        await cls.con.execute(f'''DELETE FROM {ARTICLE}''')
