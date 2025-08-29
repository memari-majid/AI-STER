# AI-STER Changelog

## [2.0.0] - 2024-12-19

### 🚀 Major Features Added

#### AI Version Tracking System
- **Save AI Original**: Capture AI-generated content before supervisor modifications
- **PDF Export**: Professional PDF reports for AI-generated evaluations
- **Comparison Tools**: Side-by-side analysis of AI vs. supervisor versions
- **Research Data**: Structured data for educational research

#### Enhanced PDF Generation
- **Professional Formatting**: Clean, readable layouts with proper styling
- **Multiple Report Types**: Standard evaluations, AI versions, and comparisons
- **Rich Content**: Tables, headers, metadata, and signature sections
- **Export Options**: Download buttons for different report types

#### Deployment Infrastructure
- **Ngrok Integration**: Public access without static IP requirements
- **Systemd Service**: Persistent deployment with auto-start
- **Domain Configuration**: Custom domain support (aister.ngrok.app)
- **Process Management**: Automated start/stop scripts

#### User Experience Improvements
- **Synthetic Data Generation**: Quick testing with sample data
- **Simplified Navigation**: Removed redundant menu items
- **Better Button Placement**: Logical grouping of related features
- **Clear Labels**: Descriptive button text with icons

### 🔧 Technical Enhancements

#### Code Structure
- **Modular Services**: Separated PDF and OpenAI services
- **Session Management**: Improved state handling for AI version tracking
- **Error Handling**: Better error messages and fallback options
- **Configuration**: Environment-based API key management

#### Security
- **API Key Protection**: Removed hardcoded keys from source code
- **Environment Variables**: Secure configuration management
- **Example Files**: Provided env.example for setup guidance

### 📁 New Files Added
- `data/sample_observation_notes.py` - Sample data for testing
- `services/pdf_service.py` - Enhanced PDF generation service
- `deploy/` - Complete deployment automation scripts
- `env.example` - Environment configuration template

### 🔄 Migration Notes
- **API Key Setup**: Users must create `.env` file with their OpenAI API key
- **Deployment**: New deployment scripts available for ngrok integration
- **Navigation**: Simplified menu structure for better UX

### 🐛 Bug Fixes
- Fixed PDF generation error handling
- Resolved style conflicts in PDF service
- Corrected variable scope issues in AI version tracking

### 📚 Documentation
- Added comprehensive deployment guides
- Included environment setup instructions
- Created feature usage documentation

---

## [1.0.0] - Previous Release
- Initial AI-STER application with basic evaluation functionality
- OpenAI integration for competency analysis
- Basic JSON data storage
