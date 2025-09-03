#!/usr/bin/env python3
"""
Script to generate PDF version of the AI-STER symposium poster.
Requires installation of weasyprint: pip install weasyprint
"""

import os
import sys
from pathlib import Path

def generate_poster_pdf():
    """Generate PDF from HTML poster"""
    
    # Check if weasyprint is available
    try:
        from weasyprint import HTML, CSS
        from weasyprint.text.fonts import FontConfiguration
    except ImportError:
        print("❌ Error: weasyprint is not installed.")
        print("📦 Install with: pip install weasyprint")
        print("🔧 On Ubuntu/Debian, you may also need: sudo apt-get install build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info")
        return False
    
    # Get current directory
    current_dir = Path(__file__).parent
    html_file = current_dir / "AI-STER_Symposium_Poster.html"
    pdf_file = current_dir / "AI-STER_Symposium_Poster.pdf"
    
    # Check if HTML file exists
    if not html_file.exists():
        print(f"❌ Error: {html_file} not found")
        return False
    
    print("🖨️  Generating PDF poster...")
    print(f"📄 Input: {html_file}")
    print(f"📊 Output: {pdf_file}")
    
    try:
        # Configure for poster size (36" x 24")
        poster_css = CSS(string='''
            @page {
                size: 36in 24in;
                margin: 0;
            }
            body {
                margin: 0;
                padding: 0;
            }
        ''')
        
        # Create PDF
        font_config = FontConfiguration()
        html = HTML(filename=str(html_file))
        html.write_pdf(
            str(pdf_file),
            stylesheets=[poster_css],
            font_config=font_config
        )
        
        print("✅ PDF poster generated successfully!")
        print(f"📏 Size: 36\" × 24\" (standard academic poster)")
        print(f"💾 File: {pdf_file}")
        print("\n🖨️  Printing Tips:")
        print("   • Use a professional poster printing service")
        print("   • Recommended paper: Matte or semi-gloss")
        print("   • Ensure 'Actual Size' is selected when printing")
        print("   • Consider lamination for durability")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        return False

def main():
    """Main function"""
    print("🎓 AI-STER Poster PDF Generator")
    print("=" * 50)
    
    success = generate_poster_pdf()
    
    if not success:
        print("\n💡 Alternative options:")
        print("1. Open the HTML file in Chrome/Edge and print to PDF")
        print("2. Use an online HTML to PDF converter")
        print("3. Install weasyprint and run this script again")
        sys.exit(1)
    
    print("\n🎉 Poster ready for the One-U Responsible AI Initiative Annual Symposium!")
    print("📅 Event: September 12, 2025")
    print("📍 Location: Douglas Ballroom, University of Utah Guest House")

if __name__ == "__main__":
    main()
