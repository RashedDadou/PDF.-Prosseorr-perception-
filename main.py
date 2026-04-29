# main.py - النسخة السيادية المصلحة

import os
import sys
from pathlib import Path

# استيراد الوحدات الخاصة بك
from P1_sovereign_utils import SovereignSupervisorySystem
from P2_embedding_logic import EmbeddingManager
from P3_memory import PDFpageCacheNetwork
from B_data_extractor import SovereignDataExtractor
from A_Basic_pdf_processor import SovereignDataProcessor
from D_Overall_conclusion import UniversalSovereignInference
from Sovereign_Visualizer import SovereignReportEngine

def is_valid_kinematic_matrix(text: str) -> bool:
    """
    [مدقق النزاهة الهندسية المطور]:
    التحسينات: معالجة أسرع، تنظيف القيم العلمية، وفحص استقرار المصفوفة.
    """
    import re
    import numpy as np

    if not text or len(text.strip()) < 20: # حماية أولية للمساحة
        return False

    # 1. تنظيف النص (إزالة الأقواس والفاصلات لتوحيد الهيكل)
    cleaned = re.sub(r'[\[\](){},;]', ' ', str(text).lower())

    # 2. استخراج الأرقام (دعم الأرقام العلمية e-05)
    # استخدام Regex محسن لالتقاط الأرقام الحقيقية فقط
    numbers = re.findall(r"[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?", cleaned)

    # يجب أن يكون لدينا 16 رقماً على الأقل لتمثيل مصفوفة 4x4
    if len(numbers) < 16:
        return False

    try:
        # 3. بناء المصفوفة (نأخذ أول 16 رقماً يتم رصدهم ككتلة)
        matrix_data = [float(n) for n in numbers[:16]]
        matrix = np.array(matrix_data).reshape(4, 4)

        # 4. [اختبار النزاهة السيادي]:
        # أ - فحص السطر الأخير القياسي [0, 0, 0, 1]
        last_row = matrix[3, :]
        is_projection_valid = np.allclose(last_row, [0, 0, 0, 1], atol=1e-3)

        # ب - فحص "الحياة" في المصفوفة (ليست كلها أصفار)
        # نضمن أن الجزء الدوراني يحتوي على بيانات حقيقية
        has_data = np.any(np.abs(matrix[:3, :3]) > 1e-6)

        # ج - الحماية من القيم غير المنطقية (Inf أو NaN)
        is_finite = np.all(np.isfinite(matrix))

        # التحويل الصريح لـ bool لإيقاف خطأ Pylance
        return bool(is_projection_valid and has_data and is_finite)

    except (ValueError, IndexError):
        return False

# ==========================================
#    __main__
# ==========================================
if __name__ == "__main__":
    # .......... المرحلة 1: تهيئة مستودع الأسلحة (Infrastructure) ..........
    supervisor = SovereignSupervisorySystem(name="SOVEREIGN_CORE")
    logger = supervisor.logger

    # تهيئة الأدوات الأساسية (ضمان تعريفها قبل الاستخدام)
    embedder = EmbeddingManager(logger=logger)
    network_memory = PDFpageCacheNetwork(supervisor)
    extractor = SovereignDataExtractor(chunk_size=500, overlap=200)

    # .......... المرحلة 2: بناء القائد الميداني وتزويده بالأسلحة ..........
    commander = SovereignDataProcessor(
        supervisor=supervisor,
        extractor=extractor,
        logger=logger,
        network=network_memory,
        embedder=embedder
    )

