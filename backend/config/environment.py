# Graftcode: CORS origin lists removed (compose DEVELOPMENT_ORIGINS → gg --corsAllowedOrigins). DB/host settings stayed.
# FastAPI is fully removed; remote methods are called like local ones. Same methods are MCP — copy the config from Graftcode Vision.
# https://graftcode.com · https://github.com/grft-dev/graftcode · https://docs.graftcode.com

import os
import tempfile

# Environment constants
APP_ENV = os.getenv("APP_ENV", "development")

# Database paths
DEVELOPMENT_DB_PATH = "todos_development.sqlite"
TEST_DB_PATH = os.path.join(tempfile.gettempdir(), "todos_test.sqlite")
PRODUCTION_DB_PATH = "todos_production.sqlite"

# Server configuration
DEVELOPMENT_HOST = "0.0.0.0"
DEVELOPMENT_PORT = 8000
TEST_HOST = "0.0.0.0"
TEST_PORT = 8001
PRODUCTION_HOST = "0.0.0.0"
PRODUCTION_PORT = 8000

# Environment-based configuration
if APP_ENV == "test":
    DATABASE_PATH = TEST_DB_PATH
    SERVER_HOST = TEST_HOST
    SERVER_PORT = TEST_PORT
    APP_TITLE = "Todo API - Test"
    RELOAD = False
elif APP_ENV == "production":
    DATABASE_PATH = PRODUCTION_DB_PATH
    SERVER_HOST = PRODUCTION_HOST
    SERVER_PORT = PRODUCTION_PORT
    APP_TITLE = "Todo API - Production"
    RELOAD = False
else:  # Default to development
    DATABASE_PATH = DEVELOPMENT_DB_PATH
    SERVER_HOST = DEVELOPMENT_HOST
    SERVER_PORT = DEVELOPMENT_PORT
    APP_TITLE = "Todo API"
    RELOAD = True

DATABASE_PATH = os.getenv("DATABASE_PATH", DATABASE_PATH)
