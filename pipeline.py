# pipeline.py
"""
ProcessingPipeline - The core parallel processing engine of Sovereign System
Handles multi-threaded page processing with robust error handling and reporting.
"""

import time
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from logger import get_logger
from config import SovereignConfig
from page_processor import PageProcessor
from matrix_models import ExtractionResult


class ProcessingPipeline:
    """
    Sovereign Processing Pipeline - Orchestrates parallel page processing
    """

    def __init__(self, logger=None, max_workers: Optional[int] = None):
        self.logger = logger or get_logger("Pipeline")
        self.config = SovereignConfig
        
        self.max_workers = max_workers or getattr(self.config, 'MAX_WORKERS', 6)
        self.page_processor = PageProcessor(logger=self.logger)
        
        self.logger.info(
            f"🚀 ProcessingPipeline initialized | "
            f"Max Workers: {self.max_workers} | "
            f"Default Domain: {self.config.DEFAULT_DOMAIN}"
        )

    def process_document(self, pages_data: Dict[int, Any], domain: Optional[str] = None) -> Dict[str, Any]:
        """
        Process all pages of a document in parallel.
        """
        start_time = time.time()
        
        if domain is None:
            domain = self.config.DEFAULT_DOMAIN

        pages_list = list(pages_data.values())
        total_pages = len(pages_list)

        self.logger.info(f"⚙️ Starting processing of {total_pages} pages | Domain: {domain} | Workers: {self.max_workers}")

        if total_pages == 0:
            return self._build_empty_report(domain)

        # ====================== Parallel Processing ======================
        results: List[ExtractionResult] = []
        processed_count = 0
        errors_count = 0

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_page = {
                executor.submit(
                    self.page_processor.process_page, 
                    page, 
                    domain=domain
                ): page.page_number 
                for page in pages_list
            }

            for future in as_completed(future_to_page):
                page_num = future_to_page[future]
                try:
                    result = future.result()
                    if result is not None:
                        results.append(result)
                        processed_count += 1
                    else:
                        errors_count += 1
                        self.logger.warning(f"⚠️ Page {page_num} returned None")
                except Exception as e:
                    errors_count += 1
                    self.logger.error(f"❌ Error processing page {page_num}: {e}", exc_info=False)

                # Progress logging
                if processed_count % 20 == 0 or processed_count == total_pages:
                    progress = round(processed_count / total_pages * 100, 1)
                    self.logger.info(
                        f"⏳ Progress: {processed_count}/{total_pages} pages | "
                        f"Errors: {errors_count} | Completed: {progress}%"
                    )

        # Sort results by page number
        results.sort(key=lambda x: getattr(x, 'page_number', 0))

        execution_time = time.time() - start_time

        final_report = self._build_processing_report(
            results, execution_time, domain, total_pages, errors_count
        )

        self._log_summary(final_report)

        return final_report

    def _build_empty_report(self, domain: str) -> Dict[str, Any]:
        """Build report for empty document"""
        return {
            "status": "EMPTY",
            "total_pages": 0,
            "processed_pages": 0,
            "statistics": {"total_matrices_extracted": 0},
            "pages": [],
            "execution_time": 0.0,
            "domain": domain,
            "success_rate": 0.0
        }

    def _build_processing_report(self, 
                                results: List[ExtractionResult], 
                                execution_time: float,
                                domain: str,
                                total_pages: int,
                                errors_count: int = 0) -> Dict[str, Any]:
        """Build comprehensive final processing report"""
        
        valid_results = [r for r in results if r is not None]
        processed_count = len(valid_results)

        # Calculate statistics
        total_matrices = sum(
            len(getattr(r, 'extracted_matrices', [])) for r in valid_results
        )
        
        pages_with_matrices = sum(
            1 for r in valid_results if len(getattr(r, 'extracted_matrices', [])) > 0
        )

        technical_scores = [getattr(r, 'technical_score', 0) for r in valid_results]
        avg_technical_score = round(sum(technical_scores) / len(technical_scores), 1) \
                            if technical_scores else 0.0

        avg_matrices_per_page = round(total_matrices / processed_count, 2) if processed_count > 0 else 0.0

        statistics = {
            "total_matrices_extracted": total_matrices,
            "pages_with_matrices": pages_with_matrices,
            "avg_technical_score": avg_technical_score,
            "avg_matrices_per_page": avg_matrices_per_page,
            "pages_with_errors": errors_count,
            "domain": domain
        }

        success_rate = round(processed_count / total_pages * 100, 1) if total_pages > 0 else 0.0

        # Determine overall status
        if processed_count == 0:
            status = "FAILED"
        elif success_rate >= 90 and total_matrices > 0:
            status = "SUCCESS"
        elif success_rate >= 70:
            status = "PARTIAL_SUCCESS"
        else:
            status = "PARTIAL_FAILED"

        return {
            "status": status,
            "total_pages": total_pages,
            "processed_pages": processed_count,
            "statistics": statistics,
            "pages": valid_results,
            "execution_time": round(execution_time, 2),
            "domain": domain,
            "success_rate": success_rate,
            "error_count": errors_count,
            "has_matrices": total_matrices > 0
        }

    def _log_summary(self, report: Dict[str, Any]):
        """Log beautiful final summary"""
        stats = report.get("statistics", {})
        
        total_pages = report.get("total_pages", 0)
        processed = report.get("processed_pages", total_pages)
        success_rate = report.get("success_rate", 0.0)
        execution_time = report.get("execution_time", 0.0)
        
        total_matrices = stats.get("total_matrices_extracted", 0)
        pages_with_matrices = stats.get("pages_with_matrices", 0)
        avg_score = stats.get("avg_technical_score", 0.0)
        avg_matrices = stats.get("avg_matrices_per_page", 0.0)

        # Choose emoji based on result
        if success_rate >= 95 and total_matrices > 0:
            icon = "🎉"
        elif success_rate >= 80:
            icon = "✅"
        elif success_rate >= 60:
            icon = "🟡"
        else:
            icon = "⚠️"

        self.logger.info(
            f"{icon} Pipeline completed | "
            f"Pages: {processed}/{total_pages} | "
            f"Matrices: {total_matrices} | "
            f"Active Pages: {pages_with_matrices} | "
            f"Avg Score: {avg_score} | "
            f"Avg Matrices/Page: {avg_matrices:.2f} | "
            f"Success: {success_rate}% | "
            f"Time: {execution_time:.2f}s"
        )

        if report.get("error_count", 0) > 0:
            self.logger.warning(f"⚠️ {report['error_count']} errors occurred during processing")