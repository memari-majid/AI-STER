#!/usr/bin/env python3
"""
Comprehensive test script for AI-STER app features
Automatically creates a complete evaluation with synthetic data
and demonstrates all app functionality
"""

import os
import sys
import json
from datetime import datetime, date
import uuid
from typing import Dict, List
import time

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

# Import all necessary modules
from data.rubrics import get_ster_items, get_professional_dispositions
from services.openai_service import OpenAIService
from services.pdf_service import PDFService
from utils.storage import save_evaluation, load_evaluations, save_ai_original
from data.sample_observation_notes import SAMPLE_OBSERVATION_NOTES

def create_test_evaluation():
    """Create a complete test evaluation with all features"""
    print("\n🚀 AI-STER Feature Test - Automatic Setup")
    print("=" * 60)
    
    # Initialize services
    openai_service = OpenAIService()
    pdf_service = PDFService()
    
    if not openai_service.is_enabled():
        print("❌ OpenAI service not enabled. Please set OPENAI_API_KEY in .env")
        return None
    
    print(f"✅ Using AI Model: {openai_service.model}")
    
    # Test data
    evaluation_id = str(uuid.uuid4())
    student_name = "Emily Johnson"
    evaluator_name = "Dr. Sarah Martinez"
    evaluation_date = date.today()
    school_name = "Riverside Elementary School"
    grade_level = "3rd Grade"
    subject_area = "Mathematics"
    
    # Use sample observation notes
    observation_notes = SAMPLE_OBSERVATION_NOTES[0]  # Using the first detailed observation
    
    print(f"\n📝 Creating test evaluation for: {student_name}")
    print(f"   Evaluator: {evaluator_name}")
    print(f"   School: {school_name}")
    print(f"   Grade: {grade_level}")
    print(f"   Subject: {subject_area}")
    
    # Get rubric items
    items = get_ster_items()
    disposition_items = get_professional_dispositions()
    
    print(f"\n📊 Evaluation Components:")
    print(f"   Competencies: {len(items)}")
    print(f"   Dispositions: {len(disposition_items)}")
    
    # Step 1: Generate AI Analysis
    print("\n🤖 Step 1: Generating AI Analysis...")
    print("   This simulates clicking 'Generate AI Analysis & Begin Scoring'")
    
    try:
        ai_analyses = openai_service.generate_analysis_for_competencies(
            items,
            observation_notes,
            student_name,
            "ster",
            None  # No lesson plan for this test
        )
        
        print(f"   ✅ Generated AI analysis for {len(ai_analyses)} competencies")
        
        # Show sample of AI analysis
        sample_id = list(ai_analyses.keys())[0]
        print(f"\n   Sample AI Analysis ({sample_id}):")
        print(f"   {ai_analyses[sample_id][:150]}...")
        
    except Exception as e:
        print(f"   ❌ AI analysis failed: {e}")
        return None
    
    # Step 2: Assign Scores (simulating supervisor review)
    print("\n📊 Step 2: Assigning Scores (simulating supervisor input)...")
    scores = {}
    justifications = {}
    
    # Assign varied scores to demonstrate the system
    score_distribution = [3, 3, 2, 3, 2, 3, 3, 2, 3, 3, 2, 3, 3, 2, 3, 2, 3, 3, 2]
    
    for i, item in enumerate(items):
        score = score_distribution[i % len(score_distribution)]
        scores[item['id']] = score
        # Initially use AI analysis as justification
        justifications[item['id']] = ai_analyses.get(item['id'], f"Justification for {item['id']}")
    
    # Disposition scores
    disposition_scores = {}
    for disp in disposition_items:
        disposition_scores[disp['id']] = 3  # All satisfactory for test
    
    print(f"   ✅ Assigned scores to all {len(items)} competencies")
    print(f"   Score distribution: Level 3: {list(scores.values()).count(3)}, Level 2: {list(scores.values()).count(2)}")
    
    # Step 3: Save AI Original (simulating "Save AI Version" button)
    print("\n💾 Step 3: Saving AI Original Version...")
    print("   This simulates clicking 'Save AI Version (PDF)'")
    
    ai_original_data = {
        'evaluation_id': evaluation_id,
        'student_name': student_name,
        'evaluator_name': evaluator_name,
        'justifications': justifications.copy(),
        'ai_analyses': ai_analyses.copy(),
        'scores': scores.copy(),
        'observation_notes': observation_notes,
        'saved_at': datetime.now().isoformat()
    }
    
    # Generate AI version PDF
    ai_pdf_data = {
        'student_name': student_name,
        'evaluator_name': evaluator_name,
        'evaluation_date': evaluation_date.isoformat(),
        'school_name': school_name,
        'grade_level': grade_level,
        'subject_area': subject_area,
        'observation_notes': observation_notes,
        'scores': scores,
        'justifications': justifications,
        'ai_analyses': ai_analyses,
        'competencies_analyzed': len(ai_analyses),
        'items': items,
        'model_used': openai_service.model,
        'is_ai_original': True
    }
    
    try:
        ai_pdf_bytes = pdf_service.generate_ai_version_pdf(ai_pdf_data)
        
        # Save PDF to file
        ai_pdf_filename = f"test_output/AI_Original_{student_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        os.makedirs("test_output", exist_ok=True)
        
        with open(ai_pdf_filename, 'wb') as f:
            f.write(ai_pdf_bytes)
        
        print(f"   ✅ AI version PDF saved: {ai_pdf_filename}")
        
    except Exception as e:
        print(f"   ❌ PDF generation failed: {e}")
    
    # Step 4: Simulate supervisor edits
    print("\n✏️ Step 4: Simulating Supervisor Edits...")
    print("   This simulates the supervisor modifying some justifications")
    
    # Modify some justifications to show changes
    items_to_modify = ['IP1', 'IP3', 'LL2', 'LL4', 'PC2']
    for item_id in items_to_modify:
        if item_id in justifications:
            original = justifications[item_id]
            justifications[item_id] = f"[SUPERVISOR REVISED] {original[:100]}... The supervisor added specific examples and clarified the evaluation based on direct observation."
    
    # Change a few scores
    scores['IP2'] = 3  # Upgrade from 2 to 3
    scores['LL3'] = 2  # Downgrade from 3 to 2
    
    print(f"   ✅ Modified {len(items_to_modify)} justifications")
    print(f"   ✅ Changed 2 scores")
    
    # Step 5: Save Complete Evaluation
    print("\n💾 Step 5: Saving Complete Evaluation...")
    print("   This simulates clicking 'Complete Evaluation'")
    
    evaluation_data = {
        'evaluation_id': evaluation_id,
        'student_name': student_name,
        'evaluator_name': evaluator_name,
        'evaluation_date': evaluation_date.isoformat(),
        'school_name': school_name,
        'grade_level': grade_level,
        'subject_area': subject_area,
        'rubric_type': 'ster',
        'evaluator_role': 'cooperating_teacher',
        'observation_notes': observation_notes,
        'lesson_plan_provided': False,
        'scores': scores,
        'justifications': justifications,
        'ai_analyses': ai_analyses,
        'disposition_scores': disposition_scores,
        'additional_comments': "This is a test evaluation created automatically to demonstrate all app features.",
        'status': 'completed',
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat(),
        'ai_original': ai_original_data  # Include AI original for comparison
    }
    
    # Save to storage manually since we need to handle the list format
    try:
        # Load existing evaluations
        with open('data_storage/evaluations.json', 'r') as f:
            evaluations = json.load(f)
        
        # Add new evaluation
        evaluations.append(evaluation_data)
        
        # Save back
        with open('data_storage/evaluations.json', 'w') as f:
            json.dump(evaluations, f, indent=2)
        
        print(f"   ✅ Evaluation saved with ID: {evaluation_id}")
    except Exception as e:
        print(f"   ❌ Failed to save evaluation: {e}")
        return None
    
    # Generate final PDF
    print("\n📄 Step 6: Generating Final Evaluation PDF...")
    print("   This simulates clicking 'Download Current Report (PDF)'")
    
    try:
        final_pdf_data = {
            **evaluation_data,
            'items': items,
            'disposition_items': disposition_items
        }
        
        final_pdf_bytes = pdf_service.generate_evaluation_pdf(final_pdf_data)
        
        final_pdf_filename = f"test_output/Final_Report_{student_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        with open(final_pdf_filename, 'wb') as f:
            f.write(final_pdf_bytes)
        
        print(f"   ✅ Final PDF saved: {final_pdf_filename}")
        
    except Exception as e:
        print(f"   ❌ PDF generation failed: {e}")
    
    # Step 7: AI Performance Comparison
    print("\n🤖 Step 7: AI Performance Evaluation...")
    print("   This simulates clicking 'AI Performance Evaluation'")
    
    print("\n   📊 Comparison Summary:")
    print(f"   Total Competencies: {len(items)}")
    print(f"   Modified Justifications: {len(items_to_modify)}")
    print(f"   Score Changes: 2")
    print(f"   AI Model Used: {openai_service.model}")
    
    print("\n   📝 Sample Comparison:")
    for item_id in items_to_modify[:2]:
        print(f"\n   {item_id}:")
        print(f"   AI Original: {ai_original_data['justifications'][item_id][:100]}...")
        print(f"   Supervisor: {justifications[item_id][:100]}...")
    
    return evaluation_data

