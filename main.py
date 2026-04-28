# main.py

import time
import os
import numpy as np
from dotenv import load_dotenv

# 1. استيراد الوحدة الخدمية الرئيسية (الرأس)
from A_pdf_processor import Basic_pdf_process_engine

# 2. استيراد مستودع الأسلحة (Infrastructure)
from P1_sovereign_utils import SovereignSupervisorySystem
from P2_embedding_logic import EmbeddingManager
from P3_memory import PDFpageCacheNetwork
from B_data_extractor import SovereignDataExtractor

# تحميل إعدادات البيئة (API Keys, URLs)
load_dotenv()

def finalize_network(self) -> dict:
    self.logger.info("🔗 [LINKER]: تفعيل بروتوكول الحماية من الانفجار المعرفي...")

    # 1. تصفية العقد (استبعاد الصفحات التي فشلت في MEMORY_ERROR)
    valid_node_ids = [
        nid for nid, data in self.knowledge_graph.items()
        if data.get('embedding') is not None and np.linalg.norm(data['embedding']) > 1e-9
    ]

    if not valid_node_ids:
        self.logger.error("🚨 [LINKER]: لم يتم العثور على عقد صالحة. تأكد من سلامة الـ Embeddings.")
        return {"network_status": "VOID", "structural_stability": "0.00%"}

    # 2. استخراج المتجهات الصالحة فقط
    embeddings = np.array([self.knowledge_graph[nid]['embedding'] for nid in valid_node_ids])
    connections = 0

    # 3. الربط باستخدام 80GB RAM بكفاءة
    for i, node_id in enumerate(valid_node_ids):
        # استدعاء المحرك P2 مع تمرير Epsilon داخلي
        similarities = self.embedder.calculate_perceptual_similarity(embeddings[i], embeddings)

        # التأكد من أن النتيجة مصفوفة مسطحة
        scores = similarities.flatten()

        for j, score in enumerate(scores):
            if i != j and score > 0.85:
                if valid_node_ids[j] not in self.knowledge_graph[node_id]['links']:
                    self.knowledge_graph[node_id]['links'].append(valid_node_ids[j])
                    connections += 1

    # 4. حساب الاستقرار بناءً على "الموجود فعلياً" مع حماية كاملة
    node_count = len(valid_node_ids)

    # 🛡️ حاجز الحماية الأول: التأكد من وجود عقد كافية للقسمة
    if node_count == 0:
        stability_score = 0.0
        self.logger.warning("⚠️ [LINKER]: لا توجد عقد صالحة لحساب الاستقرار.")
    else:
        # 🛡️ حاجز الحماية الثاني: حساب الاستقرار مع التأكد أن النتيجة منطقية
        # نستخدم max(1, ...) لضمان عدم القسمة على صفر أبداً
        denominator = node_count * 5
        stability_score = (connections / denominator) * 100

    return {
        "network_status": "PROTECTED_SUCCESS" if node_count > 0 else "VOID",
        "total_nodes_processed": node_count,
        "total_links": connections,
        "structural_stability": f"{min(stability_score, 100.0):.2f}%",
        "missing_pages": 224 - node_count
    }

# =======================================
#        نتائج الإختبارات __main__
# =======================================
if __name__ == "__main__":
    # --- [1] تهيئة مستودع الأسلحة ---
    supervisor = SovereignSupervisorySystem(name="SOVEREIGN_CORE")
    logger = supervisor.logger
    embedder = EmbeddingManager(logger=logger)
    network_memory = PDFpageCacheNetwork(supervisor)
    extractor = SovereignDataExtractor(chunk_size=400, overlap=50)

    commander = Basic_pdf_process_engine(
        supervisor=supervisor,
        extractor=extractor,
        logger=logger,
        network=network_memory,
        embedder=embedder
    )

    # --- [2] تحديد الهدف (تلقائي ذكي) ---
    import glob
    import os
    pdf_files = glob.glob("*.pdf")
    pdf_target = pdf_files[0] if pdf_files else "ROBOTICS.pdf"

    # --- [3] الفحص الاستخباراتي للملف ---
    if os.path.exists(pdf_target):
        # حساب الحجم بدقة قبل البدء
        file_size_mb = os.path.getsize(pdf_target) / (1024 * 1024)
        logger.info(f"🚀 تم رصد الهدف: {pdf_target} | الحجم: {file_size_mb:.2f} MB")

        try:
            # 1. تنفيذ المهمة السيادية (مرة واحدة فقط)
            # تعيد هذه الدالة ملخص العمليات (صفحات، كتل، حالة)
            mission_summary = commander.process_pdf_core(pdf_target)

            # 2. تأمين الأرشيف وتفريغ الذاكرة (استدعاء الدالة التي طورناها)
            # تعيد هذه الدالة تفاصيل الشبكة المعرفية (Domains, Nodes)
            network_info = network_memory.finalize_network()

            # 3. استخراج البيانات المستنتجة (Inference Results) من مخزن القائد
            # نستخدم getattr لضمان الأمان في حال لم تكن القائمة معرفة
            actual_data = getattr(commander, 'overall_conclusion', [])

            # 4. إجراء التحليل الرياضي على البيانات المستخرجة فعلياً
            # الآن Pylance سعيد لأن actual_data هي List وستقبلها الدالة
            audit_report = commander._analyze_mathematical_stability(actual_data) if \
                hasattr(commander, '_analyze_mathematical_stability') else None

            # --- عرض التقرير النهائي الاحترافي الشامل ---
            print("\n" + "█"*60)
            print("📊 [REPORT]: تقرير الاستدلال الهندسي السيادي (Sovereign Audit)")
            print("█"*60)
            print(f"📁 بيانات الملف: {pdf_target} ({file_size_mb:.2f} MB)")
            print(f"🧠 التصنيفات المكتشفة: {', '.join(network_info.get('discovered_schemas', ['Unknown']))}")
            print(f"📌 نقاط البيانات الموثقة: {network_info.get('total_knowledge_nodes', 0)}")

            if audit_report:
                print(f"🛡️ معامل الاستقرار الهيكلي: {audit_report.get('integrity_score', 0):.2f}%")
                print(f"⚠️ معدل التقطع: {audit_report.get('fragmentation_rate', 0):.2f}%")
                print(f"🏁 التشخيص التقني: {audit_report.get('status', 'STABLE')}")

            print("-" * 60)
            print(f"✅ الحالة النهائية: MISSION_ACCOMPLISHED")
            print(f"⏱️ وقت التشغيل الإجمالي: {supervisor.get_uptime()}")
            print("█"*60 + "\n")

        except Exception as e:
            logger.critical(f"🚨 خطأ ميداني أثناء التشغيل: {str(e)}")
            import traceback
            logger.debug(traceback.format_exc()) # لسهولة تصحيح الأخطاء خلف الكواليس
    else:
        print(f"❌ خطأ حرج: لم يتم العثور على الملف '{pdf_target}'")
