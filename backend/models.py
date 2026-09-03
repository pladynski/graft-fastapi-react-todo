# Graftcode: Peewee Todo model unchanged. Import-time DB init was removed; startup is main.Lifespan.startup (--initMethod).
# FastAPI is gone — remote methods are local. Same methods are MCP; copy the config from Graftcode Vision.
# https://graftcode.com · https://github.com/grft-dev/graftcode · https://docs.graftcode.com

from peewee import *
from config.environment import DATABASE_PATH

# Database setup
db = SqliteDatabase(DATABASE_PATH)

class Todo(Model):
    id = AutoField()
    title = CharField()
    description = TextField(default='')
    completed = BooleanField(default=False)

    class Meta:
        database = db
