# Calculator.py

import numpy as np
import math
from typing import List, Dict, Any, Union, Optional

class Calculator_:
    """
    [الحاسب الآلي]: المحرك الرياضي الصلب المسؤول عن الحسابات الكينماتيكية،
    الدقة الميكانيكية، وتخطيط المسارات الانسيابية.
    """
    def __init__(self, logger):
        self.logger = logger

    def calculate_system_precision(self, divisions: Union[int, float], total_range: float, mode: str = "auto") -> Dict[str, Any]:
        """
        [حساب الدقة الشامل المطور]: يدعم التمييز الذكي بين البتات والخطوات مع تحليل الخطأ.
        """
        try:
            if divisions <= 0: return {"error": "Divisions must be positive"}

            # تحديد الدلالة (Denomination Logic)
            # إذا كان النمط آلي، نفترض أن أقل من 32 هو Bits (لأن 2^32 هو الحد القياسي للأنظمة)
            if mode == "bits" or (mode == "auto" and divisions < 32):
                denominator = 2**divisions
                unit_type = "Exponential (Bits)"
            else:
                denominator = divisions
                unit_type = "Linear (Steps/Divisions)"

            resolution = total_range / denominator

            return {
                "resolution": float(resolution),
                "unit_type": unit_type,
                "segments": denominator,
                "precision_percentage": (resolution / total_range) * 100 if total_range != 0 else 0
            }
        except Exception as e:
            self.logger.error(f"❌ Precision Error: {e}")
            return {"resolution": 0.0, "status": "ERROR"}

    def compute_joint_analysis(self, delta_pos: float, delta_t: float, max_limit: Optional[float] = None) -> Dict[str, Any]:
        """
        [محلل السرعة المتجهي]: يحسب السرعة مع التحقق من السلامة الفيزيائية.
        """
        if delta_t <= 0:
            return {"velocity": 0.0, "status": "STATIONARY/ERR"}

        velocity = delta_pos / delta_t

        # تحليل الحالة
        status = "NORMAL"

        # فحص max_limit: التأكد أنه ليس None قبل المقارنة
        if max_limit is not None and abs(velocity) > max_limit:
            status = "⚠️ OVER_LIMIT"
            if self.logger:
                self.logger.warning(f"Velocity {velocity} exceeds limit {max_limit}")

        return {
            "velocity": round(velocity, 6),
            "direction": "FORWARD" if velocity > 0 else "BACKWARD" if velocity < 0 else "IDLE",
            "status": status,
            "magnitude": abs(velocity)
        }

    def verify_dh_matrix(self, matrix: Union[List[List[float]], np.ndarray]) -> bool:
        """
        [مدقق النزاهة الهندسية]: لا يكتفي بالأبعاد، بل يفحص تعامد مصفوفة الدوران.
        """
        mat = np.array(matrix)
        if mat.shape != (4, 4): return False

        # فحص السطر الأخير (المعيار السيادي)
        if not np.allclose(mat[3, :], [0, 0, 0, 1], atol=1e-5): return False

        # فحص مصفوفة الدوران 3x3 (يجب أن يكون محددها 1 أو -1)
        rotation_part = mat[:3, :3]
        is_orthogonal = np.allclose(np.dot(rotation_part.T, rotation_part), np.eye(3), atol=1e-4)

        return is_orthogonal

    def calculate_forward_kinematics(self, dh_params_list: List[Dict[str, float]]) -> np.ndarray:
        """
        [سلسلة السيادة]: تضرب مصفوفات D-H لكل المفاصل للوصول للموقع النهائي.
        """
        t_total = np.eye(4)
        for params in dh_params_list:
            t_joint = self.calculate_joint_transformation(
                theta=params['theta'], d=params['d'], a=params['a'], alpha=params['alpha']
            )
            t_total = np.dot(t_total, t_joint)
        return t_total

    def calculate_joint_transformation(self, theta: float, d: float, a: float, alpha: float) -> np.ndarray:
        """
        [المعالج الرياضي المطور]: حساب مصفوفات التحويل بدقة هندسية عالية.
        التحسين: تقليل العمليات الحسابية، تنظيف القيم المتناهية الصغر، وتحسين الأداء.
        """
        import numpy as np

        # 1. الحساب المسبق للقيم المثلثية (لتحسين السرعة)
        c_th = np.cos(theta)
        s_th = np.sin(theta)
        c_al = np.cos(alpha)
        s_al = np.sin(alpha)

        # 2. بناء المصفوفة باستخدام NumPy مباشرة (أسرع من تحويل القائمة لاحقاً)
        matrix = np.array([
            [c_th, -s_th * c_al,  s_th * s_al, a * c_th],
            [s_th,  c_th * c_al, -c_th * s_al, a * s_th],
            [0.0,   s_al,         c_al,        d       ],
            [0.0,   0.0,          0.0,         1.0     ]
        ], dtype=np.float64)

        # 3. [تطوير متقدم]: تنظيف الأخطاء العشرية الصغيرة جداً
        # هذا يمنع ظهور قيم مثل -0.000000000000000122 ويحولها لصفر صريح
        matrix[np.abs(matrix) < 1e-10] = 0.0

        return matrix

    def calculate_sovereign_resolution(self, motor_steps: int, gear_ratio: float, arm_length: float) -> Dict[str, Any]:
        """
        [الحاسبة السيادية المتقدمة]: حساب الدقة الميكرونية مع تحليل النطاق العملياتي.
        تضيف طبقة من التقييم الهندسي لتحديد فئة الاستخدام المثالية.
        """
        try:
            # 1. الدفاعات السيادية (Safety Guard)
            if motor_steps <= 0 or gear_ratio <= 0 or arm_length <= 0:
                raise ValueError("المعاملات الميكانيكية يجب أن تكون موجبة تماماً.")

            # 2. الحسابات الفيزيائية الأساسية
            step_angle = (2 * math.pi) / motor_steps
            output_angle = step_angle / gear_ratio
            linear_res_m = arm_length * output_angle
            micron_res = linear_res_m * 1000000

            # 3. [الأسلوب المتقدم]: تقييم النطاق العملياتي (Operational Grade)
            # هذه الوظيفة تحول الأرقام إلى قرار هندسي
            def evaluate_grade(microns):
                if microns < 1.0: return "💎 ULTRA-PRECISION (Medical/Semiconductor)"
                if microns < 50.0: return "🛠️ HIGH-PRECISION (Micro-Assembly/Watchmaking)"
                if microns < 500.0: return "🏭 INDUSTRIAL-GRADE (CNC/3D Printing)"
                return "📦 GENERAL-PURPOSE (Pick & Place/Logistics)"

            # 4. حساب أقصى خطأ تراكمي نظري (Theoretical Backlash Impact)
            # نفترض وجود فجوة ضئيلة في التروس (0.01 درجة كمثال) لرفع واقعية التقرير
            estimated_backlash_mm = (arm_length * math.radians(0.01)) * 1000

            return {
                "status": "SUCCESS",
                "metrics": {
                    "angular_rad": round(output_angle, 10),
                    "linear_micron": round(micron_res, 2),
                    "linear_mm": round(linear_res_m * 1000, 6)
                },
                "sovereign_analysis": {
                    "operational_grade": evaluate_grade(micron_res),
                    "theoretical_stability": "STABLE" if gear_ratio >= 10 else "UNSTABLE_LOW_TORQUE",
                    "estimated_backlash_error_mm": round(estimated_backlash_mm, 4)
                },
                "metadata": {
                    "motor_steps": motor_steps,
                    "gear_ratio": gear_ratio,
                    "arm_length_m": arm_length
                }
            }

        except Exception as e:
            self.logger.error(f"❌ [CALCULATOR_ADVANCED_ERROR]: {str(e)}")
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
