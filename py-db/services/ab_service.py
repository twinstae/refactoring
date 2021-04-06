from abc import ABC, abstractmethod
from typing import List

from pydantic_models import ArticleOut, UserIn


class ABService(ABC):
    name = "서비스 자신의 이름"

    @classmethod
    @abstractmethod
    async def setup(cls) -> None:
        """
        1. 커넥션, 세션 등을 초기화한다
        2. 테이블을 생성한다
        """

    @classmethod
    @abstractmethod
    async def teardown(cls) -> None:
        """
        1. 모든 유저를 삭제한다
        2. 커넥션, 세션 등을 닫는다.
        """

    @classmethod
    @abstractmethod
    async def create_user(cls, user_in: UserIn) -> None:
        """
        UserIn 으로 유저를 생성한다
        """

    @classmethod
    @abstractmethod
    async def get_user_articles(cls, user_name: str):
        """
        user_name 으로 user 를 찾아서. 해당 유저가 쓴 모든 Article 을 가져온다.
        :return: List[Article, ArticleOut]
        """

    @classmethod
    @abstractmethod
    async def read_articles(cls):
        """
        모든 Article 을 Author 와 함께 조인해서 가져온다.
        :return: List[Article, ArticleOut]
        """

    @classmethod
    @abstractmethod
    async def create_article(cls) -> None:
        """
        author_name 으로 author 를 찾아서
        아티클을 생성한다.
        """

    @classmethod
    @abstractmethod
    async def delete_all_articles(cls) -> None:
        """
        모든 article 을 삭제한다
        """

