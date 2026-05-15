# matrix_OCR_duty.py

import fitz  # PyMuPDF
from pathlib import Path
from typing import List, Dict, Any, Optional
import re
from datetime import datetime

from logger import get_logger

# ====================== OCR Setup ======================
try:
    import pytesseract
    from PIL import Image
    import io
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    pytesseract = None
# ======================================================


class OCRDuty:
    """
    [OCRDuty السيادي] - مسؤول عن استخراج النص بجودة عالية مع تركيز خاص على المصفوفات والجداول
    """

    def __init__(self, logger=None):
        self.logger = logger or get_logger("OCRDuty")
        self.logger.info("📸 OCRDuty تم تهيئته بنجاح")

    def extract_text(self, page, page_number: int, prefer_table_mode: bool = False) -> str:
        """
        الدالة الرئيسية الموحدة لاستخراج النص باستخدام OCR
        """
        if not OCR_AVAILABLE or pytesseract is None:
            return ""

        try:
            # تحويل الصفحة إلى صورة
            pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
            img = Image.open(io.BytesIO(pix.tobytes("png")))

            # اختيار إعدادات OCR حسب نوع الصفحة
            config = r'--oem 3 --psm 6' if prefer_table_mode else r'--oem 3 --psm 3'
            
            raw_ocr = pytesseract.image_to_string(img, lang='eng+ara', config=config)
            
            if not raw_ocr or len(raw_ocr.strip()) < 30:
                return ""

            # تنظيف وتهيئة خاصة بالمصفوفات
            cleaned_text = self._preprocess_for_matrix_detection(raw_ocr, page_number)

            self.logger.info(f"    📸 OCRDuty Page {page_number} | "
                           f"Raw: {len(raw_ocr)} → Cleaned: {len(cleaned_text)} | "
                           f"TableMode: {prefer_table_mode}")

            return cleaned_text

        except Exception as e:
            self.logger.debug(f"OCRDuty فشل على صفحة {page_number}: {e}")
            return f"[OCR_FAILED_PAGE_{page_number}]"

    def _preprocess_for_matrix_detection(self, text: str, page_number: Optional[int] = None) -> str:
        """
        تنظيف متقدم + إعادة ترميم الجداول باستخدام مسافات ثابتة
        متخصص لمصفوفات H-Point وجداول التحويل
        """
        if not text or len(text) < 20:
            return text

        lines = text.split('\n')
        cleaned_lines = []
        matrix_block = []  # لتجميع أسطر المصفوفة المتتالية

        for line in lines:
            original_line = line
            line = line.strip()
            
            if not line:
                if matrix_block:
                    cleaned_lines.extend(self._reconstruct_table_block(matrix_block))
                    matrix_block = []
                cleaned_lines.append('')
                continue

            # تنظيف أساسي
            line = re.sub(r'0\s+0\s+0\s+1', '0 0 0 1', line)
            line = re.sub(r'[•·∙]', '.', line)

            numbers = re.findall(r'[-+]?\d*\.?\d+', line)
            numbers_count = len(numbers)

            # ====================== كشف الجداول والمصفوفات ======================
            if numbers_count >= 4:
                # تجميع الأسطر المتتالية للمصفوفات
                if numbers_count >= 6 or re.search(r'\d\s+\d\s+\d', line):
                    matrix_block.append(line)
                    continue
                else:
                    if matrix_block:
                        cleaned_lines.extend(self._reconstruct_table_block(matrix_block))
                        matrix_block = []
                    line = "[TABLE_ROW] " + line
            elif matrix_block:
                # انتهى البلوك
                cleaned_lines.extend(self._reconstruct_table_block(matrix_block))
                matrix_block = []

            # علامات إضافية
            if re.search(r'[\[\(]', line) or '0 0 0 1' in line:
                line = "[MATRIX_START] " + line

            cleaned_lines.append(line)

        # معالجة آخر بلوك إذا بقي
        if matrix_block:
            cleaned_lines.extend(self._reconstruct_table_block(matrix_block))

        # ====================== إعادة تجميع النص ======================
        processed_text = '\n'.join(cleaned_lines)
        
        # تنظيف نهائي
        processed_text = re.sub(r'\n{4,}', '\n\n\n', processed_text)
        processed_text = re.sub(r' +([.,:;])', r'\1', processed_text)

        if page_number:
            self.logger.info(f"📋 Pre-processor Page {page_number} | "
                            f"Original: {len(text)} → Processed: {len(processed_text)} | "
                            f"Matrix blocks reconstructed: {processed_text.count('[MATRIX_ROW]')//4}")

        return processed_text.strip()


    def _reconstruct_table_block(self, block_lines: List[str]) -> List[str]:
        """
        إعادة ترميم متقدم للجداول والمصفوفات مع محاذاة ذكية
        """
        if not block_lines:
            return []
        
        if len(block_lines) == 1:
            return ["[MATRIX_ROW] " + block_lines[0]]

        reconstructed = []
        all_numbers = []
        original_positions = []  # لمحاولة اكتشاف محاذاة أصلية

        for line in block_lines:
            # استخراج الأرقام مع مواقعها التقريبية
            nums = re.findall(r'[-+]?\d*\.?\d+', line)
            if nums:
                all_numbers.append([float(x) for x in nums])
                
                # حفظ المواقع التقريبية لكل رقم
                positions = [m.start() for m in re.finditer(r'[-+]?\d*\.?\d+', line)]
                original_positions.append(positions)
            else:
                all_numbers.append([])
                original_positions.append([])

        if not all_numbers or max(len(row) for row in all_numbers) == 0:
            return ["[MATRIX_ROW] " + line for line in block_lines]

        # حساب أكبر عدد أعمدة
        max_cols = max(len(row) for row in all_numbers if row)

        for i, line in enumerate(block_lines):
            nums = re.findall(r'[-+]?\d*\.?\d+', line)
            if not nums:
                reconstructed.append("[MATRIX_ROW] " + line.strip())
                continue

            formatted_parts = []
            
            for j, num in enumerate(nums):
                # محاولة ذكية لتحديد عرض العمود
                width = 14  # عرض افتراضي
                if j < len(original_positions[i]):
                    # يمكن توسيعها لاحقاً بتحليل المسافات بين الأعمدة
                    pass
                
                formatted_parts.append(f"{num:>{width}}")

            # ملء الأعمدة الناقصة
            while len(formatted_parts) < max_cols:
                formatted_parts.append(" " * 14)

            reconstructed_line = "[MATRIX_ROW] " + " | ".join(formatted_parts)
            reconstructed.append(reconstructed_line)

        # إضافة علامة بداية المصفوفة في أول سطر
        if reconstructed:
            reconstructed[0] = "[MATRIX_START] " + reconstructed[0][len("[MATRIX_ROW] "):]

        return reconstructed

    def should_use_table_mode(self, quick_text: str) -> bool:
        """كشف سريع إذا كانت الصفحة تحتاج وضع جداول"""
        if not quick_text:
            return False
        return (self._has_matrix_signals(quick_text) or 
                len(re.findall(r'\d', quick_text)) > 70)

    def _has_matrix_signals(self, text: str) -> bool:
        """نسخة بسيطة للكشف السريع (مؤقتة داخل OCRDuty)"""
        if not text or len(text) < 20:
            return False
        lower = text.lower()
        if any(kw in lower for kw in ['h-point', 'sg rp', 'matrix', '0 0 0 1']):
            return True
        if len(re.findall(r'[-+]?\d*\.?\d+', text)) > 35:
            return True
        return False