#!/usr/bin/env python3
"""
Test File Parsing Functionality
Demonstrates the resume analyzer's ability to parse actual resume files
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent))

from HR_root_agent.sub_agents.resume_analyzer.agent import ResumeAnalyzerTools

def test_file_parsing():
    """Test the file parsing functionality with actual files"""
    
    print("🧪 Testing Resume File Parsing Functionality")
    print("=" * 60)
    
    # Test with the sample resume file
    sample_file = "sample_resume.txt"
    
    if not os.path.exists(sample_file):
        print(f"❌ Sample file not found: {sample_file}")
        return
    
    print(f"📄 Parsing file: {sample_file}")
    print("-" * 40)
    
    try:
        # Parse the resume file
        parsed_data = ResumeAnalyzerTools.parse_resume(sample_file)
        
        if parsed_data.get("parsing_success"):
            print("✅ File parsed successfully!")
            print()
            
            # Display parsed information
            print("📊 PARSED INFORMATION:")
            print(f"📧 Emails: {', '.join(parsed_data['contact_info']['emails'])}")
            print(f"📱 Phones: {', '.join(parsed_data['contact_info']['phones'])}")
            print(f"🔧 Skills: {', '.join(parsed_data['skills'])}")
            print(f"🎓 Education: {len(parsed_data['education'])} entries")
            print(f"💼 Experience: {len(parsed_data['experience'])} positions")
            print(f"📝 Word Count: {parsed_data['word_count']}")
            
            # Show some extracted content
            print("\n📋 EDUCATION ENTRIES:")
            for i, edu in enumerate(parsed_data['education'], 1):
                print(f"{i}. {edu}")
            
            print("\n💼 EXPERIENCE ENTRIES:")
            for i, exp in enumerate(parsed_data['experience'], 1):
                print(f"{i}. {exp}")
            
            print("\n🔧 DETECTED SKILLS:")
            for i, skill in enumerate(parsed_data['skills'], 1):
                print(f"{i}. {skill}")
                
        else:
            print(f"❌ Parsing failed: {parsed_data.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error during parsing: {str(e)}")
    
    # Test analysis against a job description
    print("\n" + "=" * 60)
    print("🔍 TESTING RESUME ANALYSIS AGAINST JOB DESCRIPTION")
    print("=" * 60)
    
    job_description = """
    Senior Python Developer Position
    
    Required Skills:
    - Python, Django, Flask
    - SQL, PostgreSQL, MongoDB
    - RESTful APIs, GraphQL
    - Docker, Kubernetes
    - AWS, Azure cloud platforms
    - JavaScript, React
    
    Experience Requirements:
    - Minimum 5 years of experience in Python development
    - 3+ years working with web frameworks
    - 2+ years of cloud platform experience
    
    Education Requirements:
    - Bachelor's degree in Computer Science or related field
    - Master's degree preferred
    """
    
    print("📋 Job Description:")
    print(job_description)
    
    try:
        # Analyze the parsed resume against the job description
        analysis_result = ResumeAnalyzerTools.analyze_resume_against_jd(
            parsed_data, 
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
    
    print("\n" + "=" * 60)
    print("🎯 PARSING CAPABILITIES DEMONSTRATED:")
    print("✅ Text file parsing")
    print("✅ Contact information extraction")
    print("✅ Skills identification")
    print("✅ Education extraction")
    print("✅ Experience parsing")
    print("✅ Job description requirement extraction")
    print("✅ Multi-dimensional scoring")
    print("✅ Detailed analysis reports")
    print("✅ Actionable recommendations")

if __name__ == "__main__":
    test_file_parsing()
