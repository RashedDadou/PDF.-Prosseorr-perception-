# P3_memory.py

import os
import time
import math
import numpy as np
from datetime import datetime  # <--- هذا هو السطر الناقص
from collections import OrderedDict, defaultdict
from typing import Dict, List, Any, Optional
from P1_sovereign_utils import LoggerProtocol

class PDFpageCacheNetwork:
    """
    [شبكة الوعي الهيكلي V3.0]:
    إدارة متقدمة للذاكرة بنظام الدفعات (Batches) والأرشفة التلقائية.
    """
    def __init__(self, supervisor: Any, batch_size: int = 20, archive_dir: str = "sovereign_knowledge_base"):
        self.supervisor = supervisor
        self.logger = supervisor.logger

        # 1. إدارة الكاش (OrderedDict للحفاظ على ترتيب الصفحات)
        self.cache: OrderedDict[int, Dict[str, Any]] = OrderedDict()

        # 2. [التصحيح الحاسم]: تعريف موحد للدماغ المعرفي كقاموس مرن
        # حذفنا تعريف الـ defaultdict(list) لأنه كان يسبب خطأ النوع
        self.knowledge_graph: Dict[str, Any] = {}

        self.detected_schemas = set()

        # 3. إعدادات الدفعات والأرشفة (تحسين لبيئة 80GB RAM)
        self.batch_size = batch_size
        self.current_batch_pages: List[int] = []
        self.archive_dir = archive_dir
        self.max_cache = 300 # رفعنا السعة لتغطية الـ 224 صفحة بالكامل في الرام

        # 4. إنشاء البنية التحتية للأرشفة
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_archive_path = os.path.join(self.archive_dir, f"session_{self.session_id}")

        if not os.path.exists(self.current_archive_path):
            os.makedirs(self.current_archive_path)
            self.logger.info(f"🛡️ [SECURITY]: Session archive established: {self.current_archive_path}")

    # 1. دالة الإضافة (النسخة المحصنة)
    def add_page(self, page_num: int, content: str, embedding: np.ndarray, metadata: Dict[str, Any]):
        """
        [MEMORY_STORE]: التخزين الذكي مع الحماية من الـ KeyError والانهيار.
        """
        try:
            # صمام أمان للمتجهات: منع تخزين متجه فارغ
            if embedding is None or np.linalg.norm(embedding) < 1e-9:
                raise ValueError(f"Empty embedding for page {page_num}")

            # إدارة سعة الرام (LRU)
            if len(self.cache) >= self.max_cache:
                old_page, _ = self.cache.popitem(last=False)
                # self.logger.debug(f"🧹 [RAM_CLEANUP]: Evicting page {old_page}")

            # التخزين الفعلي
            self.cache[page_num] = {
                "content": content,
                "embedding": embedding,
                "metadata": metadata,
                "timestamp": time.time()
            }

            # [التصحيح الحاسم]: تهيئة التصنيف إذا لم يكن موجوداً
            category = metadata.get("category", "General Technical")
            if category not in self.knowledge_graph:
                self.knowledge_graph[category] = [] # إنشاء القائمة فوراً

            self.knowledge_graph[category].append(page_num)
            self.current_batch_pages.append(page_num)

            # الأرشفة التلقائية للدفعات
            if len(self.current_batch_pages) >= self.batch_size:
                self._archive_current_batch()

            self.logger.info(f"🧠 [MEMORY_UPDATE]: Page {page_num} stored under {category}.")

        except Exception as e:
            # الآن سنعرف السبب الحقيقي للفشل (هل هو KeyError أم شيء آخر؟)
            self.logger.error(f"❌ [MEMORY_ERROR]: Failed to store page {page_num}. Reason: {str(e)}")

    # 2. دالة الاسترجاع (The Getter) - هنا نستخدم Optional
    def get_page(self, page_num: int) -> Optional[Dict[str, Any]]:
        """
        [MEMORY_RETRIEVAL]: استرجاع آمن للبيانات.
        تعيد القاموس إذا وجدت الصفحة، أو None إذا كانت غير موجودة.
        """
        # استخدام .get() مع الـ OrderedDict هو الطريقة الأسلم برمجياً
        page_data = self.cache.get(page_num)

        if page_data is None:
            self.logger.warning(f"⚠️ [MEMORY_MISS]: Page {page_num} not found in active RAM.")

        return page_data

    def add_perceptual_node(self, node: dict) -> bool:
        """
        [إصلاح خطأ النوع]: ضمان إسناد القاموس المعرفي بشكل سليم.
        """
        try:
            node_id = str(node.get('id', ''))
            if not node_id:
                return False

            # التأكد من استخراج البيانات بشكل منفصل لتجنب خلط الأنواع
            content = str(node.get('content', ''))
            metadata = dict(node.get('metadata', {}))
            # التأكد من أن التضمين مصفوفة أو قائمة وليس None
            embedding = node.get('embedding')

            # الإسناد الصحيح الذي يقبله Pylance
            self.knowledge_graph[node_id] = {
                "content": content,
                "metadata": metadata,
                "embedding": embedding,
                "links": [] # قائمة فارغة للروابط القادمة من الـ Linker
            }
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f"❌ [GRAPH_TYPE_ERROR]: {e}")
            return False

    def _archive_current_batch(self):
        """
        [الأرشفة السيادية]: تجميع الدفعة وحفظها مع الحفاظ على "المتجهات السيمانتيكية"
        لضمان إمكانية استعادة البحث دون إعادة المعالجة.
        """
        import json
        import numpy as np

        if not self.current_batch_pages:
            return

        batch_id = f"batch_{self.current_batch_pages[0]}_to_{self.current_batch_pages[-1]}"
        batch_path = os.path.join(self.archive_dir, batch_id)

        try:
            if not os.path.exists(batch_path):
                os.makedirs(batch_path)

            # 1. حفظ خريطة المعرفة (Knowledge Mapping)
            batch_graph = {cat: [p for p in p_list if p in self.current_batch_pages]
                           for cat, p_list in self.knowledge_graph.items()
                           if any(p in self.current_batch_pages for p in p_list)}

            with open(os.path.join(batch_path, "knowledge_map.json"), "w", encoding="utf-8") as f:
                json.dump(batch_graph, f, ensure_ascii=False, indent=4)

            # 2. حفظ المحتوى النصي والميتا-داتا
            batch_data = {
                p: {
                    "content": self.cache[p]["content"],
                    "metadata": self.cache[p]["metadata"]
                } for p in self.current_batch_pages if p in self.cache
            }
            with open(os.path.join(batch_path, "content_dump.json"), "w", encoding="utf-8") as f:
                json.dump(batch_data, f, ensure_ascii=False, indent=4)

            # 3. [تطوير سيادي]: حفظ المتجهات بصيغة مضغوطة .npz
            # هذا هو "مفتاح التوافق" مع محرك البحث لضمان سرعة الاستعادة
            vectors = {str(p): self.cache[p]["embedding"] for p in self.current_batch_pages if p in self.cache}
            if vectors:
                np.savez_compressed(os.path.join(batch_path, "embeddings.npz"), **vectors)

            self.logger.info(f"💾 [ARCHIVE_SUCCESS]: Batch {batch_id} secured with semantic embeddings.")

            # 4. تصفير الدفعة (Reset) للاستعداد للـ 20 صفحة القادمة
            self.current_batch_pages = []

        except Exception as e:
            self.logger.error(f"❌ [ARCHIVE_ERROR]: Failed to secure batch {batch_id}: {str(e)}")

    def finalize_network(self) -> Dict[str, Any]:
        """
        [THE SOVEREIGN LINKER]:
        تحويل العقد المعزولة إلى شبكة معرفية مترابطة لرفع معامل الاستقرار.
        """
        self.logger.info("🔗 [LINKER]: بدء عملية الربط السيادي لـ 224 عقدة...")

        # 1. استخراج جميع المتجهات (Embeddings)
        node_ids = list(self.knowledge_graph.keys())
        embeddings = np.array([self.knowledge_graph[nid]['embedding'] for nid in node_ids])

        # 2. حساب مصفوفة التشابه لرفع معامل الاستقرار من 0.00%
        # نستخدم الدالة المسرعة التي تعتمد على الـ 80GB RAM لديك
        from P2_embedding_logic import EmbeddingManager
        manager = EmbeddingManager(logger=self.logger)

        connections_count = 0
        for i, node_id in enumerate(node_ids):
            # مقارنة العقدة الحالية بكل العقد الأخرى
            similarities = manager.calculate_perceptual_similarity(embeddings[i], embeddings)

            # 3. بناء الروابط (نربط العقد التي تتجاوز نسبة تشابه 85%)
            for j, score in enumerate(similarities):
                if i != j and score > 0.85:
                    self.knowledge_graph[node_id]['links'].append(node_ids[j])
                    connections_count += 1

        # 4. تحديث حالة الشبكة للتقرير الختامي
        stability = (connections_count / (len(node_ids) * 2)) * 100
        return {
            "network_status": "SEALED",
            "total_knowledge_nodes": len(node_ids),
            "structural_stability": f"{min(stability, 100.0):.2f}%",
            "discovered_schemas": self.detected_schemas
        }
