from services import TortoiseService, DatabasesService
from template import TestTemplate

# class AioSqliteTest(TestTemplate): 템플릿과 같다


class DatabasesTest(TestTemplate):
    service_name = DatabasesService.name


class TortoiseTest(TestTemplate):
    service_name = TortoiseService.name
