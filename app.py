import streamlit as st
import pandas as pd
import json
from datetime import datetime, date
import uuid
from typing import Dict, List, Optional
import os

# Import our modules
from data.rubrics import get_field_evaluation_items, get_ster_items, get_professional_dispositions
from data.synthetic import generate_synthetic_evaluations
from services.openai_service import OpenAIService
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
            ["📊 Dashboard", "📝 New Evaluation", "🧪 Test Data", "⚙️ Settings"]
        )
        
        # Quick stats
        evaluations = load_evaluations()
        st.metric("Total Evaluations", len(evaluations))
        st.metric("Completed", len([e for e in evaluations if e.get('status') == 'completed']))
        st.metric("Drafts", len([e for e in evaluations if e.get('status') == 'draft']))
        
        # STIR Rubric Access
        st.divider()
        st.markdown("### 📖 Resources")
        
        # Rubric button
        if st.button("📋 View STIR Rubric", type="primary", use_container_width=True):
            show_rubric_modal()
        
        # Help text
        st.caption("Access the complete STIR evaluation rubric for reference while completing evaluations.")
    
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

@st.cache_data
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

@st.cache_data
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
    
    for disposition in dispositions:
        disp_id = disposition['id']
        score = disposition_scores.get(disp_id, 0)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{disposition['name']}**")
            st.caption(disposition['description'])
        with col2:
            if score >= 3:
                st.success(f"Level {score}")
            else:
                st.error(f"Level {score} (Needs Level 3+)")

