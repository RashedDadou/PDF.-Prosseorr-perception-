# vector_store.py

"""
VectorStore - Sovereign Vector & Embedding Management
النسخة النهائية - متكامل مع الشبكة الاستدلالية
"""

import numpy as np
import time
from typing import List, Dict, Any, Optional
from collections import OrderedDict

from logger import get_logger
from config import SovereignConfig
from matrix_models import ExtractionResult


class VectorStore:
    """
    [متجر المتجهات السيادي] - إدارة Embeddings + Cache ذكية
    """

    def __init__(self, logger=None):
        self.logger = logger or get_logger("VectorStore")
        self.config = SovereignConfig
        
        # OrderedDict لـ LRU Cache
        self.cache: OrderedDict[int, Dict[str, Any]] = OrderedDict()
        
        self.embedder = None
        self.logger.info("🧠 VectorStore تم تهيئته بنجاح")

    def set_embedder(self, embedder):
        """ربط الـ Embedder"""
        self.embedder = embedder
        if embedder and getattr(embedder, 'is_ready', lambda: False)():
            self.logger.info("✅ Embedder مرتبط بـ VectorStore بنجاح")
        else:
            self.logger.warning("⚠️ Embedder مرتبط ولكنه غير جاهز")

    def add_page(self, page_num: int, extraction_result: ExtractionResult, embedding: Optional[np.ndarray] = None):
        """إضافة صفحة إلى الـ Cache"""
        try:
            max_cache = getattr(self.config, 'MAX_CACHE_SIZE', 500)
            
            # LRU Eviction
            if len(self.cache) >= max_cache:
                self.cache.popitem(last=False)

            # توليد Embedding إذا لم يُمرر
            if embedding is None and self.embedder is not None:
                try:
                    text = getattr(extraction_result, 'clean_text', '')
                    if text and len(text.strip()) > 30:
                        embedding = self.embedder.encode([text])[0]
                        if embedding is not None:
                            embedding = embedding / np.linalg.norm(embedding)
                except Exception as e:
                    self.logger.debug(f"⚠️ فشل توليد embedding للصفحة {page_num}: {e}")

            # بناء البيانات
            metadata = getattr(extraction_result, 'metadata', {}) or {}

            data = {
                "content": getattr(extraction_result, 'clean_text', '')[:1600],
                "embedding": embedding,
                "technical_score": getattr(extraction_result, 'technical_score', 50),
                "content_type": getattr(extraction_result, 'content_type', "GENERAL_TECHNICAL"),
                "matrices_count": len(getattr(extraction_result, 'extracted_matrices', [])),
                "perception_score": metadata.get("perception_score", 0),
                "timestamp": time.time(),
                "metadata": metadata,
                "keywords": metadata.get("keywords", [])
            }

            self.cache[page_num] = data

            matrices = data["matrices_count"]
            self.logger.debug(
                f"{'🟢' if matrices > 0 else '⚪'} [CACHE] Page {page_num:3d} | "
                f"Matrices: {matrices} | Embedding: {'✓' if embedding is not None else '✗'}"
            )

        except Exception as e:
            self.logger.error(f"❌ خطأ في add_page({page_num}): {e}", exc_info=True)

    def enrich_page(self, page_num: int, extra_data: Dict[str, Any]) -> bool:
        """إثراء الصفحة بالبيانات الاستدلالية من MemoryManager"""
        if page_num not in self.cache:
            return False

        try:
            data = self.cache[page_num]
            if "inference" not in data:
                data["inference"] = {}

            data["inference"].update({
                "is_hub": extra_data.get("is_hub", False),
                "hub_keywords": extra_data.get("hub_keywords", []),
                "relation_count": len(extra_data.get("relations", [])),
                "strong_matrix": extra_data.get("strong_matrix", False)
            })

            self.logger.debug(f"🔗 [ENRICH] Page {page_num} enriched")
            return True

        except Exception as e:
            self.logger.error(f"❌ فشل إثراء الصفحة {page_num}: {e}")
            return False

    def search(self, query: str, top_k: int = 8, min_score: float = 0.33) -> List[Dict[str, Any]]:
        """بحث دلالي متقدم مع دعم الشبكة الاستدلالية"""
        if not query or not query.strip() or not self.embedder or len(self.cache) == 0:
            return []

        try:
            query_embedding = self.embedder.encode([query])[0]
            query_embedding = query_embedding / np.linalg.norm(query_embedding)

            query_lower = query.lower()
            results = []

            for page_num, data in self.cache.items():
                embedding = data.get("embedding")
                if embedding is None:
                    continue

                similarity = self._cosine_similarity(query_embedding, embedding)

                base_score = similarity * 0.68
                technical_boost = (data.get("technical_score", 50) / 100.0) * 0.32
                hybrid_score = base_score + technical_boost

                # Boost من الشبكة الاستدلالية
                inference = data.get("inference", {})
                if inference.get("is_hub"):
                    hybrid_score += 0.22

                page_keywords = data.get("keywords", []) or inference.get("hub_keywords", [])
                common_keywords = sum(1 for kw in page_keywords if kw in query_lower)
                hybrid_score += common_keywords * 0.09

                if data.get("matrices_count", 0) >= 2:
                    hybrid_score += 0.15

                if hybrid_score < min_score:
                    continue

                results.append({
                    "page_number": page_num,
                    "score": round(float(hybrid_score), 4),
                    "semantic_similarity": round(float(similarity), 4),
                    "content": data.get("content", "")[:650],
                    "technical_score": data.get("technical_score", 50),
                    "matrices_count": data.get("matrices_count", 0),
                    "content_type": data.get("content_type", "GENERAL"),
                    "keywords": page_keywords,
                    "is_hub": inference.get("is_hub", False),
                    "hub_boost": round(common_keywords * 0.09 + (0.22 if inference.get("is_hub") else 0), 3)
                })

            results.sort(key=lambda x: x["score"], reverse=True)
            return results[:top_k]

        except Exception as e:
            self.logger.error(f"❌ VectorStore.search error: {e}", exc_info=True)
            return []

    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Cosine Similarity آمنة"""
        try:
            vec1 = np.asarray(vec1).ravel()
            vec2 = np.asarray(vec2).ravel()
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            if norm1 == 0 or norm2 == 0:
                return 0.0
            return float(np.dot(vec1, vec2) / (norm1 * norm2))
        except:
            return 0.0

    # ====================== دوال مساعدة ======================
    def get_page_data(self, page_num: int) -> Optional[Dict]:
        return self.cache.get(page_num)

    def get_embedding(self, page_num: int) -> Optional[np.ndarray]:
        return self.cache.get(page_num, {}).get("embedding")

    def clear(self):
        self.cache.clear()
        self.logger.info("🧹 VectorStore cache cleared")

    def get_cache_size(self) -> int:
        return len(self.cache)

    def get_stats(self) -> Dict[str, Any]:
        """إحصائيات شاملة"""
        total_matrices = sum(d.get("matrices_count", 0) for d in self.cache.values())
        high_quality = sum(1 for d in self.cache.values() if d.get("technical_score", 0) >= 75)
        
        hub_pages = sum(1 for d in self.cache.values() if d.get("inference", {}).get("is_hub"))

        return {
            "cache_size": len(self.cache),
            "total_matrices_in_cache": total_matrices,
            "high_quality_pages": high_quality,
            "inference_hubs": hub_pages,
            "hub_ratio": round(hub_pages / max(len(self.cache), 1), 3),
            "avg_matrices_per_page": round(total_matrices / max(len(self.cache), 1), 3),
            "embedder_ready": self.embedder is not None
        }