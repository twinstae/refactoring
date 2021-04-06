from tortoise.models import Model
from tortoise import fields, Tortoise
from pydantic_models import ArticleIn
from services import ABService

name = "tortoise"

DATABASE_URL = "sqlite://test.db"
USER_1 = {"name": "테스트유저"}


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(16)


class Article(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(128)
    body = fields.TextField()
    author = fields.ForeignKeyField('models.User')


class TortoiseService(ABService):
    name = "tortoise"

    @classmethod
    async def setup(cls):
        await Tortoise.init(
            db_url='sqlite://:memory:',
            modules={'models': ['services.tortoise_service']}
        )
        await Tortoise.generate_schemas()

        await User.create(**USER_1)

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

    @classmethod
    async def teardown(cls):
        await User.all().delete()
        await Tortoise.close_connections()
