from unittest import TestCase

from starlette.testclient import TestClient
from app import app


TEST_USER_NAME = "테스트유저"

ARTICLE_1 = {"title": "제목", "body": "내용"}
ARTICLE_2 = {"title": "title", "body": "body"}
ARTICLE_1_WITH_AUTHOR = {'author': {'name': TEST_USER_NAME}, **ARTICLE_1}
ARTICLE_2_WITH_AUTHOR = {'author': {'name': TEST_USER_NAME}, **ARTICLE_2}


class TestTemplate(TestCase):
    client = TestClient(app)
    service_name = "aiosqlite"

    @classmethod
    def setUpClass(cls) -> None:
        cls.client.post("/setup/"+cls.service_name)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.client.delete("/teardown/")

    def tearDown(self) -> None:
        self.client.delete("/articles/")

    def test_write_article(self):
        self.client.post("/articles/", json={"author_name": TEST_USER_NAME, **ARTICLE_1})

        response = self.client.get("/articles/")
        result = response.json()
        consistency_check(result, [ARTICLE_1_WITH_AUTHOR])

    def test_write_many_articles(self):
        self.client.post("/articles/", json={"author_name": TEST_USER_NAME, **ARTICLE_1})
        self.client.post("/articles/", json={"author_name": TEST_USER_NAME, **ARTICLE_2})

        response = self.client.get("/articles/")
        result = response.json()
        consistency_check(result, [ARTICLE_1_WITH_AUTHOR, ARTICLE_2_WITH_AUTHOR])


def consistency_check(result, expected):
    print("")
    for r, e in zip(result, expected):
        print(r)
        for key in ['title', 'body']:
            assert r[key] == e[key]
        assert r['author']['name'] == e['author']['name']