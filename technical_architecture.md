# AI-STER Technical Architecture
**Updated for June 25, 2025 Client Action Items**

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                  Simplified Frontend Layer                       │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │              Streamlit Web Application                      │ │
│  │  ┌────────────────┐  ┌────────────────┐  ┌───────────────┐ │ │
│  │  │   Evaluation   │  │   Dashboard    │  │  Test Data    │ │ │
│  │  │     Form       │  │   Analytics    │  │  Generator    │ │ │
│  │  │                │  │                │  │               │ │ │
│  │  │ Supervisor-Only│  │ Score Tracking │  │ Synthetic     │ │ │
│  │  │   Interface    │  │ Progress View  │  │ Evaluations   │ │ │
│  │  └────────────────┘  └────────────────┘  └───────────────┘ │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                     Core Business Logic                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Evaluation  │  │   Scoring    │  │  Simplified  │         │
│  │   Service    │  │   Engine     │  │     Export   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │      AI      │  │   Session    │  │  Validation  │         │
│  │ Justification│  │  Management  │  │   Service    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                      Simplified Data Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  JSON Files  │  │    Session   │  │   PDF Export │         │
│  │   Storage    │  │    State     │  │   Generator  │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

## Key Architecture Changes (June 2025)

### 1. **Role Simplification**
```python
# REMOVED: Cooperating Teacher Role Support
# OLD: Dual-role system with role-based filtering
# NEW: University Supervisor focused system

class UserRole:
    SUPERVISOR = "supervisor"
    # REMOVED: COOPERATING_TEACHER = "cooperating_teacher"

def get_evaluation_items(rubric_type):
    """Simplified item retrieval - no role filtering needed"""
    if rubric_type == "field_evaluation":
        return get_field_evaluation_items()
    else:
        return get_ster_items()  # All STER items for supervisors
    # REMOVED: filter_items_by_evaluator_role()
```

### 2. **Enhanced Scoring System**
```python
# NEW: Extended score options including "Not Observed"
class ScoreOption:
    NOT_SELECTED = None
    NOT_OBSERVED = "not_observed"
    LEVEL_0 = 0
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3

def validate_evaluation_scores(scores):
    """Updated validation - 'not_observed' is valid"""
    missing = []
    for item_id, score in scores.items():
        if score is None:  # Only None is invalid
            missing.append(item_id)
    return missing
```

### 3. **Simplified Evaluation Logic**
```python
# NEW: Conditional disposition display
def show_evaluation_form():
    # ... evaluation setup ...
    
    # Simplified role assignment
    evaluator_role = "supervisor"  # Fixed role
    
    # Conditional dispositions based on evaluation type
    if rubric_type == "field_evaluation":
        show_professional_dispositions()  # Include dispositions
    # STER evaluations: No dispositions section
    
    # Combined analysis and scoring interface
    show_combined_analysis_scoring_interface(items)
```

## Updated Component Architecture

### **Evaluation Form Components (Simplified)**

```python
# app.py - Main evaluation form
def show_evaluation_form():
    """Streamlined supervisor-focused evaluation form"""
    
    # Step 1: Lesson Plan (Optional)
    lesson_plan_section()
    
    # Step 2: Basic Information  
    student_evaluator_info()
    
    # Step 3: Observation Notes with AI Analysis Button
    observation_notes_with_ai_button()
    
    # Step 4: Combined Analysis & Scoring Interface
    combined_analysis_scoring_section()
    
    # Step 5: Conditional Dispositions (Field only)
    if rubric_type == "field_evaluation":
        dispositions_section()
    
    # Step 6: Save/Complete with Session Clearing
    save_complete_with_clearing()

def combined_analysis_scoring_section():
    """NEW: Side-by-side analysis and scoring"""
    for item in items:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # AI Analysis Display & Edit
            show_ai_analysis_for_item(item)
            edit_justification_inline(item)
        
        with col2:
            # Scoring Controls
            score_with_enhanced_options(item)
            display_score_description(item)
```

### **Session Management (Enhanced)**

