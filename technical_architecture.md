# AI-STER Technical Architecture
Implementation Guide for Client Feedback Features

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend Layer                            │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐         │
│  │  Streamlit  │  │ React Admin  │  │  Email Client  │         │
│  │     App     │  │  Dashboard   │  │   Interface    │         │
│  └─────────────┘  └──────────────┘  └────────────────┘         │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                         API Gateway                              │
│  ┌────────────────────────────────────────────────────┐         │
│  │            FastAPI with Authentication             │         │
│  └────────────────────────────────────────────────────┘         │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                      Business Logic Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Evaluation  │  │   Scoring    │  │    Report    │         │
│  │   Service    │  │   Engine     │  │  Generator   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │      AI      │  │    Email     │  │   Analytics  │         │
│  │ Justification│  │ Distribution │  │   Service    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                        Data Layer                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  PostgreSQL  │  │    Redis     │  │   Vector DB  │         │
│  │   Database   │  │    Cache     │  │  (Pinecone)  │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│  ┌──────────────┐  ┌──────────────┐                            │
│  │  S3 Storage  │  │   Message    │                            │
│  │   (Files)    │  │    Queue     │                            │
│  └──────────────┘  └──────────────┘                            │
└─────────────────────────────────────────────────────────────────┘
```

## Feature Implementation Details

### 1. AI Justification System

#### Components
```python
class AIJustificationService:
    def __init__(self, llm_client, vector_db):
        self.llm = llm_client
        self.vector_db = vector_db
    
    def generate_justification(self, context):
        """Generate AI justification for evaluation scores"""
        # Components:
        # 1. Context extraction
        # 2. Relevant examples retrieval
        # 3. Prompt engineering
        # 4. LLM generation
        # 5. Post-processing
```

#### Database Schema
```sql
-- Justifications table
CREATE TABLE justifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    evaluation_id UUID REFERENCES evaluations(id),
    competency_id VARCHAR(50),
    ai_generated_text TEXT,
    supervisor_edited_text TEXT,
    final_score INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Justification history for audit
CREATE TABLE justification_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    justification_id UUID REFERENCES justifications(id),
    version INTEGER,
    text TEXT,
    edited_by UUID REFERENCES users(id),
    edited_at TIMESTAMP DEFAULT NOW()
);
```

### 2. STER Evaluation Type System

#### State Management
```python
class STEREvaluationType(Enum):
    FORMATIVE_1 = "formative_1"
    FORMATIVE_2 = "formative_2"
    FORMATIVE_3 = "formative_3"
    FORMATIVE_4 = "formative_4"
    SUMMATIVE = "summative"

class EvaluatorRole(Enum):
    SUPERVISOR = "supervisor"           # 19 competencies: LL2-LL7, IC1/IC2, IC3, IC4, IC5/IC6, IC7, IP1-IP8
    COOPERATING_TEACHER = "cooperating_teacher"  # 16 competencies: LL1, CC1-CC8, PR1-PR7

class STERCompetencyArea(Enum):
    LEARNERS_LEARNING = "Learners and Learning"        # 7 items total (LL1=CT, LL2-LL7=Supervisor)
    INSTRUCTIONAL_CLARITY = "Instructional Clarity"    # 5 items (all supervisor, IC1/IC2 and IC5/IC6 combined)
    INSTRUCTIONAL_PRACTICE = "Instructional Practice"  # 8 items (all supervisor)
    CLASSROOM_CLIMATE = "Classroom Climate"            # 8 items (all cooperating teacher)
    PROFESSIONAL_RESPONSIBILITY = "Professional Responsibility"  # 7 items (all cooperating teacher)

class STERTracker:
    def __init__(self, db_session):
        self.db = db_session
    
    def get_items_for_role(self, evaluator_role: EvaluatorRole) -> List[Dict]:
        """Get competency items appropriate for evaluator role"""
        return filter_items_by_evaluator_role(get_ster_items(), evaluator_role.value)
    
    def get_formative_count(self, student_id, ster_type):
        """Count completed formative evaluations by type"""
        
    def is_summative_required(self, student_id):
        """Check if summative evaluation is due based on formative completion"""
        
    def get_role_specific_progress(self, student_id, evaluator_role):
        """Track progress for role-specific competencies"""
