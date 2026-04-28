# SovereignTillage.py

import re
import numpy as np
from typing import Dict, List, Any, Optional

class SovereignTillage:
    """
    [محرك الحرث السيادي V1.0]:
    المسؤول عن جمع المحصول المعرفي (Nodes) واستخلاص الهياكل الرياضية (Matrices).
    """
    def __init__(self, logger: Any = None):
        self.logger = logger
        self.nodes = []  # مخزن العقد الكاملة
        self.matrix_vault = []  # مخزن المصفوفات المكتشفة
        self.global_ledger = ""  # السجل النصي المتراكم للرنين السياقي

        # أنماط التعرف على المصفوفات (مثلاً: [[1,0,0],[0,1,0]])
        self.matrix_regex = r"\[\s*(?:\[[\d\s\.,\-]+\]\s*,?\s*)+\]"
        # نمط التعرف على المتغيرات التقنية
        self.tech_var_regex = r"(\b[a-zA-Zθταβγδ]\d*)\s*[:=]\s*(-?\d+\.?\d*)"

    def build_global_ledger(self, chunks: List[Dict[str, Any]], generate_func) -> tuple:
        """
        [بناء السجل العالمي V2.0]:
        تحويل الكتل الخام إلى خريطة منطقية مترابطة باستخدام ذكاء المحرك C.
        """
        self.logger.info(f"🧬 [TILLAGE_CORE]: بدء صهر {len(chunks)} كتلة في سجل سيادي واحد...")

        full_summary = []
        # نستخدم حجم خطوة (Step) لتحليل عينات استراتيجية إذا كان الملف ضخماً
        # أو نعالجها بالكامل بفضل الـ 80GB RAM
        for i, chunk in enumerate(chunks):
            content = chunk.get('content', '')
            page_num = chunk.get('metadata', {}).get('page', '??')

            # استخراج المؤشرات الفنية السريعة (المصفوفات والمتغيرات)
            tech_indicators = self._harvest_matrices(content)

            # بناء "نبضة" للسجل
            pulse = f"Page {page_num}: "
            if tech_indicators:
                pulse += f"[MATRICES_DETECTED: {len(tech_indicators)}] "

            pulse += content[:200].replace('\n', ' ') + "..."
            full_summary.append(pulse)

            # تسجيل العقدة في الذاكرة النشطة
            self.register_node(chunk)

        # دمج كل النبضات في نص واحد ضخم (The Ledger)
        combined_ledger = "\n".join(full_summary)

        # استدعاء محرك الاستنتاج (Inference) لتلخيص السجل بالكامل
        # هذا هو "الرنين الإدراكي" الذي سيغذي العمليات اللاحقة
        self.logger.info("🧠 [INFERENCE_SYNC]: طلب التلخيص الاستراتيجي من المحرك C...")

        # بناء البرومبت السيادي للتلخيص
        prompt = (
            f"### [RAW KNOWLEDGE LEDGER]:\n{combined_ledger[-8000:]}\n\n"
            "### [MISSION]: Provide a high-level technical summary of this document's logic structure, "
            "focusing on kinematics, robotic parameters, and mathematical foundations."
        )

        try:
            # استدعاء دالة التوليد (Inference)
            strategic_summary, _ = generate_func(prompt, "Strategic Ledger Summary")
            self.global_ledger = str(strategic_summary)
            return self.global_ledger, True
        except Exception as e:
            self.logger.error(f"⚠️ [LEDGER_FAIL]: فشل التلخيص الاستراتيجي: {e}")
            self.global_ledger = combined_ledger[:5000] # العودة للسجل الخام في حال الفشل
            return self.global_ledger, False

    def register_node(self, node: Dict[str, Any]):
        """
        تسجيل العقدة المكتشفة وحرث البيانات منها فوراً.
        """
        content = node.get("content", "")
        node_id = node.get("id", "UNKNOWN")

        # 1. إضافة العقدة للمخزن الرئيسي
        self.nodes.append(node)

        # 2. حرث المصفوفات الرياضية
        found_matrices = self._harvest_matrices(content)
        if found_matrices:
            for mat in found_matrices:
                self.matrix_vault.append({
                    "node_id": node_id,
                    "matrix_raw": mat,
                    "timestamp": np.datetime64('now')
                })
            if self.logger:
                self.logger.debug(f"📊 [TILLAGE]: تم حصد {len(found_matrices)} مصفوفة من {node_id}")

        # 3. تحديث السجل العالمي (Global Ledger) لضمان "الرنين" في العمليات القادمة
        # نأخذ زبدة المحتوى (أول 150 حرف) لإضافتها للسياق
        summary = content[:150].replace('\n', ' ')
        self.global_ledger += f"\n📍 Node {node_id}: {summary}..."

    def harvest(self, node_id: str, content: str):
        """
        [دالة الحصاد]: استقبال البيانات من المستخلص (ملف B) وتخزينها
        بشكل لحظي لاستغلال الـ 80GB RAM.
        """
        # إضافة العقدة للمخزن
        self.nodes.append({"id": node_id, "content": content})

        # البحث عن مصفوفات في المحتوى فوراً
        found_matrices = re.findall(self.matrix_regex, content)
        if found_matrices:
            for mat in found_matrices:
                self.matrix_vault.append({
                    "node_id": node_id,
                    "matrix_raw": mat,
                    "timestamp": np.datetime64('now')
                })

        # تحديث السجل العالمي (الرنين السياقي)
        summary = content[:150].replace('\n', ' ')
        self.global_ledger += f"\n📍 {node_id}: {summary}..."

        if self.logger:
            self.logger.debug(f"🌾 [TILLAGE]: تم حصد بيانات {node_id}")

    def _harvest_matrices(self, text: str) -> List[str]:
        """استخراج المصفوفات النصية وتحويلها لأنماط قابلة للتحليل"""
        return re.findall(self.matrix_regex, text)

    def get_harvest_summary(self) -> Dict[str, Any]:
        """إرجاع ملخص لما تم حصده من الـ 224 صفحة"""
        return {
            "total_nodes": len(self.nodes),
            "total_matrices": len(self.matrix_vault),
            "ledger_size": len(self.global_ledger),
            "status": "RICH_DATA" if len(self.matrix_vault) > 0 else "TEXT_ONLY"
        }

    def get_full_ledger(self) -> str:
        """إرجاع السجل الكامل لاستخدامه في 'المحفز السيادي' (Prompt)"""
        return self.global_ledger[-5000:] # نكتفي بآخر 5000 حرف لضمان كفاءة البرومبت
