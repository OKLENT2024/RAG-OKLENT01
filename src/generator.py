"""موليد الإجابات باستخدام نماذج اللغة"""

from typing import List, Optional, Dict, Any
from loguru import logger

try:
    import openai
except ImportError:
    logger.warning("openai غير مثبتة. بعض الميزات قد لا تعمل.")

from src.config import config


class ResponseGenerator:
    """موليد الإجابات"""

    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        """تهيئة موليد الإجابات

        Args:
            model_name: اسم نموذج اللغة
        """
        self.model_name = model_name

        if config.OPENAI_API_KEY:
            openai.api_key = config.OPENAI_API_KEY
            logger.info(f"✅ تم تكوين OpenAI API")
        else:
            logger.warning("⚠️ لم يتم تعيين OPENAI_API_KEY")

    def generate(
        self,
        question: str,
        context_docs: List[Dict[str, Any]],
        language: str = "ar",
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """توليد إجابة بناءً على السؤال والمستندات ذات الصلة

        Args:
            question: السؤال
            context_docs: المستندات ذات الصلة
            language: اللغة
            temperature: درجة الحرارة للنموذج
            max_tokens: الحد الأقصى للرموز

        Returns:
            الإجابة الموليدة
        """
        logger.info(f"جاري توليد إجابة للسؤال: {question}")

        try:
            temperature = temperature or config.OPENAI_TEMPERATURE
            max_tokens = max_tokens or config.OPENAI_MAX_TOKENS

            # بناء السياق من المستندات
            context = self._build_context(context_docs)

            # بناء الرسالة
            system_prompt = self._get_system_prompt(language)
            user_message = self._build_user_message(question, context, language)

            # استدعاء OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )

            answer = response["choices"][0]["message"]["content"]
            logger.info("✅ تمت توليد الإجابة بنجاح")
            return answer

        except Exception as e:
            logger.error(f"❌ خطأ في توليد الإجابة: {str(e)}")
            # إرجاع رسالة افتراضية في حالة الخطأ
            return f"عذراً، حدث خطأ في معالجة سؤالك. الخطأ: {str(e)}"

    def _build_context(self, context_docs: List[Dict[str, Any]]) -> str:
        """بناء سياق من المستندات

        Args:
            context_docs: المستندات

        Returns:
            النص السياقي
        """
        if not context_docs:
            return "لا توجد مستندات ذات صلة."

        context_parts = []
        for i, doc in enumerate(context_docs, 1):
            context_parts.append(
                f"المستند {i} (التشابه: {doc.get('similarity', 0):.2%}):\n{doc.get('document', '')}"
            )

        return "\n\n".join(context_parts)

    def _get_system_prompt(self, language: str = "ar") -> str:
        """الحصول على رسالة النظام

        Args:
            language: اللغة

        Returns:
            رسالة النظام
        """
        if language == "ar":
            return (
                "أنت مساعد ذكي متخصص في الإجابة عن الأسئلة بناءً على المستندات المتاحة. "
                "قدم إجابات دقيقة وواضحة ومفيدة باللغة العربية. "
                "إذا لم تتمكن من العثور على إجابة في المستندات، فأخبر المستخدم بذلك."
            )
        else:
            return (
                "You are an intelligent assistant specialized in answering questions based on provided documents. "
                "Provide accurate, clear, and helpful answers in English. "
                "If you cannot find an answer in the documents, inform the user."
            )

    def _build_user_message(self, question: str, context: str, language: str = "ar") -> str:
        """بناء رسالة المستخدم

        Args:
            question: السؤال
            context: السياق
            language: اللغة

        Returns:
            رسالة المستخدم
        """
        if language == "ar":
            return (
                f"بناءً على المستندات التالية، أجب على السؤال:\n\n"
                f"المستندات:\n{context}\n\n"
                f"السؤال: {question}\n\n"
                f"الإجابة:"
            )
        else:
            return (
                f"Based on the following documents, answer the question:\n\n"
                f"Documents:\n{context}\n\n"
                f"Question: {question}\n\n"
                f"Answer:"
            )