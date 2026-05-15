# logic_extractor.py

import re
from typing import List, Dict, Any, Optional
from logger import get_logger


class LogicExtractor:
    """
    [مستخرج المنطق السيادي]: يستخرج المتغيرات والمعادلات والأنماط المنطقية
    """

    def __init__(self, logger=None):
        self.logger = logger or get_logger("LogicExtractor")

    def extract_logic(self, text: str) -> Dict[str, Any]:
        """استخراج شامل للمنطق"""
        if not text or len(text) < 30:
            return {"vars": {}, "formulas": [], "status": "EMPTY"}

        vars_found = self._extract_variables(text)
        formulas = self._extract_formulas(text)

        return {
            "vars": vars_found,
            "formulas": formulas,
            "matrices_detected": len(re.findall(r'\[\s*[\d\.\s,-]+\s*\]', text)),
            "status": "SUCCESS" if vars_found or formulas else "LOW_CONTENT"
        }

    def _extract_variables(self, text: str) -> Dict[str, float]:
        """استخراج المتغيرات"""
        pattern = r'(\b[A-Za-z][A-Za-z0-9]*)\s*[:=]\s*(-?\d+\.?\d*(?:[eE][-+]?\d+)?)'
        matches = re.findall(pattern, text)
        return {name.strip(): float(value) for name, value in matches}

    def _extract_formulas(self, text: str) -> List[str]:
        """استخراج المعادلات"""
        patterns = [
            r'\b\w+\s*=\s*[\w\s\+\-\*/\.\(\)]+',
            r'[A-Za-z]\d*\s*[:=]\s*.+',
        ]
        formulas = []
        for pat in patterns:
            matches = re.findall(pat, text)
            formulas.extend([m.strip() for m in matches if len(m) > 8])
        
        # إزالة التكرارات مع الحفاظ على الترتيب
        return list(dict.fromkeys(formulas))