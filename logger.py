# logger.py

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime

from config import SovereignConfig


class SovereignLogger:
    """
    [اللوغر السيادي] - نظام تسجيل مركزي، احترافي ومتين
    """

    def __init__(self, name: str = "Sovereign"):
        self.name = name
        self.logger = logging.getLogger(name)
        
        # تجنب إضافة Handlers متعددة
        if not self.logger.handlers:
            self.logger.setLevel(getattr(logging, SovereignConfig.LOG_LEVEL.upper(), logging.INFO))
            self._setup_handlers()
        

    def _setup_handlers(self):
        """إعداد Handlers للـ Console والملف"""
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s',
            datefmt='%H:%M:%S'
        )

        # Console Handler
        if getattr(SovereignConfig, 'LOG_TO_CONSOLE', True):
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

        # File Handler
        if getattr(SovereignConfig, 'LOG_TO_FILE', True):
            try:
                log_dir: Path = SovereignConfig.LOGS_DIR
                log_dir.mkdir(parents=True, exist_ok=True)

                log_file = log_dir / f"sovereign_{datetime.now().strftime('%Y%m%d_%H%M')}.log"

                file_handler = logging.FileHandler(log_file, encoding='utf-8', delay=True)
                file_handler.setLevel(logging.DEBUG)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)

                self.logger.info(f"📝 Logging to file: {log_file}")

            except Exception as e:
                print(f"⚠️ Warning: Could not setup file logger: {e}")

    # ====================== Convenience Methods ======================
    def info(self, msg: str, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def debug(self, msg: str, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg: str, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)

    def exception(self, msg: str, *args, **kwargs):
        """تسجيل استثناء مع traceback كامل"""
        self.logger.exception(msg, *args, **kwargs)


# ====================== Singleton + Factory ======================
_loggers: dict[str, SovereignLogger] = {}


def get_logger(name: str = "Sovereign") -> SovereignLogger:
    """
    إرجاع Logger (مع دعم متعدد الأسماء)
    """
    if name not in _loggers:
        _loggers[name] = SovereignLogger(name)
    return _loggers[name]


# ====================== Utility ======================
def log_config_summary():
    """طباعة ملخص الإعدادات عند بدء التشغيل"""
    logger = get_logger("Config")
    
    try:
        config_dict = SovereignConfig.get_config_dict() if hasattr(SovereignConfig, 'get_config_dict') else {}
        
        logger.info("🚀 Sovereign Engine Configuration Summary:")
        important_keys = [
            'LOG_LEVEL', 'MAX_WORKERS', 'MATRIX_REPAIR_ENABLED', 'DEFAULT_DOMAIN',
            'AGGRESSIVE_MATRIX_DETECTION', 'MATRIX_MIN_QUALITY_THRESHOLD',
            'OPENAI_API_KEY' if hasattr(SovereignConfig, 'OPENAI_API_KEY') else None,
            'LOG_TO_FILE', 'LOG_TO_CONSOLE'
        ]
        
        for key in important_keys:
            if key and hasattr(SovereignConfig, key):
                value = getattr(SovereignConfig, key)
                # إخفاء API Key جزئياً
                if key == 'OPENAI_API_KEY' and value:
                    value = str(value)[:8] + "..." if len(str(value)) > 8 else "***"
                logger.info(f"   • {key}: {value}")
                
    except Exception as e:
        logger.warning(f"⚠️ Could not display config summary: {e}")


# تهيئة أولية عند الاستيراد
if __name__ != "__main__":
    log_config_summary()