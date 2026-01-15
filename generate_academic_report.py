"""
UIDAI Aadhaar Enrolment Analysis Report Generator
Academic PDF for Government Data Hackathon
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
OUTPUT_PATH = os.path.join(BASE_DIR, 'UIDAI_Report_Maharashtra.pdf')

# Simple color palette
DARK_BLUE = colors.HexColor('#1e3a5f')
DARK_TEXT = colors.HexColor('#1f2937')
LIGHT_GRAY = colors.HexColor('#e5e7eb')


def create_styles():
    """Create paragraph styles for the academic report."""
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
    
    styles.add(ParagraphStyle(
        name='PageFooter',
        fontSize=9,
        leading=11,
        alignment=TA_CENTER,
        textColor=colors.gray
    ))
    
    return styles


def add_header_footer(canvas, doc):
    """Add simple header and footer."""
    canvas.saveState()
    
    # Header line
    canvas.setStrokeColor(DARK_BLUE)
    canvas.setLineWidth(1)
    canvas.line(2*cm, A4[1] - 1.5*cm, A4[0] - 2*cm, A4[1] - 1.5*cm)
    
    # Header text
    canvas.setFont('Helvetica', 9)
    canvas.setFillColor(colors.gray)
    canvas.drawString(2*cm, A4[1] - 1.2*cm, "UIDAI Data Hackathon 2026")
    canvas.drawRightString(A4[0] - 2*cm, A4[1] - 1.2*cm, "Maharashtra Enrolment Analysis")
    
    # Footer line
    canvas.setStrokeColor(LIGHT_GRAY)
    canvas.line(2*cm, 1.5*cm, A4[0] - 2*cm, 1.5*cm)
    
    # Footer text
    canvas.setFont('Helvetica', 9)
    canvas.drawCentredString(A4[0]/2, 0.8*cm, f"Page {doc.page}")
    
    canvas.restoreState()


def create_cover_page(styles):
    """Create the title page."""
    elements = []
    
    elements.append(Spacer(1, 2*inch))
    
    # Title
    elements.append(Paragraph(
        "UIDAI Aadhaar Enrolment Analysis for Maharashtra",
        styles['ReportTitle']
    ))
    
    elements.append(Spacer(1, 0.5*inch))
    
    elements.append(HRFlowable(
        width="50%", thickness=2, color=DARK_BLUE,
        spaceBefore=10, spaceAfter=10, hAlign='CENTER'
    ))
    
    elements.append(Spacer(1, 0.5*inch))
    
    # Author details
    elements.append(Paragraph("Submitted by", styles['AuthorInfo']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("Mandar Kajbaje", styles['ReportTitle']))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("BSc Computer Science", styles['AuthorInfo']))
    elements.append(Paragraph("Expected Graduation Year 2026", styles['AuthorInfo']))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("Team ID UIDAI 3519", styles['AuthorInfo']))
    
    elements.append(Spacer(1, 1.5*inch))
    
    # Submission date
    elements.append(Paragraph(
        f"Submitted on {datetime.now().strftime('%d %B %Y')}",
        styles['AuthorInfo']
    ))
    
    elements.append(PageBreak())
    return elements


def create_introduction(styles):
    """Create the introduction section."""
    elements = []
    
    elements.append(Paragraph("1. Introduction", styles['SectionTitle']))
    
    elements.append(Paragraph(
        "Aadhaar is the foundation of digital identity in India. It provides a unique twelve digit number to every resident and enables access to government services and benefits. The Unique Identification Authority of India manages this system and ensures that enrolment reaches all citizens across the country.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "Maharashtra is one of the most populous states in India. It has a diverse population spread across urban centers and rural areas. Understanding enrolment patterns in Maharashtra helps the government plan better and serve citizens more effectively.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "This report presents an analysis of Aadhaar enrolment data for Maharashtra. The analysis covers monthly trends, district level patterns, age group distribution, and seasonal variations. The findings provide useful information for planning and decision making.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "The purpose of this study is to help UIDAI understand where enrolment is growing, where it is slowing down, and which areas need more attention. By examining the data carefully, we can identify opportunities to improve service delivery and reach underserved populations.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "Data driven analysis is important for government programs. It helps in making informed decisions based on facts rather than assumptions. This report aims to demonstrate how enrolment data can be used to support evidence based planning for Aadhaar services in Maharashtra.",
        styles['BodyParagraph']
    ))
    
    return elements


def create_dataset_description(styles):
    """Create the dataset description section."""
    elements = []
    
    elements.append(Paragraph("2. Dataset Description", styles['SectionTitle']))
    
    elements.append(Paragraph(
        "The dataset used for this analysis contains aggregated Aadhaar enrolment information for Maharashtra. The data covers multiple years and includes monthly records for all districts in the state. This aggregated format protects individual privacy while providing useful information for analysis.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "The dataset includes enrolment counts organized by month, district, and pincode. Each record shows how many people enrolled for Aadhaar in a specific location during a specific month. This granular information allows for detailed analysis at different geographic levels.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "Age group information is also included in the dataset. Enrolments are categorized into three groups. The first group covers children from birth to five years. The second group covers children from five to seventeen years. The third group covers adults who are eighteen years and older.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "The dataset contains over ninety thousand records spanning more than one hundred months of data. It covers fifty three districts and over fifteen hundred unique pincodes across Maharashtra. This comprehensive coverage ensures that the analysis reflects the entire state.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "The data quality is high as it comes from official UIDAI sources. The aggregated nature of the data means that individual details are not exposed while still providing meaningful insights about enrolment patterns. This balance between privacy and utility makes the data suitable for policy analysis.",
        styles['BodyParagraph']
    ))
    
    return elements


def create_methodology(styles):
    """Create the methodology section."""
    elements = []
    
    elements.append(Paragraph("3. Methodology", styles['SectionTitle']))
    
    elements.append(Paragraph(
        "The analysis followed a systematic approach to ensure accurate and reliable results. The first step involved cleaning the data to handle any missing or inconsistent values. Date formats were standardized and numeric fields were verified for correctness.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "After cleaning, the data was aggregated at different levels. Monthly totals were calculated at the state level to understand overall trends. District level aggregations helped identify geographic variations. Pincode level analysis revealed local patterns within districts.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "Trend analysis was performed to understand how enrolment has changed over time. This involved comparing monthly figures across the observation period. Growth rates were calculated to measure the pace of enrolment activity. Recent trends were compared with historical patterns to identify shifts in momentum.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "Disparity analysis focused on differences between districts. Some districts show high enrolment numbers while others show very low activity. By ranking districts and comparing their performance, we identified areas that may need additional attention or resources.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "Seasonality analysis examined month of year patterns. Enrolment activity often follows predictable cycles related to school admissions and other annual events. Understanding these patterns helps in planning campaigns and allocating resources at the right times.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "Age group analysis looked at the distribution of enrolments across different age categories. This revealed which population segments are driving current enrolment activity. The analysis helps in understanding whether the focus should be on children or adults.",
        styles['BodyParagraph']
    ))
    
    return elements


def create_key_findings(styles):
    """Create the key findings section."""
    elements = []
    
    elements.append(Paragraph("4. Key Findings", styles['SectionTitle']))
    
    # Overall trend
    elements.append(Paragraph(
        "The overall enrolment trend shows significant growth over the observation period. From the earliest months to the most recent data, enrolment activity has increased substantially. This indicates successful implementation of Aadhaar programs across Maharashtra.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "However, recent monthly data shows a gradual slowdown in the rate of new enrolments. This is expected as Aadhaar coverage approaches saturation levels. Most adults in Maharashtra already have Aadhaar cards, so new enrolments are increasingly focused on newborns and children.",
        styles['BodyParagraph']
    ))
    
    # Age distribution
    elements.append(Paragraph(
        "Age group analysis reveals that children dominate current enrolment activity. The youngest age group from birth to five years accounts for the majority of new enrolments. This is because most adults have already enrolled while new children continue to be born.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "School age children from five to seventeen years also contribute significantly to enrolment numbers. The adult category shows minimal new enrolments, with most adult activity being updates rather than fresh registrations. This pattern confirms that Maharashtra has achieved high adult coverage.",
        styles['BodyParagraph']
    ))
    
    # District differences
    elements.append(Paragraph(
        "District level analysis shows significant variation across Maharashtra. Some districts like Thane, Pune, and Nashik report very high enrolment numbers. These are large urban districts with high population density and good infrastructure availability.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "Other districts show much lower enrolment activity. Some remote and rural districts have very few monthly enrolments. This disparity suggests that enrolment infrastructure may not be equally distributed across the state. Areas with low activity may need additional attention.",
        styles['BodyParagraph']
    ))
    
    # Seasonal patterns
    elements.append(Paragraph(
        "Seasonality analysis identified predictable patterns in enrolment activity. Certain months consistently show higher than average enrolments. July and April emerge as peak months for Aadhaar enrolment in Maharashtra.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "These peaks appear to coincide with the academic calendar. April marks the beginning of the school year when many parents register children for Aadhaar. July may correspond to post admission requirements or mid year enrolment drives organized by schools.",
        styles['BodyParagraph']
    ))
    
    # Child focus
    elements.append(Paragraph(
        "The analysis confirms that child enrolment is now the primary focus of Aadhaar activity in Maharashtra. Nearly all new enrolments are for children under eighteen years. This shift from adult to child enrolment marks a new phase in the Aadhaar program.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "This finding has important implications for service delivery. Enrolment centers need to be equipped for child specific requirements. Staff should be trained in handling infant biometrics. Partnerships with hospitals and schools become strategically important.",
        styles['BodyParagraph']
    ))
    
    elements.append(PageBreak())
    return elements


def create_policy_insights(styles):
    """Create the policy insights section."""
    elements = []
    
    elements.append(Paragraph("5. Policy Insights", styles['SectionTitle']))
    
    elements.append(Paragraph(
        "The findings from this analysis provide several useful insights for policy planning. These insights can help UIDAI improve service delivery and ensure that Aadhaar benefits reach all citizens in Maharashtra.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "First, the dominance of child enrolments suggests that infrastructure should be optimized for young registrants. This includes ensuring that enrolment centers have appropriate equipment for capturing infant biometrics. Training programs for staff should emphasize child friendly procedures.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "Second, the district level disparities indicate a need for targeted interventions. Districts with very low enrolment activity may lack adequate infrastructure or awareness. Mobile enrolment units could be deployed to reach underserved areas. Awareness campaigns in local languages may help increase participation.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "Third, the seasonal patterns can guide campaign planning. Launching enrolment drives before peak months like April and July would maximize impact. Additional staff and equipment can be arranged in advance to handle increased demand during these periods.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "Fourth, partnerships with health and education departments can improve reach. Hospitals can facilitate Aadhaar registration at birth. Schools can organize enrolment camps for students who do not yet have Aadhaar. These partnerships align with natural points of contact with the target population.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "Fifth, as saturation levels increase, the focus should shift from quantity to quality. In areas where most people already have Aadhaar, the emphasis should be on service quality, update facilities, and grievance resolution. This ensures continued citizen satisfaction with the Aadhaar system.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "Finally, continuous monitoring of enrolment data helps in early identification of issues. Districts showing unusual patterns or declining activity can be investigated promptly. Data driven monitoring enables proactive rather than reactive management of the enrolment program.",
        styles['BodyParagraph']
    ))
    
    return elements


def create_conclusion(styles):
    """Create the conclusion section."""
    elements = []
    
    elements.append(Paragraph("6. Conclusion", styles['SectionTitle']))
    
    elements.append(Paragraph(
        "This report has presented a comprehensive analysis of Aadhaar enrolment patterns in Maharashtra. The analysis examined monthly trends, district level variations, age group distribution, and seasonal patterns. The findings provide a clear picture of the current state of Aadhaar enrolment in the state.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "The data shows that Maharashtra has made significant progress in Aadhaar coverage. The shift from adult to child enrolments indicates that the adult population is largely covered. Current activity focuses on registering newborns and children, which is a sign of program maturity.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "However, challenges remain in ensuring equitable coverage across all districts. Some areas show significantly lower enrolment activity compared to others. Addressing these disparities requires targeted interventions and resource allocation based on local needs.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "The seasonal patterns identified in this analysis can help in better planning of enrolment activities. Aligning campaigns with peak demand periods improves efficiency and reduces citizen wait times. Understanding these patterns enables proactive resource management.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "Data analysis plays a crucial role in supporting evidence based decision making. By examining enrolment data systematically, UIDAI can identify opportunities for improvement and track progress over time. This analytical approach ensures that policies are grounded in facts rather than assumptions.",
        styles['BodyParagraph']
    ))
    
    elements.append(Paragraph(
        "In conclusion, this analysis demonstrates the value of data driven insights for government programs. The findings can help UIDAI plan more effectively, allocate resources efficiently, and ensure that Aadhaar services reach all citizens in Maharashtra. Continued analysis and monitoring will support the ongoing success of the Aadhaar program.",
        styles['BodyParagraph']
    ))
    
    elements.append(Spacer(1, 1*inch))
    
    # End of report
    elements.append(HRFlowable(width="30%", thickness=1, color=DARK_BLUE, hAlign='CENTER'))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph(
        "End of Report",
        ParagraphStyle('EndNote', fontSize=10, alignment=TA_CENTER, textColor=colors.gray)
    ))
    
    return elements


def generate_academic_report():
    """Generate the complete academic PDF report."""
    print("Creating academic report...")
    
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
    
    # Build document sections
    elements.extend(create_cover_page(styles))
    elements.extend(create_introduction(styles))
    elements.extend(create_dataset_description(styles))
    elements.extend(create_methodology(styles))
    elements.extend(create_key_findings(styles))
    elements.extend(create_policy_insights(styles))
    elements.extend(create_conclusion(styles))
    
    # Build PDF
    doc.build(elements, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    
    print(f"Academic report generated successfully at {OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == '__main__':
    generate_academic_report()
