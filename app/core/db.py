from tortoise import Tortoise
from app.core.settings import settings


TORTOISE_ORM = {
    "connections": {
        "default": f"sqlite://{settings.sqlite_path}"
    },
    "apps": {
        "models": {
            "models": [
                "app.schemas.application",
                "app.schemas.event",
            ],
            "default_connection": "default",
        }
    },
}


async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()


async def close_db():
    await Tortoise.close_connections()

