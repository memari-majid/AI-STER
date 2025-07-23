"""
Validation utilities for AI-STER evaluations
"""

from typing import List, Dict, Any

def validate_evaluation(
    scores: Dict[str, int],
    justifications: Dict[str, str],
    disposition_scores: Dict[str, int],
    items: List[Dict],
    dispositions: List[Dict]
) -> List[str]:
    """
    Validate evaluation data before completion
    
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    # Check that all items are scored (including "not_observed" as valid)
    item_ids = {item['id'] for item in items}
    scored_item_ids = set(scores.keys())
    
    missing_scores = item_ids - scored_item_ids
    if missing_scores:
        errors.append(f"Missing scores for items: {', '.join(sorted(missing_scores))}")
    
    # Check minimum score requirements (all scored items must score >= 2, except "not_observed")
    failing_items = []
    for item_id, score in scores.items():
        if score != "not_observed" and isinstance(score, int) and score < 2:
            failing_items.append(item_id)
    
    if failing_items:
        errors.append(f"Items scoring below Level 2 (required minimum): {', '.join(sorted(failing_items))}")
    
    # Check justifications for items scoring >= 2 (not required for "not_observed")
    missing_justifications = []
    for item_id, score in scores.items():
        if isinstance(score, int) and score >= 2 and not justifications.get(item_id, '').strip():
            missing_justifications.append(item_id)
    
    if missing_justifications:
        errors.append(f"Missing justifications for items scoring Level 2+: {', '.join(sorted(missing_justifications))}")
    
    # Check disposition scores
    disposition_ids = {disp['id'] for disp in dispositions}
    scored_disposition_ids = set(disposition_scores.keys())
    
    missing_dispositions = disposition_ids - scored_disposition_ids
    if missing_dispositions:
        errors.append(f"Missing disposition scores: {', '.join(sorted(missing_dispositions))}")
    
    # Check that all dispositions score >= 3
    failing_dispositions = []
    for disp_id, score in disposition_scores.items():
        if score < 3:
            failing_dispositions.append(disp_id)
    
    if failing_dispositions:
        errors.append(f"Dispositions scoring below Level 3 (required): {', '.join(sorted(failing_dispositions))}")
    
    return errors

def calculate_score(scores: Dict[str, int]) -> int:
    """Calculate total score from individual item scores (excludes 'not_observed')"""
    return sum(score for score in scores.values() if isinstance(score, int))

def get_score_summary(scores: Dict[str, int]) -> Dict[str, Any]:
    """Get summary statistics for scores"""
    if not scores:
        return {
            'total': 0,
            'average': 0.0,
            'distribution': {0: 0, 1: 0, 2: 0, 3: 0, 'not_observed': 0},
            'meets_minimum': False
        }
    
    # Only count numeric scores for calculations
    numeric_scores = [score for score in scores.values() if isinstance(score, int)]
    total = sum(numeric_scores)
    average = total / len(numeric_scores) if numeric_scores else 0.0
    
    distribution = {level: 0 for level in range(4)}
    distribution['not_observed'] = 0
    
    for score in scores.values():
        if score == "not_observed":
            distribution['not_observed'] += 1
        elif isinstance(score, int):
            distribution[score] += 1
    
    # Check if meets minimum requirements (all numeric scores >= 2)
    meets_minimum = all(score >= 2 for score in numeric_scores)
    
    return {
        'total': total,
        'average': average,
        'distribution': distribution,
        'meets_minimum': meets_minimum
    }

def get_disposition_summary(disposition_scores: Dict[str, int]) -> Dict[str, Any]:
    """Get summary for disposition scores"""
    if not disposition_scores:
        return {
            'average': 0.0,
            'distribution': {1: 0, 2: 0, 3: 0, 4: 0},
            'meets_requirement': False
        }
    
    average = sum(disposition_scores.values()) / len(disposition_scores)
    
    distribution = {level: 0 for level in range(1, 5)}
    for score in disposition_scores.values():
        distribution[score] += 1
    
    # Check if meets requirements (all scores >= 3)
    meets_requirement = all(score >= 3 for score in disposition_scores.values())
    
    return {
        'average': average,
        'distribution': distribution,
        'meets_requirement': meets_requirement
    } 