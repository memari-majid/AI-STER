# AI-STER: AI-Powered Student Teaching Evaluation Rubric

An application for the School of Education at Utah Valley University.

AI-STER is a web-based application designed to streamline the evaluation of student teachers by leveraging AI to assist with generating standards-aligned feedback. It implements the Utah State Board of Education (USBE) Student Teacher Evaluation Rubric (STER).

---

## ✨ Features

- **Comprehensive Evaluation:** Covers all 9 STER indicators, 8 field evaluation items, and 6 professional dispositions.
- **AI-Powered Feedback:** Uses OpenAI's GPT-4o-mini to generate smart, context-aware justifications for evaluations.
- **Compliance Validation:** Ensures all required fields and standards are met before submission.
- **Data Portability:** Easy JSON-based import and export of evaluation data.
- **No Database Needed:** Runs locally with simple JSON file storage.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- An OpenAI API Key provided by the university.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [repository-url]
    cd AI-STER
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure your environment:**
    - Rename `.env.example` to `.env`.
    - Add your OpenAI API key to the `.env` file:
      ```
      OPENAI_API_KEY="your-api-key-here"
      ```

4.  **Run the application:**
    ```bash
    streamlit run app.py
    ```
---

## 📚 Documentation

For complete project details, architecture, and guides, please see the main documentation hub:

➡️ **[View Full Documentation](./docs/README.md)**

---

## 📄 License

This project is the property of the School of Education at Utah Valley University. All rights reserved.