"""
PDF Generation Service for AI-STER Evaluations
Handles creation of professional PDF reports from evaluation data
"""

import io
import os
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
        
        # Competency header style
        self.styles.add(ParagraphStyle(
            name='CompetencyHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#2e5c8a'),
            spaceBefore=12,
            spaceAfter=6
        ))
        
        # Justification style
        self.styles.add(ParagraphStyle(
            name='JustificationStyle',
            parent=self.styles['Normal'],
            fontSize=11,
            leading=14,
            alignment=TA_JUSTIFY,
            spaceAfter=12
        ))
        
        # Bold style
        self.styles.add(ParagraphStyle(
            name='CustomBold',
            parent=self.styles['Normal'],
            fontName='Helvetica-Bold'
        ))
        
        # Italic style
        self.styles.add(ParagraphStyle(
            name='CustomItalic',
            parent=self.styles['Normal'],
            fontName='Helvetica-Oblique'
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
        
        # Add targeted improvement analysis if available
        if 'targeted_improvement_analysis' in evaluation_data and evaluation_data['targeted_improvement_analysis']:
            elements.append(Spacer(1, 0.3*inch))
            elements.extend(self._create_targeted_improvement_section(evaluation_data))
        
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
    
    def _create_targeted_improvement_section(self, data: Dict[str, Any]) -> list:
        """Create the targeted improvement analysis section"""
        elements = []
        
        # Add section header
        elements.append(Paragraph("Targeted Improvement Analysis", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Add the analysis text
        analysis_text = data.get('targeted_improvement_analysis', '')
        if analysis_text:
            # Split into paragraphs for better formatting
            paragraphs = analysis_text.split('\n\n')
            for paragraph in paragraphs:
                if paragraph.strip():
                    elements.append(Paragraph(paragraph.strip(), self.styles['Normal']))
                    elements.append(Spacer(1, 0.1*inch))
        else:
            elements.append(Paragraph("No targeted improvement analysis available.", self.styles['Normal']))
        
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
    
    def generate_ai_version_pdf(self, data: Dict[str, Any]) -> bytes:
        """
        Generate a PDF report for AI-generated original version
        
        Args:
            data: Dictionary containing AI-generated evaluation information
            
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
        
        # Add title
        elements.append(Paragraph("AI-STER: AI-Generated Original Version", self.styles['CustomTitle']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Add warning/notice
        notice_style = ParagraphStyle(
            name='Notice',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#d9534f'),
            alignment=TA_CENTER,
            spaceAfter=20
        )
        notice_text = "This document contains the original AI-generated content before any supervisor modifications"
        elements.append(Paragraph(notice_text, notice_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Add metadata section
        elements.extend(self._create_ai_version_header(data))
        
        # Add generation summary
        elements.extend(self._create_ai_generation_summary(data))
        
        # Add observation notes section
        if data.get('observation_notes'):
            elements.append(PageBreak())
            elements.extend(self._create_observation_notes_section(data))
        
        # Add competency analyses
        elements.append(PageBreak())
        elements.extend(self._create_ai_competency_analyses(data))
        
        # Add footer
        elements.append(Spacer(1, 0.5*inch))
        elements.extend(self._create_ai_version_footer(data))
        
        # Build PDF
        doc.build(elements)
        
        # Get PDF value
        buffer.seek(0)
        return buffer.getvalue()
    
    def _create_ai_version_header(self, data: Dict[str, Any]) -> list:
        """Create the AI version PDF header section"""
        elements = []
        
        # Metadata table
        metadata = [
            ['Student Teacher:', data.get('student_name', 'N/A')],
            ['Evaluator:', data.get('evaluator_name', 'N/A')],
            ['Evaluation Type:', data.get('rubric_type', 'STER').replace('_', ' ').title()],
            ['Date Generated:', data.get('date', datetime.now().strftime('%Y-%m-%d'))],
            ['Time Generated:', data.get('time_generated', datetime.now().strftime('%H:%M:%S'))],
            ['School/Site:', data.get('school', 'N/A')],
            ['Subject Area:', data.get('subject', 'N/A')],
            ['Grade Levels:', data.get('grade_levels', 'N/A')],
            ['Class Size:', str(data.get('class_size', 'N/A'))]
        ]
        
        metadata_table = Table(metadata, colWidths=[2.5*inch, 4*inch])
        metadata_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(metadata_table)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_ai_generation_summary(self, data: Dict[str, Any]) -> list:
        """Create AI generation summary section"""
        elements = []
        
        elements.append(Paragraph("AI Analysis Summary", self.styles['SectionHeader']))
        
        # Summary box
        summary_data = [
            ['Total Competencies Analyzed:', str(data.get('competencies_analyzed', 0))],
            ['AI Model:', f'{data.get("model_used", "gpt-5-mini")}'],
            ['Analysis Based On:', 'Classroom observation notes' + (' and lesson plan' if data.get('lesson_plan_analysis') else '')],
            ['Status:', 'Original AI-generated content - unmodified']
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 4*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
            ('BORDER', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('PADDING', (0, 0), (-1, -1), 12),
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_observation_notes_section(self, data: Dict[str, Any]) -> list:
        """Create observation notes section"""
        elements = []
        
        elements.append(Paragraph("Classroom Observation Notes", self.styles['CustomSubtitle']))
        elements.append(Paragraph("(Used as basis for AI analysis)", self.styles['CustomItalic']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Observation notes in a bordered box
        notes_text = data.get('observation_notes', 'No observation notes provided')
        notes_style = ParagraphStyle(
            name='ObservationNotes',
            parent=self.styles['Normal'],
            fontSize=10,
            leading=14,
            alignment=TA_JUSTIFY,
            spaceAfter=12
        )
        
        # Split notes into paragraphs for better formatting
        notes_lines = notes_text.split('\n')
        for line in notes_lines:
            if line.strip():
                elements.append(Paragraph(line, notes_style))
        
        return elements
    
    def _create_ai_competency_analyses(self, data: Dict[str, Any]) -> list:
        """Create AI competency analyses section"""
        elements = []
        
        elements.append(Paragraph("AI-Generated Competency Analyses", self.styles['CustomSubtitle']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Get items for proper names
        items = data.get('items', [])
        item_dict = {item['id']: item for item in items}
        
        # AI analyses
        ai_analyses = data.get('ai_analyses', {})
        justifications = data.get('justifications', {})
        scores = data.get('scores', {})
        
        for item_id, analysis in ai_analyses.items():
            item = item_dict.get(item_id, {})
            
            # Competency header
            comp_header = f"{item.get('name', item_id)}"
            elements.append(Paragraph(comp_header, self.styles['CompetencyHeader']))
            
            # Score if available
            if item_id in scores and scores[item_id] is not None:
                score_text = f"AI Suggested Score: Level {scores[item_id]}"
                elements.append(Paragraph(score_text, self.styles['ScoreStyle']))
            
            # AI analysis/justification
            analysis_text = analysis or justifications.get(item_id, 'No AI analysis generated')
            elements.append(Paragraph("AI Analysis:", self.styles['CustomBold']))
            elements.append(Paragraph(analysis_text, self.styles['JustificationStyle']))
            
            elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_ai_version_footer(self, data: Dict[str, Any]) -> list:
        """Create footer for AI version PDF"""
        elements = []
        
        # Separator line
        line_data = [['']]
        line_table = Table(line_data, colWidths=[6.5*inch])
        line_table.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
        ]))
        elements.append(line_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Footer information
        footer_style = ParagraphStyle(
            name='Footer',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#6c757d'),
            alignment=TA_CENTER
        )
        
        if data.get('is_redownload'):
            footer_text = f"Originally generated: {data.get('time_generated', 'Unknown')} | Re-downloaded: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        else:
            footer_text = f"Generated by AI-STER on {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}"
        
        elements.append(Paragraph(footer_text, footer_style))
        elements.append(Paragraph("This is an AI-generated document for research and review purposes", footer_style))
        
        return elements
    
    def generate_comparison_pdf(self, comparison_data: Dict[str, Any]) -> bytes:
        """Generate PDF report for AI vs Supervisor comparison"""
        doc = SimpleDocTemplate(
            "temp_comparison.pdf",
            pagesize=letter,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch,
            leftMargin=0.75*inch,
            rightMargin=0.75*inch
        )
        
        elements = []
        
        # Header
        elements.append(Paragraph("AI Performance Evaluation - Comparison Report", self.styles['CustomTitle']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Evaluation info
        eval_info = comparison_data.get('evaluation_info', {})
        info_data = [
            ['Student Name:', eval_info.get('student_name', 'N/A')],
            ['Evaluator:', eval_info.get('evaluator_name', 'N/A')],
            ['Evaluation Date:', eval_info.get('evaluation_date', 'N/A')[:10] if eval_info.get('evaluation_date') else 'N/A'],
            ['Rubric Type:', eval_info.get('rubric_type', 'N/A').replace('_', ' ').title()]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Summary metrics
        summary = comparison_data.get('comparison_summary', {})
        elements.append(Paragraph("Comparison Summary", self.styles['SectionHeader']))
        
        summary_data = [
            ['Total Competencies:', str(summary.get('total_competencies', 0))],
            ['Modified Justifications:', str(summary.get('modified_justifications', 0))],
            ['Score Changes:', str(summary.get('score_changes', 0))],
            ['AI Version Saved:', summary.get('ai_version_saved_at', 'Unknown')[:19] if summary.get('ai_version_saved_at') else 'Unknown']
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 3.5*inch])
        summary_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f0f0f0")),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Detailed comparisons
        elements.append(Paragraph("Competency-by-Competency Comparison", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        ai_data = comparison_data.get('ai_original', {})
        supervisor_data = comparison_data.get('supervisor_final', {})
        items = comparison_data.get('items', [])
        
        for item in items:
            item_id = item['id']
            
            # Only show items that have AI analysis
            if item_id in ai_data.get('justifications', {}):
                # Competency header
                comp_title = f"{item['code']}: {item['title']}"
                elements.append(Paragraph(comp_title, self.styles['CompetencyHeader']))
                
                # Create comparison table
                ai_score = ai_data.get('scores', {}).get(item_id, 'Not scored')
                supervisor_score = supervisor_data.get('scores', {}).get(item_id, 'Not scored')
                ai_just = ai_data.get('justifications', {}).get(item_id, 'No justification')
                supervisor_just = supervisor_data.get('justifications', {}).get(item_id, 'No justification')
                
                # Score comparison
                score_changed = ai_score != supervisor_score
                score_text = f"Score: {supervisor_score}"
                if score_changed:
                    score_text += f" (changed from {ai_score})"
                
                # Justification comparison
                just_changed = ai_just != supervisor_just
                
                comp_data = []
                comp_data.append([
                    Paragraph("<b>AI Original</b>", self.styles['Normal']),
                    Paragraph("<b>Supervisor Revised</b>", self.styles['Normal'])
                ])
                comp_data.append([
                    Paragraph(f"Score: {ai_score}", self.styles['Normal']),
                    Paragraph(score_text, self.styles['Normal'])
                ])
                comp_data.append([
                    Paragraph(ai_just, self.styles['Normal']),
                    Paragraph(supervisor_just, self.styles['Normal'])
                ])
                
                comp_table = Table(comp_data, colWidths=[3*inch, 3*inch])
                comp_table.setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('BACKGROUND', (0, 0), (1, 0), colors.HexColor("#e8e8e8")),
                ]))
                
                elements.append(comp_table)
                elements.append(Spacer(1, 0.2*inch))
        
        # Footer
        elements.append(Spacer(1, 0.5*inch))
        footer_style = ParagraphStyle(
            name='ComparisonFooter',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#666666'),
            alignment=TA_CENTER
        )
        elements.append(Paragraph(
            f"Report generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            footer_style
        ))
        
        # Build PDF
        doc.build(elements)
        
        # Read and return PDF content
        with open("temp_comparison.pdf", 'rb') as f:
            pdf_content = f.read()
        
        # Clean up temp file
        os.remove("temp_comparison.pdf")
        
        return pdf_content