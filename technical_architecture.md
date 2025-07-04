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

### 2. Formative/Summative Evaluation System

#### State Management
```python
class EvaluationType(Enum):
    FORMATIVE = "formative"
    SUMMATIVE = "summative"

class EvaluationStatus(Enum):
    DRAFT = "draft"
    COMPLETED = "completed"
    SUBMITTED = "submitted"
    ARCHIVED = "archived"

class EvaluationTracker:
    def __init__(self, db_session):
        self.db = db_session
    
    def get_formative_count(self, student_id):
        """Count completed formative evaluations"""
        
    def is_summative_required(self, student_id):
        """Check if summative evaluation is due"""
        
    def create_summative_from_formatives(self, student_id):
        """Generate summative evaluation from formative data"""
```

#### Database Schema
```sql
-- Enhanced evaluations table
CREATE TABLE evaluations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID REFERENCES students(id),
    supervisor_id UUID REFERENCES users(id),
    type VARCHAR(20) CHECK (type IN ('formative', 'summative')),
    status VARCHAR(20) CHECK (status IN ('draft', 'completed', 'submitted', 'archived')),
    evaluation_date DATE,
    observation_notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    submitted_at TIMESTAMP,
    UNIQUE(student_id, evaluation_date, type)
);

-- Evaluation relationships for summative generation
CREATE TABLE formative_summative_links (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    summative_id UUID REFERENCES evaluations(id),
    formative_id UUID REFERENCES evaluations(id),
    weight DECIMAL(3,2) DEFAULT 1.0
);
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
```sql
-- Performance indexes
CREATE INDEX idx_evaluations_student_date ON evaluations(student_id, evaluation_date);
CREATE INDEX idx_evaluations_type_status ON evaluations(type, status);
CREATE INDEX idx_scores_evaluation ON scores(evaluation_id);
CREATE INDEX idx_justifications_evaluation ON justifications(evaluation_id);
```

## Monitoring & Analytics

### Application Metrics
```python
# Prometheus metrics
evaluation_counter = Counter('evaluations_total', 'Total evaluations created')
ai_generation_histogram = Histogram('ai_generation_duration', 'AI justification generation time')
email_send_counter = Counter('emails_sent', 'Total evaluation emails sent')

# Usage tracking
@track_metrics
def create_evaluation(data):
    evaluation_counter.inc()
    # Implementation
```

### Error Handling
```python
class AISTERException(Exception):
    """Base exception for AI-STER application"""
    pass

class EvaluationNotFoundError(AISTERException):
    """Raised when evaluation doesn't exist"""
    pass

class InsufficientPermissionsError(AISTERException):
    """Raised when user lacks required permissions"""
    pass

# Global error handler
@app.exception_handler(AISTERException)
async def handle_app_exception(request, exc):
    logger.error(f"Application error: {exc}")
    return JSONResponse(
        status_code=400,
        content={"error": str(exc)}
    )
```

## Deployment Strategy

### Docker Configuration
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Kubernetes Deployment
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-ster-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-ster-api
  template:
    metadata:
      labels:
        app: ai-ster-api
    spec:
      containers:
      - name: api
        image: ai-ster:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: ai-ster-secrets
              key: database-url
```

This architecture provides a robust foundation for implementing all client-requested features while maintaining scalability, security, and compliance requirements. 