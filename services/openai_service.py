"""
OpenAI service for AI-powered evaluation features
"""

import os
from typing import Dict, List, Optional
import openai
from openai import OpenAI
import json

try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

class OpenAIService:
    """Service for OpenAI API integration"""
    
    def __init__(self):
        """Initialize OpenAI service"""
        self.client = None
        self.model = "gpt-4o-mini"
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize OpenAI client if API key is available"""
        api_key = self._get_api_key()
        if api_key:
            try:
                self.client = OpenAI(api_key=api_key)
            except Exception as e:
                print(f"Failed to initialize OpenAI client: {e}")
                self.client = None
    
    def _get_api_key(self) -> Optional[str]:
        """Get OpenAI API key from Streamlit secrets or environment variables"""
        # First try Streamlit secrets (preferred for Streamlit Cloud)
        if HAS_STREAMLIT:
            try:
                if hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
                    return st.secrets['OPENAI_API_KEY']
            except Exception:
                pass  # Fall back to environment variable
        
        # Fall back to environment variable (for local development)
        return os.getenv('OPENAI_API_KEY')
    
    def is_enabled(self) -> bool:
        """Check if OpenAI service is enabled and configured"""
        return self.client is not None
    
    def analyze_lesson_plan(self, lesson_plan_text: str) -> Dict[str, any]:
        """
        Analyze lesson plan and extract key information
        
        Args:
            lesson_plan_text: The lesson plan content as text
        
        Returns:
            Dictionary containing extracted information
        """
        if not self.is_enabled():
            raise Exception("OpenAI service is not configured")
        
        prompt = self._build_lesson_plan_analysis_prompt(lesson_plan_text)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert educational supervisor who analyzes lesson plans. Extract key information accurately and provide it in the specified JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=800,
                temperature=0.1  # Low temperature for consistent extraction
            )
            
            # Parse the JSON response
            response_text = response.choices[0].message.content.strip()
            
            # Extract JSON from response (in case there's extra text)
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_text = response_text[start_idx:end_idx]
                extracted_info = json.loads(json_text)
                
                # Validate and clean the extracted information
                return self._validate_lesson_plan_extraction(extracted_info)
            else:
                raise Exception("Could not parse JSON from AI response")
        
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse AI response as JSON: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to analyze lesson plan: {str(e)}")
    
    def _build_lesson_plan_analysis_prompt(self, lesson_plan_text: str) -> str:
        """Build prompt for lesson plan analysis"""
        
        prompt = f"""Analyze the following lesson plan and extract key information. Return ONLY a valid JSON object with the extracted data.

LESSON PLAN TEXT:
{lesson_plan_text}

Extract the following information and return it as a JSON object:

{{
    "teacher_name": "Full name of the teacher/student teacher",
    "lesson_date": "Date of the lesson (YYYY-MM-DD format if possible, or as written)",
    "subject_area": "Subject being taught",
    "grade_levels": "Grade level(s) of students",
    "school_name": "Name of the school",
    "lesson_topic": "Main topic or title of the lesson",
    "class_period": "Class period or time if mentioned",
    "duration": "Lesson duration if mentioned",
    "total_students": "Number of students in class",
    "utah_core_standards": "Utah Core Standards referenced if mentioned",
    "learning_objectives": ["List", "of", "learning", "objectives"],
    "materials": ["List", "of", "materials", "needed"],
    "assessment_methods": ["Types", "of", "assessment", "mentioned"],
    "lesson_structure": "Brief description of lesson flow/structure",
    "notes": "Any additional notes or special considerations",
    "confidence_score": 0.95
}}

IMPORTANT INSTRUCTIONS:
1. If information is not found or unclear, use null for that field
2. For grade_levels, extract the specific grade(s) mentioned (e.g., "3rd Grade", "6-8", "K-5")
3. For lesson_date, convert to YYYY-MM-DD format if possible, otherwise keep as written
4. Be very careful to extract the actual teacher name, not example names
5. For total_students, look for class size information
6. confidence_score should reflect how clear and complete the information is (0.0-1.0)
7. Return ONLY the JSON object, no additional text

