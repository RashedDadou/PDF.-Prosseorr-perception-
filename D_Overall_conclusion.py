# D_Overall_conclusion.py

from typing import Dict, Any, Optional, TYPE_CHECKING, List
import re
import numpy as np

# 1. استخدام البروتوكول لتوضيح الأنواع (إسكات Pylance عبر الاستخدام الفعلي)
if TYPE_CHECKING:
    from P1_sovereign_utils import LoggerProtocol
else:
    LoggerProtocol = Any

class UniversalSovereignInference:
    """
    [المستنتج الشامل - النسخة الإدراكية]:
    تم تحديثه ليدار بواسطة خوارزمية الإدراك الحسي.
    """
    # 2. إضافة LoggerProtocol كنوع للبارامتر logger
    def __init__(self, logger: LoggerProtocol, data_type: str = "Robotics"):
        self.logger = logger
        self.data_type = data_type
        self.knowledge_base = {}

        # الآن Pylance سيتوقف عن الشكوى لأننا استخدمنا النوع هنا
        self.logger.info(f"🧠 [INFERENCE_ENGINE]: تم تفعيل المستنتج لبيانات: {data_type}")

    def extract_logic_pattern(self, batch_content: str, perceptual_code: Optional[Dict[str, Any]] = None):
        """
        [المستنتج السيادي V5.1]:
        تم توحيد الاستخراج وإلغاء التعارض لضمان وصول 'الوزن الإدراكي' للوحدات اللاحقة.
        """
        self.logger.debug("🔎 جاري فحص الأنماط المنطقية والكينماتيكية...")

        # 1. تقييم شدة الإدراك (Intensity)
        intensity = 1.0
        if perceptual_code and isinstance(perceptual_code, dict):
            intensity = perceptual_code.get("intensity", 1.0)

        # 2. استخراج البيانات (استخدام Batch_content المتوافق)
        variables = re.findall(r'(\w+)\s*[:=]\s*(-?\d+\.?\d*)', batch_content)
        matrix_pattern = re.findall(r'(\[[\d\s\.,\-]{5,}\])', batch_content)

        # رصد المعادلات الهندسية المعقدة (المهمة للروبوتات)
        formulas = re.findall(
            r'(\w+\s*=\s*[\w\s\*\/\+\-\(\)\.]*(?:sin|cos|tan|atan2|sqrt)[\w\s\*\/\+\-\(\)\.]*)',
            batch_content,
            re.IGNORECASE
        )

        # 3. تجميع النتائج في كائن واحد سيادي
        logic_results = {
            "vars": {k: float(v) for k, v in variables},
            "matrices": matrix_pattern,
            "formulas": list(set(formulas)),
            "perceptual_weight": intensity,
            "status": "Logic_Extracted" if (variables or formulas or matrix_pattern) else "No_Pattern_Found"
        }

        # 4. الرقابة والترقية (Priority Check)
        if intensity > 2.5:
            logic_results["priority"] = "CRITICAL_KINEMATIC_DATA"
            self.logger.info(f"🧠 [RESONANCE_HIT]: رصد رنين عالي ({intensity}) - تفعيل أولوية البيانات.")

        # العودة بنتيجة واحدة شاملة (إلغاء return patterns القديم)
        return logic_results

    def simulate_extracted_logic(self, var_map: Dict, formula_str: str, perceptual_weight: float = 1.0):
        """
        [المحاكي السيادي]: تنفيذ المعادلات المستخرجة مع تطبيق معامل الرنين.
        """
        try:
            # دمج المتغيرات مع دوال مكتبة numpy للحسابات الكينماتيكية
            safe_env = {**var_map, "np": np, "sin": np.sin, "cos": np.cos, "sqrt": np.sqrt, "atan2": np.atan2}

            # استخلاص طرف المعادلة الأيمن فقط
            if "=" in formula_str:
                formula_to_eval = formula_str.split("=")[1].strip()
            else:
                formula_to_eval = formula_str

            # الحساب الفعلي
            raw_result = eval(formula_to_eval, {"__builtins__": None}, safe_env)

            # تطبيق الوزن الإدراكي (اختياري: لتعديل الدقة أو الثقة في النتيجة)
            final_result = raw_result * perceptual_weight if isinstance(raw_result, (int, float)) else raw_result

            return round(final_result, 6)
        except Exception as e:
            self.logger.debug(f"⚠️ فشل محاكاة المعادلة {formula_str}: {e}")
            return None
