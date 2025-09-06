"""
ATS (Applicant Tracking System) Tool Agent
Provides comprehensive hiring workflow management and candidate evaluation
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from google.adk.agents import Agent


class ATSTools:
    """
    ATS Tools for managing job postings, candidates, and hiring workflow
    """
    
    # In-memory storage for demo purposes
    jobs = {}
    candidates = {}
    evaluations = {}
    interviews = {}
    activities = []
    
    @staticmethod
    def create_job_posting(title: str, description: str, requirements: dict) -> dict:
        """Create a new job posting"""
        try:
            job_id = f"job_{len(ATSTools.jobs) + 1}_{datetime.now().strftime('%Y%m%d')}"
            
            job_data = {
                "job_id": job_id,
                "title": title,
                "description": description,
                "requirements": requirements,
                "status": "active",
                "created_date": datetime.now().isoformat(),
                "applications": []
            }
            
            ATSTools.jobs[job_id] = job_data
            ATSTools._log_activity(f"Created job posting: {title}", job_id)
            
            return {
                "success": True,
                "job_id": job_id,
                "message": f"Job posting '{title}' created successfully"
            }
            
        except Exception as e:
            return {"success": False, "error": f"Failed to create job posting: {str(e)}"}
    
    @staticmethod
    def submit_resume(job_id: str, candidate_info: dict, resume_file: str) -> dict:
        """Submit a resume for a job posting"""
        try:
            if job_id not in ATSTools.jobs:
                return {"success": False, "error": f"Job {job_id} not found"}
            
            candidate_id = f"candidate_{len(ATSTools.candidates) + 1}_{datetime.now().strftime('%Y%m%d')}"
            
            candidate_data = {
                "candidate_id": candidate_id,
                "job_id": job_id,
                "personal_info": candidate_info.get("personal_info", {}),
                "resume_file": resume_file,
                "status": "submitted",
                "submission_date": datetime.now().isoformat(),
                "evaluation": None
            }
            
            ATSTools.candidates[candidate_id] = candidate_data
            ATSTools.jobs[job_id]["applications"].append(candidate_id)
            
            name = candidate_info.get("personal_info", {}).get("name", "Unknown")
            ATSTools._log_activity(f"Resume submitted by {name}", candidate_id)
            
            return {
                "success": True,
                "candidate_id": candidate_id,
                "message": f"Resume submitted successfully for {name}"
            }
            
        except Exception as e:
            return {"success": False, "error": f"Failed to submit resume: {str(e)}"}
    
    @staticmethod
    def evaluate_resume(candidate_id: str, parsed_resume: dict) -> dict:
        """Evaluate a resume against job requirements"""
        try:
            if candidate_id not in ATSTools.candidates:
                return {"success": False, "error": f"Candidate {candidate_id} not found"}
            
            candidate = ATSTools.candidates[candidate_id]
            job_id = candidate["job_id"]
            
            if job_id not in ATSTools.jobs:
                return {"success": False, "error": f"Job {job_id} not found"}
            
            job = ATSTools.jobs[job_id]
            requirements = job["requirements"]
            
            # Calculate evaluation scores
            evaluation = ATSTools._calculate_scores(parsed_resume, requirements)
            
            # Determine qualification status
            overall_score = evaluation["overall_score"]
            if overall_score >= 80:
                status = "strong_candidate"
                qualification = "qualified"
            elif overall_score >= 60:
                status = "good_candidate"
                qualification = "qualified"
            else:
                status = "not_qualified"
                qualification = "not_qualified"
            
            # Store evaluation
            evaluation_data = {
                "candidate_id": candidate_id,
                "job_id": job_id,
                "evaluation": evaluation,
                "status": status,
                "qualification": qualification,
                "evaluation_date": datetime.now().isoformat()
            }
            
            ATSTools.evaluations[candidate_id] = evaluation_data
            ATSTools.candidates[candidate_id]["status"] = qualification
            ATSTools.candidates[candidate_id]["evaluation"] = evaluation
            
            name = candidate.get("personal_info", {}).get("name", "Unknown")
            ATSTools._log_activity(f"Evaluated resume for {name} - Score: {overall_score:.1f}", candidate_id)
            
            return {
                "success": True,
                "evaluation": evaluation,
                "candidate_status": qualification,
                "message": f"Resume evaluation completed - Score: {overall_score:.1f}/100"
            }
            
        except Exception as e:
            return {"success": False, "error": f"Failed to evaluate resume: {str(e)}"}
    
    @staticmethod
    def _calculate_scores(parsed_resume: dict, requirements: dict) -> dict:
        """Calculate evaluation scores based on requirements"""
        
        # Skills evaluation (40% weight)
        required_skills = [skill.lower() for skill in requirements.get("skills", [])]
        candidate_skills = [skill.lower() for skill in parsed_resume.get("skills", [])]
        
        skill_matches = sum(1 for skill in required_skills if any(skill in candidate_skill for candidate_skill in candidate_skills))
        skill_score = (skill_matches / len(required_skills) * 100) if required_skills else 0
        
        # Experience evaluation (40% weight)
        required_experience = requirements.get("experience_years", 0)
        candidate_experience = parsed_resume.get("total_years_experience", 0)
        
        if candidate_experience >= required_experience:
            experience_score = 100
        else:
            experience_score = (candidate_experience / required_experience * 100) if required_experience > 0 else 0
        
        # Education evaluation (20% weight)
        required_education = requirements.get("education_level", "").lower()
        candidate_education = parsed_resume.get("education", [])
        
        education_levels = {
            "high school": 1, "associate": 2, "bachelor": 3, "master": 4, "phd": 5, "doctorate": 5
        }
        
        required_level = education_levels.get(required_education, 0)
        candidate_level = 0
        for edu in candidate_education:
            degree = edu.get("degree", "").lower()
            for level_name, level_value in education_levels.items():
                if level_name in degree:
                    candidate_level = max(candidate_level, level_value)
        
        education_score = min(100, (candidate_level / required_level * 100)) if required_level > 0 else 100
        
        # Calculate overall score with weights
        overall_score = (skill_score * 0.4) + (experience_score * 0.4) + (education_score * 0.2)
        
        # Generate recommendations
        recommendations = []
        if skill_score < 70:
            missing_skills = [skill for skill in required_skills if not any(skill in candidate_skill for candidate_skill in candidate_skills)]
            if missing_skills:
                recommendations.append(f"Consider candidates with stronger background in: {', '.join(missing_skills[:3])}")
        
        if experience_score < 100:
            recommendations.append(f"Candidate has {candidate_experience} years experience, requirement is {required_experience}+ years")
        
        if education_score < 100:
            recommendations.append(f"Education level may not fully meet requirements")
        
        return {
            "overall_score": round(overall_score, 2),
            "skill_score": round(skill_score, 2),
            "experience_score": round(experience_score, 2),
            "education_score": round(education_score, 2),
            "skill_matches": skill_matches,
            "total_required_skills": len(required_skills),
            "recommendations": recommendations
        }
    
    @staticmethod
    def get_candidate_status(candidate_id: str) -> dict:
        """Get candidate status and information"""
        try:
            if candidate_id not in ATSTools.candidates:
                return {"success": False, "error": f"Candidate {candidate_id} not found"}
            
            return {"success": True, "candidate": ATSTools.candidates[candidate_id]}
            
        except Exception as e:
            return {"success": False, "error": f"Failed to get candidate status: {str(e)}"}
    
    @staticmethod
    def schedule_interview(candidate_id: str, interview_date: str, interview_type: str) -> dict:
        """Schedule an interview for a candidate"""
        try:
            if candidate_id not in ATSTools.candidates:
                return {"success": False, "error": f"Candidate {candidate_id} not found"}
            
            candidate = ATSTools.candidates[candidate_id]
            interview_id = f"interview_{len(ATSTools.interviews) + 1}_{datetime.now().strftime('%Y%m%d')}"
            
            interview_data = {
                "interview_id": interview_id,
                "candidate_id": candidate_id,
                "job_id": candidate["job_id"],
                "interview_date": interview_date,
                "interview_type": interview_type,
                "status": "scheduled",
                "scheduled_date": datetime.now().isoformat()
            }
            
            ATSTools.interviews[interview_id] = interview_data
            
            name = candidate.get("personal_info", {}).get("name", "Unknown")
            ATSTools._log_activity(f"Interview scheduled for {name} on {interview_date}", candidate_id)
            
            return {
                "success": True,
                "interview_id": interview_id,
                "message": f"Interview scheduled for {interview_date}"
            }
            
        except Exception as e:
            return {"success": False, "error": f"Failed to schedule interview: {str(e)}"}
    
    @staticmethod
    def get_job_applications(job_id: str) -> dict:
        """Get all applications for a job"""
        try:
            if job_id not in ATSTools.jobs:
                return {"success": False, "error": f"Job {job_id} not found"}
            
            job = ATSTools.jobs[job_id]
            applications = []
            
            for candidate_id in job["applications"]:
                if candidate_id in ATSTools.candidates:
                    candidate = ATSTools.candidates[candidate_id]
                    applications.append({
                        "candidate_id": candidate_id,
                        "name": candidate.get("personal_info", {}).get("name", "Unknown"),
                        "status": candidate["status"],
                        "evaluation": candidate.get("evaluation"),
                        "submission_date": candidate["submission_date"]
                    })
            
            return {
                "success": True,
                "job_title": job["title"],
                "total_applications": len(applications),
                "applications": applications
            }
            
        except Exception as e:
            return {"success": False, "error": f"Failed to get job applications: {str(e)}"}
    
    @staticmethod
    def get_ats_dashboard() -> dict:
        """Get ATS dashboard with analytics"""
        try:
            # Calculate status breakdown
            status_breakdown = {}
            for candidate in ATSTools.candidates.values():
                status = candidate["status"]
                status_breakdown[status] = status_breakdown.get(status, 0) + 1
            
            dashboard = {
                "total_job_postings": len(ATSTools.jobs),
                "total_candidates": len(ATSTools.candidates),
                "total_evaluations": len(ATSTools.evaluations),
                "total_interviews": len(ATSTools.interviews),
                "candidate_status_breakdown": status_breakdown,
                "recent_activity": ATSTools.activities[-10:]
            }
            
            return {"success": True, "dashboard": dashboard}
            
        except Exception as e:
            return {"success": False, "error": f"Failed to get dashboard: {str(e)}"}
    
    @staticmethod
    def _log_activity(description: str, entity_id: str = None):
        """Log activity for tracking"""
        activity = {
            "description": description,
            "entity_id": entity_id,
            "date": datetime.now().isoformat()
        }
        ATSTools.activities.append(activity)


# Create the ATS agent
ats_agent = Agent(
    name="ats_agent",
    model="gemini-2.0-flash",
    description="ATS (Applicant Tracking System) agent for managing job postings, candidate applications, resume evaluation, and hiring workflow",
    instruction="""You are an ATS (Applicant Tracking System) agent that manages the complete hiring workflow.

Your capabilities include:
- Creating and managing job postings with detailed requirements
- Processing candidate resume submissions 
- Evaluating resumes against job requirements using multi-dimensional scoring
- Managing candidate status throughout the hiring pipeline
- Scheduling interviews for qualified candidates
- Providing analytics and reporting through the ATS dashboard
- Tracking hiring activities and maintaining audit trails

You integrate seamlessly with the Resume Analyzer agent to provide automated resume parsing and evaluation. You use intelligent scoring algorithms that consider:
- Skills matching (40% weight)
- Experience requirements (40% weight) 
- Education requirements (20% weight)

You automatically qualify candidates based on overall scores:
- 80+ points: Strong candidate (recommend for interview)
- 60-79 points: Good candidate (consider for interview)
- <60 points: Not qualified (below requirements)

Always provide clear, data-driven recommendations to help HR teams make informed hiring decisions.""",
    tools=[]
)
