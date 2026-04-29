# C_Tillage_engine_PDF_files.py

import ast
import operator
import math
from typing import Dict, Any, Union, TYPE_CHECKING, Optional, Sequence

if TYPE_CHECKING:
    from P1_sovereign_utils import LoggerProtocol
else:
    LoggerProtocol = Any

class SafeSovereignEvaluator:
    """
    [المقيم السيادي الآمن]: يقوم بتحليل المعادلات الرياضية برمجياً.
    """
    # العمليات والدوال المسموح بها (كما هي في كودك)
    ALLOWED_OPERATORS = {
        ast.Add: operator.add, ast.Sub: operator.sub,
        ast.Mult: operator.mul, ast.Div: operator.truediv,
        ast.Pow: operator.pow, ast.USub: operator.neg
    }

    ALLOWED_FUNCTIONS = {
        'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
        'sqrt': math.sqrt, 'radians': math.radians, 'pi': math.pi,
        'atan2': math.atan2
    }

    def __init__(self, logger: Optional['LoggerProtocol'] = None):
        # الحل الاحترافي: إخبار Pylance أن الـ logger قد يكون None (Optional)
        self.logger: Optional['LoggerProtocol'] = logger

    def safe_eval(self, node: Any, var_map: Dict[str, float]) -> Any:
        """
        تحليل شجرة الكود (AST) وتحويلها إلى قيم رياضية حقيقية.
        """
        # للأرقام (بايثون 3.8+)
        if isinstance(node, ast.Constant):
            return node.value

        # للمتغيرات الهندسية (L1, theta1)
        elif isinstance(node, ast.Name):
            if node.id in var_map:
                return var_map[node.id]
            elif node.id in self.ALLOWED_FUNCTIONS:
                return self.ALLOWED_FUNCTIONS[node.id]
            raise NameError(f"🚫 [UNDEFINED_VAR]: المتغير '{node.id}' غير موجود في قاعدة البيانات.")

        # للعمليات الثنائية (+, -, *, /)
        elif isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type in self.ALLOWED_OPERATORS:
                return self.ALLOWED_OPERATORS[op_type](
                    self.safe_eval(node.left, var_map),
                    self.safe_eval(node.right, var_map)
                )
            raise TypeError(f"⚠️ [UNSUPPORTED_OP]: العملية {op_type} غير مدعومة.")

        # للعمليات الأحادية (مثل -5)
        elif isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type in self.ALLOWED_OPERATORS:
                return self.ALLOWED_OPERATORS[op_type](
                    self.safe_eval(node.operand, var_map)
                )
            raise TypeError(f"⚠️ [UNSUPPORTED_UNARY]: {op_type} غير مدعومة.")

        # استدعاء الدوال مثل sin(theta)
        elif isinstance(node, ast.Call):
            func = self.safe_eval(node.func, var_map)
            args = [self.safe_eval(arg, var_map) for arg in node.args]

            # التأكد من أن الكائن قابل للاستدعاء (مثل math.sin)
            if callable(func):
                return func(*args)
            raise TypeError(f"❌ [NOT_CALLABLE]: الكائن {type(func)} ليس دالة رياضية.")

        else:
            raise TypeError(f"🛡️ [SECURITY_ALERT]: تم رصد محاولة تشغيل عملية غير مسموح بها: {type(node)}")

    def evaluate_expression(self, expression: str, var_map: Dict[str, float]) -> float:
        """
        دالة المداخل الرئيسية: تحول النص إلى نتيجة رقمية.
        """
        try:
            tree = ast.parse(expression, mode='eval')
            result = self.safe_eval(tree.body, var_map)
            return float(result)
        except Exception as e:
            # يمكن ربط هذا بـ logger النظام لاحقاً
            raise ValueError(f"فشل تقييم المعادلة '{expression}': {str(e)}")

    def simulate_extracted_logic(self, var_map: dict, formula_str: str):
        """
        [منفذ المنطق السيادي]: تنفيذ المعادلات المستخرجة بأمان تام ودعم كامل للكينماتيكا.
        """
        try:
            # 1. معالجة المعادلة وتجهيز الطرف الأيمن فقط للحساب
            target_expression = formula_str
            if '=' in formula_str:
                # نأخذ ما بعد علامة الـ "=" فقط
                target_expression = formula_str.split('=', 1)[1].strip()

            # 2. تهيئة المقيم الآمن (الذي بنيناه في الوحدة C)
            evaluator = SafeSovereignEvaluator()

            # 3. التحويل البرمجى إلى AST (Abstract Syntax Tree)
            # وضعنا ميزة الإصلاح التلقائي للمسافات لضمان عدم فشل الـ parsing
            clean_expr = target_expression.replace('^', '**').strip()
            tree = ast.parse(clean_expr, mode='eval')

            # 4. التنفيذ والحصول على النتيجة الرقمية
            result = evaluator.safe_eval(tree.body, var_map)

            # 5. التنسيق النهائي: تقريب للروبوتات (5 خانات عشرية)
            if isinstance(result, (int, float)):
                return round(float(result), 5)
            return result

        except Exception as e:
            # التصحيح السيادي: التحقق الصريح من أن الـ logger ليس None
            # هذا يخبر Pylance يقيناً أن الاستدعاء آمن
            if self.logger is not None:
                self.logger.debug(f"🛑 [LOGIC_EXEC_FAIL]: {formula_str} | {str(e)}")

            return f"Execution Error: {str(e)}"