```python
# utils/session.py - NEW: Enhanced session management
class SessionManager:
    @staticmethod
    def clear_evaluation_data():
        """Clear all evaluation-related session data"""
        keys_to_clear = [
            'scores', 'justifications', 'disposition_scores',
            'disposition_comments', 'ai_analyses', 'extracted_info'
        ]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
    
    @staticmethod
    def start_new_evaluation():
        """Initialize new evaluation with clear state"""
        SessionManager.clear_evaluation_data()
        st.success("✅ New evaluation started - previous data cleared")
    
    @staticmethod
    def complete_evaluation(evaluation_data):
        """Complete evaluation and clear session"""
        save_evaluation(evaluation_data)
        SessionManager.clear_evaluation_data()
        st.success("🎉 Evaluation completed - ready for next evaluation")
```

### **Enhanced Scoring Interface**

```python
# components/scoring.py - NEW: Enhanced scoring options
def render_score_selector(item_id, current_score=None):
    """Enhanced score selector with 'Not Observed' option"""
    
    options = [None, "not_observed", 0, 1, 2, 3]
    
    def format_option(score):
        if score is None:
            return "Select score..."
        elif score == "not_observed":
            return "Not Observed - Competency not demonstrated"
        else:
            return f"Level {score} - {get_level_name(score)}"
    
    score = st.selectbox(
        "Score",
        options=options,
        index=get_score_index(current_score),
        format_func=format_option,
        key=f"score_{item_id}"
    )
    
    return score

def validate_scores_with_not_observed(scores):
    """Updated validation allowing 'not_observed' as valid"""
    missing = []
    for item_id, score in scores.items():
        if score is None:  # Only None is invalid
            missing.append(item_id)
    return missing
```

## Updated Data Models

### **Evaluation Data Structure (Simplified)**

```python
# data/models.py
class Evaluation:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.student_name = ""
        self.evaluator_name = ""
        self.evaluator_role = "supervisor"  # Fixed role
        self.rubric_type = ""  # "field_evaluation" or "ster"
        self.scores = {}  # Can include "not_observed" values
        self.justifications = {}
        self.disposition_scores = {}  # Only for field evaluations
        self.disposition_comments = {}  # Only for field evaluations
        self.status = "draft"  # "draft" or "completed"
        self.created_at = datetime.now().isoformat()
        self.completed_at = None

class ScoreValidation:
    @staticmethod
    def is_valid_score(score):
        """Check if score is valid (includes 'not_observed')"""
        return score in [0, 1, 2, 3, "not_observed"]
    
    @staticmethod
    def is_complete_evaluation(scores, rubric_type):
        """Check if evaluation is complete"""
        # All items must have a score (including 'not_observed')
        incomplete_items = [k for k, v in scores.items() if v is None]
        return len(incomplete_items) == 0
```

## UI/UX Improvements Implementation

### **Terminology Updates**
```python
# utils/terminology.py - NEW: Positive terminology
TERMINOLOGY_MAP = {
    "Critical Areas": "Areas for Improvement",
    "critical areas": "areas for improvement",
    "Failed": "Needs Development", 
    "❌ Not Met": "⚠️ Needs Improvement",
    "Red X": "⚠️ Warning Icon"
}

def update_terminology(text):
    """Replace negative terminology with positive alternatives"""
    for old_term, new_term in TERMINOLOGY_MAP.items():
        text = text.replace(old_term, new_term)
    return text
```

### **Visual Stress Reduction**
```python
# components/indicators.py - NEW: Stress-reduced indicators
def show_evaluation_status(meets_requirements):
    """Show status without stressful red X indicators"""
    if meets_requirements:
        st.success("✅ Requirements Met")
    else:
        st.warning("⚠️ Needs Improvement - Some areas require Level 2+")
        # REMOVED: Red X and "FAILED" messaging

def show_competency_status(score):
    """Show individual competency status with neutral colors"""
    if score is None:
        st.info("⏸️ Not yet scored")
    elif score == "not_observed":
        st.info("👁️ Not observed in this session")
    elif score >= 2:
        st.success(f"✅ Level {score}")
    else:
        st.warning(f"⚠️ Level {score} - Consider improvement strategies")
```

