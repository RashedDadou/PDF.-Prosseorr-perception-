# pdf_models.py

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Any, Optional
from datetime import datetime
import os
from dataclasses import dataclass, field


# ====================== Pydantic Models ======================

class RawPage(BaseModel):
    """تمثيل صفحة خام من PDF"""
    page_number: int
    raw_text: str = Field(default="")
    text_length: int = Field(default=0, ge=0)
    image_count: int = Field(default=0, ge=0)
    has_potential_matrix: bool = Field(default=False)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra='ignore',
        json_encoders={datetime: lambda v: v.isoformat()}
    )

    def __str__(self):
        matrices_hint = " [🟢 Matrices]" if self.has_potential_matrix else ""
        return f"RawPage({self.page_number} | {len(self.raw_text)} chars{matrices_hint})"


class PDFDocument(BaseModel):
    """تمثيل الوثيقة الكاملة - معالجة محسنة للحالات الخطأ"""
    
    # الحقول الأساسية مع قيم افتراضية
    file_path: str = Field(default="")
    file_name: str = Field(default="")
    
    total_pages: int = Field(default=0, ge=0)
    pages: List[RawPage] = Field(default_factory=list)
    
    status: str = Field(default="SUCCESS")
    error_message: Optional[str] = None
    processed_at: datetime = Field(default_factory=datetime.now)
    file_size: Optional[int] = Field(default=None)   # مهم لملف 25MB
    
    # للوصول السريع
    page_dict: Optional[Dict[int, RawPage]] = Field(default=None, exclude=True)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra='ignore'
    )

    def model_post_init(self, __context):
        """يتم تنفيذه بعد الـ initialization"""
        if self.file_path and not self.file_name:
            self.file_name = os.path.basename(self.file_path)
        
        if not self.file_name and self.file_path:
            self.file_name = os.path.basename(self.file_path)

        # بناء page_dict تلقائياً
        if self.pages and self.page_dict is None:
            self.build_page_dict()

    def build_page_dict(self) -> None:
        if self.pages:
            self.page_dict = {page.page_number: page for page in self.pages}

    def get_page(self, page_number: int) -> Optional[RawPage]:
        if self.page_dict is None:
            self.build_page_dict()
        return self.page_dict.get(page_number) if self.page_dict else None

    def get_pages_with_matrices(self) -> List[RawPage]:
        return [page for page in self.pages if page.has_potential_matrix]

    def __str__(self):
        return (f"PDFDocument({self.file_name or 'Unknown'} | "
                f"{self.total_pages} pages | Status: {self.status})")


# ====================== Utility Functions ======================

def create_pdf_document(
    file_path: str,
    pages: List[RawPage],
    status: str = "SUCCESS",
    error_message: Optional[str] = None,
    file_size: Optional[int] = None,
) -> PDFDocument:
    """دالة مساعدة آمنة لإنشاء PDFDocument"""
    
    file_name = os.path.basename(file_path) if file_path else ""
    
    doc = PDFDocument(
        file_path=str(file_path),
        file_name=file_name,
        total_pages=len(pages),
        pages=pages,
        status=status,
        error_message=error_message,
        file_size=file_size,
    )
    return doc


# ====================== Dataclass Version (احتياطي) ======================

@dataclass
class RawPageDC:
    page_number: int
    raw_text: str = ""
    text_length: int = 0
    image_count: int = 0
    has_potential_matrix: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PDFDocumentDC:
    file_path: str = ""
    file_name: str = ""
    total_pages: int = 0
    pages: List[RawPageDC] = field(default_factory=list)
    status: str = "SUCCESS"
    error_message: Optional[str] = None
    processed_at: datetime = field(default_factory=datetime.now)
    file_size: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)