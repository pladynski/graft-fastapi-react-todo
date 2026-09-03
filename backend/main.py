# Graftcode: FastAPI app, routes, and CORSMiddleware deleted. Lifespan.startup is gg --initMethod (connect sqlite + create_tables).
# Benefit: process startup without standing up a REST app.
# https://graftcode.com · https://github.com/grft-dev/graftcode · https://docs.graftcode.com

from models import db, Todo


def get_database():
    return db


class Lifespan:
    """Process bootstrap analog of the original FastAPI lifespan startup."""

    @staticmethod
    def startup():
        current_db = get_database()
        if current_db.is_closed():
            current_db.connect()
        current_db.create_tables([Todo], safe=True)
