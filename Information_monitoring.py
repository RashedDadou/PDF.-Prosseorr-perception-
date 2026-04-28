# Information_monitoring.py

import re
import time
import logging
import numpy as np
import copy
from typing import Dict, List, Any, Optional, Tuple
from collections import deque

# استيراد الأدوات السيادية التي رفعتها
from P1_sovereign_utils import SovereignSupervisorySystem, profile_performance

class SovereignCloner:
    """
    [CLONING ENGINE V1.0]: محرك الاستنساخ الإدراكي.
    يعمل كآلية كاتبة تنسخ المستندات مع الحفاظ على الأصول في الذاكرة النشطة.
    """
    def __init__(self):
        # 1. تفعيل نظام الرقابة السيادي (هذا هو التعريف الوحيد الصحيح للوجر)
        self.logger = SovereignSupervisorySystem("CLONER_CORE")

        # 2. الذاكرة المؤقتة الدائمة (الخزنة غير القابلة للتغيير)
        self._immutable_vault = {}

        # 3. الذاكرة النشطة (الرام 80GB - حيث تتم العمليات الثقيلة)
        self.active_workspace = {}

        # 4. الذاكرة السياقية (الرنين الإدراكي)
        # بفضل سعة جهازك، رفعنا الـ maxlen لتعزيز ذاكرة النظام
        self.context_memory = deque(maxlen=20)

        self.logger.info("✅ [CLONER_READY]: تم تهيئة الخزنة والذاكرة السياقية بنجاح.")


    @profile_performance
    def process_and_clone(self, file_id: str, content: Any) -> Dict[str, Any]:
        """
        [THE SUPERVISED TYPEWRITER V5.5]:
        دمج الاستنساخ مع الرصد الحسي (sense_signal) لتوليد نسخة نشطة واعية.
        """
        self.logger.info(f"🚀 بدء الاستنساخ الإدراكي العميق للملف: {file_id}")

        # المرحلة 1: التأمين في الخزنة (Immutable Vault)
        # نستخدم نسخة عميقة لضمان عدم تلوث الأصل أثناء المعالجة
        self._immutable_vault[file_id] = {
            "original_data": str(content),
            "timestamp": time.time(),
            "status": "LOCKED"
        }

        raw_stream = str(content)

        # المرحلة 2: الرصد الحسي (المدمج - sense_signal Logic)
        # ---------------------------------------------------
        # 2.1 استخراج البصمة الترددية (الأنماط التقنية للروبوتات)
        signal_patterns = {
            "kinematic": r"(θ|τ|deg|rad|link|joint|arm|dh-params)",
            "dynamic": r"(mass|torque|inertia|force|gravity|acceleration)",
            "structural": r"(matrix|transform|jacobian|vector|eigen|projection)"
        }

        detected_frequencies = [
            tag for tag, pattern in signal_patterns.items()
            if re.search(pattern, raw_stream, re.IGNORECASE)
        ]

        # 2.2 حساب الرنين مع الذاكرة السياقية
        resonance_factor = 1.0

        # نتحقق من وجود الذاكرة، وإذا لم توجد نستخدم قائمة فارغة
        context_slice = list(self.context_memory)[-5:] if hasattr(self, 'context_memory') else []

        for past_event in context_slice:
            # تأكد من أن past_event قاموس (Dict) ويحتوي على signals
            if isinstance(past_event, dict):
                shared_signals = set(detected_frequencies) & set(past_event.get('signals', []))
                resonance_factor += (len(shared_signals) * 1.5)

        # 2.3 حساب النبضة الإدراكية (Perceptual Spike)
        spike_intensity = (len(detected_frequencies) * 2.0) * resonance_factor

        # المرحلة 3: رادار الصور والإحداثيات
        visual_map = []
        image_patterns = r"(?P<name>[\w\-_]+\.(png|jpg|jpeg|gif))|(?P<coord>rect\([\d,\s]+\))"
        for match in re.finditer(image_patterns, raw_stream, re.IGNORECASE):
            visual_map.append({
                "asset": match.group("name"),
                "coord": match.group("coord"),
                "index": match.start()
            })

        # المرحلة 4: بناء النسخة النشطة في الوعي (Active Workspace)
        # -------------------------------------------------------
        active_copy = {
            "data": raw_stream,
            "sensory_intelligence": {
                "perceptual_spike": round(spike_intensity, 2),
                "signals": detected_frequencies,
                "visual_assets": visual_map,
                "is_conscious": spike_intensity > 15.0 or len(visual_map) > 0,
                "resonance_factor": round(resonance_factor, 2)
            },
            "metadata": {
                "source_id": file_id,
                "version": "SOVEREIGN_V5.5_INTEGRATED",
                "cloned_at": time.time()
            }
        }

        # التخزين في مساحة العمل النشطة (RAM)
        self.active_workspace[file_id] = active_copy

        # تحديث ذاكرة السياق للحدث القادم
        if hasattr(self, 'context_memory'):
            self.context_memory.append({"file_id": file_id, "signals": detected_frequencies})

        if active_copy["sensory_intelligence"]["is_conscious"]:
            self.logger.info(f"🧠 [CONSCIOUS_SPIKE]: الملف {file_id} سجل شدة إدراكية: {spike_intensity}")

        return active_copy

    def finalize_session(self):
        """إغلاق المحرك واستخراج ملخص الرقابة"""
        summary = self.logger.get_audit_summary()
        self.logger.info(f"📊 ملخص الجلسة: {summary}")
        self.logger.shutdown_sequence()

    def sense_signal(self, raw_stream: str, current_context_window: deque) -> Dict[str, Any]:
        """
        [SENSORY MONITOR V1.0]: دالة الرصد الحسي للمعلومات.
        تحول النص الخام إلى 'نبضة إدراكية' بناءً على الرنين مع الذاكرة السياقية.
        """

        # 1. المرحلة الحسية: استخراج "البصمة الترددية" (Patterns)
        # لا نبحث عن كلمات فقط، بل عن "هياكل" (رموز رياضية، قيم عددية، علاقات)
        signal_patterns = {
            "kinematic": r"(θ|τ|deg|rad|link|joint|arm)",
            "dynamic": r"(mass|torque|inertia|force|gravity)",
            "structural": r"(matrix|transform|jacobian|vector|eigen)"
        }

        detected_frequencies = []
        for tag, pattern in signal_patterns.items():
            if re.search(pattern, raw_stream, re.IGNORECASE):
                detected_frequencies.append(tag)

        # 2. استدعاء الذاكرة السياقية (Contextual Resonance)
        # فحص "الرنين" مع آخر 5 أحداث في الذاكرة لرفع درجة الإدراك
        resonance_factor = 1.0
        for past_event in list(current_context_window)[-5:]:
            # إذا كان هناك تطابق في التردد بين الماضي والحاضر، يحدث "رنين" (Resonance)
            shared_signals = set(detected_frequencies) & set(past_event.get('signals', []))
            resonance_score = len(shared_signals) * 1.5
            resonance_factor += resonance_score

        # 3. حساب "النبضة الإدراكية" (Perceptual Spike)
        # شدة النبضة تعتمد على وجود المعلومات + الرنين مع السياق
        spike_intensity = (len(detected_frequencies) * 2.0) * resonance_factor

        # 4. الترميز الحسي النهائي (Sensory Encoding)
        sensory_code = {
            "perceptual_spike": round(spike_intensity, 2),
            "signals": detected_frequencies,
            "is_conscious": spike_intensity > 15.0, # هل المعلومة تستحق الانتقال للوعي؟
            "timestamp": time.time()
        }

        return sensory_code

