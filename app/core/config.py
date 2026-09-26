from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str = ""
    llm_model: str = "gpt-4o-mini"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    top_k: int = 6
    chunk_size: int = 800
    chunk_overlap: int = 120
    max_history_turns: int = 6
    data_dir: str = "data"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def root(self) -> Path:
        return Path(self.data_dir)

    @property
    def upload_dir(self) -> Path:
        return self.root / "uploads"

    @property
    def index_dir(self) -> Path:
        return self.root / "index"


settings = Settings()
settings.upload_dir.mkdir(parents=True, exist_ok=True)
settings.index_dir.mkdir(parents=True, exist_ok=True)
