# archive_manager.py

"""
ArchiveManager - Sovereign Archiving System
Responsible for saving content dumps, batches, and managing long-term storage.
"""

import json
import time
from pathlib import Path
from typing import Dict, Any, Optional, List

from logger import get_logger
from config import SovereignConfig


class ArchiveManager:
    """
    Sovereign Archive Manager - Handles persistent storage of processed documents
    """

    def __init__(self, logger=None):
        self.logger = logger or get_logger("ArchiveManager")
        self.config = SovereignConfig
        self.archive_dir: Path = self.config.ARCHIVE_DIR
        
        try:
            self.archive_dir.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"📦 ArchiveManager initialized | Path: {self.archive_dir}")
        except Exception as e:
            self.logger.error(f"❌ Failed to create archive directory: {e}")

    def save_content_dump(self, pages_data: Dict[int, Any], document_name: str = "document") -> bool:
        """Save a complete content dump of all processed pages"""
        try:
            if not pages_data:
                self.logger.warning(f"⚠️ Attempted to save empty content dump for {document_name}")
                return False

            self.logger.info(f"💾 Saving content dump for '{document_name}' | Pages: {len(pages_data)}")

            content_dump = {}
            for page_num, data in pages_data.items():
                content_dump[str(page_num)] = {
                    "text": data.get("content", "")[:2000],
                    "technical_score": data.get("technical_score", 50),
                    "content_type": data.get("content_type", "GENERAL_TECHNICAL"),
                    "matrices_count": data.get("matrices_count", 0),
                    "perception_score": data.get("perception_score", 0),
                    "timestamp": data.get("timestamp", time.time()),
                    "metadata": data.get("metadata", {})
                }

            # Create safe filename
            safe_name = "".join(c if c.isalnum() or c in "._-" else "_" for c in str(document_name).strip())
            if not safe_name:
                safe_name = "document"

            # Save main dump + document-specific dump
            main_path = self.archive_dir / "content_dump.json"
            doc_path = self.archive_dir / f"content_dump_{safe_name}.json"

            for path in [main_path, doc_path]:
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(content_dump, f, ensure_ascii=False, indent=2)

            self.logger.info(
                f"✅ Content dump saved successfully | {len(content_dump)} pages | Document: {document_name}"
            )
            return True

        except Exception as e:
            self.logger.error(f"❌ Failed to save content dump for {document_name}: {e}", exc_info=True)
            return False

    def save_batch(self, batch_pages: Dict[int, Any], batch_id: str) -> bool:
        """Save a processing batch in a dedicated folder"""
        try:
            safe_batch_id = "".join(c if c.isalnum() or c in "._-" else "_" for c in str(batch_id))
            batch_dir = self.archive_dir / f"batch_{safe_batch_id}"
            batch_dir.mkdir(parents=True, exist_ok=True)

            # Save full batch data
            with open(batch_dir / "batch_data.json", "w", encoding="utf-8") as f:
                json.dump(batch_pages, f, ensure_ascii=False, indent=2)

            # Save metadata
            total_matrices = sum(p.get("matrices_count", 0) for p in batch_pages.values())

            metadata = {
                "batch_id": str(batch_id),
                "page_count": len(batch_pages),
                "created_at": time.time(),
                "matrices_count": total_matrices,
                "document_name": str(batch_id).split('_')[0] if '_' in str(batch_id) else str(batch_id)
            }

            with open(batch_dir / "metadata.json", "w", encoding="utf-8") as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)

            self.logger.info(
                f"📦 Batch '{batch_id}' archived successfully | "
                f"Pages: {len(batch_pages)} | Matrices: {total_matrices}"
            )
            return True

        except Exception as e:
            self.logger.error(f"❌ Failed to archive batch {batch_id}: {e}", exc_info=True)
            return False

    def load_content_dump(self, document_name: Optional[str] = None) -> Dict:
        """Load content dump (main or specific document)"""
        try:
            if document_name:
                safe_name = "".join(c if c.isalnum() or c in "._-" else "_" for c in Path(document_name).stem)
                path = self.archive_dir / f"content_dump_{safe_name}.json"
            else:
                path = self.archive_dir / "content_dump.json"

            if not path.exists():
                self.logger.debug(f"⚠️ Content dump not found: {path}")
                return {}

            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)

        except Exception as e:
            self.logger.warning(f"⚠️ Failed to load content dump: {e}")
            return {}

    def list_archived_batches(self) -> List[Dict[str, Any]]:
        """List all archived batches"""
        try:
            batches = []
            for batch_dir in self.archive_dir.glob("batch_*"):
                meta_path = batch_dir / "metadata.json"
                if meta_path.exists():
                    try:
                        with open(meta_path, "r", encoding="utf-8") as f:
                            metadata = json.load(f)
                            batches.append(metadata)
                    except Exception:
                        continue
            return sorted(batches, key=lambda x: x.get("created_at", 0), reverse=True)
        except Exception as e:
            self.logger.error(f"Error listing archived batches: {e}")
            return []

    def get_archive_stats(self) -> Dict[str, Any]:
        """Return archive statistics"""
        try:
            total_batches = len(list(self.archive_dir.glob("batch_*")))
            dump_files = len(list(self.archive_dir.glob("content_dump*.json")))
            
            total_size = sum(f.stat().st_size for f in self.archive_dir.rglob("*") if f.is_file())
            
            return {
                "total_batches": total_batches,
                "content_dump_files": dump_files,
                "archive_size_mb": round(total_size / (1024 * 1024), 2),
                "last_updated": max(
                    (f.stat().st_mtime for f in self.archive_dir.rglob("*") if f.is_file()), 
                    default=0
                )
            }
        except Exception as e:
            self.logger.error(f"Failed to calculate archive stats: {e}")
            return {"error": "Failed to calculate archive statistics"}