"""
Storage utilities for AI-STER Streamlit application
Uses JSON files for simple local storage
"""

import json
import os
import streamlit as st
from typing import List, Dict, Any, Optional
from datetime import datetime

STORAGE_DIR = "data_storage"
EVALUATIONS_FILE = os.path.join(STORAGE_DIR, "evaluations.json")

def ensure_storage_dir():
    """Ensure storage directory exists"""
    if not os.path.exists(STORAGE_DIR):
        os.makedirs(STORAGE_DIR)

def save_evaluation(evaluation: Dict[str, Any]) -> None:
    """Save an evaluation to storage"""
    ensure_storage_dir()
    
    load_evaluations.clear()
    evaluations = load_evaluations()
    
    # Update existing or add new
    existing_index = None
    for i, existing in enumerate(evaluations):
        if existing.get('id') == evaluation.get('id'):
            existing_index = i
            break
    
    if existing_index is not None:
        evaluations[existing_index] = evaluation
    else:
        evaluations.append(evaluation)
    
    # Save to file
    with open(EVALUATIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(evaluations, f, indent=2, ensure_ascii=False)

@st.cache_data
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
    load_evaluations.clear()
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
    
    load_evaluations.clear()
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
    load_evaluations.clear()

def get_evaluation_by_id(evaluation_id: str) -> Optional[Dict[str, Any]]:
    """Get a specific evaluation by ID"""
    evaluations = load_evaluations()
    
    for evaluation in evaluations:
        if evaluation.get('id') == evaluation_id:
            return evaluation
    
    return None   