# How AI-STER Works - Complete Guide

## What is AI-STER?

AI-STER (AI-Supported Teacher Evaluation and Reflection) is a digital platform that helps student teachers and their evaluators streamline the lesson planning and evaluation process.

## Core Features

### 1. 📋 Lesson Plan Management
- **Upload**: Student teachers upload lesson plans (PDF, Word, images)
- **AI Analysis**: System automatically extracts key information
- **Storage**: All lesson plans are organized and searchable

### 2. 🤖 AI-Powered Extraction
The AI analyzes lesson plans to extract 15 key fields:
- Teacher name, date, school
- Subject, grade level, topic
- Duration, class period, student count
- Learning objectives, materials, assessments
- Utah Core Standards alignment
- Lesson structure/flow

**Confidence Score**: Shows how many fields were successfully extracted (0-100%)

### 3. 📊 Evaluation System
- **Digital Rubric**: Based on official STER evaluation criteria
- **16 Evaluation Items**: Grouped into Planning, Instruction, Assessment, and Management
- **Scoring**: 0-3 scale with detailed descriptors
- **AI Assistance**: Suggests scores and generates feedback

### 4. 📈 Progress Tracking
- **Dashboard**: Visual overview of all evaluations
- **Analytics**: Track progress over time
- **Export**: Generate reports for university requirements

## User Workflow

### For Student Teachers:
1. **Create Account** → Sign up with university email
2. **Upload Lesson Plan** → PDF, Word, or image files
3. **Review AI Extraction** → Verify extracted information
4. **Submit for Evaluation** → Send to supervising teacher
5. **View Feedback** → See scores and comments
6. **Track Progress** → Monitor improvement over time

### For Evaluators:
1. **Access Submissions** → View student lesson plans
2. **Review AI Analysis** → See extracted information
3. **Complete Evaluation** → Score using digital rubric
4. **Provide Feedback** → Add comments and suggestions
5. **Track Students** → Monitor multiple student teachers

## Technical Architecture

### Frontend
- **Streamlit**: Python-based web interface
- **Responsive Design**: Works on desktop and mobile
- **Real-time Updates**: Live data synchronization

### Backend
- **Supabase**: PostgreSQL database for data storage
- **OpenAI GPT-4**: Powers AI extraction and analysis
- **Python**: Core application logic

### Security
- **Authentication**: Email/password with session management
- **Data Privacy**: Encrypted storage, no sharing
- **Access Control**: Role-based permissions

## Key Components

### 1. AI Lesson Plan Analysis
```
Input: Uploaded lesson plan → AI Processing → Extracted Fields → Confidence Score
```

### 2. Evaluation Rubric
```
16 Items → 4 Categories → Score (0-3) → Feedback → Final Report
```

### 3. Database Schema
- **Users**: Student teachers and evaluators
- **Lesson Plans**: Uploaded documents and extracted data
- **Evaluations**: Scores, feedback, and metadata
- **Analytics**: Progress tracking data

## Best Practices

### For High AI Confidence (85%+):
- Use structured lesson plan format
- Include all required fields clearly
- Label sections explicitly
- Use standard formatting

### For Accurate Evaluations:
- Complete all 16 rubric items
- Provide specific feedback
- Use AI suggestions as starting points
- Export reports regularly

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Low AI confidence | Use structured format with clear labels |
| Can't upload file | Check file type (PDF/Word/Image) and size (<10MB) |
| Missing evaluations | Check filter settings on dashboard |
| Export problems | Ensure all required fields are complete |

## System Requirements

- **Browser**: Chrome, Firefox, Safari, Edge (latest versions)
- **Internet**: Stable connection required
- **Screen**: Minimum 1024x768 resolution
- **Files**: PDF, DOCX, JPG, PNG supported

## Support

- **Documentation**: This guide
- **In-app Help**: Click help icons for context
- **Email Support**: [support email]
- **Response Time**: 24-48 hours

## Future Features

- Mobile app
- Batch uploads
- Video lesson plan support
- Integration with university systems
- Advanced analytics

---

*AI-STER is designed to reduce administrative burden while maintaining high educational standards. The system combines AI efficiency with human expertise to support the next generation of teachers.*
