#!/usr/bin/env python3

"""
Sovereign Engine - Easy Runner
"""

import sys
import asyncio
from pathlib import Path

# Add project root to path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

print("=" * 70)
print("🚀 Sovereign Engine v2.0 - Advanced PDF Matrix Extractor")
print("=" * 70)


async def main():
    try:
        # Import after path setup
        from sovereign_engine import SovereignEngine

        print("\n🔧 Initializing Sovereign Engine...\n")
        engine = SovereignEngine()

        # Show status
        status = engine.get_status()
        print(f"📊 Engine Status     : {status.get('status', 'UNKNOWN')}")
        print(f"🧠 Cached Pages     : {status.get('cache_size', 0)}")
        print(f"🧬 Embedder         : {'✅ Ready' if status.get('embedder_ready') else '⚠️ Not Ready'}")
        print("-" * 50)

        # Get PDF path
        pdf_path = input("\n📂 Enter PDF file path (or drag & drop): ").strip().strip('"\' ')

        if not pdf_path:
            print("❌ No file path provided.")
            return

        pdf_path = Path(pdf_path).resolve()

        if not pdf_path.exists():
            print(f"❌ File not found: {pdf_path}")
            return

        if pdf_path.suffix.lower() != '.pdf':
            print("❌ The file is not a PDF.")
            return

        print(f"\n⏳ Processing: {pdf_path.name} ...\n")

        # Start processing
        result = await engine.process_pdf(str(pdf_path), domain="Vehicle_Design")

        if result.get("status") == "SUCCESS":
            print("\n" + "="*70)
            print("🎉 PROCESSING COMPLETED SUCCESSFULLY!")
            print("="*70)
            print(f"   📄 File Name          : {result.get('file_name')}")
            print(f"   📑 Total Pages        : {result.get('total_pages')}")
            print(f"   🔢 Extracted Matrices : {result.get('total_matrices')}")
            print(f"   ⏱️  Time Taken        : {result.get('execution_time')} seconds")
            print("="*70)

        else:
            print(f"\n❌ Processing failed: {result.get('error', 'Unknown error')}")

    except KeyboardInterrupt:
        print("\n\n⛔ Operation cancelled by user.")
    except Exception as e:
        print(f"\n🛑 Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())