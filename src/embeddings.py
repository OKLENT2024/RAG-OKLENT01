"""مدير التضمينات والنماذج"""

import numpy as np
from typing import List
from loguru import logger

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    logger.warning("sentence-transformers غير مثبتة. بعض الميزات قد لا تعمل.")


class EmbeddingsManager:
    """إدارة حساب التضمينات"""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """تهيئة مدير التضمينات

        Args:
            model_name: اسم نموذج التضمينات
        """
        self.model_name = model_name
        logger.info(f"جاري تحميل نموذج التضمينات: {model_name}")

        try:
            self.model = SentenceTransformer(model_name)
            self.embedding_dimension = self.model.get_sentence_embedding_dimension()
            logger.info(
                f"✅ تم تحميل النموذج بنجاح. البعد: {self.embedding_dimension}"
            )
        except Exception as e:
            logger.error(f"❌ خطأ في تحميل النموذج: {str(e)}")
            raise

    def get_embeddings(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """حساب التضمينات للنصوص

        Args:
            texts: قائمة النصوص
            batch_size: حجم الدفعة

        Returns:
            مصفوفة numpy بالتضمينات
        """
        logger.info(f"جاري حساب التضمينات لـ {len(texts)} نص...")

        try:
            embeddings = self.model.encode(
                texts, batch_size=batch_size, show_progress_bar=True
            )
            logger.info(f"✅ تم حساب {len(embeddings)} تضمين")
            return embeddings

        except Exception as e:
            logger.error(f"❌ خطأ في حساب التضمينات: {str(e)}")
            raise

    def get_single_embedding(self, text: str) -> np.ndarray:
        """حساب التضمين لنص واحد

        Args:
            text: النص

        Returns:
            مصفوفة numpy بالتضمين
        """
        try:
            embedding = self.model.encode([text])
            return embedding[0]
        except Exception as e:
            logger.error(f"❌ خطأ في حساب التضمين: {str(e)}")
            raise

    def get_dimension(self) -> int:
        """الحصول على بعد التضمينات

        Returns:
            البعد
        """
        return self.embedding_dimension