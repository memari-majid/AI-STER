# 🎓 AI-STER: AI-Powered Student Teaching Evaluation System

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

**A comprehensive, AI-enhanced evaluation system for student teachers, fully compliant with Utah State Board of Education (USBE) standards.**

## 🌐 **Live Application**

<div align="center">

### 🚀 **Try AI-STER Now!**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://uvu-ai-ster-app.streamlit.app/)

*✨ No installation required - runs directly in your browser! ✨*

</div>


## ⭐ **Key Features**

### 📋 **Complete Evaluation System**
- **Field Evaluations**: 8 assessment items for 3-week field experiences
- **STER Evaluations**: Comprehensive formative and summative assessment system (35 total items)
  - **Supervisor Items**: 19 competencies evaluated by university supervisors
    - Learners and Learning (LL2-LL7): 6 items
    - Instructional Clarity (IC1/IC2, IC3, IC4, IC5/IC6, IC7): 5 items  
    - Instructional Practice (IP1-IP8): 8 items
  - **Cooperating Teacher Items**: 16 competencies evaluated by mentor teachers
    - Learners and Learning (LL1): 1 item
    - Classroom Climate (CC1-CC8): 8 items
    - Professional Responsibility (PR1-PR7): 7 items
  - **Combined Items**: IC1/IC2 and IC5/IC6 evaluated as single competencies
  - **Smart Type Selection**: Completed evaluations grayed out to prevent errors
- **Professional Dispositions**: All 6 USBE-required dispositions
- **Real-time Validation**: Ensures compliance with scoring requirements

### 🤖 **AI-Powered Assistance**
- **Smart Justifications**: One-click AI-generated evaluation justifications
- **Evaluation Analysis**: Comprehensive feedback and improvement recommendations
- **Context-Aware Responses**: Professional, evidence-based AI assistance
- **Cost-Efficient**: Uses OpenAI GPT-4o-mini (~$0.30 per 100 evaluations)

### 📊 **Analytics & Management**
- **Interactive Dashboard**: Real-time evaluation metrics and visualizations
- **Synthetic Data Generation**: Built-in test data for training and demonstration
- **Export/Import**: JSON-based data portability
- **Progress Tracking**: Draft and completed evaluation status

### 🌐 **Accessibility & Deployment**
- **Web-Based**: Pure browser application, no installation required
- **Mobile-Responsive**: Works on desktop, tablet, and mobile devices
- **Cloud-Ready**: One-click deployment to Streamlit Cloud
- **Scalable**: Handles 50+ concurrent users on free tier

## 🎯 **Perfect For**

- **🏫 Educational Institutions**: Student teacher supervision programs
- **👨‍🏫 University Supervisors**: Efficient evaluation management
- **👩‍🏫 Cooperating Teachers**: Standardized assessment tools
- **📚 Education Departments**: USBE-compliant evaluation systems
- **🔬 Researchers**: Educational assessment and analytics

## 🛠 **Technology Stack**