class PerceptualPerceptionEngine:
    """
    [PERCEPTUAL ENGINE V1.0]:
    نظام إدراك حسي يعتمد على الترميز النبضي والتغذية السياقية.
    """
    def __init__(self, logger=None, memory_size: int = 100): # أضف logger هنا
            # الذاكرة السياقية المؤقتة
            self.contextual_memory = deque(maxlen=memory_size)
            # مصفوفة الأوزان الإدراكية
            self.perceptual_weights = {}

            # الإصلاح: نستخدم اللوجر الممرر، أو ننشئ واحدًا افتراضيًا إذا كان None
            if logger:
                self.logger = logger
            else:
                import logging
                self.logger = logging.getLogger("PerceptionEngine")

    @profile_performance
    def sense_and_encode(self, raw_input: str, sensory_schema: str) -> Dict[str, Any]:
        """
        [THE DIPLOMATIC ENCODER]:
        تحويل المدخلات الخام إلى كود حسي عبر إدارة متوازنة للدوال المساعدة وتوافق مع آلية الاستنساخ.
        """
        # 1. المرحلة الدبلوماسية الأولى: التحقق والاستخراج اللطيف
        # نضمن أن المدخلات نصية لتجنب كسر دالة التوقيع الترددي
        safe_input = str(raw_input) if raw_input else ""

        # استدعاء الدالة الأصلية لاستخراج الترددات
        frequency_signature = self._extract_frequency_signature(safe_input)

        # 2. المرحلة الدبلوماسية الثانية: تقييم الرنين السياقي
        # إذا كانت الترددات فارغة، نتعامل معها كـ "نبضة هادئة" دون توقف النظام
        if not frequency_signature:
            self.logger.warning(f"⚠️ [SENSE]: لم يتم رصد ترددات واضحة في الوسم {sensory_schema}")
            perception_intensity = 1.0 # إدراك أساسي محايد
        else:
            # استدعاء الدالة الأصلية لحساب الرنين بناءً على الذاكرة السياقية
            perception_intensity = self._calculate_resonance(frequency_signature)

        # 3. المرحلة الدبلوماسية الثالثة: الترميز المتوافق (The Perceptual Encoding)
        # نستخدم np.datetime64 لضمان دقة الطابع الزمني كما في التصميم الأصلي
        perceptual_code = {
            "signature": frequency_signature,
            "intensity": perception_intensity,
            "schema_tag": sensory_schema,
            "timestamp": np.datetime64('now'),
            "is_conscious": perception_intensity > 2.0 # عتبة وعي دبلوماسية
        }

        # 4. التغذية الراجعة وتحديث الذاكرة
        # نغذي الذاكرة السياقية فوراً لرفع الوعي اللحظي للعمليات القادمة
        self.contextual_memory.append(perceptual_code)

        # 5. التوافق مع process_and_clone:
        # نقوم بإرسال إشارة للمراقب إذا كانت النبضة تتطلب "انتباه" المحرك السيادي
        if perceptual_code["is_conscious"]:
            self.logger.info(f"✨ [DIPLOMAT]: رصد رنين عالي ({perception_intensity}) تحت وسم {sensory_schema}")

        return perceptual_code


    def _calculate_resonance(self, current_signature: List[str]) -> float:
        """
        حساب الرنين: هل المعلومة الحالية "مألوفة" أو "مكملة" لما في الذاكرة؟
        """
        if not self.contextual_memory:
            return 1.0  # إدراك أساسي

        resonance_score = 1.0
        # فحص آخر 10 نبضات في الذاكرة السياقية
        recent_memory = list(self.contextual_memory)[-10:]

        for past_code in recent_memory:
            # إذا كانت الكلمات تتكرر، يزداد "الرنين الإدراكي" (تصبح المعلومة حساسة)
            common_elements = set(current_signature) & set(past_code['signature'])
            resonance_score += (len(common_elements) * 0.5)

        return resonance_score

    def _extract_frequency_signature(self, text: str) -> List[str]:
        # استخراج العناصر التي تمثل "هوية" النص التقنية
        return re.findall(r'\b\w{4,}\b', text.lower()) # كمثال عام
