# 🏗️ AI-STER Repository Architecture Guide

## 📁 **Repository Structure (FIXED)**

```
AI-STER/                          # ← ROOT: Deploy from here!
├── 📄 app.py                     # ← Main Streamlit application (REQUIRED IN ROOT)
├── 📄 README.md                  # ← Main project documentation (GitHub displays this)
├── 📄 requirements.txt           # ← Dependencies (deployment needs this in root)
├── 📄 CHANGELOG.md               # ← Version history
├── 📄 CONTRIBUTING.md            # ← Contribution guidelines
├── 📄 LICENSE                    # ← MIT license
├── 📄 .gitignore                 # ← Git ignore rules (excludes ai-ster-env/)
├── 📄 .env                       # ← Environment variables (OpenAI API key)
├── 📁 data/                      # ← Data modules (rubrics, synthetic data)
├── 📁 services/                  # ← AI services (OpenAI integration)
├── 📁 utils/                     # ← Utilities (storage, validation)
├── 📁 docs/                      # ← Documentation (implementation plans, guides)
└── 📁 ai-ster-env/              # ← Virtual environment (EXCLUDED from Git)
```

## 🚀 **For Streamlit Cloud Deployment**

### ✅ **CORRECT: Deploy from ROOT directory**
- **Repository URL**: `https://github.com/yourusername/AI-STER`
- **Main file path**: `app.py` (automatically detected in root)
- **Python version**: 3.12
- **Requirements**: `requirements.txt` (automatically found in root)

### ❌ **WRONG: Don't use subdirectories**
- ~~Do NOT deploy from `/streamlit-ster` (this no longer exists)~~
- ~~Do NOT deploy from `/ai-ster-env` (this is a virtual environment)~~

## 🎯 **Why This Architecture?**

### **Previous Problem (FIXED)**
```
❌ OLD STRUCTURE (broken for deployment):
AI-STER/
├── ai-ster-env/          # Virtual env in repo (bad practice)
└── streamlit-ster/       # App in subdirectory (deployment issues)
    ├── app.py           # Not in root → Streamlit can't find it
    └── README.md        # Not in root → GitHub can't display it
```

### **Current Solution (OPTIMAL)**
```
✅ NEW STRUCTURE (deployment-ready):
AI-STER/
├── app.py               # In root → Streamlit finds it immediately
├── README.md           # In root → GitHub displays it properly
├── requirements.txt    # In root → Deployment tools find it
└── ai-ster-env/        # Excluded from Git (local development only)
```

## 📋 **Quick Deployment Checklist**

### **GitHub Repository Setup**
1. ✅ `app.py` is in root directory
2. ✅ `README.md` is in root directory  
3. ✅ `requirements.txt` is in root directory
4. ✅ `.env` contains OpenAI API key (for local dev)
5. ✅ Virtual environment excluded from Git

### **Streamlit Cloud Deployment**
1. ✅ Connect GitHub repository (root directory)
2. ✅ Main file: `app.py` (auto-detected)
3. ✅ Python version: 3.12
4. ✅ Add OpenAI API key in Streamlit secrets
5. ✅ Deploy → App URL: `https://your-app.streamlit.app`

## 🔗 **Next Steps**

1. **Push to GitHub**: Repository is now optimally structured
2. **Deploy on Streamlit Cloud**: See `docs/STREAMLIT_CLOUD_DEPLOYMENT.md`
3. **Alternative Deployment**: See `docs/DEPLOYMENT.md` for other options

---

**✨ Repository restructured for optimal deployment and GitHub best practices!** 