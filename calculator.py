# calculator.py

import re
import numpy as np
from typing import List, Dict, Any, Optional

from logger import get_logger
from config import SovereignConfig


class SovereignCalculator:
    """
    [المحرك الحسابي السيادي] - متخصص في تقييم المصفوفات والحركيات
    """

    def __init__(self, logger=None):
        self.logger = logger or get_logger("Calculator")
        self.config = SovereignConfig
        self.logger.info("🧮 SovereignCalculator تم تهيئته بنجاح")

    # ====================== تقييم المصفوفات ======================

    def is_valid_kinematic_matrix(self, text: str, atol: float = 1e-3) -> bool:
        """فحص ما إذا كان النص يحتوي على مصفوفة تحويل حركية 4x4 صالحة"""
        if not text or len(text.strip()) < 30:
            return False

        try:
            numbers = [float(x) for x in re.findall(
                r"[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?", text
            )]
            
            if len(numbers) < 16:
                return False

            for i in range(len(numbers) - 15):
                sample = numbers[i:i+16]
                matrix = np.array(sample).reshape(4, 4)

                if self._is_homogeneous_transformation(matrix, atol=atol):
                    return True
            return False

        except Exception as e:
            self.logger.debug(f"خطأ في is_valid_kinematic_matrix: {e}")
            return False

    def _is_homogeneous_transformation(self, matrix: np.ndarray, atol: float = 1e-3) -> bool:
            """التحقق من شروط مصفوفة Homogeneous Transformation - نسخة متسامحة (H-Point Optimized)"""
            if matrix.shape != (4, 4):
                return False

            # 1. الصف الأخير [0, 0, 0, 1] → متسامح مع ضوضاء OCR
            last_row = matrix[3, :]
            if not np.allclose(last_row, [0, 0, 0, 1], atol=0.15):
                # فحص بديل: القيم قريبة من الصفر والرابعة قريبة من 1
                if abs(last_row[3] - 1.0) > 0.25 or np.abs(last_row[:3]).max() > 0.3:
                    return False

            # 2. الجزء الدوراني (Rotation)
            rot = matrix[:3, :3]
            try:
                det = np.linalg.det(rot)
                # قبول Reflection أيضاً (مهم في بعض التحويلات)
                if not (abs(det - 1.0) < 0.22 or abs(det + 1.0) < 0.25):
                    return False
            except:
                return False

            # 3. Orthogonality (متسامح)
            ortho_error = np.abs(rot.T @ rot - np.eye(3)).mean()
            if ortho_error > 0.18:   # زيادة التسامح
                return False

            return True

    def evaluate_matrix_quality(self, matrix: np.ndarray) -> float:
            """تقييم جودة مصفوفة 4x4 - نسخة محسنة ومتوافقة مع H-Point"""
            if not isinstance(matrix, np.ndarray) or matrix.shape != (4, 4):
                return 0.0

            score = 0.0

            # 1. Homogeneous Check (أهم شيء)
            last_row = matrix[3, :]
            if abs(last_row[3] - 1.0) < 0.18 and np.abs(last_row[:3]).max() < 0.25:
                score += 45
            elif abs(last_row[3] - 1.0) < 0.35:
                score += 28

            # 2. Rotation Elements
            rot = matrix[:3, :3]
            if np.any(np.abs(rot) > 1e-4):
                score += 25

            # 3. Determinant
            try:
                det = np.linalg.det(rot)
                if abs(det - 1.0) < 0.20:
                    score += 22
                elif abs(det + 1.0) < 0.28:
                    score += 14
            except:
                pass

            # 4. Translation (مهم جداً في Vehicle Packaging)
            translation = np.abs(matrix[:3, 3])
            trans_mag = np.max(translation)
            if trans_mag > 0.01:
                score += 12
            if trans_mag < 1500:        # قيم منطقية للسيارات (mm)
                score += 8

            # 5. Orthogonality
            try:
                ortho_error = np.abs(rot.T @ rot - np.eye(3)).mean()
                if ortho_error < 0.08:
                    score += 12
                elif ortho_error < 0.15:
                    score += 7
            except:
                pass

            # 6. Structure Bonus (Small + Large values)
            if np.any((np.abs(matrix) > 0.001) & (np.abs(matrix) < 0.4)) and np.any(np.abs(matrix) > 0.6):
                score += 10

            return round(min(max(score, 0.0), 100.0), 1)
    
    # ====================== الحركيات ======================

    def calculate_forward_kinematics(self, dh_params: List[Dict[str, float]]) -> np.ndarray:
        """حساب Forward Kinematics باستخدام Denavit-Hartenberg Parameters"""
        try:
            T = np.eye(4)
            for params in dh_params:
                theta = np.radians(params.get('theta', 0))
                d = params.get('d', 0)
                a = params.get('a', 0)
                alpha = np.radians(params.get('alpha', 0))

                T_joint = np.array([
                    [np.cos(theta), -np.sin(theta)*np.cos(alpha),  np.sin(theta)*np.sin(alpha), a*np.cos(theta)],
                    [np.sin(theta),  np.cos(theta)*np.cos(alpha), -np.cos(theta)*np.sin(alpha), a*np.sin(theta)],
                    [0,              np.sin(alpha),                np.cos(alpha),               d],
                    [0,              0,                            0,                           1]
                ])
                T = T @ T_joint

            return T
        except Exception as e:
            self.logger.error(f"Forward Kinematics Error: {e}")
            return np.eye(4)

    # ====================== العتبات الديناميكية ======================

    def calculate_dynamic_threshold(self, text: str, content_type: str, candidates_count: int) -> float:
            """حساب عتبة قبول ديناميكية - محسنة لـ H-Point"""
            if not text or len(text) < 50:
                return 42.0

            base = 38.0
            lower = text.lower()

            # طول النص
            text_len = len(text)
            if text_len > 1600:
                base += 14
            elif text_len > 900:
                base += 9
            elif text_len > 500:
                base += 5

            # نوع المحتوى (مهم جداً)
            if content_type in ["HPOINT_TECHNICAL", "VEHICLE_DESIGN"]:
                base += 18
            elif content_type == "MATRIX_TECHNICAL":
                base += 14
            elif content_type == "NUMERIC_HEAVY":
                base += 11

            # كلمات مفتاحية
            hpoint_keywords = ["h-point", "hip point", "sg rp", "sgrp", "manikin", "eyellipse", "j826", "packaging"]
            keyword_count = sum(1 for kw in hpoint_keywords if kw in lower)
            base += keyword_count * 9

            # عدد المرشحين
            if candidates_count >= 8:
                base += 8
            elif candidates_count >= 4:
                base += 5
            elif candidates_count >= 1:
                base += 2

            # Tags مباشرة
            if "[MATRIX" in text or "[TABLE" in text:
                base -= 10   # تخفيض قوي لو فيه tags

            return round(max(22.0, min(base, 68.0)), 1)
    
    # ====================== دوال مساعدة إضافية ======================

    def compare_matrices(self, mat1: np.ndarray, mat2: np.ndarray, atol: float = 1e-4) -> float:
        """مقارنة مصفوفتين وإرجاع درجة التشابه"""
        if not (isinstance(mat1, np.ndarray) and isinstance(mat2, np.ndarray)):
            return 0.0
        try:
            diff = np.abs(mat1 - mat2)
            return float(100 - np.mean(diff) * 10)  # درجة بسيطة
        except:
            return 0.0