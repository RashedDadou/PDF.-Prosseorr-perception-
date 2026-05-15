# matrix_detector.py

import re
from typing import List, Dict, Any, Optional

from logger import get_logger


class MatrixDetector:
    """
    [كاشف المصفوفات المتقدم] - متخصص في اكتشاف الإشارات والمرشحين لمصفوفات 4x4
    """

    def __init__(self, logger=None):
        self.logger = logger or get_logger("MatrixDetector")
        self.logger.info("🔍 MatrixDetector تم تهيئته بنجاح")

    def _perceive_page_potential(self, text: str) -> Dict[str, Any]:
        """
        الحس الإدراكي (Perception Layer) - نسخة Aggressive Hybrid محسنة لكتب H-Point
        """
        if not text or len(text) < 25:
            return {"score": 0, "recommendation": "LOW", "has_matrix_signals": False,
                    "signals_count": 0, "signals": [], "reason": "text_too_short"}

        score = 0
        signals = []
        lower = text.lower()
        clean_text = re.sub(r'\s+', ' ', text)

        # ====================== 1. إشارات قوية جداً (أعلى وزن) ======================
        has_matrix_tag = '[MATRIX_START]' in text or '[MATRIX]' in text
        has_table_tag = '[TABLE_ROW]' in text

        if has_matrix_tag:
            score += 65
            signals.append("matrix_start_tag")
        if has_table_tag:
            score += 50
            signals.append("table_row_tag")

        # أنماط Homogeneous Transformation
        if re.search(r'0\s+0\s+0\s+1', text):
            score += 58
            signals.append("homogeneous_0001")

        if re.search(r'T\s*[=:]\s*[\[\(]', text) or re.search(r'T\s*=', text):
            score += 45
            signals.append("T_matrix_notation")

        # ====================== 2. كلمات H-Point & Vehicle Packaging (وزن أعلى) ======================
        strong_hpoint_keywords = [
            'h-point', 'hip point', 'h point', 'sg rp', 'sgrp', 'sg-rp',
            'seating reference', 'manikin', 'j826', 'sae j826', 'eyellipse',
            'occupant package', 'packaging', 'hardpoint', 'hard point',
            'wheelbase', 'track width', 'section', 'grid'
        ]

        hpoint_matches = sum(1 for kw in strong_hpoint_keywords if kw in lower)
        score += hpoint_matches * 32                    # زيادة الوزن
        if hpoint_matches >= 2:
            signals.append(f"hpoint_keywords:{hpoint_matches}")
        elif hpoint_matches == 1:
            score += 18

        # ====================== 3. كثافة الأرقام والجداول (أكثر حساسية) ======================
        decimals = len(re.findall(r'\d+\.\d+', clean_text))
        total_numbers = len(re.findall(r'[-+]?(?:\d*\.\d+|\d+)', clean_text))

        if decimals > 45:
            score += 55
            signals.append("very_high_decimal")
        elif decimals > 28:
            score += 42
            signals.append("high_decimal")
        elif decimals > 15:
            score += 25

        if total_numbers > 85:
            score += 38
            signals.append("extreme_number_density")

        # كشف صفوف أرقام كثيفة (مؤشر قوي)
        dense_rows = len(re.findall(r'(?:\s*[-+]?\d+\.?\d*\s+){4,}', clean_text))
        if dense_rows >= 4:
            score += 52
            signals.append(f"very_dense_rows:{dense_rows}")
        elif dense_rows >= 2:
            score += 35
            signals.append(f"dense_rows:{dense_rows}")
        elif dense_rows >= 1:
            score += 20

        # ====================== 4. سياق H-Point & Technical (موسع) ======================
        broad_context = [
            'transformation', 'homogeneous', 'rotation', 'translation', 'coordinate',
            'denavit', 'hartenberg', 'kinematic', 'matrix', 'dimension', 'section',
            'hardpoint', 'grid', 'view', 'package', 'occupant'
        ]
        
        context_matches = sum(1 for word in broad_context if word in lower)
        if context_matches > 0:
            score += context_matches * 19
            signals.append(f"context:{context_matches}")

        # ====================== 5. طول النص ======================
        text_len = len(clean_text)
        if text_len > 1400:
            score += 18
        elif text_len > 850:
            score += 12
        elif text_len > 450:
            score += 6

        # ====================== Normalization ======================
        final_score = min(max(int(score), 0), 100)

        recommendation = "HIGH" if final_score >= 65 else \
                        "MEDIUM" if final_score >= 42 else "LOW"

        return {
            "score": final_score,
            "recommendation": recommendation,
            "has_matrix_signals": final_score >= 40,          # خفضنا العتبة
            "signals_count": len(signals),
            "signals": signals[:22],
            "reason": "strong_tags" if has_matrix_tag else 
                      "hpoint_context" if hpoint_matches >= 2 else 
                      "high_numeric" if decimals > 30 else 
                      "dense_rows" if dense_rows >= 2 else "medium_signals"
        }
        
    def _detect_potential_matrices(self, text: str, page_number: Optional[int] = None) -> List[str]:
        """كشف قوي ومتعدد المستويات - نسخة H-Point Aggressive"""
        if not text or len(text) < 30:
            return []

        candidates = []
        clean_text = re.sub(r'\s+', ' ', text)
        lower_clean = clean_text.lower()

        # ====================== 1. Tagged Blocks (أعلى أولوية) ======================
        tagged_blocks = re.findall(
            r'\[MATRIX_START\](.*?)(?=\[MATRIX_START\]|\[MATRIX_END\]|\Z)', 
            text, re.DOTALL | re.IGNORECASE
        )
        tagged_rows = re.findall(
            r'\[TABLE_ROW\].*?(?=\[TABLE_ROW\]|\[MATRIX_START\]|\Z)', 
            text, re.DOTALL | re.IGNORECASE
        )

        candidates.extend(tagged_blocks)
        candidates.extend(tagged_rows)

        # ====================== 2. أنماط مباشرة قوية ======================
        direct_patterns = [
            r'T\s*[=:]\s*[\[\(][^\n]{20,}',
            r'0\s+0\s+0\s+1',
            r'Homogeneous.*?Transform',
            r'Transformation Matrix',
            r'Denavit-Hartenberg|DH Parameter',
        ]
        for pat in direct_patterns:
            candidates.extend(re.findall(pat, text, re.IGNORECASE | re.DOTALL))

        # ====================== 3. صفوف أرقام كثيفة (محسن) ======================
        for line in text.split('\n'):
            nums = re.findall(r'[-+]?(?:\d*\.\d+|\d+)', line)
            if len(nums) >= 4:                    # خفضنا الحد
                candidates.append(line.strip())

        # كتل متعددة الصفوف (أكثر تسامحاً)
        dense_blocks = re.findall(
            r'(?:(?:[-+]?\d*\.?\d+\s+){3,}[-\+]?\d*\.?\d+(?:\s+[-+]?\d*\.?\d+)*\s*){2,8}',
            clean_text
        )
        candidates.extend(dense_blocks)

        # ====================== 4. أنماط H-Point & Packaging (جديد وقوي) ======================
        hpoint_patterns = [
            r'(?:H-Point|Hip Point|SG RP|SgRP|Eyellipse).*?[\d\.\s,]{15,}',
            r'Coordinates?\s*[:=].*?[\d\.\s,]{20,}',
            r'(?:X|Y|Z)\s*[:=]?\s*[-+]?\d*\.?\d+.*?(?:X|Y|Z)',
            r'(?:Length|Width|Height|Wheelbase|Track).*?[\d\.\s,]{15,}',
            r'Section\s+[A-Z]-\s*[A-Z].*?[\d\.\s,]{10,}',
            r'Hardpoint|Hard Point',
        ]
        for pat in hpoint_patterns:
            candidates.extend(re.findall(pat, text, re.IGNORECASE | re.DOTALL))

        # ====================== 5. أنماط جداول وأبعاد عامة ======================
        dimension_patterns = [
            r'(?:\d+\.?\d*\s+){6,}',                    # 6 أرقام أو أكثر متتالية
            r'[\d\.\s,]{30,}',                          # سلاسل أرقام طويلة
            r'(?:mm|inch|deg|°)\s*[:=]?\s*[\d\.\s,]+', # وحدات قياس
        ]
        for pat in dimension_patterns:
            candidates.extend(re.findall(pat, clean_text))

        # ====================== تنظيف وإزالة التكرارات ======================
        unique = []
        seen = set()

        for c in candidates:
            if not c:
                continue
            cleaned = re.sub(r'\s+', ' ', c.strip())
            if len(cleaned) < 38:          # خفضنا الحد الأدنى
                continue

            key = cleaned[:650]
            if key not in seen:
                seen.add(key)
                unique.append(cleaned)

        # ====================== Logging ======================
        if unique and page_number is not None:
            tagged_count = sum(1 for c in unique if any(tag in c.upper() for tag in ['[MATRIX', '[TABLE']))

            self.logger.info(
                f"📊 [MATRIX DETECTED] Page {page_number} → Found {len(unique)} candidates "
                f"(Tagged: {tagged_count} | Dense/Quasi: {len(unique)-tagged_count})"
            )

        # حد أقصى معقول للأداء
        return unique[:45]