## Export and Data Management

### **PDF Export System (NEW)**
```python
# services/export.py - NEW: PDF generation for completed evaluations
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

class PDFExportService:
    @staticmethod
    def generate_evaluation_pdf(evaluation):
        """Generate PDF report for completed evaluation"""
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        # Header
        p.setFont("Helvetica-Bold", 16)
        p.drawString(50, 750, f"AI-STER Evaluation Report")
        
        # Student Information
        p.setFont("Helvetica", 12)
        y_position = 700
        p.drawString(50, y_position, f"Student: {evaluation['student_name']}")
        p.drawString(50, y_position - 20, f"Evaluator: {evaluation['evaluator_name']}")
        p.drawString(50, y_position - 40, f"Date: {evaluation['created_at'][:10]}")
        
        # Scores and Justifications
        y_position = 620
        for item_id, score in evaluation['scores'].items():
            item_title = get_item_title(item_id)
            justification = evaluation['justifications'].get(item_id, '')
            
            p.drawString(50, y_position, f"{item_id}: {format_score_display(score)}")
            y_position -= 20
            
            if justification:
                wrapped_text = wrap_text(justification, 80)
                for line in wrapped_text:
                    p.drawString(70, y_position, line)
                    y_position -= 15
            
            y_position -= 10
        
        p.save()
        buffer.seek(0)
        return buffer

def format_score_display(score):
    """Format score for display in reports"""
    if score == "not_observed":
        return "Not Observed"
    elif isinstance(score, int):
        return f"Level {score}"
    else:
        return "Not Scored"
```

## Implementation Dependencies

### **Phase 1 Dependencies (Week 1-2)**
1. **Score Dropdown Enhancement**
   - Update: `app.py` scoring interface
   - Update: `utils/validation.py` score validation
   - Test: All evaluation workflows

2. **Terminology Updates**  
   - Update: All UI text in `app.py`
   - Update: Status indicators and messages
   - Update: Documentation and help text

3. **Visual Improvements**
   - Update: CSS/styling for status indicators
   - Remove: Red error styling
   - Add: Neutral warning styling

### **Phase 2 Dependencies (Week 2-3)**
1. **Interface Consolidation**
   - Redesign: Evaluation form layout
   - Combine: Analysis and scoring sections
   - Update: Session state management

2. **AI Analysis Button**
   - Add: Prominent analysis trigger button
   - Update: Workflow guidance
   - Improve: User experience flow

### **Phase 3 Dependencies (Week 3-4)**
1. **Role Simplification**
   - Remove: Cooperating teacher logic
   - Update: Item filtering logic
   - Simplify: User interface

2. **Evaluation Type Configuration**
   - Update: Disposition conditional logic
   - Test: Field evaluation workflow
   - Validate: STER evaluation workflow

### **Phase 4 Dependencies (Week 4-5)**
1. **PDF Export**
   - Install: ReportLab library
   - Implement: PDF generation service
   - Add: Download buttons

2. **Session Management**
   - Implement: Clear data functions
   - Update: Save/complete workflows
   - Add: Clear user feedback

## Success Metrics & Testing

### **User Experience Metrics**
- Evaluation completion time reduction: Target 25%
- User error rate reduction: Target 50%
- User satisfaction improvement: Target to 4.5/5
- Support requests reduction: Target 60%

### **Technical Quality Metrics**
- Zero data persistence bugs
- 100% successful PDF generation
- Clear session behavior validation
- Proper evaluation type differentiation

### **Testing Strategy**
1. **Unit Tests**: Each component function
2. **Integration Tests**: Complete evaluation workflows  
3. **User Acceptance Tests**: Real supervisor testing
4. **Performance Tests**: Large evaluation datasets
5. **Accessibility Tests**: Screen reader compatibility

---

**Architecture Updated**: January 2025  
**Next Review**: After Phase 1 completion  
**Maintainer**: AI-STER Development Team