"""مثال بسيط لاستخدام نظام RAG"""

from src.main import RAGSystem
from loguru import logger


def main():
    """تشغيل المثال الأساسي"""

    logger.info("=" * 60)
    logger.info("🚀 مثال بسيط لاستخدام نظام RAG")
    logger.info("=" * 60)

    # إنشاء نظام RAG
    rag = RAGSystem()

    # مستندات تجريبية
    documents = [
        "Python هي لغة برمجة قوية وسهلة التعلم، تستخدم على نطاق واسع في تطوير التطبيقات",
        "JavaScript هي لغة برمجة تعمل في المتصفحات والخوادم، وهي أساسية لتطوير مواقع الويب",
        "Java هي لغة برمجة موجهة للكائنات، تستخدم في تطوير التطبيقات الكبيرة والأنظمة الموزعة",
        "Machine Learning هو فرع من الذكاء الاصطناعي يركز على تدريب الآلات على التعلم من البيانات",
        "قواعد البيانات هي أنظمة منظمة تخزن وتدير البيانات بكفاءة وأمان",
    ]

    # إضافة المستندات
    logger.info("\n📝 جاري إضافة المستندات...")
    rag.add_documents(documents)

    # الاستعلامات التجريبية
    queries = [
        "ما هي لغات البرمجة الشهيرة؟",
        "كيف يعمل Machine Learning؟",
        "ما هي استخدامات قواعد البيانات؟",
    ]

    # الإجابة عن الأسئلة
    logger.info("\n" + "=" * 60)
    for i, query in enumerate(queries, 1):
        logger.info(f"\n❓ السؤال {i}: {query}")
        logger.info("-" * 60)

        result = rag.query(query)

        logger.info(f"\n💬 الإجابة:\n{result['answer']}")
        logger.info(f"\n📚 المستندات ذات الصلة: {len(result['relevant_documents'])}")

        for j, doc in enumerate(result["relevant_documents"], 1):
            logger.info(
                f"   {j}. التشابه: {doc['similarity']:.2%} - {doc['document'][:50]}..."
            )

        logger.info("-" * 60)

    logger.info("\n✅ انتهى المثال")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
