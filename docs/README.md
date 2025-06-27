# 📖 AI-STER Documentation

Welcome to the AI-STER documentation! This directory contains comprehensive guides for deploying, configuring, and contributing to the AI-powered Student Teaching Evaluation Rubric System.

## 📚 **Documentation Index**

### 🚀 **Deployment Guides**

| Document | Description | Audience |
|----------|-------------|----------|
| [🌐 Streamlit Cloud Deployment](STREAMLIT_CLOUD_DEPLOYMENT.md) | **Recommended**: Step-by-step guide for free Streamlit Cloud hosting | All users |
| [⚙️ Advanced Deployment Options](DEPLOYMENT.md) | Railway, Docker, self-hosting, and enterprise deployment | Advanced users |

### 🔧 **Configuration**

| Document | Description | Audience |
|----------|-------------|----------|
| [🌍 Environment Variables](env_template.txt) | Template for environment configuration | Developers |

### 📋 **Original Requirements & Research**

| Document | Description | Purpose |
|----------|-------------|----------|
| [📊 STER CT&US FINAL 3.md](STER%20CT&US%20FINAL%203.md) | Complete USBE evaluation rubric standards | Reference material |
| [📝 Field Evaluations.md](Field%20Evaluations.md) | Field evaluation requirements and rubrics | Educational standards |
| [📈 Project History.md](Project_History.md) | Original project README and requirements | Historical context |

### 🏗 **Development History**

| Document | Description | Purpose |
|----------|-------------|----------|
| [🎯 AI-STER Implementation Plan.md](AI-STER_Implementation_Plan.md) | Original implementation strategy | Development reference |
| [💻 Local Implementation Plan.md](Local_Implementation_Plan.md) | Local development approach | Technical planning |
| [🔍 Codebase Review Summary.md](Codebase_Review_Summary.md) | Code analysis and decisions | Development insights |

### 📋 **Quick Reference**

#### **Deployment Comparison**
| Platform | Cost | Complexity | Best For |
|----------|------|------------|----------|
| **Streamlit Cloud** | FREE | ⭐ | Education, demos, testing |
| **Railway** | $5/month | ⭐⭐ | Professional, institutions |
| **Self-Hosted** | Server costs | ⭐⭐⭐ | Enterprise, custom needs |

#### **Common Commands**
```bash
# Local development
streamlit run app.py

# Install dependencies
pip install -r requirements.txt

# Test all functionality
python -c "from data.rubrics import get_field_evaluation_items; print('✅ Working!')"
```

## 🎯 **Getting Started**

