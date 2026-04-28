# C_Tillage_engine_PDF_files.py

import ast
import operator
import math
from typing import Dict, Any, Union, Sequence

class SafeSovereignEvaluator:
    # توحيد العمليات في مكان واحد لسهولة الصيانة
    ALLOWED_OPERATORS = {
        ast.Add: operator.add, ast.Sub: operator.sub,
        ast.Mult: operator.mul, ast.Div: operator.truediv,
        ast.Pow: operator.pow, ast.USub: operator.neg,
        ast.BinOp: None # نحتاجه للتحليل الهيكلي
    }

    def __init__(self, logger=None):
        self.logger = logger if logger else self._setup_fallback_logger()

        # القاموس الموحد للدوال والمتغيرات الرياضية
        self.functions = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'sqrt': math.sqrt,
            'radians': math.radians,
            'pi': math.pi,
            'abs': abs
        }

    def _setup_fallback_logger(self):
        import logging
        log = logging.getLogger("Sovereign_Fallback")
        log.warning("⚠️ [SAFE_EVAL]: Initialized with fallback logger.")
        return log

    def safe_eval(self, node, var_map):
        """
        [التنفيذ السيادي]: فحص العقد وتوجيه العمليات بناءً على نوعها.
        """
        # 1. التعامل مع الأرقام الثابتة
        if isinstance(node, ast.Constant): # Python 3.8+
            return node.value
        elif isinstance(node, ast.Num): # النسخ الأقدم
            return node.n

        # 2. التعامل مع المتغيرات (L1, theta1, etc.)
        elif isinstance(node, ast.Name):
            if node.id in var_map:
                return var_map[node.id]
            if node.id in self.functions:
                return self.functions[node.id]
            raise NameError(f"Variable '{node.id}' is not defined in Sovereign Map.")

        # 3. التعامل مع العمليات الحسابية (+, -, *, /)
        elif isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type in self.ALLOWED_OPERATORS:
                left = self.safe_eval(node.left, var_map)
                right = self.safe_eval(node.right, var_map)
                return self.ALLOWED_OPERATORS[op_type](left, right)
            raise TypeError(f"Operator {op_type} is NOT allowed.")

        # 4. التعامل مع استدعاء الدوال (cos, sin)
        elif isinstance(node, ast.Call):
            # التأكد أن الاستدعاء هو اسم مباشر لدالة (مثل cos) وليس (math.cos)
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
                if func_name in self.functions:
                    args = [self.safe_eval(arg, var_map) for arg in node.args]
                    return self.functions[func_name](*args)
                raise NameError(f"Function '{func_name}' is NOT allowed.")
            else:
                # في حال حاول أحد استخدام استدعاءات معقدة مثل math.cos
                raise ValueError("Complex function calls (e.g., math.cos) are not supported. Use direct names.")

        # 5. العمليات الأحادية (مثل -5)
        elif isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type in self.ALLOWED_OPERATORS:
                return self.ALLOWED_OPERATORS[op_type](self.safe_eval(node.operand, var_map))

    def simulate_extracted_logic(self, var_map: dict, formula_str: str):
        """
        [محاكي المنطق السيادي]: تنفيذ المعادلات المستخرجة مع دعم الدوال المثلثية.
        تم تحسينه لضمان استقرار حسابات الـ Forward Kinematics.
        """
        try:
            # 1. تنظيف وتجهيز المعادلة
            if '=' in formula_str:
                # نأخذ ما بعد اليساوي إذا كانت المعادلة كاملة (x = ...)
                formula_str = formula_str.split('=')[1].strip()

            # 2. تجهيز القاموس الرياضي (حقن دوال الجيب والتمام)
            # لضمان أن المعادلات مثل L1 * cos(theta1) تعمل فوراً
            safe_vars = {
                'cos': math.cos,
                'sin': math.sin,
                'tan': math.tan,
                'sqrt': math.sqrt,
                'pi': math.pi,
                **var_map # دمج متغيرات المستخدم (L1, q2, etc.)
            }

            # 3. التحليل والتنفيذ باستخدام SafeSovereignEvaluator
            # ملاحظة: تأكد أن كلاس SafeSovereignEvaluator يدعم تمرير القاموس الرياضي
            evaluator = SafeSovereignEvaluator(logger=self.logger)

            tree = ast.parse(formula_str, mode='eval')
            result = evaluator.safe_eval(tree.body, safe_vars)

            return round(result, 5) if isinstance(result, (int, float)) else result

        except Exception as e:
            # فحص السيادة: هل الـ logger موجود فعلاً؟
            error_msg = f"⚠️ [SIMULATION_ERROR]: {str(e)} in formula: {formula_str}"

            if self.logger:
                self.logger.error(error_msg)
            else:
                print(error_msg) # Fallback للطباعة العادية إذا كان None

            return f"Logic Execution Error: {str(e)}"

