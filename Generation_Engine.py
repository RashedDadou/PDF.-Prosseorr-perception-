# Generation_Engine.py

import re
from typing import List, Dict, Any, Tuple

class SovereignInferenceEngine:
    """
    [المحرك الاستدلالي]: المسؤول عن تحليل الأنماط الهندسية، استخراج المعادلات الكينماتيكية،
    وتوليد الاستنتاجات التقنية عالية الدقة.
    """
    def __init__(self, logger, embedder, openai_client=None):
        self.logger = logger
        self.embedder = embedder
        self.client = openai_client  # للربط مع OpenAI أو LM Studio

    def extract_kinematic_equations(self, text_content: str) -> List[str]:
        """
        [المجس الرياضي السيادي]: استخراج المعادلات مع محيطها المنطقي
        لضمان عدم فقدان سياق المتغيرات.
        """
        # تحسين الأنماط لتشمل المساحات، الأقواس، والرموز اللاتينية المتقدمة
        math_patterns = [
            r"T\d+\s*=\s*\[[\s\S]*?\]",               # مصفوفات التحويل (بما في ذلك المتعددة الأسطر)
            r"[θφαβγ]\d*\s*=\s*[^.!?\n]+",           # قيم الزوايا والمعادلات المثلثية
            r"J\(q\)\s*=\s*[^.!?\n]+",               # مصفوفات الياكوبي (Jacobian)
            r"[xyz]\s*=\s*f\([θq]\d*\)",             # معادلات التحويل الأمامي
            r"τ\d*\s*=\s*[^.!?\n]+",                 # معادلات العزم والديناميكا
            r"\d+\s*=\s*2\^n\s*Where\s*n\s*=\s*\d+"   # أنماط الذاكرة والتحكم التي ظهرت في تقريرك
        ]

        found_equations = []
        for pattern in math_patterns:
            # استخدام DOTALL للتعامل مع المعادلات التي تمتد لأكثر من سطر
            matches = re.findall(pattern, text_content, re.IGNORECASE | re.DOTALL)
            for m in matches:
                clean_match = " ".join(m.split()) # تنظيف المسافات الزائدة
                if len(clean_match) > 5:
                    found_equations.append(f"📐 [MATH_MODEL]: {clean_match}")

        return list(set(found_equations))

    def analyze_trajectory_logic(self, text_content: str) -> Dict[str, str]:
        """
        [محلل الأنماط السيادي]: يكتشف المنطق الهيكلي في أي نص (تقني، إداري، أو هندسي).
        تمت إضافة فلتر لمنع "تلوث الأوامر" في التقرير النهائي.
        """
        import re

        logic_map = {
            "Technical Constants": r"(fixed value|constant|threshold|parameter|coefficient)",
            "Operational Procedures": r"(step-by-step|procedure|workflow|protocol|methodology)",
            "Data Relationships": r"(correlates with|depends on|mapped to|linked with|associated)",
            "Decision Logic": r"(if-then|condition|case study|decision|priority)",
            "Kinematics/Geometry": r"(point-to-point|PTP|interpolation|coordinate|matrix|axis)"
        }

        # أنماط يجب تجاهلها تماماً لأنها تعود لأوامر النظام وليس محتوى الملف
        system_noise = r"(STRICT TARGET|OPERATIONAL COMMANDS|MATHEMATICAL INTEGRITY|STRATEGIC KNOWLEDGE)"

        results = {}
        for algo_name, pattern in logic_map.items():
            # البحث عن النمط واستخراج الجملة الكاملة
            search_pattern = rf"([^.!?\n]*?{pattern}[^.!?\n]*[\.!?])"

            # نستخدم finditer لاستخراج كافة الأنماط بدلاً من أول واحد فقط لزيادة دقة التقرير
            matches = re.finditer(search_pattern, text_content, re.IGNORECASE | re.DOTALL)

            for match in matches:
                context = match.group(1).strip()

                # التحقق: هل هذه الجملة معلومة حقيقية أم مجرد أمر من أوامر النظام؟
                if not re.search(system_noise, context, re.IGNORECASE):
                    results[algo_name] = f"⚙️ [LOGIC_FOUND]: {context}"
                    break # نكتفي بأول جملة حقيقية نظيفة لكل تصنيف

        return results

    def process_high_precision(self, chunk: str) -> Dict[str, Any]:
        """
        [بروتوكول الدقة المجهرية]: المترجم السيادي الذي يحول المعادلات الرياضية
        إلى خوارزميات برمجية جاهزة للتنفيذ.
        """
        # 1. استخراج المعادلات الكينماتيكية باستخدام المحسن الرياضي
        equations = self.extract_kinematic_equations(chunk)

        # 2. تحليل منطق المسار لتحديد نوع الخوارزمية (PTP, CP, etc.)
        trajectory_logic = self.analyze_trajectory_logic(chunk)

        # 3. بناء الـ Prompt السيادي (النسخة العالمية المرنة)
        prompt = (
            f"--- [SOVEREIGN AUDIT DATA] ---\n"
            f"TECHNICAL CONTEXT: {chunk[:2000]}\n\n"
            f"TASK FOR SENIOR DATA ARCHITECT:\n"
            f"1. Extract all structured information, key variables, and logical relations.\n"
            f"2. If mathematical patterns or formulas are present, identify them clearly.\n"
            f"3. Provide a high-level Python representation or data structure (JSON/Dict) that summarizes this logic.\n"
            f"4. Focus on the actual content of the data core, not on predefined assumptions."
        )

        self.logger.info(f"⚡ [HIGH_PRECISION]: Analyzing {len(equations)} equations and {len(trajectory_logic)} logic patterns.")

        # 4. استدعاء محرك التوليد مع هوية مرنة
        # نغير الوصف ليكون "محلل بيانات شامل" بدلاً من "مهندس روبوتات"
        role_description = "System: Senior Technical Data Analyst and Systems Architect"
        response, status = self.generate_analyzer(prompt, role_description)

        # 5. بناء الحزمة المعرفية النهائية بطريقة مرنة
        return {
            "status": status.get("engine_status", "PROCESSED"),
            "data_points_found": equations if equations else "General Technical Content",
            "detected_patterns": list(trajectory_logic.keys()) if trajectory_logic else ["Semantic Patterns"],
            "analytical_output": response,
            "complexity_level": "HIGH" if (equations and len(equations) > 3) else "STANDARD"
        }

    def generate_analyzer(self, context: str, user_request: str) -> Tuple[List[str], Dict[str, Any]]:
        """
        [المحلل الاستدلالي العالمي]: يقوم بتحليل أي نص تقنياً أو سردياً واستنتاج الأفكار
        بناءً على هوية "المحلل التقني الشامل" (Universal Technical Analyst).
        """
        try:
            # 1. تحديث الهوية عند استخدام الذكاء الاصطناعي (Deep Inference)
            if self.client:
                # تغيير الدور هنا هو المفتاح لتحرير المحرك من سجن الروبوتات
                universal_role = "System: Senior Universal Technical Analyst & Data Architect"
                return self._ai_inference(context, f"{universal_role}\nRequest: {user_request}")

            # 2. إذا كان العمل محلياً (Regex)، نستخدم أنماطاً "عالمية" لا تقتصر على الروبوتات
            technical_insights = []

            # أنماط مطورة تغطي (البيانات، العلاقات، الإجراءات، والمفاهيم الجوهرية)
            dynamic_patterns = {
                "structural": r"(table|section|chapter|framework|architecture|system)",
                "logical": r"(if|then|because|leads to|results in|process|flow)",
                "quantitative": r"(\d+(\.\d+)?|percent|total|average|sum|increase|decrease)",
                "conceptual": r"(concept|theory|strategy|objective|definition|context)",
                "technical": r"(technical|specification|parameter|data|function|variable)"
            }

            sentences = re.split(r'(?<=[.!?])\s+', context)
            seen_insights = set()

            for sent in sentences:
                sent_clean = sent.strip()

                # تصفية "ضجيج الأوامر" لكي لا تظهر تعليمات الروبوت القديمة في التقرير
                if "STRICT TARGET" in sent_clean or "OPERATIONAL COMMANDS" in sent_clean:
                    continue

                # التحقق من الأنماط الشاملة الجديدة
                matches = [label for label, pat in dynamic_patterns.items() if re.search(pat, sent_clean, re.IGNORECASE)]

                # قبول الجملة إذا كانت تحمل قيمة معلوماتية (أيا كان نوعها)
                if matches and sent_clean not in seen_insights and len(sent_clean) > 30:
                    label_str = f"[{'|'.join(matches).upper()}]"
                    technical_insights.append(f"💡 {label_str}: {sent_clean}")
                    seen_insights.add(sent_clean)

                if len(technical_insights) >= 15: break # رفع السقف لزيادة تفاصيل التقرير

            return technical_insights, {"engine_status": "UNIVERSAL_LOCAL_ANALYSIS"}

        except Exception as e:
            self.logger.error(f"Error in Universal Generation: {e}")
            return [f"Inference interrupted for: {user_request}"], {"engine_status": "ERROR"}

    def _ai_inference(self, context: str, user_request: str) -> Tuple[List[str], Dict[str, Any]]:
        """
        [محرك الاستدلال السيادي]: دالة استدلال مرنة تتكيف مع نوع المحتوى
        وتدعم أي تخصص تقني أو إداري.
        """
        # 1. صياغة محفز ذكي لا يفترض نوع المستند مسبقاً
        prompt = f"""
        ### [TECHNICAL DATA CORE]:
        {context[:3000]}  # زيادة الحجم لضمان استيعاب المصفوفات المعقدة

        ### [EXTRACTION PROTOCOL]:
        You are a Senior Technical Auditor. Based on the data above,
        execute the following request with absolute precision:
        "{user_request}"

        ### [OUTPUT REQUIREMENTS]:
        1. Extract the top 5 strategic insights.
        2. Maintain the integrity of any numerical values or formulas.
        3. Format the response in a professional, clear, and structured manner.
        """

        try:
            # هنا يتم استدعاء المحرك (سواء OpenAI أو محلي)
            # مثال: response = self.client.chat.completions.create(...)

            # نفترض أننا استلمنا الإجابة وسنحولها لقائمة
            ai_insights = ["تم استخراج البيانات بدقة عالية...", "تحليل الأنماط المكتشفة..."]

            return ai_insights, {"engine_status": "SOVEREIGN_AI_POWERED", "context_length": len(context)}

        except Exception as e:
            self.logger.error(f"🛑 [AI_INFERENCE_ERROR]: {str(e)}")
            return [f"Error: {str(e)}"], {"engine_status": "FAILED"}