### **New to AI-STER?**
1. Start with the main [README.md](../README.md) for project overview
2. Follow the [Quick Start guide](../README.md#-quick-start) for local setup
3. Try the [Streamlit Cloud deployment](STREAMLIT_CLOUD_DEPLOYMENT.md) for hosting

### **Understanding the Requirements?**
1. Read [STER CT&US FINAL 3.md](STER%20CT&US%20FINAL%203.md) for complete USBE standards
2. Review [Field Evaluations.md](Field%20Evaluations.md) for field experience requirements
3. Check [Project History.md](Project_History.md) for original context

### **Want to Contribute?**
1. Read the [Contributing Guidelines](../CONTRIBUTING.md)
2. Check the [Changelog](../CHANGELOG.md) for current development
3. Review the [Code of Conduct](../CONTRIBUTING.md#-code-of-conduct)

### **Need Help?**
1. Check the [troubleshooting sections](DEPLOYMENT.md#-troubleshooting) in deployment guides
2. Search [GitHub Issues](https://github.com/YOUR_USERNAME/ai-ster/issues)
3. Create a new issue with detailed information

## 🏗 **Architecture Overview**

### **Project Structure**
```
ai-ster/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Dependencies
├── data/                     # Rubric and test data
│   ├── rubrics.py           # STER & Field evaluation rubrics
│   └── synthetic.py         # Test data generation
├── services/                 # External integrations
│   └── openai_service.py    # AI functionality
├── utils/                    # Core utilities
│   ├── storage.py           # Data persistence
│   └── validation.py        # Evaluation validation
└── docs/                     # This documentation
    ├── README.md            # This file
    ├── DEPLOYMENT.md        # Advanced deployment
    ├── STREAMLIT_CLOUD_DEPLOYMENT.md  # Streamlit Cloud guide
    ├── env_template.txt     # Environment setup
    ├── STER CT&US FINAL 3.md  # Original USBE standards
    ├── Field Evaluations.md   # Field requirements
    ├── Project_History.md      # Original project README
    ├── AI-STER_Implementation_Plan.md  # Implementation strategy
    ├── Local_Implementation_Plan.md   # Local development plan
    └── Codebase_Review_Summary.md     # Development decisions
```

### **Key Components**

#### **Evaluation System**
- **Field Evaluations**: 8 assessment items for 3-week experiences
- **STER Evaluations**: 9 comprehensive summative items
- **Professional Dispositions**: 6 USBE-required dispositions
- **Validation**: Real-time compliance checking

#### **AI Integration**
- **OpenAI GPT-4o-mini**: Cost-efficient AI model
- **Smart Justifications**: Context-aware evaluation text
- **Analysis**: Comprehensive feedback and recommendations
- **Cost**: ~$0.30 per 100 AI-enhanced evaluations

#### **Data Management**
- **Local Storage**: JSON-based, no database required
- **Synthetic Data**: Built-in test data generation
- **Export/Import**: Full data portability
- **Validation**: USBE compliance enforcement

## 🎓 **Educational Context**

### **USBE Compliance**
AI-STER implements Utah State Board of Education standards (July 2024):
- All required assessment items and competency areas
- Proper scoring levels (2+ for items, 3+ for dispositions)
- Required justifications for passing scores
- Professional disposition tracking

### **Use Cases**
- **University Programs**: Student teacher supervision
- **School Districts**: Cooperating teacher evaluations
- **Research**: Educational assessment analytics
- **Training**: Supervisor and teacher preparation

## 🔄 **Updates and Maintenance**

### **Staying Current**
- **GitHub Releases**: Follow for updates and new features
- **Documentation**: Updated with each release
- **Deployment**: Most platforms auto-update from GitHub

### **Version Support**
- **Current**: v1.0.0 (full support)
- **Previous**: Development versions (deprecated)
- **Future**: See [roadmap](../CHANGELOG.md#-future-roadmap)

## 🤝 **Community**

### **Getting Involved**
- **GitHub Discussions**: Feature requests and questions
- **Issues**: Bug reports and technical problems
- **Pull Requests**: Code contributions
- **Documentation**: Improvements and translations

### **Communication Channels**
- **Primary**: GitHub Issues and Discussions
- **Documentation**: Updates via pull requests
- **Announcements**: GitHub Releases and README updates

---

## 🆘 **Need More Help?**

| Issue Type | Where to Go |
|------------|-------------|
| **🐛 Bug Reports** | [GitHub Issues](https://github.com/YOUR_USERNAME/ai-ster/issues) |
| **💡 Feature Ideas** | [GitHub Discussions](https://github.com/YOUR_USERNAME/ai-ster/discussions) |
| **📖 Documentation** | This docs folder or main README |
| **🚀 Deployment** | [Deployment guides](STREAMLIT_CLOUD_DEPLOYMENT.md) |
| **🤝 Contributing** | [Contributing guidelines](../CONTRIBUTING.md) |
| **📋 USBE Standards** | [STER CT&US FINAL 3.md](STER%20CT&US%20FINAL%203.md) |
| **🏫 Field Requirements** | [Field Evaluations.md](Field%20Evaluations.md) |

---

**📍 You are here**: `/docs/` - Return to [main README](../README.md) or explore the guides above! 