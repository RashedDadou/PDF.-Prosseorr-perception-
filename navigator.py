# navigator.py
"""
SovereignNavigator - محرك البحث الدلالي الذكي
النسخة النهائية - متكامل مع الشبكة الاستدلالية
"""

import time
from typing import List, Optional

from logger import get_logger
from config import SovereignConfig
from memory_manager import MemoryManager
from search_models import SearchResult


class SovereignNavigator:
    """
    [الملاح السيادي] - محرك البحث الدلالي والذكي (Semantic Search + Hybrid)
    """

    def __init__(self, memory_manager: MemoryManager, logger=None):
        self.logger = logger or get_logger("Navigator")
        self.config = SovereignConfig
        self.memory = memory_manager

        self.logger.info("🧭 SovereignNavigator تم تهيئته بنجاح")

    def navigate(self, query: str, top_k: int = 6, min_score: float = 0.42, 
                 preferred_type: Optional[str] = None) -> List[SearchResult]:
        """
        البحث الدلالي الرئيسي مع الاستفادة الكاملة من MemoryManager + الشبكة الاستدلالية
        """
        start_time = time.time()
        
        if not query or not query.strip():
            self.logger.warning("⚠️ تم استدعاء navigate بـ query فارغ")
            return []

        self.logger.info(f"🔍 بحث دلالي: '{query[:70]}...' | top_k={top_k}")

        try:
            # استخدام MemoryManager.navigate() (يحتوي على Hubs Boost)
            raw_results = self.memory.navigate(
                query=query, 
                top_k=top_k * 2, 
                min_score=min_score * 0.7
            )

            results: List[SearchResult] = []

            for item in raw_results:
                page_num = item.get("page_number") or item.get("page") or 0

                result = SearchResult(
                    page_number=int(page_num),
                    content=str(item.get("content", ""))[:820],
                    score=round(float(item.get("score", 0)), 4),
                    semantic_similarity=float(item.get("semantic_similarity", 0.0)),
                    technical_score=int(item.get("technical_score", 50)),
                    content_type=str(item.get("content_type", "GENERAL_TECHNICAL")),
                    matrices_count=int(item.get("matrices_count", 0)),
                    rank=0,
                    metadata={
                        **(item.get("metadata") or {}),
                        "cache_hit": True,
                        "hub_boost": float(item.get("hub_boost", 0.0)),
                        "search_method": "hybrid_inference"
                    }
                )
                results.append(result)

            # ترتيب نهائي
            results.sort(key=lambda x: x.score, reverse=True)
            final_results = results[:top_k]

            for idx, res in enumerate(final_results):
                res.rank = idx + 1

            execution_time = round(time.time() - start_time, 3)

            self.logger.info(
                f"✅ Navigate نجح | نتائج: {len(final_results)} | "
                f"أعلى درجة: {final_results[0].score if final_results else 0:.3f} | "
                f"زمن: {execution_time}s"
            )

            return final_results

        except Exception as e:
            self.logger.error(f"🛑 خطأ في البحث الدلالي (Navigator): {e}", exc_info=True)
            self.logger.warning("↩️ العودة إلى Keyword Search")
            return self._simple_keyword_search(query, top_k)

    def _simple_keyword_search(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """بحث نصي احتياطي - نسخة متقدمة"""
        if not query or not self.memory.vector_store.cache:
            return []

        results = []
        query_lower = query.lower().strip()
        query_words = set(query_lower.split())

        for page_num, data in self.memory.vector_store.cache.items():
            content = data.get("content", "")
            if not content or len(content) < 15:
                continue

            content_lower = content.lower()
            score = 0.0

            if query_lower in content_lower:
                score += 50
            else:
                word_matches = sum(1 for word in query_words if word in content_lower)
                score += word_matches * 22

            if content_lower.startswith(query_lower) or query_lower in content_lower[:350]:
                score += 28

            tech_score = data.get("technical_score", 40)
            score += (tech_score - 30) * 0.45

            matrices = data.get("matrices_count", 0)
            if matrices > 0:
                score += matrices * 15

            # تعزيز من الشبكة
            page_keywords = data.get("keywords", [])
            if page_keywords:
                common = sum(1 for kw in page_keywords if kw in query_lower)
                score += common * 10

            if data.get("inference", {}).get("is_hub"):
                score += 18

            if score > 20:
                results.append(SearchResult(
                    page_number=page_num,
                    content=content[:720],
                    score=round(score / 100, 3),
                    semantic_similarity=0.0,
                    technical_score=tech_score,
                    content_type=data.get("content_type", "GENERAL_TECHNICAL"),
                    matrices_count=matrices,
                    rank=0,
                    metadata={
                        "search_type": "keyword",
                        "has_matrices": matrices > 0,
                        "hub_page": bool(data.get("inference", {}).get("is_hub"))
                    }
                ))

        results.sort(key=lambda x: x.score, reverse=True)

        for i, res in enumerate(results[:top_k]):
            res.rank = i + 1

        return results[:top_k]

    def aggregate_context(self, results: List[SearchResult], max_length: int = 12000) -> str:
        """تجميع سياق ذكي للـ RAG"""
        if not results:
            return "لم يتم العثور على مصادر ذات صلة."

        context_blocks = []
        total_length = 0

        for res in results:
            block = f"""📍 [صفحة {res.page_number}] 
نوع المحتوى: {getattr(res, 'content_type', 'GENERAL_TECHNICAL')}
الدرجة: {res.score:.3f}
"""

            if getattr(res, 'matrices_count', 0) > 0:
                block += f"عدد المصفوفات: {res.matrices_count}\n"
            
            if getattr(res, 'technical_score', 0) >= 75:
                block += f"الدرجة التقنية: {res.technical_score} ⭐\n"

            block += f"\n{res.content.strip()}\n"
            block += "-" * 85 + "\n"

            block_length = len(block)
            if total_length + block_length > max_length:
                remaining = max_length - total_length
                if remaining > 500:
                    truncated = block[:remaining].rsplit('\n', 1)[0]
                    block = truncated + "\n... [تم تقصير السياق]"
                    context_blocks.append(block)
                break

            context_blocks.append(block)
            total_length += block_length

        full_context = "\n".join(context_blocks)

        if not full_context.strip():
            return "لم يتم العثور على سياق كافٍ للإجابة."

        return full_context