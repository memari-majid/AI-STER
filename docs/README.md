# AI-STER Documentation Hub

This directory contains all project documentation, consolidated for clarity and simplicity.

---

## 1. Project Overview

_(This content was formerly the root `README.md`)_

AI-STER is a web-based application designed to streamline the evaluation of student teachers by leveraging AI to assist with generating standards-aligned feedback. It implements the Utah State Board of Education (USBE) Student Teacher Evaluation Rubric (STER).

### ✨ Features

- **Comprehensive Evaluation:** Covers all 9 STER indicators, 8 field evaluation items, and 6 professional dispositions.
- **AI-Powered Feedback:** Uses OpenAI's GPT-4o-mini to generate smart, context-aware justifications for evaluations.
- **Compliance Validation:** Ensures all required fields and standards are met before submission.
- **Data Portability:** Easy JSON-based import and export of evaluation data.
- **No Database Needed:** Runs locally with simple JSON file storage.

---

## 2. Master Documents

All detailed documentation has been merged into the following master files:

- [**PROJECT.md](./PROJECT.md) - The complete project plan, history, and technical architecture.
- [**PROCESS.md](./PROCESS.md) - All processes, including evaluation workflows, meeting notes, and source materials.
- [**DEPLOYMENT_GUIDE.md**](./DEPLOYMENT_GUIDE.md) - A unified guide for all deployment scenarios.

---

## 3. Contributor & Project Files

- [**CONTRIBUTING.md**](./CONTRIBUTING.md) - Guidelines for contributing to the project.
- [**CHANGELOG.md**](./CHANGELOG.md) - A log of all notable changes.

---

## 4. Root Directory Guide

This guide provides a map to the AI-STER project repository.

- **`/` (Root Directory)**
  - `app.py`: The main Streamlit application prototype.
  - `requirements.txt`: Python package dependencies for the project.
  - `README.md`: The main project entry point, linking to this documentation hub.
  - `.env.example`: Template for environment variables (e.g., API keys).
  - `LICENSE`: The project's open-source license.
  - `.gitignore`: Specifies files and directories for Git to ignore.

- **`/docs`**: Contains all project documentation.
  - `README.md`: This file, the central documentation hub.
  - `PROJECT.md`: The master document for the project plan, history, and architecture.
  - `PROCESS.md`: All procedural documentation, including meeting notes and evaluation workflows.
  - `DEPLOYMENT_GUIDE.md`: Instructions for deploying the application.
  - `CHANGELOG.md`: A log of notable changes to the project.
  - `CONTRIBUTING.md`: Guidelines for contributing to the project.

- **`/data`**: Contains all data-related modules and sample materials.
  - `rubrics.py`: Defines the core evaluation rubrics and competencies.
  - `synthetic.py`: Generates synthetic data for testing and demonstration.
  - `utah_lesson_plans.py`: Manages real Utah lesson plan data.
  - `process_samples.py`: A script for processing files in the `samples` directory.
  - `samples/`: A directory containing sample evaluation documents, lesson plans, and other materials for testing and reference.

- **`/services`**: Houses services that connect to external APIs.
  - `openai_service.py`: Manages all interactions with the OpenAI API.

- **`/utils`**: Contains core utility functions used throughout the application.
  - `storage.py`: Handles data storage and retrieval.
  - `validation.py`: Provides data validation functions.

- **`/data_storage`**: The default location for storing runtime data, such as evaluation JSON files.