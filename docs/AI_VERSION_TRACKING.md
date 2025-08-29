# AI Version Tracking Feature

## Overview

The AI Version Tracking feature allows supervisors to save a snapshot of AI-generated evaluation content before making any modifications. This is crucial for research purposes to compare what AI generated versus how supervisors revised the feedback.

## How It Works

### 1. Generating AI Content
When creating a new evaluation:
1. Upload or paste a lesson plan (optional but recommended)
2. Enter detailed observation notes
3. Click "🤖 Generate AI Analysis & Begin Scoring"
4. The AI will generate evidence-based justifications for each competency

### 2. Saving AI Version
After AI analysis is complete:
1. A new button appears: "💾 Save AI Version"
2. Click this button BEFORE making any modifications
3. The system will save:
   - All AI-generated justifications
   - Initial scores (if any)
   - Observation notes at the time of generation
   - Timestamp of when saved

### 3. Making Modifications
After saving the AI version:
1. Review and modify scores as needed
2. Edit justifications to add your professional judgment
3. Complete the evaluation normally
4. Save as draft or complete

### 4. Viewing Comparisons
To compare AI vs Supervisor versions:
1. Navigate to "🔬 Research Comparison" in the menu
2. Select an evaluation that has a saved AI version
3. View:
   - Total number of changes
   - Score changes (with direction indicators)
   - Justification modifications (side-by-side comparison)
4. Export comparison data as JSON for further analysis

## Data Structure

### AI Original Storage
```json
{
  "ai_original": {
    "justifications": { "item_id": "AI-generated text..." },
    "ai_analyses": { "item_id": "AI analysis..." },
    "scores": { "item_id": 2 },
    "observation_notes": "Original observation notes",
    "saved_at": "2025-01-01T12:00:00"
  },
  "has_ai_original": true,
  "ai_original_saved_at": "2025-01-01T12:00:00"
}
```

### Comparison Output
```json
{
  "differences": [
    {
      "field": "justification",
      "item_id": "LL2",
      "ai_value": "AI-generated justification...",
      "current_value": "Supervisor-modified justification..."
    },
    {
      "field": "score",
      "item_id": "IC1",
      "ai_value": 2,
      "current_value": 3
    }
  ],
  "has_changes": true
}
```

## Research Benefits

1. **Quality Analysis**: Compare AI accuracy with expert judgment
2. **Pattern Recognition**: Identify areas where AI consistently needs correction
3. **Training Data**: Use differences to improve AI models
4. **Efficiency Metrics**: Measure time saved vs. modifications needed
5. **Bias Detection**: Analyze patterns in score adjustments

## Best Practices

1. **Always save AI version** immediately after generation
2. **Don't regenerate** AI analysis after saving the version
3. **Complete modifications** in one session when possible
4. **Export data regularly** for backup and analysis
5. **Document significant changes** in justification text

## Technical Details

- AI versions are preserved when updating evaluations
- The system tracks the exact timestamp of AI version creation
- Comparison logic handles missing or added content gracefully
- All data is stored in JSON format for easy analysis
- No personal data is sent to external services

## Troubleshooting

**Q: The "Save AI Version" button doesn't appear**
A: Ensure you've generated AI analysis first. The button only appears after AI content is generated.

**Q: Can I save multiple AI versions?**
A: No, only one AI original version is saved per evaluation. This preserves the first AI-generated state.

**Q: What if I forget to save the AI version?**
A: Unfortunately, once you modify the content, the original AI version cannot be recovered. Always save before editing.

**Q: Can I edit the AI version after saving?**
A: No, the AI version is immutable once saved. This ensures research data integrity.

## Future Enhancements

- Batch export of all AI comparisons
- Statistical analysis dashboard
- ML model training integration
- Automated insight generation
- Version history timeline view
