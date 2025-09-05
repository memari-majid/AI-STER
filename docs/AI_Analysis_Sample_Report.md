# AI-STER Lesson Plan Analysis - Sample Report

## Executive Summary

This report demonstrates how the AI-STER system analyzes different lesson plan formats and calculates confidence scores. We tested 4 different formats to show the range of AI performance.

---

## Test Results Overview

| Lesson Plan Format | Fields Extracted | Confidence Score | Usability Rating |
|-------------------|------------------|------------------|------------------|
| Structured Format | 14/15 | 93.3% | ✅ Excellent |
| Narrative Format | 11/15 | 73.3% | ⚠️ Good |
| Table Format | 10/15 | 66.7% | ⚠️ Acceptable |
| Minimal Format | 1/15 | 6.7% | ❌ Poor |

---

## Detailed Analysis by Format

### 1. Structured Format (93.3% Confidence) ✅

**Input Sample:**
```
LESSON PLAN

Teacher Name: Sarah Mitchell
Date: 2024-11-15
Subject Area: Mathematics
Grade Levels: 4th Grade
School Name: Riverside Elementary

Lesson Topic: Fractions and Decimals
Class Period: 2nd Period
Duration: 45 minutes
Total Students: 24

UTAH CORE STANDARDS:
- 4.NF.6: Use decimal notation for fractions

LEARNING OBJECTIVES:
- Students will convert fractions to decimals
- Students will compare decimal values
- Students will apply decimals in real-world contexts

MATERIALS:
- Fraction bars
- Decimal place value charts
- Interactive whiteboard

ASSESSMENT METHODS:
- Exit ticket
- Peer assessment
- Observation checklist

LESSON STRUCTURE:
Opening warm-up (5 min), direct instruction (15 min), 
guided practice (15 min), independent work (10 min), closure (5 min)
```

**AI Extraction Results:**
| Field | Extracted Value | Status |
|-------|----------------|---------|
| teacher_name | Sarah Mitchell | ✅ Found |
| lesson_date | 2024-11-15 | ✅ Found |
| subject_area | Mathematics | ✅ Found |
| grade_levels | 4th Grade | ✅ Found |
| school_name | Riverside Elementary | ✅ Found |
| lesson_topic | Fractions and Decimals | ✅ Found |
| class_period | 2nd Period | ✅ Found |
| duration | 45 minutes | ✅ Found |
| total_students | 24 | ✅ Found |
| utah_core_standards | 4.NF.6: Use decimal notation... | ✅ Found |
| learning_objectives | [3 objectives listed] | ✅ Found |
| materials | [3 items listed] | ✅ Found |
| assessment_methods | [3 methods listed] | ✅ Found |
| lesson_structure | Opening warm-up (5 min)... | ✅ Found |
| notes | null | ❌ Not Found |

---

### 2. Narrative Format (73.3% Confidence) ⚠️

**Input Sample:**
```
Today I'll be teaching my 3rd grade science class at Oak Valley School. 
I'm Ms. Jennifer Lee, and this 50-minute lesson on the water cycle is 
scheduled for Monday, November 20th. My 22 students will explore how 
water moves through different states.

We'll start with a demonstration using a hot plate and ice to show 
evaporation and condensation. Students will work in groups to create 
water cycle diagrams using provided materials including poster boards, 
markers, and cotton balls for clouds.

The lesson aligns with Utah Science Standard 3.1.2 about matter 
changing states. I'll assess understanding through group presentations 
and a quick exit quiz about the water cycle stages.
```

