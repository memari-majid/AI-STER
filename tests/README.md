# Tests Directory

This directory contains all test files and test data for the AI-STER application.

## Structure

- `test_app_features.py` - Main test suite for application features
- `test_data/` - Sample data used for testing
  - `sample_lesson_plan.txt` - Example lesson plan for testing
- `test_output/` - Directory for test outputs (contents are gitignored)
  - `.gitkeep` - Preserves directory structure

## Running Tests

To run the tests:

```bash
python tests/test_app_features.py
```

## Note

Test outputs in `test_output/` are not tracked by git. This directory is used for temporary test artifacts during development.
