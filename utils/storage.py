"""
Storage utilities for AI-STER Streamlit application
Uses JSON files for simple local storage
"""

import json
import os
from typing import List, Dict, Any
from datetime import datetime

STORAGE_DIR = "data_storage"
EVALUATIONS_FILE = os.path.join(STORAGE_DIR, "evaluations.json")

def ensure_storage_dir():
    """Ensure storage directory exists"""
    if not os.path.exists(STORAGE_DIR):
        os.makedirs(STORAGE_DIR)

def save_evaluation(evaluation: Dict[str, Any], preserve_ai_original: bool = True) -> None:
    """Save an evaluation to storage
    
    Args:
        evaluation: The evaluation data to save
        preserve_ai_original: If True, preserves existing ai_original data when updating
    """
    ensure_storage_dir()
    
    evaluations = load_evaluations()
    
    # Update existing or add new
    existing_index = None
    existing_eval = None
    for i, existing in enumerate(evaluations):
        if existing.get('id') == evaluation.get('id'):
            existing_index = i
            existing_eval = existing
            break
    
    if existing_index is not None:
        # Preserve ai_original if it exists and preserve_ai_original is True
        if preserve_ai_original and existing_eval.get('ai_original'):
            evaluation['ai_original'] = existing_eval['ai_original']
            evaluation['ai_original_saved_at'] = existing_eval.get('ai_original_saved_at')
        
        evaluations[existing_index] = evaluation
    else:
        evaluations.append(evaluation)
    
    # Save to file
    with open(EVALUATIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(evaluations, f, indent=2, ensure_ascii=False)

def load_evaluations() -> List[Dict[str, Any]]:
    """Load all evaluations from storage"""
    if not os.path.exists(EVALUATIONS_FILE):
        return []
    
    try:
        with open(EVALUATIONS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def delete_evaluation(evaluation_id: str) -> bool:
    """Delete an evaluation by ID"""
    evaluations = load_evaluations()
    
    original_length = len(evaluations)
    evaluations = [e for e in evaluations if e.get('id') != evaluation_id]
    
    if len(evaluations) < original_length:
        with open(EVALUATIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(evaluations, f, indent=2, ensure_ascii=False)
        return True
    
    return False

def export_data() -> Dict[str, Any]:
    """Export all data for backup"""
    evaluations = load_evaluations()
    
    return {
        'evaluations': evaluations,
        'export_date': datetime.now().isoformat(),
        'version': '1.0'
    }

def import_data(data: Dict[str, Any]) -> int:
    """Import data from backup"""
    if 'evaluations' not in data:
        raise ValueError("Invalid data format: missing 'evaluations' key")
    
    imported_evaluations = data['evaluations']
    if not isinstance(imported_evaluations, list):
        raise ValueError("Invalid data format: 'evaluations' must be a list")
    
    current_evaluations = load_evaluations()
    
    # Merge evaluations, avoiding duplicates
    existing_ids = {e.get('id') for e in current_evaluations}
    new_evaluations = []
    imported_count = 0
    
    for evaluation in imported_evaluations:
        if evaluation.get('id') not in existing_ids:
            new_evaluations.append(evaluation)
            imported_count += 1
    
    # Save merged data
    all_evaluations = current_evaluations + new_evaluations
    
    ensure_storage_dir()
    with open(EVALUATIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_evaluations, f, indent=2, ensure_ascii=False)
    
    return imported_count

def clear_all_data() -> None:
    """Clear all stored data"""
    if os.path.exists(EVALUATIONS_FILE):
        os.remove(EVALUATIONS_FILE)

def get_evaluation_by_id(evaluation_id: str) -> Dict[str, Any]:
    """Get a specific evaluation by ID"""
    evaluations = load_evaluations()
    
    for evaluation in evaluations:
        if evaluation.get('id') == evaluation_id:
            return evaluation
    
    return None

def save_ai_original(evaluation_id: str, ai_data: Dict[str, Any]) -> bool:
    """Save the AI-generated original version of an evaluation
    
    Args:
        evaluation_id: The evaluation ID
        ai_data: The AI-generated data to preserve (justifications, analyses, etc.)
        
    Returns:
        True if saved successfully, False otherwise
    """
    evaluations = load_evaluations()
    
    for i, evaluation in enumerate(evaluations):
        if evaluation.get('id') == evaluation_id:
            # Save AI original data
            evaluation['ai_original'] = {
                'justifications': ai_data.get('justifications', {}),
                'ai_analyses': ai_data.get('ai_analyses', {}),
                'scores': ai_data.get('scores', {}),
                'observation_notes': ai_data.get('observation_notes', ''),
                'saved_at': datetime.now().isoformat()
            }
            evaluation['has_ai_original'] = True
            evaluation['ai_original_saved_at'] = datetime.now().isoformat()
            
            # Save back to file
            with open(EVALUATIONS_FILE, 'w', encoding='utf-8') as f:
                json.dump(evaluations, f, indent=2, ensure_ascii=False)
            
            return True
    
    return False

def get_evaluation_comparison(evaluation_id: str) -> Dict[str, Any]:
    """Get comparison data between AI original and current version
    
    Returns dict with:
        - current: Current evaluation data
        - ai_original: Original AI-generated data
        - differences: List of fields that differ
    """
    evaluation = get_evaluation_by_id(evaluation_id)
    if not evaluation or not evaluation.get('ai_original'):
        return None
    
    differences = []
    ai_original = evaluation.get('ai_original', {})
    
    # Compare justifications
    current_just = evaluation.get('justifications', {})
    ai_just = ai_original.get('justifications', {})
    
    for item_id in set(list(current_just.keys()) + list(ai_just.keys())):
        if current_just.get(item_id, '') != ai_just.get(item_id, ''):
            differences.append({
                'field': 'justification',
                'item_id': item_id,
                'ai_value': ai_just.get(item_id, ''),
                'current_value': current_just.get(item_id, '')
            })
    
    # Compare scores
    current_scores = evaluation.get('scores', {})
    ai_scores = ai_original.get('scores', {})
    
    for item_id in set(list(current_scores.keys()) + list(ai_scores.keys())):
        if current_scores.get(item_id) != ai_scores.get(item_id):
            differences.append({
                'field': 'score',
                'item_id': item_id,
                'ai_value': ai_scores.get(item_id),
                'current_value': current_scores.get(item_id)
            })
    
    return {
        'current': evaluation,
        'ai_original': ai_original,
        'differences': differences,
        'has_changes': len(differences) > 0
    } 