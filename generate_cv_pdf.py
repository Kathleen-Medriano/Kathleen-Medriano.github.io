#!/usr/bin/env python3
"""
CV PDF Generator
Generates a PDF from the CV JSON data file.
"""

import json
import os
from datetime import datetime
from pathlib import Path

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
    from reportlab.lib.colors import black, darkblue, gray
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("Warning: reportlab not available. Install with: pip install reportlab")

def load_cv_data(json_path):
    """Load CV data from JSON file."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: CV data file not found at {json_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in CV data file: {e}")
        return None

def create_styles():
    """Create custom styles for the PDF."""
    styles = getSampleStyleSheet()
    
    # Custom styles
    styles.add(ParagraphStyle(
        name='CVTitle',
        parent=styles['Title'],
        fontSize=24,
        spaceAfter=12,
        alignment=TA_CENTER,
        textColor=darkblue
    ))
    
    styles.add(ParagraphStyle(
        name='CVSubtitle',
        parent=styles['Normal'],
        fontSize=14,
        spaceAfter=6,
        alignment=TA_CENTER,
        textColor=gray
    ))
    
    styles.add(ParagraphStyle(
        name='CVContact',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=12,
        alignment=TA_CENTER,
        textColor=black
    ))
    
    styles.add(ParagraphStyle(
        name='CVSectionHeader',
        parent=styles['Heading2'],
        fontSize=14,
        spaceBefore=18,
        spaceAfter=6,
        textColor=darkblue,
        borderWidth=1,
        borderColor=darkblue,
        borderPadding=3
    ))
    
    styles.add(ParagraphStyle(
        name='CVEntryTitle',
        parent=styles['Normal'],
        fontSize=12,
        spaceBefore=6,
        spaceAfter=2,
        textColor=black,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='CVEntryOrg',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=2,
        textColor=gray,
        fontName='Helvetica-Oblique'
    ))
    
    styles.add(ParagraphStyle(
        name='CVEntryDate',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=2,
        textColor=gray,
        alignment=TA_RIGHT
    ))
    
    styles.add(ParagraphStyle(
        name='CVEntryDesc',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        textColor=black,
        leftIndent=0.2*inch
    ))
    
    return styles

def format_date_range(start_date, end_date):
    """Format date range for display."""
    if start_date and end_date:
        return f"{start_date} - {end_date}"
    elif start_date:
        return f"{start_date} - Present"
    elif end_date:
        return end_date
    else:
        return ""

def generate_pdf(cv_data, output_path):
    """Generate PDF from CV data."""
    if not REPORTLAB_AVAILABLE:
        print("Error: reportlab library is required for PDF generation.")
        print("Install with: pip install reportlab")
        return False
    
    if not cv_data:
        print("Error: No CV data provided")
        return False
    
    # Create document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    # Get styles
    styles = create_styles()
    story = []
    
    # Basic information
    basics = cv_data.get('basics', {})
    
    # Name and title
    if basics.get('name'):
        story.append(Paragraph(basics['name'], styles['CVTitle']))
    
    if basics.get('label'):
        story.append(Paragraph(basics['label'], styles['CVSubtitle']))
    
    # Contact information
    contact_info = []
    if basics.get('email'):
        contact_info.append(f"Email: {basics['email']}")
    if basics.get('phone'):
        contact_info.append(f"Phone: {basics['phone']}")
    if basics.get('website'):
        contact_info.append(f"Website: {basics['website']}")
    
    location = basics.get('location', {})
    location_parts = []
    if location.get('city'):
        location_parts.append(location['city'])
    if location.get('region'):
        location_parts.append(location['region'])
    if location.get('countryCode'):
        location_parts.append(location['countryCode'])
    if location_parts:
        contact_info.append(f"Location: {', '.join(location_parts)}")
    
    if contact_info:
        story.append(Paragraph(' | '.join(contact_info), styles['CVContact']))
    
    story.append(Spacer(1, 12))
    
    # Summary
    if basics.get('summary'):
        story.append(Paragraph('Summary', styles['CVSectionHeader']))
        story.append(Paragraph(basics['summary'], styles['Normal']))
        story.append(Spacer(1, 12))
    
    # Education
    education = cv_data.get('education', [])
    if education:
        story.append(Paragraph('Education', styles['CVSectionHeader']))
        for edu in education:
            title_parts = []
            if edu.get('area'):
                title_parts.append(edu['area'])
            if edu.get('studyType'):
                title_parts.append(edu['studyType'])
            
            if title_parts:
                story.append(Paragraph(', '.join(title_parts), styles['CVEntryTitle']))
            
            if edu.get('institution'):
                story.append(Paragraph(edu['institution'], styles['CVEntryOrg']))
            
            date_range = format_date_range(edu.get('startDate'), edu.get('endDate'))
            if date_range:
                story.append(Paragraph(date_range, styles['CVEntryDate']))
            
            if edu.get('gpa'):
                story.append(Paragraph(f"GPA: {edu['gpa']}", styles['CVEntryDesc']))
            
            if edu.get('courses'):
                courses_text = f"Relevant Coursework: {', '.join(edu['courses'])}"
                story.append(Paragraph(courses_text, styles['CVEntryDesc']))
        
        story.append(Spacer(1, 12))
    
    # Work Experience
    work = cv_data.get('work', [])
    if work:
        story.append(Paragraph('Work Experience', styles['CVSectionHeader']))
        for job in work:
            if job.get('position'):
                story.append(Paragraph(job['position'], styles['CVEntryTitle']))
            
            org_parts = []
            if job.get('company'):
                org_parts.append(job['company'])
            if job.get('location'):
                org_parts.append(job['location'])
            
            if org_parts:
                story.append(Paragraph(', '.join(org_parts), styles['CVEntryOrg']))
            
            date_range = format_date_range(job.get('startDate'), job.get('endDate'))
            if date_range:
                story.append(Paragraph(date_range, styles['CVEntryDate']))
            
            if job.get('summary'):
                story.append(Paragraph(job['summary'], styles['CVEntryDesc']))
            
            if job.get('highlights'):
                for highlight in job['highlights']:
                    story.append(Paragraph(f"• {highlight}", styles['CVEntryDesc']))
        
        story.append(Spacer(1, 12))
    
    # Skills
    skills = cv_data.get('skills', [])
    if skills:
        story.append(Paragraph('Skills', styles['CVSectionHeader']))
        for skill in skills:
            skill_text = skill.get('name', '')
            if skill.get('level'):
                skill_text += f" ({skill['level']})"
            if skill_text:
                story.append(Paragraph(skill_text, styles['CVEntryTitle']))
            
            if skill.get('keywords'):
                keywords_text = ', '.join(skill['keywords'])
                story.append(Paragraph(keywords_text, styles['CVEntryDesc']))
        
        story.append(Spacer(1, 12))
    
    # Awards
    awards = cv_data.get('awards', [])
    if awards:
        story.append(Paragraph('Awards & Honors', styles['CVSectionHeader']))
        for award in awards:
            if award.get('title'):
                story.append(Paragraph(award['title'], styles['CVEntryTitle']))
            
            if award.get('awarder'):
                story.append(Paragraph(award['awarder'], styles['CVEntryOrg']))
            
            if award.get('date'):
                story.append(Paragraph(award['date'], styles['CVEntryDate']))
            
            if award.get('summary'):
                story.append(Paragraph(award['summary'], styles['CVEntryDesc']))
        
        story.append(Spacer(1, 12))
    
    # Publications
    publications = cv_data.get('publications', [])
    if publications:
        story.append(Paragraph('Publications', styles['CVSectionHeader']))
        for pub in publications:
            if pub.get('name'):
                story.append(Paragraph(pub['name'], styles['CVEntryTitle']))
            
            pub_info = []
            if pub.get('publisher'):
                pub_info.append(pub['publisher'])
            if pub.get('releaseDate'):
                pub_info.append(pub['releaseDate'])
            
            if pub_info:
                story.append(Paragraph(', '.join(pub_info), styles['CVEntryOrg']))
            
            if pub.get('summary'):
                story.append(Paragraph(pub['summary'], styles['CVEntryDesc']))
        
        story.append(Spacer(1, 12))
    
    # Projects
    projects = cv_data.get('projects', [])
    if projects:
        story.append(Paragraph('Projects', styles['CVSectionHeader']))
        for project in projects:
            if project.get('name'):
                story.append(Paragraph(project['name'], styles['CVEntryTitle']))
            
            date_range = format_date_range(project.get('startDate'), project.get('endDate'))
            if date_range:
                story.append(Paragraph(date_range, styles['CVEntryDate']))
            
            if project.get('description'):
                story.append(Paragraph(project['description'], styles['CVEntryDesc']))
            
            if project.get('highlights'):
                for highlight in project['highlights']:
                    story.append(Paragraph(f"• {highlight}", styles['CVEntryDesc']))
        
        story.append(Spacer(1, 12))
    
    # Languages
    languages = cv_data.get('languages', [])
    if languages:
        story.append(Paragraph('Languages', styles['CVSectionHeader']))
        for lang in languages:
            lang_text = lang.get('language', '')
            if lang.get('fluency'):
                lang_text += f" ({lang['fluency']})"
            if lang_text:
                story.append(Paragraph(lang_text, styles['CVEntryTitle']))
        
        story.append(Spacer(1, 12))
    
    # Online Profiles
    profiles = basics.get('profiles', [])
    if profiles:
        story.append(Paragraph('Online Profiles', styles['CVSectionHeader']))
        for profile in profiles:
            if profile.get('network') and profile.get('url'):
                profile_text = f"{profile['network']}: {profile['url']}"
                story.append(Paragraph(profile_text, styles['CVEntryDesc']))
    
    # Build PDF
    try:
        doc.build(story)
        return True
    except Exception as e:
        print(f"Error building PDF: {e}")
        return False

def main():
    """Main function to generate CV PDF."""
    # Determine script directory
    script_dir = Path(__file__).parent
    
    # Paths
    cv_json_path = script_dir / '_data' / 'cv.json'
    output_path = script_dir / 'files' / 'cv.pdf'
    
    # Ensure output directory exists
    output_path.parent.mkdir(exist_ok=True)
    
    print("Loading CV data...")
    cv_data = load_cv_data(cv_json_path)
    
    if not cv_data:
        return 1
    
    print(f"Generating PDF: {output_path}")
    success = generate_pdf(cv_data, str(output_path))
    
    if success:
        print(f"✓ PDF generated successfully: {output_path}")
        print(f"File size: {output_path.stat().st_size} bytes")
        return 0
    else:
        print("✗ Failed to generate PDF")
        return 1

if __name__ == '__main__':
    exit(main())