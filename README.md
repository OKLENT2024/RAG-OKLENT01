# RAG System - RYD26

##  (RAG)

نظام متكامل لاسترجاع المعلومات وتوليد الإجابات الذكية باستخدام نماذج اللغة الكبيرة.

---

## 📋 نظرة عامة على المشروع

هذا المشروع يبني نظام RAG قادر على:
- 📄 معالجة ملايين المستندات
- 🔍 البحث السريع عن المستندات المشابهة
- 🤖 توليد إجابات دقيقة بناءً على المستندات المسترجعة
- 🌐 دعم لغات متعددة (العربية والإنجليزية)

---

## 🏗️ العمارة (Architecture)

انظر `docs/ARCHITECTURE.md` للتفاصيل الكاملة

---

## 🚀 البدء السريع

### المتطلبات
- Python 3.8+
- pip أو conda

### التثبيت

```bash
# استنساخ المستودع
git clone https://github.com/OKLENT2024/RAG-OKLENT01.git
cd RAG-OKLENT01

# إنشاء بيئة افتراضية
python -m venv venv
source venv/bin/activate  # في Linux/Mac
venv\Scripts\activate     # في Windows

# تثبيت المكتبات
pip install -r requirements.txt

# تعيين متغيرات البيئة
cp .env.example .env
```

### التشغيل

```bash
# تشغيل النظام
python src/main.py

# تشغيل الاختبارات
pytest tests/
```

---

## 📁 هيكل المشروع

```
RAG-OKLENT01/
├── src/                    # الكود الرئيسي
├── data/                   # البيانات
├── tests/                  # الاختبارات
├── docs/                   # التوثيق
├── examples/               # أمثلة
├── README.md              # هذا الملف
├── requirements.txt       # المكتبات
└── .env.example          # متغيرات البيئة
```

---

## 💡 الاستخدام

```python
from src.main import RAGSystem

# إنشاء النظام
rag = RAGSystem()

# إضافة مستندات
rag.add_documents([
    "Python هي لغة برمجة قوية",
    "JavaScript تستخدم في تطوير الويب"
])

# الاستعلام
result = rag.query("ما هي لغات البرمجة الشهيرة؟")
print(result['answer'])
```

---

## 🤝 المساهمة

نرحب بالمساهمات! انظر المشاكل والطلبات المفتوحة.

---

## 📝 الترخيص

MIT License

---

**آخر تحديث**: 2026-07-26
