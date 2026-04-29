# Search_Engine.py

import numpy as np
import re
from typing import List, Dict, Any

class SovereignNavigator:
    """
    [الملاح السيادي]: العقل المسؤول عن الملاحة الدلالية، البحث في المتجهات،
    وربط السياق التقني بالذاكرة المخبئية.
    """
    def __init__(self, network, embedder, logger):
        self.network = network
        self.embedder = embedder
        self.logger = logger
        self.seen_content = set() # ذاكرة قصيرة لمنع التكرار في نفس الجلسة

    def _extract_technical_tokens(self, text: str) -> List[str]:
        """
        [التشريح السيادي]: استخراج الرموز الهندسية والكلمات التقنية بدقة عالية.
        تم تطويره ليشمل المعادلات والرموز الرياضية المعقدة.
        """
        # استهداف: الكلمات التقنية، الرموز اليونانية، والمصطلحات المكتوبة بـ CamelCase أو ALL_CAPS
        patterns = [
            r'\b[A-Z]{2,}\b',                      # الاختصارات (مثل ROI, PDF, CEO, DOF)
            r'\b[A-Z][a-z]+[A-Z][a-z]+\b',         # كلمات CamelCase (مثل DataBase, FinalReport)
            r'\b\d+\.?\d*[a-zA-Z]+\b',             # قيم مع وحدات (مثل 50kg, 100km, 200MB)
            r'[\$£€¥]\d+',                         # قيم مالية (للملفات الإدارية)
            r'[A-Za-z]\d+',                        # متغيرات مرقمة (هندسية)
            r'(?i)\b(total|result|status|final|error|critical|summary)\b' # كلمات دلالية عامة
        ]
        combined_pattern = "|".join(patterns)
        tokens = re.findall(combined_pattern, text)

        # تنظيف وتصفية الرموز (إزالة المكرر والحفاظ على الترتيب الأهم)
        unique_tokens = []
        for t in tokens:
            if t not in unique_tokens:
                unique_tokens.append(t)

        return unique_tokens[:15] # العودة بأهم 15 رمزاً فقط لعدم إثقال السياق

    def aggregate_context(self, matches: List[Dict[str, Any]]) -> str:
        """
        [تجميع السيادة]: دمج الكتل النصية مع وسمها تقنياً لبناء صورة ذهنية كاملة للمحرك.
        """
        context_blocks = []
        for match in matches:
            content = match.get('content', '')

            # منع المحرك من "اقتباس" تعليماتنا الخاصة في التقرير
            if "STRICT TARGET" in content or "OPERATIONAL COMMANDS" in content:
                continue

        for match in matches:
            content = match.get('content', '')
            metadata = match.get('metadata', {})
            page = metadata.get('page', '??')

            # استخراج الأوسمة التقنية لهذا المقطع تحديداً
            tokens = self._extract_technical_tokens(content)

            # بناء كتلة سياقية غنية بالبيانات الوصفية
            block_header = f"📍 [ENTRY_POINT: PAGE {page}]"
            token_line = f"🏷️ [TECHNICAL_SIGNATURE: {', '.join(tokens[:8])}]"

            full_block = f"{block_header}\n{token_line}\n{content.strip()}"
            context_blocks.append(full_block)

        return "\n\n" + "—" * 30 + "\n\n".join(context_blocks)

    def infer_navigation_path(self, query: str) -> List[int]:
        """
        [تطوير سيادي]: الملاحة لم تعد تعتمد على الكلمات الحرفية فقط،
        بل أصبحت تفهم "سياق" الملف أياً كان نوعه.
        """
        # 1. استخدام البحث الدلالي (Semantic Search) بدلاً من الرموز فقط
        # إذا فشلت الرموز الحرفية، ننتقل للبحث في المتجهات (Vectors)
        query_vector = self.embedder.encode_text(query)

        # 2. استرجاع الصفحات ذات الصلة من الذاكرة الشبكية مباشرة
        # هذا يضمن أنك ستجد نتائج حتى لو لم يكن هناك Knowledge Graph مبني
        semantic_results = self.network.search_similar_pages(query_vector, top_k=10)

        target_pages = [res['page_num'] for res in semantic_results]

        if not target_pages:
            self.logger.warning(f"⚠️ [NAVIGATOR]: المحرك لم يجد صلة دلالية للاستعلام: {query}")
            return []

        self.logger.info(f"📍 [NAVIGATOR]: تم العثور على {len(target_pages)} صفحة مرتبطة بالمحتوى.")
        return target_pages

    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        [البوصلة السيادية المحدثة]: توجيه دقيق للبيانات مع إلغاء العشوائية لضمان جودة التقرير.
        """
        query_vector = self.embedder.encode_text(query)
        if query_vector is None: return []

        results = []
        for page_num, data in self.network.cache.items():
            content_vector = data.get('embedding')
            content = data.get('content', '')

            if content_vector is not None:
                # حساب التشابه بجيب التمام (Cosine Similarity)
                similarity = np.dot(query_vector, content_vector) / (
                    np.linalg.norm(query_vector) * np.linalg.norm(content_vector)
                )

                # عقوبة التكرار (لضمان تنوع التقرير وعدم تكرار نفس الفقرة)
                if content in self.seen_content:
                    similarity -= 0.15 # تقليل العقوبة قليلاً

                results.append({
                    "score": similarity,
                    "content": content,
                    "metadata": data.get('metadata', {})
                })

        # ترتيب النتائج من الأقوى للأضعف
        results.sort(key=lambda x: x['score'], reverse=True)

        # التصحيح: نأخذ أفضل النتائج مباشرة دون اختيار عشوائي (Determinism)
        # هذا يضمن أن أهم معلومة في الملف ستصل للتقرير دائماً
        final_selection = results[:top_k]

        for res in final_selection:
            self.seen_content.add(res['content'])

        self.logger.info(f"🎯 [NAVIGATOR]: تم استخلاص السياق من أفضل {len(final_selection)} عقد معرفية.")
        return final_selection
