import logging.config
from time import sleep

from grandid.client import BankIDClient

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {"format": "%(levelname)-8s %(name)-25s %(lineno)-6d %(message)s"},
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "default",
            }
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["console"],
        },
    }
)
logger = logging.getLogger(__name__)

APIKEY = ""
AUTHENTICATESERVICEKEY = ""

client = BankIDClient(APIKEY, AUTHENTICATESERVICEKEY)

response = client.authenticate(personalNumber="", gui=False)
logger.debug(response)
sessionId = response["sessionId"]
logger.debug(sessionId)

for i in range(1, 10):
    sleep(2)
    response = client.collect(sessionId)
    logger.debug(response)
    if "sessionId" in response:
        break
