#!/usr/bin/env python3
"""
Convenient script to process sample files from the root directory
Run this after uploading sample lesson plans and evaluations
"""

import sys
import os
from pathlib import Path

# Add the data directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'data'))

from sample_processor import SampleProcessor

def main():
    """Run the sample processor with enhanced output"""
    print("🎯 AI-STER Sample File Processor")
    print("=" * 50)
    print("📁 Processing files in data/samples/")
    print()
    
    # Initialize processor
    processor = SampleProcessor()
    
    # Quick file count
    inventory = processor.scan_sample_files()
    total_files = sum(len(files) for files in inventory.values())
    
    if total_files == 0:
        print("⚠️  No sample files found in data/samples/")
        print()
        print("📋 To use this tool:")
        print("1. Upload lesson plans to: data/samples/lesson_plans/")
        print("2. Upload evaluations to: data/samples/evaluations/")
        print("3. Upload templates to: data/samples/templates/")
        print("4. Upload standards docs to: data/samples/standards_references/")
        print("5. Run this script again: python process_samples.py")
        print()
        print("💡 Supported formats: .txt, .md")
        print("📦 Optional support: .pdf (PyPDF2), .docx (python-docx)")
        print("   Install with: pip install -r data/samples/optional_requirements.txt")
        return
    
    print(f"📊 Found {total_files} files to process:")
    for category, files in inventory.items():
        if files:
            print(f"   {category}: {len(files)} files")
    print()
    
    # Run comprehensive analysis
    try:
        print("🔄 Running analysis...")
        report_path = processor.save_report()
        print("✅ Analysis complete!")
        print()
        print(f"📄 Detailed report saved to: {report_path}")
        print()
        
        # Show quick summary
        analysis = processor.analyze_lesson_plans()
        if analysis["utah_standards_found"]:
            print(f"🎯 Found {len(analysis['utah_standards_found'])} Utah Core Standards")
            print(f"📚 Subjects: {', '.join(analysis['subject_areas_found'])}")
            print(f"🎓 Grade levels: {', '.join(analysis['grade_levels_found'])}")
        
        # Test AI if available
        ai_results = processor.test_ai_analysis()
        if "error" not in ai_results and ai_results["tests_run"] > 0:
            success_rate = (ai_results["successful"] / ai_results["tests_run"]) * 100
            print(f"🤖 AI Analysis: {ai_results['successful']}/{ai_results['tests_run']} successful ({success_rate:.1f}%)")
        elif "error" in ai_results:
            print(f"⚠️  AI testing: {ai_results['error']}")
        
        print()
        print("🚀 Next steps:")
        print("- Review the detailed JSON report")
        print("- Use findings to improve synthetic data in data/synthetic.py")
        print("- Update Utah standards in data/utah_lesson_plans.py")
        print("- Test AI analysis accuracy with your specific samples")
        
    except Exception as e:
        print(f"❌ Error during processing: {str(e)}")
        print("🔧 Check file permissions and formats")

if __name__ == "__main__":
    main() 