# embedding_logic.py

import numpy as np
import warnings
from typing import List, Union, Optional, Any, Dict

warnings.filterwarnings("ignore", category=FutureWarning)

# محاولة استيراد بأمان
try:
    from sentence_transformers import SentenceTransformer
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False
    SentenceTransformer = None


from logger import get_logger
from config import SovereignConfig


class SovereignEmbedder:
    """
    [مدير التشفير السيادي] - إدارة الـ Embeddings بطريقة آمنة ومرنة
    """

    def __init__(self, logger=None, model_name: Optional[str] = None):
        self.logger = logger or get_logger("Embedder")
        self.config = SovereignConfig
        
        self.model_name = model_name or getattr(self.config, 'EMBEDDING_MODEL', "all-MiniLM-L6-v2")
        self._model = None
        self.dimension: int = 384
        self._initialize_model()

    def _initialize_model(self):
        """تهيئة النموذج مع حماية كاملة"""
        if not HAS_TRANSFORMERS:
            self.logger.warning("⚠️ مكتبة 'sentence-transformers' غير مثبتة.")
            self.logger.info("   قم بتثبيتها باستخدام: pip install sentence-transformers")
            self._model = None
            self.dimension = 384
            return

        try:
            self.logger.info(f"🧬 [EMBEDDER] جاري تحميل النموذج: {self.model_name}")
            
            self._model = SentenceTransformer(self.model_name)
            
            # الحصول على الأبعاد بأمان
            if hasattr(self._model, 'get_sentence_embedding_dimension'):
                self.dimension = self._model.get_sentence_embedding_dimension() or 384
            else:
                # طريقة احتياطية آمنة
                test_embedding = self._model.encode(["test sentence"])
                self.dimension = test_embedding.shape[-1]
                
            self.logger.info(f"✅ [EMBEDDER] تم التحميل بنجاح | النموذج: {self.model_name} | أبعاد: {self.dimension}")
            
        except Exception as e:
            self.logger.error(f"❌ فشل تحميل النموذج '{self.model_name}': {e}")
            self._model = None
            self.dimension = 384
            self.logger.warning("⚠️ سيتم استخدام Fallback عشوائي في encode()")

    def _safe_encode(self, texts: List[str]) -> np.ndarray:
        """طبقة حماية إضافية لتجنب استدعاء None"""
        if not self._model:
            self.logger.debug("⚠️ _model غير موجود → Fallback")
            dim = getattr(self, 'dimension', 384)
            fallback = np.random.randn(len(texts), dim).astype('float32')
            fallback = fallback / np.linalg.norm(fallback, axis=1, keepdims=True)
            return fallback

        try:
            return self._model.encode(
                texts,
                convert_to_numpy=True,
                show_progress_bar=False,
                normalize_embeddings=True,
                batch_size=32
            )
        except Exception as e:
            self.logger.error(f"❌ خطأ في _safe_encode: {e}")
            dim = getattr(self, 'dimension', 384)
            return np.zeros((len(texts), dim), dtype='float32')
        
    def encode(self, input_data: Union[str, List[str]]) -> np.ndarray:
        """تحويل نص أو قائمة نصوص إلى متجه/متجهات"""
        is_single = isinstance(input_data, str)
        texts = [input_data] if is_single else input_data

        if not texts or len(texts) == 0:
            dim = getattr(self, 'dimension', 384)
            empty = np.zeros(dim, dtype='float32')
            return empty if is_single else np.zeros((0, dim), dtype='float32')

        # Fallback إذا لم يكن النموذج محمل
        if not self._model:
            self.logger.debug("⚠️ Embedder غير متوفر → استخدام Fallback")
            dim = getattr(self, 'dimension', 384)
            fallback = np.random.randn(len(texts), dim).astype('float32')
            fallback = fallback / np.linalg.norm(fallback, axis=1, keepdims=True)
            return fallback[0] if is_single else fallback

        try:
            vectors = self._model.encode(
                texts,
                convert_to_numpy=True,
                show_progress_bar=False,
                normalize_embeddings=True,
                batch_size=32
            )
            vectors = np.asarray(vectors, dtype='float32')
            return vectors[0] if is_single else vectors

        except Exception as e:
            self.logger.error(f"❌ خطأ في encode(): {e}")
            dim = getattr(self, 'dimension', 384)
            zeros = np.zeros((len(texts), dim), dtype='float32')
            return zeros[0] if is_single else zeros
        
    def calculate_similarity(self, v1: np.ndarray, v2: np.ndarray) -> float:
        """حساب Cosine Similarity بأمان"""
        try:
            v1 = np.asarray(v1).ravel()
            v2 = np.asarray(v2).ravel()
            
            norm_v1 = np.linalg.norm(v1)
            norm_v2 = np.linalg.norm(v2)
            
            if norm_v1 == 0 or norm_v2 == 0:
                return 0.0
                
            return float(np.dot(v1, v2) / (norm_v1 * norm_v2))
        except Exception as e:
            self.logger.debug(f"خطأ في حساب التشابه: {e}")
            return 0.0

    def is_ready(self) -> bool:
        """التحقق مما إذا كان النموذج جاهزاً"""
        return self._model is not None

    def get_model_info(self) -> Dict[str, Any]:
        """معلومات عن حالة النموذج"""
        return {
            "model_name": self.model_name,
            "dimension": self.dimension,
            "is_ready": self.is_ready(),
            "has_transformers": HAS_TRANSFORMERS
        }