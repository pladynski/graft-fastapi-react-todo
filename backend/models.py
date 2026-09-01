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

if db.is_closed():
    db.connect()
db.create_tables([Todo], safe=True)
