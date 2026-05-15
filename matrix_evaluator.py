# matrix_evaluator.py

import numpy as np
import re
from typing import Tuple, List, Optional

from logger import get_logger
from config import SovereignConfig
from calculator import SovereignCalculator


class MatrixEvaluator:
    def __init__(self, logger=None):
        self.logger = logger or get_logger("MatrixEvaluator")
        self.config = SovereignConfig
        self.calculator = SovereignCalculator(logger=self.logger)
        self.logger.info("✅ MatrixEvaluator تم تهيئته بنجاح (H-Point Optimized v2)")

    def _attempt_extract_and_repair(self, snippet: str, page: int) -> Tuple[Optional[np.ndarray], float, bool]:
        """
        كشف هجين متكيف (Hybrid Adaptive) - النسخة المحسنة والمُثبتة
        """
        try:
            if not self.quick_validate(snippet):
                return None, 0.0, False

            # استخراج الأرقام
            numbers_str = re.findall(r"[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?", snippet)
            numbers = [float(x) for x in numbers_str if self._is_valid_number(x)]

            if len(numbers) < 12:        # خفض الحد لزيادة الحساسية
                return None, 0.0, False

            # ====================== Hybrid Context Features ======================
            has_strong_pattern = bool(re.search(r'0\s+0\s+0\s+1|T\s*=|Homogeneous|Transform', snippet, re.IGNORECASE))
            is_hpoint_like = len(re.findall(r'h-?point|sg-?rp|manikin|eyellipse|j826', snippet.lower())) > 0
            has_table_tags = any(tag in snippet for tag in ["[MATRIX_START]", "[TABLE_ROW]", "[MATRIX]"])
            num_density = len(numbers) / max(len(snippet.split()), 1)

            candidates = []
            best_matrix = None
            best_hybrid_score = 0.0

            # توليد مرشحين بكفاءة أعلى (تجنب الحلقات الطويلة)
            start_idx = max(0, len(numbers) - 40)
            for i in range(start_idx, len(numbers) - 15):
                sample = numbers[i:i+16]
                if len(sample) == 16:
                    candidates.append(np.array(sample).reshape(4, 4))

            if len(numbers) >= 16:
                candidates.append(np.array(numbers[-16:]).reshape(4, 4))

            # تقييم المرشحين
            for matrix in candidates:
                quality = self._evaluate_matrix_quality(matrix)

                # Hybrid Score
                hybrid_score = quality
                if has_strong_pattern:
                    hybrid_score += 18
                if is_hpoint_like:
                    hybrid_score += 15
                if has_table_tags:
                    hybrid_score += 12
                if num_density > 0.65:
                    hybrid_score += 8

                if hybrid_score > best_hybrid_score:
                    best_hybrid_score = hybrid_score
                    best_matrix = matrix.copy()

                # Early Accept - Hybrid Logic (أكثر تسامحاً)
                if (quality >= 27 or 
                    (has_strong_pattern and quality >= 19) or
                    (is_hpoint_like and quality >= 18) or
                    (has_table_tags and quality >= 21)):
                    
                    self.logger.info(f"✅ [MATRIX SUCCESS] Page {page} | Q:{quality:.1f} | Hybrid:{hybrid_score:.1f}")
                    return matrix, quality, False

            # قرار نهائي
            if best_matrix is not None:
                min_threshold = 21 if (has_strong_pattern or is_hpoint_like or has_table_tags) else 26
                
                if best_hybrid_score >= min_threshold:
                    self.logger.info(f"🟡 [MATRIX ACCEPTED] Page {page} | Hybrid Score: {best_hybrid_score:.1f}")
                    return best_matrix, best_hybrid_score, False
                elif best_hybrid_score >= 16:
                    self.logger.debug(f"⚪ [WEAK MATRIX] Page {page} | Hybrid: {best_hybrid_score:.1f}")

            return None, 0.0, False

        except Exception as e:
            self.logger.debug(f"Error in _attempt_extract_and_repair (Page {page}): {e}")
            return None, 0.0, False
        
    def _is_valid_number(self, x: str) -> bool:
        """تنظيف بسيط للأرقام"""
        try:
            float(x)
            return True
        except:
            return False
        
    def evaluate_page(self, raw_text: str, page_num: int, domain: str = "Vehicle_Design") -> Optional[object]:
        """
        تقييم واستخراج مصفوفات من صفحة كاملة - نقطة دخول رئيسية
        """
        try:
            # تمرير النص كاملاً إلى المحرك الهجين
            matrix, quality, repaired = self._attempt_extract_and_repair(raw_text, page_num)
            
            if matrix is not None:
                self.logger.info(
                    f"📊 Page {page_num} | Domain: {domain} → "
                    f"Matrix extracted | Quality: {quality:.1f} | Repaired: {repaired}"
                )
                
                return {
                    "matrix": matrix,
                    "quality": quality,
                    "repaired": repaired,
                    "page_number": page_num,
                    "domain": domain
                }
            
            return None

        except Exception as e:
            self.logger.error(f"❌ Error in evaluate_page (Page {page_num}): {e}")
            return None
        
    def _extract_from_page(self, raw_text: str, raw_page: Optional[object], page_num: int, domain: str) -> Optional[object]:
        """
        استخراج المصفوفات من صفحة واحدة مع تقييم شامل
        """
        try:
            # محاولة الاستخراج والتقييم
            result = self._attempt_extract_and_repair(raw_text, page_num)       
            return result
        except Exception as e:
            self.logger.debug(f"Error in _extract_from_page (Page {page_num}): {e}")
            return None

    def _evaluate_matrix_quality(self, matrix: np.ndarray) -> float:
        """
        تقييم جودة مصفوفة 4x4 - نسخة Hybrid Adaptive محسنة لـ H-Point
        """
        if not isinstance(matrix, np.ndarray) or matrix.shape != (4, 4):
            return 0.0

        # التقييم الأساسي من Calculator
        base_score = self.calculator.evaluate_matrix_quality(matrix)
        score = float(base_score)

        # ====================== Hybrid Adaptive Scoring ======================
        
        # Translation Bonus (مهم جداً في Vehicle Design)
        translation = np.abs(matrix[:3, 3])
        trans_magnitude = np.max(translation)
        if trans_magnitude > 0.005:
            score += 13
        if trans_magnitude < 2000:        # قيم منطقية للسيارات (mm)
            score += 9

        # Orthogonality (متسامح مع OCR noise)
        rot = matrix[:3, :3]
        try:
            ortho_error = np.abs(rot.T @ rot - np.eye(3)).mean()
            if ortho_error < 0.09:
                score += 18
            elif ortho_error < 0.16:
                score += 12
            elif ortho_error < 0.24:
                score += 6
        except:
            pass

        # Homogeneous Check
        h_val = abs(matrix[3, 3])
        if abs(matrix[3, 3] - 1.0) < 0.18 or h_val < 0.22:
            score += 17
        elif h_val < 0.40:
            score += 9

        # Rotation Elements Bonus
        rot_elements = np.abs(rot)
        if np.any((rot_elements > 0.0005) & (rot_elements < 0.45)):
            score += 11

        # Mixed Values Bonus (شائع في H-Point)
        has_small = np.any((np.abs(matrix) > 0.0001) & (np.abs(matrix) < 0.35))
        has_large = np.any(np.abs(matrix) > 0.5)
        if has_small and has_large:
            score += 12

        # Penalty للقيم الشاذة
        max_val = np.max(np.abs(matrix))
        if max_val > 1e7:
            score = max(10.0, score - 40)
        elif max_val > 1e6:
            score -= 18

        # Clean Matrix Bonus
        zero_count = np.count_nonzero(np.abs(matrix) < 1e-5)
        if zero_count <= 13:
            score += 8

        final_score = round(max(15.0, min(score, 100.0)), 1)
        return final_score
    
    # ====================== دوال مساعدة ======================

    def quick_validate(self, snippet: str) -> bool:
        """فحص سريع لوجود مصفوفة محتملة"""
        if not snippet or len(snippet) < 30:
            return False
            
        # أنماط قوية
        if re.search(r'0\s+0\s+0\s+1', snippet):
            return True
        if re.search(r'T:\s*|\bT\s*=', snippet, re.IGNORECASE):
            return True
            
        # كثافة أرقام
        num_count = len(re.findall(r"[-+]?(?:\d*\.\d+|\d+)", snippet))
        return num_count >= 14