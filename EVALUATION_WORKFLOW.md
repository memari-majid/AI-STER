# AI-STER Evaluation Workflow
Comprehensive guide for the AI-powered evaluation process

## Overview
The AI-STER evaluation workflow leverages AI to analyze lesson plans and observation notes, providing comprehensive evidence-based analysis that supervisors use alongside their observations to make informed scoring decisions.

## Core Design Principles
1. **AI as Analytical Assistant**: AI extracts and organizes information to support decision-making
2. **Supervisor Expertise Central**: Professional judgment drives all scoring decisions
3. **Evidence-Based Process**: Combines planned activities with observed execution
4. **Flexible Workflow**: Accommodates various evaluation scenarios

## Complete Workflow Sequence

### Phase 1: Pre-Observation

#### Step 1: Lesson Plan Upload (Optional)
- Upload lesson plan in PDF, DOCX, or TXT format
- AI extracts key information:
  - Learning objectives
  - Planned activities
  - Assessment strategies
  - Standards alignment
- Can proceed without lesson plan (reduced AI accuracy)

#### Step 2: Student Information
- Enter student teacher details (triggers evaluation tracking)
- System displays student's evaluation progress
- Choose appropriate rubric (STER/Field)

#### Step 2.5: STER Evaluation Type Selection (STER Only)
- **Intelligent Type Selection**: System analyzes student's completion history
- **Available Options**: Only shows available formative types (1-4) or summative
- **Visual Indicators**: 
  - Completed formative evaluations grayed out/disabled
  - Clear indication of next required evaluation type
  - Progress bar showing formative completion status
- **Automatic Summative Eligibility**: Summative option appears after sufficient formatives
- **Error Prevention**: Cannot select already-completed formative types

### Phase 2: Observation

#### Step 3: Classroom Observation & Documentation
```
📝 Detailed Observation Notes
- Comprehensive observations during lesson
- Structured prompts guide documentation
- Focus areas:
  • Teaching strategies employed
  • Student engagement and responses
  • Classroom management techniques
  • Assessment methods used
  • Professional behaviors demonstrated
```

**Requirements:**
- Minimum 200 words recommended
- Specific examples and behaviors
- Time-stamped incidents when relevant
- Both strengths and areas for growth

### Phase 3: AI Analysis

#### Step 4: AI-Powered Evidence Extraction
```
🤖 Generate AI Analysis
Trigger: "Generate AI Analysis" button
Process: AI analyzes lesson plan + observation notes
Output: Evidence-based justifications for each competency
```

**AI Analysis Components:**
1. **Lesson Plan Analysis**
   - Extracts relevant objectives and activities
   - Identifies planned assessment strategies
   - Maps content to competency criteria

2. **Observation Analysis**
   - Identifies specific behaviors and incidents
   - Extracts evidence of competency demonstration
   - Notes alignment between planning and execution

3. **Comprehensive Justification**
   - Synthesizes all evidence
   - Provides balanced analysis
   - Suggests areas of strength and improvement

### Phase 4: Scoring

#### Step 5: Informed Scoring Process
```
🎯 Evidence-Based Scoring
Left Side: AI Analysis & Justifications
Right Side: Scoring Controls
Process: Review AI analysis → Consider observations → Assign scores
```

**Scoring Workflow:**
1. Review AI-generated analysis for each competency
2. Consider your direct observations
3. Edit justifications as needed
4. Assign score based on comprehensive evidence
5. Ensure score aligns with justification

**Score Levels:**
- Level 0: Does not demonstrate
- Level 1: Approaching
- Level 2: Demonstrates
- Level 3: Exceeds

### Phase 5: Finalization

#### Step 6: Professional Dispositions
- Score each disposition (Levels 1-4)
- Add specific feedback comments
- All must score Level 3+ for completion

#### Step 7: Review and Submit
- Final review of all scores and justifications
- Validation checks ensure completeness
- Save as draft or complete evaluation
- Generate PDF report

## Technical Implementation Details

### AI Prompt Structure
```python
"""
Analyze the following lesson plan and observation notes to extract 
relevant information for evaluating [Competency X].

Lesson Plan: [Content]
Observation Notes: [Content]

Extract and analyze:
1. Relevant objectives from the lesson plan
2. Specific observed behaviors
3. Evidence of competency demonstration
4. Alignment between planning and execution
5. Concrete examples and incidents

Provide comprehensive analysis to support evaluation.
"""
```

### Session State Management
- `observation_notes`: Supervisor's detailed observations
- `ai_analyses`: Generated justifications by competency
- `scores`: Assigned scores
- `disposition_scores`: Professional disposition ratings
- `disposition_comments`: Feedback for each disposition

### UI/UX Flow
1. **Linear Progression**: Clear step-by-step process
2. **Visual Indicators**: Progress tracking and status
3. **Contextual Help**: Tooltips and examples
4. **Save Progress**: Draft functionality
5. **Validation**: Real-time requirement checking

## Workflow Variations

### Scenario 1: Complete Workflow
- Full lesson plan uploaded
- Detailed observations recorded
- AI analysis for all competencies
- Comprehensive scoring and feedback

### Scenario 2: No Lesson Plan
- Skip lesson plan upload
- Rely on observation notes
- AI analysis based on observations only
- Manual context addition as needed

### Scenario 3: Partial Evaluation
- Score some competencies
- Save as draft
- Return later to complete
- AI can analyze scored items only

### Scenario 4: Manual Override
- Skip AI analysis
- Enter justifications manually
- Direct scoring based on observations
- Full supervisor control

## Best Practices

### For Supervisors
1. **Detailed Observations**: More detail enables better AI analysis
2. **Specific Examples**: Include concrete behaviors and incidents
3. **Balanced Feedback**: Note both strengths and growth areas
4. **Review AI Output**: Always verify and edit AI justifications
5. **Consistent Scoring**: Ensure scores align with evidence

### For System Optimization
1. **Complete Information**: Provide lesson plans when available
2. **Structured Notes**: Use observation prompts as guides
3. **Timely Completion**: Complete evaluations while fresh
4. **Regular Saves**: Use draft functionality
5. **Feedback Loop**: Report AI accuracy issues

## Quality Assurance

### Validation Checks
- All competencies scored before completion
- Justifications present for all scores
- Dispositions meet minimum requirements
- Required fields completed
- Score-justification alignment

### AI Quality Metrics
- Evidence extraction accuracy
- Justification relevance
- Balanced analysis
- Appropriate length
- Professional tone

## Future Enhancements

### Near Term
- Voice-to-text for observations
- Competency-specific prompts
- Comparative analytics
- Batch evaluation processing

### Long Term
- Video lesson analysis
- Real-time observation tools
- Predictive scoring suggestions
- Multi-rater workflows
- Mobile application

## Troubleshooting

### Common Issues

**AI Analysis Not Generating**
- Check observation notes length (min 50 words)
- Verify OpenAI API key configured
- Ensure stable internet connection

**Scores Not Saving**
- Check all required fields completed
- Verify session hasn't timed out
- Use "Save as Draft" regularly

**Justifications Seem Generic**
- Add more specific observation details
- Include concrete examples
- Edit AI output to add context

## Support Resources

- User Guide: See help menu in application
- Video Tutorials: Available in training portal
- Technical Support: Contact IT helpdesk
- Feedback: Use in-app feedback form

---

*Last Updated: December 2024*
*Version: 2.0 - Unified Workflow*
*Compatibility: All modern browsers* 