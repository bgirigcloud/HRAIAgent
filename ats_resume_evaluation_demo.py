#!/usr/bin/env python3
"""
ATS Resume Evaluation Demo
Demonstrates the complete ATS workflow with resume evaluation
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent))

from HR_root_agent.sub_agents.ats_tool.agent import ATSTools
from HR_root_agent.sub_agents.resume_analyzer.agent import ResumeAnalyzerTools

def demonstrate_ats_workflow():
    """Demonstrate the complete ATS workflow"""
    
    print("🏢 ATS Resume Evaluation Workflow Demo")
    print("=" * 70)
    
    # Step 1: Create a job posting
    print("1️⃣ STEP 1: Create Job Posting")
    print("-" * 50)
    
    job_title = "Senior Full-Stack Developer"
    job_description = """
    We are seeking a Senior Full-Stack Developer to join our growing team.
    
    Responsibilities:
    - Develop and maintain web applications
    - Design and implement database schemas
    - Deploy applications to cloud platforms
    - Mentor junior developers
    - Participate in code reviews
    """
    
    job_requirements = {
        "skills": ["python", "javascript", "react", "node.js", "django", "flask", "sql", "aws", "docker"],
        "experience_years": 4,
        "education_level": "bachelor",
        "location": "Remote",
        "employment_type": "Full-time"
    }
    
    # Create job posting in ATS
    job_result = ATSTools.create_job_posting(job_title, job_description, job_requirements)
    
    if job_result.get("success"):
        job_id = job_result["job_id"]
        print(f"✅ Job posting created successfully!")
        print(f"📋 Job ID: {job_id}")
        print(f"📝 Title: {job_title}")
        print(f"🔧 Required Skills: {', '.join(job_requirements['skills'])}")
        print(f"💼 Experience: {job_requirements['experience_years']}+ years")
        print(f"🎓 Education: {job_requirements['education_level'].title()} degree")
    else:
        print(f"❌ Failed to create job posting: {job_result.get('error')}")
        return
    
    # Step 2: Submit candidate resumes
    print("\n2️⃣ STEP 2: Submit Candidate Resumes")
    print("-" * 50)
    
    candidates = [
        {
            "name": "John Doe",
            "email": "john.doe@email.com",
            "phone": "+1-555-123-4567",
            "resume_file": "sample_resume.txt"
        },
        {
            "name": "Jane Smith",
            "email": "jane.smith@email.com",
            "phone": "+1-555-987-6543",
            "resume_file": "sample_resume.txt"  # Using same file for demo
        }
    ]
    
    candidate_ids = []
    
    for i, candidate_info in enumerate(candidates, 1):
        print(f"\n📄 Submitting resume for {candidate_info['name']}...")
        
        personal_info = {
            "name": candidate_info["name"],
            "email": candidate_info["email"],
            "phone": candidate_info["phone"]
        }
        
        # Submit resume to ATS
        submission_result = ATSTools.submit_resume(
            job_id, 
            {"personal_info": personal_info}, 
            candidate_info["resume_file"]
        )
        
        if submission_result.get("success"):
            candidate_id = submission_result["candidate_id"]
            candidate_ids.append(candidate_id)
            print(f"✅ Resume submitted successfully!")
            print(f"🆔 Candidate ID: {candidate_id}")
            print(f"📧 Email: {candidate_info['email']}")
        else:
            print(f"❌ Failed to submit resume: {submission_result.get('error')}")
    
    if not candidate_ids:
        print("❌ No candidates submitted successfully")
        return
    
    # Step 3: Parse and evaluate resumes
    print("\n3️⃣ STEP 3: Parse and Evaluate Resumes")
    print("-" * 50)
    
    for candidate_id in candidate_ids:
        print(f"\n🔍 Evaluating resume for candidate: {candidate_id}")
        
        # Get candidate info
        candidate_status = ATSTools.get_candidate_status(candidate_id)
        if not candidate_status.get("success"):
            print(f"❌ Failed to get candidate status: {candidate_status.get('error')}")
            continue
        
        candidate = candidate_status["candidate"]
        resume_file = candidate.get("resume_file")
        
        if resume_file and os.path.exists(resume_file):
            # Parse resume using ResumeAnalyzerTools
            print(f"📄 Parsing resume file: {resume_file}")
            parsed_resume = ResumeAnalyzerTools.parse_resume(resume_file)
            
            if parsed_resume.get("parsing_success"):
                print("✅ Resume parsed successfully")
                print(f"🔧 Skills detected: {', '.join(parsed_resume['skills'][:5])}...")
                print(f"💼 Experience: {parsed_resume.get('total_years_experience', 0)} years")
                print(f"🎓 Education entries: {len(parsed_resume['education'])}")
                
                # Evaluate resume using ATS
                print("📊 Evaluating resume against job requirements...")
                evaluation_result = ATSTools.evaluate_resume(candidate_id, parsed_resume)
                
                if evaluation_result.get("success"):
                    evaluation = evaluation_result["evaluation"]
                    print("✅ Resume evaluation complete!")
                    print(f"📊 Overall Score: {evaluation['overall_score']}/100")
                    print(f"🔧 Skills Score: {evaluation['skill_score']}/100")
                    print(f"💼 Experience Score: {evaluation['experience_score']}/100")
                    print(f"🎓 Education Score: {evaluation['education_score']}/100")
                    print(f"📋 Status: {evaluation_result['candidate_status']}")
                    
                    # Show recommendations
                    if evaluation.get('recommendations'):
                        print("💡 Recommendations:")
                        for rec in evaluation['recommendations']:
                            print(f"   • {rec}")
                else:
                    print(f"❌ Evaluation failed: {evaluation_result.get('error')}")
            else:
                print(f"❌ Resume parsing failed: {parsed_resume.get('error')}")
        else:
            print(f"❌ Resume file not found: {resume_file}")
    
    # Step 4: Review applications and schedule interviews
    print("\n4️⃣ STEP 4: Review Applications and Schedule Interviews")
    print("-" * 50)
    
    # Get all applications for the job
    applications_result = ATSTools.get_job_applications(job_id)
    
    if applications_result.get("success"):
        applications = applications_result["applications"]
        print(f"📋 Total Applications: {applications_result['total_applications']}")
        print(f"📝 Job Title: {applications_result['job_title']}")
        
        print("\n👥 Candidate Applications:")
        for app in applications:
            candidate_id = app["candidate_id"]
            status = app["status"]
            evaluation = app.get("evaluation", {})
            score = evaluation.get("overall_score", "N/A") if evaluation else "N/A"
            
            print(f"   • {candidate_id}: Status={status}, Score={score}")
            
            # Schedule interview for qualified candidates
            if status == "qualified":
                print(f"     🎯 Scheduling interview for qualified candidate...")
                
                # Schedule interview (tomorrow for demo)
                from datetime import datetime, timedelta
                tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
                
                interview_result = ATSTools.schedule_interview(
                    candidate_id, 
                    tomorrow, 
                    "phone"
                )
                
                if interview_result.get("success"):
                    print(f"     ✅ Interview scheduled for {tomorrow}")
                else:
                    print(f"     ❌ Failed to schedule interview: {interview_result.get('error')}")
    else:
        print(f"❌ Failed to get applications: {applications_result.get('error')}")
    
    # Step 5: ATS Dashboard Overview
    print("\n5️⃣ STEP 5: ATS Dashboard Overview")
    print("-" * 50)
    
    dashboard_result = ATSTools.get_ats_dashboard()
    
    if dashboard_result.get("success"):
        dashboard = dashboard_result["dashboard"]
        
        print("📊 ATS Dashboard:")
        print(f"   📋 Total Job Postings: {dashboard['total_job_postings']}")
        print(f"   👥 Total Candidates: {dashboard['total_candidates']}")
        print(f"   📊 Total Evaluations: {dashboard['total_evaluations']}")
        print(f"   📅 Total Interviews: {dashboard['total_interviews']}")
        
        print(f"\n📈 Candidate Status Breakdown:")
        for status, count in dashboard['candidate_status_breakdown'].items():
            print(f"   • {status.title()}: {count}")
        
        print(f"\n🔄 Recent Activity:")
        for activity in dashboard['recent_activity'][:5]:
            print(f"   • {activity['description']} ({activity['date'][:10]})")
    else:
        print(f"❌ Failed to get dashboard: {dashboard_result.get('error')}")
    
    print("\n" + "=" * 70)
    print("🎯 ATS WORKFLOW COMPLETED SUCCESSFULLY!")
    print("✅ Job posting created")
    print("✅ Candidate resumes submitted")
    print("✅ Resumes parsed and evaluated")
    print("✅ Applications reviewed")
    print("✅ Interviews scheduled for qualified candidates")
    print("✅ Dashboard analytics generated")

def show_ats_capabilities():
    """Show the ATS tool capabilities"""
    
    print("\n🤖 ATS Tool Capabilities")
    print("=" * 70)
    
    print("📋 JOB MANAGEMENT:")
    print("   - Create and manage job postings")
    print("   - Define job requirements and evaluation criteria")
    print("   - Track job status and applications")
    
    print("\n👥 CANDIDATE MANAGEMENT:")
    print("   - Process resume submissions")
    print("   - Track candidate status and progress")
    print("   - Manage candidate profiles and information")
    
    print("\n📊 RESUME EVALUATION:")
    print("   - Automated resume parsing and analysis")
    print("   - Multi-dimensional scoring (skills, experience, education)")
    print("   - Intelligent requirement matching")
    print("   - Automated recommendations")
    
    print("\n📅 INTERVIEW MANAGEMENT:")
    print("   - Schedule interviews for qualified candidates")
    print("   - Track interview status and outcomes")
    print("   - Manage interview pipeline")
    
    print("\n📈 ANALYTICS & REPORTING:")
    print("   - ATS dashboard with key metrics")
    print("   - Candidate status breakdown")
    print("   - Recent activity tracking")
    print("   - Performance analytics")
    
    print("\n🔗 INTEGRATION FEATURES:")
    print("   - Seamless integration with Resume Analyzer")
    print("   - HR system workflow coordination")
    print("   - Automated candidate evaluation")
    print("   - Data-driven hiring decisions")

if __name__ == "__main__":
    demonstrate_ats_workflow()
    show_ats_capabilities()
