from django.apps import AppConfig

REPAIR_URL_HOST = "REPAIR_URL_HOST"
REPAIR_DETAIL_URL = "REPAIR_DETAIL_URL"


class RepairScrapyConfig(AppConfig):
    name = 'repair_scrapy'
    REPAIR_URL_HOST = 'http://10.128.20.119:8080'