```

#### Database Schema
```sql
-- Enhanced evaluations table with role-based STER support
CREATE TABLE evaluations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID REFERENCES students(id),
    evaluator_id UUID REFERENCES users(id),
    evaluator_role VARCHAR(20) CHECK (evaluator_role IN ('supervisor', 'cooperating_teacher')),
    evaluation_type VARCHAR(20) CHECK (evaluation_type IN ('field_evaluation', 'ster')),
    ster_type VARCHAR(20) CHECK (ster_type IN ('formative_1', 'formative_2', 'formative_3', 'formative_4', 'summative')),
    status VARCHAR(20) CHECK (status IN ('draft', 'completed', 'submitted', 'archived')),
    evaluation_date DATE,
    observation_notes TEXT,
    total_items_evaluated INTEGER, -- 19 for supervisor, 16 for cooperating_teacher
    total_score INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    submitted_at TIMESTAMP,
    UNIQUE(student_id, evaluation_date, ster_type, evaluator_role)
);

-- STER competency scores with role tracking
CREATE TABLE ster_competency_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    evaluation_id UUID REFERENCES evaluations(id),
    competency_code VARCHAR(10), -- LL1, LL2, IC1, IP1, CC1, PR1, etc.
    competency_area VARCHAR(50), -- Learners and Learning, Instructional Clarity, etc.
    evaluator_role VARCHAR(20), -- supervisor or cooperating_teacher
    score INTEGER CHECK (score >= 0 AND score <= 3),
    justification TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- STER progress tracking per student
CREATE TABLE ster_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID REFERENCES students(id),
    
    -- Formative evaluation completion tracking
    formative_1_completed BOOLEAN DEFAULT FALSE,
    formative_1_date DATE,
    formative_2_completed BOOLEAN DEFAULT FALSE,
    formative_2_date DATE,
    formative_3_completed BOOLEAN DEFAULT FALSE,
    formative_3_date DATE,
    formative_4_completed BOOLEAN DEFAULT FALSE,
    formative_4_date DATE,
    
    -- Summative eligibility and completion
    summative_eligible BOOLEAN DEFAULT FALSE,
    summative_completed BOOLEAN DEFAULT FALSE,
    summative_date DATE,
    
    -- Role-based completion tracking
    supervisor_evaluations_count INTEGER DEFAULT 0,    -- Track supervisor evaluations
    cooperating_teacher_evaluations_count INTEGER DEFAULT 0, -- Track CT evaluations
    
    last_updated TIMESTAMP DEFAULT NOW()
);

-- Role-based competency mapping
CREATE TABLE ster_competency_roles (
    competency_code VARCHAR(10) PRIMARY KEY,
    competency_title TEXT NOT NULL,
    competency_area VARCHAR(50) NOT NULL,
    evaluator_role VARCHAR(20) NOT NULL CHECK (evaluator_role IN ('supervisor', 'cooperating_teacher')),
    context TEXT, -- Observation, Conference w/MT, etc.
    sort_order INTEGER
);

-- Insert role mappings (19 supervisor + 16 cooperating teacher = 35 total)
INSERT INTO ster_competency_roles VALUES
-- Supervisor Items (19)
('LL2', 'Design learning that builds on learner background knowledge', 'Learners and Learning', 'supervisor', 'Observation', 2),
('LL3', 'Strengthen classroom norms for positive relationships', 'Learners and Learning', 'supervisor', 'Observation', 3),
-- ... (continue with all 35 competencies)
;
```

### 3. Disposition Comments System

#### UI Component
```python
def render_disposition_with_comments(disposition_name, disposition_id):
    """Render disposition slider with comment box"""
    col1, col2 = st.columns([1, 2])
    
    with col1:
        score = st.select_slider(
            f"{disposition_name}",
            options=range(1, 5),
            format_func=get_disposition_level_name
        )
    
    with col2:
        comment = st.text_area(
            "Feedback & Suggestions",
            key=f"comment_{disposition_id}",
            height=100,
            max_chars=500,
            placeholder="Provide specific feedback..."
        )
    
    # Auto-save to session state
    st.session_state[f"disp_{disposition_id}_comment"] = comment
    
    return score, comment
```

#### Database Schema
```sql
-- Disposition comments table
CREATE TABLE disposition_comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    evaluation_id UUID REFERENCES evaluations(id),
    disposition_id VARCHAR(50),
    score INTEGER CHECK (score BETWEEN 1 AND 4),
    comment TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 4. Email Distribution System

#### Email Service Implementation
```python
class EmailDistributionService:
    def __init__(self, email_provider):
        self.provider = email_provider  # SendGrid/AWS SES
        
    async def send_evaluation_report(self, evaluation_id):
        """Send completed evaluation to all stakeholders"""
        # 1. Generate PDF report
        pdf_report = await self.generate_pdf_report(evaluation_id)
        
        # 2. Get recipient list
        recipients = await self.get_recipients(evaluation_id)
        
        # 3. Prepare email content
        email_content = self.prepare_email_content(evaluation_id)
        
        # 4. Send emails
        for recipient in recipients:
            await self.send_email(
                to=recipient.email,
                subject=f"Evaluation Report - {recipient.student_name}",
                content=email_content,
                attachments=[pdf_report]
            )
```

