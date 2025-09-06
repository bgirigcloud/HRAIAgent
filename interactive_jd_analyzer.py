#!/usr/bin/env python3
"""
Interactive Job Description Analyzer
This script allows you to input your own job description for analysis
"""

import os
import sys
from pathlib import Path
import re

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent))

def get_user_job_description():
    """Get job description input from user"""
    
    print("📋 Interactive Job Description Analyzer")
    print("=" * 60)
    print("Please paste your job description below.")
    print("When you're done, type 'END' on a new line and press Enter.\n")
    
    lines = []
    while True:
        line = input()
        if line.strip().upper() == 'END':
            break
        lines.append(line)
    
    return '\n'.join(lines)

def smart_extract_jd_components(job_description):
    """Extract components using pattern matching and keywords"""
    
    jd_text = job_description.lower()
    
    # Extract position title
    position = extract_position_title(job_description)
    
    # Extract experience requirements
    experience = extract_experience_requirements(jd_text)
    
    # Extract salary information
    salary = extract_salary_info(jd_text)
    
    # Extract skills
    required_skills, preferred_skills = extract_skills(jd_text)
    
    # Extract education requirements
    education = extract_education_requirements(jd_text)
    
    # Extract location information
    location = extract_location_info(jd_text)
    
    return {
        'position': position,
        'experience_required': experience,
        'salary_range': salary,
        'required_skills': required_skills,
        'preferred_skills': preferred_skills,
        'education_requirements': education,
        'location': location
    }

def extract_position_title(job_description):
    """Extract job position from the first few lines"""
    lines = job_description.split('\n')
    for line in lines[:5]:
        line = line.strip()
        if len(line) > 10 and len(line) < 100:
            # Skip lines that look like company names or headers
            if not any(word in line.lower() for word in ['about', 'company', 'we are', 'join']):
                return line
    return "Position not clearly specified"

def extract_experience_requirements(jd_text):
    """Extract experience requirements using regex patterns"""
    
    experience_patterns = [
        r'(\d+[\+\-]?\s*(?:to\s+\d+)?\s*years?\s+(?:of\s+)?experience)',
        r'(minimum\s+\d+\s+years?)',
        r'(\d+\+?\s*years?\s+(?:in|with|of))',
        r'(experience:\s*\d+[\+\-]?\s*years?)'
    ]
    
    experiences = []
    for pattern in experience_patterns:
        matches = re.findall(pattern, jd_text, re.IGNORECASE)
        experiences.extend(matches)
    
    return list(set(experiences)) if experiences else ["Experience requirements not specified"]

def extract_salary_info(jd_text):
    """Extract salary information"""
    
    salary_patterns = [
        r'\$[\d,]+\s*(?:-|to)\s*\$?[\d,]+',
        r'salary[:\s]*\$?[\d,]+(?:\s*(?:-|to)\s*\$?[\d,]+)?',
        r'compensation[:\s]*\$?[\d,]+(?:\s*(?:-|to)\s*\$?[\d,]+)?'
    ]
    
    for pattern in salary_patterns:
        match = re.search(pattern, jd_text, re.IGNORECASE)
        if match:
            return match.group(0)
    
    return "Salary information not provided"

def extract_skills(jd_text):
    """Extract technical and soft skills"""
    
    # Common technical skills to look for
    tech_skills = [
        'python', 'java', 'javascript', 'react', 'angular', 'vue',
        'node.js', 'django', 'flask', 'spring', 'express',
        'sql', 'postgresql', 'mysql', 'mongodb', 'redis',
        'aws', 'azure', 'gcp', 'docker', 'kubernetes',
        'git', 'jira', 'jenkins', 'ci/cd', 'devops',
        'html', 'css', 'typescript', 'php', 'ruby',
        'c++', 'c#', '.net', 'scala', 'go', 'rust',
        'machine learning', 'ai', 'data science',
        'rest api', 'graphql', 'microservices'
    ]
    
    # Soft skills to look for
    soft_skills = [
        'communication', 'teamwork', 'leadership', 'problem solving',
        'analytical', 'creative', 'detail oriented', 'organized',
        'time management', 'adaptable', 'collaborative'
    ]
    
    found_tech_skills = []
    found_soft_skills = []
    
    for skill in tech_skills:
        if skill.lower() in jd_text:
            found_tech_skills.append(skill.title())
    
    for skill in soft_skills:
        if skill.lower() in jd_text:
            found_soft_skills.append(skill.title())
    
    # Try to separate required vs preferred
    required_section = ""
    preferred_section = ""
    
    # Look for sections that indicate requirements vs preferences
    if 'required' in jd_text and 'preferred' in jd_text:
        parts = jd_text.split('preferred')
        required_section = parts[0]
        preferred_section = parts[1] if len(parts) > 1 else ""
    elif 'required' in jd_text:
        required_section = jd_text
    else:
        required_section = jd_text  # Assume all are required if not specified
    
    required_skills = []
    preferred_skills = []
    
    for skill in found_tech_skills + found_soft_skills:
        if skill.lower() in required_section:
            required_skills.append(skill)
        elif skill.lower() in preferred_section:
            preferred_skills.append(skill)
        else:
            required_skills.append(skill)  # Default to required
    
    return list(set(required_skills)), list(set(preferred_skills))

