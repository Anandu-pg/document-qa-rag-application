from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    weaviate_url: str = "http://localhost:8080"
    ollama_base_url: str = "http://localhost:11434"
    llm_model: str = "llama3.2"
    embedding_model: str = "all-MiniLM-L6-v2"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
