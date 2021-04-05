import aiosqlite
from sqlite3 import Row
from typing import List, Tuple, Coroutine, Any, Iterable, Optional
from unittest import TestCase

TEST_USER_NAME = "test"

ARTICLES = "ARTICLES"
USER = "USER"


class Sqlite3Test(TestCase):
    con = aiosqlite.connect(':memory:')

    @classmethod
    def setUpClass(cls) -> None:
        cls.con.execute(f'''CREATE TABLE {ARTICLES} (
            id integer primary key,
            title text,
            body text,
            FOREIGN KEY(author) REFERENCES USER(id)
        );''')
        cls.con.execute(f'''CREATE TABLE {USER} (
            id integer primary key,
            name varchar
        );''')
        cls.con.execute(f"INSERT INTO {USER} VALUES (?);", (TEST_USER_NAME,))

    def tearDown(self) -> None:
        self.con.execute(f'''DELETE FROM {ARTICLES}''')
        self.con.commit()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.con.close()

    async def write_article(self, title: str, body: str, author_id: int):
        await self.con.execute(f"INSERT INTO {ARTICLES} VALUES (?, ?, ?);", (title, body, author_id))

    async def get_article_by_title(self, title: str) -> Coroutine[Any, Any, Optional[Row]]:
        cursor = await self.con.execute(f"SELECT * FROM {ARTICLES} WHERE title=:title;", {"title": title})
        return cursor.fetchone()

    async def test_write_article(self):
        await self.write_article("제목", "내용", 1)
        await self.con.commit()

        article = await self.get_article_by_title("제목")

        assert article == (1, "제목", "내용")

    async def get_articles(self) -> Coroutine[Any, Any, Iterable[Row]]:
        cursor = await self.con.execute(f"SELECT * FROM {ARTICLES};")
        return cursor.fetchall()

    async def write_many_articles(self, articles: List[Tuple[str, str, int]]):
        await self.con.executemany(f"INSERT INTO {ARTICLES} VALUES (?, ?, ?);", articles)

    async def test_write_many_article(self):
        await self.write_many_articles([("제목", "내용", 1), ("title", "body", 1)])
        await self.con.commit()

        articles = await self.get_articles()

        assert articles == [(1, "제목", "내용"), (2, "title", "body")]

    async def get_article_with_author(self, title: str) -> Coroutine[Any, Any, Iterable[Row]]:
        cursor = await self.con.execute(f"""
            SELECT * FROM {ARTICLES}
            INNER JOIN {USER}
            ON {ARTICLES}.author={USER}.id
            WHERE title=:title;""", {"title": title})
        return cursor.fetchone()

    async def test_get_article_with_author(self):
        await self.write_article("제목", "내용", 1)
        await self.con.commit()

        article = await self.get_article_with_author("제목")

        assert article == (1, "제목", "내용", TEST_USER_NAME)
