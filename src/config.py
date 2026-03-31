import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    EMBEDDING_MODEL: str = "text-embedding-3-small"
    EMBEDDING_DIMENSIONS: int = 1536

    CHROMA_PERSIST_DIR: str = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "data", "chroma"
    )
    CHROMA_COLLECTION_NAME: str = "enterprise_docs"

    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    APP_ENV: str = os.getenv("APP_ENV", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "DEBUG")
    
    # __file__ = lokasi file config.py ini
    # os.path.dirname = ambil folder-nya
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_RAW_DIR: str = os.path.join(BASE_DIR, "data", "raw")
    DATA_PROCESSED_DIR: str = os.path.join(BASE_DIR, "data", "processed")
    
    def validate(self):
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY hasn't been set in .env!")
        print("All configs are valid.")

config = Config()