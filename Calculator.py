# Calculator.py

import numpy as np
import math
from typing import List, Dict, Any, Optional

class Calculator_:
    """
    [CORE CALCULATOR]: Hardened mathematical engine responsible for kinematic calculations,
    mechanical precision, and smooth trajectory planning.
    """
    def __init__(self, logger):
        self.logger = logger

    def calculate_precision(self, bits: Optional[int], range_max: Optional[float], schema: str = "GENERAL_TECHNICAL") -> float:
        """
        [PHASE 2: CONFIGURATION - MATH]
        Calculates resolution with full Optional support and Zero-Error handling.
        """
        # 1. المعالجة الآمنة للمدخلات (Null Safety)
        # نستخدم القيم الافتراضية السيادية في حال فشل الاستخراج من الـ PDF
        final_bits = bits if bits is not None else 12
        final_range = range_max if range_max is not None else 1.0

        try:
            # 2. ضمان عدم القسمة على صفر (ZeroDivision Safeguard)
            final_bits = max(1, final_bits)

            # 3. الحساب الرياضي الدقيق
            resolution = final_range / (2**final_bits)

            # 4. الربط مع الـ Schema المكتشف (Adaptive Logging)
            if schema == "MATHEMATICAL_STRUCTURE":
                self.logger.info(f"🔬 [CALCULATOR]: High-precision context detected. Resolution: {resolution}")

            return float(resolution)

        except Exception as e:
            # في حالة الخطأ الكارثي، نعود بالقيمة الآمنة المحسوبة مسبقاً
            self.logger.error(f"❌ [CALCULATOR]: Precision Calculation Error: {e}")
            return final_range / (2**12)

    def compute_angular_velocity(self, delta_theta: float, delta_t: float) -> float:
        """
        [حساب السرعة الزاوية]: الحفاظ على التخصص الميكانيكي مع حماية الـ Pipeline.
        """
        # حماية من القسمة على صفر التي قد تخرب مخرجات التقرير النهائي
        if delta_t <= 0:
            self.logger.warning("⚠️ [CALCULATOR]: Zero time interval in velocity calculation. Returning 0.0")
            return 0.0

        velocity = delta_theta / delta_t

        # رصد القيم الشاذة (Outliers) التي قد تشير لخطأ في بيانات المصدر
        if abs(velocity) > 500: # قيمة افتراضية للسرعات غير المنطقية
             self.logger.debug(f"⚙️ [CALCULATOR]: High angular velocity detected: {velocity}")

        return float(velocity)

    def verify_transformation_matrix(self, matrix: List[List[float]]) -> bool:
        """
        Validates D-H (Denavit-Hartenberg) or general transformation matrices.
        Ensures the matrix is a standard 4x4 structure.
        """
        try:
            # التأكد من الأبعاد الأصلية (4x4)
            if len(matrix) == 4 and all(len(row) == 4 for row in matrix):
                # فحص إضافي: هل القيم عددية؟ (لمنع انهيار المحرك عند وجود نصوص مشوهة)
                for row in matrix:
                    if not all(isinstance(val, (int, float, np.number)) for val in row):
                        return False
                return True
        except Exception:
            return False
        return False

    def calculate_transformation(self, theta: float, d: float, a: float, alpha: float) -> np.ndarray:
        """
        [KINEMATIC PROCESSOR]: Computes a 4x4 transformation matrix using standard D-H parameters.
        Used to link coordinates between adjacent mechanical segments.
        """
        # الحفاظ على الأسماء الأصلية للمعاملات
        try:
            # حماية رياضية: التأكد من أن المدخلات أرقام وليست None
            theta, d, a, alpha = map(float, [theta, d, a, alpha])

            c_th = math.cos(theta)
            s_th = math.sin(theta)
            c_al = math.cos(alpha)
            s_al = math.sin(alpha)

            # Standard D-H Sovereign Matrix - نفس الهيكل الأصلي تماماً
            return np.array([
                [c_th, -s_th * c_al,  s_th * s_al, a * c_th],
                [s_th,  c_th * c_al, -c_th * s_al, a * s_th],
                [0,     s_al,         c_al,         d     ],
                [0,     0,            0,            1     ]
            ])
        except Exception as e:
            self.logger.error(f"❌ [CALCULATOR_MATH]: Matrix computation failed: {e}")
            # العودة بمصفوفة الوحدة (Identity Matrix) لضمان عدم توقف الـ Pipeline
            return np.eye(4)

    def calculate_sovereign_resolution(self, steps: int, ratio: float, length: float) -> Dict[str, Any]:
        """
        [SOVEREIGN CALCULATOR]: Calculates theoretical micron-level resolution.
        Fixed Type Assignment: Ensuring 'steps' remains an Integer.
        """
        try:
            # 1. تصحيح الأنواع مع الحفاظ على قيم الأمان (Safety Values)
            # نستخدم int() بدلاً من float() لمتغير الخطوات
            safe_steps = int(steps) if steps > 0 else 200
            safe_ratio = float(ratio) if ratio > 0 else 1.0
            safe_length = float(length) if length > 0 else 1.0

            # 2. الحسابات الرياضية الأصلية
            # (2 * pi) / 200 يعطي زاوية الخطوة بالراديان
            step_angle = (2 * math.pi) / safe_steps
            output_angle = step_angle / safe_ratio
            linear_resolution_m = safe_length * output_angle

            # 3. بناء الحزمة المعرفية
            return {
                "status": "SUCCESS",
                "angular_res_rad": round(output_angle, 10),
                "angular_res_deg": round(math.degrees(output_angle), 6),
                "linear_res_mm": round(linear_resolution_m * 1000, 6),
                "linear_res_micron": round(linear_resolution_m * 1000000, 2),
                "metadata": {"steps": safe_steps, "effective_ratio": safe_ratio}
            }
        except Exception as e:
            self.logger.error(f"❌ [CALCULATOR_ERROR]: Calculation failed: {str(e)}")
            return {"status": "ERROR", "message": str(e)}

    def trajectory_cubic_spline(self, t: List[float], q: List[float]) -> Dict[str, Any]:
        """
        [منعم الحركة السيادي]: توليد مسار انسيابي من الدرجة الثالثة (Cubic Spline).
        يضمن استمرارية الموقع والسرعة لمنع الصدمات الميكانيكية (Jerks).
        """
        try:
            if len(t) < 2 or len(q) < 2:
                return {"status": "ERROR", "message": "نقاط غير كافية لتوليد المسار"}

            # تحديد نقطة البداية والنهاية
            t0, tf = t[0], t[-1]
            q0, qf = q[0], q[-1]

            T = tf - t0
            if T <= 0:
                raise ValueError("يجب أن يكون زمن النهاية أكبر من زمن البداية")

            # حساب المعاملات (Coefficients) بفرض سرعة البداية والنهاية = 0
            # المعادلات السيادية للمسار: q(t) = a0 + a1τ + a2τ² + a3τ³ حيث τ هو الزمن النسبي
            a0 = q0
            a1 = 0.0  # السرعة الابتدائية
            a2 = 3 * (qf - q0) / (T**2)
            a3 = -2 * (qf - q0) / (T**3)

            # توليد نقاط المسار (السرعة والتسارع أيضاً لأهميتهما في الرقابة)
            time_steps = np.linspace(0, T, 50)
            position_path = []
            velocity_path = []
            acceleration_path = []

            for tau in time_steps:
                # الموقع
                pos = a0 + a1*tau + a2*(tau**2) + a3*(tau**3)
                # السرعة (المشتقة الأولى)
                vel = a1 + 2*a2*tau + 3*a3*(tau**2)
                # التسارع (المشتقة الثانية)
                acc = 2*a2 + 6*a3*tau

                position_path.append(round(pos, 6))
                velocity_path.append(round(vel, 6))
                acceleration_path.append(round(acc, 6))

            self.logger.info(f"✅ [TRAJECTORY]: تم توليد مسار انسيابي لـ {len(position_path)} نقطة.")

            return {
                "status": "SUCCESS",
                "time_axis": (time_steps + t0).tolist(), # العودة للزمن المطلق
                "position_path": position_path,
                "velocity_path": velocity_path,
                "acceleration_path": acceleration_path,
                "metadata": {"total_time": T, "start_pos": q0, "end_pos": qf}
            }

        except Exception as e:
            self.logger.error(f"🚨 [TRAJECTORY_ERROR]: فشل توليد المسار: {e}")
            return {"status": "ERROR", "message": str(e)}
