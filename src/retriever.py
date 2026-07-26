"""محرك البحث واسترجاع المستندات"""

import os
from typing import List, Optional, Dict, Any
from loguru import logger

try:
    import faiss
except ImportError:
    logger.warning("FAISS غير مثبتة. بعض الميزات قد لا تعمل.")

from src.embeddings import EmbeddingsManager


class Retriever:
    """محرك البحث واسترجاع المستندات"""

    def __init__(
        self,
        embeddings_manager: EmbeddingsManager,
        use_pinecone: bool = False,
        index_path: Optional[str] = None,
    ):
        """تهيئة محرك البحث

        Args:
            embeddings_manager: مدير التضمينات
            use_pinecone: استخدام Pinecone بدلاً من FAISS
            index_path: مسار الفهرس
        """
        self.embeddings_manager = embeddings_manager
        self.use_pinecone = use_pinecone
        self.index_path = index_path
        self.documents = []  # تخزين المستندات الأصلية
        self.index = None

        if use_pinecone:
            logger.info("استخدام Pinecone كقاعدة بيانات متجهة")
            self._init_pinecone()
        else:
            logger.info("استخدام FAISS كقاعدة بيانات متجهة")
            self._init_faiss()

    def _init_faiss(self):
        """تهيئة FAISS"""
        try:
            dimension = self.embeddings_manager.get_dimension()
            self.index = faiss.IndexFlatL2(dimension)
            logger.info(f"✅ تم تهيئة FAISS بنجاح (البعد: {dimension})")
        except Exception as e:
            logger.error(f"❌ خطأ في تهيئة FAISS: {str(e)}")
            raise

    def _init_pinecone(self):
        """تهيئة Pinecone"""
        logger.info("جاري تهيئة Pinecone...")
        # سيتم تنفيذه لاحقاً
        pass

    def add_documents(
        self,
        documents: List[str],
        embeddings,
        metadata: Optional[List[Dict]] = None,
    ) -> None:
        """إضافة مستندات إلى قاعدة البيانات

        Args:
            documents: قائمة المستندات
            embeddings: التضمينات
            metadata: البيانات الوصفية
        """
        logger.info(f"جاري إضافة {len(documents)} مستند إلى الفهرس...")

        try:
            self.documents.extend(documents)
            self.index.add(embeddings.astype("float32"))
            logger.info(f"✅ تمت إضافة {len(documents)} مستند")
        except Exception as e:
            logger.error(f"❌ خطأ في إضافة المستندات: {str(e)}")
            raise

    def search(
        self, query: str, top_k: int = 5, threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """البحث عن المستندات ذات الصلة

        Args:
            query: الاستعلام
            top_k: عدد النتائج
            threshold: حد التشابه

        Returns:
            قائمة بالمستندات ذات الصلة
        """
        logger.info(f"جاري البحث عن: '{query}'")

        try:
            # حساب تضمين الاستعلام
            query_embedding = self.embeddings_manager.get_single_embedding(query)

            # البحث في الفهرس
            distances, indices = self.index.search(
                query_embedding.reshape(1, -1).astype("float32"), top_k
            )

            results = []
            for i, idx in enumerate(indices[0]):
                if idx < len(self.documents):
                    distance = distances[0][i]
                    similarity = 1 / (1 + distance)  # تحويل المسافة إلى تشابه

                    if similarity >= threshold:
                        results.append(
                            {
                                "document": self.documents[idx],
                                "similarity": float(similarity),
                                "index": int(idx),
                            }
                        )

            logger.info(f"✅ تم العثور على {len(results)} مستند ذي صلة")
            return results

        except Exception as e:
            logger.error(f"❌ خطأ في البحث: {str(e)}")
            raise

    def save_index(self, path: str) -> None:
        """حفظ الفهرس

        Args:
            path: مسار الحفظ
        """
        logger.info(f"جاري حفظ الفهرس في: {path}")

        try:
            if self.use_pinecone:
                logger.info("Pinecone يحفظ تلقائياً")
            else:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                faiss.write_index(self.index, path)
                logger.info(f"✅ تم حفظ الفهرس")
        except Exception as e:
            logger.error(f"❌ خطأ في حفظ الفهرس: {str(e)}")
            raise

    def load_index(self, path: str) -> None:
        """تحميل الفهرس

        Args:
            path: مسار الفهرس
        """
        logger.info(f"جاري تحميل الفهرس من: {path}")

        try:
            self.index = faiss.read_index(path)
            logger.info(f"✅ تم تحميل الفهرس")
        except Exception as e:
            logger.error(f"❌ خطأ في تحميل الفهرس: {str(e)}")
            raise