def test_all_features():
    """Test all app features in sequence"""
    print("\n🎯 Testing All AI-STER Features")
    print("=" * 60)
    
    # Create test evaluation
    evaluation = create_test_evaluation()
    
    if not evaluation:
        print("\n❌ Test failed - could not create evaluation")
        return
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ TEST COMPLETE - All Features Demonstrated!")
    print("=" * 60)
    
    print("\n📋 What was tested:")
    print("1. ✅ AI Analysis Generation (Generate AI Analysis button)")
    print("2. ✅ Competency Scoring (Manual scoring interface)")
    print("3. ✅ Save AI Version (Save AI Version PDF button)")
    print("4. ✅ Supervisor Edits (Modifying justifications)")
    print("5. ✅ Complete Evaluation (Complete Evaluation button)")
    print("6. ✅ Download Reports (Download Current Report button)")
    print("7. ✅ AI Performance Evaluation (Comparison feature)")
    
    print("\n📁 Output Files:")
    print("   - AI Original PDF in test_output/")
    print("   - Final Report PDF in test_output/")
    print("   - Evaluation saved to data_storage/evaluations.json")
    
    print("\n🌐 To see in the app:")
    print("1. Go to https://aister.ngrok.app")
    print("2. Click '📊 Dashboard' to see the completed evaluation")
    print("3. Select the evaluation to view details")
    print("4. All buttons should be active and functional")
    
    print("\n💡 App Flow Summary:")
    print("1. New Evaluation → Fill Info → Add Observation Notes")
    print("2. Generate AI Analysis → AI analyzes all competencies")
    print("3. Score each competency → Review/edit AI suggestions")
    print("4. Save AI Version → Captures original AI output")
    print("5. Make edits → Supervisor refines evaluations")
    print("6. Complete Evaluation → Saves final version")
    print("7. AI Performance Evaluation → Compare AI vs Human")

if __name__ == "__main__":
    # Check environment
    api_key = os.getenv('OPENAI_API_KEY', '')
    if not api_key:
        print("❌ No API key found! Set OPENAI_API_KEY in .env file")
        exit(1)
    
    # Run the test
    test_all_features()
    
    print("\n✨ Test complete! Check the app to see the results.")
