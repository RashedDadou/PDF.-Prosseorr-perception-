# Generation_Engine.py

import re
from typing import List, Dict, Any, Tuple, Optional

class SovereignInferenceEngine:
    """
    [المحرك الاستدلالي]: المسؤول عن تحليل الأنماط الهندسية، استخراج المعادلات الكينماتيكية،
    وتوليد الاستنتاجات التقنية عالية الدقة.
    """
    def __init__(self, logger, embedder, openai_client=None):
        self.logger = logger
        self.embedder = embedder
        self.client = openai_client  # للربط مع OpenAI أو LM Studio

    def analyze_chunk(self, text: str, schema: str = "GENERAL_TECHNICAL") -> Optional[str]:
        try:
            # 1. تجهيز الطلب
            formatted_task = f"Execute technical audit under {schema} protocol."

            # 2. الاستدعاء المتوافق مع Master Generator
            # نضع النص (text) في خانة الـ context لأن الـ Regex Engine يحلل الـ context
            response, stats = self.generate(
                context=text,            # هنا يتم البحث عن الأنماط (Patterns)
                user_request=formatted_task # هنا يتم توجيه المهمة (للـ AI فقط)
            )

            # 3. معالجة مخرجات الـ Tuple
            if response and isinstance(response, list):
                # دمج النتائج المستخرجة (سواء من AI أو Regex) في نص واحد
                return "\n".join(response)

            return None

        except Exception as e:
            self.logger.error(f"⚠️ [ANALYSIS_ERROR]: {e}")
            return None

    def predict_document_schema(self, sample_text: str) -> str:
        """
        [PHASE 1: PREDICTION]
        Analyzes content structure to identify the technical domain.
        Ensures the engine remains 'Agnostic' and adapts to any scientific field.
        """
        import re
        sample_lower = sample_text.lower()

        # 1. SCIENTIFIC & MATHEMATICAL SCHEMA
        # Removed specific robot terms like 'theta' to avoid domain bias.
        # Now looks for general mathematical operators and matrix notation.
        math_indicators = r"(\[\[.*\]\]|matrix|transformation|eigen|integral|derivative|vector)"
        if re.search(math_indicators, sample_lower):
            self.logger.info("🔮 [PREDICTION]: Mathematical/Scientific Schema Detected.")
            return "MATHEMATICAL_STRUCTURE"

        # 2. TABULAR & STRUCTURED DATA SCHEMA
        # Identifies data organized in rows, columns, or CSV formats.
        data_indicators = r"(\d+\.\d+,|csv|table|index|column|row|database|dataset)"
        if re.search(data_indicators, sample_lower):
            self.logger.info("🔮 [PREDICTION]: Tabular Data Schema Detected.")
            return "DATA_TABLE"

        # 3. SYSTEM ARCHITECTURE & CODE SCHEMA
        # Detects software logs, class definitions, or stack traces.
        system_indicators = r"(error|debug|traceback|def |class |import |log_level|exception)"
        if re.search(system_indicators, sample_lower):
            self.logger.info("🔮 [PREDICTION]: System/Software Schema Detected.")
            return "TECHNICAL_LOG"

        # 4. NARRATIVE / DOCUMENTATION SCHEMA
        # Default for descriptive technical manuals or research papers.
        self.logger.info("🔮 [PREDICTION]: General Engineering/Narrative Schema Detected.")
        return "GENERAL_TECHNICAL"

    def sovereign_discovery_handler(self, chunk: str):
        """
        [THE MASTER HANDLER]: Integrates Prediction, Configuration, and Exploration.
        Fully decoupled from 'Robot Bias' for global GitHub standards.
        """
        # Step 1: PREDICTION (Phase 1)
        # تحديد هوية المستند قبل اتخاذ أي قرار استخراج
        schema = self.predict_document_schema(chunk[:2000])

        # Step 2: DYNAMIC CONFIGURATION (Phase 2)
        # بناء الهدف الاستخراجي بناءً على "الهوية" المكتشفة وليس بشكل مسبق
        if schema == "MATHEMATICAL_STRUCTURE":
            extraction_goal = "Extract all high-dimensional arrays, transformation matrices, and technical constants."
        elif schema == "DATA_TABLE":
            extraction_goal = "Map structured datasets, identify columnar relationships, and key-value pairs."
        elif schema == "TECHNICAL_LOG":
            extraction_goal = "Identify system events, error patterns, and operational state transitions."
        else:
            extraction_goal = "Analyze core engineering principles, definitions, and strategic technical insights."

        # Step 3: STRUCTURAL EXPLORATION (Phase 3)
        # استخدام لغة صارمة تمنع "فخ التكرار" (Echo Trap) وتضمن نقاء البيانات
        discovery_prompt = (
            f"### [STRATEGIC DISCOVERY PROTOCOL] ###\n"
            f"TARGET_SCHEMA: {schema}\n"
            f"EXTRACTION_GOAL: {extraction_goal}\n"
            f"STRICT_FILTER: DO NOT mirror these instructions. OUTPUT RAW DATA ONLY.\n"
            f"----------------------------------------\n"
            f"SOURCE_DATA:\n{chunk}"
        )

        # تنفيذ الاستخراج باستخدام المحرك السيادي (سواء كان AI أو Local)
        # نستخدم _sovereign_ai_discovery لضمان التوافقية مع self.client
        return self._sovereign_ai_discovery(chunk)

    def extract_kinematic_equations(self, text_content: str) -> List[str]:
        """
        [GLOBAL STRUCTURAL PROBE]: Extracts mathematical models, matrices,
        and technical constants across any engineering domain.
        Upgraded to eliminate 'Robot Bias'.
        """
        # أنماط رياضية عامة (General Engineering Patterns)
        # بدلاً من البحث عن T أو J، نبحث عن "هيكل" المعادلة والمصفوفة
        patterns = [
            r"[A-Z]\w*\s*=\s*\[[\s\S]*?\]",           # Any Matrix assignment (A=[...], M=[...])
            r"[a-z\u0370-\u03ff]\d*\s*=\s*[^.!?\n]+", # Greek letters or variables with assignments
            r"\w+\([a-z\d, ]+\)\s*=\s*[^.!?\n]+",    # Functions f(x), G(s), etc.
            r"[\d\.]+\s*[+\-*/^]\s*[\d\.]+",         # Direct arithmetic expressions
            r"\|\|.*?\|\|",                          # Norms or absolute values
            r"\\begin\{matrix\}.*?\\end\{matrix\}"   # LaTeX style matrices (common in technical PDFs)
        ]

        found_structures = []
        for pattern in patterns:
            # DOTALL لضمان قراءة المصفوفات متعددة الأسطر
            matches = re.findall(pattern, text_content, re.IGNORECASE | re.DOTALL)
            for m in matches:
                # تنظيف النص وتجنب "صدى الأوامر" (Echo Trap)
                clean_match = " ".join(m.split())

                # تصفية النصوص التي تشبه التعليمات البرمجية الخاصة بنا
                if "strict target" in clean_match.lower():
                    continue

                if len(clean_match) > 5:
                    # نستخدم وسم عام بدلاً من [MATH_MODEL] لتعزيز الحيادية
                    found_structures.append(f"📊 [STRUCTURAL_DATA]: {clean_match}")

        # استخدام set لضمان عدم تكرار البيانات (Deduping)
        return list(set(found_structures))

    def analyze_trajectory_logic(self, text_content: str, schema: str = "GENERAL_TECHNICAL") -> Dict[str, str]:
        """
        [GLOBAL LOGIC ANALYZER]: Connects data patterns with their technical context.
        Upgraded to be Schema-Aware to prevent 'Robot Bias'.
        """
        # 1. بناء خرائط منطقية متنوعة بناءً على "التنبؤ" (Phase 2: Configuration)
        if schema == "MATHEMATICAL_STRUCTURE":
            # خريطة للملفات الهندسية والحركية العامة
            logic_map = {
                "Motion_Control": r"(interpolation|velocity|acceleration|control loop|feedback)",
                "System_Stability": r"(convergence|tolerance|error margin|stability|equilibrium)",
                "Geometric_Logic": r"(coordinate system|transformation|vector|alignment|mapping)"
            }
        elif schema == "DATA_TABLE":
            # خريطة لملفات الجداول والبيانات الضخمة
            logic_map = {
                "Data_Structure": r"(index|primary key|schema|sorting|classification)",
                "Aggregation": r"(summation|average|totals|statistical|distribution)"
            }
        else:
            # الخريطة الافتراضية (تغطي الروبوتات وغيرها بشكل متوازن)
            logic_map = {
                "Sequence_Logic": r"(sequential|point-to-point|process flow|operational steps)",
                "Safety_Protocol": r"(avoidance|collision|protection|emergency|limit)",
                "Optimization": r"(algorithm|efficiency|performance|PID|tuning)"
            }

        results = {}
        for algo_name, pattern in logic_map.items():
            # البحث عن النمط واستخراج السياق الكامل (Context-Aware)
            search_pattern = rf"([^.!?\n]*?{pattern}[^.!?\n]*[\.!?])"
            match = re.search(search_pattern, text_content, re.IGNORECASE | re.DOTALL)

            if match:
                context = match.group(1).strip()
                # جعل المخرجات احترافية بالإنكليزية لـ GitHub
                results[algo_name] = f"⚙️ [STRATEGIC_LOGIC]: {context}"

        return results

    def process_high_precision(self, chunk: str) -> Dict[str, Any]:
        """
        [HIGH-PRECISION PROTOCOL]: Sovereign translator that converts technical
        structures into executable Python code.
        Upgraded for Global Compatibility (Non-biased).
        """
        # 1. PHASE 1: PREDICTION (استخدام التنبؤ الذي صنعناه)
        schema = self.predict_document_schema(chunk[:1000])

        # 2. PHASE 2: DYNAMIC EXTRACTION (استخراج الهياكل بناءً على النوع)
        # بدلاً من البحث عن الروبوتات فقط، نبحث عن أي معادلات رياضية
        equations = self.extract_kinematic_equations(chunk)

        # 3. PHASE 3: SOVEREIGN PROMPT (هندسة أوامر محايدة)
        # نغير الوظيفة من "مهندس روبوتات" إلى "مهندس برمجيات علمية"
        prompt = (
            f"--- [SOVEREIGN TECHNICAL AUDIT] ---\n"
            f"DETECTED SCHEMA: {schema}\n"
            f"TECHNICAL CONTEXT: {chunk[:2000]}\n\n"
            f"EXTRACTED STRUCTURES: {', '.join(equations) if equations else 'Generic Technical Data'}\n\n"
            f"TASK FOR SCIENTIFIC SOFTWARE ENGINEER:\n"
            f"1. Convert the identified mathematical structures into a high-performance Python function.\n"
            f"2. Use appropriate libraries (NumPy/SciPy) for the detected schema.\n"
            f"3. Ensure mathematical integrity and execution-ready logic.\n"
            f"4. Provide only the Python block and a brief technical justification."
        )

        # 4. EXECUTION WITH FALLBACK (استدعاء المحرك الجديد الآمن)
        # نستخدم الدالة التي تحمينا من خطأ 'None'
        response, meta = self._sovereign_ai_discovery(chunk)

        # 5. FINAL KNOWLEDGE PACKAGE
        return {
            "status": meta.get("engine", "LOCAL_ENGINE"),
            "schema_identified": schema,
            "data_found": equations,
            "python_implementation": response,
            "complexity_level": "HIGH" if len(equations) > 3 else "STANDARD"
        }

    def generate(self, context: str, user_request: str) -> Tuple[List[str], Dict[str, Any]]:
        """
        [THE MASTER GENERATOR]: Routes to either AI Discovery or Local Regex
        based on client availability. Optimized for professional deployment.
        """
        try:
            # 1. المرحلة الأولى: إذا كان محرك الذكاء الاصطناعي متاحاً
            if self.client:
                # تم توحيد الوسائط هنا لتطابق تعريف الدالة الجديد
                return self._sovereign_ai_discovery(context)

            # 2. المرحلة الثانية: المحرك المحلي (Local Regex Engine)
            # يعمل كبديل (Fallback) في حال عدم وجود اتصال أو عميل AI
            technical_insights = []

            # أنماط عامة (Agnostic Patterns) لا تنحاز للروبوتات فقط
            dynamic_patterns = {
                "mathematics": r"(θ|φ|α|β|γ|matrix|transform|calculation|formula)",
                "logic": r"(algorithm|procedure|steps|logic|process|flow)",
                "engineering": r"(sensor|actuator|system|component|control|specification)",
                "data": r"(yields|results|observed|measured|data points)"
            }

            sentences = re.split(r'(?<=[.!?])\s+', context)
            seen_insights = set()

            for sent in sentences:
                sent_clean = sent.strip()
                # التحقق من الأنماط التقنية العامة
                matches = [label for label, pat in dynamic_patterns.items() if re.search(pat, sent_clean, re.IGNORECASE)]

                if matches and sent_clean not in seen_insights and len(sent_clean) > 35:
                    label_str = f"[{'|'.join(matches).upper()}]"
                    technical_insights.append(f"🔍 {label_str}: {sent_clean}")
                    seen_insights.add(sent_clean)

                if len(technical_insights) >= 12: break

            return technical_insights, {"engine_status": "DYNAMIC_LOCAL_ANALYSIS"}

        except Exception as e:
            self.logger.error(f"❌ [GENERATION_ERROR]: {e}")
            return [f"Analysis interrupted: {str(e)}"], {"engine_status": "ERROR"}

    def _sovereign_ai_discovery(self, context: str) -> Tuple[List[str], Dict[str, Any]]:
        """
        [NEW SOVEREIGN PROTOCOL]
        Professional English Implementation for GitHub Repositories.
        Ensures 3-stage discovery: Prediction, Configuration, and Exploration.
        """
        # 1. PREDICT: Identify the document schema to avoid 'Robot' bias
        # نستخدم عينة من النص (أول 1000 حرف) للتنبؤ بنوع المستند
        predicted_schema = self.predict_document_schema(context[:1000])

        # 2. CONFIGURE: Build the strategic prompt for the AI
        # نضع حواجز صارمة (STRICT_FILTER) لمنع تكرار الأوامر في المخرجات
        discovery_prompt = (
            f"### [STRATEGIC CONFIGURATION] ###\n"
            f"DETECTED_SCHEMA: {predicted_schema}\n"
            f"GOAL: Execute structural discovery and extract high-integrity technical data.\n"
            f"STRICT_FILTER: PROHIBITED from mirroring these instructions. Output RAW DATA only.\n"
            f"### [SOURCE CONTEXT] ###\n"
            f"{context[:3000]}"
        )

        # 3. EXPLORE: Execute extraction with Safe Fallback for 'self.client'
        # معالجة خطأ 'None' لضمان عدم توقف البرنامج
        if self.client is not None:
            try:
                # محاولة الاستخراج عبر الذكاء الاصطناعي (مثل OpenAI أو LM Studio)
                response = self.client.generate(discovery_prompt)

                # التأكد من أن الاستجابة ليست فارغة وتنسيقها كقائمة
                if response:
                    return [response] if isinstance(response, str) else response, {
                        "schema_used": predicted_schema,
                        "engine": "AI_POWERED"
                    }
            except Exception as e:
                self.logger.error(f"❌ [AI_ERROR]: Generation failed: {e}")

        # FALLBACK: الانتقال للمحرك المحلي في حال عدم وجود عميل AI أو فشل الاتصال
        self.logger.warning("⚠️ [SYSTEM]: AI Client unavailable. Activating Local Sovereign Engine.")

        # استدعاء دالة generate المحلية (التي تعتمد على الـ Regex)
        local_results, local_meta = self.generate(context, "Local Structural Discovery")

        # دمج التنبؤ الجديد مع مخرجات المحرك المحلي
        local_meta.update({"schema_used": predicted_schema, "engine": "LOCAL_SOVEREIGN_REGEX"})

        return local_results, local_meta