JSON Response:"""
        
        return prompt
    
    def _validate_lesson_plan_extraction(self, extracted_info: Dict) -> Dict:
        """Validate and clean extracted lesson plan information"""
        
        # Ensure required fields exist with defaults
        validated = {
            'teacher_name': extracted_info.get('teacher_name', None),
            'lesson_date': extracted_info.get('lesson_date', None),
            'subject_area': extracted_info.get('subject_area', None),
            'grade_levels': extracted_info.get('grade_levels', None),
            'school_name': extracted_info.get('school_name', None),
            'lesson_topic': extracted_info.get('lesson_topic', None),
            'class_period': extracted_info.get('class_period', None),
            'duration': extracted_info.get('duration', None),
            'total_students': extracted_info.get('total_students', None),
            'utah_core_standards': extracted_info.get('utah_core_standards', None),
            'learning_objectives': extracted_info.get('learning_objectives', []),
            'materials': extracted_info.get('materials', []),
            'assessment_methods': extracted_info.get('assessment_methods', []),
            'lesson_structure': extracted_info.get('lesson_structure', None),
            'notes': extracted_info.get('notes', None),
            'confidence_score': extracted_info.get('confidence_score', 0.8),
            'extraction_timestamp': None  # Will be set when used
        }
        
        # Clean up lists - ensure they're actually lists
        for list_field in ['learning_objectives', 'materials', 'assessment_methods']:
            if not isinstance(validated[list_field], list):
                validated[list_field] = []
        
        # Convert total_students to int if it's a string number
        if validated['total_students']:
            try:
                validated['total_students'] = int(validated['total_students'])
            except (ValueError, TypeError):
                validated['total_students'] = None
        
        return validated
    
    def generate_justification(
        self,
        item: Dict,
        score: int,
        student_name: str,
        context: Optional[str] = None
    ) -> str:
        """
        Generate AI-assisted justification for a given score
        
        Args:
            item: Assessment item dictionary
            score: Score level (0-3)
            student_name: Name of the student being evaluated
            context: Additional context (optional)
        
        Returns:
            Generated justification text
        """
        if not self.is_enabled():
            # Return generic justification if AI is not enabled
            return self._create_generic_justification(item, score)
        
        # Check if context is empty or not relevant to this competency
        if not context or not context.strip():
            return self._create_generic_justification(item, score)
        
        prompt = self._build_justification_prompt(item, score, student_name, context)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert educational evaluator specializing in student teacher assessments. Provide clear, professional, evidence-based justifications. If the provided context does not contain relevant information for the specific competency, return '[NO_CONTEXT]' as the first word of your response."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Check if AI indicates no relevant context
            if ai_response.startswith('[NO_CONTEXT]'):
                return self._create_generic_justification(item, score)
            
            return ai_response
        
        except Exception as e:
            # Fallback to generic justification on error
            return self._create_generic_justification(item, score)
    
    def analyze_evaluation(
        self,
        scores: Dict[str, int],
        justifications: Dict[str, str],
        disposition_scores: Dict[str, int],
        rubric_type: str
    ) -> str:
        """
        Analyze complete evaluation and provide feedback
        
        Args:
            scores: Assessment item scores
            justifications: Assessment justifications
            disposition_scores: Professional disposition scores
            rubric_type: Type of rubric ("field_evaluation" or "ster")
        
        Returns:
            Analysis and feedback text
        """
        if not self.is_enabled():
            raise Exception("OpenAI service is not configured")
        
        prompt = self._build_analysis_prompt(scores, justifications, disposition_scores, rubric_type)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert educational supervisor providing constructive feedback on student teacher evaluations. Focus on growth and development."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=400,
                temperature=0.6
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            raise Exception(f"Failed to generate AI analysis: {str(e)}")
    
    def _build_justification_prompt(
        self,
        item: Dict,
        score: int,
        student_name: str,
        context: Optional[str] = None
    ) -> str:
        """Build prompt for justification generation"""
        
        score_labels = {
            0: "Does not demonstrate competency",
            1: "Is approaching competency at expected level",
            2: "Demonstrates competency at expected level",
            3: "Exceeds expected level of competency"
        }
        
        prompt = f"""You are an expert education evaluator helping write a justification for a student teaching evaluation.

