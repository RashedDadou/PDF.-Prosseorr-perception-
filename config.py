# config.py

import os
from pathlib import Path
from typing import Dict, Any, Optional

class SovereignConfig:
    """
    [الإعدادات السيادية] - مركز التحكم في كل إعدادات Sovereign Engine
    """

    # ====================== Debug Settings ======================
    DEBUG_MODE: bool = True
    DEBUG_PRINT_SAMPLE_TEXT: bool = True
    DEBUG_SAMPLE_LENGTH: int = 450
    DEBUG_HIGH_NUMBER_PAGES_ONLY: bool = False

    # ====================== مسارات النظام ======================
    BASE_DIR = Path(__file__).parent
    REPORTS_DIR = BASE_DIR / "reports"
    LOGS_DIR = BASE_DIR / "logs"
    ARCHIVE_DIR = BASE_DIR / "archive"
    CACHE_DIR = BASE_DIR / "cache"

    # ====================== إعدادات المصفوفات (H-Point Optimized) ======================
    MATRIX_REPAIR_ENABLED: bool = True
    MATRIX_MIN_QUALITY_THRESHOLD: float = 21.0      # خفض للكتب التقنية
    MATRIX_ACCEPTANCE_TOLERANCE: float = 12.0

    # إعدادات LLM Repair
    MATRIX_REPAIR_MODEL: str = "gpt-4o-mini"
    LLM_TEMPERATURE: float = 0.0
    LLM_MAX_TOKENS: int = 1100
    LLM_TOP_P: float = 0.95

    MATRIX_REPAIR_SYSTEM_PROMPT: str = (
        "أنت خبير عالي الدقة في مصفوفات التحويل المتجانسة 4x4 (Homogeneous Transformation Matrices) "
        "في مجال تصميم السيارات و H-Point. أعد بناء المصفوفة بدقة حتى لو كان النص تالفاً من OCR."
    )

    # ====================== إعدادات المعالجة ======================
    DEFAULT_DOMAIN: str = "Vehicle_Design"
    MAX_PAGES_TO_PROCESS: int = 9999
    TEXT_CLEANING_ENABLED: bool = True

    # عتبات الإدراك
    PERCEPTION_HIGH_THRESHOLD: int = 68
    PERCEPTION_MEDIUM_THRESHOLD: int = 42

    # Aggressive Detection
    AGGRESSIVE_MATRIX_DETECTION: bool = True
    MIN_NUMBERS_FOR_CANDIDATE: int = 10

    # ====================== Vector Store & Embedding ======================
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    SIMILARITY_MIN_SCORE: float = 0.35
    VECTOR_CACHE_ENABLED: bool = True

    # ====================== Logging ======================
    LOG_LEVEL: str = "INFO"          # غيّر إلى DEBUG للتشخيص
    LOG_TO_FILE: bool = True
    LOG_TO_CONSOLE: bool = True

    # ====================== Performance ======================
    MAX_CANDIDATES_PER_PAGE: int = 35
    MAX_WORKERS: int = 6
    ENABLE_LLM_REPAIR_ON_LOW_QUALITY: bool = True

    # ====================== OpenAI Settings ======================
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")   # يمكن تجاوزه من env

    # ====================== Cache Settings ======================
    MAX_CACHE_SIZE: int = 500

    @classmethod
    def create_directories(cls):
        """إنشاء جميع المجلدات المطلوبة"""
        for directory in [cls.REPORTS_DIR, cls.LOGS_DIR, cls.ARCHIVE_DIR, cls.CACHE_DIR]:
            directory.mkdir(parents=True, exist_ok=True)

    @classmethod
    def get_config_dict(cls) -> Dict[str, Any]:
        """إرجاع جميع الإعدادات كقاموس"""
        config_dict = {}
        for attr in dir(cls):
            if not attr.startswith("_") and not callable(getattr(cls, attr)):
                value = getattr(cls, attr)
                # تجنب كائنات Path في الـ dict
                if isinstance(value, Path):
                    value = str(value)
                config_dict[attr] = value
        return config_dict

    @classmethod
    def update(cls, **kwargs):
        """تحديث الإعدادات ديناميكياً"""
        for key, value in kwargs.items():
            if hasattr(cls, key):
                setattr(cls, key, value)
            else:
                print(f"⚠️ Warning: Unknown config key '{key}'")


# ====================== Singleton Pattern ======================
config = SovereignConfig
SovereignConfig = config   # للتوافق مع الاستيرادات