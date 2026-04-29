# A_Basic_pdf_processor.py

import re
import os
import fitz  # PyMuPDF
from typing import Dict, Any, List
from concurrent.futures import ThreadPoolExecutor, as_completed

# --- [الارتباط بالوحدات الخدمية] ---
from B_data_extractor import SovereignDataExtractor
from C_Tillage_engine_PDF_files import TillageenginePDFfiles, SafeSovereignEvaluator
from D_Overall_conclusion import UniversalSovereignInference

# --- [الارتباط بالمحركات الذكية] ---
from Generation_Engine import SovereignInferenceEngine
from Search_Engine import SovereignNavigator
from Calculator import Calculator_

# ==========================================
# 1. كلاس معالج البيانات (The Data Processor)
# ==========================================
class SovereignDataProcessor:
    """
    [معالج البيانات السيادي]: القائد الميداني المسؤول عن الربط بين
    العمليات الفيزيائية للملفات والمحركات الذكية للاستدلال.
    """
    def __init__(self, supervisor, extractor: SovereignDataExtractor, logger, network, embedder, openai_client=None):
        # 1. استقبال البنية التحتية من ملف main
        self.supervisor = supervisor
        self.extractor = extractor  # الوحدة B
        self.logger = logger
        self.network = network    # الوحدة P3 (الذاكرة)
        self.embedder = embedder   # الوحدة P2

        self.logger.info("🏗️ [A_Processor]: بدأ تهيئة المحركات الذكية والوحدات الخدمية...")

        # 2. تهيئة المحركات الذكية (Smart Engines) داخلياً
        self.inference_engine = SovereignInferenceEngine(logger, embedder, openai_client)
        self.navigator = SovereignNavigator(network, embedder, logger)
        self.calculator = Calculator_(logger)

        # 3. تهيئة الوحدات الخدمية الإضافية
        self.batch_engine = TillageenginePDFfiles()

        # تمرير الـ logger لإنهاء خطأ Pylance في وحدة الاستنتاج
        self.conclusion_unit = UniversalSovereignInference(logger=self.logger)

        # تهيئة المقيم الآمن للحسابات الرياضية وتمرير الـ logger له أيضاً
        self.safe_evaluator = SafeSovereignEvaluator(logger=self.logger)

        self.logger.info("✅ [A_Processor]: جميع المحركات جاهزة للعمل بنظام السيادة الكاملة.")

        # --- تصحيح المخزن الاستنتاجي (إزالة التكرار = []) ---
        self.overall_conclusion = []

    def process_pdf_core(self, pdf_path: str) -> Dict[str, Any]:
        if not os.path.exists(pdf_path):
            return {"status": "error", "error_details": "File not found", "total_pages": 0}

        actual_pages = 0
        completed = 0
        total_attempted_chunks = 0 # متغير جديد لضبط دقة الإحصائيات

        try:
            # --- [تطهير الذاكرة السيادية قبل البدء] ---
            if hasattr(self, 'global_ledger'):
                self.global_ledger = ""
            self.overall_conclusion = [] # تصفير قائمة النتائج

            if hasattr(self.network, 'reset_for_new_document'):
                self.network.reset_for_new_document()

            with fitz.open(pdf_path) as doc:
                actual_pages = len(doc)
                self.total_pages = actual_pages
                self.logger.info(f"📊 [CORE]: فحص {actual_pages} صفحة.")

            # 2. استدعاء المستخلص (الوحدة B)
            raw_result = self.extractor.process_document(pdf_path)
            raw_chunks = raw_result.get("nodes", []) if isinstance(raw_result, dict) else raw_result

            if not raw_chunks:
                return {"status": "error", "error_details": "PDF is empty", "total_pages": actual_pages}

            # 3. المعالجة المتوازية مع فلترة ذكية
            valid_chunks = [item for item in raw_chunks if isinstance(item, dict) and len(str(item.get('content', ''))) > 5]
            total_attempted_chunks = len(valid_chunks) # هذا هو الرقم الحقيقي للمقام

            with ThreadPoolExecutor(max_workers=4) as executor:
                future_to_chunk = {executor.submit(self._process_single_chunk_logic, item): item for item in valid_chunks}

                for future in as_completed(future_to_chunk):
                    try:
                        if future.result():
                            completed += 1
                    except Exception as chunk_err:
                        chunk = future_to_chunk[future]
                        page_num = chunk.get('metadata', {}).get('page', 'unknown')
                        self.logger.error(f"❌ [CHUNK_ERROR] Page {page_num}: {str(chunk_err)}")

            # 4. الختم النهائي
            if hasattr(self.network, 'finalize_network'):
                self.network.finalize_network()

            self.logger.info(f"✅ [MISSION_COMPLETE]: نجاح {completed} من أصل {total_attempted_chunks} كتلة.")

            return {
                "status": "success",
                "total_pages": actual_pages,
                "processed_chunks": completed,
                "total_attempted": total_attempted_chunks, # نمرر هذا الرقم للتقرير
                "data_found": len(self.overall_conclusion)
            }

        except Exception as e:
            # صمام أمان لضمان عدم تعطل main.py
            return {
                "status": "error",
                "error_details": str(e),
                "total_pages": actual_pages,
                "processed_chunks": completed,
                "data_found": 0
            }

    def _process_single_chunk_logic(self, chunk_data: Dict[str, Any]):
        """
        [معالج الكتل السيادي المطور]: يدمج التحليل المنطقي مع الحسابات الهندسيّة الحية.
        """
        # ........ 1. تأمين البيانات التعريفية ................
        metadata = chunk_data.get('metadata', {})
        page_num = metadata.get('page', chunk_data.get('page_label', 0))
        total_pages = metadata.get('total_pages', getattr(self, 'total_pages', 0))

        content = chunk_data.get('content', '')
        if not content or len(content.strip()) < 5:
            return False

        try:
            # ........ 2. تطهير النص واستخراج الأنماط المنطقية ................
            clean_text = self._clean_sovereign_text(content)
            logic_results = self.conclusion_unit.Filtering_logical_patterns(clean_text)

            # ........ 3. التحليل الهندسي والحسابي (Geometric & Mechanical Analysis) ........
            engineering_analysis = {}

            # أ. رصد وتحليل المصفوفات الحركية
            if self.is_valid_kinematic_matrix(clean_text):
                import re
                import numpy as np
                numbers = re.findall(r"[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?", clean_text)
                matrix_data = [float(n) for n in numbers[:16]]
                matrix_np = np.array(matrix_data).reshape(4, 4)

                # التحقق من المصفوفة كـ D-H Matrix عبر الحاسبة
                if self.calculator.verify_dh_matrix(matrix_np.tolist()):
                    engineering_analysis["matrix_check"] = "✅ Valid D-H Transformation Matrix"
                    # يمكن هنا إضافة استخراج لزوايا المفاصل إذا تطلب الأمر

            # ب. معالجة المتغيرات الميكانيكية (مثل الخطوات والتروس)
            extracted_vars = logic_results.get('vars', {})
            if all(k in extracted_vars for k in ['motor_steps', 'gear_ratio']):
                res_report = self.calculator.calculate_sovereign_resolution(
                    # تحويل motor_steps إلى int لإرضاء Pylance ومطابقة توقيع الدالة
                    motor_steps=int(float(extracted_vars.get('motor_steps', 200))),
                    gear_ratio=float(extracted_vars.get('gear_ratio', 1)),
                    arm_length=float(extracted_vars.get('arm_length', 1.0))
                )
                engineering_analysis["precision_report"] = res_report

            # ........ 4. بناء هيكل البيانات النهائي ................
            is_logic = logic_results.get('status') == "Logic_Extracted"
            is_kinematic = "matrix_check" in engineering_analysis

            entry_data = {
                "page": page_num,
                "total_pages": total_pages,
                "content_preview": clean_text[:150],
                "full_content": clean_text,
                "logic": logic_results,
                "engineering_data": engineering_analysis, # إضافة الحسابات الهندسية هنا
                "is_valid": is_logic or is_kinematic,
                "type": "ROBOTIC_ANALYSIS" if is_kinematic else ("STRUCTURED_LOGIC" if is_logic else "RAW_KNOWLEDGE")
            }

            self.overall_conclusion.append(entry_data)
            return True

        except Exception as e:
            self.logger.error(f"❌ [CHUNK_ERROR] Page {page_num}: {str(e)}")
            return False

    def execute_sovereign_mission(self, pdf_path: str):
        """
        [إدارة المهمة الشاملة المحدثة]:
        تنسيق تدفق البيانات من الاستخراج (B) إلى الاستنتاج (C) ثم التدقيق النهائي.
        """
        # 1. تصفير الذاكرة والحيادية التامة
        self.start_new_document_session() # استخدام دالة التطهير الموحدة التي وضعناها سابقاً

        if not os.path.exists(pdf_path):
            self.logger.error(f"❌ الهدف غير موجود: {pdf_path}")
            return []

        # --- 2. تشريح الملف (الوحدة B) ---
        extraction_package = self.extractor.process_document(pdf_path)
        all_chunks = extraction_package.get("nodes", [])
        self.total_pages = extraction_package.get("total_pages", 0)

        # --- 3. التدفق الاستنتاجي (المحرك C - Turbo Mode) ---
        # ملاحظة: تم تقديم هذه الخطوة لأنها المصدر الرئيسي للبيانات الآن
        try:
            self.logger.info(f"⚙️ [STREAM]: بدء استخراج المعرفة الشاملة من {len(all_chunks)} كتلة...")

            results = self.batch_engine.stream_to_engine(
                all_chunks,
                self.inference_engine.generate_analyzer
            )

            if results:
                # تصفية أي نتائج فارغة قبل الإضافة
                valid_results = [r for r in results if r]
                self.overall_conclusion.extend(valid_results)
                self.logger.info(f"✅ تم استقبال {len(valid_results)} استنتاج معرفي.")

        except Exception as e:
            self.logger.error(f"❌ خطأ في تدفق المحرك C: {str(e)}")

        # --- 4. فحص النزاهة (باستخدام المنطق الجديد) ---
        # نرسل النتائج النهائية للمحلل لحساب "نسبة الجودة"
        final_results = self.overall_conclusion
        report = self._analyze_mathematical_stability(final_results)

        # --- 5. التقرير الختامي السيادي (عرض البيانات المصححة) ---
        print(f"\n" + "═"*50)
        print(f"🛡️ [FINAL SOVEREIGN AUDIT REPORT]")
        print(f"═"*50)
        print(f"📄 الملف: {os.path.basename(pdf_path)}")
        print(f"📊 إجمالي الكتل المعالجة: {len(all_chunks)}") # إجمالي ما تم قراءته
        print(f"✅ كتل معرفية صالحة: {len(final_results)}")    # ما تم استنتاجه فعلياً
        print(f"🔢 الأنماط الهيكلية: {report.get('matrix_4x4_count', 0)}")
        print(f"🛡️ حالة الاستقرار: {report.get('status', 'Stable')}")
        print(f"📈 معامل النزاهة: {report.get('integrity_score', 0):.2f}%") # الآن ستكون النسبة دقيقة
        print("═"*50 + "\n")

        return final_results

    def is_valid_kinematic_matrix(self, text: str) -> bool:
        """
        [فحص النزاهة الهندسية]: يتحقق من هيكلية مصفوفة التحويل 4x4.
        التحسين: نقل numpy للأعلى وزيادة دقة الفحص الفيزيائي.
        """

        import numpy as np

        # استخدام re المار من الأعلى أسرع برمجياً
        cleaned = re.sub(r'[\[\](){},;]', ' ', str(text).lower())
        numbers = re.findall(r"[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?", cleaned)

        # مصفوفة 4x4 تتطلب 16 رقماً بالتمام والكمال ككتلة واحدة
        if len(numbers) < 16:
            return False

        try:
            # تحويل أول 16 رقماً تم رصدهم
            matrix_data = [float(n) for n in numbers[:16]]
            matrix = np.array(matrix_data).reshape(4, 4)

            # 1. اختبار السطر الأخير (المعيار الهندسي الأساسي)
            last_row = matrix[3, :]
            # np.allclose تعيد numpy.bool_، لذا نحولها يدوياً
            is_projection_valid = bool(np.allclose(last_row, [0, 0, 0, 1], atol=1e-3))

            # 2. اختبار إضافي: استبعاد المصفوفات الصفرية
            # np.any أيضاً تعيد نوع بيانات numpy، نحولها لـ bool بايثون
            is_not_empty = bool(np.any(matrix[:3, :3] != 0))

            return is_projection_valid and is_not_empty

        except (ValueError, IndexError):
            return False

    def _analyze_mathematical_stability(self, extracted_data: List[Any]) -> Dict[str, Any]:
        """
        [محلل النزاهة السيادي المحدث]: يقارن بين جودة البيانات المستخرجة وإجمالي الكتل المعالجة.
        تم إلغاء الاعتماد على عدد الصفحات لمنع تضخم النسب المئوية.
        """
        import re
        import numpy as np

        self.logger.info("🛡️ [STABILITY_CHECK]: بدء فحص النزاهة المنطقية والنوعية...")

        report = {
            "total_nodes": len(extracted_data),
            "valid_data_points": 0,
            "matrix_4x4_count": 0,
            "integrity_score": 0.0,
            "status": "Incomplete"
        }

        if report["total_nodes"] == 0:
            report["status"] = "🚨 Empty Target"
            return report

        for entry in extracted_data:
            entry_str = str(entry)

            # 1. فحص وجود مصفوفة حركية (منطق صلب)
            if self.is_valid_kinematic_matrix(entry_str):
                report["matrix_4x4_count"] += 1
                report["valid_data_points"] += 1
                continue

            # 2. فحص النزاهة المنطقية (Logical Filtering)
            # نعتبر البيانات صالحة إذا اجتازت معايير الجودة (أرقام، هيكلة، أو كثافة نصية)
            has_numbers = len(re.findall(r"[-+]?\d*\.?\d+", entry_str)) > 0
            has_structure = ":" in entry_str or "=" in entry_str or "###" in entry_str
            is_rich_text = len(entry_str.split()) > 10

            if has_numbers or has_structure or is_rich_text:
                report["valid_data_points"] += 1

        # --- الحساب الجديد للنزاهة (بناءً على الكتل المعالجة فعلياً) ---
        # النسبة الآن تعبر عن: "كم من البيانات التي استخرجناها تعتبر فعلاً بيانات قيمة؟"
        denominator = report["total_nodes"]

        # حساب النسبة المئوية (الحد الأقصى سيكون 100% دائماً)
        report["integrity_score"] = (report["valid_data_points"] / denominator) * 100

        # --- تقييم الحالة السيادية بناءً على المعايير الجديدة ---
        score = report["integrity_score"]

        if report["matrix_4x4_count"] > 0:
            report["status"] = f"💎 Kinematic Data Found ({report['matrix_4x4_count']} matrices)"
        elif score >= 85:
            report["status"] = "💎 High Integrity (Dense Knowledge)"
        elif score >= 50:
            report["status"] = "⚠️ Stable (Mixed Content)"
        else:
            report["status"] = "🚨 Low Data Quality"

        return report

    def start_new_document_session(self):
        """تطهير الذاكرة التراكمية لضمان عدم تداخل الملفات."""
        self.global_ledger = ""
        self.overall_conclusion = []
        self.total_pages = 0  # إضافة تصفير العداد لضمان دقة التقارير الجديدة
        self.logger.info("🧹 [PURGE]: تم تنظيف الذاكرة والعدادات للمهمة الجديدة.")

    def _clean_sovereign_text(self, text: str) -> str:
        """
        [تطهير النص السيادي]: عزل تفكير المحرك وأوامر النظام عن البيانات الحقيقية.
        """
        if not text or not isinstance(text, str):
            return ""

        import re

        # قائمة الأنماط المحظورة (توسيع القائمة بناءً على رصد التقرير الأخير)
        forbidden_patterns = [
            r"STRICT TARGET:.*",
            r"OPERATIONAL COMMANDS:.*",
            r"STRATEGIC KNOWLEDGE MAP.*",
            r"MATHEMATICAL INTEGRITY:.*",
            r"TECHNICAL FOCUS:.*",
            r"INITIATING NEUTRAL AUDIT.*",
            r"FORMAT:.*",           # منع ظهور تعليمات التنسيق
            r"SCOPE:.*",            # منع ظهور تعليمات نطاق العمل
            r"[\u2500-\u257F]+",    # تنظيف كافة أشكال خطوط الـ Box Drawing (═══, ───)
            r"📝 \[LOGIC_NARRATIVE\].*", # منع تكرار الوسوم إذا تم دمجها بالخطأ
        ]

        lines = text.splitlines()
        cleaned_lines = []

        for line in lines:
            # 1. تجاهل الأسطر التي تحتوي على أنماط محظورة
            if any(re.search(p, line, re.IGNORECASE) for p in forbidden_patterns):
                continue

            # 2. تنظيف المسافات الزائدة (الحفاظ على مسافة واحدة للأرقام والمصفوفات)
            clean_line = re.sub(r'[ \t]+', ' ', line).strip()

            # 3. استبعاد الأسطر التي هي مجرد رموز تجميلية أو فارغة
            if clean_line and not re.match(r'^[=\-_*#]+$', clean_line):
                cleaned_lines.append(clean_line)

        return "\n".join(cleaned_lines)