def show_evaluation_form():
    """Evaluation form for creating new evaluations"""
    st.header("📝 New Evaluation")
    
    # Evaluation type selection
    rubric_type = st.selectbox(
        "Select Evaluation Type",
        ["field_evaluation", "ster"],
        format_func=lambda x: "Field Evaluation (3-week)" if x == "field_evaluation" else "STER (Final Assessment)"
    )
    
    # Get rubric items
    items = get_field_evaluation_items() if rubric_type == "field_evaluation" else get_ster_items()
    dispositions = get_professional_dispositions()
    
    # Initialize session state for lesson plan analysis
    if 'lesson_plan_analysis' not in st.session_state:
        st.session_state.lesson_plan_analysis = None
    if 'extracted_info' not in st.session_state:
        st.session_state.extracted_info = {}
    
    # STEP 1: Lesson Plan Upload
    st.subheader("📄 Step 1: Upload Lesson Plan (Optional)")
    st.caption("While a lesson plan helps generate better evaluations, you can proceed without one.")
    
    # Add skip option prominently
    col1, col2 = st.columns([3, 1])
    with col1:
        st.info("💡 Providing a lesson plan improves AI-generated justifications and helps extract evaluation context automatically.")
    with col2:
        if st.button("⏭️ Skip Lesson Plan", type="secondary"):
            st.session_state.skip_lesson_plan = True
            st.session_state.lesson_plan_analysis = None
            st.rerun()
    
    # Only show upload options if not skipped
    if not st.session_state.get('skip_lesson_plan', False):
        # Option to use synthetic data or upload real file
        input_method = st.radio(
            "Choose input method:",
            ["📤 Upload File", "🧪 Use Synthetic Data", "✏️ Paste Text"],
            horizontal=True
        )
    
    lesson_plan_text = None
    
    if input_method == "🧪 Use Synthetic Data":
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
    
    # If user skipped lesson plan
    elif st.session_state.get('skip_lesson_plan', False):
        st.warning("⚠️ Proceeding without lesson plan. Some AI features may be limited.")
        lesson_plan_text = None
        # Reset button
        if st.button("📄 Add Lesson Plan", type="primary"):
            st.session_state.skip_lesson_plan = False
            st.rerun()
    
    # Display Extracted Information or Basic Form
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
            'evaluation_date': evaluation_date.isoformat() if hasattr(evaluation_date, 'isoformat') and not isinstance(evaluation_date, tuple) and evaluation_date is not None else str(evaluation_date) if evaluation_date else '',
            'lesson_plan_text': lesson_plan_text,
            'ai_analysis': analysis
        }
    
    # Basic Information (Traditional Form - when no lesson plan or skipped)
    else:
        # Adjust step number based on whether lesson plan was skipped
        step_num = "2" if not st.session_state.get('skip_lesson_plan', False) else "1b"
        st.subheader(f"📋 Step {step_num}: Basic Information")
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
        
        # Store manual information
        st.session_state.extracted_info = {
            'student_name': student_name,
            'subject_area': subject_area,
            'grade_levels': grade_levels,
            'school_name': school_name,
            'class_size': class_size,
            'evaluation_date': evaluation_date.isoformat() if hasattr(evaluation_date, 'isoformat') and not isinstance(evaluation_date, tuple) and evaluation_date is not None else str(evaluation_date) if evaluation_date else '',
            'lesson_plan_text': lesson_plan_text if lesson_plan_text else None,
            'ai_analysis': None
        }
    
    # Evaluator Information - Step 2 or 3 depending on path
    step_num = "3" if st.session_state.lesson_plan_analysis else "2"
    st.subheader(f"👨‍🏫 Step {step_num}: Evaluator Information")
    col1, col2 = st.columns(2)
    with col1:
        evaluator_name = st.text_input("Evaluator Name *", key="evaluator_name")
    with col2:
        evaluator_role = st.selectbox("Evaluator Role", ["supervisor", "cooperating_teacher"])
    
    # Check if we have minimum required information
    if not student_name or not evaluator_name:
        st.warning("Please provide student teacher name and evaluator name to continue.")
        return
    
    # Initialize session state for scores
    if 'scores' not in st.session_state:
        st.session_state.scores = {}
    if 'justifications' not in st.session_state:
        st.session_state.justifications = {}
    if 'disposition_scores' not in st.session_state:
        st.session_state.disposition_scores = {}
    if 'observation_notes' not in st.session_state:
        st.session_state.observation_notes = ""
    
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
    
    # STEP 4: Generate AI Justifications (NEW - moved before scoring)
    st.subheader("🤖 Step 4: Generate AI Justifications")
    st.caption("Generate evidence-based justifications from your observation notes before scoring")
    
    # Initialize justifications in session state if not already present
    if 'justifications' not in st.session_state:
        st.session_state.justifications = {}
    
    # Show AI generation options if observation notes are provided
    if observation_notes.strip():
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            if openai_service.is_enabled():
                if st.button("🤖 Generate All Justifications", type="primary", key="generate_all_justifications"):
                    with st.spinner("Analyzing observation notes and generating justifications..."):
                        try:
                            # Create scores dict with Level 2 as default for justification generation
                            temp_scores = {item['id']: 2 for item in items}  # Default to "meets expectations"
                            
                            bulk_justifications = openai_service.generate_bulk_justifications(
                                items,
                                temp_scores,
                                observation_notes,
                                student_name,
                                rubric_type
                            )
                            
                            # Update session state with generated justifications
                            st.session_state.justifications = bulk_justifications
                            st.success(f"✅ Generated justifications for {len(bulk_justifications)} competencies!")
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"Failed to generate justifications: {str(e)}")
            else:
                st.warning("🤖 AI features disabled. Add OpenAI API key in Settings to enable.")
        
        with col2:
            if st.session_state.justifications:
                if st.button("🔄 Regenerate All", key="regenerate_justifications"):
                    st.session_state.justifications = {}
                    st.rerun()
        
        with col3:
            if st.session_state.justifications:
                st.success(f"✅ {len(st.session_state.justifications)} generated")
    else:
        st.info("📝 Please add observation notes in Step 3 to enable AI justification generation.")
    
    # Display and allow editing of justifications
    if st.session_state.justifications:
        st.subheader("✏️ Review and Edit Justifications")
        st.caption("Review AI-generated justifications and edit as needed. These will guide your scoring decisions.")
        
        # Group items by competency area
        competency_groups = {}
        for item in items:
            area = item['competency_area']
            if area not in competency_groups:
                competency_groups[area] = []
            competency_groups[area].append(item)
        
        for area, area_items in competency_groups.items():
            st.markdown(f"### {area}")
            
            for item in area_items:
                item_id = item['id']
                
                with st.expander(f"{item['code']}: {item['title']}", expanded=True):
                    # Show competency context
                    st.caption(f"*{item['context']}*")
                    
                    # Justification text area
                    current_justification = st.session_state.justifications.get(item_id, "")
                    
                    justification = st.text_area(
                        "Justification",
                        value=current_justification,
                        height=120,
                        key=f"justification_edit_{item_id}",
                        help="Edit the AI-generated justification based on your observations"
                    )
                    
                    # Update justification in session state
                    if justification != current_justification:
                        st.session_state.justifications[item_id] = justification
                    
                    # Option to regenerate individual justification
                    if openai_service.is_enabled():
                        if st.button(f"🔄 Regenerate", key=f"regen_{item_id}"):
                            with st.spinner("Regenerating..."):
                                try:
                                    new_justification = openai_service.generate_justification(
                                        item, 2, student_name, observation_notes
                                    )
                                    st.session_state.justifications[item_id] = new_justification
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Failed: {str(e)}")
            
            st.divider()
    
    # STEP 5: Assessment Scoring (now based on justifications)
    st.subheader("🎯 Step 5: Score Based on Justifications")
    st.caption("Assign scores that align with your justifications for each competency")
    
    # Initialize scores in session state
    if 'scores' not in st.session_state:
        st.session_state.scores = {}
    
    st.markdown("**Score Each Competency (Level 0-3)**")
    
    total_score = 0
    all_items_scored = True
    
    # Group items by competency area for scoring
    competency_groups = {}
    for item in items:
        area = item['competency_area']
        if area not in competency_groups:
            competency_groups[area] = []
        competency_groups[area].append(item)
    
    # Score each competency area
    for area, area_items in competency_groups.items():
        st.markdown(f"**{area}**")
        
        for item in area_items:
            item_id = item['id']
            current_score = st.session_state.scores.get(item_id)
            current_justification = st.session_state.justifications.get(item_id, "")
            
            # Create scoring interface for each item
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"*{item['code']}: {item['title']}*")
                
                # Show justification if available
                if current_justification:
                    st.info(f"**Justification:** {current_justification}")
                else:
                    st.warning("No justification provided - consider generating one first")
            
            with col2:
                score = st.selectbox(
                    f"Score",
                    options=[None, 0, 1, 2, 3],
                    index=0 if current_score is None else current_score + 1,
                    format_func=lambda x: "Select..." if x is None else f"Level {x}",
                    key=f"score_select_{item_id}",
                    help=f"Select score level based on the justification"
                )
                
                if score is not None:
                    st.session_state.scores[item_id] = score
                    total_score += score
                else:
                    all_items_scored = False
            
            # Show score level description
            display_score = score if score is not None else current_score
            if display_score is not None:
                score_desc = item['levels'].get(str(display_score), 'No description available')
                level_name = get_level_name(display_score)
                
                # Color code based on score
                if display_score >= 3:
                    st.success(f"**Level {display_score} - {level_name}:** {score_desc}")
                elif display_score >= 2:
                    st.info(f"**Level {display_score} - {level_name}:** {score_desc}")
                elif display_score >= 1:
                    st.warning(f"**Level {display_score} - {level_name}:** {score_desc}")
                else:
                    st.error(f"**Level {display_score} - {level_name}:** {score_desc}")
                
                # Check alignment between score and justification
                if current_justification and openai_service.is_enabled():
                    # Simple keyword check for alignment
                    justification_lower = current_justification.lower()
                    if display_score == 3 and ("exceeds" not in justification_lower and "exceptional" not in justification_lower):
                        st.warning("⚠️ Score may not align with justification - consider reviewing")
                    elif display_score == 0 and ("does not" not in justification_lower and "lacking" not in justification_lower):
                        st.warning("⚠️ Score may not align with justification - consider reviewing")
        
        st.divider()
    
    # Score Summary
    min_required = len(items) * 2
    scored_items = len([s for s in st.session_state.scores.values() if s is not None])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Items Scored", f"{scored_items}/{len(items)}")
    with col2:
        st.metric("Current Total", total_score)
    with col3:
        st.metric("Maximum Possible", len(items) * 3)
    with col4:
        meets_req = total_score >= min_required and all_items_scored
        st.metric("Meets Requirements", "✅ Yes" if meets_req else "❌ No")
    
    # STEP 6: Professional Dispositions
    st.subheader("🌟 Step 6: Professional Dispositions")
    st.caption("All dispositions must score Level 3 to complete the evaluation. Provide specific feedback for each disposition.")
    
    st.markdown("**Score Each Disposition (Level 1-4)**")
    
    # Initialize disposition comments in session state
    if 'disposition_comments' not in st.session_state:
        st.session_state.disposition_comments = {}
    
    all_dispositions_scored = True
    
    for idx, disposition in enumerate(dispositions, 1):
        disp_id = disposition['id']
        current_score = st.session_state.disposition_scores.get(disp_id)
        current_comment = st.session_state.disposition_comments.get(disp_id, '')
        
        # Section header
        st.markdown(f"### {idx}. {disposition['name']}")
        st.caption(disposition['description'])
        
        # Create scoring and comment interface
        col1, col2 = st.columns([1, 2])
        
        with col1:
            score = st.selectbox(
                f"Score",
                options=[None, 1, 2, 3, 4],
                index=0 if current_score is None else current_score,
                format_func=lambda x: "Select..." if x is None else f"Level {x}",
                key=f"disposition_select_{disp_id}",
                help=f"Select score level for {disposition['name']}"
            )
            
            if score is not None:
                st.session_state.disposition_scores[disp_id] = score
                
                # Show score description with color coding
                score_desc = get_disposition_level_name(score)
                if score >= 3:
                    st.success(f"**{score_desc}**")
                elif score == 2:
                    st.warning(f"**{score_desc}**")
                    st.caption("⚠️ Level 3+ required")
                else:
                    st.error(f"**{score_desc}**")
                    st.caption("⚠️ Level 3+ required")
            else:
                all_dispositions_scored = False
        
        with col2:
            # Comment text area
            comment = st.text_area(
                "Feedback & Suggestions",
                value=current_comment,
                placeholder="Provide specific feedback for improvement...",
                height=100,
                max_chars=500,
                key=f"disposition_comment_{disp_id}",
                help="Provide constructive feedback and specific suggestions for this disposition"
            )
            
            # Update comment in session state
            if comment != current_comment:
                st.session_state.disposition_comments[disp_id] = comment
            
            # Character count
            if comment:
                st.caption(f"{len(comment)}/500 characters")
        
        st.divider()
    
    # AI Analysis
    if openai_service.is_enabled() and st.session_state.scores:
        st.subheader("🤖 AI Analysis")
        if st.button("Generate AI Evaluation Analysis"):
            with st.spinner("Analyzing evaluation..."):
                try:
                    analysis = openai_service.analyze_evaluation(
                        st.session_state.scores,
                        st.session_state.justifications,
                        st.session_state.disposition_scores,
                        rubric_type
                    )
                    st.info(analysis)
                except Exception as e:
                    st.error(f"AI analysis failed: {str(e)}")
    
    # Save buttons
    st.subheader("Save Evaluation")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 Save as Draft"):
            # Get additional context from session state
            extracted_info = st.session_state.get('extracted_info', {})
            
            evaluation = {
                'id': str(uuid.uuid4()),
                'student_name': student_name,
                'evaluator_name': evaluator_name,
                'evaluator_role': evaluator_role,
                'rubric_type': rubric_type,
                'scores': st.session_state.scores,
                'justifications': st.session_state.justifications,
                'disposition_scores': st.session_state.disposition_scores,
                'disposition_comments': st.session_state.get('disposition_comments', {}),
                'observation_notes': st.session_state.get('observation_notes', ''),
                'total_score': total_score,
                'status': 'draft',
                'created_at': datetime.now().isoformat(),
                # Additional context from extracted info
                'subject_area': extracted_info.get('subject_area', ''),
                'grade_levels': extracted_info.get('grade_levels', ''),
                'school_name': extracted_info.get('school_name', ''),
                'lesson_topic': extracted_info.get('lesson_topic', ''),
                'lesson_plan_text': extracted_info.get('lesson_plan_text', None)
            }
            save_evaluation(evaluation)
            st.success("Evaluation saved as draft!")
    
    with col2:
        if st.button("✅ Complete Evaluation"):
            # Validation
            errors = validate_evaluation(
                st.session_state.scores,
                st.session_state.justifications,
                st.session_state.disposition_scores,
                items,
                dispositions
            )
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Get additional context from session state
                extracted_info = st.session_state.get('extracted_info', {})
                
                evaluation = {
                    'id': str(uuid.uuid4()),
                    'student_name': student_name,
                    'evaluator_name': evaluator_name,
                    'evaluator_role': evaluator_role,
                    'rubric_type': rubric_type,
                    'scores': st.session_state.scores,
                    'justifications': st.session_state.justifications,
                    'disposition_scores': st.session_state.disposition_scores,
                    'disposition_comments': st.session_state.get('disposition_comments', {}),
                    'observation_notes': st.session_state.get('observation_notes', ''),
                    'total_score': total_score,
                    'status': 'completed',
                    'created_at': datetime.now().isoformat(),
                    'completed_at': datetime.now().isoformat(),
                    # Additional context from extracted info
                    'subject_area': extracted_info.get('subject_area', ''),
                    'grade_levels': extracted_info.get('grade_levels', ''),
                    'school_name': extracted_info.get('school_name', ''),
                    'lesson_topic': extracted_info.get('lesson_topic', ''),
                    'lesson_plan_text': extracted_info.get('lesson_plan_text', None)
                }
                save_evaluation(evaluation)
                st.success("🎉 Evaluation completed successfully!")
                
                # Clear session state
                for key in ['scores', 'justifications', 'disposition_scores', 'disposition_comments', 'observation_notes']:
                    if key in st.session_state:
                        del st.session_state[key]

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
    
    api_key = st.text_input(
        "OpenAI API Key",
        value=os.getenv('OPENAI_API_KEY', ''),
        type="password",
        help="Your OpenAI API key for AI-powered features"
    )
    
    if api_key:
        os.environ['OPENAI_API_KEY'] = api_key
        st.success("API key configured! AI features are now available.")
    else:
        st.info("Add your OpenAI API key to enable AI features.")
    
    model = st.selectbox(
        "OpenAI Model",
        ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"],
        help="Choose the AI model for evaluation assistance"
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

def get_level_name(level: int) -> str:
    """Get the name for a scoring level"""
    names = {
        0: "Does not demonstrate",
        1: "Approaching", 
        2: "Demonstrates",
        3: "Exceeds"
    }
    return names.get(level, "Unknown")

def get_disposition_level_name(level: int) -> str:
    """Get the name for a disposition scoring level"""
    names = {
        1: "Does not demonstrate disposition",
        2: "Is approaching disposition at expected level", 
        3: "Demonstrates disposition at expected level",
        4: "Exceeds expectations"
    }
    return names.get(level, "Unknown")

@st.dialog("📋 STIR Evaluation Rubric", width="large")
def show_rubric_modal():
    """Display STIR rubric in a modal dialog"""
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["📚 Competencies", "🌟 Dispositions", "📊 Scoring Guide", "📥 Download"])
    
    with tab1:
        st.markdown("## Teaching Competencies")
        st.caption("All competencies are scored on a 0-3 scale")
        
        # Get competency items to display
        from data.rubrics import get_field_evaluation_items
        items = get_field_evaluation_items()
        
        # Group by competency area
        competency_groups = {}
        for item in items:
            area = item['competency_area']
            if area not in competency_groups:
                competency_groups[area] = []
            competency_groups[area].append(item)
        
        for area, area_items in competency_groups.items():
            st.markdown(f"### {area}")
            
            for item in area_items[:3]:  # Show first 3 items as examples
                with st.expander(f"{item['code']}: {item['title']}", expanded=False):
                    st.caption(item['context'])
                    st.markdown("**Scoring Levels:**")
                    for level in range(4):
                        level_desc = item['levels'].get(str(level), 'No description')
                        if level == 0:
                            st.error(f"**Level {level}:** {level_desc}")
                        elif level == 1:
                            st.warning(f"**Level {level}:** {level_desc}")
                        elif level == 2:
                            st.info(f"**Level {level}:** {level_desc}")
                        else:
                            st.success(f"**Level {level}:** {level_desc}")
    
    with tab2:
        st.markdown("## Professional Dispositions")
        st.caption("All dispositions must score Level 3 or higher")
        
        from data.rubrics import get_professional_dispositions
        dispositions = get_professional_dispositions()
        
        for idx, disposition in enumerate(dispositions, 1):
            st.markdown(f"### {idx}. {disposition['name']}")
            st.caption(disposition['description'])
            
            st.markdown("**Scoring Levels:**")
            for level in range(1, 5):
                level_desc = get_disposition_level_name(level)
                if level < 3:
                    st.error(f"**Level {level}:** {level_desc} ❌")
                elif level == 3:
                    st.info(f"**Level {level}:** {level_desc} ✅")
                else:
                    st.success(f"**Level {level}:** {level_desc} ⭐")
            
            st.divider()
    
    with tab3:
        st.markdown("## Scoring Guidelines")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Competency Scoring")
            st.markdown("""
            - **Level 0**: Does not demonstrate competency
            - **Level 1**: Is approaching competency at expected level
            - **Level 2**: Demonstrates competency at expected level
            - **Level 3**: Exceeds expected level of competency
            
            **Minimum Requirements:**
            - Average score of 2.0 or higher
            - No more than 2 scores at Level 0
            """)
        
        with col2:
            st.markdown("### Disposition Scoring")
            st.markdown("""
            - **Level 1**: Does not demonstrate disposition
            - **Level 2**: Is approaching disposition at expected level
            - **Level 3**: Demonstrates disposition at expected level
            - **Level 4**: Exceeds expectations
            
            **Minimum Requirements:**
            - All dispositions must score Level 3 or higher
            - No exceptions allowed
            """)
        
        st.divider()
        
        st.markdown("### Evaluation Types")
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("""
            **Field Evaluation (3-week)**
            - Formative assessment
            - Focus on growth and development
            - Provides feedback for improvement
            """)
        
        with col2:
            st.success("""
            **STER (Final Assessment)**
            - Summative evaluation
            - Comprehensive assessment
            - Determines readiness for teaching
            """)
    
    with tab4:
        st.markdown("## Download Resources")
        
        # Create a sample rubric PDF content (in real implementation, this would be an actual PDF)
        rubric_content = """
STIR Evaluation Rubric - Utah State Board of Education
Version: July 2024

This rubric is designed to evaluate student teachers based on Utah teaching standards.

For the complete rubric document, please visit:
https://www.schools.utah.gov/file/stir-rubric-2024.pdf
        """
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="📥 Download Rubric (PDF)",
                data=rubric_content,
                file_name="STIR_Rubric_2024.pdf",
                mime="application/pdf",
                help="Download the complete STIR rubric as a PDF"
            )
        
        with col2:
            st.link_button(
                "🌐 View Online",
                "https://www.schools.utah.gov/certification/educators",
                help="View the latest rubric on the USBE website"
            )
        
        st.info("💡 **Tip:** Keep the rubric open in another tab while completing evaluations for easy reference.")

if __name__ == "__main__":
    main()          