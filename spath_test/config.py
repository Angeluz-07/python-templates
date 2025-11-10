# --- Configuration ---
# NOTE: In a real FastAPI application, you would load these values from environment variables
# or a configuration file (e.g., using Pydantic Settings).
MONGO_URI = "mongodb://fastapi_root_user:your_secure_root_password_123@localhost:27017/fastapi_app_db?authSource=admin"
DATABASE_NAME = "fastapi_app_db"
COLLECTION_NAME = "tasks"

# --- Configuration ---
# Connection details are pulled directly from your README.md and dev.env
# NOTE: In a real FastAPI app, you would load this from environment variables
POSTGRES_USER = "fastapi_user"
POSTGRES_PASSWORD = "secure_postgres_password_456"
POSTGRES_DB = "fastapi_postgres_db"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)