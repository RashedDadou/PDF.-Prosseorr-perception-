# matrix_llm.py

import os
import json
import numpy as np
import asyncio
import concurrent.futures
from typing import Tuple, Optional

from logger import get_logger
from config import SovereignConfig
from calculator import SovereignCalculator
class MatrixLLMRepairer:
    """
    [مصلح المصفوفات بالـ LLM] - متخصص في إصلاح وتحسين مصفوفات التحويل 4x4
    """

    def __init__(self, logger=None, config=None):
        self.logger = logger or get_logger("MatrixLLMRepairer")
        self.config = config or SovereignConfig
        self.calculator = SovereignCalculator(logger=self.logger)

        # التحقق من توفر OpenAI
        try:
            import openai
            self.openai_available = True
        except ImportError:
            self.openai_available = False
            self.logger.warning("⚠️ مكتبة 'openai' غير مثبتة. LLM Repair معطل.")

        self.logger.info("🧠 MatrixLLMRepairer تم تهيئته بنجاح")


    async def repair_matrix(self, snippet: str, page: int) -> Tuple[Optional[np.ndarray], float, bool]:
        """إصلاح مصفوفة باستخدام LLM (Async)"""
        if not getattr(self.config, 'MATRIX_REPAIR_ENABLED', False):
            return None, 0.0, False

        if not self.openai_available:
            self.logger.debug("LLM Repair: OpenAI library not available")
            return None, 0.0, False

        try:
            from openai import AsyncOpenAI

            # دعم API Key من Config أو Environment
            api_key = getattr(self.config, 'OPENAI_API_KEY', None) or os.getenv("OPENAI_API_KEY")
            if not api_key:
                self.logger.warning("⚠️ OPENAI_API_KEY غير معرف. LLM Repair معطل.")
                return None, 0.0, False

            client = AsyncOpenAI(api_key=api_key)

            system_prompt = getattr(
                self.config, 
                'MATRIX_REPAIR_SYSTEM_PROMPT',
                "أنت خبير متخصص في مصفوفات التحويل المتجانسة 4x4 في سياق تصميم السيارات (H-Point & Vehicle Packaging)."
            )

            user_prompt = self._build_user_prompt(snippet)

            response = await client.chat.completions.create(
                model=getattr(self.config, 'MATRIX_REPAIR_MODEL', "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=getattr(self.config, 'LLM_TEMPERATURE', 0.0),
                max_tokens=getattr(self.config, 'LLM_MAX_TOKENS', 1000),
                top_p=getattr(self.config, 'LLM_TOP_P', 0.95),
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content.strip()
            data = json.loads(content)

            matrix_list = data.get("matrix")
            confidence = float(data.get("confidence", 60.0))

            if not self._is_valid_matrix_list(matrix_list):
                self.logger.warning(f"⚠️ LLM Page {page} - Invalid matrix format returned")
                return None, 0.0, False

            matrix = np.array(matrix_list, dtype=float)
            quality = self.calculator.evaluate_matrix_quality(matrix)

            self.logger.info(
                f"🧠 [LLM REPAIR SUCCESS] Page {page} | "
                f"Quality: {quality:.1f} | Confidence: {confidence:.1f}"
            )

            return matrix, quality, True

        except json.JSONDecodeError:
            self.logger.error(f"❌ LLM Page {page} - JSON Parse Error")
            return None, 0.0, False
        except Exception as e:
            self.logger.error(f"❌ LLM Repair فشل على صفحة {page}: {e}")
            return None, 0.0, False
        
    def run_sync(self, snippet: str, page: int) -> Tuple[Optional[np.ndarray], float, bool]:
        """استدعاء متزامن آمن للـ LLM Repair"""
        if not getattr(self.config, 'MATRIX_REPAIR_ENABLED', False):
            return None, 0.0, False

        try:
            # استخدام ThreadPoolExecutor لتجنب مشاكل event loop
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(
                    self._run_async_repair, snippet, page
                )
                return future.result(timeout=40.0)  # Timeout معقول

        except concurrent.futures.TimeoutError:
            self.logger.warning(f"⏰ LLM Repair timeout على صفحة {page} (40 ثانية)")
            return None, 0.0, False
        except Exception as e:
            self.logger.error(f"❌ LLM Repair sync فشل (Page {page}): {e}")
            return None, 0.0, False

    def _run_async_repair(self, snippet: str, page: int) -> Tuple[Optional[np.ndarray], float, bool]:
        """دالة داخلية لتشغيل الـ async"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self.repair_matrix(snippet, page))
            loop.close()
            return result
        except Exception as e:
            self.logger.error(f"خطأ في _run_async_repair: {e}")
            return None, 0.0, False
        
    def _build_user_prompt(self, snippet: str) -> str:
        """بناء Prompt قوي ومتخصص في H-Point"""
        return f"""أنت خبير في مصفوفات التحويل المتجانسة 4x4 (Homogeneous Transformation Matrices) المستخدمة في Vehicle Packaging و H-Point.

النص الخام المستخرج من OCR (قد يحتوي على أخطاء):
{snippet[:2000]}

أعد JSON صالح فقط بالشكل التالي:

{{
  "matrix": [
    [r11, r12, r13, tx],
    [r21, r22, r23, ty],
    [r31, r32, r33, tz],
    [0,   0,   0,   1]
  ],
  "confidence": 85,
  "explanation": "شرح مختصر للتصحيحات التي قمت بها"
}}

ركز على إصلاح الأخطاء الناتجة عن OCR واجعل المصفوفة Homogeneous Transformation صالحة.""" 

    def _is_valid_matrix_list(self, matrix_list) -> bool:
        """التحقق من صحة تنسيق المصفوفة المعادة من LLM"""
        if not isinstance(matrix_list, list) or len(matrix_list) != 4:
            return False
        
        for row in matrix_list:
            if not isinstance(row, list) or len(row) != 4:
                return False
            # التأكد من أن جميع العناصر أرقام
            if not all(isinstance(x, (int, float)) or 
                      (isinstance(x, str) and x.replace('.', '', 1).replace('-', '', 1).isdigit()) 
                      for x in row):
                return False
        return True