class TillageenginePDFfiles:
    """
    هذا هو 'منظم الدفعات السيادي'.
    وظيفتة تقسيم الـ 217 كتلة إلى مجموعات صغيرة وإرسالها لـ LM Studio
    مع الحفاظ على 'خريطة معرفية' تربط أجزاء الكتاب ببعضها.
    """
    def __init__(self, batch_size=4): # تقليل العدد من 8 إلى 4 لزيادة التركيز
        self.batch_size = batch_size
        self.global_ledger = "" # هذه هي الشبكة الاستدلالية التي اقترحتها أنت

    def stream_to_engine(self, all_chunks: Sequence[Union[Dict[str, Any], str]], generate_func, context_schema: str = "GENERAL"):
        """
        [النسخة السيادية الملحمية V3.2]: معالجة دفعات متسلسلة مع حقن السياق المكتشف (Schema-Aware).
        تم التعديل لإصلاح خطأ context_schema وإزالة انحياز الروبوتات.
        """
        final_insights = []
        total_chunks = len(all_chunks)
        contextual_bridge = ""

        # 1. إعداد الأوامر العملياتية بناءً على السياق (Dynamic Operational Commands)
        # بدلاً من تثبيت "الروبوتات"، نغير الأهداف بناءً على نوع الملف المكتشف
        if context_schema == "MATHEMATICAL_STRUCTURE":
            extraction_targets = (
                "STRICT TARGET: Extract 4x4 Transformation Matrices and Kinematic Chains.\n"
                "TECHNICAL FOCUS: Identify variables (theta, L, alpha, d) and verify matrix integrity.\n"
                "MATHEMATICAL INTEGRITY: No row or equation fragmentation allowed."
            )
        elif context_schema == "DATA_TABLE":
            extraction_targets = (
                "STRICT TARGET: Extract structural data and tabular relationships.\n"
                "TECHNICAL FOCUS: Map numeric values to their specific headers and units.\n"
                "DATA INTEGRITY: Ensure row-column synchronization is preserved."
            )
        else:
            extraction_targets = (
                "STRICT TARGET: Extract core technical specifications and system logic.\n"
                "TECHNICAL FOCUS: Identify components, standards, and operational parameters.\n"
                "INTEGRITY: Preserve the semantic hierarchy of the documentation."
            )

        for i in range(0, total_chunks, self.batch_size):
            batch = all_chunks[i:i + self.batch_size]

            # (نفس منطق استخراج النصوص وتحديث الجسر السياقي الخاص بك...)
            batch_texts = []
            for c in batch:
                content = c.get('content', '') if isinstance(c, dict) else str(c)
                if content.strip():
                    batch_texts.append(content)

            current_raw_context = "\n".join(batch_texts)
            current_full_context = contextual_bridge + "\n" + current_raw_context
            contextual_bridge = current_raw_context[-500:] if len(current_raw_context) > 500 else current_raw_context

            # 2. بناء "المحفز السيادي" (Sovereign Prompt) مع حقن السياق
            sovereign_prompt = (
                f"### [STRATEGIC KNOWLEDGE MAP (PREVIOUS)]:\n{self.global_ledger[-2000:]}\n\n"
                f"### [SCHEMA CONTEXT]: {context_schema}\n"  # حقن السياق هنا
                f"### [OPERATIONAL COMMANDS]:\n{extraction_targets}\n\n"
                f"### [CURRENT DATA CORE - BATCH {i//self.batch_size + 1}]:\n{current_full_context}\n\n"
                f"### [MISSION]: Execute a critical technical audit under the {context_schema} protocol."
            )

            print(f"🚀 [TURBO-MODE] Processing Batch {i//self.batch_size + 1}/{ (total_chunks // self.batch_size) + 1}...")

            # 3. استدعاء محرك التوليد (نفس المنطق الخاص بك)
            try:
                # نمرر الـ schema للمحرك لزيادة الدقة
                ideas, _ = generate_func(sovereign_prompt, f"Critical {context_schema} Audit")

                if ideas:
                    final_insights.extend(ideas)
                    summary_concepts = [text.strip() for text in ideas if len(text) > 20][:2]
                    node_entry = f"\n📍 Node {i//self.batch_size + 1} ({context_schema}): {'. '.join(summary_concepts)}"
                    self.global_ledger += node_entry
            except Exception as e:
                print(f"⚠️ [ENGINE_SKIP] Error in Batch {i//self.batch_size + 1}: {str(e)}")
                continue

        return final_insights
