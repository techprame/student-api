import os

from dotenv import load_dotenv

# Read settings from a .env file in the project root (if it exists)
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-secret-key-change-me-in-the-env-file")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./students.db")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
