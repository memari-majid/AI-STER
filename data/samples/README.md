# AI-STER Sample Files

This directory contains sample lesson plans and evaluations for testing and improving AI-STER's synthetic data generation.

## Directory Structure

```
data/samples/
├── lesson_plans/           # Utah DOE lesson plan samples
├── evaluations/           # Completed evaluation examples  
├── templates/             # Official Utah DOE templates
├── standards_references/  # Utah Core Standards documents
└── sample_processor.py    # Analysis and processing script
```

## How to Use

### 1. Upload Your Sample Files

**Lesson Plans** (`lesson_plans/`):
- Utah DOE approved lesson plan formats
- UEN (Utah Education Network) templates
- USBE (Utah State Board of Education) examples
- Real teacher lesson plans aligned to Utah Core Standards

**Evaluations** (`evaluations/`):
- Completed STER evaluations
- Field evaluation examples
- Supervisor feedback samples
- Student teacher assessment rubrics

**Templates** (`templates/`):
- Official Utah DOE templates
- Blank evaluation forms
- Lesson plan templates

**Standards References** (`standards_references/`):
- Utah Core Standards documents
- Subject-specific standards guides
- Grade-level expectations

### 2. Run the Analysis Script

```bash
# From the AI-STER root directory
cd data
python sample_processor.py
```

This will:
- ✅ Scan all sample files
- 📚 Analyze lesson plans for Utah standards and structure  
- 🤖 Test AI analysis accuracy against real samples
- 📊 Generate comprehensive analysis report
- 💡 Provide recommendations for improving synthetic data

### 3. View Results

The script generates `sample_analysis_report.json` with:
- File inventory and processing status
- Utah Core Standards found in samples
- Grade levels and subjects detected
- AI analysis test results
- Recommendations for improving synthetic data generation

## Supported File Formats

### Currently Supported
- `.txt` - Plain text files
- `.md` - Markdown files

### Optional Support (install additional libraries)
- `.pdf` - PDF documents (`pip install PyPDF2`)
- `.docx` - Word documents (`pip install python-docx`)

## Using Samples to Improve AI-STER

### 1. Test AI Analysis Accuracy
Compare AI extraction against real lesson plans:
```python
from data.sample_processor import SampleProcessor
processor = SampleProcessor()
results = processor.test_ai_analysis()
```

### 2. Extract Real Utah Standards
Use found standards to update synthetic data:
```python
analysis = processor.analyze_lesson_plans()
utah_standards = analysis["utah_standards_found"]
# Add these to data/utah_lesson_plans.py
```

### 3. Improve Synthetic Justifications
Reference real evaluation justifications:
- Compare AI-generated justifications with real supervisor feedback
- Update justification templates in `services/openai_service.py`
- Enhance rubric-based scoring in `data/synthetic.py`

### 4. Validate Grade/Subject Categories
Ensure synthetic data matches real samples:
- Check grade level patterns match your school district
- Verify subject areas align with actual placements
- Update categorization logic if needed

## Integration with AI-STER

### Lesson Plan Analysis
Real samples help improve:
- `services/openai_service.analyze_lesson_plan()`
- Utah Core Standards recognition
- Teacher name extraction accuracy
- Subject/grade level detection

### Evaluation Generation  
Real evaluations improve:
- `data/synthetic.py` justification templates
- Scoring distribution patterns
- Supervisor feedback quality
- Rubric code accuracy

### Testing & Validation
Use samples to:
- Test AI analysis before deployment
- Validate synthetic data realism
- Compare AI justifications with human evaluators
- Ensure Utah DOE compliance

## Best Practices

1. **Anonymize Data**: Remove student names and sensitive information
2. **Organize by Type**: Group similar lesson plans and evaluations
3. **Document Sources**: Note where samples came from (district, teacher, etc.)
4. **Regular Testing**: Re-run analysis after AI updates
5. **Quality Control**: Review AI analysis results for accuracy

## Troubleshooting

### No Files Found
- Ensure files are in correct subdirectories
- Check file permissions
- Verify file formats are supported

### AI Analysis Fails
- Ensure OpenAI API key is configured in `.env`
- Check file content is readable (not corrupted)
- Try with smaller/simpler files first

### Poor Extraction Results
- Sample files may be formatted differently than expected
- Consider installing additional file processing libraries
- Manual review may be needed for complex documents

## Contributing Samples

When adding new samples:
1. Remove any personally identifiable information
2. Ensure Utah DOE compliance
3. Include variety of grade levels and subjects
4. Add both high-quality and problematic examples
5. Document any special formatting or requirements 