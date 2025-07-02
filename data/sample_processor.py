"""
Sample File Processor for AI-STER
Processes uploaded lesson plans and evaluations to improve synthetic data generation
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Import file processing libraries
try:
    import pdfplumber
    PDF_AVAILABLE = True
except ImportError:
    try:
        import PyPDF2
        PDF_AVAILABLE = "basic"
    except ImportError:
        PDF_AVAILABLE = False

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

class SampleProcessor:
    """Process and analyze sample lesson plans and evaluations"""
    
    def __init__(self, samples_dir: str = "data/samples"):
        self.samples_dir = Path(samples_dir)
        self.lesson_plans_dir = self.samples_dir / "lesson_plans"
        self.evaluations_dir = self.samples_dir / "evaluations"
        self.templates_dir = self.samples_dir / "templates"
        self.standards_dir = self.samples_dir / "standards_references"
    
    def scan_sample_files(self) -> Dict[str, List[str]]:
        """Scan all sample directories and return file inventory"""
        inventory = {
            "lesson_plans": [],
            "evaluations": [],
            "templates": [],
            "standards_references": []
        }
        
        directories = {
            "lesson_plans": self.lesson_plans_dir,
            "evaluations": self.evaluations_dir,
            "templates": self.templates_dir,
            "standards_references": self.standards_dir
        }
        
        for category, directory in directories.items():
            if directory.exists():
                for file_path in directory.rglob("*"):
                    if file_path.is_file():
                        inventory[category].append(str(file_path.relative_to(self.samples_dir)))
        
        return inventory
    
    def extract_text_from_file(self, file_path: Path) -> Optional[str]:
        """Extract text content from various file formats"""
        try:
            if file_path.suffix.lower() in ['.txt', '.md']:
                return file_path.read_text(encoding='utf-8')
            
            elif file_path.suffix.lower() == '.pdf':
                return self._extract_pdf_text(file_path)
            
            elif file_path.suffix.lower() == '.docx':
                return self._extract_docx_text(file_path)
            
            else:
                print(f"Note: {file_path.suffix} files not supported")
                return None
        except Exception as e:
            print(f"Error reading {file_path}: {str(e)}")
            return None
    
    def _extract_pdf_text(self, file_path: Path) -> Optional[str]:
        """Extract text from PDF using best available method"""
        if PDF_AVAILABLE == True:  # pdfplumber available
            try:
                text = ""
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                return text if text.strip() else None
            except Exception as e:
                print(f"PDF extraction error with pdfplumber: {e}")
                return None
        
        elif PDF_AVAILABLE == "basic":  # PyPDF2 fallback
            try:
                text = ""
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
                return text if text.strip() else None
            except Exception as e:
                print(f"PDF extraction error with PyPDF2: {e}")
                return None
        
        else:
            print(f"PDF support not available for {file_path}")
            return None
    
    def _extract_docx_text(self, file_path: Path) -> Optional[str]:
        """Extract text from DOCX file"""
        if not DOCX_AVAILABLE:
            print(f"DOCX support not available for {file_path}")
            return None
        
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text if text.strip() else None
        except Exception as e:
            print(f"DOCX extraction error: {e}")
            return None
    
    def analyze_lesson_plans(self) -> Dict[str, Any]:
        """Analyze lesson plan samples for Utah standards and structure"""
        analysis = {
            "total_files": 0,
            "processed_files": 0,
            "readable_files": 0,
            "utah_standards_found": [],
            "grade_levels_found": set(),
            "subject_areas_found": set(),
            "files_processed": []
        }
        
        if not self.lesson_plans_dir.exists():
            return analysis
        
        for file_path in self.lesson_plans_dir.rglob("*"):
            if file_path.is_file():
                analysis["total_files"] += 1
                
                text = self.extract_text_from_file(file_path)
                if text and len(text.strip()) > 50:  # Must have substantial content
                    analysis["processed_files"] += 1
                    analysis["readable_files"] += 1
                    
                    # Find Utah Core Standards
                    utah_standards = re.findall(r'\b\d+\.[A-Z]{1,3}\.\d+(?:\.\d+)?\b', text)
                    utah_standards.extend(re.findall(r'\b[A-Z]{2,3}\.[A-Z]{1,3}\.\d+(?:\.\d+)?\b', text))
                    
                    # Find grade levels
                    grade_matches = re.findall(r'\bgrade\s*(\d+|\w+)\b', text, re.IGNORECASE)
                    grade_matches.extend(re.findall(r'\b(\d+)(?:st|nd|rd|th)\s*grade\b', text, re.IGNORECASE))
                    
                    # Find subjects
                    text_lower = text.lower()
                    subjects = ['mathematics', 'math', 'english', 'language arts', 'ela', 'science',
                              'social studies', 'history', 'art', 'music', 'physical education', 'sped']
                    found_subjects = [s for s in subjects if s in text_lower]
                    
                    analysis["utah_standards_found"].extend(utah_standards)
                    analysis["grade_levels_found"].update(grade_matches)
                    analysis["subject_areas_found"].update(found_subjects)
                    
                    analysis["files_processed"].append({
                        "file": str(file_path.relative_to(self.samples_dir)),
                        "format": file_path.suffix.lower(),
                        "utah_standards": utah_standards,
                        "grade_levels": grade_matches,
                        "subjects": found_subjects,
                        "word_count": len(text.split()),
                        "readable": True
                    })
                else:
                    analysis["files_processed"].append({
                        "file": str(file_path.relative_to(self.samples_dir)),
                        "format": file_path.suffix.lower(),
                        "readable": False,
                        "reason": "Could not extract text or file too short"
                    })
        
        # Convert sets to lists
        analysis["grade_levels_found"] = list(analysis["grade_levels_found"])
        analysis["subject_areas_found"] = list(analysis["subject_areas_found"])
        analysis["utah_standards_found"] = list(set(analysis["utah_standards_found"]))
        
        return analysis
    
    def test_ai_analysis(self) -> Dict[str, Any]:
        """Test AI lesson plan analysis against samples"""
        try:
            from services.openai_service import OpenAIService
            ai_service = OpenAIService()
            
            if not ai_service.is_enabled():
                return {"error": "OpenAI service not configured"}
            
            results = {"tests_run": 0, "successful": 0, "failed": 0, "results": []}
            
            for file_path in self.lesson_plans_dir.rglob("*"):
                if file_path.is_file():
                    text = self.extract_text_from_file(file_path)
                    if text and len(text.strip()) > 100:
                        results["tests_run"] += 1
                        
                        try:
                            ai_analysis = ai_service.analyze_lesson_plan(text)
                            results["successful"] += 1
                            results["results"].append({
                                "file": str(file_path.relative_to(self.samples_dir)),
                                "success": True,
                                "confidence": ai_analysis.get("confidence_score", 0),
                                "extracted_teacher": ai_analysis.get("teacher_name"),
                                "extracted_subject": ai_analysis.get("subject_area"),
                                "extracted_grade": ai_analysis.get("grade_levels"),
                                "extracted_standards": ai_analysis.get("utah_core_standards"),
                                "word_count": len(text.split())
                            })
                        except Exception as e:
                            results["failed"] += 1
                            results["results"].append({
                                "file": str(file_path.relative_to(self.samples_dir)),
                                "success": False,
                                "error": str(e)
                            })
            
            return results
            
        except ImportError:
            return {"error": "OpenAI service not available"}
        except Exception as e:
            return {"error": str(e)}
    
    def detailed_ai_test(self, file_name: str) -> Dict[str, Any]:
        """Test AI analysis on a specific file with detailed output"""
        file_path = self.lesson_plans_dir / file_name
        
        if not file_path.exists():
            return {"error": f"File not found: {file_name}"}
        
        text = self.extract_text_from_file(file_path)
        if not text:
            return {"error": f"Could not extract text from {file_name}"}
        
        try:
            from services.openai_service import OpenAIService
            ai_service = OpenAIService()
            
            if not ai_service.is_enabled():
                return {"error": "OpenAI service not configured"}
            
            # Manual analysis
            manual_analysis = self._analyze_lesson_plan_text(text)
            
            # AI analysis
            ai_analysis = ai_service.analyze_lesson_plan(text)
            
            return {
                "file": file_name,
                "text_length": len(text),
                "word_count": len(text.split()),
                "manual_analysis": manual_analysis,
                "ai_analysis": ai_analysis,
                "comparison": self._compare_analyses(ai_analysis, manual_analysis)
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _analyze_lesson_plan_text(self, text: str) -> Dict[str, Any]:
        """Manual pattern-based analysis for comparison"""
        text_lower = text.lower()
        
        # Utah Core Standards
        utah_standards = re.findall(r'\b\d+\.[A-Z]{1,3}\.\d+(?:\.\d+)?\b', text, re.IGNORECASE)
        utah_standards.extend(re.findall(r'\b[A-Z]{2,3}\.[A-Z]{1,3}\.\d+(?:\.\d+)?\b', text, re.IGNORECASE))
        
        # Teacher names (look for common patterns)
        teacher_patterns = [
            r'teacher:\s*([A-Z][a-z]+\s+[A-Z][a-z]+)',
            r'instructor:\s*([A-Z][a-z]+\s+[A-Z][a-z]+)',
            r'by:\s*([A-Z][a-z]+\s+[A-Z][a-z]+)'
        ]
        teachers = []
        for pattern in teacher_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            teachers.extend(matches)
        
        # Subjects
        subjects = ['mathematics', 'math', 'english', 'language arts', 'ela', 'science',
                   'social studies', 'history', 'art', 'music', 'physical education', 'sped']
        found_subjects = [s for s in subjects if s in text_lower]
        
        # Grade levels
        grade_matches = re.findall(r'\bgrade\s*(\d+|\w+)\b', text, re.IGNORECASE)
        grade_matches.extend(re.findall(r'\b(\d+)(?:st|nd|rd|th)\s*grade\b', text, re.IGNORECASE))
        
        return {
            "utah_standards": utah_standards,
            "teachers": teachers,
            "subjects": found_subjects,
            "grade_levels": grade_matches
        }
    
    def _compare_analyses(self, ai_analysis: Dict, manual_analysis: Dict) -> Dict[str, Any]:
        """Compare AI vs manual analysis"""
        comparison = {
            "standards_match": False,
            "teacher_extracted": bool(ai_analysis.get("teacher_name")),
            "subject_match": False,
            "grade_match": False
        }
        
        # Compare standards
        ai_standards = ai_analysis.get("utah_core_standards", "")
        manual_standards = manual_analysis.get("utah_standards", [])
        if ai_standards and manual_standards:
            comparison["standards_match"] = any(std in ai_standards for std in manual_standards)
        
        # Compare subjects
        ai_subject = ai_analysis.get("subject_area", "").lower()
        manual_subjects = [s.lower() for s in manual_analysis.get("subjects", [])]
        if ai_subject and manual_subjects:
            comparison["subject_match"] = any(subj in ai_subject for subj in manual_subjects)
        
        # Compare grades
        ai_grades = ai_analysis.get("grade_levels", "").lower()
        manual_grades = [str(g).lower() for g in manual_analysis.get("grade_levels", [])]
        if ai_grades and manual_grades:
            comparison["grade_match"] = any(grade in ai_grades for grade in manual_grades)
        
        return comparison
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive analysis report"""
        print("🔍 Scanning sample files...")
        inventory = self.scan_sample_files()
        
        print("📚 Analyzing lesson plans...")
        lesson_analysis = self.analyze_lesson_plans()
        
        print("🤖 Testing AI analysis...")
        ai_test_results = self.test_ai_analysis()
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "file_inventory": inventory,
            "lesson_plan_analysis": lesson_analysis,
            "ai_test_results": ai_test_results,
            "recommendations": self._generate_recommendations(lesson_analysis, ai_test_results)
        }
        
        return report
    
    def _generate_recommendations(self, lesson_analysis: Dict, ai_results: Dict) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        if lesson_analysis["utah_standards_found"]:
            recommendations.append(
                f"Found {len(lesson_analysis['utah_standards_found'])} Utah Core Standards. "
                f"Consider adding these to synthetic data generation."
            )
        
        if lesson_analysis["subject_areas_found"]:
            recommendations.append(
                f"Subjects found: {', '.join(lesson_analysis['subject_areas_found'])}. "
                f"Verify alignment with synthetic data subjects."
            )
        
        if lesson_analysis["grade_levels_found"]:
            recommendations.append(
                f"Grade levels: {', '.join(lesson_analysis['grade_levels_found'])}. "
                f"Update grade categorization if needed."
            )
        
        # AI performance recommendations
        if "error" not in ai_results and ai_results.get("tests_run", 0) > 0:
            success_rate = (ai_results["successful"] / ai_results["tests_run"]) * 100
            if success_rate < 80:
                recommendations.append(
                    f"AI success rate is {success_rate:.1f}%. Consider improving text extraction or file quality."
                )
            elif success_rate >= 95:
                recommendations.append(
                    f"Excellent AI success rate ({success_rate:.1f}%). AI analysis is working well with your samples."
                )
        
        # File format recommendations
        readable_rate = (lesson_analysis["readable_files"] / lesson_analysis["total_files"]) * 100 if lesson_analysis["total_files"] > 0 else 0
        if readable_rate < 80:
            recommendations.append(
                f"Only {readable_rate:.1f}% of files are readable. Consider converting files or checking formats."
            )
        
        return recommendations
    
    def save_report(self, filename: str = "sample_analysis_report.json") -> str:
        """Save analysis report to file"""
        report = self.generate_report()
        
        report_path = self.samples_dir / filename
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Report saved to: {report_path}")
        return str(report_path)

def main():
    """Run the sample processor"""
    processor = SampleProcessor()
    
    print("🚀 AI-STER Sample File Processor")
    print("=" * 40)
    
    # Check capabilities
    capabilities = []
    if PDF_AVAILABLE == True:
        capabilities.append("PDF (pdfplumber)")
    elif PDF_AVAILABLE == "basic":
        capabilities.append("PDF (PyPDF2)")
    if DOCX_AVAILABLE:
        capabilities.append("Word documents")
    capabilities.append("Text/Markdown")
    
    print(f"📂 Supported formats: {', '.join(capabilities)}")
    
    # Check if sample files exist
    inventory = processor.scan_sample_files()
    total_files = sum(len(files) for files in inventory.values())
    
    if total_files == 0:
        print("📁 No sample files found.")
        print("💡 Upload files to these directories:")
        print("   - data/samples/lesson_plans/")
        print("   - data/samples/evaluations/")
        print("   - data/samples/templates/")
        print("   - data/samples/standards_references/")
        return
    
    print(f"📁 Found {total_files} sample files")
    
    # Generate and save analysis
    report_path = processor.save_report()
    
    print("\n✅ Analysis complete!")
    print(f"📄 View report: {report_path}")

if __name__ == "__main__":
    main() 