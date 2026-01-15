"""
Simple Student Level Project Report Generator
Aadhaar Enrolment Study for Maharashtra
"""

import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(BASE_DIR, 'UIDAI_Report.pdf')

DARK_BLUE = colors.HexColor('#1e3a5f')
DARK_TEXT = colors.HexColor('#1f2937')
LIGHT_GRAY = colors.HexColor('#e5e7eb')


def create_styles():
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(
        name='ReportTitle',
        fontSize=18,
        leading=24,
        alignment=TA_CENTER,
        textColor=DARK_BLUE,
        spaceAfter=12,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='AuthorInfo',
        fontSize=11,
        leading=16,
        alignment=TA_CENTER,
        textColor=DARK_TEXT,
        spaceAfter=6,
        fontName='Helvetica'
    ))
    
    styles.add(ParagraphStyle(
        name='SectionTitle',
        fontSize=14,
        leading=18,
        textColor=DARK_BLUE,
        spaceBefore=20,
        spaceAfter=12,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='BodyParagraph',
        fontSize=11,
        leading=16,
        alignment=TA_JUSTIFY,
        textColor=DARK_TEXT,
        spaceAfter=12,
        fontName='Helvetica'
    ))
    
    return styles


def add_header_footer(canvas, doc):
    canvas.saveState()
    
    canvas.setStrokeColor(DARK_BLUE)
    canvas.setLineWidth(1)
    canvas.line(2*cm, A4[1] - 1.5*cm, A4[0] - 2*cm, A4[1] - 1.5*cm)
    
    canvas.setFont('Helvetica', 9)
    canvas.setFillColor(colors.gray)
    canvas.drawString(2*cm, A4[1] - 1.2*cm, "Student Project Report")
    canvas.drawRightString(A4[0] - 2*cm, A4[1] - 1.2*cm, "Maharashtra Enrolment Study")
    
    canvas.setStrokeColor(LIGHT_GRAY)
    canvas.line(2*cm, 1.5*cm, A4[0] - 2*cm, 1.5*cm)
    
    canvas.setFont('Helvetica', 9)
    canvas.drawCentredString(A4[0]/2, 0.8*cm, f"Page {doc.page}")
    
    canvas.restoreState()


def create_cover_page(styles):
    elements = []
    
    elements.append(Spacer(1, 2*inch))
    
    elements.append(Paragraph(
        "Aadhaar Enrolment Study for Maharashtra",
        styles['ReportTitle']
    ))
    
    elements.append(Spacer(1, 0.5*inch))
    
    elements.append(HRFlowable(
        width="50%", thickness=2, color=DARK_BLUE,
        spaceBefore=10, spaceAfter=10, hAlign='CENTER'
    ))
    
    elements.append(Spacer(1, 0.5*inch))
    
    elements.append(Paragraph("Project Report", styles['AuthorInfo']))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("Mandar Kajbaje", styles['ReportTitle']))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("BSc Computer Science", styles['AuthorInfo']))
    elements.append(Paragraph("Year 2026", styles['AuthorInfo']))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("Team ID UIDAI 3519", styles['AuthorInfo']))
    
    elements.append(Spacer(1, 1.5*inch))
    
    elements.append(Paragraph(
        f"Submitted on {datetime.now().strftime('%d %B %Y')}",
        styles['AuthorInfo']
    ))
    
    elements.append(PageBreak())
    return elements


def create_introduction(styles):
    elements = []
    
    elements.append(Paragraph("Introduction", styles['SectionTitle']))
    
    elements.append(Paragraph(
        "This project studies enrolment data for Maharashtra. The data is freely available as open data. The goal is to understand how enrolment happens across the state.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "Maharashtra is a large state with many districts. Each district has different enrolment numbers. This study looks at those numbers to find patterns.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "The project uses simple methods to analyze the data. Charts and graphs help show the results clearly. The findings are easy to understand.",
        styles['BodyParagraph']
    ))
    
    return elements


def create_dataset_overview(styles):
    elements = []
    
    elements.append(Paragraph("Dataset Overview", styles['SectionTitle']))
    
    elements.append(Paragraph(
        "The dataset contains enrolment records for Maharashtra. Each record shows how many people enrolled in a given month. The data covers many months over several years.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "The records are organized by district. Maharashtra has many districts. Each district has its own enrolment numbers.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "The data also shows age groups. There are three age groups in the data. The first group is children up to five years old. The second group is children from five to seventeen years. The third group is adults.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "The dataset has over ninety thousand records. It covers more than fifty districts. This gives a good view of enrolment across the state.",
        styles['BodyParagraph']
    ))
    
    return elements


