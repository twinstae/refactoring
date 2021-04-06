from abc import ABC, abstractmethod
from typing import List

from pydantic_models import ArticleOut


class ABService(ABC):
    name = "서비스 자신의 이름"

    @classmethod
    @abstractmethod
    async def setup(cls) -> None:
        """
        1. 커넥션, 세션 등을 초기화한다
        2. 테이블을 생성한다
        3. User1을 추가한다 -> 분리 예정
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
    async def read_articles(cls) -> List[ArticleOut]:
        """
        :return: 모든 Article 을 Author 와 함께 조인해서 가져오고,
        pydantic 모델로 반환한다.
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

