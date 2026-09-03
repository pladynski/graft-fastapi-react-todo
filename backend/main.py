# Graftcode: FastAPI app/routes gone. Lifespan.startup is gg --initMethod (the old lifespan DB bootstrap: connect + create_tables).
# No integration method — remote methods are local calls. Same methods are MCP; copy the config from Graftcode Vision.
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
