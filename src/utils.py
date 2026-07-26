"""دوال مساعدة وأدوات عامة"""

import json
import os
from typing import Any, Dict, List
from pathlib import Path
from loguru import logger


def save_json(data: Dict[str, Any], file_path: str) -> None:
    """حفظ بيانات JSON إلى ملف

    Args:
        data: البيانات
        file_path: مسار الملف
    """
    try:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"✅ تم حفظ البيانات في: {file_path}")
    except Exception as e:
        logger.error(f"❌ خطأ في حفظ البيانات: {str(e)}")
        raise


def load_json(file_path: str) -> Dict[str, Any]:
    """تحميل بيانات JSON من ملف

    Args:
        file_path: مسار الملف

    Returns:
        البيانات المحملة
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"✅ تم تحميل البيانات من: {file_path}")
        return data
    except Exception as e:
        logger.error(f"❌ خطأ في تحميل البيانات: {str(e)}")
        raise