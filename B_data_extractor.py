# B_data_extractor.py
import fitz  # PyMuPDF
import re
import logging
from typing import List, Dict, Any, Optional
from collections import OrderedDict

class SovereignDataExtractor:
    """
    [المستخلص السيادي V2.0]:
    محرك متكامل للتشريح والحصاد الإدراكي.
    """
    def __init__(self, chunk_size: int = 1000, overlap: int = 200, logger=None):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.logger = logger if logger else logging.getLogger("EXTRACTOR")

        # 🚀 [التصحيح الحاسم]: إخبار Pylance أن هذا المتغير "ديناميكي"
        # نستخدم Any لإسكات التنبيه والسماح للملف A بحقن المحرك هنا
        self.tillage_engine: Any = None

    # B_data_extractor.py - التعديل الجوهري في دالة process_document

    def process_document(self, pdf_path: str) -> List[Dict[str, Any]]:
        document_structure = []
        try:
            with fitz.open(pdf_path) as doc:
                self.total_pages = len(doc)
                for page_num in range(self.total_pages):
                    page = doc[page_num]

                    # 🚀 [1] تهيئة المتغيرات لضمان عدم وجود UnboundLocalError
                    raw_chunks = []
                    raw_text_input = page.get_text("text") or ""

                    # [2] معالجة النص سواء كان قائمة أو نصاً
                    if isinstance(raw_text_input, list):
                        raw_text = " ".join([str(item) for item in raw_text_input])
                    else:
                        raw_text = str(raw_text_input)

                    clean_text = raw_text.strip()

                    # [3] محاولة استخراج الكتل إذا كان الناتج لا يزال فارغاً
                    if not clean_text:
                        blocks = page.get_text("blocks")
                        raw_text = "\n".join([str(b[4]) for b in blocks if len(b) > 4 and b[4]])
                        clean_text = raw_text.strip()

                    # [4] التقطيع السيادي
                    if clean_text:
                        raw_chunks = self._apply_overlap_chunking(clean_text)
                        # صمام أمان: إذا كان هناك نص وفشل التقطيع، نعتبر الصفحة قطعة واحدة
                        if not raw_chunks:
                            raw_chunks = [clean_text]

                    # [5] بناء الهيكل (هنا raw_chunks دائماً لها قيمة حتى لو [] فارغة)
                    refined_chunks = []
                    for c in raw_chunks:
                        refined_chunks.append({
                            "content": c,
                            "page": page_num + 1,
                            "metadata": {
                                "source": pdf_path,
                                "page": page_num + 1,
                                "type": "technical_chunk"
                            }
                        })

                    page_data = {
                        "page": page_num + 1,
                        "content": clean_text,
                        "chunks": refined_chunks,
                        "metadata": {"page": page_num + 1, "source": pdf_path}
                    }
                    document_structure.append(page_data)

                    if self.tillage_engine and clean_text:
                        self.tillage_engine.harvest(f"P_{page_num+1}", clean_text)

        except Exception as e:
            self.logger.error(f"❌ [EXTRACTOR_ERROR]: {str(e)}")
        return document_structure

    def _sanitize_technical_text(self, text: str) -> str:
        """تنظيف النص من الرموز الغريبة مع الحفاظ على المعادلات."""
        # إزالة المسافات الزائدة والحفاظ على السطور الجديدة للمصفوفات
        text = re.sub(r'[ \t]+', ' ', text)
        return text.strip()

    def _apply_overlap_chunking(self, text: str) -> List[str]:
        """تقطيع يحترم تماسك المعادلات والمصفوفات."""
        if len(text) <= self.chunk_size:
            return [text]

        chunks = []
        # استخدام تقسيم ذكي بناءً على الفقرات لضمان عدم كسر مصفوفة في المنتصف
        paragraphs = text.split('\n')
        current_chunk = ""

        for para in paragraphs:
            if len(current_chunk) + len(para) <= self.chunk_size:
                current_chunk += para + "\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                # الحفاظ على التداخل (Overlap) لضمان استمرارية السياق
                overlap_size = min(len(current_chunk), self.overlap)
                overlap_text = current_chunk[-overlap_size:] if overlap_size > 0 else ""
                current_chunk = overlap_text + para + "\n"

        if current_chunk:
            chunks.append(current_chunk.strip())
        return chunks

    def _extract_technical_tokens(self, text: str) -> List[str]:
        """استخراج التوكنز التقنية والمعادلات الكينماتيكية."""
        patterns = [
            r'\b[A-Z][a-z]{3,}\b',              # Kinematics, Dynamics
            r'\b[a-z]+\d+\b',                   # theta1, q2
            r'\b[A-Z]{1,2}\d{1,2}\b',           # T1, R3
            r'sin|cos|tan|atan2|sqrt',          # الدوال الرياضية
            r'\[[\d\s\.,\-]{5,}\]'              # كشف أنماط المصفوفات البسيطة
        ]

        tokens = []
        for pattern in patterns:
            tokens.extend(re.findall(pattern, text))

        return list(OrderedDict.fromkeys(tokens)) # إزالة التكرار مع الحفاظ على الترتيب
