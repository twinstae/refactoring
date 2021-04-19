from services import TortoiseService, DatabasesService, AsyncpgService
from template import TestTemplate

# class AioSqliteTest(TestTemplate): 템플릿과 같다


class DatabasesTest(TestTemplate):
    service_name = DatabasesService.name


class TortoiseTest(TestTemplate):
    service_name = TortoiseService.name


class AsyncpgTest(TestTemplate):
    service_name = AsyncpgService.name
