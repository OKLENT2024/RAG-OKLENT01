"""إعدادات المشروع الرئيسية"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()


class Config:
    """إعدادات المشروع الأساسية"""

    # معلومات المشروع
    PROJECT_NAME: str = "RAG-OKLENT01"
    PROJECT_VERSION: str = "0.1.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # المسارات
    BASE_DIR: Path = Path(__file__).parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    RAW_DATA_PATH: Path = Path(os.getenv("DATA_RAW_PATH", DATA_DIR / "raw"))
    PROCESSED_DATA_PATH: Path = Path(os.getenv("DATA_PROCESSED_PATH", DATA_DIR / "processed"))
    EMBEDDINGS_PATH: Path = Path(os.getenv("EMBEDDINGS_PATH", DATA_DIR / "embeddings"))
    MODELS_PATH: Path = BASE_DIR / "models"
    LOGS_PATH: Path = BASE_DIR / "logs"

    # إنشاء المجلدات إذا لم تكن موجودة
    @staticmethod
    def ensure_directories():
        """إنشاء المجلدات المطلوبة"""
        for path in [
            Config.RAW_DATA_PATH,
            Config.PROCESSED_DATA_PATH,
            Config.EMBEDDINGS_PATH,
            Config.MODELS_PATH,
            Config.LOGS_PATH,
        ]:
            path.mkdir(parents=True, exist_ok=True)

    # OpenAI API
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    OPENAI_MAX_TOKENS: int = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))

    # Hugging Face
    HUGGINGFACE_API_KEY: Optional[str] = os.getenv("HUGGINGFACE_API_KEY")
    EMBEDDING_MODEL: str = os.getenv(
        "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
    )

    # قاعدة البيانات المتجهة
    FAISS_INDEX_PATH: str = os.getenv("FAISS_INDEX_PATH", str(EMBEDDINGS_PATH / "faiss_index"))
    PINECONE_API_KEY: Optional[str] = os.getenv("PINECONE_API_KEY")
    PINECONE_ENVIRONMENT: str = os.getenv("PINECONE_ENVIRONMENT", "us-west1-gcp")
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "rag-index")

    # إعدادات النظام
    MAX_DOCUMENTS: int = int(os.getenv("MAX_DOCUMENTS", "10000"))
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "512"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "50"))

    # إعدادات البحث
    TOP_K_RESULTS: int = int(os.getenv("TOP_K_RESULTS", "5"))
    SIMILARITY_THRESHOLD: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.5"))

    # اللغات المدعومة
    DEFAULT_LANGUAGE: str = os.getenv("DEFAULT_LANGUAGE", "ar")
    SUPPORTED_LANGUAGES: list = os.getenv("SUPPORTED_LANGUAGES", "ar,en").split(",")

    @classmethod
    def get_config(cls) -> "Config":
        """الحصول على إعدادات المشروع"""
        cls.ensure_directories()
        return cls()


# إنشاء مثيل من الإعدادات
config = Config.get_config()