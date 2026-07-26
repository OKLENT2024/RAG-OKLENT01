"""نقطة الدخول الرئيسية للنظام"""

import logging
from typing import List, Optional, Dict, Any
from loguru import logger
from src.config import config
from src.data_processor import DataProcessor
from src.embeddings import EmbeddingsManager
from src.retriever import Retriever
from src.generator import ResponseGenerator

# إعداد التسجيل
logger.add(
    config.LOGS_PATH / "rag_system.log",
    rotation="500 MB",
    retention="10 days",
    level=config.LOG_LEVEL,
)


class RAGSystem:
    """نظام الاسترجاع والتوليد المحسّن (RAG System)"""

    def __init__(
        self,
        use_pinecone: bool = False,
        embedding_model: Optional[str] = None,
        llm_model: Optional[str] = None,
    ):
        """تهيئة نظام RAG

        Args:
            use_pinecone: استخدام Pinecone بدلاً من FAISS
            embedding_model: نموذج التضمينات المراد استخدامه
            llm_model: نموذج اللغة المراد استخدامه
        """
        logger.info("جاري تهيئة نظام RAG...")

        self.use_pinecone = use_pinecone
        self.embedding_model = embedding_model or config.EMBEDDING_MODEL
        self.llm_model = llm_model or config.OPENAI_MODEL

        # تهيئة المكونات
        try:
            self.data_processor = DataProcessor(chunk_size=config.CHUNK_SIZE)
            logger.info("تم تهيئة معالج البيانات")

            self.embeddings_manager = EmbeddingsManager(
                model_name=self.embedding_model
            )
            logger.info(f"تم تهيئة مدير التضمينات: {self.embedding_model}")

            self.retriever = Retriever(
                embeddings_manager=self.embeddings_manager,
                use_pinecone=use_pinecone,
            )
            logger.info("تم تهيئة محرك البحث")

            self.generator = ResponseGenerator(model_name=self.llm_model)
            logger.info(f"تم تهيئة موليد الإجابات: {self.llm_model}")

            logger.info("✅ تم تهيئة نظام RAG بنجاح")

        except Exception as e:
            logger.error(f"❌ خطأ في تهيئة نظام RAG: {str(e)}")
            raise

    def add_documents(self, documents: List[str], metadata: Optional[List[Dict]] = None) -> None:
        """إضافة مستندات إلى النظام

        Args:
            documents: قائمة المستندات
            metadata: بيانات وصفية إضافية (اختيارية)
        """
        logger.info(f"جاري إضافة {len(documents)} مستند...")

        try:
            # معالجة المستندات
            chunks = self.data_processor.process_documents(documents)
            logger.info(f"تم معالجة {len(chunks)} قطعة من المستندات")

            # حساب التضمينات
            embeddings = self.embeddings_manager.get_embeddings(chunks)
            logger.info(f"تم حساب {len(embeddings)} تضمين")

            # إضافة إلى قاعدة البيانات المتجهة
            self.retriever.add_documents(chunks, embeddings, metadata)
            logger.info("✅ تمت إضافة المستندات بنجاح")

        except Exception as e:
            logger.error(f"❌ خطأ في إضافة المستندات: {str(e)}")
            raise

    def query(
        self,
        question: str,
        top_k: Optional[int] = None,
        language: Optional[str] = None,
    ) -> Dict[str, Any]:
        """الاستعلام عن السؤال والحصول على الإجابة

        Args:
            question: السؤال المراد الإجابة عليه
            top_k: عدد المستندات المراد استرجاعها
            language: اللغة المراد استخدامها

        Returns:
            قاموس يحتوي على الإجابة والمستندات ذات الصلة
        """
        logger.info(f"📝 استعلام جديد: {question}")

        try:
            top_k = top_k or config.TOP_K_RESULTS
            language = language or config.DEFAULT_LANGUAGE

            # البحث عن المستندات ذات الصلة
            relevant_docs = self.retriever.search(question, top_k=top_k)
            logger.info(f"تم استرجاع {len(relevant_docs)} مستند ذي صلة")

            # توليد الإجابة
            response = self.generator.generate(
                question=question,
                context_docs=relevant_docs,
                language=language,
            )

            logger.info("✅ تمت الإجابة بنجاح")

            return {
                "question": question,
                "answer": response,
                "relevant_documents": relevant_docs,
                "language": language,
            }

        except Exception as e:
            logger.error(f"❌ خطأ في معالجة الاستعلام: {str(e)}")
            raise

    def save_index(self, path: Optional[str] = None) -> None:
        """حفظ قاعدة البيانات المتجهة

        Args:
            path: المسار المراد حفظ الفهرس فيه
        """
        path = path or config.FAISS_INDEX_PATH
        logger.info(f"جاري حفظ الفهرس في: {path}")

        try:
            self.retriever.save_index(path)
            logger.info("✅ تم حفظ الفهرس بنجاح")
        except Exception as e:
            logger.error(f"❌ خطأ في حفظ الفهرس: {str(e)}")
            raise

    def load_index(self, path: Optional[str] = None) -> None:
        """تحميل قاعدة البيانات المتجهة

        Args:
            path: المسار المراد تحميل الفهرس منه
        """
        path = path or config.FAISS_INDEX_PATH
        logger.info(f"جاري تحميل الفهرس من: {path}")

        try:
            self.retriever.load_index(path)
            logger.info("✅ تم تحميل الفهرس بنجاح")
        except Exception as e:
            logger.error(f"❌ خطأ في تحميل الفهرس: {str(e)}")
            raise


def main():
    """تشغيل المثال الأساسي"""
    logger.info("=" * 50)
    logger.info("🚀 بدء نظام RAG")
    logger.info("=" * 50)

    try:
        # إنشاء نظام RAG
        rag = RAGSystem()

        # إضافة مستندات تجريبية
        sample_documents = [
            "Python هي لغة برمجة قوية وسهلة التعلم",
            "JavaScript تستخدم في تطوير تطبيقات الويب",
            "Machine Learning يتطلب كميات كبيرة من البيانات",
        ]

        rag.add_documents(sample_documents)

        # الاستعلام
        question = "ما هي لغات البرمجة الشهيرة؟"
        result = rag.query(question)

        logger.info(f"\n📝 السؤال: {result['question']}")
        logger.info(f"\n📢 الإجابة:\n{result['answer']}")

    except Exception as e:
        logger.error(f"خطأ في تشغيل البرنامج: {str(e)}")


if __name__ == "__main__":
    main()