import streamlit as st
import pandas as pd
import json
from datetime import datetime, date
import uuid
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import our modules
from data.rubrics import get_field_evaluation_items, get_ster_items, get_professional_dispositions
from data.synthetic import generate_synthetic_evaluations
from services.openai_service import OpenAIService
from services.pdf_service import PDFService
from utils.storage import save_evaluation, load_evaluations, export_data, import_data
from utils.validation import validate_evaluation, calculate_score

# Page configuration
st.set_page_config(
    page_title="AI-STER - Student Teaching Evaluation System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize services
openai_service = OpenAIService()
pdf_service = PDFService()

def main():
    """Main application entry point"""
    
    # Header with AI status
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🎓 AI-STER")
        st.caption("Student Teaching Evaluation Rubric System")
    
    with col2:
        if openai_service.is_enabled():
            st.success("🤖 AI Enabled")
        else:
            st.info("💡 Add OpenAI API key for AI features")
    
    # Sidebar navigation
    with st.sidebar:
        st.image("logo.png", width=200)
        
        page = st.selectbox(
            "Navigation",
            ["📝 New Evaluation", "📊 Dashboard", "🧪 Test Data", "⚙️ Settings"],
            index=0  # Explicitly set the default to first item (New Evaluation)
        )
        
        # Quick stats
        evaluations = load_evaluations()
        st.metric("Total Evaluations", len(evaluations))
        st.metric("Completed", len([e for e in evaluations if e.get('status') == 'completed']))
        st.metric("Drafts", len([e for e in evaluations if e.get('status') == 'draft']))
        
        # Lesson plan submission rate
        if evaluations:
            lesson_plan_count = len([e for e in evaluations if e.get('lesson_plan_provided', False)])
            submission_rate = (lesson_plan_count / len(evaluations)) * 100
            st.metric("Lesson Plan Rate", f"{submission_rate:.0f}%")
    
    # Route to different pages
    if page == "📊 Dashboard":
        show_dashboard()
    elif page == "📝 New Evaluation":
        show_evaluation_form()
    elif page == "🧪 Test Data":
        show_test_data()
    elif page == "⚙️ Settings":
        show_settings()

def show_dashboard():
    """Dashboard with evaluation overview and analytics"""
    st.header("📊 Evaluation Dashboard")
    
    evaluations = load_evaluations()
    
    if not evaluations:
        st.info("No evaluations found. Create your first evaluation to get started!")
        if st.button("Create New Evaluation"):
            st.session_state.page = "📝 New Evaluation"
            st.rerun()
        return
    
    # Convert to DataFrame for analysis
    df = pd.DataFrame(evaluations)
    
    # Enhanced Metrics Row 1
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Evaluations", len(df))
    with col2:
        if 'status' in df.columns:
            completed = len(df[df['status'] == 'completed'])
        else:
            completed = 0
        st.metric("Completed", completed)
    with col3:
        if completed > 0 and 'total_score' in df.columns:
            avg_score = df[df['status'] == 'completed']['total_score'].mean()
            st.metric("Average Score", f"{avg_score:.1f}")
        else:
            st.metric("Average Score", "N/A")
    with col4:
        if len(df) > 0 and 'status' in df.columns:
            success_rate = (completed/len(df)*100)
            st.metric("Success Rate", f"{success_rate:.1f}%")
        else:
            st.metric("Success Rate", "N/A")
    
    # Enhanced Metrics Row 2 - Context Information
    if 'school_setting' in df.columns and 'subject_area' in df.columns:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            unique_schools = df['school_name'].nunique() if 'school_name' in df.columns else 0
            st.metric("Schools", unique_schools)
        with col2:
            unique_settings = df['school_setting'].nunique() if 'school_setting' in df.columns else 0
            st.metric("School Types", unique_settings)
        with col3:
            unique_subjects = df['subject_area'].nunique() if 'subject_area' in df.columns else 0
            st.metric("Subject Areas", unique_subjects)
        with col4:
            current_semester = df['semester'].mode()[0] if 'semester' in df.columns and len(df) > 0 else "N/A"
            st.metric("Current Semester", current_semester)
    
    # Enhanced Charts Section
    st.subheader("📈 Evaluation Analytics")
    
    # Row 1: Status and Type Charts (existing)
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Evaluation Status")
        if 'status' in df.columns:
            status_counts = df['status'].value_counts()
            st.bar_chart(status_counts)
        else:
            st.info("No status data available")
    
    with col2:
        st.subheader("Evaluations by Type")
        if 'rubric_type' in df.columns:
            type_counts = df['rubric_type'].value_counts()
            st.bar_chart(type_counts)
        else:
            st.info("No type data available")
    
    # Row 2: New Enhanced Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Score Distribution")
        if 'total_score' in df.columns and completed > 0:
            completed_df = df[df['status'] == 'completed']
            score_bins = pd.cut(completed_df['total_score'], bins=[0, 10, 15, 20, 25, 30], labels=['0-10', '11-15', '16-20', '21-25', '26+'])
            score_dist = score_bins.value_counts().sort_index()
            st.bar_chart(score_dist)
        else:
            st.info("No score data available")
    
    with col2:
        st.subheader("Subject Areas")
        if 'subject_area' in df.columns:
            subject_counts = df['subject_area'].value_counts()
            st.bar_chart(subject_counts)
        else:
            st.info("No subject data available")
    
    # Row 3: School Context Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("School Settings")
        if 'school_setting' in df.columns:
            setting_counts = df['school_setting'].value_counts()
            st.bar_chart(setting_counts)
        else:
            st.info("No school setting data available")
    
    with col2:
        st.subheader("Grade Levels")
        if 'grade_levels' in df.columns:
            grade_counts = df['grade_levels'].value_counts()
            st.bar_chart(grade_counts)
        else:
            st.info("No grade level data available")
    
    # Competency Area Analysis
    st.subheader("🎯 Competency Area Performance")
    
    completed_evals = [e for e in evaluations if e.get('status') == 'completed']
    if completed_evals:
        competency_analysis = analyze_competency_performance(completed_evals)
        
        if competency_analysis:
            # Create competency performance chart
            comp_df = pd.DataFrame(list(competency_analysis.items()), columns=['Competency Area', 'Average Score'])
            comp_df = comp_df.sort_values('Average Score', ascending=True)
            
            st.bar_chart(comp_df.set_index('Competency Area'))
            
            # Show detailed breakdown
            with st.expander("Detailed Competency Analysis"):
                for area, avg_score in sorted(competency_analysis.items(), key=lambda x: x[1], reverse=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**{area}**")
                    with col2:
                        if avg_score >= 2.5:
                            st.success(f"{avg_score:.2f}")
                        elif avg_score >= 2.0:
                            st.warning(f"{avg_score:.2f}")
                        else:
                            st.error(f"{avg_score:.2f}")
    else:
        st.info("No completed evaluations for competency analysis")
    
    # Professional Dispositions Summary
    st.subheader("🌟 Professional Dispositions Summary")
    
    if completed_evals:
        disposition_analysis = analyze_disposition_performance(completed_evals)
        
        if disposition_analysis:
            disp_df = pd.DataFrame(list(disposition_analysis.items()), columns=['Disposition', 'Average Score'])
            disp_df = disp_df.sort_values('Average Score', ascending=True)
            
            st.bar_chart(disp_df.set_index('Disposition'))
            
            # Alert for dispositions below requirement
            failing_dispositions = [disp for disp, score in disposition_analysis.items() if score < 3.0]
            if failing_dispositions:
                st.error(f"⚠️ Dispositions below Level 3 requirement: {', '.join(failing_dispositions)}")
            else:
                st.success("✅ All dispositions meeting requirements (Level 3+)")
    else:
        st.info("No completed evaluations for disposition analysis")
    
    # Enhanced Recent Evaluations Table
    st.subheader("📋 Recent Evaluations")
    
    # Check if created_at column exists and sort accordingly
    if 'created_at' in df.columns:
        recent_df = df.sort_values('created_at', ascending=False).head(10)
    else:
        recent_df = df.head(10)
    
    # Enhanced display columns
    display_columns = ['student_name', 'evaluator_name', 'school_name', 'subject_area', 
                      'grade_levels', 'rubric_type', 'status', 'total_score']
    
    # Only include columns that exist
    available_columns = [col for col in display_columns if col in recent_df.columns]
    display_df = recent_df[available_columns].copy()
    
    # Add date if available
    if 'created_at' in df.columns:
        display_df['created_at'] = pd.to_datetime(recent_df['created_at']).dt.strftime('%Y-%m-%d')
        available_columns.append('created_at')
    
    # Enhanced column configuration
    column_config = {
        "student_name": st.column_config.TextColumn("Student", width="medium"),
        "evaluator_name": st.column_config.TextColumn("Evaluator", width="medium"),
        "school_name": st.column_config.TextColumn("School", width="large"),
        "subject_area": st.column_config.TextColumn("Subject", width="medium"),
        "grade_levels": st.column_config.TextColumn("Grades", width="small"),
        "rubric_type": st.column_config.TextColumn("Type", width="medium"),
        "status": st.column_config.TextColumn("Status", width="small"),
        "total_score": st.column_config.NumberColumn("Score", format="%d", width="small"),
        "created_at": st.column_config.DateColumn("Date", width="medium")
    }
    
    # Filter column config to only available columns
    filtered_config = {k: v for k, v in column_config.items() if k in available_columns}
    
    st.dataframe(
        display_df,
        column_config=filtered_config,
        hide_index=True,
        use_container_width=True
    )
    
    # Detailed Evaluation Viewer
    st.subheader("🔍 Detailed Evaluation Viewer")
    
    if completed_evals:
        eval_options = [f"{e['student_name']} - {e.get('school_name', 'Unknown School')} ({e['created_at'][:10]})" 
                       for e in completed_evals]
        
        selected_eval_idx = st.selectbox("Select evaluation to view details:", 
                                        range(len(eval_options)), 
                                        format_func=lambda x: eval_options[x])
        
        if selected_eval_idx is not None:
            selected_eval = completed_evals[selected_eval_idx]
            show_detailed_evaluation_view(selected_eval)
    
    # Export functionality
    st.subheader("💾 Data Management")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export All Data"):
            export_data = {
                'evaluations': evaluations,
                'export_date': datetime.now().isoformat(),
                'version': '1.0',
                'summary': {
                    'total_evaluations': len(evaluations),
                    'completed_evaluations': completed,
                    'average_score': avg_score if completed > 0 else 0
                }
            }
            st.download_button(
                "Download JSON",
                json.dumps(export_data, indent=2),
                f"ster-evaluations-{datetime.now().strftime('%Y%m%d')}.json",
                "application/json"
            )
    
    with col2:
        uploaded_file = st.file_uploader("📤 Import Data", type=['json'])
        if uploaded_file:
            try:
                data = json.load(uploaded_file)
                imported_count = import_data(data)
                st.success(f"Imported {imported_count} evaluations!")
                st.rerun()
            except Exception as e:
                st.error(f"Import failed: {str(e)}")

def analyze_competency_performance(evaluations):
    """Analyze performance by competency area"""
    from data.rubrics import get_field_evaluation_items, get_ster_items
    
    competency_scores = {}
    competency_counts = {}
    
    for evaluation in evaluations:
        rubric_type = evaluation.get('rubric_type', 'field_evaluation')
        scores = evaluation.get('scores', {})
        
        # Get appropriate rubric items
        items = get_field_evaluation_items() if rubric_type == 'field_evaluation' else get_ster_items()
        
        for item in items:
            item_id = item['id']
            competency_area = item['competency_area']
            
            if item_id in scores:
                if competency_area not in competency_scores:
                    competency_scores[competency_area] = 0
                    competency_counts[competency_area] = 0
                
                competency_scores[competency_area] += scores[item_id]
                competency_counts[competency_area] += 1
    
    # Calculate averages
    competency_averages = {}
    for area in competency_scores:
        if competency_counts[area] > 0:
            competency_averages[area] = competency_scores[area] / competency_counts[area]
    
    return competency_averages

def analyze_disposition_performance(evaluations):
    """Analyze professional disposition performance"""
    from data.rubrics import get_professional_dispositions
    
    dispositions = get_professional_dispositions()
    disposition_scores = {}
    disposition_counts = {}
    
    for evaluation in evaluations:
        disp_scores = evaluation.get('disposition_scores', {})
        
        for disposition in dispositions:
            disp_id = disposition['id']
            disp_name = disposition['name']
            
            if disp_id in disp_scores:
                if disp_name not in disposition_scores:
                    disposition_scores[disp_name] = 0
                    disposition_counts[disp_name] = 0
                
                disposition_scores[disp_name] += disp_scores[disp_id]
                disposition_counts[disp_name] += 1
    
    # Calculate averages
    disposition_averages = {}
    for disp_name in disposition_scores:
        if disposition_counts[disp_name] > 0:
            disposition_averages[disp_name] = disposition_scores[disp_name] / disposition_counts[disp_name]
    
    return disposition_averages

def show_detailed_evaluation_view(evaluation):
    """Show detailed view of a specific evaluation"""
    from data.rubrics import get_field_evaluation_items, get_ster_items, get_professional_dispositions
    
    # Basic information
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"**Student:** {evaluation['student_name']}")
        st.info(f"**Evaluator:** {evaluation['evaluator_name']}")
    with col2:
        st.info(f"**School:** {evaluation.get('school_name', 'N/A')}")
        st.info(f"**Subject:** {evaluation.get('subject_area', 'N/A')}")
    with col3:
        st.info(f"**Type:** {evaluation['rubric_type'].replace('_', ' ').title()}")
        st.info(f"**Total Score:** {evaluation['total_score']}")
    
    # Assessment Items Detail
    rubric_type = evaluation['rubric_type']
    items = get_field_evaluation_items() if rubric_type == 'field_evaluation' else get_ster_items()
    scores = evaluation.get('scores', {})
    justifications = evaluation.get('justifications', {})
    
    st.subheader("Assessment Items Breakdown")
    
    for item in items:
        item_id = item['id']
        score = scores.get(item_id, 0)
        justification = justifications.get(item_id, 'No justification provided')
        
        with st.expander(f"{item['code']}: {item['title']} (Score: {score})"):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.write(f"**Competency Area:** {item['competency_area']}")
                st.write(f"**Score:** Level {score}")
                
                # Color code the score
                if score >= 3:
                    st.success("Exceeds expectations")
                elif score >= 2:
                    st.info("Meets expectations")
                elif score >= 1:
                    st.warning("Approaching expectations")
                else:
                    st.error("Does not demonstrate")
            
            with col2:
                st.write("**Justification:**")
                st.write(justification)
    
    # Dispositions Detail
    st.subheader("Professional Dispositions")
    
    dispositions = get_professional_dispositions()
    disposition_scores = evaluation.get('disposition_scores', {})
    disposition_comments = evaluation.get('disposition_comments', {})
    
    for disposition in dispositions:
        disp_id = disposition['id']
        score = disposition_scores.get(disp_id, 0)
        comment = disposition_comments.get(disp_id, "No feedback provided")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.write(f"**{disposition['name']}**")
            st.caption(disposition['description'])
            if score >= 3:
                st.success(f"Level {score}")
            else:
                st.error(f"Level {score} (Needs Level 3+)")
        with col2:
            st.write("**Supervisor Feedback:**")
            st.write(comment if comment.strip() else "_No feedback provided_")
    
    # PDF Export button for this evaluation
    st.markdown("---")
    st.subheader("📄 Export Options")
    col1_export, col2_export = st.columns(2)
    
    with col1_export:
        # Prepare data for PDF generation
        pdf_data = {
            'rubric_type': evaluation['rubric_type'],
            'student_name': evaluation['student_name'],
            'evaluator_name': evaluation['evaluator_name'],
            'date': evaluation.get('created_at', datetime.now().isoformat())[:10],
            'school': evaluation.get('school_name', 'N/A'),
            'subject': evaluation.get('subject_area', 'N/A'),
            'is_formative': True,  # TODO: Add formative/summative tracking
            'competency_scores': [],
            'total_items': len(items),
            'meeting_expectations': sum(1 for score in scores.values() if score >= 3),
            'areas_for_growth': sum(1 for score in scores.values() if score < 3)
        }
        
        # Add competency scores
        for item in items:
            score = scores.get(item['id'], 0)
            pdf_data['competency_scores'].append({
                'competency': f"{item['code']}: {item['title']}",
                'score': score,
                'justification': justifications.get(item['id'], 'No justification provided')
            })
        
        # Add dispositions
        if evaluation['rubric_type'] == 'field_evaluation' and disposition_scores:
            pdf_data['dispositions'] = []
            for disposition in dispositions:
                disp_id = disposition['id']
                score = disposition_scores.get(disp_id, 0)
                pdf_data['dispositions'].append({
                    'disposition': disposition['name'],
                    'score': score,
                    'notes': disposition_comments.get(disp_id, '')
                })
        
        # Add AI analysis if available
        ai_analyses = evaluation.get('ai_analyses', {})
        if ai_analyses:
            # Collect all AI analyses
            all_analyses = []
            strengths = []
            areas_for_growth = []
            
            for item_id, analysis in ai_analyses.items():
                if analysis and isinstance(analysis, str):
                    # Get the item name for context
                    item = next((i for i in items if i['id'] == item_id), None)
                    if item:
                        item_name = f"{item['code']}: {item['title']}"
                        # Add the analysis with context
                        all_analyses.append(f"{item_name}\n{analysis}")
                        
                        # Extract strengths (look for positive indicators)
                        if any(word in analysis.lower() for word in ['strong', 'excellent', 'effective', 'well', 'good', 'demonstrates']):
                            strengths.append(f"{item['code']}: {analysis[:150]}...")
                        
                        # Extract areas for growth (look for improvement indicators)
                        if any(word in analysis.lower() for word in ['improve', 'develop', 'consider', 'could', 'should', 'needs']):
                            areas_for_growth.append(f"{item['code']}: {analysis[:150]}...")
            
            pdf_data['ai_analysis'] = {
                'strengths': strengths[:5],  # Limit to top 5
                'areas_for_growth': areas_for_growth[:5],  # Limit to top 5
                'recommendations': [],  # Could be extracted from overall analysis
                'full_analyses': all_analyses  # Include all analyses
            }
        
        # Generate PDF
        try:
            pdf_bytes = pdf_service.generate_evaluation_pdf(pdf_data)
            
            # Create filename
            filename = f"{evaluation['student_name'].replace(' ', '_')}_{evaluation['rubric_type']}_{evaluation.get('created_at', datetime.now().isoformat())[:10]}.pdf"
            
            st.download_button(
                label="📄 Download Evaluation Report (PDF)",
                data=pdf_bytes,
                file_name=filename,
                mime="application/pdf",
                help="Download the complete evaluation report as a PDF file"
            )
        except Exception as e:
            st.error(f"Error generating PDF: {str(e)}")
    
    with col2_export:
        st.info("💡 **Tip**: Download the PDF report for archival or distribution purposes.")

def show_evaluation_form():
    """Evaluation form for creating new evaluations"""
    st.header("📝 New Evaluation")
    
    # Get dispositions (same for all evaluation types)
    dispositions = get_professional_dispositions()
    
    # Initialize session state for lesson plan analysis
    if 'lesson_plan_analysis' not in st.session_state:
        st.session_state.lesson_plan_analysis = None
    if 'extracted_info' not in st.session_state:
        st.session_state.extracted_info = {}
    
    # STEP 1: Lesson Plan Upload (Optional)
    st.subheader("📄 Step 1: Upload Lesson Plan (Optional)")
    st.caption("Upload the student teacher's lesson plan to automatically extract evaluation information, or skip to proceed without it")
    
    # Add skip option
    col1, col2 = st.columns([3, 1])
    with col1:
        # Option to use synthetic data or upload real file
        input_method = st.radio(
            "Choose input method:",
            ["📤 Upload File", "🧪 Use Synthetic Data", "✏️ Paste Text", "⏭️ Skip Lesson Plan"],
            horizontal=True
        )
    
    with col2:
        if input_method != "⏭️ Skip Lesson Plan":
            st.info("💡 Lesson plan helps AI generate better analysis")
        else:
            st.warning("⚠️ Proceeding without lesson plan")
    
    lesson_plan_text = None
    
    if input_method == "⏭️ Skip Lesson Plan":
        st.info("✅ Skipping lesson plan upload. You can proceed directly to basic information.")
        lesson_plan_text = None
        # Clear any existing lesson plan analysis
        st.session_state.lesson_plan_analysis = None
        
    elif input_method == "🧪 Use Synthetic Data":
        # Load available synthetic lesson plans
        evaluations = load_evaluations()
        synthetic_evaluations = [e for e in evaluations if e.get('is_synthetic', False) and e.get('lesson_plan')]
        
        if synthetic_evaluations:
            st.info(f"Found {len(synthetic_evaluations)} synthetic lesson plans available for testing")
            
            # Create selection options
            eval_options = []
            for i, eval_data in enumerate(synthetic_evaluations):
                student_name = eval_data.get('student_name', f'Student {i+1}')
                subject = eval_data.get('subject_area', 'Unknown Subject')
                grade = eval_data.get('grade_levels', 'Unknown Grade')
                school = eval_data.get('school_name', 'Unknown School')
                option_text = f"{student_name} - {subject} ({grade}) at {school}"
                eval_options.append(option_text)
            
            selected_index = st.selectbox(
                "Select a synthetic lesson plan:",
                range(len(eval_options)),
                format_func=lambda x: eval_options[x],
                help="Choose from available synthetic lesson plans for testing"
            )
            
            if selected_index is not None:
                selected_evaluation = synthetic_evaluations[selected_index]
                lesson_plan_text = selected_evaluation.get('lesson_plan', '')
                
                # Show preview
                with st.expander("📋 Preview Selected Lesson Plan"):
                    st.text_area(
                        "Lesson Plan Content:",
                        value=lesson_plan_text[:500] + "..." if len(lesson_plan_text) > 500 else lesson_plan_text,
                        height=200,
                        disabled=True
                    )
                
                st.success(f"✅ Loaded synthetic lesson plan for {selected_evaluation.get('student_name', 'Unknown Student')}")
        else:
            st.warning("No synthetic lesson plans available. Generate some test data first!")
            if st.button("🧪 Go to Test Data Generation"):
                st.session_state.page = "🧪 Test Data"
                st.rerun()
    
    elif input_method == "📤 Upload File":
        uploaded_file = st.file_uploader(
            "Choose lesson plan file",
            type=['txt', 'docx', 'pdf', 'doc'],
            help="Upload the lesson plan in text, Word, or PDF format"
        )
    
        if uploaded_file is not None:
            # Read file content based on type
            try:
                if uploaded_file.type == "text/plain":
                    lesson_plan_text = str(uploaded_file.read(), "utf-8")
                elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", 
                                          "application/msword"]:
                    st.info("Word document uploaded. Please copy and paste the content below for analysis.")
                    lesson_plan_text = st.text_area(
                        "Paste lesson plan content:",
                        height=200,
                        placeholder="Copy and paste your lesson plan content here..."
                    )
                elif uploaded_file.type == "application/pdf":
                    st.info("PDF uploaded. Please copy and paste the content below for analysis.")
                    lesson_plan_text = st.text_area(
                        "Paste lesson plan content:",
                        height=200,
                        placeholder="Copy and paste your lesson plan content here..."
                    )
                else:
                    lesson_plan_text = st.text_area(
                        "Paste lesson plan content:",
                        height=200,
                        placeholder="Copy and paste your lesson plan content here..."
                    )
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
                lesson_plan_text = st.text_area(
                    "Paste lesson plan content:",
                    height=200,
                    placeholder="Copy and paste your lesson plan content here..."
                )
    
    elif input_method == "✏️ Paste Text":
        lesson_plan_text = st.text_area(
            "Paste lesson plan content directly:",
            height=200,
            placeholder="Paste your lesson plan content here...",
            help="Copy and paste the lesson plan text for AI analysis"
        )
    
    # AI Analysis of Lesson Plan
    if lesson_plan_text and len(lesson_plan_text.strip()) > 50:
        if openai_service.is_enabled():
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("🤖 Analyze Lesson Plan with AI", type="primary"):
                    with st.spinner("Analyzing lesson plan..."):
                        try:
                            analysis = openai_service.analyze_lesson_plan(lesson_plan_text)
                            analysis['extraction_timestamp'] = datetime.now().isoformat()
                            st.session_state.lesson_plan_analysis = analysis
                            st.success("✅ Lesson plan analyzed successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Analysis failed: {str(e)}")
            
            with col2:
                if st.session_state.lesson_plan_analysis:
                    st.success("✅ Analysis Complete")
                    confidence = st.session_state.lesson_plan_analysis.get('confidence_score', 0)
                    st.metric("AI Confidence", f"{confidence:.1%}")
        else:
            st.warning("🤖 AI features disabled. Add OpenAI API key in Settings to enable automatic extraction.")
    
    # Display Extracted Information
    if st.session_state.lesson_plan_analysis:
        st.subheader("📋 Step 2: Review Extracted Information")
        st.caption("Review and modify the information extracted from the lesson plan. Supervisor notes override lesson plan data.")
        
        analysis = st.session_state.lesson_plan_analysis
        
        # Create two columns for extracted vs editable info
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("**🤖 AI Extracted Information**")
            with st.container():
                st.text_input("Teacher Name (Extracted)", value=analysis.get('teacher_name', 'Not found'), disabled=True)
                st.text_input("Lesson Date (Extracted)", value=analysis.get('lesson_date', 'Not found'), disabled=True)
                st.text_input("Subject (Extracted)", value=analysis.get('subject_area', 'Not found'), disabled=True)
                st.text_input("Grade Level (Extracted)", value=analysis.get('grade_levels', 'Not found'), disabled=True)
                st.text_input("School (Extracted)", value=analysis.get('school_name', 'Not found'), disabled=True)
                st.text_input("Class Size (Extracted)", value=str(analysis.get('total_students', 'Not found')), disabled=True)
        
        with col2:
            st.markdown("**✏️ Supervisor Override (Fill as needed)**")
            with st.container():
                student_name = st.text_input(
                    "Student Teacher Name *", 
                    value=analysis.get('teacher_name', ''),
                    key="student_name",
                    help="Override the extracted teacher name if incorrect"
                )
                
                evaluation_date = st.date_input(
                    "Evaluation Date *",
                    value=datetime.now().date(),
                    help="Date of this evaluation (may differ from lesson date)"
                )
                
                subject_area = st.text_input(
                    "Subject Area",
                    value=analysis.get('subject_area', ''),
                    key="subject_area_override"
                )
                
                grade_levels = st.text_input(
                    "Grade Levels",
                    value=analysis.get('grade_levels', ''),
                    key="grade_levels_override"
                )
                
                school_name = st.text_input(
                    "School Name",
                    value=analysis.get('school_name', ''),
                    key="school_name_override"
                )
                
                class_size = st.number_input(
                    "Class Size",
                    min_value=1,
                    max_value=40,
                    value=analysis.get('total_students', 20) if analysis.get('total_students') else 20,
                    key="class_size_override"
                )
                
                # Additional context from lesson plan
                lesson_topic = st.text_input(
                    "Lesson Topic",
                    value=analysis.get('lesson_topic', ''),
                    key="lesson_topic_override"
                )
        
        # Store the final information (supervisor override takes precedence)
        st.session_state.extracted_info = {
            'student_name': student_name,
            'subject_area': subject_area or analysis.get('subject_area', ''),
            'grade_levels': grade_levels or analysis.get('grade_levels', ''),
            'school_name': school_name or analysis.get('school_name', ''),
            'class_size': class_size,
            'lesson_topic': lesson_topic or analysis.get('lesson_topic', ''),
            'evaluation_date': evaluation_date.isoformat(),
            'lesson_plan_text': lesson_plan_text,
            'ai_analysis': analysis
        }
    
    # Basic Information (Traditional Form - fallback if no lesson plan)
    else:
        st.subheader("📋 Step 2: Basic Information")
        if input_method == "⏭️ Skip Lesson Plan":
            st.caption("✅ No lesson plan provided - please enter evaluation information manually")
            # Visual indicator for skipped lesson plan
            st.info("📋 **Lesson Plan Status:** Skipped - AI analysis will rely solely on observation notes")
        else:
            st.caption("Enter evaluation information manually")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            student_name = st.text_input("Student Teacher Name *", key="student_name")
        with col2:
            evaluation_date = st.date_input("Evaluation Date *", value=datetime.now().date())
        with col3:
            subject_area = st.text_input("Subject Area", key="subject_area_manual")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            grade_levels = st.text_input("Grade Levels", key="grade_levels_manual")
        with col2:
            school_name = st.text_input("School Name", key="school_name_manual")
        with col3:
            class_size = st.number_input("Class Size", min_value=1, max_value=40, value=20)
        
        # Visual reminder about lesson plan benefits
        if input_method == "⏭️ Skip Lesson Plan":
            with st.expander("💡 Why upload a lesson plan?", expanded=False):
                st.markdown("""
                **Benefits of uploading a lesson plan:**
                - 🤖 **Better AI Analysis**: AI can compare planned vs. observed activities
                - 📊 **More Accurate Justifications**: Evidence-based analysis using lesson objectives
                - ⚡ **Faster Evaluation**: Auto-extraction of student and lesson information
                - 🎯 **Contextual Insights**: AI understands the lesson's goals and structure
                
                **You can still get good results without a lesson plan** - just ensure your observation notes are detailed!
                """)
        
        # Store manual information
        st.session_state.extracted_info = {
            'student_name': student_name,
            'subject_area': subject_area,
            'grade_levels': grade_levels,
            'school_name': school_name,
            'class_size': class_size,
            'evaluation_date': evaluation_date.isoformat(),
            'lesson_plan_text': lesson_plan_text if lesson_plan_text else None,
            'ai_analysis': None
        }
    
    # Evaluator Information
    st.subheader("👨‍🏫 Evaluator Information")
    col1, col2 = st.columns(2)
    with col1:
        evaluator_name = st.text_input("Evaluator Name *", key="evaluator_name")
    with col2:
        # Supervisor is the only role now
        evaluator_role = "supervisor"
        st.text_input("Evaluator Role", value="Supervisor", disabled=True)
    
    # Evaluation Type Selection
    st.subheader("📋 Evaluation Type")
    rubric_type = st.selectbox(
        "Select Evaluation Type",
        ["field_evaluation", "ster"],
        index=1,  # Make STER default (index 1)
        format_func=lambda x: "Field Evaluation" if x == "field_evaluation" else "STER"
    )
    
    # Add rubric reference section
    with st.expander("📖 **View Official Rubric**", expanded=False):
        if rubric_type == "field_evaluation":
            st.markdown("### Field Evaluation Rubric")
            st.caption("Official USBE STER standards applied to field evaluation context")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("[📄 View Online (PDF)](https://github.com/memari-majid/AI-STER/blob/main/docs/STER%20Rubric.pdf)")
            with col2:
                # Add download button
                try:
                    with open("docs/STER Rubric.pdf", "rb") as pdf_file:
                        st.download_button(
                            label="⬇️ Download PDF",
                            data=pdf_file.read(),
                            file_name="STER_Rubric.pdf",
                            mime="application/pdf"
                        )
                except FileNotFoundError:
                    st.error("PDF file not found")
            with col3:
                st.info("💡 **Tip**: View online or download for offline use")
            
            # Quick reference for Field Evaluation
            st.markdown("""
            **Field Evaluation Components:**
            - 8 Core Competency Items
            - 6 Professional Dispositions (Level 3+ required)
            - Focus on 3-week field experience assessment
            """)
        else:  # STER evaluation
            st.markdown("### STER Evaluation Rubric")
            st.caption("Official USBE STER (Student Teaching Evaluation Rubric) standards")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("[📄 View Online (PDF)](https://github.com/memari-majid/AI-STER/blob/main/docs/STER%20Rubric.pdf)")
            with col2:
                # Add download button
                try:
                    with open("docs/STER Rubric.pdf", "rb") as pdf_file:
                        st.download_button(
                            label="⬇️ Download PDF",
                            data=pdf_file.read(),
                            file_name="STER_Rubric.pdf",
                            mime="application/pdf"
                        )
                except FileNotFoundError:
                    st.error("PDF file not found")
            with col3:
                st.info("💡 **Tip**: View online or download for offline use")
            
            # Quick reference for STER
            st.markdown("""
            **STER Competency Areas:**
            - **Learners and Learning (LL)**: LL1-LL7
            - **Instructional Clarity (IC)**: IC1/IC2, IC3, IC4, IC5/IC6, IC7
            - **Instructional Practice (IP)**: IP1-IP8
            - **Classroom Climate (CC)**: CC1-CC8
            - **Professional Responsibility (PR)**: PR1-PR7
            
            *All 35 competencies require Level 2+ for passing*
            """)
        
        st.divider()
        st.caption("📌 Keep the rubric open in another tab for easy reference during evaluation")
    
    # Get rubric items based on evaluation type
    if rubric_type == "field_evaluation":
        items = get_field_evaluation_items()
    else:  # STER evaluation
        # Get all STER items (no filtering needed since only supervisors exist)
        items = get_ster_items()
        
        # Display evaluation information
        st.info(f"📋 **Supervisor STER Evaluation** - You will evaluate {len(items)} competencies")
        st.caption("All items based on classroom observation and lesson planning")
        
        # Remove role indicator legend since we only have supervisors now

    
    # Check if we have minimum required information
    if not student_name or not evaluator_name:
        st.warning("Please provide student teacher name and evaluator name to continue.")
        return
    
    # Initialize session state for scores and justifications
    if 'scores' not in st.session_state:
        st.session_state.scores = {}
    if 'justifications' not in st.session_state:
        st.session_state.justifications = {}
    if 'disposition_scores' not in st.session_state:
        st.session_state.disposition_scores = {}
    if 'disposition_comments' not in st.session_state:
        st.session_state.disposition_comments = {}
    if 'observation_notes' not in st.session_state:
        st.session_state.observation_notes = ""
    if 'ai_analyses' not in st.session_state:
        st.session_state.ai_analyses = {}
    
    # STEP 3: Classroom Observation Notes
    st.subheader("📝 Step 3: Classroom Observation Notes")
    st.caption("Record your detailed observations of the student teacher's performance during the lesson")
    
    observation_notes = st.text_area(
        "Detailed Observation Notes",
        value=st.session_state.observation_notes,
        height=200,
        placeholder="""Record specific observations about the student teacher's performance:

• How did they introduce the lesson and engage students?
• What teaching strategies and methods were used?
• How did they manage the classroom and respond to student needs?
• What evidence did you see of lesson planning and preparation?
• How did they assess student learning and provide feedback?
• What professional behaviors and dispositions were demonstrated?
• Any specific examples of strengths or areas for improvement?

Be as detailed as possible - these notes will be used to generate evidence-based justifications for each competency area.""",
        help="Detailed observations will help generate more accurate AI justifications",
        key="observation_text_area"
    )
    
    # Store observation notes in session state
    st.session_state.observation_notes = observation_notes
    
    # STEP 4: AI Analysis and Justification Generation
    st.subheader("🤖 Step 4: AI Analysis and Justification Generation")
    if st.session_state.lesson_plan_analysis:
        st.caption("AI analyzes your observation notes and lesson plan to generate evidence-based justifications")
    else:
        st.caption("AI analyzes your observation notes to generate evidence-based justifications")
        st.info("📋 **Note:** No lesson plan provided - AI analysis will focus on observation notes only")
    
    # Check if observation notes are available
    if observation_notes.strip():
        if openai_service.is_enabled():
            col1, col2 = st.columns([2, 1])
            with col1:
                button_text = "🤖 Generate AI Analysis for All Competencies"
                if not st.session_state.lesson_plan_analysis:
                    button_text += " (Observation Notes Only)"
                    
                if st.button(button_text, type="primary", key="generate_ai_analysis"):
                    with st.spinner("Analyzing observation notes and generating evidence-based justifications..."):
                        try:
                            # Get lesson plan context if available
                            lesson_plan_context = None
                            if st.session_state.lesson_plan_analysis:
                                lesson_plan_context = f"Lesson Topic: {st.session_state.lesson_plan_analysis.get('lesson_topic', 'N/A')}\n"
                                lesson_plan_context += f"Learning Objectives: {', '.join(st.session_state.lesson_plan_analysis.get('learning_objectives', []))}\n"
                                lesson_plan_context += f"Lesson Structure: {st.session_state.lesson_plan_analysis.get('lesson_structure', 'N/A')}"
                            
                            # Generate AI analysis for all items
                            ai_analyses = openai_service.generate_analysis_for_competencies(
                                items,
                                observation_notes,
                                student_name,
                                rubric_type,
                                lesson_plan_context
                            )
                            
                            # Store AI analyses in session state
                            st.session_state.ai_analyses = ai_analyses
                            success_message = f"✅ Generated AI analysis for {len(ai_analyses)} competencies!"
                            if not st.session_state.lesson_plan_analysis:
                                success_message += " (Based on observation notes only)"
                            st.success(success_message)
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"Failed to generate AI analysis: {str(e)}")
            
            with col2:
                if st.session_state.get('ai_analyses'):
                    st.success("✅ AI Analysis Complete")
                    st.metric("Competencies Analyzed", len(st.session_state.ai_analyses))
                    if st.button("🔄 Regenerate Analysis", key="regenerate_analysis"):
                        st.session_state.ai_analyses = {}
                        st.rerun()
                else:
                    # Show lesson plan status
                    if st.session_state.lesson_plan_analysis:
                        st.info("📄 Lesson plan available")
                    else:
                        st.warning("📄 No lesson plan")
        else:
            st.warning("🤖 AI features disabled. Add OpenAI API key in Settings to enable AI analysis.")
    else:
        st.info("ℹ️ Please add detailed observation notes to enable AI analysis generation.")
        if not st.session_state.lesson_plan_analysis:
            st.warning("⚠️ **Important:** Without a lesson plan, detailed observation notes are crucial for quality AI analysis!")
    
    # Show AI Analysis Results
    if st.session_state.get('ai_analyses'):
        st.subheader("📊 AI Analysis Results")
        st.caption("Review the AI's evidence-based analysis before assigning scores")
        
        # Group items by competency area for better organization
        competency_groups = {}
        for item in items:
            area = item['competency_area']
            if area not in competency_groups:
                competency_groups[area] = []
            competency_groups[area].append(item)
        
        for area, area_items in competency_groups.items():
            with st.expander(f"📋 {area} - AI Analysis", expanded=True):
                for item in area_items:
                    item_id = item['id']
                    
                    # No role indicator needed - all items are for supervisors
                    st.markdown(f"**{item['code']}: {item['title']}**")
                    st.markdown(f"*{item['context']}*")
                    
                    # Always display something for each competency - either AI analysis or a placeholder
                    if st.session_state.get('ai_analyses') and item_id in st.session_state.ai_analyses:
                        ai_analysis = st.session_state.ai_analyses[item_id]
                        
                        # Check for warning indicators and display them prominently
                        warning_displayed = False
                        original_analysis = ai_analysis
                        
                        # Check for various warning patterns
                        if ai_analysis.startswith('[LIMITED_EVIDENCE]') or '[LIMITED_EVIDENCE]' in ai_analysis:
                            st.error("⚠️ **Limited Evidence Available** - No specific observations found for this competency in the observation notes.")
                            ai_analysis = ai_analysis.replace('[LIMITED_EVIDENCE]', '').strip()
                            warning_displayed = True
                        elif ai_analysis.startswith('[NO_CONTEXT]') or '[NO_CONTEXT]' in ai_analysis:
                            st.error("⚠️ **No Relevant Context** - The observation notes do not contain information relevant to this competency.")
                            ai_analysis = ai_analysis.replace('[NO_CONTEXT]', '').strip()
                            warning_displayed = True
                        elif ai_analysis.startswith('[GENERIC]') or '[GENERIC]' in ai_analysis:
                            st.error("⚠️ **Generic Analysis** - Limited specific evidence was available for this competency.")
                            ai_analysis = ai_analysis.replace('[GENERIC]', '').strip()
                            warning_displayed = True
                        elif 'no specific observations were recorded' in ai_analysis.lower():
                            st.error("⚠️ **Limited Observations** - No specific observations were recorded for this competency area.")
                            warning_displayed = True
                        elif 'limited specific evidence' in ai_analysis.lower():
                            st.error("⚠️ **Limited Evidence** - Limited specific evidence was found for this competency.")
                            warning_displayed = True
                        elif 'note:' in ai_analysis.lower() and 'observation' in ai_analysis.lower():
                            st.error("⚠️ **Observation Note** - Additional observations may be needed for this competency.")
                            warning_displayed = True
                        
                        # Display cleaned analysis
                        if ai_analysis.strip():
                            st.info(f"**AI Analysis:** {ai_analysis}")
                        else:
                            st.warning("No specific analysis available for this competency.")
                        
                        # Allow editing of AI analysis
                        edited_analysis = st.text_area(
                            f"Edit AI Analysis for {item['code']}",
                            value=ai_analysis,
                            height=80,
                            key=f"edit_analysis_{item_id}",
                            help="Edit the AI analysis as needed based on your observations"
                        )
                        
                        # Update session state with edited analysis
                        if edited_analysis != ai_analysis:
                            st.session_state.ai_analyses[item_id] = edited_analysis
                    
                    elif st.session_state.get('ai_analyses'):
                        # AI analysis was generated but this competency is missing - show warning
                        st.error("⚠️ **Missing Analysis** - AI analysis was not generated for this competency. This may indicate limited relevant observations.")
                        st.warning(f"No AI analysis available for {item['code']}. Consider adding specific observations for this competency area.")
                        
                        # Provide empty text area for manual input
                        manual_analysis = st.text_area(
                            f"Manual Analysis for {item['code']}",
                            value="",
                            height=80,
                            placeholder="Add your own analysis based on observations...",
                            key=f"manual_analysis_{item_id}",
                            help="Enter your own analysis since AI analysis was not generated"
                        )
                        
                        # Store manual analysis if provided
                        if manual_analysis.strip():
                            if 'ai_analyses' not in st.session_state:
                                st.session_state.ai_analyses = {}
                            st.session_state.ai_analyses[item_id] = manual_analysis
                    
                    else:
                        # No AI analysis generated yet - show placeholder
                        st.info(f"⏳ **Analysis Pending** - AI analysis not yet generated for {item['code']}.")
                        st.write("Generate AI analysis above to see evidence-based insights for this competency.")
                        
                    st.divider()
    
    # STEP 5: Informed Assessment Scoring
    st.subheader("🎯 Step 5: Informed Assessment Scoring")
    st.caption("Assign scores based on your observations and the AI analysis above")
    
    # Show guidance about using AI analysis
    if st.session_state.get('ai_analyses'):
        st.success("✅ AI analysis available! Use the evidence-based justifications above to inform your scoring decisions.")
    else:
        st.info("💡 Generate AI analysis first to get evidence-based justifications that will help inform your scoring.")
    
    st.markdown("**Score Each Competency (Level 0-3)**")
    
    # Check for missing scores and show warning (treat "not_observed" as valid)
    total_items = len(items)
    scored_items = len([s for s in st.session_state.scores.values() if s is not None])
    missing_scores = total_items - scored_items
    
    if missing_scores > 0:
        st.warning(f"⚠️ **{missing_scores} out of {total_items} competencies still need scores.** Please score all competencies before saving the evaluation.")
    else:
        st.success(f"✅ **All {total_items} competencies have been scored!**")
    
    total_score = 0
    all_items_scored = True
    
    # Group items by competency area for better organization
    competency_groups = {}
    for item in items:
        area = item['competency_area']
        if area not in competency_groups:
            competency_groups[area] = []
        competency_groups[area].append(item)
    
    for area, area_items in competency_groups.items():
        st.markdown(f"**{area}**")
        
        for item in area_items:
            item_id = item['id']
            current_score = st.session_state.scores.get(item_id)
            
            # Create scoring interface for each item
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # No role indicator needed - all items are for supervisors
                st.markdown(f"*{item['code']}: {item['title']}*")
                st.caption(f"{item['context']}")
                
                # Show AI analysis if available
                if st.session_state.get('ai_analyses') and item_id in st.session_state.ai_analyses:
                    with st.expander("🤖 View AI Analysis", expanded=False):
                        ai_analysis = st.session_state.ai_analyses[item_id]
                        
                        # Check for and display warnings
                        warning_displayed = False
                        original_analysis = ai_analysis
                        
                        # Check for various warning patterns
                        if ai_analysis.startswith('[LIMITED_EVIDENCE]') or '[LIMITED_EVIDENCE]' in ai_analysis:
                            st.error("⚠️ **Limited Evidence Available** - No specific observations found for this competency.")
                            ai_analysis = ai_analysis.replace('[LIMITED_EVIDENCE]', '').strip()
                            warning_displayed = True
                        elif ai_analysis.startswith('[NO_CONTEXT]') or '[NO_CONTEXT]' in ai_analysis:
                            st.error("⚠️ **No Relevant Context** - The observation notes do not contain information relevant to this competency.")
                            ai_analysis = ai_analysis.replace('[NO_CONTEXT]', '').strip()
                            warning_displayed = True
                        elif ai_analysis.startswith('[GENERIC]') or '[GENERIC]' in ai_analysis:
                            st.error("⚠️ **Generic Analysis** - Limited specific evidence was available for this competency.")
                            ai_analysis = ai_analysis.replace('[GENERIC]', '').strip()
                            warning_displayed = True
                        elif 'no specific observations were recorded' in ai_analysis.lower():
                            st.error("⚠️ **Limited Observations** - No specific observations were recorded for this competency area.")
                            warning_displayed = True
                        elif 'limited specific evidence' in ai_analysis.lower():
                            st.error("⚠️ **Limited Evidence** - Limited specific evidence was found for this competency.")
                            warning_displayed = True
                        elif 'note:' in ai_analysis.lower() and 'observation' in ai_analysis.lower():
                            st.error("⚠️ **Observation Note** - Additional observations may be needed for this competency.")
                            warning_displayed = True
                        
                        if ai_analysis.strip():
                            st.write(ai_analysis)
                        else:
                            st.write("No specific analysis available.")
                else:
                    with st.expander("🤖 View AI Analysis", expanded=False):
                        st.warning("AI analysis not yet generated. Generate AI analysis above to see insights.")
            
            with col2:
                def format_score_option(score):
                    if score is None:
                        return "Select score..."
                    elif score == "not_observed":
                        return "Not Observed - Competency not demonstrated in this observation"
                    else:
                        return f"Level {score} - {get_level_name(score)}"
                
                score = st.selectbox(
                    f"Score",
                    options=[None, "not_observed", 0, 1, 2, 3],
                    index=0 if current_score is None else (1 if current_score == "not_observed" else current_score + 2),
                    format_func=format_score_option,
                    key=f"score_select_{item_id}",
                    help=f"Select score level for {item['code']} based on your observations and AI analysis"
                )
                
                if score is not None:
                    st.session_state.scores[item_id] = score
                    # Use AI analysis as justification if available
                    if st.session_state.get('ai_analyses') and item_id in st.session_state.ai_analyses:
                        # Clean the analysis before using as justification
                        clean_analysis = st.session_state.ai_analyses[item_id]
                        # Remove all warning patterns
                        clean_analysis = clean_analysis.replace('[LIMITED_EVIDENCE]', '').replace('[NO_CONTEXT]', '').replace('[GENERIC]', '').strip()
                        # Remove common warning phrases
                        warning_phrases = [
                            '**NOTE: No specific observations were recorded for this competency area',
                            'supervisor may wish to add additional details',
                            'limited specific evidence was recorded',
                            'Based on the available observation notes, limited specific evidence'
                        ]
                        for phrase in warning_phrases:
                            if phrase.lower() in clean_analysis.lower():
                                # Find and remove the sentence containing the warning
                                sentences = clean_analysis.split('. ')
                                clean_sentences = [s for s in sentences if phrase.lower() not in s.lower()]
                                clean_analysis = '. '.join(clean_sentences).strip()
                        
                        if clean_analysis and not clean_analysis.endswith('.'):
                            clean_analysis += '.'
                        
                        if clean_analysis.strip():
                            st.session_state.justifications[item_id] = clean_analysis
                    if isinstance(score, int):  # Only add numeric scores to total
                        total_score += score
                else:
                    all_items_scored = False
            
            # Show selected score description (use actual selected score, not session state)
            display_score = score if score is not None else current_score
            if display_score is not None:
                if display_score == "not_observed":
                    st.info(f"**Not Observed:** This competency was not demonstrated during this observation session")
                else:
                    score_desc = item['levels'].get(str(display_score), 'No description available')
                    st.info(f"**Level {display_score}:** {score_desc}")
            else:
                # Show that this competency is not yet scored with warning
                st.warning(f"⏸️ **Not yet scored** - {item['code']} requires a score level to complete the evaluation")
        
        st.divider()
    
    # Score Summary
    scored_items = len([s for s in st.session_state.scores.values() if s is not None])
    level_1_count = len([s for s in st.session_state.scores.values() if s == 1])
    level_0_count = len([s for s in st.session_state.scores.values() if s == 0])
    critical_areas = level_0_count + level_1_count
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if scored_items < len(items):
            st.metric("Items Scored", f"{scored_items}/{len(items)}", delta=f"-{len(items) - scored_items} missing", delta_color="inverse")
        else:
            st.metric("Items Scored", f"{scored_items}/{len(items)}", delta="Complete ✅")
    with col2:
        if critical_areas > 0:
            st.metric("Areas for Improvement", critical_areas, delta="Need Level 2+", delta_color="inverse", help="Areas scoring Level 0-1 that must improve to Level 2+ to pass")
        else:
            st.metric("Areas for Improvement", 0, delta="All Level 2+ ✅", help="All competencies meeting minimum requirements")
    with col3:
        if scored_items > 0:
            passing_items = len([s for s in st.session_state.scores.values() if isinstance(s, int) and s >= 2])
            st.metric("Meeting Standards", f"{passing_items}/{scored_items}", help="Competencies at Level 2 or higher")
        else:
            st.metric("Meeting Standards", "0/0")
    with col4:
        all_items_scored = scored_items == len(items)
        meets_minimum = all_items_scored and critical_areas == 0
        if meets_minimum:
            st.metric("Pass Requirements", "✅ Met", help="All competencies at Level 2+")
        elif all_items_scored:
            st.metric("Pass Requirements", "🌱 Growing", delta=f"{critical_areas} areas for growth", delta_color="inverse")
        else:
            st.metric("Pass Requirements", "⏳ Pending", help="Complete scoring to determine status")
    
    # Growth Areas Alert (Level 1 scores)
    if scored_items > 0:
        level_1_items = [(item_id, item) for item in items for item_id, score in st.session_state.scores.items() if item['id'] == item_id and score == 1]
        level_0_items = [(item_id, item) for item in items for item_id, score in st.session_state.scores.items() if item['id'] == item_id and score == 0]
        
        if level_1_items or level_0_items:
            st.subheader("🌟 Areas for Growth and Development")
            st.caption("Supporting student teachers to achieve Level 2+ in all competencies. These areas offer opportunities for focused improvement.")
            
            if level_0_items:
                st.info("**Level 0 - Emerging Skills (Priority for Development)**")
                for item_id, item in level_0_items:
                    st.write(f"• **{item['code']}**: {item['title']}")
            
            if level_1_items:
                st.info("**Level 1 - Developing Competency (Almost There!)**")
                for item_id, item in level_1_items:
                    st.write(f"• **{item['code']}**: {item['title']}")
            
            st.info("💡 **Next Steps**: Use AI analysis below to get specific guidance on moving these areas from Level 1 to Level 2")
            st.divider()
        elif scored_items == len(items):
            st.success("🎉 **Excellent Progress!** All competencies are at Level 2 or higher - student is meeting minimum standards.")
            st.divider()
    
    # STEP 6: Review and Edit Justifications
    st.subheader("✏️ Step 6: Review and Edit Justifications")
    st.caption("Review and edit justifications for all competencies (scored and unscored)")
    
    # Group items by competency area for better organization
    competency_groups = {}
    for item in items:
        area = item['competency_area']
        if area not in competency_groups:
            competency_groups[area] = []
        competency_groups[area].append(item)
    
    for area, area_items in competency_groups.items():
        st.markdown(f"**{area}**")
        
        for item in area_items:
            item_id = item['id']
            current_score = st.session_state.scores.get(item_id)
            
            # Show all competencies, indicate scoring status
            if current_score is not None:
                st.markdown(f"**{item['code']}: {item['title']}** (Level {current_score} ✅)")
            else:
                st.markdown(f"**{item['code']}: {item['title']}** (Not scored ⏸️)")
            
            # Justification text area for all items
            current_justification = st.session_state.justifications.get(item_id, "")
            justification = st.text_area(
                f"Justification for {item['code']}",
                value=current_justification,
                height=100,
                placeholder="Enter justification here... (AI-generated justifications appear automatically when you score items above)" if current_score is None else "Edit the justification as needed...",
                key=f"edit_justification_{item_id}",
                help="Edit the AI-generated justification or write your own"
            )
            
            # Update session state
            if justification.strip():
                st.session_state.justifications[item_id] = justification
            elif item_id in st.session_state.justifications and not justification.strip():
                # Remove empty justifications
                del st.session_state.justifications[item_id]
            
            # Individual AI generation as fallback (only for scored items or if requested)
            col1, col2 = st.columns([2, 1])
            with col1:
                if openai_service.is_enabled() and not st.session_state.justifications.get(item_id, "").strip():
                    if current_score is not None:
                        if st.button(f"🤖 Generate Individual Justification", key=f"individual_ai_{item_id}"):
                            with st.spinner(f"Generating justification for {item['code']}..."):
                                try:
                                    ai_justification = openai_service.generate_justification(
                                        item, current_score, student_name, observation_notes
                                    )
                                    st.session_state.justifications[item_id] = ai_justification
                                    st.success("Individual justification generated!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Failed to generate justification: {str(e)}")
                    else:
                        st.info("💡 Score this competency above to enable individual AI justification generation")
            
            with col2:
                if current_score is not None:
                    st.success(f"Scored: Level {current_score}")
                else:
                    st.warning("Not scored")
            
            st.divider()
    
    # STEP 7: Professional Dispositions (Field Evaluation Only)
    if rubric_type == "field_evaluation":
        st.subheader("🌟 Step 7: Professional Dispositions (Supervisor Manual Assessment)")
        st.caption("Supervisors evaluate dispositions based on observations across multiple interactions and timeframes, not limited to a single lesson.")
        
        # Add context about manual assessment
        st.info("""
        **Professional Dispositions Assessment:**
        • ⏰ **Broader Time Scope**: Based on multiple observations, conferences, and interactions over time
        • 👨‍🏫 **Supervisor Assessment**: Manual evaluation by supervisor (no AI assistance)  
        • 📝 **Feedback Required**: Provide specific comments and suggestions for growth
        • ⭐ **Completion Requirement**: All dispositions must score Level 3+ to complete evaluation
        """)
        
        st.markdown("**Score Each Disposition (Level 1-4) and Provide Feedback**")
        
        all_dispositions_scored = True
        
        for disposition in dispositions:
            disp_id = disposition['id']
            current_score = st.session_state.disposition_scores.get(disp_id)
            current_comment = st.session_state.disposition_comments.get(disp_id, "")
            
            # Create header for each disposition
            st.markdown(f"**{disposition['name']}**")
            st.caption(disposition['description'])
            
            # Create scoring and comment interface for each disposition  
            col1, col2 = st.columns([1, 2])
            
            with col1:
                score = st.selectbox(
                    f"Score",
                    options=[None, 1, 2, 3, 4],
                    index=0 if current_score is None else current_score,
                    format_func=lambda x: "Select..." if x is None else f"Level {x} - {get_disposition_level_name(x)}",
                    key=f"disposition_select_{disp_id}",
                    help=f"Select score level for {disposition['name']}"
                )
                
                if score is not None:
                    st.session_state.disposition_scores[disp_id] = score
                else:
                    all_dispositions_scored = False
            
            with col2:
                comment = st.text_area(
                    "Feedback & Suggestions",
                    value=current_comment,
                    height=100,
                    placeholder="Provide specific feedback, observations, and suggestions for professional growth...",
                    key=f"disposition_comment_{disp_id}",
                    help="Enter detailed feedback based on your observations across multiple interactions",
                    max_chars=1000
                )
                
                # Update session state for comments
                st.session_state.disposition_comments[disp_id] = comment
                
                # Character count
                st.caption(f"{len(comment)}/1000 characters")
            
            # Show selected score description and color coding
            display_score = score if score is not None else current_score
            if display_score is not None:
                score_desc = get_disposition_level_name(display_score)
                if display_score >= 3:
                    st.success(f"**Level {display_score}:** {score_desc}")
                elif display_score == 2:
                    st.warning(f"**Level {display_score}:** {score_desc} (Level 3+ required)")
                else:
                    st.warning(f"**Level {display_score}:** {score_desc} (Level 3+ required)")
            else:
                # Show warning for unscored disposition
                st.warning(f"⏸️ **Not yet scored** - {disposition['name']} requires a score level to complete the evaluation")
            
            st.divider()
    
    # AI Analysis
    if openai_service.is_enabled() and st.session_state.scores:
        st.subheader("🤖 Overall Performance Analysis")
        st.caption("AI analysis focused on specific areas needing improvement and actionable guidance for growth")
        
        # Show preview of areas needing attention
        level_1_items = [item_id for item_id, score in st.session_state.scores.items() if score == 1]
        low_dispositions = []
        if rubric_type == "field_evaluation":
            low_dispositions = [disp_id for disp_id, score in st.session_state.disposition_scores.items() if score < 3]
        
        if level_1_items or low_dispositions:
            warning_msg = f"⚠️ **Areas Requiring Attention**: {len(level_1_items)} competencies at Level 1"
            if low_dispositions:
                warning_msg += f", {len(low_dispositions)} dispositions below Level 3"
            st.warning(warning_msg)
        else:
            st.success("✅ **All areas meeting minimum requirements** - Analysis will focus on strengths and growth opportunities")
        
        if st.button("Generate Targeted Improvement Analysis"):
            with st.spinner("Analyzing specific areas needing improvement..."):
                try:
                    # Enhanced analysis that focuses on specific improvement areas
                    analysis = openai_service.analyze_evaluation(
                        st.session_state.scores,
                        st.session_state.justifications,
                        st.session_state.disposition_scores,
                        rubric_type
                    )
                    
                    st.success("**Targeted Performance Analysis:**")
                    st.info(analysis)
                    
                    # Updated guidance reflecting new approach
                    st.markdown("""
                    **How to use this analysis:**
                    • 🎯 **Focus on Level 1 areas**: Students must achieve Level 2+ in ALL competencies to pass
                    • 📝 **Use specific improvement steps**: Provide targeted guidance for moving from Level 1 to Level 2
                    • 🗣️ **Conference planning**: Address specific concerns rather than overall averages
                    • 📈 **Track progress**: Monitor improvement in identified growth areas
                    • 💪 **Leverage strengths**: Use Level 2-3 areas to support growth in struggling competencies
                    """)
                    
                except Exception as e:
                    st.error(f"AI analysis failed: {str(e)}")
    
    # Save buttons
    st.subheader("Save Evaluation")
    
    # Check for completion before saving
    missing_competency_scores = len(items) - len([s for s in st.session_state.scores.values() if s is not None])
    missing_disposition_scores = 0
    if rubric_type == "field_evaluation":
        missing_disposition_scores = len(dispositions) - len([s for s in st.session_state.disposition_scores.values() if s is not None])
    
    if missing_competency_scores > 0 or missing_disposition_scores > 0:
        warning_msg = "⚠️ **Incomplete Evaluation Warning:**\n"
        if missing_competency_scores > 0:
            warning_msg += f"\n• {missing_competency_scores} competencies still need scores"
        if missing_disposition_scores > 0:
            warning_msg += f"\n• {missing_disposition_scores} professional dispositions still need scores"
        warning_msg += "\n\n*You can save as draft with missing scores, but completion requires all items to be scored.*"
        st.warning(warning_msg)
    else:
        if rubric_type == "field_evaluation":
            st.success("✅ **Evaluation is complete!** All competencies and dispositions have been scored.")
        else:
            st.success("✅ **Evaluation is complete!** All competencies have been scored.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 Save as Draft"):
            evaluation = {
                'id': str(uuid.uuid4()),
                'student_name': student_name,
                'evaluator_name': evaluator_name,
                'evaluator_role': evaluator_role,
                'rubric_type': rubric_type,
                'evaluated_items_count': len(items),  # Track how many items this role evaluated
                'scores': st.session_state.scores,
                'justifications': st.session_state.justifications,
                'disposition_scores': st.session_state.disposition_scores if rubric_type == "field_evaluation" else {},
                'disposition_comments': st.session_state.disposition_comments if rubric_type == "field_evaluation" else {},
                'total_score': total_score,
                'status': 'draft',
                'created_at': datetime.now().isoformat(),
                'lesson_plan_provided': st.session_state.lesson_plan_analysis is not None,
                'lesson_plan_method': input_method if 'input_method' in locals() else 'unknown',
                'ai_analyses': st.session_state.get('ai_analyses', {})
            }
            save_evaluation(evaluation)
            st.success("Evaluation saved as draft!")
    
    with col2:
        if st.button("✅ Complete Evaluation"):
            # Validation
            if rubric_type == "field_evaluation":
                errors = validate_evaluation(
                    st.session_state.scores,
                    st.session_state.justifications,
                    st.session_state.disposition_scores,
                    items,
                    dispositions
                )
            else:
                # For STER, validate without dispositions
                errors = validate_evaluation(
                    st.session_state.scores,
                    st.session_state.justifications,
                    {},  # Empty dispositions for STER
                    items,
                    []   # Empty dispositions list for STER
                )
            
            if errors:
                st.warning("⚠️ **Evaluation has issues:**")
                for error in errors:
                    st.error(error)
                st.info("The evaluation will be saved with a 'needs_improvement' status.")
            
            # Save evaluation regardless of validation errors
            evaluation = {
                'id': str(uuid.uuid4()),
                'student_name': student_name,
                'evaluator_name': evaluator_name,
                'evaluator_role': evaluator_role,
                'rubric_type': rubric_type,
                'scores': st.session_state.scores,
                'justifications': st.session_state.justifications,
                'disposition_scores': st.session_state.disposition_scores,
                'disposition_comments': st.session_state.disposition_comments,
                'total_score': total_score,
                'status': 'needs_improvement' if errors else 'completed',
                'validation_errors': errors if errors else [],
                'created_at': datetime.now().isoformat(),
                'completed_at': datetime.now().isoformat(),
                'lesson_plan_provided': st.session_state.lesson_plan_analysis is not None,
                'lesson_plan_method': input_method if 'input_method' in locals() else 'unknown',
                'ai_analyses': st.session_state.get('ai_analyses', {})
            }
            save_evaluation(evaluation)
            
            if errors:
                st.warning("🎯 **Evaluation saved with 'needs improvement' status**")
                st.caption("The student teacher requires additional support in the identified areas.")
            else:
                st.success("🎉 Evaluation completed successfully!")
            
            # Add PDF export button for all evaluations (regardless of status)
            st.markdown("---")
            st.subheader("📄 Download Your Evaluation Report")
            col1_pdf, col2_pdf = st.columns(2)
            
            with col1_pdf:
                # Prepare data for PDF generation
                pdf_data = {
                        'rubric_type': rubric_type,
                        'student_name': student_name,
                        'evaluator_name': evaluator_name,
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'school': st.session_state.get('school_name', 'N/A'),
                        'subject': st.session_state.get('subject_grade', 'N/A'),
                        'is_formative': True,  # TODO: Add formative/summative selection
                        'competency_scores': [],
                        'total_items': len(items),
                        'meeting_expectations': sum(1 for score in st.session_state.scores.values() if score >= 3),
                        'areas_for_growth': sum(1 for score in st.session_state.scores.values() if score < 3)
                }
                
                # Add competency scores
                for item_key, score in st.session_state.scores.items():
                    item = next((i for i in items if i['key'] == item_key), None)
                    if item:
                        pdf_data['competency_scores'].append({
                                'competency': item['item'],
                                'score': score,
                                'justification': st.session_state.justifications.get(item_key, '')
                        })
                
                # Add dispositions for field evaluations
                if rubric_type == 'field_evaluation' and st.session_state.disposition_scores:
                    pdf_data['dispositions'] = []
                    for disp_key, score in st.session_state.disposition_scores.items():
                        disp = next((d for d in dispositions if d['key'] == disp_key), None)
                        if disp:
                            pdf_data['dispositions'].append({
                                    'disposition': disp['disposition'],
                                    'score': score,
                                    'notes': st.session_state.disposition_comments.get(disp_key, '')
                            })
                
                # Add AI analysis if available
                if hasattr(st.session_state, 'ai_analyses') and st.session_state.ai_analyses:
                    # Collect all AI analyses
                    all_analyses = []
                    strengths = []
                    areas_for_growth = []
                    
                    for item_id, analysis in st.session_state.ai_analyses.items():
                        if analysis and isinstance(analysis, str):
                            # Get the item name for context
                            item = next((i for i in items if i.get('key', i.get('id')) == item_id), None)
                            if item:
                                item_name = f"{item['code']}: {item['item']}"
                                # Add the analysis with context
                                all_analyses.append(f"{item_name}\n{analysis}")
                                
                                # Extract strengths (look for positive indicators)
                                if any(word in analysis.lower() for word in ['strong', 'excellent', 'effective', 'well', 'good', 'demonstrates']):
                                    strengths.append(f"{item['code']}: {analysis[:150]}...")
                                
                                # Extract areas for growth (look for improvement indicators)
                                if any(word in analysis.lower() for word in ['improve', 'develop', 'consider', 'could', 'should', 'needs']):
                                    areas_for_growth.append(f"{item['code']}: {analysis[:150]}...")
                    
                    pdf_data['ai_analysis'] = {
                        'strengths': strengths[:5],  # Limit to top 5
                        'areas_for_growth': areas_for_growth[:5],  # Limit to top 5
                        'recommendations': [],  # Could be extracted from overall analysis
                        'full_analyses': all_analyses  # Include all analyses
                    }
                
                # Generate PDF
                try:
                    pdf_bytes = pdf_service.generate_evaluation_pdf(pdf_data)
                    
                    # Create filename
                    filename = f"{student_name.replace(' ', '_')}_{rubric_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                    
                    st.download_button(
                            label="📄 Download Evaluation Report (PDF)",
                            data=pdf_bytes,
                            file_name=filename,
                            mime="application/pdf",
                            help="Download the complete evaluation report as a PDF file"
                    )
                except Exception as e:
                    st.error(f"Error generating PDF: {str(e)}")
            
            with col2_pdf:
                st.info("💡 **Tip**: Download the PDF report for your records or to share with the student teacher.")
            
            # Show a message about refreshing
            st.info("🔄 To create another evaluation, refresh the page or click 'New Evaluation' in the sidebar.")
                
                # TODO: Add session clearing logic after user confirms they've downloaded the PDF
                # for key in ['scores', 'justifications', 'disposition_scores', 'disposition_comments', 'ai_analyses']:
                #     if key in st.session_state:
                #         del st.session_state[key]

