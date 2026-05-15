# conclusion_engine.py

from typing import Dict, Any, List, Optional
from datetime import datetime

from logger import get_logger
from config import SovereignConfig
from calculator import SovereignCalculator
from logic_extractor import LogicExtractor
from matrix_models import ExtractionResult


class ConclusionEngine:
    """
    [محرك الاستنتاج السيادي] - يقوم بتحليل نهائي وتقييم ذكي للصفحات والمستند ككل
    """

    def __init__(self, logger=None):
        self.logger = logger or get_logger("ConclusionEngine")
        self.config = SovereignConfig
        self.calculator = SovereignCalculator(logger=self.logger)
        self.logic = LogicExtractor(logger=self.logger)
        
        self.logger.info("🧠 ConclusionEngine تم تهيئته بنجاح")

    def analyze_page(self, extraction_result: ExtractionResult) -> Dict[str, Any]:
        """تحليل شامل وذكي لصفحة واحدة"""
        if not extraction_result:
            return self._empty_analysis(0)

        try:
            page_num = getattr(extraction_result, 'page_number', 0)
            matrices_count = len(getattr(extraction_result, 'extracted_matrices', []))

            # استخراج المنطق والمعادلات
            logic_data = self.logic.extract_logic(
                getattr(extraction_result, 'clean_text', '')
            )

            # حساب درجة النزاهة
            integrity_score = self._calculate_integrity(extraction_result, logic_data)

            # توليد توصية
            recommendation = self._generate_recommendation(integrity_score, matrices_count)

            analysis = {
                "page_number": page_num,
                "technical_score": getattr(extraction_result, 'technical_score', 0),
                "content_type": getattr(extraction_result, 'content_type', "UNKNOWN"),
                "matrices_count": matrices_count,
                "integrity_score": round(integrity_score, 1),
                "recommendation": recommendation,
                "logic_summary": {
                    "variables_count": len(logic_data.get("vars", {})),
                    "formulas_count": len(logic_data.get("formulas", [])),
                    "has_matrices": matrices_count > 0
                },
                "perception_score": extraction_result.metadata.get("perception_score", 0) 
                                   if hasattr(extraction_result, 'metadata') else 0,
                "timestamp": datetime.now().isoformat(),
                "confidence": round(min(integrity_score / 100, 1.0), 2)
            }

            # Logging
            status_icon = "🟢" if integrity_score >= 75 else "🟡" if integrity_score >= 55 else "🔴"
            self.logger.info(
                f"{status_icon} Page {page_num:3d} Analysis | "
                f"Matrices: {matrices_count} | Integrity: {integrity_score:.1f} | "
                f"Type: {analysis['content_type']}"
            )

            return analysis

        except Exception as e:
            self.logger.error(f"❌ خطأ في analyze_page (Page {getattr(extraction_result, 'page_number', '?')}): {e}", exc_info=False)
            return self._empty_analysis(getattr(extraction_result, 'page_number', 0))

    def _calculate_integrity(self, result: ExtractionResult, logic_data: Dict) -> float:
        """حساب درجة النزاهة الشاملة"""
        base = getattr(result, 'technical_score', 50)
        matrices = len(getattr(result, 'extracted_matrices', []))
        formulas = len(logic_data.get("formulas", []))
        perception = result.metadata.get("perception_score", 50) if hasattr(result, 'metadata') else 50

        score = (
            base * 0.40 +
            matrices * 11.0 +           # زيادة وزن المصفوفات
            min(formulas * 5.0, 40) +
            perception * 0.20
        )

        # مكافأة خاصة لـ H-Point
        if getattr(result, 'content_type', '') in ["HPOINT_TECHNICAL", "VEHICLE_DESIGN"]:
            score += 15

        return round(min(max(score, 10), 100), 1)

    def _generate_recommendation(self, score: float) -> str:
        """توليد توصية ذكية حسب الدرجة"""
        if score >= 88:
            return "🏆 صفحة ممتازة - يُفضل حفظها كمرجع تقني رئيسي"
        elif score >= 75:
            return "✅ صفحة عالية الجودة - تحتوي على معلومات قيمة جداً"
        elif score >= 60:
            return "🟡 صفحة جيدة - تحتوي معلومات مفيدة مع بعض الضعف"
        elif score >= 45:
            return "⚠️ صفحة متوسطة - تحتاج مراجعة أو تحسين استخراج"
        else:
            return "🔴 صفحة ضعيفة - يُفضل إعادة معالجتها أو التحقق من جودة النص"

    def analyze_document(self, pages_analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """تحليل شامل للوثيقة كاملة"""
        if not pages_analyses:
            return {"status": "EMPTY", "message": "لا توجد بيانات للتحليل"}

        total_pages = len(pages_analyses)
        high_quality = sum(1 for p in pages_analyses if p.get("integrity_score", 0) >= 75)
        total_matrices = sum(p.get("matrices_count", 0) for p in pages_analyses)

        avg_integrity = round(
            sum(p.get("integrity_score", 0) for p in pages_analyses) / total_pages, 1
        )

        return {
            "document_summary": {
                "total_pages": total_pages,
                "total_matrices": total_matrices,
                "avg_integrity_score": avg_integrity,
                "high_quality_pages": high_quality,
                "quality_percentage": round(high_quality / total_pages * 100, 1)
            },
            "overall_recommendation": self._document_level_recommendation(avg_integrity, high_quality, total_pages),
            "timestamp": datetime.now().isoformat()
        }

    def _document_level_recommendation(self, avg_score: float, high_quality: int, total: int) -> str:
        if avg_score >= 78 and high_quality / total > 0.6:
            return "الوثيقة ممتازة وغنية بالمعلومات التقنية عالية الجودة"
        elif avg_score >= 65:
            return "الوثيقة جيدة ومفيدة للاستخدام"
        else:
            return "الوثيقة تحتاج تحسين في جودة الاستخراج أو المحتوى"

    def _empty_analysis(self, page_number: int) -> Dict[str, Any]:
        """تحليل فارغ في حالة الخطأ"""
        return {
            "page_number": page_number,
            "technical_score": 0,
            "integrity_score": 0.0,
            "recommendation": "خطأ في التحليل",
            "error": True
        }