Assessment Item: {item['code']} - {item['title']}
Competency Area: {item['competency_area']}
Context: {item['context']}
Score Level: {score} ({score_labels.get(score, 'Unknown')})

Score Description: {item['levels'].get(str(score), 'No description available')}

Student: {student_name}
{f'Additional Context: {context}' if context else ''}

Write a professional, specific justification (2-3 sentences) that:
1. Explains why this score was given
2. Provides specific examples of observed behaviors
3. Aligns with the score description
4. Maintains a constructive, professional tone

{f'Reference example: {item.get("example_justification", "")}' if item.get("example_justification") else ''}

Justification:"""
        
        return prompt
    
    def _build_analysis_prompt(
        self,
        scores: Dict[str, int],
        justifications: Dict[str, str],
        disposition_scores: Dict[str, int],
        rubric_type: str
    ) -> str:
        """Build prompt for evaluation analysis"""
        
        total_score = sum(scores.values())
        item_count = len(scores)
        avg_score = total_score / item_count if item_count > 0 else 0
        
        score_counts = {
            0: len([s for s in scores.values() if s == 0]),
            1: len([s for s in scores.values() if s == 1]),
            2: len([s for s in scores.values() if s == 2]),
            3: len([s for s in scores.values() if s == 3])
        }
        
        missing_justifications = len([j for j in justifications.values() if not j.strip()])
        
        avg_disposition = sum(disposition_scores.values()) / len(disposition_scores) if disposition_scores else 0
        
        prompt = f"""Analyze this student teaching evaluation and provide constructive feedback:

Evaluation Type: {rubric_type.replace('_', ' ').title()}
Total Items: {item_count}
Total Score: {total_score}
Average Score: {avg_score:.2f}

Score Distribution:
- Level 0 (Does not demonstrate): {score_counts[0]} items
- Level 1 (Approaching): {score_counts[1]} items  
- Level 2 (Demonstrates): {score_counts[2]} items
- Level 3 (Exceeds): {score_counts[3]} items

Missing Justifications: {missing_justifications}
Professional Dispositions Average: {avg_disposition:.2f}

Provide:
1. Overall assessment of performance
2. Strengths identified
3. Areas for improvement
4. Specific recommendations
5. Next steps for professional growth

