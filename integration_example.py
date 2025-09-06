#!/usr/bin/env python3
"""
HR System Integration Example
Shows how to integrate the Resume Analyzer Agent with the HR system
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent))

from HR_root_agent.sub_agents.resume_analyzer.agent import ResumeAnalyzerTools, resume_analyzer_agent

def demonstrate_hr_integration():
    """Demonstrate how the resume analyzer integrates with the HR system"""
    
    print("🏢 HR System Integration Demo")
    print("=" * 60)
    
    # Simulate HR workflow
    print("1️⃣ STEP 1: Job Description Creation")
    print("-" * 40)
    
    job_description = """
    Senior Full-Stack Developer
    
    We are seeking a Senior Full-Stack Developer to join our growing team.
    
    Required Skills:
    - Python, JavaScript, React, Node.js
    - Django, Flask, Express.js
    - SQL, PostgreSQL, MongoDB
    - AWS, Docker, Git
    - RESTful APIs, GraphQL
    
    Experience Requirements:
    - Minimum 4 years of full-stack development experience
    - 2+ years working with Python and JavaScript
    - 1+ years of cloud platform experience
    
    Education Requirements:
    - Bachelor's degree in Computer Science or related field
    - Master's degree preferred
    """
    
    print("✅ Job Description created")
    print(f"📝 Skills Required: Python, JavaScript, React, Node.js, Django, Flask")
    print(f"💼 Experience: 4+ years")
    print(f"🎓 Education: Bachelor's degree preferred")
    
    print("\n2️⃣ STEP 2: Resume Submission and Parsing")
    print("-" * 40)
    
    # Parse a resume
    resume_file = "sample_resume.txt"
    if os.path.exists(resume_file):
        parsed_resume = ResumeAnalyzerTools.parse_resume(resume_file)
        
        if parsed_resume.get("parsing_success"):
            print("✅ Resume parsed successfully")
            print(f"📧 Contact: {', '.join(parsed_resume['contact_info']['emails'])}")
            print(f"🔧 Skills: {', '.join(parsed_resume['skills'][:5])}...")
            print(f"💼 Experience: {len(parsed_resume['experience'])} positions")
            print(f"🎓 Education: {len(parsed_resume['education'])} entries")
        else:
            print(f"❌ Resume parsing failed: {parsed_resume.get('error')}")
            return
    else:
        print(f"❌ Resume file not found: {resume_file}")
        return
    
    print("\n3️⃣ STEP 3: Automated Resume Analysis")
    print("-" * 40)
    
    # Analyze resume against job description
    analysis_result = ResumeAnalyzerTools.analyze_resume_against_jd(
        parsed_resume, 
        job_description
    )
    
    if analysis_result.get("analysis_success"):
        print("✅ Automated analysis complete")
        print(f"📊 Overall Score: {analysis_result['overall_score']}/100")
        print(f"🔧 Skills Match: {analysis_result['skill_match_score']}/100")
        print(f"💼 Experience: {analysis_result['experience_score']}/100")
        print(f"🎓 Education: {analysis_result['education_score']}/100")
        
        # Get recommendation
        recommendation = analysis_result['recommendations'][0] if analysis_result['recommendations'] else "No recommendation"
        print(f"💡 Recommendation: {recommendation}")
        
    else:
        print(f"❌ Analysis failed: {analysis_result.get('error')}")
        return
    
    print("\n4️⃣ STEP 4: HR Decision Support")
    print("-" * 40)
    
    # Simulate HR decision making
    overall_score = analysis_result['overall_score']
    
    if overall_score >= 80:
        print("🎯 DECISION: Strong Candidate - Schedule Interview")
        print("   - High skill match and experience")
        print("   - Meets all major requirements")
        print("   - Recommend for technical interview")
        
    elif overall_score >= 60:
        print("🎯 DECISION: Good Candidate - Consider for Interview")
        print("   - Meets most requirements")
        print("   - Some areas for improvement")
        print("   - Consider for interview with reservations")
        
    elif overall_score >= 40:
        print("🎯 DECISION: Consider with Reservations")
        print("   - Partial match to requirements")
        print("   - May need additional training")
        print("   - Consider for junior position or future roles")
        
    else:
        print("🎯 DECISION: Not Recommended")
        print("   - Low match to requirements")
        print("   - Significant gaps in skills/experience")
        print("   - Consider for other positions or future applications")
    
    print("\n5️⃣ STEP 5: Next Steps")
    print("-" * 40)
    
    print("📋 Automated Actions:")
    print("   - Resume data stored in HR database")
    print("   - Analysis report generated and saved")
    print("   - Candidate profile created")
    
    print("\n🤝 Manual Actions Required:")
    print("   - Review analysis results")
    print("   - Schedule interviews if recommended")
    print("   - Send follow-up communications")
    print("   - Update candidate status in ATS")
    
    print("\n" + "=" * 60)
    print("🎯 INTEGRATION BENEFITS:")
    print("✅ Automated resume screening")
    print("✅ Consistent evaluation criteria")
    print("✅ Time-saving for HR team")
    print("✅ Data-driven decision making")
    print("✅ Improved candidate experience")
    print("✅ Better hiring outcomes")

def show_agent_capabilities():
    """Show the resume analyzer agent capabilities"""
    
    print("\n🤖 Resume Analyzer Agent Capabilities")
    print("=" * 60)
    
    print("📊 PARSING CAPABILITIES:")
    print("   - PDF files (.pdf)")
    print("   - Word documents (.docx)")
    print("   - Text files (.txt)")
    
    print("\n🔍 ANALYSIS FEATURES:")
    print("   - Skills extraction and matching")
    print("   - Experience evaluation")
    print("   - Education assessment")
    print("   - Contact information extraction")
    
    print("\n📈 SCORING SYSTEM:")
    print("   - Overall fit score (0-100)")
    print("   - Skills match score (0-100)")
    print("   - Experience score (0-100)")
    print("   - Education score (0-100)")
    
    print("\n💡 INTELLIGENT FEATURES:")
    print("   - Pattern-based requirement extraction")
    print("   - Fuzzy skill matching")
    print("   - Experience duration calculation")
    print("   - Automated recommendations")

if __name__ == "__main__":
    demonstrate_hr_integration()
    show_agent_capabilities()
