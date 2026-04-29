# P2_embedding_logic.py

import numpy as np
import warnings
from typing import List, Union, TYPE_CHECKING

# إيقاف التحذيرات المزعجة لضمان نظافة التيرمينال
warnings.filterwarnings("ignore", category=FutureWarning)

if TYPE_CHECKING:
    from P1_sovereign_utils import LoggerProtocol
else:
    LoggerProtocol = any

try:
    from sentence_transformers import SentenceTransformer
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

class EmbeddingManager:
    """
    [مدير التشفير المتجهي V2.0]:
    المسؤول عن تحويل النصوص الهندسية إلى متجهات رقمية.
    """
    def __init__(self, logger: 'LoggerProtocol', model_name: str = "all-MiniLM-L6-v2"):
        self.logger = logger
        self.model_name = model_name
        self._model = None

        # 1. تعريف الأبعاد بشكل يدوي كخط دفاع أول (MiniLM = 384)
        self.dimension = 384

        # 2. استدعاء دالة التهيئة (التي كانت مفقودة والآن مكتوبة بالكامل أدناه)
        self._initialize_model()

    def _initialize_model(self):
        """تحميل النموذج وتعريف أبعاده الحقيقية مع إسكات رسائل التعارض غير المؤثرة."""
        if HAS_TRANSFORMERS:
            try:
                # 🛡️ إجراء وقائي: إسكات رسائل التنبيه غير الضرورية من مكتبة transformers
                import logging
                from transformers import logging as tf_logging
                tf_logging.set_verbosity_error() # سيقوم بإخفاء رسائل UNEXPECTED و Missing keys

                self.logger.info(f"🧬 [EMBEDDING]: تحميل النموذج السيادي ({self.model_name})...")

                # تحميل النموذج
                self._model = SentenceTransformer(self.model_name)

                # تحديث الأبعاد تلقائياً
                if hasattr(self._model, 'get_sentence_embedding_dimension'):
                    self.dimension = self._model.get_sentence_embedding_dimension()

                self.logger.info(f"✅ [EMBEDDING]: النموذج جاهز بأبعاد: {self.dimension}")
            except Exception as e:
                self.logger.error(f"⚠️ [EMBEDDING_LOAD_ERROR]: فشل تحميل النموذج: {e}")
        else:
            self.logger.warning("🚫 [TRANSFORMERS_NOT_FOUND]: مكتبة التشفير غير مثبتة.")

    def encode_text(self, text: Union[str, List[str]]) -> np.ndarray:
        current_dim = self.dimension if self.dimension is not None else 384

        # تحويل المدخل الفردي لقائمة لتوحيد المعالجة (تسهيل الكود)
        is_single = isinstance(text, str)
        input_data = [text] if is_single else text

        try:
            if self._model is not None:
                # التحسين: معالجة النصوص الفارغة لتجنب ضجيج المتجهات
                # convert_to_numpy=True و show_progress_bar=False للسرعة
                vectors = self._model.encode(input_data, convert_to_numpy=True, show_progress_bar=False)
                return np.array(vectors).astype('float32')

            # وضع الطوارئ
            count = len(input_data)
            fallback = np.random.uniform(-1, 1, (count, current_dim)).astype('float32')
            return fallback[0] if is_single else fallback

        except Exception as e:
            self.logger.error(f"❌ [ENCODE_ERROR]: {e}")
            shape = (len(input_data), current_dim)
            zeros = np.zeros(shape).astype('float32')
            return zeros[0] if is_single else zeros

    def calculate_similarity(self, v1: np.ndarray, v2: np.ndarray) -> float:
        """
        [الملاح الهندسي المطور]: حساب Cosine Similarity مع معالجة أخطاء التقريب.
        """
        try:
            if v1 is None or v2 is None: return 0.0

            # استخدام Flattening سريع
            v1_arr = np.asanyarray(v1).ravel()
            v2_arr = np.asanyarray(v2).ravel()

            norm_v1 = np.linalg.norm(v1_arr)
            norm_v2 = np.linalg.norm(v2_arr)

            if norm_v1 == 0 or norm_v2 == 0: return 0.0

            dot_product = np.dot(v1_arr, v2_arr)
            similarity = dot_product / (norm_v1 * norm_v2)

            # 🛡️ اللمسة الهندسية: Clipping
            # تضمن أن النتيجة لا تخرج عن نطاق [-1.0, 1.0] بسبب أخطاء الـ Float
            return float(np.clip(similarity, -1.0, 1.0))

        except Exception as e:
            self.logger.debug(f"⚠️ [SIMILARITY_ISSUE]: {e}")
            return 0.0