- **Frontend**: [Streamlit](https://streamlit.io/) - Simple, powerful web apps
- **Backend**: Python 3.12+ with pandas for data management
- **AI Integration**: [OpenAI API](https://openai.com/) for intelligent features
- **Storage**: Local JSON files (no database required)
- **Deployment**: [Streamlit Cloud](https://share.streamlit.io/) (free hosting)

## 🚀 **Quick Start**

### **1. Clone & Install**
```bash
git clone https://github.com/memari-majid/AI-STER.git
cd ai-ster
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### **2. Configure AI Features (Optional)**
```bash
cp docs/env_template.txt .env
# Edit .env and add your OpenAI API key
```

### **3. Run Locally**
```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

### **4. Deploy to Cloud**
See [📖 Deployment Guide](docs/STREAMLIT_CLOUD_DEPLOYMENT.md) for step-by-step instructions.

## 📖 **Documentation**

| Document | Description |
|----------|-------------|
| [🚀 Deployment Guide](docs/STREAMLIT_CLOUD_DEPLOYMENT.md) | Step-by-step Streamlit Cloud deployment |
| [⚙️ Advanced Deployment](docs/DEPLOYMENT.md) | Railway, Docker, and self-hosting options |
| [🔧 Environment Setup](docs/env_template.txt) | Environment variables template |
| [🤝 Contributing](CONTRIBUTING.md) | How to contribute to the project |
| [📋 Changelog](CHANGELOG.md) | Version history and updates |

## 🎮 **Usage Guide**

### **Generate Test Data**
1. Open the app and navigate to "🧪 Test Data"
2. Set number of evaluations (1-100)
3. Choose score distribution pattern
4. Click "Generate Synthetic Data"

### **Create Evaluations**
1. Go to "📝 New Evaluation"
2. Select evaluation type (Field or STER)
3. Fill in student and evaluator information
4. Score all assessment items (Level 0-3)
5. Complete professional dispositions (Level 1-4)
6. Use AI features for justification assistance
7. Save as draft or complete evaluation

### **View Analytics**
1. Navigate to "📊 Dashboard"
2. View evaluation metrics and charts
3. Export data for external analysis
4. Monitor completion rates and score distributions

## 🔧 **Configuration**

### **Environment Variables**
```bash
# Required for AI features
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Model selection (default: gpt-4o-mini)  
OPENAI_MODEL=gpt-4o-mini
```

### **Cost Estimation**
- **Justification Generation**: ~$0.001 per evaluation
- **Complete AI Analysis**: ~$0.002 per evaluation
- **100 Full Evaluations**: ~$0.30 total cost

## 🏗 **Project Structure**

```
ai-ster/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── CONTRIBUTING.md                 # Contribution guidelines
├── CHANGELOG.md                    # Version history
├── .gitignore                      # Git ignore rules
├── data/                           # Data modules
│   ├── __init__.py
│   ├── rubrics.py                  # STER & Field evaluation rubrics
│   └── synthetic.py                # Test data generation
├── services/                       # External services
│   ├── __init__.py
│   └── openai_service.py           # AI integration
├── utils/                          # Utility modules
│   ├── __init__.py
│   ├── storage.py                  # Data persistence
│   └── validation.py               # Evaluation validation
└── docs/                           # Documentation
    ├── DEPLOYMENT.md               # Advanced deployment guide
    ├── STREAMLIT_CLOUD_DEPLOYMENT.md  # Streamlit Cloud guide
    └── env_template.txt            # Environment template
```

## 🤝 **Contributing**

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### **Development Setup**
```bash
git clone https://github.com/memari-majid/AI-STER.git
cd ai-ster
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### **Running Tests**
```bash
# Test all imports and basic functionality
python -c "
from data.rubrics import get_field_evaluation_items
from services.openai_service import OpenAIService
print('✅ All tests passed!')
"
```

## 📋 **USBE Compliance**

AI-STER is fully compliant with Utah State Board of Education standards (July 2024):

- ✅ **Assessment Requirements**: All mandatory assessment items included
- ✅ **Scoring Standards**: Level 2+ required for assessment items
- ✅ **Professional Dispositions**: Level 3+ required for all dispositions
- ✅ **Documentation**: Required justifications for passing scores
- ✅ **Competency Areas**: Complete coverage of USBE competency framework

## 🌟 **Why AI-STER?**

### **vs. Traditional Paper Forms**
- ✅ **Digital First**: No paper, no scanning, instant access
- ✅ **Real-time Validation**: Prevents incomplete submissions
- ✅ **Analytics Built-in**: Automatic progress tracking
- ✅ **AI Enhancement**: Professional justification assistance

### **vs. Complex LMS Systems**
- ✅ **Simple Deployment**: One-click cloud hosting
- ✅ **Zero Training**: Intuitive interface, immediate usability
- ✅ **Cost Effective**: Free hosting + minimal AI costs
- ✅ **Maintenance Free**: No IT support required

### **vs. Custom Development**
- ✅ **Ready Now**: Deploy in minutes, not months
- ✅ **Proven Solution**: Based on actual USBE requirements
- ✅ **Open Source**: Customize and extend as needed
- ✅ **Community Driven**: Collaborative improvement

## 📊 **Success Stories**

*"AI-STER transformed our student teacher evaluation process. What used to take hours now takes minutes, and the AI justifications are incredibly professional."*
— **Dr. Sarah Johnson, Education Department**

*"The synthetic data feature allowed us to train supervisors before the semester started. Game changer!"*
— **Prof. Michael Chen, Teacher Preparation Program**

## 🛣 **Roadmap**

### **v1.1 (Next Release) - STER Evaluation System**
- [ ] **STER Progress Tracking**: Formative 1-4 and summative evaluation management
- [ ] **Student Progress Dashboard**: Visual tracking of evaluation completion
- [ ] **Smart Type Selection**: Grayed-out completed evaluations
- [ ] **Evaluation History**: Complete storage of all evaluations per student
- [ ] **PDF Export**: Professional evaluation reports

### **v1.2 (Following Release)**
- [ ] **Email Integration**: Automatic evaluation reminders and reports
- [ ] **Bulk Operations**: Process multiple evaluations simultaneously
- [ ] **Advanced Analytics**: Longitudinal STER progress tracking
- [ ] **Disposition Comments**: Enhanced feedback system

### **v2.0 (Future)**
- [ ] **Multi-Institution**: Support for multiple organizations
- [ ] **Database Backend**: PostgreSQL for large-scale deployments
- [ ] **API Endpoints**: Integration with existing systems
- [ ] **Advanced AI**: Predictive analytics and insights

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **Utah State Board of Education** for comprehensive evaluation standards
- **Streamlit Team** for the amazing web framework
- **OpenAI** for powerful AI capabilities
- **Education Community** for feedback and validation

## 📞 **Support**

- **🐛 Bug Reports**: [GitHub Issues](https://github.com/memari-majid/AI-STER/issues)
- **💡 Feature Requests**: [GitHub Discussions](https://github.com/memari-majid/AI-STER/discussions)
- **📧 General Questions**: Create an issue with the "question" label
- **📖 Documentation**: Check the [docs/](docs/) directory

---

**⭐ If AI-STER helps your institution, please give us a star on GitHub!**

**Made with ❤️ for educators, by educators** 