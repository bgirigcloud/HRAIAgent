#!/usr/bin/env python3
"""
Resume Analysis Example Script
Demonstrates how to use the Resume Analyzer Agent to analyze resumes against job descriptions
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent))

from HR_root_agent.sub_agents.resume_analyzer.agent import ResumeAnalyzerTools

def main():
    """Main function to demonstrate resume analysis"""
    
    print("🚀 Resume Analyzer Agent Demo")
    print("=" * 50)
    
    # Example job description
    job_description = """
    Senior Python Developer
    
    We are looking for a Senior Python Developer to join our team.
    
    Required Skills:
    - Python, Django, Flask
    - SQL, PostgreSQL, MongoDB
    - RESTful APIs, GraphQL
    - Docker, Kubernetes
    - AWS, Azure cloud platforms
    
    Experience Requirements:
    - Minimum 5 years of experience in Python development
    - 3+ years working with web frameworks
    - 2+ years of cloud platform experience
    
    Education Requirements:
    - Bachelor's degree in Computer Science or related field
    - Master's degree preferred
    
    Responsibilities:
    - Develop and maintain web applications
    - Design and implement database schemas
    - Deploy applications to cloud platforms
    - Mentor junior developers
    - Participate in code reviews
    """
    
    print("\n📋 Job Description:")
    print(job_description)
    
    # Example resume data (simulated parsed resume)
    example_resume_data = {
        "contact_info": {
            "emails": ["john.doe@email.com"],
            "phones": ["+1-555-123-4567"]
        },
        "skills": [
            "python", "django", "flask", "sql", "postgresql", 
            "mongodb", "restful apis", "docker", "aws", "azure"
        ],
        "education": [
            "Master's Degree in Computer Science - Stanford University (2020)",
            "Bachelor's Degree in Software Engineering - MIT (2018)"
        ],
        "experience": [
            "Senior Python Developer - Tech Corp (2020-2024) - 4 years",
            "Python Developer - Startup Inc (2018-2020) - 2 years"
        ],
        "raw_text": "John Doe - Senior Python Developer with 6 years of experience...",
        "word_count": 150,
        "parsing_success": True
        }
    
    print("\n📄 Resume Data (Simulated):")
    print(f"Skills: {', '.join(example_resume_data['skills'])}")
    print(f"Education: {len(example_resume_data['education'])} entries")
    print(f"Experience: {len(example_resume_data['experience'])} positions")
    
    # Analyze resume against job description
    print("\n🔍 Analyzing Resume Against Job Description...")
    
    try:
        analysis_result = ResumeAnalyzerTools.analyze_resume_against_jd(
            example_resume_data, 
            job_description
        )
        
        if analysis_result.get("analysis_success"):
            print("\n✅ Analysis Complete!")
            print("=" * 50)
            
            # Display scores
            print(f"📊 OVERALL SCORE: {analysis_result['overall_score']}/100")
            print(f"🔧 Skills Match: {analysis_result['skill_match_score']}/100")
            print(f"💼 Experience: {analysis_result['experience_score']}/100")
            print(f"🎓 Education: {analysis_result['education_score']}/100")
            
            # Display detailed analysis
            print("\n📋 DETAILED ANALYSIS:")
            print(analysis_result['detailed_analysis'])
            
            # Display recommendations
            print("\n💡 RECOMMENDATIONS:")
            for i, rec in enumerate(analysis_result['recommendations'], 1):
                print(f"{i}. {rec}")
                
        else:
            print(f"❌ Analysis failed: {analysis_result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
    
    # Demonstrate file parsing capability
    print("\n📁 File Parsing Capabilities:")
    print("The agent can parse resumes from:")
    print("- PDF files (.pdf)")
    print("- Word documents (.docx)")
    print("- Text files (.txt)")
    
    print("\n💡 Usage Instructions:")
    print("1. Use parse_resume_tool to extract information from resume files")
    print("2. Use analyze_resume_tool to compare resume data against job descriptions")
    print("3. Get comprehensive evaluation scores and recommendations")
    
    print("\n🎯 Key Features:")
    print("- 100% accurate evaluation based on content analysis")
    print("- Multi-dimensional scoring (skills, experience, education)")
    print("- Detailed analysis reports with actionable recommendations")
    print("- Support for multiple file formats")
    print("- Intelligent requirement extraction from job descriptions")

if __name__ == "__main__":
    main()
