# page_processor.py

"""
PageProcessor - Transforms RawPage into ExtractionResult with matrix extraction
Core component responsible for single page processing in Sovereign Engine.
"""

import re
from typing import List, Dict, Any

from logger import get_logger
from document import RawPage, create_empty_page
from matrix_extractor import MatrixExtractor
from matrix_models import ExtractionResult


class PageProcessor:
    """
    Sovereign Page Processor - Processes individual pages and extracts matrices
    """

    def __init__(self, logger=None):
        self.logger = logger or get_logger("PageProcessor")
        self.matrix_extractor = MatrixExtractor(logger=self.logger)

        self.logger.info("🔧 PageProcessor initialized successfully")

    def process_page(self, raw_page: RawPage, domain: str = "Vehicle_Design") -> ExtractionResult:
        """
        Process a single raw page and return extraction result with matrices.
        """
        if not raw_page or not hasattr(raw_page, 'page_number'):
            self.logger.error("❌ Invalid RawPage object passed")
            return self._create_error_result(0, "Invalid RawPage object", domain)

        page_num = raw_page.page_number
        raw_text = getattr(raw_page, 'raw_text', "") or ""

        self.logger.debug(
            f"🔧 Processing page {page_num} | Domain: {domain} | Text length: {len(raw_text)}"
        )

        try:
            # Extract matrices using MatrixExtractor
            result: ExtractionResult = self.matrix_extractor.extract_from_page(
                raw_text=raw_text,
                page_number=page_num
            )

            if result is None:
                self.logger.warning(f"⚠️ extract_from_page returned None for page {page_num}")
                return self._create_error_result(page_num, "extract_from_page returned None", domain)

            # ====================== Enhance Metadata ======================
            if not hasattr(result, 'metadata') or result.metadata is None:
                result.metadata = {}

            extracted_matrices = getattr(result, 'extracted_matrices', []) or []
            matrices_count = len(extracted_matrices)

            # Calculate quality statistics
            matrices_quality = [
                getattr(m, 'quality_score', getattr(m, 'quality', 0)) 
                for m in extracted_matrices
            ]
            avg_quality = round(sum(matrices_quality) / len(matrices_quality), 2) if matrices_quality else 0.0
            max_quality = max(matrices_quality) if matrices_quality else 0.0

            # Update metadata
            result.metadata.update({
                "original_length": getattr(raw_page, 'text_length', len(raw_text)),
                "image_count": getattr(raw_page, 'image_count', 0),
                "had_potential_matrix": getattr(raw_page, 'has_potential_matrix', False),
                "domain": domain,
                "page_source": "pdf_reader",
                "has_dense_numbers": self._has_dense_numbers(raw_text),
                "matrices_count": matrices_count,
                "avg_matrix_quality": avg_quality,
                "max_matrix_quality": max_quality,
            })

            # ====================== Logging ======================
            status_icon = "🟢" if getattr(result, 'technical_score', 50) >= 75 else \
                         "🟡" if getattr(result, 'technical_score', 50) >= 55 else "🔴"

            self.logger.info(
                f"{status_icon} Page {page_num:3d} | "
                f"Type: {getattr(result, 'content_type', 'GENERAL'):<18} | "
                f"Score: {getattr(result, 'technical_score', 50):3d} | "
                f"Matrices: {matrices_count:2d} | "
                f"AvgQ: {avg_quality:.1f} | "
                f"Domain: {domain}"
            )

            return result

        except Exception as e:
            self.logger.error(f"❌ Error processing page {page_num}: {e}", exc_info=True)
            return self._create_error_result(page_num, str(e), domain)

    # ====================== Helper Methods ======================
    def _has_dense_numbers(self, text: str) -> bool:
        """Detect if page has dense numerical content"""
        if not text:
            return False
        numbers = re.findall(r'[-+]?(?:\d*\.\d+|\d+)', text)
        return len(numbers) > 25

    def _create_error_result(self, page_num: int, error_msg: str, domain: str) -> ExtractionResult:
        """Create a standardized error result"""
        try:
            # Try using the utility function first
            empty = create_empty_page(page_num)
            
            if isinstance(empty, ExtractionResult):
                empty.technical_score = 20
                empty.content_type = "ERROR"
                if hasattr(empty, 'metadata'):
                    empty.metadata["error"] = error_msg
                    empty.metadata["domain"] = domain
                return empty

        except Exception as inner_e:
            self.logger.debug(f"Error using create_empty_page: {inner_e}")

        # Ultimate safe fallback
        return ExtractionResult(
            page_number=page_num,
            clean_text="",
            technical_score=20,
            content_type="ERROR",
            potential_matrices_count=0,
            extracted_matrices=[],
            metadata={
                "error": error_msg,
                "domain": domain,
                "creation_method": "direct_fallback"
            }
        )