def extract_education_requirements(jd_text):
    """Extract education requirements"""
    
    education_patterns = [
        r'bachelor[\'s]*\s+degree',
        r'master[\'s]*\s+degree',
        r'phd|doctorate',
        r'high school|diploma',
        r'associate[\'s]*\s+degree',
        r'computer science|engineering|mathematics|it'
    ]
    
    education_reqs = []
    for pattern in education_patterns:
        matches = re.findall(pattern, jd_text, re.IGNORECASE)
        education_reqs.extend(matches)
    
    return list(set(education_reqs)) if education_reqs else ["Education requirements not specified"]

def extract_location_info(jd_text):
    """Extract location information"""
    
    location_keywords = ['remote', 'hybrid', 'on-site', 'onsite', 'location', 'city', 'state']
    
    for keyword in location_keywords:
        if keyword in jd_text:
            # Try to extract the line containing location info
            lines = jd_text.split('\n')
            for line in lines:
                if keyword in line.lower():
                    return line.strip()
    
    return "Location not specified"

def analyze_jd_complexity(jd_analysis):
    """Analyze the complexity and clarity of the job description"""
    
    complexity_score = 0
    feedback = []
    
    # Check if position is clearly defined
    if "not clearly specified" in jd_analysis['position']:
        feedback.append("❌ Position title is unclear")
    else:
        complexity_score += 20
        feedback.append("✅ Position title is clear")
    
    # Check skill requirements
    total_skills = len(jd_analysis['required_skills']) + len(jd_analysis['preferred_skills'])
    if total_skills > 15:
        feedback.append("⚠️ Too many skill requirements may limit candidate pool")
    elif total_skills > 8:
        complexity_score += 20
        feedback.append("✅ Good balance of skill requirements")
    else:
        feedback.append("⚠️ Consider adding more specific skill requirements")
    
    # Check experience requirements
    if "not specified" in str(jd_analysis['experience_required']):
        feedback.append("❌ Experience requirements are unclear")
    else:
        complexity_score += 20
        feedback.append("✅ Experience requirements are specified")
    
    # Check salary information
    if "not provided" in jd_analysis['salary_range']:
        feedback.append("⚠️ Consider adding salary range for better response rate")
    else:
        complexity_score += 20
        feedback.append("✅ Salary information provided")
    
    # Check location clarity
    if "not specified" in jd_analysis['location']:
        feedback.append("⚠️ Location/remote work policy is unclear")
    else:
        complexity_score += 20
        feedback.append("✅ Location information is clear")
    
    return complexity_score, feedback

def main():
    """Main function to run the interactive analyzer"""
    
    # Get job description from user
    job_description = get_user_job_description()
    
    if not job_description.strip():
        print("❌ No job description provided. Please try again.")
        return
    
    print("\n🔍 Analyzing your job description...")
    print("=" * 60)
    
    # Extract components
    jd_analysis = smart_extract_jd_components(job_description)
    
    # Display results
    print("\n1️⃣ EXTRACTED INFORMATION")
    print("-" * 50)
    print(f"📌 Position: {jd_analysis['position']}")
    print(f"📅 Experience: {', '.join(jd_analysis['experience_required'])}")
    print(f"💰 Salary: {jd_analysis['salary_range']}")
    print(f"📍 Location: {jd_analysis['location']}")
    
    print("\n2️⃣ SKILLS ANALYSIS")
    print("-" * 50)
    print(f"🔧 Required Skills ({len(jd_analysis['required_skills'])}):")
    for skill in jd_analysis['required_skills']:
        print(f"   • {skill}")
    
    if jd_analysis['preferred_skills']:
        print(f"\n🎯 Preferred Skills ({len(jd_analysis['preferred_skills'])}):")
        for skill in jd_analysis['preferred_skills']:
            print(f"   • {skill}")
    
    print(f"\n📚 Education: {', '.join(jd_analysis['education_requirements'])}")
    
    # Analyze complexity and provide feedback
    print("\n3️⃣ JOB DESCRIPTION QUALITY ANALYSIS")
    print("-" * 50)
    
    complexity_score, feedback = analyze_jd_complexity(jd_analysis)
    
    print(f"📊 Overall Quality Score: {complexity_score}/100")
    print("\n💡 Feedback:")
    for item in feedback:
        print(f"   {item}")
    
    print("\n4️⃣ RECOMMENDATIONS")
    print("-" * 50)
    
    if complexity_score < 60:
        print("🔴 Priority Improvements Needed:")
        print("   • Clarify position title and responsibilities")
        print("   • Add specific skill requirements")
        print("   • Include experience requirements")
        print("   • Consider adding salary range")
    elif complexity_score < 80:
        print("🟡 Good Foundation - Minor Improvements:")
        print("   • Consider adding more specific requirements")
        print("   • Review skill list for balance")
        print("   • Clarify location/remote work policy")
    else:
        print("🟢 Excellent Job Description!")
        print("   • Well-structured and comprehensive")
        print("   • Clear requirements and expectations")
        print("   • Ready for posting and candidate sourcing")
    
    print("\n" + "=" * 60)
    print("📈 ANALYSIS COMPLETE!")
    print("Thank you for using the Job Description Analyzer!")

if __name__ == "__main__":
    main()


