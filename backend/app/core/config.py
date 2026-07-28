from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://prasasti:prasasti@localhost:5432/prasasti"
    database_url_sync: str = "postgresql://prasasti:prasasti@localhost:5432/prasasti"
    face_engine: str = "facenet"
    face_embedding_dim: int = 512
    face_top_k: int = 5
    face_match_threshold: float = 0.6
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]
    upload_dir: str = "/tmp/prasasti/uploads"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