Keep response concise (4-5 sentences) and constructive."""
        
        return prompt
    
    def generate_bulk_justifications(
        self,
        items: List[Dict],
        scores: Dict[str, int],
        observation_notes: str,
        student_name: str,
        rubric_type: str
    ) -> Dict[str, str]:
        """
        Generate justifications for all scored items using supervisor's observation notes
        
        Args:
            items: List of assessment item dictionaries
            scores: Dictionary mapping item IDs to scores
            observation_notes: Supervisor's classroom observation notes
            student_name: Name of the student being evaluated
            rubric_type: Type of rubric ("field_evaluation" or "ster")
        
        Returns:
            Dictionary mapping item IDs to generated justifications
        """
        if not self.is_enabled():
            raise Exception("OpenAI service is not configured")
        
        prompt = self._build_bulk_justification_prompt(
            items, scores, observation_notes, student_name, rubric_type
        )
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert educational supervisor who writes professional, evidence-based justifications for student teacher evaluations. Use the provided observation notes to create specific, individualized justifications for each competency."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=2000,  # Increased for multiple justifications
                temperature=0.6
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Parse the JSON response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_text = response_text[start_idx:end_idx]
                justifications = json.loads(json_text)
                
                # Validate that we have justifications for all scored items
                validated_justifications = {}
                for item in items:
                    item_id = item['id']
                    if item_id in scores and item_id in justifications:
                        validated_justifications[item_id] = justifications[item_id]
                    elif item_id in scores:
                        # Generate generic justification if missing
                        validated_justifications[item_id] = self._create_generic_justification(item, scores[item_id])
                
                return validated_justifications
            else:
                raise Exception("Could not parse JSON from AI response")
        
        except json.JSONDecodeError as e:
            # Fallback: Generate generic justifications
            fallback_justifications = {}
            for item in items:
                item_id = item['id']
                if item_id in scores:
                    fallback_justifications[item_id] = self._create_generic_justification(item, scores[item_id])
            return fallback_justifications
        except Exception as e:
            raise Exception(f"Failed to generate bulk justifications: {str(e)}")
    
    def _create_generic_justification(self, item: Dict, score: int) -> str:
        """
        Create a generic justification when no specific observation notes are available
        
        Args:
            item: Assessment item dictionary
            score: Score level (0-3)
            
        Returns:
            Generic justification with warning
        """
        score_labels = {
            0: "does not demonstrate competency",
            1: "is approaching competency at expected level",
            2: "demonstrates competency at expected level", 
            3: "exceeds expected level of competency"
        }
        
        score_description = item['levels'].get(str(score), 'No description available')
        score_label = score_labels.get(score, 'demonstrates competency')
        
        generic_justification = (
            f"The student teacher {score_label} for {item['code']} - {item['title']}. "
            f"{score_description} "
            f"**NOTE: No specific observations were recorded for this competency area - "
            f"supervisor may wish to add additional details based on classroom observation.**"
        )
        
        return generic_justification
    
    def _build_bulk_justification_prompt(
        self,
        items: List[Dict],
        scores: Dict[str, int],
        observation_notes: str,
        student_name: str,
        rubric_type: str
    ) -> str:
        """Build prompt for bulk justification generation"""
        
        score_labels = {
            0: "Does not demonstrate competency",
            1: "Is approaching competency at expected level", 
            2: "Demonstrates competency at expected level",
            3: "Exceeds expected level of competency"
        }
        
        # Build items list with scores
        items_text = ""
        for item in items:
            item_id = item['id']
            if item_id in scores:
                score = scores[item_id]
                items_text += f"\n{item['code']} - {item['title']}\n"
                items_text += f"Competency Area: {item['competency_area']}\n"
                items_text += f"Assigned Score: Level {score} ({score_labels.get(score, 'Unknown')})\n"
                items_text += f"Score Description: {item['levels'].get(str(score), 'No description available')}\n"
                items_text += "---\n"
        
        prompt = f"""You are writing professional justifications for a student teaching evaluation based on classroom observation notes.

STUDENT: {student_name}
EVALUATION TYPE: {rubric_type.replace('_', ' ').title()}

SUPERVISOR'S OBSERVATION NOTES:
{observation_notes}

ASSESSMENT ITEMS TO JUSTIFY:
{items_text}

INSTRUCTIONS:
1. Write a specific, evidence-based justification for EACH item listed above
2. Use details from the observation notes to support each score
3. Each justification should be 2-3 sentences and reference specific observed behaviors
4. Maintain a professional, constructive tone
5. Ensure justifications align with the assigned score level

IMPORTANT: If the observation notes do not contain relevant information for a specific competency area, generate a generic justification using this format:
"[GENERIC] The student teacher demonstrates competency for the assessed item. **NOTE: No specific observations were recorded for this competency area - supervisor may wish to add additional details.**"

Return your response as a JSON object with item IDs as keys and justifications as values:

{{
    "item_id_1": "Professional justification based on observation notes...",
    "item_id_2": "[GENERIC] The student teacher demonstrates for CC1 - Classroom Environment...",
    ...
}}

JSON Response:"""
        
        return prompt 