# .......... المرحلة 3: الرادار السيادي (اكتشاف ومعالجة كافة الملفات) ..........
    import os
    import re
    current_dir = os.getcwd()
    target_files = [f for f in os.listdir(current_dir) if f.endswith('.pdf')]

    if not target_files:
        print("\n" + "!"*55)
        print(f"⚠️ [SYSTEM ALERT]: الرادار لم يرصد أي أهداف في: {current_dir}")
        print("!"*55)
        logger.warning("توقف المحرك: المسار خالي من البيانات.")
    else:
        print(f"📡 [RADAR]: تم رصد {len(target_files)} أهداف. بدء التسلسل العملياتي...")

        for pdf_target in target_files:
            logger.info(f"🚀 إطلاق المهمة السيادية على الهدف: {pdf_target}")

            # 1. Execute Mission
            final_results = commander.execute_sovereign_mission(pdf_target)

            # 2. Preparation of Metadata (Optional for better details)
            meta = {
                "total_pages": 224,
                "valid_blocks": len(final_results),
                "structural_patterns": 0 # Can be fetched from your inference class
            }

            # 3. Call the Sovereign Visualizer
            SovereignReportEngine.generate_audit_report(pdf_target, final_results, logger, meta)

            try:
                # ........ 1. تنفيذ المعالجة واستلام الاستنتاجات ................
                # يتم هنا استلام الكتل (Chunks) التي تمثل الصفحات أو أجزاءها
                final_results = commander.execute_sovereign_mission(pdf_target)

                if final_results is None or not isinstance(final_results, list) or len(final_results) == 0:
                    logger.error(f"❌ [CRITICAL]: فشل استخراج المعرفة من الهدف {pdf_target}.")
                    continue

                # إشعار نجاح المعالجة الأولية
                logger.info(f"📦 [SUCCESS]: تم استلام {len(final_results)} كتلة معرفية.")

                # السطر الذي كان يسبب الخطأ (تم ضمه داخل البنية أو إغلاقها قبله)
                print(f"✅ تم الانتهاء من رصد وتحليل {len(final_results)} عنصر معرفي بنجاح.")

            finally:
                # إغلاق البنية لضمان عدم توقف المحرك
                pass

                # ........ 1.5 محرك استنتاج الهوية والتقرير التتابعي (Sequential Intel) ................
                def get_target_intelligence(filename, results):
                    # أ. استنتاج الاسم والسنة (الهوية السيادية)
                    base_name = filename.split('_')[-1].replace('.pdf', '').upper()
                    inferred_title, design_year = base_name, "Unknown"

                    # تنظيف العينة من نصوص التعليمات (FORMAT/SCOPE) للوصول للبيانات الحقيقية
                    sample_data = " ".join([str(r) for r in results[:20] if "FORMAT:" not in str(r)])

                    year_match = re.search(r"\b20[0-2]\d\b", sample_data)
                    if year_match: design_year = year_match.group(0)

                    title_search = re.search(r"(?i)title[:\s]+([A-Z0-9\s\-]{5,})", sample_data)
                    if title_search: inferred_title = title_search.group(1).strip()

                    return inferred_title, design_year

                # تنفيذ استخراج الهوية
                official_title, creation_year = get_target_intelligence(pdf_target, final_results)

                # عرض التقرير التتابعي (صفحة بصفحة) لضمان الشمولية
                print(f"\n📡 " + "═"*62)
                print(f"🎯 الهوية المستنتجة: {official_title}")
                print(f"📅 مرجع التصميم: {creation_year}")
                print(f"📑 [SEQUENTIAL REPORT]: تحليل تتابعي لكافة الكتل ({len(final_results)} كتلة)")
                print("═"*65)

                for idx, insight in enumerate(final_results):
                    page_id = idx + 1
                    content_str = str(insight).strip().replace('\n', ' ')

                    # منطق الربط البسيط ليعرف القائد مكملات الصفحات
                    if any(x in content_str for x in ['[', '=', 'theta', 'T']):
                        status = "⚙️ [DATA_CORE]" # بيانات هندسية صلبة
                    elif len(content_str) < 50:
                        status = "🔗 [CONTINUED]" # تكملة لسياق سابق
                    else:
                        status = "📄 [TEXT_INFO]" # معلومات نصية

                    # طباعة سطر مبسط لكل صفحة/كتلة
                    print(f"ص {page_id:03d} | {status:<15} | {content_str[:120]}...")

                print("═"*65)

                # ........ 2. استدعاء محرك الاستدلال لفك الشفرات المنطقية ................
                # التطوير: تحويل المحرك من "ماسح نصي" إلى "محلل علاقات"
                inference_engine = UniversalSovereignInference(logger=logger)

                # التحسين: دمج القائمة في نص واحد مع فواصل استراتيجية لضمان الدقة
                # هذا يحل خطأ Pylance ويحافظ على هيكلية البيانات للمحرك
                unified_content = "\n---BLOCK_SEPARATOR---\n".join([str(r) for r in final_results])

                logic_report = inference_engine.Filtering_logical_patterns(unified_content)

                # إضافة طبقة "الاستدلال المتقاطع" (Cross-Reference)
                # إذا وجد المحرك متغيرات، نقوم بربطها فوراً بذاكرة الشبكة
                if logic_report.get('vars'):
                    found_vars = logic_report['vars']
                    logger.info(f"🧠 [INFERENCE]: تم رصد {len(found_vars)} متغيرات استراتيجية.")
                    # ربط المتغيرات بالذاكرة الشبكية لتعزيز "الفهم" في الملفات القادمة
                    for var_name, var_val in found_vars.items():
                        network_memory.add_node(label=var_name, value=var_val, type="VARIABLE")

                for pdf_target in target_files:
                    logger.info(f"🚀 Launching Sovereign Mission: {pdf_target}")

                    try:
                        # 1. المعالجة الأساسية (مرة واحدة فقط)
                        final_results = commander.execute_sovereign_mission(pdf_target)

                        if not final_results:
                            logger.error(f"❌ Failed to extract knowledge from {pdf_target}")
                            continue

                        # 2. إعداد البيانات المساعدة (Metadata)
                        meta = {
                            "total_pages": 224, # يمكن جلبها ديناميكياً
                            "valid_blocks": len(final_results),
                            "structural_patterns": 0
                        }

                        # 3. استدعاء "الوحش" الذي صممناه للتقرير
                        # هذه الدالة ستقوم بكل العمل (الهوية، التتابع، النزاهة، الحجم، نوع المجال)
                        from Sovereign_Visualizer import SovereignReportEngine
                        SovereignReportEngine.generate_audit_report(pdf_target, final_results, logger, meta)

                    finally:
                        pass # لضمان استقرار المحرك
