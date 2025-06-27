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
        st.image("https://via.placeholder.com/200x100/4F46E5/FFFFFF?text=AI-STER", width=200)
        
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
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Evaluations", len(df))
    with col2:
        completed = len(df[df['status'] == 'completed'])
        st.metric("Completed", completed)
    with col3:
        avg_score = df[df['status'] == 'completed']['total_score'].mean() if completed > 0 else 0
        st.metric("Average Score", f"{avg_score:.1f}")
    with col4:
        st.metric("Success Rate", f"{(completed/len(df)*100):.1f}%")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Evaluation Status")
        status_counts = df['status'].value_counts()
        st.bar_chart(status_counts)
    
    with col2:
        st.subheader("Evaluations by Type")
        type_counts = df['rubric_type'].value_counts()
        st.bar_chart(type_counts)
    
    # Recent evaluations table
    st.subheader("Recent Evaluations")
    recent_df = df.sort_values('created_at', ascending=False).head(10)
    
    # Format the display
    display_df = recent_df[['student_name', 'evaluator_name', 'rubric_type', 'status', 'total_score', 'created_at']].copy()
    display_df['created_at'] = pd.to_datetime(display_df['created_at']).dt.strftime('%Y-%m-%d')
    
    st.dataframe(
        display_df,
        column_config={
            "student_name": "Student",
            "evaluator_name": "Evaluator", 
            "rubric_type": "Type",
            "status": "Status",
            "total_score": "Score",
            "created_at": "Date"
        },
        hide_index=True
    )
    
    # Export functionality
    st.subheader("Data Management")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export All Data"):
            export_data = {
                'evaluations': evaluations,
                'export_date': datetime.now().isoformat(),
                'version': '1.0'
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