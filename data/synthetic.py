"""
Synthetic data generation for testing AI-STER application
"""

import random
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any
from .rubrics import get_field_evaluation_items, get_ster_items, get_professional_dispositions

# Sample names for synthetic data
STUDENT_NAMES = [
    "Emily Johnson", "Michael Chen", "Sarah Williams", "David Rodriguez", "Ashley Brown",
    "Christopher Lee", "Jessica Garcia", "Matthew Davis", "Amanda Wilson", "Daniel Martinez",
    "Samantha Anderson", "Joshua Thompson", "Lauren Miller", "Andrew Taylor", "Rachel Moore",
    "Kevin Jackson", "Nicole White", "Tyler Harris", "Megan Martin", "Brandon Clark"
]

EVALUATOR_NAMES = [
    "Dr. Smith", "Prof. Johnson", "Ms. Anderson", "Mr. Thompson", "Dr. Williams",
    "Prof. Davis", "Ms. Miller", "Mr. Wilson", "Dr. Brown", "Prof. Jones",
    "Ms. Garcia", "Mr. Martinez", "Dr. Taylor", "Prof. Moore", "Ms. Jackson"
]

SUPERVISORS = [name for name in EVALUATOR_NAMES if name.startswith(("Dr.", "Prof."))]
COOPERATING_TEACHERS = [name for name in EVALUATOR_NAMES if name.startswith(("Ms.", "Mr."))]

def generate_synthetic_evaluations(
    count: int = 10,
    rubric_type: str = "both",
    score_distribution: str = "random"
) -> List[Dict[str, Any]]:
    """
    Generate synthetic evaluation data for testing
    
    Args:
        count: Number of evaluations to generate
        rubric_type: "field_evaluation", "ster", or "both"
        score_distribution: "random", "high_performing", "low_performing", "mixed"
    
    Returns:
        List of synthetic evaluation dictionaries
    """
    evaluations = []
    
    for i in range(count):
        # Determine rubric type for this evaluation
        if rubric_type == "both":
            eval_rubric_type = random.choice(["field_evaluation", "ster"])
        else:
            eval_rubric_type = rubric_type
        
        # Get appropriate items
        items = get_field_evaluation_items() if eval_rubric_type == "field_evaluation" else get_ster_items()
        dispositions = get_professional_dispositions()
        
        # Generate basic info
        student_name = random.choice(STUDENT_NAMES)
        evaluator_role = random.choice(["supervisor", "cooperating_teacher"])
        evaluator_name = random.choice(SUPERVISORS if evaluator_role == "supervisor" else COOPERATING_TEACHERS)
        
        # Generate scores based on distribution
        scores = generate_scores(items, score_distribution)
        disposition_scores = generate_disposition_scores(dispositions, score_distribution)
        
        # Generate justifications
        justifications = generate_justifications(items, scores)
        
        # Calculate total score
        total_score = sum(scores.values())
        
        # Determine status (some drafts, some completed)
        status = random.choices(["draft", "completed"], weights=[0.2, 0.8])[0]
        
        # Generate timestamps
        created_date = datetime.now() - timedelta(days=random.randint(0, 90))
        completed_date = None
        if status == "completed":
            completed_date = created_date + timedelta(hours=random.randint(1, 48))
        
        evaluation = {
            'id': str(uuid.uuid4()),
            'student_name': student_name,
            'evaluator_name': evaluator_name,
            'evaluator_role': evaluator_role,
            'rubric_type': eval_rubric_type,
            'scores': scores,
            'justifications': justifications,
            'disposition_scores': disposition_scores,
            'total_score': total_score,
            'status': status,
            'created_at': created_date.isoformat(),
            'completed_at': completed_date.isoformat() if completed_date else None,
            'is_synthetic': True  # Flag to identify synthetic data
        }
        
        evaluations.append(evaluation)
    
    return evaluations

def generate_scores(items: List[Dict], distribution: str) -> Dict[str, int]:
    """Generate scores for assessment items based on distribution pattern"""
    scores = {}
    
    for item in items:
        if distribution == "high_performing":
            # Mostly 2s and 3s
            score = random.choices([1, 2, 3], weights=[0.1, 0.6, 0.3])[0]
        elif distribution == "low_performing":
            # Mostly 0s and 1s
            score = random.choices([0, 1, 2], weights=[0.3, 0.5, 0.2])[0]
        elif distribution == "mixed":
            # Balanced distribution
            score = random.choices([0, 1, 2, 3], weights=[0.15, 0.25, 0.4, 0.2])[0]
        else:  # random
            score = random.randint(0, 3)
        
        scores[item['id']] = score
    
    return scores

def generate_disposition_scores(dispositions: List[Dict], distribution: str) -> Dict[str, int]:
    """Generate disposition scores (1-4 scale)"""
    scores = {}
    
    for disposition in dispositions:
        if distribution == "high_performing":
            # Mostly 3s and 4s
            score = random.choices([2, 3, 4], weights=[0.1, 0.6, 0.3])[0]
        elif distribution == "low_performing":
            # Mostly 1s and 2s
            score = random.choices([1, 2, 3], weights=[0.4, 0.5, 0.1])[0]
        elif distribution == "mixed":
            # Balanced distribution
            score = random.choices([1, 2, 3, 4], weights=[0.15, 0.25, 0.4, 0.2])[0]
        else:  # random
            score = random.randint(1, 4)
        
        scores[disposition['id']] = score
    
    return scores

def generate_justifications(items: List[Dict], scores: Dict[str, int]) -> Dict[str, str]:
    """Generate realistic justifications for assessment items"""
    justifications = {}
    
    # Templates for different score levels
    templates = {
        0: [
            "The student teacher did not demonstrate this competency during the observation period.",
            "No evidence of this skill was observed in the classroom setting.",
            "This area needs significant development and support."
        ],
        1: [
            "The student teacher showed beginning awareness of this competency but needs further development.",
            "Some evidence of this skill was observed, but implementation was inconsistent.",
            "The student teacher is making progress toward this competency with mentor support."
        ],
        2: [
            "The student teacher consistently demonstrated this competency during observations.",
            "Clear evidence of effective implementation was observed in multiple instances.",
            "The student teacher shows solid understanding and application of this skill."
        ],
        3: [
            "The student teacher exceeded expectations in this area with innovative approaches.",
            "Outstanding implementation was observed, serving as a model for other student teachers.",
            "The student teacher demonstrated advanced skill and independent application."
        ]
    }
    
    for item in items:
        score = scores.get(item['id'], 0)
        if score >= 2 or random.random() < 0.7:  # More justifications for higher scores
            template = random.choice(templates[score])
            justifications[item['id']] = template
    
    return justifications 