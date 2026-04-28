# P2_embedding_logic.py المصحح بالكامل

import numpy as np
from typing import Union, List


class EmbeddingManager:
    """
    [مدير التشفير المتجهي V4.0 - النسخة السيادية الموحدة]:
    تم توحيد جميع المسميات إلى self.model لضمان الرنين الإدراكي الكامل.
    """
    def __init__(self, logger=None, model_name='all-MiniLM-L6-v2'):
        self.logger = logger
        self.model_name = model_name
        self.dimension = 384
        self.model = None

        try:
            from sentence_transformers import SentenceTransformer
            if self.logger:
                self.logger.info(f"🧬 [EMBEDDING]: تحميل النموذج السيادي ({self.model_name})...")

            # توحيد الاسم هنا هو المفتاح
            self.model = SentenceTransformer(self.model_name)

            if self.logger:
                self.logger.info("✅ [EMBEDDING]: النموذج جاهز وموحد في الذاكرة.")
        except Exception as e:
            if self.logger:
                self.logger.error(f"❌ [EMBEDDING_ERROR]: فشل تحميل النموذج: {str(e)}")

    def get_perceptual_embedding(self, text: str, perceptual_intensity: float = 1.0) -> np.ndarray:
        """توليد متجه رقمي مشبع بالرنين الإدراكي"""
        if self.model is None:
            return np.random.uniform(-0.1, 0.1, self.dimension).astype('float32')

        # استخدام self.model الموحد
        base_vector = self.model.encode(text, convert_to_numpy=True)
        aware_vector = base_vector * perceptual_intensity
        return aware_vector.astype('float32')

    def get_aware_embedding(self, text: str, perceptual_code: dict) -> np.ndarray:
        """حقن الوعي الإدراكي لرفع معامل الاستقرار من 0.00%"""
        if self.model is None:
            return np.zeros(self.dimension, dtype='float32')

        base_vector = self.model.encode(text)
        intensity = perceptual_code.get("intensity", 1.0) if perceptual_code else 1.0

        # معادلة تضخيم الوعي لتمييز البيانات التقنية
        aware_vector = base_vector * (1.0 + (float(intensity) * 0.05))
        return aware_vector.astype('float32')

    def get_embedding(self, text: str):
        # 1. فحص المحتوى أولاً
        if not text or str(text).strip() == "":
            return np.zeros(self.dimension, dtype='float32')

        # 2. حماية Pylance: التحقق من أن النموذج ليس None وتخزينه في متغير محلي
        model_instance = self.model

        if model_instance is None:
            if self.logger:
                self.logger.error("🚨 [CRITICAL]: النموذج السيادي غير محمل في الذاكرة!")
            # العودة بمتجه عشوائي صغير لمنع الـ Division by Zero في الـ Linker
            return np.random.uniform(-0.01, 0.01, self.dimension).astype('float32')

        try:
            # الآن Pylance متأكد أن model_instance ليس None
            return model_instance.encode(
                text,
                convert_to_numpy=True,
                show_progress_bar=False
            ).astype('float32')

        except Exception as e:
            if self.logger:
                self.logger.error(f"❌ [ENCODE_ERROR]: {str(e)}")
            return np.zeros(self.dimension, dtype='float32')

    def encode_text(self, text: Union[str, List[str]], intensity: float = 1.0) -> np.ndarray:
        try:
            if not text:
                return np.zeros(self.dimension).astype('float32')

            input_data = [text] if isinstance(text, str) else text

            # تصحيح: استخدام self.model بدلاً من self._model
            if self.model:
                vectors = self.model.encode(input_data, convert_to_numpy=True).astype('float32')
                if intensity > 1.0:
                    vectors = vectors * intensity
                return vectors[0] if isinstance(text, str) else vectors

            return np.random.uniform(-0.1, 0.1, self.dimension).astype('float32')
        except Exception as e:
            if self.logger:
                self.logger.error(f"❌ [ENCODE_ERROR]: {e}") # تعديل لضمان عدم ظهور خطأ Attribute
            return np.zeros(self.dimension).astype('float32')

    def calculate_perceptual_similarity(self, query_v: np.ndarray, matrix_v: np.ndarray, intensity_boost: float = 1.0) -> np.ndarray:
        try:
            # 1. تهيئة الأبعاد
            if query_v.ndim == 1:
                query_v = query_v.reshape(1, -1)

            # 2. فحص العقد الميتة (Dead Nodes Check)
            # إذا كان المتجه كله أصفار، نرجعه كـ 1e-10 بدلاً من صفر مطلق
            query_v = np.where(np.all(query_v == 0, axis=1, keepdims=True), 1e-10, query_v)

            # 3. حساب المعايير مع حماية مضاعفة
            norm_q = np.linalg.norm(query_v, axis=1, keepdims=True)
            norm_m = np.linalg.norm(matrix_v, axis=1, keepdims=True).T

            # صمام الأمان: منع الضرب في صفر
            denominator = np.dot(norm_q, norm_m)
            denominator = np.where(denominator == 0, 1e-10, denominator)

            dot_product = np.dot(query_v, matrix_v.T)
            similarity = (dot_product / denominator) * intensity_boost

            return np.nan_to_num(similarity) # تحويل أي NaN إلى صفر آمن
        except Exception as e:
            return np.zeros((query_v.shape[0], matrix_v.shape[0]))
