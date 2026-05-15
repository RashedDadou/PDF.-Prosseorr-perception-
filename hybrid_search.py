# hybrid_search.py

import time
from typing import List

from logger import get_logger
from navigator import SovereignNavigator
from search_models import SearchResponse, SearchResult


class HybridSearch:
    """
    [البحث الهجين السيادي] - يجمع بين البحث الدلالي والكلمات المفتاحية
    """

    def __init__(self, navigator: SovereignNavigator):
        self.navigator = navigator
        self.logger = get_logger("HybridSearch")
        self.logger.info("🔍 HybridSearch تم تهيئته بنجاح")

    def search(self, query: str, top_k: int = 6, min_score: float = 0.35) -> SearchResponse:
        """
        بحث هجين شامل: Semantic + Keyword + Technical Boost
        """
        start = time.time()
        
        if not query or not query.strip():
            self.logger.warning("⚠️ تم استدعاء بحث بـ query فارغ")
            return self._empty_response(query)

        self.logger.info(f"🔍 Hybrid Search: '{query[:80]}...' | top_k={top_k}")

        all_results: List[SearchResult] = []

        # 1. البحث الدلالي (الأولوية الأولى)
        try:
            semantic_results = self.navigator.navigate(
                query=query, 
                top_k=top_k * 2, 
                min_score=min_score
            )
            if semantic_results:
                all_results.extend(semantic_results)
                self.logger.debug(f"✅ Semantic search: {len(semantic_results)} نتيجة")
        except Exception as e:
            self.logger.error(f"❌ خطأ في البحث الدلالي: {e}")

        # 2. Fallback بالكلمات المفتاحية
        if len(all_results) < top_k or self._is_weak_results(all_results, min_score):
            try:
                keyword_results = self.navigator._simple_keyword_search(query, top_k=top_k * 2)
                if keyword_results:
                    all_results.extend(keyword_results)
                    self.logger.debug(f"✅ Keyword fallback: {len(keyword_results)} نتيجة")
            except Exception as e:
                self.logger.debug(f"⚠️ Keyword search failed: {e}")

        # 3. تنظيف التكرارات
        unique_results = self._deduplicate_results(all_results)

        # 4. ترتيب ذكي (Hybrid Score)
        unique_results.sort(
            key=lambda x: getattr(x, 'score', 0) * 0.7 + 
                         (getattr(x, 'technical_score', 50) / 100.0) * 0.3,
            reverse=True
        )
        final_results = unique_results[:top_k]

        # 5. تجميع السياق
        context = self.navigator.aggregate_context(final_results)

        execution_time = round(time.time() - start, 3)

        best_score = final_results[0].score if final_results else 0.0
        self.logger.info(
            f"✅ Hybrid Search completed | "
            f"Results: {len(final_results)} | "
            f"Best Score: {best_score:.3f} | "
            f"Time: {execution_time}s"
        )

        return SearchResponse(
            query=query,
            results=final_results,
            total_found=len(unique_results),
            execution_time=execution_time,
            context_aggregated=context
        )

    def _is_weak_results(self, results: List[SearchResult], min_score: float = 0.35) -> bool:
        """التحقق إذا كانت النتائج ضعيفة (أكثر ذكاءً)"""
        if not results:
            return True
        best_score = max((getattr(r, 'score', 0) for r in results), default=0)
        return best_score < min_score * 1.15   # هامش أكثر مرونة

    def _deduplicate_results(self, results: List[SearchResult]) -> List[SearchResult]:
        """إزالة التكرارات بناءً على رقم الصفحة"""
        seen = set()
        unique = []
        for r in results:
            page = getattr(r, 'page_number', None)
            if page is not None and page not in seen:
                seen.add(page)
                unique.append(r)
        return unique

    def _empty_response(self, query: str) -> SearchResponse:
        """إرجاع رد فارغ"""
        return SearchResponse(
            query=query,
            results=[],
            total_found=0,
            execution_time=0.0,
            context_aggregated=""
        )