# search_models.py

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Any, Optional
from datetime import datetime


class SearchResult(BaseModel):
    """نتيجة بحث واحدة (من الـ Navigator أو HybridSearch)"""
    
    page_number: int
    content: str = Field(..., max_length=720, description="مقتطف من محتوى الصفحة")
    
    score: float = Field(
        ..., 
        ge=0.0, 
        le=1.0, 
        description="الدرجة النهائية المركبة (Semantic + Technical)"
    )
    
    semantic_similarity: float = Field(
        default=0.0, 
        ge=0.0, 
        le=1.0, 
        description="درجة التشابه الدلالي فقط"
    )
    
    technical_score: int = Field(
        default=50, 
        ge=0, 
        le=100, 
        description="الدرجة التقنية للصفحة"
    )
    
    content_type: str = Field(default="GENERAL_TECHNICAL")
    matrices_count: int = Field(default=0, ge=0)
    rank: int = Field(default=0, ge=0)
    
    metadata: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(
        extra='ignore',
        arbitrary_types_allowed=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )

    def is_high_quality(self) -> bool:
        """هل النتيجة تعتبر عالية الجودة؟"""
        return self.score >= 0.65 and self.matrices_count > 0

    def is_relevant(self, threshold: float = 0.45) -> bool:
        """هل النتيجة ذات صلة؟"""
        return self.score >= threshold

    def __str__(self):
        matrices = f" | Matrices: {self.matrices_count}" if self.matrices_count > 0 else ""
        return f"SearchResult(Page {self.page_number} | Score: {self.score:.3f}{matrices})"


class SearchResponse(BaseModel):
    """الرد الكامل من عملية البحث"""
    
    query: str
    results: List[SearchResult] = Field(default_factory=list)
    
    total_found: int = Field(default=0, ge=0)
    execution_time: float = Field(default=0.0, ge=0.0)
    
    context_aggregated: str = Field(
        default="", 
        max_length=12000, 
        description="السياق المجمع للـ RAG"
    )
    
    timestamp: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(
        extra='ignore',
        arbitrary_types_allowed=True
    )

    def get_top_results(self, k: int = 5) -> List[SearchResult]:
        """إرجاع أفضل K نتيجة"""
        return self.results[:k]

    def has_good_results(self, min_score: float = 0.5) -> bool:
        """هل يوجد نتائج جيدة؟"""
        if not self.results:
            return False
        return self.results[0].score >= min_score

    def total_matrices(self) -> int:
        """إجمالي المصفوفات في كل النتائج"""
        return sum(r.matrices_count for r in self.results)

    def __str__(self):
        return (
            f"SearchResponse(query='{self.query[:60]}...' | "
            f"Results: {len(self.results)} | "
            f"Best Score: {self.results[0].score:.3f if self.results else 0:.3f})"
        )