from services import TortoiseService, AioSqliteService, DatabasesService
from template import TestTemplate


class AioSqliteTest(TestTemplate):
    service_name = AioSqliteService.name


class TortoiseTest(TestTemplate):
    service_name = TortoiseService.name


class DatabasesTest(TestTemplate):
    service_name = DatabasesService.name
