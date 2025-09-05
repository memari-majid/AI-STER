# Lesson Plan Format Guide for High AI Confidence

## Problem: Low AI Confidence (6.7%)

The AI extraction system expects 15 specific fields. When lesson plans are missing these fields, the confidence score drops dramatically.

## Current Issue

Your current lesson plan format only includes:
```
UTAH CORE STANDARDS:
Primary Standard: N/A - General learning objective
Supporting Standards: Social Studies Thinking Standards

LESSON OVERVIEW:
Students will explore general topic through hands-on investigation...
```

**Result**: Only 1/15 fields extracted = 6.7% confidence

## Required Fields for High Confidence

The AI looks for these 15 fields:

1. **teacher_name** - Full name of the teacher
2. **lesson_date** - Date of the lesson
3. **subject_area** - Subject being taught
4. **grade_levels** - Specific grade(s)
5. **school_name** - Name of the school
6. **lesson_topic** - Main topic/title
7. **class_period** - Period or time
8. **duration** - Lesson length
9. **total_students** - Number of students
10. **utah_core_standards** - Standards referenced
11. **learning_objectives** - List of objectives
12. **materials** - List of materials needed
13. **assessment_methods** - Assessment types
14. **lesson_structure** - Brief description of flow
15. **notes** - Additional information

## Recommended Format for 90%+ Confidence

```
LESSON PLAN

Teacher Name: [Full Name]
Date: [YYYY-MM-DD]
Subject Area: [Subject]
Grade Levels: [Grade(s)]
School Name: [School Name]

Lesson Topic: [Main Topic/Title]
Class Period: [Period/Time]
Duration: [Length]
Total Students: [Number]

UTAH CORE STANDARDS:
[List standards here]

LEARNING OBJECTIVES:
- [Objective 1]
- [Objective 2]
- [Objective 3]

MATERIALS:
- [Material 1]
- [Material 2]
- [Material 3]

ASSESSMENT METHODS:
- [Assessment type 1]
- [Assessment type 2]

LESSON STRUCTURE:
[Brief description of lesson flow, activities, and timing]

NOTES:
[Any additional relevant information]
```

## Format Comparison

### ❌ Low Confidence Format (6.7%)
- Minimal structure
- Missing key identifiers (teacher, date, school)
- Vague descriptions
- No clear sections for materials/assessment

### ✅ High Confidence Format (85-95%)
- Clear labels for all fields
- Structured sections
- Specific information
- Complete metadata

## Tips for Maximum AI Extraction Success

1. **Use Clear Labels**: Start each section with the exact field name
2. **Be Specific**: Include actual values, not placeholders
3. **Use Lists**: For objectives, materials, and assessments, use bullet points
4. **Include Metadata**: Always include teacher name, date, and school
5. **Structure Consistently**: Follow the same format for all lesson plans

## Alternative Acceptable Formats

### Narrative Style (80-85% confidence)
If you prefer paragraph format, ensure you include phrases like:
- "I'm [Teacher Name], teaching at [School]..."
- "This [duration]-minute lesson on [date]..."
- "The [number] students in my [grade] [subject] class..."

### Table Format (75-80% confidence)
Tables can work but may have slightly lower extraction rates due to parsing complexity.

## Testing Your Format

To verify your lesson plan format achieves high confidence:

1. Include all 15 fields with clear labels
2. Use the AI analysis feature
3. Aim for 85%+ confidence score
4. Adjust format if confidence is below 70%

## Quick Checklist

Before submitting a lesson plan, verify it includes:

- [ ] Teacher name
- [ ] Date
- [ ] Subject and grade level
- [ ] School name
- [ ] Lesson topic and duration
- [ ] Student count
- [ ] Utah Core Standards
- [ ] Learning objectives (list)
- [ ] Materials needed (list)
- [ ] Assessment methods (list)
- [ ] Lesson structure description

Following this format will ensure reliable AI extraction and analysis of your lesson plans.
