# document.py

"""
[ملف الموديلز المركزي] - Sovereign Document Models
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Any, Optional
from datetime import datetime


# ====================== Matrix Models ======================

class MatrixData(BaseModel):
    """تمثيل مصفوفة تحويل حركية مستخرجة"""
    
    matrix: List[List[float]]
    page: int
    quality_score: float = Field(ge=0.0, le=100.0)
    
    type: str = Field(default="homogeneous_4x4")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    
    raw_snippet: Optional[str] = Field(default=None, max_length=700)
    repair_applied: bool = Field(default=False)
    extracted_at: datetime = Field(default_factory=datetime.now)
    
    metadata: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(
        extra='ignore', 
        arbitrary_types_allowed=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )


# ====================== Extraction Models ======================

class ExtractionResult(BaseModel):
    """نتيجة استخراج صفحة واحدة"""
    page_number: int
    clean_text: str = ""
    technical_score: int = Field(default=30, ge=0, le=100)
    content_type: str = "GENERAL"
    potential_matrices_count: int = 0
    extracted_matrices: List[MatrixData] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    timestamp: datetime = Field(default_factory=datetime.now)
    domain: str = "GENERAL"
    processing_status: str = "SUCCESS"

    model_config = ConfigDict(extra='ignore', arbitrary_types_allowed=True)


# ====================== Page & Document Models ======================

class RawPage(BaseModel):
    """صفحة خام من PDF"""
    page_number: int
    raw_text: str = Field(default="")
    text_length: int = Field(default=0, ge=0)
    image_count: int = Field(default=0, ge=0)
    has_potential_matrix: bool = Field(default=False)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class PageContent(BaseModel):
    """صفحة بعد المعالجة الكاملة"""
    page_number: int
    content: str = Field(default="")
    clean_content: str = Field(default="")
    technical_score: int = Field(default=50, ge=0, le=100)
    content_type: str = Field(default="GENERAL_TECHNICAL")
    potential_matrices: int = Field(default=0, ge=0)
    extracted_matrices: List[MatrixData] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(extra='ignore', arbitrary_types_allowed=True)

    @property
    def has_matrices(self) -> bool:
        """هل تحتوي الصفحة على مصفوفات؟"""
        return len(self.extracted_matrices) > 0

    @property
    def matrices_count(self) -> int:
        """عدد المصفوفات المستخرجة"""
        return len(self.extracted_matrices)


# ====================== Document & Result Models ======================

class DocumentMetadata(BaseModel):
    """بيانات وصفية عن المستند"""
    file_name: str
    file_path: Optional[str] = None
    total_pages: int
    processed_at: datetime = Field(default_factory=datetime.now)
    domain: str = Field(default="Vehicle_Design")
    success_rate: float = Field(default=0.0, ge=0.0, le=100.0)
    total_matrices: int = Field(default=0)
    processing_time_seconds: Optional[float] = None


class ProcessingResult(BaseModel):
    """النتيجة النهائية لمعالجة وثيقة كاملة"""
    metadata: DocumentMetadata
    pages: List[PageContent] = Field(default_factory=list)
    statistics: Dict[str, Any] = Field(default_factory=dict)
    status: str = Field(default="COMPLETED")
    error_message: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(extra='ignore', arbitrary_types_allowed=True)

    def get_total_matrices(self) -> int:
        return sum(page.matrices_count for page in self.pages)

    def summary(self) -> Dict[str, Any]:
        total_pages = len(self.pages)
        return {
            "file_name": self.metadata.file_name,
            "total_pages": self.metadata.total_pages,
            "total_matrices": self.get_total_matrices(),
            "avg_technical_score": round(
                sum(p.technical_score for p in self.pages) / total_pages, 1
            ) if total_pages > 0 else 0,
            "status": self.status,
            "success_rate": self.metadata.success_rate
        }


# ====================== Utility Functions ======================

def create_empty_page(page_num: int) -> ExtractionResult:
    """إنشاء صفحة فارغة"""
    return ExtractionResult(
        page_number=page_num,
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


def create_processing_result(
    file_name: str,
    total_pages: int,
    pages: List[PageContent],
    domain: str = "Vehicle_Design",
    processing_time: Optional[float] = None
) -> ProcessingResult:
    """إنشاء ProcessingResult بسهولة"""
    total_matrices = sum(p.matrices_count for p in pages)
    
    metadata = DocumentMetadata(
        file_name=file_name,
        total_pages=total_pages,
        domain=domain,
        total_matrices=total_matrices,
        processing_time_seconds=processing_time,
        success_rate=round(
            len([p for p in pages if p.technical_score >= 50]) / total_pages * 100, 1
        ) if total_pages > 0 else 0.0
    )

    return ProcessingResult(
        metadata=metadata,
        pages=pages,
        statistics={
            "total_matrices": total_matrices,
            "pages_with_matrices": sum(1 for p in pages if p.matrices_count > 0),
            "avg_technical_score": round(
                sum(p.technical_score for p in pages) / total_pages, 1
            ) if total_pages > 0 else 0.0
        }
    )