**AI Extraction Results:**
| Field | Extracted Value | Status |
|-------|----------------|---------|
| teacher_name | Jennifer Lee | ✅ Found |
| lesson_date | November 20th | ✅ Found |
| subject_area | Science | ✅ Found |
| grade_levels | 3rd grade | ✅ Found |
| school_name | Oak Valley School | ✅ Found |
| lesson_topic | Water cycle | ✅ Found |
| class_period | null | ❌ Not Found |
| duration | 50 minutes | ✅ Found |
| total_students | 22 | ✅ Found |
| utah_core_standards | 3.1.2 about matter changing states | ✅ Found |
| learning_objectives | null | ❌ Inferred |
| materials | [poster boards, markers, cotton balls] | ✅ Found |
| assessment_methods | [group presentations, exit quiz] | ✅ Found |
| lesson_structure | null | ❌ Could be inferred |
| notes | null | ❌ Not Found |

---

### 3. Minimal Format (6.7% Confidence) ❌

**Input Sample:**
```
UTAH CORE STANDARDS:
Primary Standard: N/A - General learning objective
Supporting Standards: Social Studies Thinking Standards

LESSON OVERVIEW:
Students will explore general topic through hands-on investigation. 
This lesson connects to cross-curricular learning.
```

**AI Extraction Results:**
| Field | Extracted Value | Status |
|-------|----------------|---------|
| teacher_name | null | ❌ Not Found |
| lesson_date | null | ❌ Not Found |
| subject_area | null | ❌ Could infer "Social Studies" |
| grade_levels | null | ❌ Not Found |
| school_name | null | ❌ Not Found |
| lesson_topic | null | ❌ Too vague |
| class_period | null | ❌ Not Found |
| duration | null | ❌ Not Found |
| total_students | null | ❌ Not Found |
| utah_core_standards | Social Studies Thinking Standards | ✅ Found |
| learning_objectives | null | ❌ Too generic |
| materials | null | ❌ Not Found |
| assessment_methods | null | ❌ Not Found |
| lesson_structure | null | ❌ Too vague |
| notes | null | ❌ Not Found |

---

## Key Findings

### 1. **Format Impact on Confidence**
- Structured formats with clear labels achieve 85-95% confidence
- Narrative formats can work but may miss 20-30% of fields
- Minimal formats severely limit AI extraction capabilities

### 2. **Most Commonly Extracted Fields**
- Subject area (when mentioned)
- Grade levels (when specified)
- Standards (when listed)
- Teacher name (when stated)

### 3. **Most Commonly Missing Fields**
- Notes/additional information
- Class period (unless explicitly labeled)
- Specific lesson structure (in narrative formats)
- Learning objectives (when not bulleted)

### 4. **Inference Capabilities**
The AI can sometimes infer:
- Subject from context or standards
- Basic objectives from overview text
- Materials from activity descriptions

However, explicit labeling always yields better results.

---

## Recommendations for Educators

### For Best Results (90%+ Confidence):
1. Use clear section headers
2. Include all basic metadata (teacher, date, school)
3. List objectives and materials as bullet points
4. Specify exact student numbers and duration
5. Describe lesson flow/structure

### Minimum Requirements (70%+ Confidence):
1. Include teacher name and school
2. Specify subject and grade level
3. List main learning objectives
4. Reference applicable standards
5. Describe assessment methods

### Common Pitfalls to Avoid:
- ❌ Vague descriptions ("various materials")
- ❌ Missing basic information (date, duration)
- ❌ Embedding information only in paragraphs
- ❌ Using abbreviations without context
- ❌ Omitting lesson structure/flow

---

## Technical Notes

**Confidence Score Formula:**
```
Confidence = (Fields Successfully Extracted / 15) × 100%
```

**Field Extraction Priority:**
1. Exact matches with clear labels
2. Pattern recognition in narrative text
3. Inference from context (lowest reliability)

**Processing Time:**
- Average: 2-3 seconds per lesson plan
- Depends on document length and complexity

---

## Questions or Feedback?

This analysis represents our current AI capabilities. We're actively working to improve extraction accuracy, especially for narrative and non-standard formats. Your feedback on what constitutes essential vs. optional information would be invaluable.

*Report generated by AI-STER System v1.0*