def create_method_used(styles):
    elements = []
    
    elements.append(Paragraph("Method Used", styles['SectionTitle']))
    
    elements.append(Paragraph(
        "The data was first cleaned to remove errors. Missing values were handled. Dates were checked for correctness.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "Next the data was grouped in different ways. One grouping was by month. This showed how enrolment changed over time. Another grouping was by district. This showed which districts had more enrolment.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "The data was also grouped by age. This showed which age groups had more enrolment. Children and adults were compared.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "Charts were made to show the results. Line charts showed trends over time. Bar charts compared districts. These charts made the patterns easy to see.",
        styles['BodyParagraph']
    ))
    
    return elements


def create_findings(styles):
    elements = []
    
    elements.append(Paragraph("Findings", styles['SectionTitle']))
    
    elements.append(Paragraph(
        "The study found that child enrolment is much higher than adult enrolment. Most new enrolments are for young children. This is because most adults already have their records.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "Children under five years make up the largest share. School age children also have high numbers. Adult enrolment is very low in comparison.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "Some districts show more activity than others. Large districts like Thane and Pune have high numbers. Smaller districts have fewer enrolments. This shows differences across the state.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "Some months have higher enrolment than others. April and July show peaks in the data. These months may relate to school admissions. Understanding these patterns helps in planning.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "Overall enrolment has grown over time. But recent months show slower growth. This may mean that coverage is becoming more complete.",
        styles['BodyParagraph']
    ))
    
    return elements


def create_learning_outcomes(styles):
    elements = []
    
    elements.append(Paragraph("Learning Outcomes", styles['SectionTitle']))
    
    elements.append(Paragraph(
        "This project taught me how to work with real data. I learned how to clean data and prepare it for analysis. This is an important skill for any data project.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "I learned how to group data in different ways. Grouping by time shows trends. Grouping by location shows differences between areas. Grouping by category shows how groups compare.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "Making charts helped me understand the data better. Visual displays make patterns clear. They also help explain findings to others.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "I learned that data can help in planning. When we know which areas need more attention we can focus efforts there. When we know which months are busy we can prepare for them.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "This project showed me the value of open data. When data is shared it can be studied and used to make better decisions. This benefits everyone.",
        styles['BodyParagraph']
    ))
    
    return elements


def create_conclusion(styles):
    elements = []
    
    elements.append(Paragraph("Conclusion", styles['SectionTitle']))
    
    elements.append(Paragraph(
        "This study looked at enrolment data for Maharashtra. The data covered many months and all districts in the state. Simple methods were used to analyze the data.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "The findings show clear patterns. Child enrolment dominates current activity. Districts differ in their enrolment numbers. Some months are busier than others.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "These findings help understand how enrolment works in Maharashtra. They can guide future planning. Areas with low numbers can get more attention. Busy months can have more resources.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "Data analysis is a useful tool. It turns raw numbers into useful information. This project shows how even simple analysis can provide valuable insights.",
        styles['BodyParagraph']
    ))
    
    elements.append(Spacer(1, 1*inch))
    
    elements.append(HRFlowable(width="30%", thickness=1, color=DARK_BLUE, hAlign='CENTER'))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph(
        "End of Report",
        ParagraphStyle('EndNote', fontSize=11, alignment=TA_CENTER, textColor=DARK_TEXT, fontName='Helvetica-Bold')
    ))
    
    return elements


def generate_student_report():
    print("Creating student report...")
    
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2.5*cm,
        bottomMargin=2.5*cm
    )
    
    styles = create_styles()
    elements = []
    
    elements.extend(create_cover_page(styles))
    elements.extend(create_introduction(styles))
    elements.extend(create_dataset_overview(styles))
    elements.extend(create_method_used(styles))
    elements.extend(create_findings(styles))
    elements.extend(create_learning_outcomes(styles))
    elements.extend(create_conclusion(styles))
    
    doc.build(elements, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    
    print(f"Student report generated at {OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == '__main__':
    generate_student_report()
