from pydantic import BaseModel


class UserIn(BaseModel):
    name: str


class UserOut(BaseModel):
    id: int
    name: str


class ArticleIn(BaseModel):
    title: str
    body: str
    author_name: str


class ArticleOut(BaseModel):
    id: int
    title: str
    body: str
    author: UserOut
