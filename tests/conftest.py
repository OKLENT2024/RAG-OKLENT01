"""إعدادات pytest المشتركة"""

import pytest
from src.config import config
from src.data_processor import DataProcessor
from src.embeddings import EmbeddingsManager


@pytest.fixture
def sample_documents():
    """مستندات تجريبية"""
    return [
        "Python هي لغة برمجة قوية",
        "JavaScript تستخدم في تطوير الويب",
        "Machine Learning يتطلب بيانات كثيرة",
    ]


@pytest.fixture
def data_processor():
    """معالج البيانات"""
    return DataProcessor(chunk_size=512)


@pytest.fixture
def embeddings_manager():
    """مدير التضمينات"""
    return EmbeddingsManager(model_name="sentence-transformers/all-MiniLM-L6-v2")