# __init__.py

"""
Sovereign Engine - Clean Architecture v2.0
Core PDF Matrix Extraction System for Vehicle Design & H-Point Documents
"""

__version__ = "2.0.0"
__author__ = "Sovereign Project"
__description__ = "Advanced PDF processing engine specialized in extracting homogeneous transformation matrices"

from sovereign_engine import SovereignEngine

# يمكنك إضافة exports أخرى مهمة في المستقبل
from .config import SovereignConfig
# from .matrix_extractor import MatrixExtractor  # إذا أردت

__all__ = [
    "SovereignEngine",
    "SovereignConfig",
]