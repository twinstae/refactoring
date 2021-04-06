from unittest import TestCase
from starlette.testclient import TestClient
from app import app
from services import AioSqliteService

USER_1 = {"name": "테스트유저"}
USER_2 = {"name": "test-user-2"}
ARTICLE_1 = {"title": "제목", "body": "내용"}
ARTICLE_2 = {"title": "title", "body": "body"}
ARTICLE_1_WITH_AUTHOR = {'author': {'name': USER_1["name"]}, **ARTICLE_1}
ARTICLE_2_WITH_AUTHOR = {'author': {'name': USER_1["name"]}, **ARTICLE_2}


class TestTemplate(TestCase):
    client = TestClient(app)
    service_name = AioSqliteService.name

    @classmethod
    def setUpClass(cls) -> None:
        cls.client.post("/setup/"+cls.service_name)
        cls.client.post("/users/", json=USER_1)
        cls.client.post("/users/", json=USER_2)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.client.delete("/teardown/")

    def tearDown(self) -> None:
        self.client.delete("/articles/")

    def create_article(self, article, author_name: str = USER_1["name"]):
        self.client.post("/articles/", json={"author_name": author_name, **article})

    def test_write_many_articles(self):
        self.create_article(ARTICLE_1)
        self.create_article(ARTICLE_2)

        response = self.client.get("/articles/")
        result = response.json()
        consistency_check(result, [ARTICLE_1_WITH_AUTHOR, ARTICLE_2_WITH_AUTHOR])

    def test_get_user_articles(self):
        self.create_article(ARTICLE_1)
        self.create_article(ARTICLE_1, author_name=USER_2["name"])

        response = self.client.get(f"/users/{USER_1['name']}/articles/")
        result = response.json()
        consistency_check(result, [ARTICLE_1_WITH_AUTHOR])


def consistency_check(result, expected):
    print("")
    for r, e in zip(result, expected):
        print(r)
        for key in ['title', 'body']:
            assert r[key] == e[key]
        assert r['author']['name'] == e['author']['name']



