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
    
    # Basic information
    st.subheader("Basic Information")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        student_name = st.text_input("Student Name *", key="student_name")
    with col2:
        evaluator_name = st.text_input("Evaluator Name *", key="evaluator_name")
    with col3:
        evaluator_role = st.selectbox("Evaluator Role", ["supervisor", "cooperating_teacher"])
    
    if not student_name or not evaluator_name:
        st.warning("Please enter student name and evaluator name to continue.")
        return
    
    # Initialize session state for scores
    if 'scores' not in st.session_state:
        st.session_state.scores = {}
    if 'justifications' not in st.session_state:
        st.session_state.justifications = {}
    if 'disposition_scores' not in st.session_state:
        st.session_state.disposition_scores = {}
    
    # Assessment items
    st.subheader("Assessment Items")
    
    total_score = 0
    min_required = len(items) * 2
    
    for i, item in enumerate(items):
        with st.container():
            st.markdown(f"### {item['code']}: {item['title']}")
            
            # Context and type badges
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.caption(f"**Context:** {item['context']}")
            with col2:
                st.caption(f"**Type:** {item['type']}")
            with col3:
                st.caption(f"**Area:** {item['competency_area']}")
            
            # Scoring buttons
            col1, col2, col3, col4 = st.columns(4)
            
            score_key = f"score_{item['id']}"
            current_score = st.session_state.scores.get(item['id'])
            
            for level in range(4):
                with [col1, col2, col3, col4][level]:
                    if st.button(
                        f"Level {level}\n{get_level_name(level)}",
                        key=f"{score_key}_{level}",
                        type="primary" if current_score == level else "secondary"
                    ):
                        st.session_state.scores[item['id']] = level
                        st.rerun()
            
            # Show selected score and description
            if current_score is not None:
                st.info(f"**Selected: Level {current_score}** - {item['levels'][str(current_score)]}")
                total_score += current_score
            
            # Justification
            justification_key = f"justification_{item['id']}"
            justification = st.text_area(
                f"Justification {('(Required)' if current_score is not None and current_score >= 2 else '')}",
                key=justification_key,
                height=100,
                placeholder="Provide specific examples and evidence to support your score..."
            )
            
            if justification:
                st.session_state.justifications[item['id']] = justification
            
            # AI Assistant
            if openai_service.is_enabled() and current_score is not None:
                if st.button(f"🤖 Generate AI Justification", key=f"ai_{item['id']}"):
                    with st.spinner("Generating AI justification..."):
                        try:
                            ai_justification = openai_service.generate_justification(
                                item, current_score, student_name
                            )
                            st.session_state.justifications[item['id']] = ai_justification
                            st.success("AI justification generated!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"AI generation failed: {str(e)}")
            
            # Example justification
            if 'example_justification' in item:
                with st.expander("View Example Justification (Level 2)"):
                    st.write(item['example_justification'])
            
            st.divider()
    
    # Score summary
    st.subheader("Score Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Total", total_score)
    with col2:
        st.metric("Maximum Possible", len(items) * 3)
    with col3:
        meets_req = total_score >= min_required
        st.metric("Meets Requirements", "✅ Yes" if meets_req else "❌ No")
    
    # Professional Dispositions
    st.subheader("Professional Dispositions")
    st.caption("All dispositions must score Level 3 to complete the evaluation.")
    
    for disposition in dispositions:
        st.markdown(f"**{disposition['name']}**")
        st.caption(disposition['description'])
        
        disp_score = st.select_slider(
            f"Score for {disposition['name']}",
            options=[1, 2, 3, 4],
            format_func=lambda x: f"Level {x}",
            key=f"disp_{disposition['id']}"
        )
        
        st.session_state.disposition_scores[disposition['id']] = disp_score
        
        if disp_score < 3:
            st.warning("Level 3 required for completion")
    
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
            evaluation = {
                'id': str(uuid.uuid4()),
                'student_name': student_name,
                'evaluator_name': evaluator_name,
                'evaluator_role': evaluator_role,
                'rubric_type': rubric_type,
                'scores': st.session_state.scores,
                'justifications': st.session_state.justifications,
                'disposition_scores': st.session_state.disposition_scores,
                'total_score': total_score,
                'status': 'draft',
                'created_at': datetime.now().isoformat()
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
                evaluation = {
                    'id': str(uuid.uuid4()),
                    'student_name': student_name,
                    'evaluator_name': evaluator_name,
                    'evaluator_role': evaluator_role,
                    'rubric_type': rubric_type,
                    'scores': st.session_state.scores,
                    'justifications': st.session_state.justifications,
                    'disposition_scores': st.session_state.disposition_scores,
                    'total_score': total_score,
                    'status': 'completed',
                    'created_at': datetime.now().isoformat(),
                    'completed_at': datetime.now().isoformat()
                }
                save_evaluation(evaluation)
                st.success("🎉 Evaluation completed successfully!")
                
                # Clear session state
                for key in ['scores', 'justifications', 'disposition_scores']:
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
        
        if st.button("🗑️ Clear All Test Data"):
            # This would need implementation in storage module
            st.warning("Test data clearing not implemented yet")

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
        ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
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

if __name__ == "__main__":
    main() 