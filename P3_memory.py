# P3_memory.py

import os
import time
import json
import numpy as np
from collections import OrderedDict, defaultdict
from typing import Dict, List, Any, Optional
from P1_sovereign_utils import LoggerProtocol

class PDFpageCacheNetwork:
    """
    [شبكة الوعي الهيكلي V3.0]:
    إدارة متقدمة للذاكرة بنظام الدفعات (Batches) والأرشفة التلقائية.
    """
    def __init__(self, supervisor: Any, batch_size: int = 20, archive_dir: str = "sovereign_knowledge_base"):
        # 1. المراجع الأساسية (تعريف السوبر فايزر واللوجر)
        self.supervisor = supervisor
        self.logger: LoggerProtocol = supervisor.logger
        self.current_time = time.strftime("%H:%M:%S")

        # 2. مخازن البيانات الأساسية (Core Storage)
        self.cache: OrderedDict[int, Dict[str, Any]] = OrderedDict()
        self.network_cache: List[Any] = []  # حل مشكلة [Attribute Access Issue]
        self.knowledge_graph: defaultdict[str, List[int]] = defaultdict(list)

        # 3. إعدادات الإدارة والأرشفة
        self.batch_size = batch_size
        self.current_batch_pages: List[int] = []
        self.archive_dir = archive_dir
        self.max_cache = 250  # سعة الرام لملفات الـ PDF الضخمة

        # 4. إنشاء البنية التحتية للأرشفة
        if not os.path.exists(self.archive_dir):
            os.makedirs(self.archive_dir)
            self.logger.info(f"📂 تم إنشاء مجلد الأرشفة السيادي: {self.archive_dir}")

    def add_page(self, page_num: int, content: str, embedding: np.ndarray, metadata: Dict[str, Any]):
        """
        [إضافة صفحة للذاكرة]: تخزين ذكي مع تفعيل نظام الدفعات كل 20 صفحة.
        """
        try:
            # 1. إدارة سعة الرام (LRU)
            if len(self.cache) >= self.max_cache:
                old_page, _ = self.cache.popitem(last=False)
                self.logger.debug(f"🧹 [RAM_CLEANUP]: إخراج الصفحة {old_page} من الرام.")

            # 2. التخزين في الذاكرة الحية (RAM)
            self.cache[page_num] = {
                "content": content,
                "vector": embedding,
                "metadata": metadata,
                "timestamp": time.time()
            }

            # 3. تحديث خريطة المعرفة الحالية
            category = metadata.get("category", "General")
            self.knowledge_graph[category].append(page_num)
            self.current_batch_pages.append(page_num)

            # 4. تفعيل "بروتوكول الدفعة" عند الوصول لـ 20 صفحة
            if len(self.current_batch_pages) >= self.batch_size:
                self._archive_current_batch()

            # أضف هذا السطر داخل دالة add_page للتأكد من وصول التصنيف
            self.logger.debug(f"🔍 [DEBUG]: الصفحة {page_num} تتبع تصنيف: {category}")

        except Exception as e:
            self.logger.error(f"❌ [MEMORY_ERROR]: فشل إضافة الصفحة {page_num}: {str(e)}")

    def add_node(self, label: str, value: Any, type: str = "GENERIC"):
        """
        [توسيع الذاكرة السيادية]: إضافة عقدة معرفية جديدة للشبكة الاستدلالية.
        """
        node_data = {
            "label": label,
            "value": value,
            "type": type,
            "timestamp": getattr(self, 'current_time', 'N/A')
        }
        # إضافة العقدة لذاكرة الكاش الحالية
        if hasattr(self, 'network_cache'):
            self.network_cache.append(node_data)
            self.supervisor.logger.debug(f"🌐 [NETWORK]: تم حقن العقدة {label} بنجاح.")

    def reset_for_new_document(self):
        """
        [تطهير الذاكرة السيادية]: تنظيف الذاكرة بالكامل لتحضيرها لملف PDF جديد.
        """
        try:
            # تنظيف الذاكرة المخبئية - الاسم البرمجي في كلاسك هو cache
            if self.cache is not None:
                self.cache.clear()

            # تنظيف خريطة المعرفة - الاسم البرمجي في كلاسك هو knowledge_graph
            if self.knowledge_graph is not None:
                self.knowledge_graph.clear()

            # تصفير قائمة الدفعات الحالية
            if self.current_batch_pages is not None:
                self.current_batch_pages = []

            self.logger.info("🧹 [MEMORY RESET]: تم تفريغ الذاكرة الشبكية بنجاح للملف الجديد.")

        except Exception as e:
            self.logger.error(f"🚨 [RESET_ERROR]: فشل في تطهير الذاكرة: {str(e)}")

    def _archive_current_batch(self):
        """
        [الأرشفة السيادية]: تجميع الدفعة الحالية وحفظها في مجلد مستقل.
        """
        batch_id = f"batch_{self.current_batch_pages[0]}_to_{self.current_batch_pages[-1]}"
        batch_path = os.path.join(self.archive_dir, batch_id)

        try:
            if not os.path.exists(batch_path):
                os.makedirs(batch_path)

            # حفظ خريطة المعرفة الخاصة بهذه الدفعة فقط
            batch_graph = {cat: [p for p in p_list if p in self.current_batch_pages]
                           for cat, p_list in self.knowledge_graph.items() if any(p in self.current_batch_pages for p in p_list)}

            with open(os.path.join(batch_path, "knowledge_map.json"), "w", encoding="utf-8") as f:
                json.dump(batch_graph, f, ensure_ascii=False, indent=4)

            # حفظ البيانات (بدون المتجهات لتوفير المساحة أو يمكن حفظها بصيغة .npy)
            batch_data = {p: self.cache[p]["content"] for p in self.current_batch_pages if p in self.cache}
            with open(os.path.join(batch_path, "content_dump.json"), "w", encoding="utf-8") as f:
                json.dump(batch_data, f, ensure_ascii=False, indent=4)

            self.logger.info(f"💾 [ARCHIVE_SUCCESS]: تم تأمين الدفعة {batch_id} في القرص الصلب.")
            self.current_batch_pages = [] # تصفير قائمة الدفعة الحالية

        except Exception as e:
            self.logger.error(f"❌ [ARCHIVE_ERROR]: فشل أرشفة الدفعة {batch_id}: {str(e)}")

    def finalize_network(self):
        """
        [الدمج الاستدلالي]: جمع كل الخرائط الفرعية في شبكة موحدة عند نهاية المهمة.
        """
        try:
            self.logger.info("🔗 [FINAL_LINKING]: جارٍ دمج الشبكات الاستدلالية الفرعية...")

            # تأمين آخر دفعة من الصفحات إذا كانت القائمة غير فارغة
            if self.current_batch_pages and len(self.current_batch_pages) > 0:
                self._archive_current_batch()

            # طباعة التقرير النهائي بناءً على knowledge_graph المعرف في الـ __init__
            total_categories = len(self.knowledge_graph) if self.knowledge_graph is not None else 0
            self.logger.info(f"🏆 [NETWORK_COMPLETE]: الشبكة الاستدلالية جاهزة. إجمالي التصنيفات: {total_categories}")

        except Exception as e:
            self.logger.error(f"🚨 [FINALIZE_ERROR]: فشل في إتمام الدمج النهائي: {str(e)}")
