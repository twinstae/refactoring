from tortoise import fields, Tortoise
from tortoise.models import Model
from tortoise.utils import get_schema_sql
from pydantic_models import ArticleIn, UserIn
from services import ABService

DATABASE_URL = "sqlite://test.db"


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(16)
    articles = fields.ReverseRelation["Article"]

    def __repr__(self):
        return f"User(id={self.id}, name={self.name})"


class Article(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(128)
    body = fields.TextField()
    author = fields.ForeignKeyField('models.User', related_name="articles")

    def __repr__(self):
        return f"Article(id={self.id}, title={self.title}, body={self.body}, author={self.author!r})"


class TortoiseService(ABService):
    name = "tortoise"

    @classmethod
    async def setup(cls):
        await Tortoise.init(
            db_url=DATABASE_URL,
            modules={'models': ['services.tortoise_service']}
        )
        sql = get_schema_sql(Tortoise.get_connection("default"), safe=False)
        print(sql)
        await Tortoise.generate_schemas()

    @classmethod
    async def teardown(cls):
        await User.all().delete()
        await Tortoise.close_connections()

    @classmethod
    async def create_user(cls, user_in: UserIn) -> None:
        await User.create(**user_in.dict())
        # user_2 = User(**user_in.dict())
        # await user_2.save()

    @classmethod
    async def get_user_articles(cls, user_name: str):
        user = await User.get_or_none(name=user_name)
        articles = await Article.filter(author=user).prefetch_related('author')
        return articles or []

    @classmethod
    async def read_articles(cls):
        return await Article.all().prefetch_related('author')

    @classmethod
    async def create_article(cls, article: ArticleIn):
        user = await User.get_or_none(name=article.author_name)
        await Article.create(**article.dict(), author=user)

    @classmethod
    async def delete_all_articles(cls):
        await Article.all().delete()
