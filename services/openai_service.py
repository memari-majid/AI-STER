"""
OpenAI service for AI-powered evaluation features
"""

import os
from typing import Dict, List, Optional
import openai
from openai import OpenAI

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
            raise Exception("OpenAI service is not configured")
        
        prompt = self._build_justification_prompt(item, score, student_name, context)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert educational evaluator specializing in student teacher assessments. Provide clear, professional, evidence-based justifications."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            raise Exception(f"Failed to generate AI justification: {str(e)}")
    
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