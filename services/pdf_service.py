"""
PDF Generation Service for AI-STER Evaluations
Handles creation of professional PDF reports from evaluation data
"""

import io
from datetime import datetime
from typing import Dict, Any, Optional
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image, KeepTogether
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas

class PDFService:
    """Service for generating PDF evaluation reports"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
    def _setup_custom_styles(self):
        """Set up custom paragraph styles for the PDF"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            textColor=colors.HexColor('#1f4e79'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2e5c8a'),
            spaceBefore=20,
            spaceAfter=12
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#1f4e79'),
            spaceBefore=15,
            spaceAfter=10,
            borderWidth=1,
            borderColor=colors.HexColor('#1f4e79'),
            borderPadding=4,
            backColor=colors.HexColor('#f0f5fa')
        ))
        
        # Score style
        self.styles.add(ParagraphStyle(
            name='ScoreStyle',
            parent=self.styles['Normal'],
            fontSize=12,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1f4e79')
        ))
        
    def generate_evaluation_pdf(self, evaluation_data: Dict[str, Any]) -> bytes:
        """
        Generate a PDF report from evaluation data
        
        Args:
            evaluation_data: Dictionary containing all evaluation information
            
        Returns:
            PDF file as bytes
        """
        # Create PDF buffer
        buffer = io.BytesIO()
        
        # Create the PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Build the content
        elements = []
        
        # Add header
        elements.extend(self._create_header(evaluation_data))
        
        # Add evaluation summary
        elements.extend(self._create_summary_section(evaluation_data))
        
        # Add competency scores
        elements.extend(self._create_competency_section(evaluation_data))
        
        # Add professional dispositions (for field evaluations)
        if evaluation_data.get('rubric_type') == 'field_evaluation' and 'dispositions' in evaluation_data:
            elements.append(PageBreak())
            elements.extend(self._create_dispositions_section(evaluation_data))
        
        # Add AI analysis if available
        if 'ai_analysis' in evaluation_data:
            elements.append(PageBreak())
            elements.extend(self._create_ai_analysis_section(evaluation_data))
        
        # Add signature section
        elements.append(Spacer(1, 0.5*inch))
        elements.extend(self._create_signature_section(evaluation_data))
        
        # Build PDF
        doc.build(elements)
        
        # Get PDF value
        buffer.seek(0)
        return buffer.getvalue()
    
    def _create_header(self, data: Dict[str, Any]) -> list:
        """Create the PDF header section"""
        elements = []
        
        # Title
        title_text = f"{data.get('rubric_type', 'STER').replace('_', ' ').title()} Evaluation Report"
        elements.append(Paragraph(title_text, self.styles['CustomTitle']))
        
        # Subtitle with student info
        subtitle = f"Student Teacher: {data.get('student_name', 'N/A')}"
        elements.append(Paragraph(subtitle, self.styles['CustomSubtitle']))
        
        # Evaluation metadata table
        metadata = [
            ['Evaluation Date:', data.get('date', datetime.now().strftime('%Y-%m-%d'))],
            ['School/Site:', data.get('school', 'N/A')],
            ['Subject/Grade:', data.get('subject', 'N/A')],
            ['Supervisor:', data.get('evaluator_name', 'N/A')],
            ['Evaluation Type:', 'Formative' if data.get('is_formative', True) else 'Summative']
        ]
        
        metadata_table = Table(metadata, colWidths=[2*inch, 4*inch])
        metadata_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(metadata_table)
        elements.append(Spacer(1, 0.25*inch))
        
        return elements
    
    def _create_summary_section(self, data: Dict[str, Any]) -> list:
        """Create the evaluation summary section"""
        elements = []
        
        elements.append(Paragraph("Evaluation Summary", self.styles['SectionHeader']))
        
        # Overall statistics
        summary_data = []
        
        # Don't show average score, just item counts
        if 'total_items' in data:
            summary_data.append(['Total Items Evaluated:', str(data['total_items'])])
            
        if 'meeting_expectations' in data:
            summary_data.append(['Items Meeting Expectations:', str(data['meeting_expectations'])])
            
        if 'areas_for_growth' in data:
            summary_data.append(['Areas for Growth:', str(data['areas_for_growth'])])
        
        if summary_data:
            summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
            summary_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            elements.append(summary_table)
        
        elements.append(Spacer(1, 0.25*inch))
        
        return elements
    
    def _create_competency_section(self, data: Dict[str, Any]) -> list:
        """Create the competency scores section"""
        elements = []
        
        elements.append(Paragraph("Competency Evaluation Details", self.styles['SectionHeader']))
        
        # Create competency table
        table_data = [['Competency', 'Score', 'Justification']]
        
        # Add each competency
        for item in data.get('competency_scores', []):
            competency = item.get('competency', 'N/A')
            score = item.get('score', 'N/A')
            justification = item.get('justification', 'No justification provided')
            
            # Truncate long justifications for the table
            if len(justification) > 100:
                justification = justification[:97] + "..."
            
            table_data.append([
                Paragraph(competency, self.styles['Normal']),
                Paragraph(str(score), self.styles['ScoreStyle']),
                Paragraph(justification, self.styles['Normal'])
            ])
        
        # Create table with responsive column widths
        competency_table = Table(table_data, colWidths=[2*inch, 0.75*inch, 3.75*inch])
        competency_table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4e79')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Data rows
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(competency_table)
        elements.append(Spacer(1, 0.25*inch))
        
        return elements
    
    def _create_dispositions_section(self, data: Dict[str, Any]) -> list:
        """Create the professional dispositions section"""
        elements = []
        
        elements.append(Paragraph("Professional Dispositions Assessment", self.styles['SectionHeader']))
        
        # Create dispositions table
        table_data = [['Disposition', 'Score', 'Notes']]
        
        # Add each disposition
        for disp in data.get('dispositions', []):
            disposition = disp.get('disposition', 'N/A')
            score = disp.get('score', 'N/A')
            notes = disp.get('notes', '')
            
            table_data.append([
                Paragraph(disposition, self.styles['Normal']),
                Paragraph(str(score), self.styles['ScoreStyle']),
                Paragraph(notes, self.styles['Normal'])
            ])
        
        # Create table
        disp_table = Table(table_data, colWidths=[2.5*inch, 0.75*inch, 3.25*inch])
        disp_table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e5c8a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Data rows
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f5fa')]),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(disp_table)
        elements.append(Spacer(1, 0.25*inch))
        
        return elements
    
    def _create_ai_analysis_section(self, data: Dict[str, Any]) -> list:
        """Create the AI analysis section"""
        elements = []
        
        elements.append(Paragraph("AI-Generated Analysis", self.styles['SectionHeader']))
        
        ai_analysis = data.get('ai_analysis', {})
        
        # Strengths
        if 'strengths' in ai_analysis:
            elements.append(Paragraph("<b>Identified Strengths:</b>", self.styles['Normal']))
            for strength in ai_analysis['strengths']:
                elements.append(Paragraph(f"• {strength}", self.styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
        
        # Areas for growth
        if 'areas_for_growth' in ai_analysis:
            elements.append(Paragraph("<b>Areas for Growth and Development:</b>", self.styles['Normal']))
            for area in ai_analysis['areas_for_growth']:
                elements.append(Paragraph(f"• {area}", self.styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
        
        # Recommendations
        if 'recommendations' in ai_analysis:
            elements.append(Paragraph("<b>Recommendations:</b>", self.styles['Normal']))
            for rec in ai_analysis['recommendations']:
                elements.append(Paragraph(f"• {rec}", self.styles['Normal']))
        
        return elements
    
    def _create_signature_section(self, data: Dict[str, Any]) -> list:
        """Create the signature section"""
        elements = []
        
        # Add separator line
        elements.append(Spacer(1, 0.5*inch))
        
        # Signature lines
        sig_data = [
            ['_' * 40, '_' * 40],
            ['Supervisor Signature', 'Date'],
            ['', ''],
            ['_' * 40, '_' * 40],
            ['Student Teacher Signature', 'Date']
        ]
        
        sig_table = Table(sig_data, colWidths=[3*inch, 3*inch])
        sig_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica'),
            ('FONTNAME', (0, 4), (-1, 4), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 3), (-1, 3), 20),
        ]))
        
        elements.append(sig_table)
        
        # Footer
        elements.append(Spacer(1, 0.25*inch))
        elements.append(Paragraph(
            f"Generated by AI-STER on {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            ParagraphStyle(
                name='Footer',
                parent=self.styles['Normal'],
                fontSize=8,
                alignment=TA_CENTER,
                textColor=colors.grey
            )
        ))
        
        return elements