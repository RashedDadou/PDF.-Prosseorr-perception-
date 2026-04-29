# D_Overall_conclusion.py

import re
from typing import Dict, Any, List, TYPE_CHECKING

# منع دورة الاستيراد وإسكات Pylance [Invisible Logic]
if TYPE_CHECKING:
    from P1_sovereign_utils import LoggerProtocol
else:
    LoggerProtocol = any

class UniversalSovereignInference:
    """
    [المستنتج الشامل]: محرك مرن يستخلص المتغيرات (Variables) والعلاقات (Formulas)
    من أي مستند تقني، ويقوم بمحاكاة النتائج بناءً على المنطق الرياضي المستخرج.
    """
    def __init__(self, logger: 'LoggerProtocol', data_type: str = "Technical"):
        self.logger = logger
        self.data_type = data_type
        self.knowledge_base: Dict[str, Any] = {}

    def is_valid_kinematic_matrix(self, text: str) -> bool:
            """هذا هو 'الميزان' الذي يتأكد أن المصفوفة هندسية حقيقية 4x4"""
            import re
            import numpy as np

            cleaned = re.sub(r'[\[\](){},;]', ' ', str(text).lower())
            numbers = re.findall(r"[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?", cleaned)

            if len(numbers) < 16:
                return False

            try:
                matrix_data = [float(n) for n in numbers[:16]]
                matrix = np.array(matrix_data).reshape(4, 4)
                last_row = matrix[3, :]
                # التأكد أن السطر الأخير هو [0, 0, 0, 1] كما في علم الروبوتات
                return np.allclose(last_row, [0, 0, 0, 1], atol=1e-3)
            except (ValueError, IndexError):
                return False

    def simulate_logic(self, logic_data: Dict[str, Any]):
        """
        [محاكي المنطق]: تعويض المتغيرات في المعادلات لضمان صحة المنطق الهندسي.
        """
        if not logic_data or "vars" not in logic_data:
            self.logger.warning("⚠️ [SIMULATOR]: لا توجد بيانات منطقية كافية للمحاكاة.")
            return

        variables = logic_data.get("vars", {})
        formulas = logic_data.get("formulas", [])

        self.logger.info(f"🧪 [SIMULATOR]: بدء محاكاة {len(formulas)} معادلة باستخدام {len(variables)} متغير.")

        simulation_results = {}

        for formula in formulas:
            try:
                # فصل المعادلة عند علامة "=" (مثال: x = L1 * cos(theta1))
                if "=" in formula:
                    name, expr = formula.split("=", 1)
                    name = name.strip()

                    # تحويل التعبيرات الرياضية النصية إلى صيغة يفهمها بايثون
                    # ملاحظة: نستخدم مكتبة math للعمليات المثلثية
                    import math
                    safe_env = {**variables, "sin": math.sin, "cos": math.cos,
                                "tan": math.tan, "sqrt": math.sqrt, "pi": math.pi}

                    # تنفيذ التعويض (Evaluation) في بيئة آمنة
                    result = eval(expr.strip(), {"__builtins__": None}, safe_env)
                    simulation_results[name] = result
                    self.logger.debug(f"✅ [SIMULATOR]: {name} = {result:.4f}")

            except Exception as e:
                # إذا فشل التعويض (بسبب متغير ناقص مثلاً) لا يتوقف النظام
                self.logger.debug(f"🛑 [SIMULATOR_SKIP]: تعذر حساب {formula}: {e}")

        return simulation_results

    def Filtering_logical_patterns(self, batch_content: str) -> Dict[str, Any]:
        """
        [المستنتج السيادي المطور]: صيد الأنماط الهندسية بمرونة عالية وتجاهل ضجيج النظام.
        """
        import re

        # 1. تنظيف المحتوى من "تعليمات النظام" لتركيز البحث على البيانات الحقيقية
        clean_content = re.sub(r'(?i)(FORMAT|SCOPE|MISSION|INSTRUCTION):.*', '', batch_content)

        # 2. استخراج المتغيرات (دعم صيغ إضافية مثل الجداول والقيم المتبوعة بوحدات)
        # الصيغة الجديدة تدعم: x=10, x:10, x is 10, Variable 10
        var_patterns = re.findall(r'(\w+|theta\d|alpha\d|phi\d)\s*(?:[:=]|is)\s*(-?\d+\.?\d*)', clean_content, re.IGNORECASE)
        extracted_vars = {k: float(v) for k, v in var_patterns}

        # 3. استخراج المصفوفات (الرادار المرن)
        # يبحث عن أي تكتل لـ 16 رقماً داخل أقواس أو حتى بدونها
        potential_matrices = re.findall(r'((?:\[[\s\d\.\-eE,]*\]|(?:\d+\.\d+\s+){3,}\d+))', clean_content)

        valid_matrices = []
        for m in potential_matrices:
            if self.is_valid_kinematic_matrix(m):
                valid_matrices.append(m)

        # 4. استخراج المعادلات (دعم العمليات الحسابية بدون دوال مثلثية أيضاً)
        formulas = re.findall(r'(\w+\s*=\s*[\w\s\*\/\+\-\(\)\.]+(?:sin|cos|tan|atan2|sqrt|exp|pow)[\w\s\*\/\+\-\(\)\.]*)', clean_content, re.IGNORECASE)

        # حساب النزاهة الهندسية
        total_attempts = len(potential_matrices)
        success_rate = (len(valid_matrices) / total_attempts * 100) if total_attempts > 0 else 0
        self.logger.info(f"📊 [INTEGRITY]: تم فحص {total_attempts} مصفوفة بنجاح {len(valid_matrices)}")

        return {
            "vars": extracted_vars,
            "matrices": valid_matrices,
            "formulas": list(set(formulas)),
            "status": "Verified_Logic" if valid_matrices else "Heuristic_Logic"
        }

    def simulate_extracted_logic(self, var_map: dict, formula_str: str):
        """
        يقوم بتنفيذ المنطق المستخرج برمجياً مع دعم الدوال المثلثية والحماية السيادية.
        تمت إضافة دعم atan2 و np لضمان معالجة المصفوفات الحركية.
        """
        import math
        try:
            # 1. تجهيز بيئة حسابية غنية (إضافة atan2 ضرورية جداً لكينماتيكا الروبوت)
            safe_dict = {
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'atan2': math.atan2, # مضافة لصيد زوايا المفاصل بدقة
                'sqrt': math.sqrt,
                'pi': math.pi,
                'radians': math.radians,
                'degrees': math.degrees,
                'abs': abs
            }

            # 2. تنظيف وتجهيز المعادلة
            if '=' in formula_str:
                target_var = formula_str.split('=')[0].strip() # المتغير المستهدف
                expression = formula_str.split('=')[1].strip() # المعادلة الحسابية
            else:
                target_var = "Result"
                expression = formula_str.strip()

            # 3. التحقق من توفر المتغيرات المطلوبة في var_map
            # نقوم بتحويل كل المتغيرات إلى float لضمان عدم فشل eval
            clean_var_map = {k: float(v) for k, v in var_map.items()}

            # 4. التنفيذ الديناميكي في بيئة معزولة
            execution_context = {**safe_dict, **clean_var_map}

            # استخدام eval بحذر مع منع الوصول للـ builtins لضمان الأمان
            result = eval(expression, {"__builtins__": None}, execution_context)

            # 5. التنسيق النهائي للنتيجة الهندسية
            final_val = round(result, 5) if isinstance(result, (int, float)) else result
            return {
                "target": target_var,
                "value": final_val,
                "status": "Success"
            }

        except ZeroDivisionError:
            return {"status": "Error", "msg": "Division by zero"}
        except NameError as ne:
            # استخراج اسم المتغير المفقود بدقة لإعلام المستخدم
            missing_var = str(ne).split("'")[1] if "'" in str(ne) else str(ne)
            return {"status": "Incomplete", "msg": f"Missing Variable: {missing_var}"}
        except Exception as e:
            return {"status": "Complexity_Limit", "msg": str(e)}
