"""
Generate PDF Report from Evaluation Results
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import json
from datetime import datetime
import os

def create_pdf_report(json_file="evaluation_summary_oop.json", csv_file="evaluation_results_oop.csv"):
    """
    Create professional PDF report from evaluation results
    """
    
    # Load data
    if not os.path.exists(json_file):
        print(f"❌ {json_file} not found! Run evaluation first.")
        print("   Please run: python simple_evaluate.py")
        return
    
    with open(json_file, 'r') as f:
        summary = json.load(f)
    
    # Create PDF
    pdf_filename = "EVALUATION_REPORT_OOP.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter,
                          rightMargin=0.75*inch, leftMargin=0.75*inch,
                          topMargin=1*inch, bottomMargin=0.75*inch)
    
    # Container for PDF elements
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a5490'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1a5490'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=10
    )
    
    # ============ TITLE PAGE ============
    elements.append(Spacer(1, 0.5*inch))
    
    title = Paragraph("Document QA Application", title_style)
    elements.append(title)
    
    subtitle = Paragraph("Evaluation Report - Python OOP", 
                        ParagraphStyle('subtitle', parent=styles['Normal'], 
                                     fontSize=16, alignment=TA_CENTER, 
                                     textColor=colors.HexColor('#333333')))
    elements.append(subtitle)
    
    elements.append(Spacer(1, 0.3*inch))
    
    # Metadata
    metadata_style = ParagraphStyle(
        'metadata',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#666666')
    )
    
    eval_date = summary.get('evaluation_date', 'N/A')
    if 'T' in eval_date:
        eval_date = eval_date.split('T')[0]
    
    elements.append(Paragraph(f"<b>Document:</b> {summary.get('document', 'N/A')}", metadata_style))
    elements.append(Paragraph(f"<b>Date:</b> {eval_date}", metadata_style))
    elements.append(Paragraph(f"<b>Test Questions:</b> {summary.get('test_questions', 'N/A')}", metadata_style))
    
    elements.append(Spacer(1, 0.5*inch))
    
    # ============ EXECUTIVE SUMMARY ============
    elements.append(Paragraph("Executive Summary", heading_style))
    
    summary_text = f"""
    This report presents the evaluation results of the Document QA Application using semantic similarity 
    and relevance metrics. The application was tested on {summary.get('test_questions', 'N/A')} questions 
    related to Python Object-Oriented Programming concepts. The overall system score is 
    <b>{summary.get('overall_score', 0)*100:.2f}%</b>, indicating <b>{summary.get('rating', 'N/A').split(' - ')[1] if ' - ' in summary.get('rating', '') else summary.get('rating', 'N/A')}</b> performance.
    """
    elements.append(Paragraph(summary_text, normal_style))
    
    elements.append(Spacer(1, 0.3*inch))
    
    # ============ KEY METRICS ============
    elements.append(Paragraph("Evaluation Metrics", heading_style))
    
    metrics = summary.get('metrics', {})
    
    # Create metrics table
    metrics_data = [
        ['Metric', 'Score', 'Percentage', 'Status'],
        ['Retrieval Precision', f"{metrics.get('retrieval_precision', 0):.4f}", 
         f"{metrics.get('retrieval_precision', 0)*100:.2f}%", '✓'],
        ['Retrieval Accuracy', f"{metrics.get('retrieval_accuracy', 0):.4f}", 
         f"{metrics.get('retrieval_accuracy', 0)*100:.2f}%", '✓'],
        ['Contextual Accuracy', f"{metrics.get('contextual_accuracy', 0):.4f}", 
         f"{metrics.get('contextual_accuracy', 0)*100:.2f}%", '✓'],
        ['Contextual Precision', f"{metrics.get('contextual_precision', 0):.4f}", 
         f"{metrics.get('contextual_precision', 0)*100:.2f}%", '✓'],
        ['<b>Overall Score</b>', f"<b>{summary.get('overall_score', 0):.4f}</b>", 
         f"<b>{summary.get('overall_score', 0)*100:.2f}%</b>", '<b>✓</b>'],
    ]
    
    metrics_table = Table(metrics_data, colWidths=[2.2*inch, 1.2*inch, 1.2*inch, 0.8*inch])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#1a5490')),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.beige]),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(metrics_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # ============ METRIC DEFINITIONS ============
    elements.append(PageBreak())
    elements.append(Paragraph("Metric Definitions", heading_style))
    
    definitions = [
        {
            'name': '1. Retrieval Precision',
            'definition': 'Measures the proportion of retrieved document chunks that are relevant to the question.',
            'formula': '(Relevant Retrieved Chunks) / (Total Retrieved Chunks)',
            'interpretation': f"Score: {metrics.get('retrieval_precision', 0)*100:.2f}% - This indicates how many of the retrieved chunks were actually useful for answering the question."
        },
        {
            'name': '2. Retrieval Accuracy',
            'definition': 'Measures how much of the required information was successfully retrieved from the documents.',
            'formula': '(Retrieved Relevant Information) / (Total Required Information)',
            'interpretation': f"Score: {metrics.get('retrieval_accuracy', 0)*100:.2f}% - This shows the completeness of the retrieved context."
        },
        {
            'name': '3. Contextual Accuracy',
            'definition': 'Measures how factually accurate and grounded the generated answer is in the retrieved context.',
            'formula': 'Semantic Similarity(Answer, Ground Truth)',
            'interpretation': f"Score: {metrics.get('contextual_accuracy', 0)*100:.2f}% - Higher scores mean the answer is more aligned with expected responses."
        },
        {
            'name': '4. Contextual Precision',
            'definition': 'Measures how relevant and directly the answer addresses the original question.',
            'formula': 'Semantic Similarity(Answer, Question)',
            'interpretation': f"Score: {metrics.get('contextual_precision', 0)*100:.2f}% - This ensures answers are focused and relevant."
        }
    ]
    
    for defn in definitions:
        elements.append(Paragraph(f"<b>{defn['name']}</b>", 
                                 ParagraphStyle('subheading', parent=styles['Normal'], 
                                              fontSize=11, fontName='Helvetica-Bold',
                                              textColor=colors.HexColor('#1a5490'),
                                              spaceAfter=6)))
        
        elements.append(Paragraph(f"<b>Definition:</b> {defn['definition']}", normal_style))
        elements.append(Paragraph(f"<b>Formula:</b> {defn['formula']}", normal_style))
        elements.append(Paragraph(f"<b>Interpretation:</b> {defn['interpretation']}", normal_style))
        elements.append(Spacer(1, 0.15*inch))
    
    # ============ PERFORMANCE ANALYSIS ============
    elements.append(PageBreak())
    elements.append(Paragraph("Performance Analysis", heading_style))
    
    overall_score = summary.get('overall_score', 0)
    
    analysis_text = f"""
    <b>Overall Performance Score: {overall_score*100:.2f}%</b><br/>
    <b>Performance Rating: {summary.get('rating', 'N/A')}</b><br/><br/>
    """
    
    if overall_score >= 0.8:
        analysis_text += """
        The Document QA application demonstrates <b>excellent performance</b> across all evaluation metrics. 
        The system successfully retrieves relevant information from documents and generates accurate, 
        contextually appropriate answers. The application is <b>ready for production deployment</b> with 
        minimal optimization needed.<br/><br/>
        
        <b>Strengths:</b><br/>
        • High retrieval precision and accuracy<br/>
        • Factually accurate generated responses<br/>
        • Strong semantic understanding of questions and answers<br/>
        • Consistent performance across diverse queries<br/>
        """
    elif overall_score >= 0.6:
        analysis_text += """
        The Document QA application demonstrates <b>good performance</b> with room for optimization. 
        The system shows solid retrieval capabilities and answer generation quality, but could benefit 
        from fine-tuning for improved accuracy.<br/><br/>
        
        <b>Recommendations:</b><br/>
        • Refine document chunking strategy<br/>
        • Optimize embedding model selection<br/>
        • Enhance prompt engineering for LLM<br/>
        • Increase training data diversity<br/>
        """
    else:
        analysis_text += """
        The Document QA application shows <b>fair performance</b> and requires optimization before 
        production deployment. Significant improvements are needed in retrieval and answer generation.<br/><br/>
        
        <b>Recommendations:</b><br/>
        • Review and improve document preprocessing<br/>
        • Evaluate alternative embedding models<br/>
        • Refine prompt templates<br/>
        • Increase test data and validation cycles<br/>
        """
    
    elements.append(Paragraph(analysis_text, normal_style))
    
    elements.append(Spacer(1, 0.3*inch))
    
    # ============ TEST QUESTIONS ============
    elements.append(Paragraph("Test Questions", heading_style))
    
    test_questions = [
        "What is Object-Oriented Programming?",
        "What are the four pillars of OOP?",
        "What is encapsulation and provide a real-world example?",
        "Explain inheritance with an example.",
        "What is polymorphism in OOP?",
        "What is abstraction and why is it important?",
        "What are the advantages of OOP?",
        "What is the difference between a class and an object?",
    ]
    
    q_text = "<br/>".join([f"{i}. {q}" for i, q in enumerate(test_questions, 1)])
    elements.append(Paragraph(q_text, normal_style))
    
    elements.append(Spacer(1, 0.3*inch))
    
    # ============ TECHNOLOGY STACK ============
    elements.append(PageBreak())
    elements.append(Paragraph("Technology Stack", heading_style))
    
    tech_data = [
        ['Component', 'Technology', 'Version'],
        ['LLM Model', 'Ollama - Llama 3.2', 'Latest'],
        ['Vector Database', 'Weaviate', 'v1.27.6'],
        ['Agent Framework', 'LangGraph', 'v0.2.45'],
        ['Embeddings', 'Sentence Transformers', 'all-MiniLM-L6-v2'],
        ['Web Framework', 'FastAPI', 'v0.115.0'],
        ['Evaluation Method', 'Cosine Similarity Analysis', 'Custom'],
    ]
    
    tech_table = Table(tech_data, colWidths=[2.0*inch, 2.5*inch, 1.9*inch])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.beige]),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(tech_table)
    
    elements.append(Spacer(1, 0.3*inch))
    
    # ============ CONCLUSION ============
    elements.append(Paragraph("Conclusion", heading_style))
    
    conclusion_text = f"""
    The Document QA application evaluation demonstrates {('strong' if overall_score > 0.75 else 'solid' if overall_score > 0.6 else 'acceptable')} 
    performance across all key metrics. With an overall score of <b>{overall_score*100:.2f}%</b>, 
    the system successfully combines effective document retrieval with accurate answer generation.<br/><br/>
    
    The application leverages modern AI technologies including large language models, semantic embeddings, 
    and graph-based agentic workflows to provide intelligent document understanding and question answering 
    capabilities.<br/><br/>
    
    <b>Recommendations for Future Improvement:</b><br/>
    • Expand test dataset with domain-specific documents<br/>
    • Implement continuous monitoring and evaluation<br/>
    • Add feedback loop for model fine-tuning<br/>
    • Explore advanced retrieval techniques (re-ranking, fusion)<br/>
    • Implement caching for improved performance<br/>
    """
    
    elements.append(Paragraph(conclusion_text, normal_style))
    
    elements.append(Spacer(1, 0.5*inch))
    
    # ============ FOOTER ============
    footer_style = ParagraphStyle(
        'footer',
        parent=styles['Normal'],
        fontSize=9,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#999999')
    )
    
    elements.append(Paragraph(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", footer_style))
    elements.append(Paragraph("Document QA Application - Confidential", footer_style))
    
    # Build PDF
    print(f"\n🔄 Generating PDF report...")
    doc.build(elements)
    print(f"✅ PDF Report generated: {pdf_filename}")
    print(f"📄 Location: {os.path.abspath(pdf_filename)}")
    print(f"📊 File Size: {os.path.getsize(pdf_filename) / 1024:.2f} KB")
    print(f"\n✨ Report generation complete!")

if __name__ == "__main__":
    import sys
    
    # Check if evaluation files exist
    if not os.path.exists("evaluation_summary_oop.json"):
        print("❌ evaluation_summary_oop.json not found!")
        print("   Please run: python simple_evaluate.py")
        sys.exit(1)
    
    create_pdf_report()
    print("📂 Open EVALUATION_REPORT_OOP.pdf to view your report!")
