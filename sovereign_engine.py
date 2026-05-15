# sovereign_engine.py

"""
Sovereign Engine - Main Orchestrator
Advanced PDF Matrix Extraction System for Vehicle Design & H-Point Analysis
"""

import time
from pathlib import Path
from typing import Dict, Any

from logger import get_logger
from config import SovereignConfig
from pdf_reader import SovereignPDFReader
from pipeline import ProcessingPipeline
from memory_manager import MemoryManager
from conclusion_engine import ConclusionEngine
from navigator import SovereignNavigator
from hybrid_search import HybridSearch


class SovereignEngine:
    """
    [Sovereign Engine] - The main orchestrator of the entire system
    """

    def __init__(self):
        self.logger = get_logger("SovereignEngine")
        self.config = SovereignConfig
        self.config.create_directories()

        self.logger.info("🚀 Starting Sovereign Engine initialization...")

        try:
            self.logger.info("1/7 → Initializing PDF Reader...")
            self.reader = SovereignPDFReader(self.logger)

            self.logger.info("2/7 → Initializing Processing Pipeline...")
            self.pipeline = ProcessingPipeline(self.logger)

            self.logger.info("3/7 → Initializing Memory Manager...")
            self.memory = MemoryManager(self.logger)

            self.logger.info("4/7 → Initializing Conclusion Engine...")
            self.conclusion = ConclusionEngine(self.logger)

            self.logger.info("5/7 → Initializing Navigator...")
            self.navigator = SovereignNavigator(self.memory, self.logger)

            self.logger.info("6/7 → Initializing Hybrid Search...")
            self.hybrid_search = HybridSearch(self.navigator)

            self.logger.info("7/7 → Initializing Embedder...")
            self._initialize_embedder()

            self.logger.info("✅ Sovereign Engine initialized successfully!")

        except Exception as e:
            self.logger.error(f"🛑 CRITICAL ERROR during initialization: {e}", exc_info=True)
            print(f"🛑 Critical error during initialization: {e}")
            raise

    def _initialize_embedder(self):
        """Initialize Embedder with graceful fallback"""
        try:
            from embedding_logic import SovereignEmbedder
            embedder = SovereignEmbedder(logger=self.logger)
            self.memory.set_embedder(embedder)
            self.logger.info("🧬 Embedder initialized and linked successfully")
        except ImportError:
            self.logger.warning("⚠️ embedding_logic module not found (using fallback mode)")
        except Exception as e:
            self.logger.warning(f"⚠️ Failed to initialize Embedder: {e} (fallback mode active)")

    async def process_pdf(self, pdf_path: str, domain: str = "Vehicle_Design") -> Dict[str, Any]:
        """Process a PDF document and extract matrices"""
        start_time = time.time()
        pdf_name = Path(pdf_path).name

        self.logger.info(f"🚀 Processing started: {pdf_name} | Domain: {domain}")

        try:
            # Read PDF
            pdf_document = self.reader.open_document(pdf_path)

            if pdf_document.status == "ERROR":
                error_msg = pdf_document.error_message or "Failed to open document"
                self.logger.error(f"🛑 Failed to open document: {error_msg}")
                raise Exception(error_msg)

            total_pages = pdf_document.total_pages
            self.logger.info(f"📂 Document opened: {pdf_document.file_name} | {total_pages} pages")

            # Process through pipeline
            self.logger.info(f"⚙️ Processing {total_pages} pages...")

            processing_report = self.pipeline.process_document(
                {page.page_number: page for page in pdf_document.pages},
                domain=domain
            )

            pages_list = processing_report.get("pages", [])

            # Calculate final statistics
            total_matrices = 0
            high_quality_matrices = 0
            pages_with_matrices = 0

            for page_result in pages_list:
                extracted = getattr(page_result, 'extracted_matrices', []) or []
                count = len(extracted)
                total_matrices += count

                if count > 0:
                    pages_with_matrices += 1

                for matrix in extracted:
                    quality = getattr(matrix, 'quality_score', getattr(matrix, 'quality', 0))
                    if quality >= 55:
                        high_quality_matrices += 1

            execution_time = round(time.time() - start_time, 2)

            # Archive the document
            self._archive_document(pages_list, pdf_name)

            # Final logging
            self.logger.info("=" * 80)
            self.logger.info(f"✅ Successfully processed {pdf_name}")
            self.logger.info(f"   • Total Pages               : {total_pages}")
            self.logger.info(f"   • Total Matrices            : {total_matrices}")
            self.logger.info(f"   • Pages with Matrices       : {pages_with_matrices}")
            self.logger.info(f"   • High Quality Matrices     : {high_quality_matrices}")
            self.logger.info(f"   • Total Execution Time      : {execution_time} seconds")
            self.logger.info("=" * 80)

            return {
                "status": "SUCCESS",
                "file_name": pdf_document.file_name,
                "total_pages": total_pages,
                "total_matrices": total_matrices,
                "pages_with_matrices": pages_with_matrices,
                "high_quality_matrices": high_quality_matrices,
                "execution_time": execution_time,
                "report": processing_report
            }

        except Exception as e:
            execution_time = round(time.time() - start_time, 2)
            self.logger.error(f"🛑 Failed to process {pdf_name} after {execution_time}s: {e}", exc_info=True)
            
            return {
                "status": "ERROR",
                "file_name": pdf_name,
                "error": str(e),
                "execution_time": execution_time
            }

    def _archive_document(self, pages_list: list, pdf_name: str):
        """Helper to archive processed document"""
        try:
            if hasattr(self.memory, 'archive') and hasattr(self.memory.archive, 'save_content_dump'):
                content_dump = {}
                for page_result in pages_list:
                    page_num = getattr(page_result, 'page_number', None)
                    if page_num is None:
                        continue
                    content_dump[page_num] = {
                        "content": getattr(page_result, 'clean_text', ''),
                        "technical_score": getattr(page_result, 'technical_score', 50),
                        "content_type": getattr(page_result, 'content_type', "GENERAL_TECHNICAL"),
                        "matrices_count": len(getattr(page_result, 'extracted_matrices', [])),
                        "metadata": getattr(page_result, 'metadata', {})
                    }
                
                self.memory.archive.save_content_dump(content_dump, pdf_name)
                self.logger.info(f"💾 Content dump archived for {pdf_name}")
        except Exception as e:
            self.logger.warning(f"⚠️ Archiving failed: {e}")

    async def query(self, question: str, top_k: int = 6) -> Dict[str, Any]:
        """Intelligent RAG query using Hybrid Search"""
        start = time.time()
        try:
            self.logger.info(f"🔍 Searching for: {question[:80]}...")

            search_response = self.hybrid_search.search(question, top_k=top_k)
            context = getattr(search_response, 'context_aggregated', "")

            answer = f"Based on {len(getattr(search_response, 'results', []))} sources:\n\n{context[:900]}..." \
                     if context else "I couldn't find sufficient relevant information in the document."

            execution_time = round(time.time() - start, 3)

            return {
                "query": question,
                "answer": answer,
                "sources": [
                    {
                        "page": getattr(r, 'page_number', None),
                        "score": getattr(r, 'score', None),
                        "content_type": getattr(r, 'content_type', None)
                    }
                    for r in getattr(search_response, 'results', [])
                ],
                "total_sources": len(getattr(search_response, 'results', [])),
                "execution_time": execution_time,
                "context_length": len(context)
            }

        except Exception as e:
            self.logger.error(f"❌ Error in query(): {e}", exc_info=True)
            return {
                "query": question,
                "answer": "An error occurred while searching. Please try again.",
                "error": str(e),
                "execution_time": round(time.time() - start, 3)
            }

    def get_status(self) -> Dict[str, Any]:
        """Return current engine status"""
        try:
            return {
                "status": "READY",
                "cache_size": len(getattr(getattr(self.memory, 'vector_store', None), 'cache', {})),
                "total_documents": len(getattr(self.memory, 'documents', {})),
                "embedder_ready": getattr(self.memory.vector_store, 'embedder', None) is not None,
                "components": {
                    "reader": hasattr(self, 'reader'),
                    "pipeline": hasattr(self, 'pipeline'),
                    "memory": hasattr(self, 'memory'),
                    "conclusion": hasattr(self, 'conclusion'),
                    "navigator": hasattr(self, 'navigator'),
                    "hybrid_search": hasattr(self, 'hybrid_search')
                }
            }
        except Exception as e:
            self.logger.warning(f"⚠️ Error getting status: {e}")
            return {"status": "DEGRADED", "error": str(e)}