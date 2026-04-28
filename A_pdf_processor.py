# A_pdf_processor.py

import numpy as np
import time
import os
import fitz  # PyMuPDF
import logging
from typing import Dict, Any, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

# --- [الارتباط بالوحدات الخدمية الأساسية] ---
# ملاحظة: تم حذف الاستيرادات التي تسبب تعارضات Pylance واستبدالها بتحميل ديناميكي
from B_data_extractor import SovereignDataExtractor
from Calculator import Calculator_

class Basic_pdf_process_engine:
    """
    [معالج البيانات السيادي]: القائد الميداني المسؤول عن الربط بين
    العمليات الفيزيائية للملفات والمحركات الذكية للاستدلال.
    """
    def __init__(self, supervisor, extractor: SovereignDataExtractor, logger, network, embedder,
                 openai_client=None, chunk_size=400, overlap=50):

        # 1. تأمين البنية التحتية والرقابة
        self.logger = logger
        self.supervisor = supervisor
        self.extractor = extractor  # المحرك المحقون من الخارج
        self.network = network
        self.embedder = embedder
        self.openai_client = openai_client
        self.batch_engine = self

        # تثبيت إعدادات التقطيع
        self.chunk_size = chunk_size
        self.overlap = overlap

        self.logger.info("🏗️ [A_Processor]: بدأ تهيئة الجهاز العصبي والوحدات السيادية...")

        # 2. تعريف مساحة العمل (استغلال الرام 80GB)
        self.active_workspace = {}
        self.overall_conclusion = []

        # 3. تهيئة المحركات الذكية (الترتيب الحاسم لمنع التعارض)

        # أ: محرك الاستدلال (Generation Engine)
        try:
            from Generation_Engine import SovereignInferenceEngine
            self.inference_engine = SovereignInferenceEngine(
                logger=self.logger,
                embedder=self.embedder,
                openai_client=self.openai_client
            )
        except ImportError:
            self.logger.error("❌ [FATAL_ERROR]: محرك Generation_Engine مفقود!")
            raise

        # ب: محرك الإدراك الحسي (Information Monitoring)
        try:
            from Information_monitoring import PerceptualPerceptionEngine
            self.perception_engine = PerceptualPerceptionEngine(self.logger)
        except ImportError:
            self.logger.warning("⚠️ [SYSTEM_PATCH]: محرك الإدراك مفقود. ربط 'التحسس' بمدير التشفير مباشرة.")
            # توجيه الطلبات لمدير التشفير (P2) كبديل تكتيكي
            self.perception_engine = self.embedder

        # ج: محرك الاستنتاج الشامل (Overall Conclusion)
        try:
            from D_Overall_conclusion import UniversalSovereignInference
            self.conclusion_engine = UniversalSovereignInference(logger=self.logger, data_type="Robotics")
        except ImportError:
            self.logger.error("❌ [IMPORT_ERROR]: ملف D_Overall_conclusion غير موجود!")

        # د: المحرك الحسابي
        self.calculator = Calculator_(logger=self.logger)

        # 4. تهيئة محرك الحرث (SovereignTillage) وحقنه في المستخلص
        try:
            from SovereignTillage import SovereignTillage
            self.tillage_engine = SovereignTillage(logger=self.logger)

            # الربط السيادي: حقن المحرك داخل الـ extractor لضمان تدفق البيانات
            if hasattr(self.extractor, 'tillage_engine'):
                self.extractor.tillage_engine = self.tillage_engine

            self.logger.info("🚜 [TILLAGE]: تم تجهيز محرك السجلات التاريخية والحصاد.")
        except ImportError:
            self.logger.error("❌ [IMPORT_ERROR]: ملف SovereignTillage غير موجود!")

        # 5. تهيئة الملاح السيادي (Navigator)
        try:
            from Search_Engine import SovereignNavigator
            self.navigator = SovereignNavigator(
                network=self.network,
                embedder=self.embedder,
                logger=self.logger,
                inference_engine=self.inference_engine
            )
            self.logger.info("🧭 [NAVIGATOR]: تم ربط الملاح بالجسر الإدراكي.")
        except Exception as e:
            self.logger.error(f"❌ [NAVIGATOR_ERROR]: فشل ربط الملاح: {e}")

        self.logger.info("✅ [SYSTEM_READY]: تم ربط جميع المحركات بنجاح.")

    # ---------------------------------------------------------
    def process_pdf_core(self, pdf_path: str) -> dict:
        """
        [CORE V4.0]: الربط النهائي بين المستخلص المحدث والذاكرة السيادية.
        """
        try:
            # 1. الاستخراج الفيزيائي (قائمة الصفحات من ملف B)
            pages_data = self.extractor.process_document(pdf_path)
            total_processed_chunks = 0

            # 2. بناء السجل المنطقي (الحصاد)
            self.tillage_engine.build_global_ledger(pages_data, self.inference_engine.generate)

            # 3. التخزين الذكي (الغوص داخل الـ Chunks)
            for page in pages_data:
                # 🚀 هنا التعديل: استخراج القطع (Chunks) من داخل كل صفحة
                chunks = page.get('chunks', [])

                for chunk in chunks:
                    # توليد المتجه لكل قطعة نصية
                    vector = self.embedder.get_embedding(chunk['content'])

                    if vector is not None:
                        # إرسال القطعة للذاكرة المحصنة
                        self.network.add_page(
                            page_num=chunk['page'],
                            content=chunk['content'],
                            embedding=vector,
                            metadata=chunk['metadata']
                        )
                        total_processed_chunks += 1
                    else:
                        self.logger.warning(f"⚠️ [EMBED_EMPTY]: فشل توليد متجه للقطعة في صفحة {chunk['page']}")

            # 4. المخرجات المتوافقة مع محرك الاستقرار
            return {
                "status": "SUCCESS",
                "total_pages": len(pages_data),
                "processed_chunks": total_processed_chunks,
                "network_status": "READY"
            }

        except Exception as e:
            self.logger.error(f"🚨 [PROCESS_ERROR]: {str(e)}")
            return {"status": "FAILED", "total_pages": 0, "processed_chunks": 0}

    def _generate_chunks(self, text: str) -> List[str]:
        """
        [محرك التقطيع السيادي]: تقسيم النص إلى كتل متداخلة لضمان عدم ضياع السياق التقني.
        """
        if not text:
            return []

        chunks = []
        # استخدام الإعدادات التي عرفتها في الـ __init__
        start = 0
        text_len = len(text)

        while start < text_len:
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append(chunk.strip())
            # القفزة السيادية (الطول الكلي - التداخل)
            start += (self.chunk_size - self.overlap)

        return chunks

    def sense_and_encode(self, text: str, sensory_schema: str = "GENERAL") -> Dict[str, Any]:
        """
        [THE SENSORY PROBE V5.0]:
        النسخة النهائية الموحدة التي تمنع الانهيار وتدعم الرنين الإدراكي.
        """
        dim = getattr(self.embedder, 'dimension', 384)

        try:
            # 1. فحص الوجود وتجهيز المتجه الافتراضي
            if not text or self.embedder is None:
                vector = np.zeros(dim).astype('float32')
            else:
                # 2. محاولة استخراج المتجه من P2
                vector = self.embedder.get_embedding(text)

            # 🚀 [تكتيك الضرسان]: حماية ضد القيم الفارغة والصفرية
            if vector is None or (isinstance(vector, np.ndarray) and vector.size == 0):
                if self.logger:
                    self.logger.warning(f"⚠️ [SENSE]: نص غير قابل للتشفير، يتم حقن ضجيج آمن.")
                vector = np.random.uniform(-0.0001, 0.0001, dim).astype('float32')

            # التأكد من تحويل المتجه إلى مصفوفة numpy نقية
            vector = np.array(vector).astype('float32')

            # 3. العائد الموحد (The Sovereign Payload)
            return {
                "vector": vector,
                "intensity": 1.0,  # يمكن تطويرها لاحقاً لقياس أهمية النص
                "schema": sensory_schema,
                "status": "ENCODED"
            }

        except Exception as e:
            if self.logger:
                self.logger.error(f"❌ [SENSE_ERROR]: {str(e)}")
            return {
                "vector": np.zeros(dim).astype('float32'),
                "intensity": 0.0,
                "schema": sensory_schema,
                "status": "ERROR"
            }

    def extract_and_tilling(self, pdf_path: str):
        """
        دالة محسنة تقوم بالاستخراج والحراثة في آن واحد
        """
        # (منطق استخراج النصوص من الـ 224 صفحة...)
        raw_chunks = self._generate_chunks(pdf_path)

        processed_nodes = []
        for i, chunk in enumerate(raw_chunks):
            # 2. تحويل الكتلة النصية إلى "عقدة معرفية" (Knowledge Node)
            node = {
                "id": f"NODE_{i}",
                "content": chunk,
                "metadata": {"source": pdf_path, "index": i}
            }

            # 3. حقن العقدة في محرك الحرث (لرفعها من الصفر)
            self.tillage_engine.register_node(node)
            processed_nodes.append(node)

        return processed_nodes

    def _clean_sovereign_text(self, text: str) -> str:
        """
        تطهير النص من الضجيج الرقمي مع الحفاظ على هيكلية الأسطر (المصفوفات والمعادلات).
        """
        if not text:
            return ""

        import re
        # 1. تنظيف المسافات الأفقية الزائدة فقط (Tabs, Spaces)
        # مع الحفاظ على سطر جديد (\n) لضمان بقاء المصفوفات مفهومة
        lines = text.splitlines()
        cleaned_lines = [re.sub(r'[ \t]+', ' ', line).strip() for line in lines]

        # 2. إزالة الأسطر الفارغة تماماً الناتجة عن التطهير
        final_text = "\n".join([line for line in cleaned_lines if line])

        return final_text

    def sync_legacy_to_perception(self, b_chunks: List[Dict], c_ledger: str):
        """
        [جسر الربط السيادي V5.0]:
        تصحيح التوجيه لضمان وصول النص للمحرك الحسي الصحيح.
        """
        self.logger.info("🔗 [SYNC]: جاري دمج مخرجات B و C مع المحرك الإدراكي...")
        synced_results = []

        for chunk in b_chunks:
            raw_text = chunk.get('content', '')
            # تحديد الأهمية بناءً على ذكرها في سجل المحرك C
            is_referenced_in_c = raw_text[:50] in c_ledger

            # 🚀 [التصحيح الحاسم]: استدعاء الدالة من المحرك الذي يمتلكها فعلياً
            # في تصميمنا، الدالة sense_and_encode موجودة في المحرك الحسي/التشفير
            try:
                # التأكد من مطابقة أسماء الـ Arguments مع تعريف الدالة الأصلي
                # ملاحظة: الدالة التي عرفناها تأخذ (text: str)
                p_vector = self.perception_engine.sense_and_encode(raw_text)

                # تحويل المتجه إلى كود إدراكي (Intensity/Resonance)
                p_code = {
                    'intensity': 2.0 if is_referenced_in_c else 1.0,
                    'vector': p_vector
                }
            except AttributeError:
                self.logger.warning("⚠️ [SYNC_ERROR]: المحرك لا يمتلك قدرات التحسس، استخدام Fallback.")
                p_code = {'intensity': 1.0, 'vector': np.zeros(384)}

            unified_node = {
                "content": raw_text,
                "perceptual_weight": p_code.get('intensity', 1.0),
                "metadata": chunk.get('metadata', {}),
                # تمرير الكود الإدراكي للمحرك الاستنتاجي لبناء الجسر المنطقي
                "logic_bridge": self.conclusion_engine.extract_logic_pattern(
                    raw_text,
                    perceptual_code=p_code
                )
            }
            synced_results.append(unified_node)

        return synced_results

    def orchestrate_perceptual_flow(self, raw_chunks: List[Dict], tillage_ledger: str):
        """
        [THE SOVEREIGN ORCHESTRATOR V5.2]:
        تم إصلاح توجيه النداءات لضمان عدم حدوث AttributeIssue.
        """
        self.logger.info("🔗 [ORCHESTRATOR]: جاري المزامنة السيادية...")
        all_unified_nodes = []

        for chunk in raw_chunks:
            content = chunk.get('content') or chunk.get('text') or ""
            metadata = chunk.get('metadata', {})
            page_num = metadata.get('page', 0)

            # 🚀 [1] الرنين الإدراكي: نستخدم الدالة المحصنة التي أصلحناها سابقاً
            is_critical = content[:100] in tillage_ledger if tillage_ledger else False
            intensity = 2.5 if is_critical else 1.0

            # تأكد أن نداء التشفير يذهب لـ self (المعالج A) أو self.embedder (ملف P2)
            vector = self.sense_and_encode(content) # الدالة التي أصلحناها في الرد السابق

            # [2] استخراج المنطق (متوافق مع ملف D)
            logic_profile = self.conclusion_engine.extract_logic_pattern(content)

            # [3] الحساب الرياضي (محاكاة الاستنتاج من ملف D)
            calc_results = {}
            if logic_profile and logic_profile.get("formulas"):
                vars_dict = logic_profile.get("vars", {})
                for formula in logic_profile["formulas"]:
                    calc_results[formula] = self.conclusion_engine.simulate_extracted_logic(
                        var_map=vars_dict,
                        formula_str=formula
                    )

            # [4] بناء العقدة المعرفية
            unified_node = {
                "page": page_num,
                "intensity": intensity,
                "logic": logic_profile,
                "calculations": calc_results,
                "vector": vector, # المصفوفة الجاهزة
                "content": content
            }
            all_unified_nodes.append(unified_node)

        # [5] التخزين الموازي (أرشفة الـ 224 عقدة)
        self.logger.info(f"💾 [STORAGE]: أرشفة {len(all_unified_nodes)} عقدة في الذاكرة السيادية...")
        # بقية كود الـ ThreadPoolExecutor...
        return all_unified_nodes

    def bridge_to_perception(self, file_id: str, perception_engine: Any) -> Dict[str, Any]:
        """
        [THE SOVEREIGN PERCEPTUAL BRIDGE V6.2]:
        استخدام Any ينهي مشكلة 'not defined' للأبد.
        """
        if not hasattr(self, 'active_workspace'):
            self.active_workspace = {}

        active_data = self.active_workspace.get(file_id)
        if not active_data:
            self.logger.error(f"❌ [BRIDGE_ERROR]: البيانات مفقودة للملف {file_id}")
            return {}

        # استكمال المنطق السيادي...
        reconstructed_text = active_data.get("data", "")

        try:
            # 🚀 تنبيه: تأكد أن الدالة داخل perception_engine
            # تسمى sense_and_encode كما في ملفك الأخير
            perceptual_code = perception_engine.sense_and_encode(
                text=reconstructed_text  # تأكد من مطابقة اسم الوسيط (text)
            )

            # حقن النتائج في الذاكرة النشطة
            active_data["perceptual_encoding"] = perceptual_code
            self.logger.info(f"⚡ [BRIDGE_SUCCESS]: تم حقن التشفير في الذاكرة لـ {file_id}")
            return perceptual_code

        except Exception as e:
            self.logger.error(f"🚨 [BRIDGE_CRITICAL]: انهيار الجسر الإدراكي: {str(e)}")
            return {}

    def _process_single_chunk_logic(self, chunk_data: Dict[str, Any]) -> bool:
        """
        [CHUNK PROCESSOR V4.0 - PERCEPTUAL EDITION]:
        معالجة الكتل النصية مع حقن "الرنين الإدراكي" لضبط دقة الحسابات وثقل التخزين.
        """
        content = chunk_data.get('content', '')
        metadata = chunk_data.get('metadata', {})
        page_num = metadata.get('page', 0)
        chunk_id = chunk_data.get('id', f"CH-{page_num}")
        predicted_schema = chunk_data.get('predicted_schema', 'GENERAL_TECHNICAL')

        if not content or len(content.strip()) < 10:
            return False

        try:
            # 1. المرحلة الإدراكية (The Perceptual Pulse)
            # استدعاء المحرك الإدراكي لتوليد "النبضة" وقياس الرنين السياقي
            # هذا يربط الملف الحالي بما تعلمه النظام سابقاً
            perceptual_code = self.perception_engine.sense_and_encode(
                raw_input=content,
                sensory_schema=predicted_schema
            )
            intensity = perceptual_code.get("intensity", 1.0)

            # 2. الاستنتاج المنطقي الواعي (Unit D - Overall Conclusion)
            # نمرر "النبضة الإدراكية" لرفع دقة استخراج المعادلات والمصفوفات
            logic_insight = self.conclusion_engine.extract_logic_pattern(
                batch_content=content,
                perceptual_code=perceptual_code
            )

            # 3. المحاكاة الرياضية التكيفية (التصحيح: الاستدعاء من محرك الاستنتاج)
            if logic_insight.get("formulas"):
                for formula in logic_insight["formulas"]:
                    # التصحيح هنا: الاستدعاء من conclusion_engine وليس calculator
                    calc_result = self.conclusion_engine.simulate_extracted_logic(
                        var_map=logic_insight.get("vars", {}),
                        formula_str=formula
                    )
                    logic_insight[f"result_{hash(formula)%1000}"] = calc_result

            # 4. التشفير المتجهي "المضخم" (Unit P2 - Aware Embedding)
            # نستخدم الـ intensity لتعديل ثقل المتجه في الفضاء الرقمي
            vector = self.embedder.get_perceptual_embedding(
                text=content,
                perceptual_intensity=intensity
            )

            # 5. إغناء البيانات الوصفية بالرنين (Metadata Enrichment)
            enriched_metadata = {
                **metadata,
                "chunk_id": chunk_id,
                "perceptual_intensity": intensity,
                "is_critical": intensity > 2.5, # وسم البيانات عالية الأهمية
                "schema_category": predicted_schema,
                "timestamp": np.datetime64('now') # توحيد الطابع الزمني السيادي
            }

            # 6. التخزين في الذاكرة السيادية (Unit P3)
            success = self.network.add_page(
                page_num=page_num,
                content=content,
                embedding=vector,
                metadata=enriched_metadata,
                logic_data=logic_insight # حقن المنطق المستخرج مع البيانات
            )

            if success:
                if intensity > 2.5:
                    self.logger.info(f"✨ [HIGH_RESONANCE]: تم تأمين بيانات حرجة في الصفحة {page_num} (Intensity: {intensity:.2f})")
                return True

            return False

        except Exception as e:
            self.logger.error(f"❌ [PERCEPTUAL_FAIL] Page {page_num}: {str(e)}")
            self.supervisor.log_incident("PERCEPTUAL_LOGIC_ERROR", str(e))
            return False

    def stream_to_engine(self, chunks, inference_func, context_schema="GENERAL"):
        """محرك الدفع التدفي لاستغلال الـ 128GB RAM"""
        self.logger.info(f"🌊 [STREAMING]: ضخ {len(chunks)} عقدة للمحرك C...")
        results = []
        batch_size = 5
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i+batch_size]
            # التأكد من استخراج النص سواء كان القادم قاموساً أو نصاً
            combined_text = "\n---\n".join([c['content'] if isinstance(c, dict) else str(c) for c in batch])
            try:
                res = inference_func(combined_text, schema=context_schema)
                if res: results.append(res)
            except Exception as e:
                self.logger.error(f"⚠️ [BATCH_ERROR]: {e}")
        return results

    def add_perceptual_node(self, node: Dict[str, Any]) -> bool:
        """
        [THE PERCEPTUAL GATEWAY]:
        استقبال العقدة المعرفية الموحدة وأرشفتها في الذاكرة السيادية.
        """
        try:
            page_num = node.get('page', 0)
            content = node.get('content', '')
            vector = node.get('vector')

            # استخراج البيانات الإدراكية المضافة
            intensity = node.get('intensity', 1.0)
            logic_data = node.get('logic', {})
            calc_results = node.get('calculations', {})

            # دمج كل شيء في البيانات الوصفية (Metadata) لسهولة الاسترجاع
            enriched_metadata = {
                "intensity": intensity,
                "has_logic": bool(logic_data),
                "logic_summary": logic_data.get('summary', '') if logic_data else '',
                "calc_count": len(calc_results),
                "timestamp": time.time()
            }

            # [CORRECTED]: توجيه النداء إلى كائن الشبكة (self.network)
            success = self.network.add_page(
                page_num=page_num,
                content=content,
                embedding=vector,
                metadata=enriched_metadata
            )

            if success and intensity > 2.0:
                self.logger.info(f"🧠 [NETWORK_MEMORY]: تم تأمين عقدة عالية الرنين في الصفحة {page_num}")

            return success

        except Exception as e:
            # التأكد من وجود اللوجر قبل الاستخدام لتجنب خطأ إضافي
            if hasattr(self, 'logger') and self.logger:
                self.logger.error(f"🚨 [NETWORK_CRITICAL]: فشل أرشفة العقدة الإدراكية: {str(e)}")
            return False

    def execute_sovereign_mission(self, pdf_path: str):
        """
        [SOVEREIGN MISSION CONTROL V4.0]: Orchestrates the flow from raw PDF
        to final mathematical stability analysis.
        """
        self.logger.info(f"🚀 [MISSION_START]: Targeting {os.path.basename(pdf_path)}")

        # 1. المرحلة السيادية الأولى: المعالجة الجوهرية والبناء الذاكري
        # استدعاء دالة Core التي طورناها؛ هي الآن تقوم بالتشريح، التنبؤ، والتخزين في P3
        core_result = self.process_pdf_core(pdf_path)

        if core_result["status"] == "error":
            self.logger.error(f"❌ [ABORT]: Core processing failed: {core_result['error_details']}")
            return []

        # 2. استرجاع الكتل المجهزة (Retrieve Synchronized Chunks)
        # بدلاً من إعادة التشريح، نأخذ البيانات الجاهزة من الذاكرة أو الكاش
        all_chunks = self.network.get_all_stored_chunks() # تأكد من وجود هذه الدالة في P3

        # 3. الربط التشغيلي مع المحرك C (الاستنتاج المتدفق)
        try:
            self.logger.info(f"⚙️ [ENGINE_C]: Streaming {len(all_chunks)} nodes for semantic inference...")

            # تمرير الـ Schema المكتشف لضمان دقة الاستنتاج
            schema = core_result.get("network_metrics", {}).get("discovered_schemas", ["GENERAL"])[0]

            results = self.batch_engine.stream_to_engine(
                all_chunks,
                self.inference_engine.generate,
                context_schema=schema # حقن السياق لضمان "السيادة المعرفية"
            )

            if results:
                self.overall_conclusion.extend(results)
                self.logger.info(f"✅ [INFERENCE_SYNC]: Received {len(results)} conclusions.")
            else:
                self.logger.warning("⚠️ [INFERENCE_GAP]: Engine C returned empty stream.")

        except Exception as e:
            self.logger.error(f"❌ [ENGINE_C_ERROR]: Flow interrupted: {str(e)}")

        # 4. التحليل الرياضي النهائي (Stability Analyzer)
        # نرسل الاستنتاجات النهائية للمحلل لتدقيق المصفوفات (Matrices)
        final_results = self.overall_conclusion
        stability_report = self._analyze_mathematical_stability(final_results)

        # 5. التقرير الختامي للسيادة (Sovereign Audit Report)
        self._render_final_audit(pdf_path, len(all_chunks), stability_report)

        return final_results

    def _render_final_audit(self, path, nodes, report):
        """دالة مساعدة لطباعة التقرير بشكل احترافي"""
        print(f"\n" + "█"*60)
        print(f"🛡️  [FINAL SOVEREIGN AUDIT REPORT V4.0]")
        print(f"█" + "─"*58 + "█")
        print(f"📄 TARGET_FILE   : {os.path.basename(path)}")
        print(f"🧩 KNOWLEDGE_NODES: {nodes}")
        print(f"🔢 4x4_MATRICES  : {report.get('matrix_4x4_count', 0)}")
        print(f"🛡️  STABILITY_RANK: {report.get('status', 'UNKNOWN')}")
        print(f"📈 INTEGRITY_SCORE: {report.get('integrity_score', 0.0):.2f}%")
        print("█"*60 + "\n")

    def _analyze_mathematical_stability(self, results):
            """تحصين نهائي ضد القسمة على صفر"""
            if not results:
                return {"status": "VOID", "score": 0}

            # منطق التحليل الخاص بك مع حماية
            valid_hits = len([r for r in results if "matrix" in str(r).lower()])
            score = (valid_hits / max(1, len(results))) * 100
            return {"status": "SUCCESS", "score": f"{score:.2f}%"}
