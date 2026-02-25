"""
PDF Export Module for Health & Safety Dashboard

This module handles generating PDF reports from the dashboard data,
including KPIs, performance matrix, and charts.

Author: Senior Frontend Engineer & Python Developer
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO
import base64
from typing import Dict, Optional
from datetime import datetime


def export_plotly_to_image(fig: go.Figure, format: str = 'png', width: int = 1200, height: int = 600) -> BytesIO:
    """
    Export a Plotly figure to an image buffer.
    
    Args:
        fig: Plotly figure object
        format: Image format ('png', 'jpeg', 'svg', 'pdf')
        width: Image width in pixels
        height: Image height in pixels
    
    Returns:
        BytesIO: Image buffer
    
    Side Effects:
        None (creates image buffer)
    """
    try:
        img_bytes = fig.to_image(format=format, width=width, height=height, engine='kaleido')
        return BytesIO(img_bytes)
    except Exception as e:
        # Fallback: return empty image
        print(f"Error exporting chart: {str(e)}")
        return BytesIO()


def create_pdf_report(kpis: Dict,
                     matrix_df: pd.DataFrame,
                     timeline_chart: Optional[go.Figure] = None,
                     pie_chart: Optional[go.Figure] = None,
                     reporting_year: str = "FY 2025",
                     output_path: str = "dashboard_report.pdf") -> BytesIO:
    """
    Create a PDF report from dashboard data.
    
    Args:
        kpis: Dictionary of KPI values
        matrix_df: Performance matrix DataFrame
        timeline_chart: Plotly figure for timeline chart (optional)
        pie_chart: Plotly figure for pie chart (optional)
        reporting_year: Reporting year string
        output_path: Output file path
    
    Returns:
        BytesIO: PDF file buffer
    
    Side Effects:
        Creates PDF file
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#001f3f'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#666666'),
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#001f3f'),
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )
    
    # Header
    story.append(Paragraph("HEALTH & SAFETY DASHBOARD", title_style))
    story.append(Paragraph("CONTRACTOR PERFORMANCE MATRIX", subtitle_style))
    story.append(Paragraph(f"Reporting Period: {reporting_year}", subtitle_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", 
                          styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # KPI Section
    story.append(Paragraph("KEY PERFORMANCE INDICATORS", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Create KPI table
    kpi_data = [
        ['Metric', 'Value'],
        ['Accidents', f"{kpis.get('total_accidents', 0):,.0f}"],
        ['Incidents', f"{kpis.get('total_incidents', 0):,.0f}"],
        ['Hazards Identified', f"{kpis.get('total_hazards', 0):,.0f}"],
        ['Near Misses', f"{kpis.get('near_misses', 0):,.0f}"],
        ['Total Hours', f"{kpis.get('total_hours', kpis.get('total_man_hours', 0)):,.2f}"],
    ]
    
    kpi_table = Table(kpi_data, colWidths=[4*inch, 2*inch])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#001f3f')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
    ]))
    
    story.append(kpi_table)
    story.append(Spacer(1, 0.4*inch))
    
    # Performance Matrix Section
    story.append(Paragraph("SAFETY PERFORMANCE MATRIX", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Convert matrix DataFrame to table
    if not matrix_df.empty:
        # Prepare matrix data for PDF table
        matrix_data = [matrix_df.columns.tolist()]  # Header
        for _, row in matrix_df.iterrows():
            matrix_data.append([str(val) for val in row.values])
        
        # Create table with appropriate column widths
        num_cols = len(matrix_df.columns)
        col_widths = [1.2*inch] + [0.5*inch] * 12 + [0.8*inch] * 3  # KPI + 12 months + 3 calc columns
        
        matrix_table = Table(matrix_data, colWidths=col_widths[:num_cols])
        matrix_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#001f3f')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),  # First column left-aligned
        ]))
        
        story.append(matrix_table)
        story.append(Spacer(1, 0.4*inch))
    
    # Charts Section
    if timeline_chart or pie_chart:
        story.append(Paragraph("VISUALIZATIONS", heading_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Timeline Chart
        if timeline_chart:
            try:
                img_buffer = export_plotly_to_image(timeline_chart, format='png', width=1000, height=500)
                img_buffer.seek(0)
                img = Image(img_buffer, width=7*inch, height=3.5*inch)
                story.append(img)
                story.append(Spacer(1, 0.3*inch))
            except Exception as e:
                story.append(Paragraph(f"Chart export error: {str(e)}", styles['Normal']))
        
        # Pie Chart
        if pie_chart:
            try:
                img_buffer = export_plotly_to_image(pie_chart, format='png', width=800, height=600)
                img_buffer.seek(0)
                img = Image(img_buffer, width=5*inch, height=3.75*inch)
                story.append(img)
            except Exception as e:
                story.append(Paragraph(f"Chart export error: {str(e)}", styles['Normal']))
    
    # Footer
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("This report was generated automatically by the Health & Safety Dashboard.", 
                          styles['Normal']))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer


def generate_pdf_download(kpis: Dict,
                          matrix_df: pd.DataFrame,
                          timeline_chart: Optional[go.Figure] = None,
                          pie_chart: Optional[go.Figure] = None,
                          reporting_year: str = "FY 2025") -> bytes:
    """
    Generate PDF and return as bytes for Streamlit download.
    
    Args:
        kpis: Dictionary of KPI values
        matrix_df: Performance matrix DataFrame
        timeline_chart: Plotly figure for timeline chart (optional)
        pie_chart: Plotly figure for pie chart (optional)
        reporting_year: Reporting year string
    
    Returns:
        bytes: PDF file as bytes
    
    Side Effects:
        None (creates PDF in memory)
    """
    pdf_buffer = create_pdf_report(
        kpis=kpis,
        matrix_df=matrix_df,
        timeline_chart=timeline_chart,
        pie_chart=pie_chart,
        reporting_year=reporting_year
    )
    return pdf_buffer.read()