#### Email Templates
```html
<!-- evaluation_complete.html -->
<html>
<body>
    <h2>Student Teaching Evaluation Complete</h2>
    <p>Dear {{ recipient_name }},</p>
    <p>The {{ evaluation_type }} evaluation for {{ student_name }} has been completed.</p>
    
    <h3>Summary:</h3>
    <ul>
        <li>Date: {{ evaluation_date }}</li>
        <li>Supervisor: {{ supervisor_name }}</li>
        <li>Overall Performance: {{ overall_score }}</li>
    </ul>
    
    <p>Please find the detailed evaluation report attached.</p>
</body>
</html>
```

### 5. Data Storage & Knowledge Base

#### Seven-Year Retention Strategy
```python
class DataRetentionManager:
    def __init__(self, db, storage):
        self.db = db
        self.storage = storage
        
    def archive_old_data(self):
        """Archive data older than 7 years"""
        cutoff_date = datetime.now() - timedelta(days=7*365)
        
        # 1. Identify old records
        old_evaluations = self.db.query(Evaluation).filter(
            Evaluation.created_at < cutoff_date
        )
        
        # 2. Export to cold storage
        for evaluation in old_evaluations:
            self.export_to_cold_storage(evaluation)
            
        # 3. Remove from active database
        self.db.query(Evaluation).filter(
            Evaluation.created_at < cutoff_date
        ).update({"archived": True})
```

#### Vector Knowledge Base
```python
class VectorKnowledgeBase:
    def __init__(self, vector_db_client):
        self.client = vector_db_client  # Pinecone/Weaviate
        
    def store_evaluation_embedding(self, evaluation):
        """Store evaluation as vector embedding"""
        # 1. Extract text content
        text = self.extract_evaluation_text(evaluation)
        
        # 2. Remove PII
        clean_text = self.remove_pii(text)
        
        # 3. Generate embedding
        embedding = self.generate_embedding(clean_text)
        
        # 4. Store in vector DB
        self.client.upsert(
            id=evaluation.id,
            vector=embedding,
            metadata={
                "type": evaluation.type,
                "date": evaluation.date,
                "anonymized": True
            }
        )
```

### 6. Qualtrics Integration

#### Import/Export Service
```python
class QualtricsIntegration:
    def __init__(self, qualtrics_api_key):
        self.api_key = qualtrics_api_key
        
    def import_from_qualtrics(self, survey_id):
        """Import evaluation data from Qualtrics"""
        # 1. Fetch survey responses
        responses = self.fetch_survey_responses(survey_id)
        
        # 2. Transform to internal format
        evaluations = self.transform_responses(responses)
        
        # 3. Store in database
        return self.store_evaluations(evaluations)
        
    def export_to_qualtrics(self, evaluation_ids):
        """Export evaluations to Qualtrics format"""
        # 1. Fetch evaluations
        evaluations = self.get_evaluations(evaluation_ids)
        
        # 2. Transform to Qualtrics format
        qualtrics_data = self.transform_to_qualtrics(evaluations)
        
        # 3. Create CSV/JSON export
        return self.create_export_file(qualtrics_data)
```

## Security & Compliance

### FERPA Compliance
```python
class FERPACompliance:
    """Ensure FERPA compliance for student data"""
    
    @staticmethod
    def validate_access(user, student_record):
        """Validate user has legitimate educational interest"""
        # Check user role and relationship to student
        
    @staticmethod
    def audit_access(user, action, resource):
        """Log all access for audit trail"""
        # Create audit log entry
        
    @staticmethod
    def anonymize_for_research(data):
        """Remove identifying information for research use"""
        # Apply anonymization rules
```

### Data Encryption
```python
# Encryption at rest
class EncryptedField(db.Column):
    """Custom SQLAlchemy field for encrypted data"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.encryptor = Fernet(settings.ENCRYPTION_KEY)
    
    def process_bind_param(self, value, dialect):
        """Encrypt before storing"""
        if value:
            return self.encryptor.encrypt(value.encode())
        return value
    
    def process_result_value(self, value, dialect):
        """Decrypt when retrieving"""
        if value:
            return self.encryptor.decrypt(value).decode()
        return value
```

## Performance Optimization

### Caching Strategy
```python
# Redis caching for frequent queries
@cache.memoize(timeout=300)
def get_student_evaluation_summary(student_id):
    """Cache student evaluation summaries"""
    return db.session.query(Evaluation).filter_by(
        student_id=student_id
    ).all()

# Invalidate cache on updates
def invalidate_student_cache(student_id):
    cache.delete_memoized(get_student_evaluation_summary, student_id)
```

### Database Indexing
```
```