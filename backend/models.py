# Graftcode: Peewee Todo fields unchanged. Only removed import-time connect/create_tables (now Lifespan.startup).
# Benefit: the model stayed; we did not invent a new persistence shape.
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