class TillageenginePDFfiles:
    """
    هذا هو 'منظم الدفعات السيادي'.
    وظيفتة تقسيم الـ 217 كتلة إلى مجموعات صغيرة وإرسالها لـ LM Studio
    مع الحفاظ على 'خريطة معرفية' تربط أجزاء الكتاب ببعضها.
    """
    def __init__(self, batch_size=4): # تقليل العدد من 8 إلى 4 لزيادة التركيز
        self.batch_size = batch_size
        self.global_ledger = "" # هذه هي الشبكة الاستدلالية التي اقترحتها أنت

    def stream_to_engine(self, all_chunks: Sequence[Union[Dict[str, Any], str]], generate_func):
        """
        [النسخة السيادية الملحمية]: معالجة دفعات متسلسلة مع الحفاظ على سلامة المعادلات الهندسية.
        """

        self.global_ledger = "INITIATING NEUTRAL AUDIT..." # تصفير التاريخ القديم

        final_insights = []
        total_chunks = len(all_chunks)
        # ذاكرة سياقية قصيرة للحفاظ على ترابط المعادلات بين الدفعات
        contextual_bridge = ""

        for i in range(0, total_chunks, self.batch_size):
            batch = all_chunks[i:i + self.batch_size]

            # 1. استخراج النص بذكاء (التوافق مع Dict أو str)
            batch_texts = []
            for c in batch:
                content = c.get('content', '') if isinstance(c, dict) else str(c)
                if content.strip():
                    batch_texts.append(content)

            # دمج السياق السابق مع الدفعة الحالية لمنع قطع المصفوفات في المنتصف
            current_raw_context = "\n".join(batch_texts)
            current_full_context = contextual_bridge + "\n" + current_raw_context

            # 2. تحديث الجسر السياقي (أخذ آخر 500 حرف لضمان عدم قطع مصفوفة 4x4)
            contextual_bridge = current_raw_context[-500:] if len(current_raw_context) > 500 else current_raw_context

            # 3. صياغة الأوامر العملياتية (تغيير من "روبوت" إلى "شامل")
            # إذا كنت تريد نظاماً يقرأ أي شيء، اجعل الأوامر عامة:
            extraction_targets = (
                "STRICT TARGET: Identify and catalog all key entities, numerical values, and structured relationships.\n"
                "FORMAT: Extract data in clear key-value pairs or structured blocks (e.g., [Variable: Value]).\n"
                "SCOPE: Capture technical, administrative, or analytical insights without domain bias."
            )

            # 4. بناء "المحفز السيادي" (Sovereign Prompt)
            # ملاحظة: إذا كان الـ global_ledger يحتوي على مخلفات قديمة، يجب تصفيره عند بداية كل ملف
            sovereign_prompt = (
                f"### [DOCUMENT CONTEXT]:\n{self.global_ledger[-1500:]}\n\n" # تقليل الحجم لترك مساحة للبيانات
                f"### [EXTRACTION PROTOCOL]:\n{extraction_targets}\n\n"
                f"### [CURRENT RAW DATA - BATCH {i//self.batch_size + 1}]:\n{current_full_context}\n\n"
                f"### [MISSION]: Exhaustive Data Extraction. Recover EVERY technical detail, name, date, and relationship found in this batch."
            )

            print(f"🚀 [TURBO-MODE] Processing Batch {i//self.batch_size + 1}/{ (total_chunks // self.batch_size) + 1}...")

            # 5. استدعاء محرك التوليد
            try:
                ideas, _ = generate_func(sovereign_prompt, "Critical Technical Audit")

                if ideas:
                    final_insights.extend(ideas)

                    # تحديث السجل العالمي بنقاط ارتكاز ذكية (Nodes)
                    summary_concepts = [text.strip() for text in ideas if len(text) > 20][:2]
                    node_entry = f"\n📍 Node {i//self.batch_size + 1}: {'. '.join(summary_concepts)}"
                    self.global_ledger += node_entry

            except Exception as e:
                print(f"⚠️ [ENGINE_SKIP] Error in Batch {i//self.batch_size + 1}: {str(e)}")
                continue

            # داخل الملف C - الجزء 5
            if ideas:
                final_insights.extend(ideas)
                # فحص فوري سريع: هل تحتوي الدفعة على مصفوفة كاملة؟
                matrix_found = any(str(idea).count(',') >= 15 for idea in ideas)
                if matrix_found:
                    print(f"💎 [STABILITY_SYNC]: تم تأمين مصفوفة مكتملة في الدفعة {i//self.batch_size + 1}")

        return final_insights
