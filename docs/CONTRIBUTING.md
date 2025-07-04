# 🤝 Contributing to AI-STER

Thank you for your interest in contributing to AI-STER! We welcome contributions from educators, developers, and anyone passionate about improving student teacher evaluations.

## 🌟 **Ways to Contribute**

### 🐛 **Bug Reports**
- Found a bug? Please check existing [issues](https://github.com/YOUR_USERNAME/ai-ster/issues) first
- Create a detailed bug report using our issue template
- Include steps to reproduce, expected behavior, and screenshots if applicable

### 💡 **Feature Requests**
- Have an idea for improvement? Start a [discussion](https://github.com/YOUR_USERNAME/ai-ster/discussions)
- Describe the feature, use case, and how it benefits educators
- Consider creating a proof of concept or mockup

### 📝 **Documentation**
- Improve README, deployment guides, or code comments
- Add examples, tutorials, or troubleshooting guides
- Translate documentation to other languages

### 🔧 **Code Contributions**
- Fix bugs, implement features, or optimize performance
- Improve test coverage or add new test cases
- Enhance the user interface or user experience

## 🚀 **Getting Started**

### **1. Development Setup**
```bash
# Fork the repository on GitHub
git clone https://github.com/YOUR_USERNAME/ai-ster.git
cd ai-ster

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### **2. Environment Configuration**
```bash
# Copy environment template
cp docs/env_template.txt .env

# Add your OpenAI API key (optional for most contributions)
# OPENAI_API_KEY=your_test_key_here
```

### **3. Test Your Changes**
```bash
# Run basic functionality tests
python -c "
from data.rubrics import get_field_evaluation_items
from services.openai_service import OpenAIService
from utils.storage import load_evaluations
print('✅ All imports working!')
"

# Test the web application
streamlit run app.py
# Visit http://localhost:8501 and test functionality
```

## 📋 **Contribution Guidelines**

### **Code Style**
- Follow [PEP 8](https://pep8.org/) Python style guidelines
- Use clear, descriptive variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and modular

### **Example Code Style**
```python
def validate_evaluation_scores(scores: Dict[str, int], min_score: int = 2) -> List[str]:
    """
    Validate evaluation scores against minimum requirements.
    
    Args:
        scores: Dictionary mapping item IDs to scores (0-3)
        min_score: Minimum required score level
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    for item_id, score in scores.items():
        if score < min_score:
            errors.append(f"Item {item_id} scored {score}, minimum {min_score} required")
    return errors
```

### **Commit Messages**
Use clear, descriptive commit messages:
```bash
# Good
git commit -m "Add validation for professional disposition scores"
git commit -m "Fix: Handle missing justifications in AI analysis"
git commit -m "Docs: Update deployment guide with Railway instructions"

# Avoid
git commit -m "fix bug"
git commit -m "update stuff"
```

### **Branch Naming**
Use descriptive branch names:
```bash
# Features
git checkout -b feature/bulk-evaluation-export
git checkout -b feature/pdf-report-generation

# Bug fixes
git checkout -b fix/scoring-validation-error
git checkout -b fix/ai-justification-timeout

# Documentation
git checkout -b docs/update-deployment-guide
```

## 🧪 **Testing Guidelines**

### **Manual Testing Checklist**
Before submitting a pull request, test these core features:

#### **Basic Functionality**
- [ ] Application starts without errors
- [ ] All navigation tabs work (Dashboard, New Evaluation, Test Data, Settings)
- [ ] Can create new evaluations (both Field and STER types)
- [ ] Score validation works correctly
- [ ] Professional dispositions validation works

#### **Data Features**
- [ ] Synthetic data generation works
- [ ] Export/import functionality works
- [ ] Data persists between sessions

#### **AI Features** (if OpenAI key available)
- [ ] AI justification generation works
- [ ] AI evaluation analysis works
- [ ] Error handling for AI failures

### **Automated Testing**
```bash
# Run the basic import test
python -c "
import sys
sys.path.append('.')

try:
    # Test all major imports
    from data.rubrics import get_field_evaluation_items, get_ster_items, get_professional_dispositions
    from data.synthetic import generate_synthetic_evaluations
    from services.openai_service import OpenAIService
    from utils.storage import save_evaluation, load_evaluations
    from utils.validation import validate_evaluation
    
    # Test basic functionality
    field_items = get_field_evaluation_items()
    ster_items = get_ster_items()
    dispositions = get_professional_dispositions()
    
    assert len(field_items) == 8, f'Expected 8 field items, got {len(field_items)}'
    assert len(ster_items) == 9, f'Expected 9 STER items, got {len(ster_items)}'
    assert len(dispositions) == 6, f'Expected 6 dispositions, got {len(dispositions)}'
    
    # Test synthetic data
    synthetic = generate_synthetic_evaluations(count=1)
    assert len(synthetic) == 1, 'Synthetic data generation failed'
    
    print('✅ All tests passed!')
    
except Exception as e:
    print(f'❌ Test failed: {e}')
    sys.exit(1)
"
```

## 📚 **Areas for Contribution**

### **🎓 Educational Features**
- **Competency Mapping**: Visual competency progress tracking
- **Evaluation Templates**: Custom evaluation forms for different programs
- **Progress Analytics**: Longitudinal student progress visualization
- **Peer Comparison**: Anonymous benchmarking features

### **🤖 AI Enhancements**
- **Smart Suggestions**: AI-powered improvement recommendations
- **Trend Analysis**: Pattern recognition in evaluation data
- **Natural Language**: Voice-to-text for evaluation input
- **Multilingual Support**: AI translations for diverse institutions

### **🔧 Technical Improvements**
- **Database Backend**: PostgreSQL/MySQL integration for scalability
- **API Development**: REST API for third-party integrations
- **Performance**: Optimization for large datasets
- **Security**: Enhanced authentication and data protection

### **🎨 User Experience**
- **Mobile App**: Native mobile application
- **Accessibility**: WCAG compliance improvements
- **Themes**: Customizable UI themes
- **Offline Mode**: Local-first data synchronization

## 🔄 **Pull Request Process**

### **1. Prepare Your Contribution**
```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Make your changes
# ... code, test, iterate ...

# Commit your changes
git add .
git commit -m "Add feature: your feature description"
```

### **2. Submit Pull Request**
1. Push your branch to your fork
2. Create a pull request on GitHub
3. Fill out the pull request template
4. Link any related issues or discussions

### **3. Pull Request Template**
```markdown
## Description
Brief description of changes and motivation.

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Manual testing completed
- [ ] All imports work correctly
- [ ] Core functionality tested
- [ ] AI features tested (if applicable)

## Screenshots
Include screenshots for UI changes.

## Additional Notes
Any additional context or considerations.
```

### **4. Review Process**
- Maintainers will review your pull request
- Address any feedback or requested changes
- Once approved, your contribution will be merged!

## 🏆 **Recognition**

### **Contributors Hall of Fame**
All contributors are recognized in our [Contributors](CONTRIBUTORS.md) file and project documentation.

### **Types of Recognition**
- **🥇 Gold Contributors**: Major features or significant improvements
- **🥈 Silver Contributors**: Bug fixes, documentation, or moderate features  
- **🥉 Bronze Contributors**: Small fixes, improvements, or first contributions

## 📞 **Getting Help**

### **Community Support**
- **💬 Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/ai-ster/discussions)
- **🐛 Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/ai-ster/issues)
- **📧 Email**: Create an issue for direct contact

### **Development Questions**
If you're stuck on a technical issue:
1. Check existing issues and discussions
2. Search the documentation in [docs/](docs/)
3. Create a new discussion with the "question" label
4. Provide code snippets, error messages, and context

## 📝 **Code of Conduct**

### **Our Standards**
We are committed to creating a welcoming environment for all contributors:

- **Be Respectful**: Treat everyone with respect and kindness
- **Be Inclusive**: Welcome people of all backgrounds and skill levels
- **Be Collaborative**: Work together and help each other succeed
- **Be Constructive**: Provide helpful feedback and suggestions

### **Educational Focus**
Remember that AI-STER serves educators and students. Consider the impact of changes on:
- **Usability**: Will this be easy for teachers to use?
- **Accessibility**: Can everyone access and use this feature?
- **Educational Value**: Does this improve student teacher evaluations?
- **Compliance**: Does this maintain USBE standard compliance?

## 🎯 **Special Interest Groups**

### **Educators**
- Share feedback on educational workflows
- Suggest improvements based on real-world usage
- Help validate USBE compliance
- Provide use case examples

### **Developers**
- Implement technical features and optimizations
- Improve code quality and architecture
- Add testing and documentation
- Enhance performance and scalability

### **Designers**
- Improve user interface and experience
- Create educational materials and guides
- Design accessibility improvements
- Develop visual identity and branding

### **Researchers**
- Validate educational assessment methodologies
- Contribute data analysis features
- Suggest evidence-based improvements
- Share research findings and insights

---

## 🙏 **Thank You!**

Every contribution, no matter how small, makes AI-STER better for educators and students worldwide. Thank you for being part of our community!

**Together, we're transforming student teacher evaluations! 🚀** 