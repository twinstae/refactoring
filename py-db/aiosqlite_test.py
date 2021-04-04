import aiosqlite
from sqlite3 import Row
from typing import List, Tuple, Coroutine, Any, Iterable, Optional
from unittest import TestCase

ARTICLES = "ARTICLES"


class Sqlite3Test(TestCase):
    con = aiosqlite.connect(':memory:')

    @classmethod
    def setUpClass(cls) -> None:
        cls.con.execute(f'''CREATE TABLE {ARTICLES} (title text, body text);''')

    def tearDown(self) -> None:
        self.con.execute(f'''DELETE FROM {ARTICLES}''')
        self.con.commit()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.con.close()

    async def write_article(self, title, body):
        await self.con.execute(f"INSERT INTO {ARTICLES} VALUES (?, ?);", (title, body))

    async def get_articles(self) -> Coroutine[Any, Any, Iterable[Row]]:
        cursor = await self.con.execute(f"SELECT * FROM {ARTICLES};")
        return cursor.fetchall()

    async def test_write_article(self):
        await self.write_article("제목", "내용")
        await self.con.commit()

        article = await self.get_article_by_title("제목")

        assert article == ("제목", "내용")

    async def write_many_articles(self, articles: List[Tuple[str, str]]):
        await self.con.executemany(f"INSERT INTO {ARTICLES} VALUES (?, ?);", articles)

    async def test_write_many_article(self):
        await self.write_many_articles([("제목", "내용"), ("title", "body")])
        await self.con.commit()

        articles = await self.get_articles()

        assert articles == [("제목", "내용"), ("title", "body")]

    async def get_article_by_title(self, title) -> Coroutine[Any, Any, Optional[Row]]:
        cursor = await self.con.execute(f"SELECT * FROM {ARTICLES} WHERE title=:title;", {"title": title})
        return cursor.fetchone()
