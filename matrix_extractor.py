# matrix_extractor.py

import re
import numpy as np
from typing import List, Optional, Dict, Any, Tuple

from logger import get_logger
from config import SovereignConfig
from document import MatrixData
from matrix_models import ExtractionResult

from calculator import SovereignCalculator
from matrix_detector import MatrixDetector
from matrix_evaluator import MatrixEvaluator
from matrix_llm import MatrixLLMRepairer


class MatrixExtractor:
    """
    [مستخرج المصفوفات السيادي] - النسخة المحسنة لكتب H-Point
    """

    def __init__(self, logger=None):
        self.logger = logger or get_logger("MatrixExtractor")
        self.config = SovereignConfig
        self.calculator = SovereignCalculator(logger=self.logger)
        
        self.detector = MatrixDetector(logger=self.logger)
        self.evaluator = MatrixEvaluator(logger=self.logger)
        self.llm_repairer = MatrixLLMRepairer(logger=self.logger, config=self.config)

        self.logger.info("✅ MatrixExtractor تم تهيئته بنجاح (نسخة محسنة - H-Point Ready)")

    def extract_from_page(self, raw_text: str, page_number: int) -> ExtractionResult:
        """استخراج المصفوفات من صفحة واحدة - نسخة نهائية محسنة"""
        clean_text = ""
        try:
            clean_text = self._clean_text(raw_text)
            content_type = self._classify_content(clean_text)
            
            # Perception Layer
            perception = self.detector._perceive_page_potential(clean_text)

            self.logger.debug(
                f"🧠 Page {page_number:3d} | Perception: {perception['score']:3d} | "
                f"Rec: {perception.get('recommendation', 'N/A')}"
            )

            # كشف المرشحين
            if perception['score'] < 16 and content_type not in ["HPOINT_TECHNICAL", "VEHICLE_DESIGN"]:
                potential_matrices = []
            else:
                potential_matrices = self.detector._detect_potential_matrices(
                    clean_text, page_number=page_number
                )

            extracted_matrices: List[MatrixData] = []
            dynamic_threshold = self._get_dynamic_threshold(
                clean_text, content_type, len(potential_matrices), perception['score']
            )

            for snippet in potential_matrices:
                # استخدام Evaluator مباشرة (الطريقة الصحيحة)
                matrix, quality, repaired = self.evaluator._attempt_extract_and_repair(snippet, page_number)
                
                if matrix is None:
                    continue

                original_quality = quality

                # LLM Repair (فقط عند الحاجة)
                if (quality < dynamic_threshold + 5 and quality >= dynamic_threshold - 35 and
                    getattr(self.config, 'MATRIX_REPAIR_ENABLED', True)):
                    try:
                        llm_matrix, llm_quality, llm_repaired = self.llm_repairer.run_sync(snippet, page_number)
                        if llm_matrix is not None and llm_quality > quality + 1.0:
                            matrix, quality, repaired = llm_matrix, llm_quality, llm_repaired
                            self.logger.info(f"🧠 [LLM REPAIR] Page {page_number} | {original_quality:.1f} → {llm_quality:.1f}")
                    except Exception as e:
                        self.logger.debug(f"LLM Repair failed on page {page_number}: {e}")

                # عتبة قبول ذكية
                if content_type in ["HPOINT_TECHNICAL", "VEHICLE_DESIGN"]:
                    acceptance_threshold = max(21.0, dynamic_threshold - 20)
                else:
                    acceptance_threshold = max(26.0, dynamic_threshold - 12)

                if quality >= acceptance_threshold:
                    matrix_list = self._convert_to_list(matrix)
                    
                    extracted_matrices.append(MatrixData(
                        matrix=matrix_list,
                        page=page_number,
                        quality_score=float(quality),
                        confidence=round(min(quality / 100, 1.0), 2),
                        raw_snippet=snippet[:600],
                        repair_applied=repaired,
                        type="homogeneous_4x4",
                        metadata={
                            "extraction_method": "evaluator" if not repaired else "llm_repaired",
                            "original_quality": float(original_quality),
                            "accepted_threshold": round(acceptance_threshold, 1),
                            "dynamic_threshold": round(dynamic_threshold, 1)
                        }
                    ))

            # Logging نهائي
            if extracted_matrices or len(potential_matrices) > 0:
                self.logger.info(
                    f"📄 Page {page_number:3d} | Potential: {len(potential_matrices):2d} | "
                    f"Accepted: {len(extracted_matrices):2d} | "
                    f"Threshold: {dynamic_threshold:.1f} | Type: {content_type}"
                )

            technical_score = self._calculate_technical_score(
                clean_text, len(extracted_matrices), content_type, perception['score']
            )

            return ExtractionResult(
                page_number=page_number,
                clean_text=clean_text[:1500],
                technical_score=technical_score,
                content_type=content_type,
                potential_matrices_count=len(potential_matrices),
                extracted_matrices=extracted_matrices,
                metadata={
                    "dynamic_threshold": round(dynamic_threshold, 1),
                    "perception_score": perception['score'],
                    "extraction_rate": round(len(extracted_matrices) / max(len(potential_matrices), 1) * 100, 1)
                }
            )

        except Exception as e:
            self.logger.error(f"❌ خطأ في extract_from_page (صفحة {page_number}): {e}", exc_info=True)
            return ExtractionResult(
                page_number=page_number,
                clean_text=clean_text[:800] if 'clean_text' in locals() else "",
                technical_score=20,
                content_type="ERROR",
                potential_matrices_count=0,
                extracted_matrices=[],
                metadata={"error": str(e)}
            )
            
    def _attempt_extract_and_repair(self, snippet: str, page: int) -> Tuple[Optional[np.ndarray], float, bool]:
        """
        Wrapper خفيف - يفوض المهمة للـ MatrixEvaluator
        """
        try:
            # التفويض للـ Evaluator (هذا هو التصميم الصحيح)
            matrix, quality, repaired = self.evaluator._attempt_extract_and_repair(snippet, page)
            
            if matrix is None:
                self.logger.debug(f"⚪ Page {page} → No valid matrix found")
                return None, 0.0, False

            # Logging حسب مستوى الجودة
            if quality >= 55.0:
                self.logger.info(f"✅ [MATRIX ACCEPTED] Page {page} | Quality: {quality:.1f}")
            elif quality >= 40.0:
                self.logger.info(f"🟡 [MATRIX PARTIAL] Page {page} | Quality: {quality:.1f}")
            elif quality >= 25.0:
                self.logger.debug(f"⚪ [MATRIX WEAK] Page {page} | Quality: {quality:.1f}")
            else:
                self.logger.debug(f"⚪ Page {page} → Extraction failed completely")

            return matrix, quality, repaired

        except AttributeError as e:
            self.logger.error(f"❌ Page {page} → MatrixEvaluator لا يحتوي على _attempt_extract_and_repair()")
            return None, 0.0, False
        except Exception as e:
            self.logger.debug(f"خطأ في wrapper _attempt_extract_and_repair (Page {page}): {e}")
            return None, 0.0, False
        
    # ====================== الدوال المساعدة المحسنة ======================
    def _get_dynamic_threshold(self, text: str, content_type: str, 
                             candidates_count: int, perception_score: int) -> float:
        """حساب عتبة قبول ديناميكية ذكية"""
        try:
            base_threshold = self.calculator.calculate_dynamic_threshold(
                text, content_type, candidates_count
            )
        except:
            base_threshold = 45.0

        threshold = base_threshold

        # تخفيض قوي لكتب H-Point
        if content_type in ["HPOINT_TECHNICAL", "VEHICLE_DESIGN"]:
            threshold = base_threshold * 0.58
            threshold = max(20.0, threshold)

        elif perception_score >= 80:
            threshold *= 0.70
        elif perception_score >= 60:
            threshold *= 0.78
        elif perception_score >= 40:
            threshold *= 0.85

        # تعديل حسب عدد المرشحين
        if candidates_count >= 10:
            threshold *= 0.85
        elif candidates_count >= 5:
            threshold *= 0.92

        # Bonus للـ Tags
        if any(tag in text for tag in ["[MATRIX_START]", "[TABLE_ROW]", "[MATRIX]"]):
            threshold = max(19.0, threshold - 9.0)

        return round(max(20.0, min(threshold, 65.0)), 1)
    
    def _convert_to_list(self, matrix) -> List[List[float]]:
        """تحويل المصفوفة إلى قائمة nested بأمان عالي"""
        if matrix is None:
            return [[0.0] * 4 for _ in range(4)]

        try:
            # حالة numpy array
            if hasattr(matrix, 'tolist'):
                return matrix.tolist()

            # حالة list بالفعل
            if isinstance(matrix, list):
                # لو كانت قائمة مسطحة (16 عنصر)
                if len(matrix) == 16 and all(isinstance(x, (int, float)) for x in matrix):
                    return [matrix[i:i+4] for i in range(0, 16, 4)]
                
                # لو كانت قائمة nested
                if matrix and isinstance(matrix[0], (list, tuple)):
                    return [[float(x) for x in row] for row in matrix]
                
                # حالة صف واحد
                return [[float(x) for x in matrix]]

            # محاولة تحويل عام
            import numpy as np
            arr = np.array(matrix, dtype=float)
            if arr.ndim == 1 and len(arr) == 16:
                arr = arr.reshape(4, 4)
            return arr.tolist()

        except Exception as e:
            self.logger.warning(f"⚠️ فشل تحويل مصفوفة إلى list (Page unknown): {e}")
            return [[0.0] * 4 for _ in range(4)]
                
    def _clean_text(self, text: str) -> str:
        """تنظيف النص مع الحفاظ على هيكل المصفوفات"""
        if not text:
            return ""

        # إزالة أحرف غير مرئية
        text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F\u200B\u200C\u200D\uFEFF]', '', text)
        
        lines = text.split('\n')
        cleaned = []

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            # الحفاظ على أسطر الجداول والمصفوفات
            if (re.search(r'\d+\.\d+', line) or          # أرقام عشرية
                re.search(r'\d+\s+\d+\s+\d+', line) or   # أرقام متتالية
                '[MATRIX' in line or '[TABLE' in line or
                re.search(r'0\s+0\s+0\s+1', line)):
                
                cleaned.append(line.rstrip())
            else:
                cleaned.append(stripped)

        clean_text = "\n".join(cleaned)
        clean_text = re.sub(r'\s+', ' ', clean_text)
        return clean_text.strip()
    

    def _classify_content(self, text: str) -> str:
        """تصنيف نوع المحتوى - متخصص في H-Point (نسخة محسنة وأكثر دقة)"""
        if not text or len(text) < 40:
            return "GENERAL_TECHNICAL"

        lower = text.lower()
        
        # كلمات مفتاحية H-Point (أولوية قصوى)
        hpoint_keywords = [
            'h-point', 'hip point', 'h point', 'sg rp', 'sgrp', 'sg-rp', 
            'seating reference point', 'manikin', 'j826', 'sae j826', 
            'eyellipse', 'occupant package', 'packaging', 'hardpoint', 
            'wheelbase', 'vehicle package'
        ]
        
        matrix_keywords = [
            'transformation matrix', 'homogeneous', 'dh parameter', 
            'denavit', 'hartenberg', 'rotation matrix', 'coordinate system', 
            't =', 'homogeneous transformation'
        ]

        # أولوية 1: H-Point (الأهم)
        if any(k in lower for k in hpoint_keywords):
            return "HPOINT_TECHNICAL"
        
        # أولوية 2: مصفوفات حركية عامة
        elif any(k in lower for k in matrix_keywords):
            return "MATRIX_TECHNICAL"
        
        # أولوية 3: كثافة أرقام (Numeric Heavy)
        decimal_count = len(re.findall(r'\d+\.\d+', text))
        integer_sequences = len(re.findall(r'(?:\d+\s+){5,}', text))  # تسلسل أرقام كثير
        
        if decimal_count > 45 or integer_sequences > 2:
            return "NUMERIC_HEAVY"
        elif decimal_count > 28 or integer_sequences > 0:
            return "NUMERIC_MEDIUM"

        # أولوية 4: محتوى تقني عام
        technical_terms = ['section', 'dimension', 'coordinate', 'grid', 'hardpoint', 'view']
        if any(term in lower for term in technical_terms) and decimal_count > 12:
            return "TECHNICAL"

        return "GENERAL_TECHNICAL"


    def _calculate_technical_score(self, text: str, matrix_count: int, 
                                 content_type: str, perception_score: int = 0) -> int:
        """حساب الدرجة التقنية للصفحة - محسن ومتوازن"""
        score = 40  # قاعدة

        text_len = len(text)
        
        # مكافأة الطول
        if text_len > 1600:
            score += 28
        elif text_len > 1000:
            score += 20
        elif text_len > 600:
            score += 14
        elif text_len > 300:
            score += 7

        # مكافأة عدد المصفوفات المستخرجة (مهم جداً)
        score += matrix_count * 32

        # مكافأة حسب نوع المحتوى
        if content_type == "HPOINT_TECHNICAL":
            score += 42
        elif content_type == "MATRIX_TECHNICAL":
            score += 35
        elif content_type == "NUMERIC_HEAVY":
            score += 25
        elif content_type == "NUMERIC_MEDIUM":
            score += 16
        elif content_type == "TECHNICAL":
            score += 18

        # Perception Score (وزن قوي)
        score += int(perception_score * 0.45)

        # سقف وأرضية
        final_score = min(max(int(score), 35), 98)
        
        return final_score