# Search_Engine.py

import numpy as np
import re
import random
from typing import List, Dict, Any, Optional

# [IMPORT LINKAGE]: ربط الملاح بمحرك الاستدلال لتفعيل التنبؤ بالهوية
from Generation_Engine import SovereignInferenceEngine

class SovereignNavigator:
    """
    [SOVEREIGN NAVIGATOR]: The context-aware engine responsible for semantic
    navigation, vector search, and dynamic noise adjustment based on schema.
    """
    def __init__(self, network, embedder, logger, inference_engine: SovereignInferenceEngine):
        self.network = network
        self.embedder = embedder
        self.logger = logger
        # [INTEGRATION]: ربط محرك الاستدلال كعقل مدبر للملاحة
        self.inference_engine = inference_engine
        self.seen_content = set()

    def _extract_technical_tokens(self, text: str, schema: Optional[str] = None) -> List[str]:
        """
        [DYNAMIC TOKENIZER]: Extracts technical signatures based on the detected schema.
        Upgraded to fix the 'Positional Argument' error and support global scaling.
        """
        # تصحيح المسافة البادئة (Indentation Fix)
        if schema is None:
            schema = "GENERAL_TECHNICAL"

        import re

        # 1. مكتبة الأنماط المرنة (Flexible Pattern Library)
        # الأنماط الأساسية التي تعمل في كل الظروف (العالمية)
        base_patterns = [
            r'\b[A-Z]{2,}\b',                     # الاختصارات التقنية (Global Acronyms)
            r'[A-Za-z]\d+',                        # المتغيرات المرقمة (General Variables)
            r'[\+\-\*\/=\^√Σ∫]'                    # الرموز الرياضية الأساسية
        ]

        # إضافة أنماط تخصصية بناءً على التنبؤ (Schema-Specific)
        if schema == "MATHEMATICAL_STRUCTURE":
            base_patterns.append(r'[θφαβγδεζηικλμνξοπρστυφχψω]') # الرموز اليونانية للرياضيات
        elif schema == "TECHNICAL_LOG":
            base_patterns.append(r'0x[0-9a-fA-F]+')              # عناوين الذاكرة (Memory Addresses)
        elif schema == "DATA_TABLE":
            base_patterns.append(r'\b\d{2,}\b')                  # المعرفات الرقمية الطويلة

        combined_pattern = "|".join(base_patterns)
        tokens = re.findall(combined_pattern, text)

        # 2. تنظيف وتصفية الرموز (De-duplication)
        unique_tokens = []
        for t in tokens:
            # تصفية النصوص التي قد تكون جزءاً من الأوامر (Echo Filtering)
            if t.lower() not in ["strict", "target", "instruction"]:
                if t not in unique_tokens:
                    unique_tokens.append(t)

        # 3. ضمان وجود أوسمة دائماً لضمان عدم حدوث خطأ في التجميع
        if not unique_tokens:
            unique_tokens = ["RAW_DATA" if any(c.isdigit() for c in text) else "STRUCTURAL_NODE"]

        return unique_tokens

    def infer_navigation_path(self, query: str) -> List[int]:
        """
        [SOVEREIGN PATH-FINDER]: Predicts relevant pages using cross-schema
        semantic tokens and structural weights.
        Upgraded for Global Compatibility (GitHub Standard).
        """
        target_pages = []
        page_scores = {}

        # 1. PREDICT: Identify what we are looking for (The Mission Type)
        # نربط الدالة بنوع الملف المكتشف لتوسيع نطاق البحث
        schema = self.inference_engine.predict_document_schema(query)

        # 2. TOKEN EXTRACTION (Agnostic Version)
        query_tokens = self._extract_technical_tokens(query)

        if not query_tokens:
            # Fallback: If no hard tokens found, use the schema itself as a broad token
            query_tokens = [schema.lower().split('_')[0]]

        # 3. KNOWLEDGE GRAPH CROSS-SCAN
        for token in query_tokens:
            for registered_token, pages in self.network.knowledge_graph.items():
                # Flexible matching to prevent 'Hard-coding' bias
                if token.lower() in registered_token.lower() or registered_token.lower() in token.lower():
                    for p in pages:
                        # Dynamic Weighting based on Schema
                        # نزيد الوزن إذا كان الرمز ينتمي لنفس نوع المستند المكتشف
                        weight = 2 if schema in registered_token.upper() else 1
                        page_scores[p] = page_scores.get(p, 0) + weight

        # 4. RANKING & OPTIMIZATION
        sorted_pages = sorted(page_scores.items(), key=lambda x: x[1], reverse=True)
        target_pages = [p[0] for p in sorted_pages]

        if target_pages:
            self.logger.info(f"📍 [NAVIGATOR]: Global path inferred. Schema: {schema}. Nodes: {target_pages[:5]}")

        return target_pages

    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        [SOVEREIGN NAVIGATOR]: Context-Aware Search Engine.
        Dynamically adjusts 'Stochastic Noise' based on Predicted Schema.
        """
        # 1. PREDICTION LINKAGE (الربط مع دالة التنبؤ)
        # نأخذ عينة من الذاكرة للتنبؤ بنوع المحتوى العام للمستند
        sample_node = list(self.network.cache.values())[0].get('content', '') if self.network.cache else ""
        schema = self.inference_engine.predict_document_schema(sample_node)

        # 2. DYNAMIC NOISE ADJUSTMENT (ضبط الضجيج حسب النوع)
        # الملفات الرياضية تحتاج دقة عالية (ضجيج منخفض)
        # الملفات السردية تحتاج استكشاف أوسع (ضجيج أعلى)
        if schema == "MATHEMATICAL_STRUCTURE":
            noise_factor = 0.005  # High Precision
        elif schema == "GENERAL_TECHNICAL":
            noise_factor = 0.02   # High Exploration
        else:
            noise_factor = 0.01   # Balanced

        # 3. ENCODE & NOISE INJECTION
        query_vector = self.embedder.encode_text(query)
        noise = np.random.normal(0, noise_factor, query_vector.shape)
        query_vector = query_vector + noise

        results = []

        # 4. SIMILARITY CALCULATION
        for node_id, data in self.network.cache.items():
            content_vector = data.get('embedding')
            content = data.get('content', '')

            if content_vector is not None:
                norm_prod = np.linalg.norm(query_vector) * np.linalg.norm(content_vector)
                similarity = np.dot(query_vector, content_vector) / max(1e-9, norm_prod)

                # 5. DYNAMIC PENALTY (عقوبة التكرار المتغيرة)
                # إذا كان المستند جدولياً، نزيد العقوبة لكي لا نكرر نفس الصفوف
                penalty = 0.30 if schema == "DATA_TABLE" else 0.15
                if content in self.seen_content:
                    similarity -= penalty

                results.append({
                    "score": float(similarity),
                    "content": content,
                    "metadata": data.get('metadata', {})
                })

        # 6. DIVERSITY SAMPLING
        results.sort(key=lambda x: x['score'], reverse=True)
        top_tier = results[:10]
        final_selection = random.sample(top_tier, min(len(top_tier), top_k))
        final_selection.sort(key=lambda x: x['score'], reverse=True)

        for res in final_selection:
            self.seen_content.add(res['content'])

        self.logger.info(f"🎯 [NAVIGATOR]: Context synthesized using {schema} protocol.")
        return final_selection

    def aggregate_context(self, matches: List[Dict[str, Any]]) -> str:
        """
        [SOVEREIGN AGGREGATOR]: Merges discovered data blocks with dynamic
        schema-aware tagging. Ensures high-fidelity context for the AI Engine.
        """
        # 1. PREDICT: Identify the global schema for this context batch
        # نأخذ عينة من أول نتيجة لتحديد "هوية" السياق المجمع
        sample_text = matches[0].get('content', '') if matches else ""
        schema = self.inference_engine.predict_document_schema(sample_text)

        context_blocks = []
        for match in matches:
            content = match.get('content', '')
            metadata = match.get('metadata', {})
            page = metadata.get('page', 'Unknown')

            # 2. SCHEMA-AWARE TOKENIZATION:
            # بدلاً من البحث عن الروبوتات، نستخرج الأوسمة بناءً على نوع الملف
            tokens = self._extract_technical_tokens(content, schema)

            # 3. DYNAMIC BLOCK ARCHITECTURE
            # بناء ترويسة احترافية تظهر نوع البيانات المكتشفة (Schema)
            block_header = f"📍 [DISCOVERY_NODE: PAGE {page} | SCHEMA: {schema}]"
            token_line = f"🏷️ [STRUCTURAL_SIGNATURE: {', '.join(tokens[:8])}]"

            # تجميع الكتلة مع ضمان نظافة النص (Sanitization)
            full_block = f"{block_header}\n{token_line}\n{content.strip()}"
            context_blocks.append(full_block)

        # 4. FINAL SYNTHESIS
        separator = "\n\n" + "—" * 40 + "\n"
        return separator + "\n\n".join(context_blocks)
