# memory_manager.py

"""
MemoryManager - Sovereign Memory & Inference System
النسخة النهائية - الشبكة الاستدلالية الدلالية + دعم استخراج المصفوفات
"""

import re
import time
from typing import Dict, List, Any, Optional
from collections import defaultdict

from logger import get_logger
from config import SovereignConfig
from vector_store import VectorStore
from archive_manager import ArchiveManager
from matrix_models import ExtractionResult


class MemoryManager:
    """
    [مدير الذاكرة السيادي] - الواجهة الموحدة للتخزين، الأرشفة، والشبكة الاستدلالية
    """

    def __init__(self, logger=None):
        self.logger = logger or get_logger("MemoryManager")
        self.config = SovereignConfig
        
        self.vector_store = VectorStore(logger=self.logger)
        self.archive = ArchiveManager(logger=self.logger)
        
        # Current processing batch
        self.current_batch: Dict[int, Dict[str, Any]] = {}
        
        # All processed documents metadata
        self.documents: Dict[str, Dict[str, Any]] = {}
        
        # الشبكة الاستدلالية
        self.inference_hubs = None
        self.page_relations = None
        self.strong_hubs = None

        self.logger.info("🧠 MemoryManager تم تهيئته بنجاح | شبكة استدلالية نشطة")

    def set_embedder(self, embedder):
        """ربط الـ Embedder بالـ VectorStore"""
        try:
            self.vector_store.set_embedder(embedder)
            self.logger.info("✅ Embedder مرتبط بـ VectorStore بنجاح")
        except Exception as e:
            self.logger.error(f"❌ فشل ربط Embedder: {e}")

    # ====================== إضافة الصفحات ======================
    def add_processed_page(self, page_num: int, result: ExtractionResult, embedding: Optional[Any] = None):
        """إضافة صفحة + بناء الشبكة + إثراء VectorStore"""
        try:
            self.vector_store.add_page(page_num, result, embedding)

            matrices_count = len(getattr(result, 'extracted_matrices', []))
            extracted_matrices = getattr(result, 'extracted_matrices', [])

            page_data = {
                "content": getattr(result, 'clean_text', '')[:1800],
                "technical_score": getattr(result, 'technical_score', 50),
                "content_type": getattr(result, 'content_type', "GENERAL_TECHNICAL"),
                "matrices_count": matrices_count,
                "perception_score": getattr(result, 'metadata', {}).get("perception_score", 0),
                "domain": getattr(result, 'metadata', {}).get("domain", self.config.DEFAULT_DOMAIN),
                "timestamp": time.time(),
                "metadata": getattr(result, 'metadata', {}),
                "keywords": self._extract_important_keywords(getattr(result, 'clean_text', '')),
                "matrix_signatures": [m.quality_score for m in extracted_matrices] if extracted_matrices else [],
                "has_strong_matrix": any(m.quality_score >= 70 for m in extracted_matrices) if extracted_matrices else False
            }

            self.current_batch[page_num] = page_data

            # بناء الشبكة الاستدلالية
            if matrices_count > 0 or page_data["technical_score"] >= 70:
                self._add_to_inference_network(page_num, page_data)

                # إثراء VectorStore
                self.vector_store.enrich_page(page_num, {
                    "is_hub": True,
                    "hub_keywords": page_data["keywords"][:6],
                    "relations": self.page_relations.get(page_num, []) if self.page_relations else [],
                    "strong_matrix": page_data["has_strong_matrix"]
                })

            log_msg = f"📄 Page {page_num:3d} → {matrices_count} matrices"
            self.logger.info(log_msg) if matrices_count > 0 else self.logger.debug(log_msg)

        except Exception as e:
            self.logger.error(f"❌ فشل إضافة صفحة {page_num}: {e}", exc_info=True)

    # ====================== الشبكة الاستدلالية ======================
    def _extract_important_keywords(self, text: str, top_n: int = 12) -> List[str]:
        """استخراج كلمات مفتاحية مهمة للشبكة الاستدلالية"""
        if not text or len(text) < 30:
            return []

        lower_text = text.lower()

        patterns = [
            r'\b[a-zA-Z][a-zA-Z0-9-]{3,}\b',
            r'\b(?:h-point|hip.?point|sg.?rp|eyellipse|manikin|hardpoint|wheelbase|track)\b',
            r'\b[A-Z]{2,}\b'
        ]

        words = []
        for pattern in patterns:
            words.extend(re.findall(pattern, lower_text))

        stop_words = {'the', 'and', 'for', 'with', 'this', 'that', 'from', 'page', 
                     'figure', 'table', 'section', 'chapter', 'design', 'vehicle'}
        
        filtered = [w for w in words if w not in stop_words and len(w) >= 3]

        from collections import Counter
        counter = Counter(filtered)
        
        important = []
        for word, count in counter.most_common(top_n * 2):
            if count >= 2 or len(important) < top_n // 2:
                important.append(word)
            if len(important) >= top_n:
                break

        return important[:top_n]

    def _add_to_inference_network(self, page_num: int, page_data: Dict[str, Any]):
        """إضافة صفحة إلى الشبكة الاستدلالية"""
        if self.inference_hubs is None:
            self.inference_hubs = defaultdict(list)
            self.page_relations = defaultdict(list)

        keywords = page_data.get("keywords", [])
        technical_score = page_data.get("technical_score", 50)
        matrices_count = page_data.get("matrices_count", 0)

        for kw in keywords[:10]:
            if not kw or len(kw) < 3:
                continue
            self.inference_hubs[kw].append({
                "page": page_num,
                "score": technical_score,
                "matrices": matrices_count,
                "strength": technical_score * (1 + matrices_count * 0.3)
            })

        # ربط الصفحات المجاورة
        if page_num > 1:
            self.page_relations[page_num].append(page_num - 1)
        if page_num < max(self.current_batch.keys(), default=0):
            self.page_relations[page_num].append(page_num + 1)
            
            
    def _build_final_inference_network(self):
        """بناء الشبكة النهائية قبل الأرشفة"""
        if self.inference_hubs is None:
            self.inference_hubs = defaultdict(list)
            self.page_relations = defaultdict(list)

        self.logger.info("🕸️  بدء بناء الشبكة الاستدلالية النهائية...")

        for page_num, page_data in self.current_batch.items():
            self._add_to_inference_network(page_num, page_data)

        # حساب أقوى Hubs
        hub_strength = {}
        for kw, entries in self.inference_hubs.items():
            if len(entries) < 2:
                continue
            total_strength = sum(e.get("strength", 0) for e in entries)
            hub_strength[kw] = round(total_strength / len(entries), 2)

        sorted_hubs = sorted(hub_strength.items(), key=lambda x: x[1], reverse=True)[:50]
        self.strong_hubs = dict(sorted_hubs)

        self.logger.info(f"✅ تم بناء الشبكة الاستدلالية | Hubs: {len(self.inference_hubs)} | Strong Hubs: {len(self.strong_hubs)}")

    def _boost_with_hubs(self, results: List[Dict], query: str):
        """تعزيز النتائج بالشبكة الاستدلالية"""
        if not self.strong_hubs:
            return

        query_lower = query.lower()
        for item in results:
            page_num = item.get("page_number") or item.get("page")
            if not page_num or page_num not in self.current_batch:
                continue

            page_data = self.current_batch[page_num]
            boost = 0.0

            if "keywords" in page_data:
                common = sum(1 for kw in page_data["keywords"] if kw in self.strong_hubs and kw in query_lower)
                boost += common * 0.22

            if page_data.get("matrices_count", 0) >= 2:
                boost += 0.18
            if page_data.get("technical_score", 0) >= 85:
                boost += 0.15

            if boost > 0:
                current_score = item.get("score", 0)
                item["score"] = round(current_score + boost, 4)
                item["hub_boost"] = round(boost, 3)

    # ====================== البحث ======================
    def navigate(self, query: str, top_k: int = 8, min_score: float = 0.35) -> List[Dict]:
        """بحث هجين مع دعم الشبكة الاستدلالية"""
        if not query or not query.strip():
            return []

        try:
            semantic_results = self.vector_store.search(
                query=query, 
                top_k=top_k * 2, 
                min_score=min_score * 0.65
            )

            if self.strong_hubs and semantic_results:
                self._boost_with_hubs(semantic_results, query)

            if len(semantic_results) < 5 and self.current_batch:
                keyword_results = self._keyword_search(query, top_k * 2)
                semantic_results.extend(keyword_results)

            # تنظيف
            filtered = [item for item in semantic_results if item.get('score', 0) >= min_score]
            filtered.sort(key=lambda x: x.get('score', 0), reverse=True)

            return filtered[:top_k]

        except Exception as e:
            self.logger.error(f"❌ خطأ في MemoryManager.navigate(): {e}", exc_info=True)
            return self._keyword_search(query, top_k)

    def _keyword_search(self, query: str, top_k: int = 10) -> List[Dict]:
        """بحث نصي احتياطي"""
        results = []
        query_lower = query.lower()

        for page_num, data in self.current_batch.items():
            content = data.get("content", "").lower()
            score = sum(1 for word in query_lower.split() if len(word) > 2 and word in content)
            
            if score > 0:
                results.append({
                    "page_number": page_num,
                    "score": score * 8,
                    "content": data.get("content", "")[:500],
                    "matrices_count": data.get("matrices_count", 0),
                    "source": "keyword"
                })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    # ====================== الإنهاء والأرشفة ======================
    def finalize_document(self, document_name: str) -> bool:
        """إنهاء المعالجة وأرشفة الوثيقة"""
        try:
            if not self.current_batch:
                self.logger.warning(f"⚠️ محاولة أرشفة وثيقة فارغة: {document_name}")
                return False

            self.logger.info(f"💾 جاري أرشفة '{document_name}' | {len(self.current_batch)} صفحة")

            self._build_final_inference_network()

            success_dump = self.archive.save_content_dump(self.current_batch, document_name)
            success_batch = self.archive.save_batch(self.current_batch, document_name)

            total_matrices = sum(p.get("matrices_count", 0) for p in self.current_batch.values())

            success = success_dump and success_batch

            self.documents[document_name] = {
                "page_count": len(self.current_batch),
                "matrices_count": total_matrices,
                "timestamp": time.time(),
                "domain": self.config.DEFAULT_DOMAIN,
                "success": success,
                "hubs_count": len(getattr(self, 'strong_hubs', {})),
                "strong_pages": sum(1 for p in self.current_batch.values() if p.get("technical_score", 0) >= 75)
            }

            if success:
                self.logger.info(f"✅ تم أرشفة '{document_name}' بنجاح | مصفوفات: {total_matrices} | Hubs: {len(getattr(self, 'strong_hubs', {}))}")
            else:
                self.logger.warning(f"⚠️ أرشفة جزئية لـ '{document_name}'")

            self.current_batch.clear()
            return success

        except Exception as e:
            self.logger.error(f"❌ فشل إنهاء الوثيقة '{document_name}': {e}", exc_info=True)
            self.current_batch.clear()
            return False

    # ====================== الإحصائيات ======================
    def get_stats(self) -> Dict[str, Any]:
        """إحصائيات شاملة"""
        total_matrices = sum(data.get("matrices_count", 0) for data in self.current_batch.values())
        high_quality_pages = sum(1 for data in self.current_batch.values() if data.get("technical_score", 0) >= 75)
        
        hubs_count = len(getattr(self, 'strong_hubs', {}))

        return {
            "current_batch_pages": len(self.current_batch),
            "current_batch_matrices": total_matrices,
            "high_quality_pages": high_quality_pages,
            "total_documents": len(self.documents),
            "vector_cache_size": self.vector_store.get_cache_size(),
            "inference_hubs": hubs_count,
            "network_density": round(hubs_count / max(len(self.current_batch), 1), 2),
            "avg_matrices_per_page": round(total_matrices / max(len(self.current_batch), 1), 3)
        }

    def clear_all(self):
        """تنظيف كامل"""
        self.vector_store.clear()
        self.current_batch.clear()
        self.documents.clear()
        self.inference_hubs = None
        self.page_relations = None
        self.strong_hubs = None
        self.logger.info("🧹 MemoryManager + VectorStore + Documents + Inference Network تم تنظيفهم بالكامل")