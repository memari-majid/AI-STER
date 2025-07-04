# Phase 1 Implementation Plan
Immediate Actions for Core Functionality Enhancement

## Week 1: AI Justification Generation

### Day 1-2: Enhance Prompt Engineering

#### Update `analyze_observation_notes()` in `app.py`
```python
def analyze_observation_notes_with_justification(notes, lesson_plan, competency):
    """Generate AI justification for specific competency"""
    
    prompt = f"""
    As an expert education evaluator, analyze the following observation notes 
    and lesson plan to generate a detailed justification for the {competency} competency.
    
    Observation Notes:
    {notes}
    
    Lesson Plan:
    {lesson_plan}
    
    Generate a professional justification that:
    1. Cites specific evidence from the observation
    2. Connects observed behaviors to the competency criteria
    3. Provides concrete examples
    4. Explains why the performance level is appropriate
    5. Suggests areas for improvement if applicable
    
    Justification (150-200 words):
    """
    
    client = anthropic.Client(api_key=st.secrets["ANTHROPIC_API_KEY"])
    response = client.completions.create(
        model="claude-2",
        prompt=prompt,
        max_tokens=300,
        temperature=0.7
    )
    
    return response.completion
```

### Day 3-4: Update UI for Justification Display

#### Add to evaluation section in `app.py`
```python
def render_competency_with_justification(competency_name, competency_id):
    """Render competency evaluation with AI justification"""
    
    st.subheader(f"📋 {competency_name}")
    
    # Generate AI justification
    if st.button(f"Generate AI Justification", key=f"gen_{competency_id}"):
        with st.spinner("AI is analyzing..."):
            justification = analyze_observation_notes_with_justification(
                st.session_state.get('observation_notes', ''),
                st.session_state.get('lesson_plan_text', ''),
                competency_name
            )
            st.session_state[f'justification_{competency_id}'] = justification
    
    # Display and allow editing
    col1, col2 = st.columns([3, 1])
    
    with col1:
        justification_text = st.text_area(
            "Evaluation Justification",
            value=st.session_state.get(f'justification_{competency_id}', ''),
            height=150,
            key=f"just_text_{competency_id}",
            help="Review and edit the AI-generated justification as needed"
        )
    
    with col2:
        score = st.select_slider(
            "Score",
            options=[0, 1, 2, 3],
            format_func=lambda x: f"Level {x}",
            key=f"score_{competency_id}"
        )
        
        # Visual indicator for score-justification alignment
        if justification_text and score:
            sentiment = analyze_justification_sentiment(justification_text)
            expected_score = map_sentiment_to_score(sentiment)
            
            if abs(score - expected_score) > 1:
                st.warning("⚠️ Score may not align with justification")
    
    return score, justification_text
```

### Day 5: Session State Management

#### Add justification storage
```python
# Initialize session state for justifications
def init_justification_state():
    """Initialize session state for justifications"""
    if 'justifications' not in st.session_state:
        st.session_state.justifications = {}
    
    for competency in TEACHING_COMPETENCIES:
        key = f'justification_{competency}'
        if key not in st.session_state:
            st.session_state[key] = ''

# Save justifications with evaluation
def save_evaluation_with_justifications():
    """Save evaluation data including justifications"""
    evaluation_data = {
        'timestamp': datetime.now().isoformat(),
        'student_name': st.session_state.get('student_name'),
        'scores': {},
        'justifications': {}
    }
    
    for competency in TEACHING_COMPETENCIES:
        evaluation_data['scores'][competency] = st.session_state.get(f'score_{competency}', 0)
        evaluation_data['justifications'][competency] = st.session_state.get(f'justification_{competency}', '')
    
    # Save to database/file
    save_to_database(evaluation_data)
```

## Week 2: Disposition Comments & Rubric Link

### Day 6-7: Disposition Comment Boxes

#### Update disposition rendering in `app.py`
```python
def render_disposition_with_feedback():
    """Render professional dispositions with comment boxes"""
    
    st.header("Professional Dispositions")
    
    dispositions_data = []
    
    for idx, (disposition, description) in enumerate(PROFESSIONAL_DISPOSITIONS.items(), 1):
        st.markdown(f"### {idx}. {disposition}")
        st.caption(description)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            score = st.select_slider(
                "Score",
                options=[1, 2, 3, 4],
                format_func=get_disposition_level_name,
                key=f"disp_score_{disposition}"
            )
        
        with col2:
            comment = st.text_area(
                "Feedback & Suggestions",
                placeholder="Provide specific feedback for improvement...",
                height=100,
                max_chars=500,
                key=f"disp_comment_{disposition}"
            )
            
            # Character count
            st.caption(f"{len(comment)}/500 characters")
        
        # Auto-save to session state
        st.session_state[f'disposition_{disposition}_score'] = score
        st.session_state[f'disposition_{disposition}_comment'] = comment
        
        dispositions_data.append({
            'disposition': disposition,
            'score': score,
            'comment': comment
        })
        
        st.divider()
    
    return dispositions_data
```

### Day 8-9: STIR Rubric Integration