def show_test_data():
    """Test data generation and management"""
    st.header("🧪 Synthetic Test Data")
    
    st.info("Generate synthetic evaluation data for testing and demonstration purposes.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        num_evaluations = st.number_input("Number of evaluations to generate", 1, 100, 10)
        rubric_type = st.selectbox("Rubric type", ["field_evaluation", "ster", "both"])
    
    with col2:
        score_distribution = st.selectbox(
            "Score distribution",
            ["random", "high_performing", "low_performing", "mixed"]
        )
    
    if st.button("Generate Synthetic Data"):
        with st.spinner("Generating synthetic evaluations..."):
            synthetic_data = generate_synthetic_evaluations(
                count=num_evaluations,
                rubric_type=rubric_type,
                score_distribution=score_distribution
            )
            
            st.success(f"Generated {len(synthetic_data)} synthetic evaluations!")
            
            # Save to storage
            for evaluation in synthetic_data:
                save_evaluation(evaluation)
            
            # Show preview
            st.subheader("Preview Generated Data")
            df = pd.DataFrame(synthetic_data)
            st.dataframe(df[['student_name', 'evaluator_name', 'rubric_type', 'total_score', 'status']])
    
    # Show current test data
    evaluations = load_evaluations()
    test_evaluations = [e for e in evaluations if e.get('is_synthetic', False)]
    
    if test_evaluations:
        st.subheader(f"Current Test Data ({len(test_evaluations)} evaluations)")
        
        # Show summary of test data
        col1, col2, col3 = st.columns(3)
        with col1:
            field_count = len([e for e in test_evaluations if e.get('rubric_type') == 'field_evaluation'])
            st.metric("Field Evaluations", field_count)
        with col2:
            ster_count = len([e for e in test_evaluations if e.get('rubric_type') == 'ster'])
            st.metric("STER Evaluations", ster_count)
        with col3:
            lesson_plan_count = len([e for e in test_evaluations if e.get('lesson_plan')])
            st.metric("With Lesson Plans", lesson_plan_count)
        
        # Preview test data
        if st.checkbox("📋 Show Test Data Preview"):
            preview_df = pd.DataFrame(test_evaluations)
            if not preview_df.empty:
                display_columns = ['student_name', 'subject_area', 'grade_levels', 'school_name', 'rubric_type', 'total_score', 'status']
                available_columns = [col for col in display_columns if col in preview_df.columns]
                st.dataframe(
                    preview_df[available_columns],
                    use_container_width=True,
                    hide_index=True
                )
        
        # Management options
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear All Test Data", type="secondary"):
                if 'confirm_delete' not in st.session_state:
                    st.session_state.confirm_delete = False
                
                if not st.session_state.confirm_delete:
                    st.session_state.confirm_delete = True
                    st.warning("⚠️ Click again to confirm deletion of all test data")
                    st.rerun()
                else:
                    # Delete all synthetic data
                    real_evaluations = [e for e in evaluations if not e.get('is_synthetic', False)]
                    
                    # Save only real evaluations
                    from utils.storage import EVALUATIONS_FILE, ensure_storage_dir
                    ensure_storage_dir()
                    with open(EVALUATIONS_FILE, 'w', encoding='utf-8') as f:
                        json.dump(real_evaluations, f, indent=2, ensure_ascii=False)
                    
                    st.success(f"✅ Deleted {len(test_evaluations)} test evaluations")
                    st.session_state.confirm_delete = False
                    st.rerun()
        
        with col2:
            if st.button("🔄 Regenerate Test Data"):
                # Clear existing and generate new
                real_evaluations = [e for e in evaluations if not e.get('is_synthetic', False)]
                
                # Generate new synthetic data with same settings as last generation
                new_synthetic_data = generate_synthetic_evaluations(
                    count=10,
                    rubric_type="both",
                    score_distribution="mixed"
                )
                
                # Save combined data
                all_evaluations = real_evaluations + new_synthetic_data
                from utils.storage import EVALUATIONS_FILE, ensure_storage_dir
                ensure_storage_dir()
                with open(EVALUATIONS_FILE, 'w', encoding='utf-8') as f:
                    json.dump(all_evaluations, f, indent=2, ensure_ascii=False)
                
                st.success(f"✅ Regenerated {len(new_synthetic_data)} test evaluations")
                st.rerun()
    
    else:
        st.info("No test data found. Generate some synthetic data to get started!")
        
        # Quick generate button
        if st.button("🚀 Quick Generate (10 Mixed Evaluations)", type="primary"):
            # Clear any pending confirmations
            if 'confirm_delete' in st.session_state:
                del st.session_state.confirm_delete
            with st.spinner("Generating quick test data..."):
                synthetic_data = generate_synthetic_evaluations(
                    count=10,
                    rubric_type="both",
                    score_distribution="mixed"
                )
                
                # Save to storage
                for evaluation in synthetic_data:
                    save_evaluation(evaluation)
                
                st.success(f"✅ Generated {len(synthetic_data)} test evaluations!")
                st.rerun()

def show_settings():
    """Settings and configuration"""
    st.header("⚙️ Settings")
    
    # OpenAI Configuration
    st.subheader("🤖 AI Configuration")
    
    # Show current model status
    current_model_display = openai_service.model if openai_service else os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
    st.info(f"🎯 Currently using model: **{current_model_display}**")
    
    # Initialize session state for API key
    if 'api_key' not in st.session_state:
        st.session_state.api_key = os.getenv('OPENAI_API_KEY', '')
    
    # Check current API key status
    current_key = os.getenv('OPENAI_API_KEY', '') or st.session_state.api_key
    
    if current_key:
        st.success("✅ API key is configured! AI features are available.")
        st.info(f"Using API key: {current_key[:7]}{'*' * 20}{current_key[-4:]}")
        
        if st.button("🔄 Update API Key"):
            st.session_state.show_api_input = True
    else:
        st.warning("⚠️ No API key configured. AI features are disabled.")
        st.session_state.show_api_input = True
    
    # Show API key input if needed
    if st.session_state.get('show_api_input', False) or not current_key:
        api_key = st.text_input(
            "OpenAI API Key",
            value=st.session_state.api_key,
            type="password",
            help="Your OpenAI API key for AI-powered features",
            placeholder="Enter your OpenAI API key"
        )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("💾 Save API Key"):
                if api_key.strip():
                    os.environ['OPENAI_API_KEY'] = api_key.strip()
                    st.session_state.api_key = api_key.strip()
                    st.session_state.show_api_input = False
                    st.success("API key saved for this session!")
                    st.rerun()
                else:
                    st.error("Please enter a valid API key")
        
        with col2:
            if st.button("❌ Cancel"):
                st.session_state.show_api_input = False
                st.rerun()
        
        st.caption("💡 **Note**: API key is saved for this session only. Set OPENAI_API_KEY environment variable for permanent storage.")
    
    # Get current model from OpenAI service
    current_model = openai_service.model if openai_service else os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
    
    # Create model options with current model first
    model_options = ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]
    if current_model in model_options:
        model_options.remove(current_model)
        model_options.insert(0, current_model)
    
    model = st.selectbox(
        "OpenAI Model",
        model_options,
        index=0,  # Select the current model
        help=f"Currently using: {current_model}. Choose a different model to override for this session."
    )
    
    # App Configuration
    st.subheader("📱 Application Settings")
    
    theme = st.selectbox("Theme", ["light", "dark", "auto"])
    
    # Data Management
    st.subheader("💾 Data Management")
    
    if st.button("Clear All Data"):
        if st.checkbox("I understand this will delete all evaluations"):
            # Implementation needed
            st.warning("Clear data functionality not implemented yet")
    
    # About
    st.subheader("ℹ️ About AI-STER")
    st.write("""
    **AI-STER** (AI-powered Student Teaching Evaluation Rubric) is a comprehensive evaluation system 
    for student teachers, aligned with USBE standards and enhanced with AI capabilities.
    
    - **Version:** 1.0.0
    - **USBE Compliance:** July 2024 standards
    - **AI Features:** OpenAI-powered evaluation assistance
    """)

def get_level_name(level) -> str:
    """Get the name for a scoring level"""
    if level == "not_observed":
        return "Not Observed"
    elif isinstance(level, int):
        names = {
            0: "Does not demonstrate",
            1: "Approaching", 
            2: "Demonstrates",
            3: "Exceeds"
        }
        return names.get(level, "Unknown")
    else:
        return "Unknown"

def get_disposition_level_name(level: int) -> str:
    """Get the name for a disposition scoring level"""
    names = {
        1: "Does not demonstrate disposition",
        2: "Is approaching disposition at expected level", 
        3: "Demonstrates disposition at expected level",
        4: "Exceeds expectations"
    }
    return names.get(level, "Unknown")

if __name__ == "__main__":
    main() 