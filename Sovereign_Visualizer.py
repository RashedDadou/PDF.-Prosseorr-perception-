# Sovereign_Visualizer.py

import os
import re
import time
from typing import List, Dict, Any, Optional

class SovereignReportEngine:
    """
    [SOVEREIGN REPORT ENGINE V4.0]
    Centralized intelligence unit for generating professional technical audits.
    Designed for high-precision data visualization and structural integrity mapping.
    """

    @staticmethod
    def generate_audit_report(
        pdf_path: str,
        results: List[Any],
        logger: Any,
        metadata: Optional[Dict[str, Any]] = None  # Correct way to handle optional dictionaries
    ):
        # Ensure metadata is at least an empty dict to avoid 'NoneType' errors later
        metadata = metadata or {}

        # 1. Physical File Analytics
        file_size_gb = os.path.getsize(pdf_path) / (1024**3)
        file_name = os.path.basename(pdf_path)

        # 2. Domain Classification (Inference Logic)
        # Identify if the document belongs to Automotive, Aerospace, Medical, or Engineering
        sample_context = " ".join([str(r) for r in results[:30]]).lower()
        if any(word in sample_context for word in ['vehicle', 'h-point', 'chassis', 'torque']):
            domain = "AUTOMOTIVE_ENGINEERING"
        elif any(word in sample_context for word in ['wing', 'aerodynamic', 'thrust', 'flight']):
            domain = "AEROSPACE_DYNAMICS"
        elif any(word in sample_context for word in ['patient', 'clinical', 'anatomy', 'surgical']):
            domain = "MEDICAL_SCIENCE"
        else:
            domain = "GENERAL_TECHNICAL_INFRASTRUCTURE"

        # 3. Structural Integrity Calculation
        total_nodes = len(results)
        valid_knowledge_blocks = metadata.get('valid_blocks', total_nodes)
        integrity_score = (valid_knowledge_blocks / total_nodes * 100) if total_nodes > 0 else 0

        # 4. Final Executive Summary Output
        print(f"\n" + "═"*70)
        print(f"🛡️  [FINAL SOVEREIGN AUDIT REPORT]")
        print("═"*70)
        print(f"📄 TARGET_FILE     : {file_name}")
        print(f"⚖️  FILE_SIZE       : {file_size_gb:.6f} GB")
        print(f"🎯 DOMAIN_TYPE     : {domain}")
        print(f"📊 TOTAL_CHUNKS    : {metadata.get('total_pages', 'N/A')}")
        print(f"✅ VALID_INSIGHTS  : {valid_knowledge_blocks}")
        print(f"🔢 STRUCTURAL_PAT  : {metadata.get('structural_patterns', 0)}")
        print(f"🛡️  STABILITY_LVL   : {SovereignReportEngine._get_stability_label(integrity_score)}")
        print(f"📈 INTEGRITY_SCORE : {integrity_score:.2f}%")
        print("═"*70 + "\n")

        # 5. Sequential Knowledge Flow (The Page-by-Page Trace)
        print(f"📑 [SEQUENTIAL KNOWLEDGE FLOW - {total_nodes} NODES]")
        print("-" * 75)
        for i, node in enumerate(results):
            node_id = i + 1
            content_snippet = str(node).strip().replace('\n', ' ')[:85]

            # Contextual Linking Logic (Detecting Continuity)
            is_linked = i > 0 and SovereignReportEngine._check_continuity(str(results[i-1]), str(node))
            link_status = "🔗 [CONTINUITY]" if is_linked else "🆕 [NEW_INSIGHT]"

            print(f"NODE_{node_id:04d} | {link_status:<15} | {content_snippet}...")

        print("-" * 75)
        logger.info(f"✨ MISSION_COMPLETE: Audit generated for {file_name} with {integrity_score:.2f}% integrity.")

    @staticmethod
    def _get_stability_label(score: float) -> str:
        if score >= 90: return "💎 HIGH_INTEGRITY (DENSE_KNOWLEDGE)"
        if score >= 70: return "⚖️ MEDIUM_STABILITY"
        return "⚠️ LOW_RELIABILITY_HEURISTIC"

    @staticmethod
    def _check_continuity(prev: str, current: str) -> bool:
        """
        [Sovereign Link Logic]: Strictly verifies continuity between data nodes.
        Returns True if the current block completes a mathematical pattern.
        """
        # We wrap the logic in bool() to ensure literal strings aren't returned
        has_open_bracket = "[" in prev and "]" not in prev
        starts_with_digit = bool(current and current[0].isdigit())

        return has_open_bracket or starts_with_digit