#### Add rubric modal
```python
def show_rubric_modal():
    """Display STIR rubric in a modal"""
    
    # Add to sidebar or header
    if st.sidebar.button("📖 View STIR Rubric", type="primary"):
        with st.expander("STIR Evaluation Rubric", expanded=True):
            # Tabs for different sections
            tab1, tab2, tab3 = st.tabs(["Competencies", "Dispositions", "Scoring Guide"])
            
            with tab1:
                st.markdown("""
                ## Teaching Competencies
                
                ### 1. Learner Development
                - **Level 0**: Does not demonstrate understanding of learner development
                - **Level 1**: Shows basic awareness of developmental differences
                - **Level 2**: Applies knowledge of learner development in planning
                - **Level 3**: Consistently adapts instruction for diverse learners
                
                ### 2. Learning Environment
                ...
                """)
            
            with tab2:
                st.markdown("""
                ## Professional Dispositions
                
                ### 1. Professional Demeanor
                - **Level 1**: Does not demonstrate professional behavior
                - **Level 2**: Occasionally demonstrates professionalism
                - **Level 3**: Consistently professional in all interactions
                - **Level 4**: Exemplary professional role model
                ...
                """)
            
            with tab3:
                st.markdown("""
                ## Scoring Guidelines
                
                - **Formative Evaluations**: Focus on growth and improvement
                - **Summative Evaluations**: Comprehensive assessment of readiness
                - **Minimum Scores**: Level 2 required for student teaching completion
                """)
            
            # PDF download option
            if st.button("📥 Download Rubric PDF"):
                pdf_path = "resources/STIR_Rubric_2024.pdf"
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="Download PDF",
                        data=pdf_file.read(),
                        file_name="STIR_Rubric.pdf",
                        mime="application/pdf"
                    )
```

### Day 10: Optional Lesson Plan Upload

#### Update file upload logic
```python
def handle_lesson_plan_upload():
    """Handle optional lesson plan upload"""
    
    st.header("📄 Lesson Plan (Optional)")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.info("💡 While a lesson plan helps generate better evaluations, you can proceed without one.")
    
    with col2:
        if st.button("Skip Lesson Plan", type="secondary"):
            st.session_state.skip_lesson_plan = True
    
    if not st.session_state.get('skip_lesson_plan', False):
        uploaded_file = st.file_uploader(
            "Upload lesson plan (Optional)",
            type=['pdf', 'docx', 'txt'],
            help="Providing a lesson plan improves AI-generated justifications"
        )
        
        if uploaded_file:
            # Process file
            lesson_plan_text = extract_text_from_file(uploaded_file)
            st.session_state.lesson_plan_text = lesson_plan_text
            st.success("✅ Lesson plan uploaded successfully!")
            
            # Preview
            with st.expander("Preview Lesson Plan"):
                st.text(lesson_plan_text[:500] + "...")
    else:
        st.warning("⚠️ Proceeding without lesson plan. Some AI features may be limited.")
        st.session_state.lesson_plan_text = "No lesson plan provided"
    
    # Analytics tracking
    track_lesson_plan_submission(
        submitted=bool(uploaded_file) if not st.session_state.get('skip_lesson_plan') else False
    )
```

## Week 3-4: Testing & Refinement

### Day 11-15: Integration Testing

#### Test suite for new features
```python
# tests/test_phase1_features.py

def test_ai_justification_generation():
    """Test AI justification generation"""
    test_notes = "Student demonstrated excellent classroom management..."
    test_lesson = "Objective: Students will learn addition..."
    
    justification = analyze_observation_notes_with_justification(
        test_notes, 
        test_lesson, 
        "Classroom Management"
    )
    
    assert len(justification) > 100
    assert "classroom management" in justification.lower()

def test_disposition_comments_storage():
    """Test disposition comment storage"""
    test_comment = "Shows great enthusiasm but needs to work on punctuality"
    
    # Simulate UI interaction
    st.session_state['disposition_Professional_comment'] = test_comment
    
    # Save and retrieve
    saved_data = save_evaluation_with_justifications()
    assert saved_data['dispositions']['Professional']['comment'] == test_comment

def test_optional_lesson_plan():
    """Test proceeding without lesson plan"""
    st.session_state.skip_lesson_plan = True
    
    # Should still allow evaluation
    result = proceed_to_evaluation()
    assert result == True
    assert st.session_state.lesson_plan_text == "No lesson plan provided"
```

### Day 16-18: User Acceptance Testing

#### UAT Checklist
- [ ] AI justifications are relevant and accurate
- [ ] Supervisors can easily edit justifications
- [ ] Disposition comments save properly
- [ ] Rubric is easily accessible
- [ ] System works without lesson plan
- [ ] All features integrate smoothly

### Day 19-20: Documentation & Deployment

#### Update user documentation
```markdown
# New Features Guide

## AI-Powered Justifications
1. Click "Generate AI Justification" for each competency
2. Review the generated text
3. Edit as needed to match your observations
4. Assign score based on justification

## Professional Feedback
- Each disposition now has a comment box
- Use this to provide specific, actionable feedback
- 500 character limit ensures concise communication

## STIR Rubric Access
- Click the "View STIR Rubric" button in sidebar
- Reference while completing evaluations
- Download PDF for offline use

## Optional Lesson Plans
- Upload if available for better AI assistance
- Click "Skip" to proceed without
- System tracks submission rates for reporting
```

## Success Criteria

### Metrics to Track
1. **AI Justification Usage**
   - % of evaluations using AI generation
   - Average editing time per justification
   - Supervisor satisfaction ratings

2. **Disposition Feedback Quality**
   - Average comment length
   - % of dispositions with comments
   - Student feedback on usefulness

3. **System Performance**
   - Page load times < 2 seconds
   - AI generation time < 5 seconds
   - Zero data loss incidents

### Weekly Progress Review
- Monday: Team standup and week planning
- Wednesday: Mid-week progress check
- Friday: Demo and stakeholder feedback

## Next Steps

After Phase 1 completion:
1. Gather user feedback
2. Address any critical issues
3. Begin Phase 2 planning
4. Prepare progress report for client

This plan provides a clear roadmap for implementing the highest priority features from the client feedback in the first phase. 