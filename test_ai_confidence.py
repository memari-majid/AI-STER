#!/usr/bin/env python3
"""Test AI confidence with different lesson plan formats"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.openai_service import OpenAIService
from pathlib import Path
import json

def test_lesson_plan_formats():
    """Test different lesson plan formats and compare AI extraction confidence"""
    
    # Initialize OpenAI service
    ai_service = OpenAIService()
    
    if not ai_service.is_enabled():
        print("❌ OpenAI service is not configured. Please set up your API key.")
        return
    
    # Test lesson plan files
    test_dir = Path("test_lesson_plans")
    test_files = [
        ("structured_lesson.txt", "Well-structured with clear labels"),
        ("narrative_lesson.txt", "Narrative paragraph style"),
        ("minimal_lesson.txt", "Minimal information"),
        ("table_format_lesson.txt", "Table/box format")
    ]
    
    results = []
    
    for filename, description in test_files:
        file_path = test_dir / filename
        
        if not file_path.exists():
            print(f"⚠️ Skipping {filename} - file not found")
            continue
            
        print(f"\n📄 Testing: {filename} ({description})")
        print("=" * 60)
        
        # Read lesson plan
        with open(file_path, 'r') as f:
            lesson_text = f.read()
        
        try:
            # Analyze with AI
            analysis = ai_service.analyze_lesson_plan(lesson_text)
            
            # Calculate extracted fields
            extracted_fields = []
            field_values = {}
            
            # Check single value fields
            single_fields = ['teacher_name', 'lesson_date', 'subject_area', 'grade_levels', 
                           'school_name', 'lesson_topic', 'class_period', 'duration', 
                           'total_students', 'utah_core_standards', 'lesson_structure']
            
            for field in single_fields:
                value = analysis.get(field)
                if value is not None and value != "":
                    extracted_fields.append(field)
                    field_values[field] = value
            
            # Check list fields
            list_fields = ['learning_objectives', 'materials', 'assessment_methods']
            for field in list_fields:
                value = analysis.get(field, [])
                if value and len(value) > 0:
                    extracted_fields.append(field)
                    field_values[field] = value
            
            confidence = analysis.get('confidence_score', 0)
            
            # Display results
            print(f"✅ Analysis Complete")
            print(f"📊 Confidence Score: {confidence:.1%}")
            print(f"📋 Extracted {len(extracted_fields)}/15 fields")
            print(f"\n🔍 Extracted Fields:")
            
            for field, value in field_values.items():
                if isinstance(value, list):
                    print(f"  • {field}: {len(value)} items")
                else:
                    print(f"  • {field}: {value}")
            
            # Store results
            results.append({
                "file": filename,
                "description": description,
                "confidence": confidence,
                "extracted_count": len(extracted_fields),
                "extracted_fields": extracted_fields,
                "analysis": analysis
            })
            
        except Exception as e:
            print(f"❌ Error analyzing {filename}: {str(e)}")
            results.append({
                "file": filename,
                "description": description,
                "error": str(e)
            })
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY OF RESULTS")
    print("=" * 60)
    
    # Sort by confidence
    successful_results = [r for r in results if 'confidence' in r]
    successful_results.sort(key=lambda x: x['confidence'], reverse=True)
    
    print("\n🏆 Ranking by Confidence Score:")
    for i, result in enumerate(successful_results, 1):
        print(f"{i}. {result['description']} ({result['file']})")
        print(f"   Confidence: {result['confidence']:.1%} | Fields: {result['extracted_count']}/15")
    
    # Save detailed results
    output_file = "test_results_ai_confidence.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Detailed results saved to: {output_file}")
    
    # Recommendations
    if successful_results:
        best_result = successful_results[0]
        print(f"\n🎯 RECOMMENDATION:")
        print(f"The {best_result['description']} format achieved the highest confidence ({best_result['confidence']:.1%})")
        print(f"It successfully extracted {best_result['extracted_count']} out of 15 fields.")
        
        # Show which fields were NOT extracted from the best format
        all_fields = ['teacher_name', 'lesson_date', 'subject_area', 'grade_levels', 
                     'school_name', 'lesson_topic', 'class_period', 'duration', 
                     'total_students', 'utah_core_standards', 'lesson_structure',
                     'learning_objectives', 'materials', 'assessment_methods']
        
        missing_fields = [f for f in all_fields if f not in best_result['extracted_fields']]
        if missing_fields:
            print(f"\n⚠️ Missing fields in best format: {', '.join(missing_fields)}")

if __name__ == "__main__":
    test_lesson_plan_formats()
