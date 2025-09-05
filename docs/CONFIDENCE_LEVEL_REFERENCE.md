# AI Confidence Level Reference Guide

## What is AI Confidence?

The AI confidence score shows how successfully the system extracted information from a lesson plan:
- **Formula**: `Confidence = (Fields Extracted / 15) × 100%`
- The AI looks for 15 specific fields in each lesson plan

## Expected Confidence Levels by Format

### 🟢 High Confidence (85-95%)
**What to expect**: 13-15 fields successfully extracted

**Lesson Plan Characteristics**:
- All sections clearly labeled
- Complete teacher and school information
- Structured format with headers
- Explicit learning objectives, materials, and assessments
- Full lesson structure/flow description

**Examples in Test Data**:
- `5th Grade Math - Fractions` (90-95%)
- `ESL Daily Routines` (90-95%)
- `Special Ed Reading Intervention` (85-90%)

### 🟡 Medium Confidence (70-85%)
**What to expect**: 10-12 fields successfully extracted

**Lesson Plan Characteristics**:
- Mix of structured and narrative elements
- Most key information present but may be embedded in text
- Some sections might be missing or unclear
- Table/visual formats that require interpretation

**Examples in Test Data**:
- `3rd Grade ELA Main Ideas` (70-80%)
- `7th Grade Social Studies` (75-85%)

### 🔴 Low Confidence (<70%)
**What to expect**: Less than 10 fields extracted

**Lesson Plan Characteristics**:
- Minimal structure or labels
- Missing most required information
- Very brief outlines
- Standards-only documents
- Vague or generic descriptions

**Examples in Test Data**:
- `Elementary Science Outline` (10-30%)
- `Generic Standards Only` (6-7%)

## The 15 Fields AI Looks For

1. **Teacher name** - Full name of instructor
2. **Lesson date** - When the lesson is taught
3. **Subject area** - Main subject (Math, Science, etc.)
4. **Grade levels** - Specific grade(s)
5. **School name** - Institution name
6. **Lesson topic** - Main topic/title
7. **Class period** - Period or time slot
8. **Duration** - Length of lesson
9. **Total students** - Number of students
10. **Utah Core Standards** - Standards alignment
11. **Learning objectives** - What students will learn (list)
12. **Materials** - Resources needed (list)
13. **Assessment methods** - How learning is evaluated (list)
14. **Lesson structure** - Flow/sequence of activities
15. **Notes** - Additional information

## Troubleshooting Low Confidence

If you're getting unexpectedly low confidence:

1. **Check for missing labels**: AI needs clear section headers
2. **Add basic information**: Teacher name, date, school often missing
3. **Structure your content**: Use bullet points for objectives/materials
4. **Be specific**: "45 minutes" not "one class period"
5. **Include all sections**: Even if brief, include all 15 fields

## Testing Your Lesson Plans

1. Use the **"🧪 Test Data"** page, **"AI Confidence Testing"** tab
2. Select lesson plans with known confidence levels
3. Compare your results to expected ranges
4. Use high-confidence examples as templates

## Quick Fix for 6.7% Confidence

If you're seeing 6.7% confidence (1/15 fields), your lesson plan likely only has:
- Utah Core Standards section
- Missing all other required fields

**Solution**: Add at minimum:
- Teacher name and school
- Subject and grade level
- Learning objectives
- Basic lesson structure

This should immediately boost confidence to 30-40% or higher.
