# pdf_reader.py

import fitz  # PyMuPDF
from pathlib import Path
from typing import List, Optional, Dict, Any
import re
from datetime import datetime

from logger import get_logger
from pdf_models import RawPage, PDFDocument, create_pdf_document
from config import SovereignConfig

# استيراد OCRDuty
from matrix_OCR_duty import OCRDuty

# ====================== OCR Global Flag ======================
OCR_AVAILABLE = False
try:
    import pytesseract
    from PIL import Image
    import io
    OCR_AVAILABLE = True
except ImportError:
    pass
# ======================================================


class SovereignPDFReader:
    """
    [قارئ PDF السيادي] - قارئ قوي ومتسامح مع مستندات H-Point التقنية
    """

    def __init__(self, logger=None):
        self.logger = logger or get_logger("PDFReader")
        self.logger.info("📖 SovereignPDFReader تم تهيئته بنجاح")
        
        if OCR_AVAILABLE:
            self.ocr_duty = OCRDuty(self.logger)
        else:
            self.ocr_duty = None
            self.logger.warning("⚠️ مكتبة pytesseract غير موجودة - OCR غير متاح")

    def open_document(self, pdf_path: str) -> PDFDocument:
        """
        فتح وقراءة ملف PDF بشكل كامل مع OCR ذكي
        """
        start_time = datetime.now()
        pdf_path_obj = Path(pdf_path)
        file_path_str = str(pdf_path_obj.absolute())

        if not pdf_path_obj.exists():
            self.logger.error(f"❌ الملف غير موجود: {pdf_path}")
            return PDFDocument(
                file_path=file_path_str,
                file_name=pdf_path_obj.name,
                status="ERROR",
                error_message=f"File not found: {pdf_path}",
                pages=[],
                total_pages=0
            )

        try:
            doc = fitz.open(str(pdf_path_obj))
            total_pages = len(doc)
            
            self.logger.info(f"📂 تم فتح الملف: {pdf_path_obj.name} | {total_pages} صفحة")

            pages: List[RawPage] = []

            for page_num in range(total_pages):
                page = doc[page_num]
                page_number = page_num + 1

                # ====================== استراتيجيات استخراج النص ======================
                raw_text = page.get_text("text").strip()

                # محاولات احتياطية إذا كان النص ضعيف
                if len(raw_text) < 120:
                    try:
                        text_dict = page.get_text("dict")
                        if isinstance(text_dict, dict):
                            raw_text = self._extract_text_from_dict(text_dict)
                    except:
                        pass

                if len(raw_text) < 100:
                    try:
                        raw_text = page.get_text("text", sort=True).strip()
                    except:
                        pass

                if len(raw_text) < 70:
                    try:
                        html = page.get_text("html")
                        if isinstance(html, bytes):
                            html = html.decode('utf-8', errors='ignore')
                        
                        raw_text = re.sub(r'<[^>]+>', ' ', html)
                        raw_text = re.sub(r'\s+', ' ', raw_text).strip()
                    except Exception as html_err:
                        self.logger.debug(f"get_text('html') فشل على صفحة {page_number}: {html_err}")
                        pass

                # ====================== OCR ذكي ======================
                if len(raw_text) < 180 and self.ocr_duty is not None:
                    try:
                        ocr_text = self.ocr_duty.extract_text(page, page_number, prefer_table_mode=True)
                        
                        if len(ocr_text) > len(raw_text) * 1.2:
                            raw_text = ocr_text
                            self.logger.info(f"    📸 OCR Smart نجح على الصفحة {page_number} | طول: {len(raw_text)}")
                    except Exception as ocr_err:
                        self.logger.debug(f"OCR فشل على صفحة {page_number}: {ocr_err}")

                # ====================== تنظيف خاص بالمصفوفات ======================
                if (len(re.findall(r'\d', raw_text)) > 40 and 
                    self.ocr_duty is not None and 
                    hasattr(self.ocr_duty, '_preprocess_for_matrix_detection')):
                    
                    try:
                        raw_text = self.ocr_duty._preprocess_for_matrix_detection(raw_text, page_number)
                    except Exception as preprocess_err:
                        self.logger.debug(f"⚠️ Preprocess for matrix failed on page {page_number}: {preprocess_err}")

                # ====================== باقي المعالجة ======================
                text_length = len(raw_text)
                image_count = len(page.get_images())

                has_potential_matrix = self._has_matrix_signals(raw_text) if hasattr(self, '_has_matrix_signals') else False

                raw_page = RawPage(
                    page_number=page_number,
                    raw_text=raw_text,
                    text_length=text_length,
                    image_count=image_count,
                    has_potential_matrix=has_potential_matrix,
                    metadata={
                        "rotation": int(page.rotation),
                        "width": float(page.rect.width),
                        "height": float(page.rect.height),
                        "char_count": len(raw_text),
                        "used_ocr": len(raw_text) > 100 and OCR_AVAILABLE
                    }
                )

                self._debug_page_content(page_number, raw_text, has_potential_matrix)
                pages.append(raw_page)

                if page_number % 30 == 0:
                    self.logger.debug(f"   → تمت معالجة {page_number}/{total_pages} صفحة")

            doc.close()

            execution_time = (datetime.now() - start_time).total_seconds()
            file_size = pdf_path_obj.stat().st_size

            self.logger.info(
                f"✅ تم قراءة {total_pages} صفحة بنجاح | زمن: {execution_time:.2f} ثانية | حجم: {file_size / (1024*1024):.1f} MB"
            )

            return create_pdf_document(
                file_path=file_path_str,
                pages=pages,
                status="SUCCESS",
                file_size=file_size
            )

        except Exception as e:
            self.logger.error(f"❌ خطأ أثناء قراءة PDF {pdf_path_obj.name}: {e}", exc_info=True)
            return PDFDocument(
                file_path=file_path_str,
                file_name=pdf_path_obj.name,
                status="ERROR",
                error_message=str(e),
                pages=[],
                total_pages=0,
                file_size=pdf_path_obj.stat().st_size if pdf_path_obj.exists() else None
            )
            
    def _extract_text_from_dict(self, text_dict: Dict) -> str:
        """استخراج نص متقدم جداً مع تركيز على المصفوفات والجداول (H-Point)"""
        try:
            if not isinstance(text_dict, dict):
                return ""

            blocks = text_dict.get("blocks", [])
            all_lines = []

            for block in blocks:
                block_type = block.get("type")

                if block_type == 0:  # Text Block
                    for line in block.get("lines", []):
                        spans_text = []
                        for span in line.get("spans", []):
                            text = span.get("text", "").strip()
                            if text:
                                spans_text.append(text)
                        
                        if spans_text:
                            # دمج النص داخل السطر مع مسافات طبيعية
                            line_text = " ".join(spans_text)
                            all_lines.append(line_text)

                elif block_type == 1:  # Image Block (قد يحتوي على جداول مصورة)
                    # يمكننا إضافة تعليق لاحقاً
                    continue

            text = "\n".join(all_lines)

            # تنظيف متقدم
            text = re.sub(r' {2,}', ' ', text)           # تقليل المسافات المتعددة
            text = re.sub(r'\n{3,}', '\n\n', text)      # تقليل الأسطر الفارغة
            text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)  # إزالة أحرف تحكم

            return text.strip()

        except Exception as e:
            self.logger.debug(f"خطأ في _extract_text_from_dict: {e}")
            return ""
        
    def _has_matrix_signals(self, text: str) -> bool:
        """كشف فائق الحساسية لوجود مصفوفات، جداول، ومحتوى H-Point"""
        if not text or len(text) < 20:
            return False

        lower = text.lower()
        clean_text = re.sub(r'\s+', ' ', text)

        # ====================== 1. كلمات مفتاحية قوية جداً ======================
        strong_signals = [
            'h-point', 'hip point', 'sg rp', 'sgrp', 'sg-rp', 'design h-point',
            'seating reference point', 'manikin', 'j826', 'sae j826', 'eyellipse',
            'occupant package', 'packaging', 'wheelbase', 'h point',
            'denavit-hartenberg', 'dh parameter'
        ]

        if any(signal in lower for signal in strong_signals):
            return True

        # ====================== 2. أنماط مصفوفات رياضية ======================
        if re.search(r'0\s+0\s+0\s+1', text):
            return True
        if re.search(r'\[\s*[-+]?\d', text) or re.search(r'T:\s*[\[\(]', text):
            return True
        if re.search(r'T\s*=', text):
            return True

        # ====================== 3. كشف الجداول والصفوف الكثيفة (الأهم) ======================
        lines = [line.strip() for line in text.split('\n') if line.strip()]

        dense_lines = 0
        for line in lines:
            numbers = re.findall(r'[-+]?\d*\.?\d+', line)
            
            if len(numbers) >= 5:                    # 5 أرقام أو أكثر في سطر واحد
                dense_lines += 1
                if dense_lines >= 2:                 # سطرين كثيفين = غالباً جدول أو مصفوفة
                    return True

            # نمط أرقام مفصولة بمسافات (مصفوفات)
            if len(numbers) >= 4 and re.search(r'\d\s+\d\s+\d', line):
                return True

        # ====================== 4. كثافة الأرقام العامة ======================
        all_numbers = re.findall(r'[-+]?\d*\.?\d+', clean_text)
        decimals = re.findall(r'\d+\.\d+', clean_text)

        if len(all_numbers) > 40 or len(decimals) > 22:
            return True

        # ====================== 5. أنماط إضافية ======================
        if re.search(r'(?:\d+\.\d+\s+){6,}', clean_text):   # صفوف أرقام طويلة
            return True

        return False
                    
    def _debug_page_content(self, page_number: int, raw_text: str, has_potential: bool):
        """وضع التصحيح (Debug Mode) - مفيد جداً لتشخيص مشاكل استخراج النص"""
        if not getattr(SovereignConfig, 'DEBUG_MODE', False):
            return

        numbers_count = len(re.findall(r'[-+]?\d*\.?\d+', raw_text))
        sample_length = getattr(SovereignConfig, 'DEBUG_SAMPLE_LENGTH', 350)
        sample = raw_text[:sample_length].replace('\n', ' ').strip()

        status = "🟢 POTENTIAL MATRIX" if has_potential else "🔴 No Signal"

        self.logger.info(
            f"🔍 [DEBUG] Page {page_number:3d} | "
            f"Chars: {len(raw_text):4d} | "
            f"Numbers: {numbers_count:3d} | "
            f"Status: {status}"
        )

        # طباعة عينة النص إذا كان يحتوي أرقام أو إشارات
        if numbers_count >= 12 or has_potential or len(raw_text) > 700:
            preview = sample[:280] + ("..." if len(sample) > 280 else "")
            self.logger.info(f"📝 Sample Text: {preview}")
            self.logger.info("-" * 100)