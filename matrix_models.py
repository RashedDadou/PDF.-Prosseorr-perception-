"""
[matrix_models.py] - Compatibility / Bridge Layer
"""

from document import (
    MatrixData,
    ExtractionResult as DocumentExtractionResult,
    PageContent
)

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Any, Optional
from datetime import datetime


# ====================== Compatibility Aliases ======================

ExtractedMatrix = MatrixData


class ExtractionResult(DocumentExtractionResult):
    """نسخة متوافقة مع الكود القديم + تحسينات للتوافق مع MatrixExtractor"""
    
    # إعادة تعريف الحقول المهمة للتوافق
    extracted_matrices: List[ExtractedMatrix] = Field(default_factory=list)
    
    # الحقول الإضافية
    timestamp: datetime = Field(default_factory=datetime.now)
    domain: str = Field(default="GENERAL")
    processing_status: str = Field(default="SUCCESS")
    metadata: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(
        populate_by_name=True,
        extra='ignore',
        arbitrary_types_allowed=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )


# ====================== Utility Functions ======================

def create_extracted_matrix(
    matrix: List[List[float]],
    page_number: int,
    quality_score: float,
    confidence: float = 0.0,
    raw_snippet: Optional[str] = None,
    repair_applied: bool = False,
    type: str = "homogeneous_4x4",
    **kwargs
) -> ExtractedMatrix:
    """دالة مساعدة لإنشاء MatrixData بطريقة آمنة"""
    return ExtractedMatrix(
        matrix=matrix,
        page=page_number,
        quality_score=quality_score,
        confidence=confidence,
        raw_snippet=raw_snippet,
        repair_applied=repair_applied,
        type=type,
        **kwargs
    )


def create_empty_extraction_result(page_number: int) -> ExtractionResult:
    """إنشاء نتيجة استخراج فارغة"""
    return ExtractionResult(
        page_number=page_number,
        clean_text="",
        technical_score=25,
        content_type="EMPTY",
        potential_matrices_count=0,
        extracted_matrices=[],
        metadata={
            "note": "Page was empty or could not be processed",
            "is_empty": True
        }
    )


# ====================== Re-exports ======================

__all__ = [
    "ExtractedMatrix",
    "ExtractionResult",
    "MatrixData",
    "PageContent",
    "create_extracted_matrix",
    "create_empty_extraction_result"
]