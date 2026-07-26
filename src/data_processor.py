"""معالجة المستندات والبيانات"""

import re
from typing import List, Optional
from loguru import logger


class DataProcessor:
    """معالجة وتقسيم المستندات"""

    def __init__(
        self,
        chunk_size: int = 512,
        chunk_overlap: int = 50,
        language: str = "ar",
    ):
        """تهيئة معالج البيانات

        Args:
            chunk_size: حجم كل قطعة من المستند
            chunk_overlap: التداخل بين القطع
            language: اللغة المراد معالجتها
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.language = language
        logger.info(f"تم تهيئة معالج البيانات: chunk_size={chunk_size}, overlap={chunk_overlap}")

    def clean_text(self, text: str) -> str:
        """تنظيف النص من الأحرف غير المرغوبة

        Args:
            text: النص المراد تنظيفه

        Returns:
            النص المنظف
        """
        # إزالة المسافات الزائدة
        text = re.sub(r"\s+", " ", text).strip()
        # إزالة الأحرف الخاصة غير المهمة
        text = re.sub(r"[^\w\s.،؛:()\-]", "", text)
        return text

    def split_into_chunks(
        self, text: str, chunk_size: Optional[int] = None, overlap: Optional[int] = None
    ) -> List[str]:
        """تقسيم النص إلى قطع متساوية الحجم

        Args:
            text: النص المراد تقسيمه
            chunk_size: حجم القطعة
            overlap: التداخل بين القطع

        Returns:
            قائمة بقطع النص
        """
        chunk_size = chunk_size or self.chunk_size
        overlap = overlap or self.chunk_overlap

        chunks = []
        text_length = len(text)

        for i in range(0, text_length, chunk_size - overlap):
            chunk = text[i : i + chunk_size]
            if chunk.strip():
                chunks.append(chunk)

            if i + chunk_size >= text_length:
                break

        return chunks

    def process_documents(self, documents: List[str]) -> List[str]:
        """معالجة قائمة من المستندات

        Args:
            documents: قائمة المستندات

        Returns:
            قائمة بقطع المستندات المعالجة
        """
        processed_chunks = []

        logger.info(f"جاري معالجة {len(documents)} مستند...")

        for i, doc in enumerate(documents):
            try:
                # تنظيف المستند
                cleaned_doc = self.clean_text(doc)

                # تقسيم إلى قطع
                chunks = self.split_into_chunks(cleaned_doc)

                processed_chunks.extend(chunks)
                logger.debug(f"تمت معالجة المستند {i + 1}: {len(chunks)} قطعة")

            except Exception as e:
                logger.warning(f"خطأ في معالجة المستند {i + 1}: {str(e)}")
                continue

        logger.info(f"✅ تمت معالجة {len(processed_chunks)} قطعة من {len(documents)} مستند")

        return processed_chunks