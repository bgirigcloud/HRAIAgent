import os
import json
import re
from typing import Dict, List, Any, Optional
from pathlib import Path
import fitz  # PyMuPDF for PDF parsing
import docx  # python-docx for Word documents
from google.adk.agents import Agent

class ResumeAnalyzerTools:
    """MCP tools for resume analysis and evaluation"""
    
    @staticmethod
    def parse_resume(file_path: str) -> Dict[str, Any]:
        """
        Parse resume from various file formats (PDF, DOCX, TXT)
        
        Args:
            file_path: Path to the resume file
            
        Returns:
            Dictionary containing parsed resume information
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {"error": f"File not found: {file_path}"}
            
            file_extension = file_path.suffix.lower()
            
            if file_extension == '.pdf':
                return ResumeAnalyzerTools._parse_pdf(file_path)
            elif file_extension == '.docx':
                return ResumeAnalyzerTools._parse_docx(file_path)
            elif file_extension == '.txt':
                return ResumeAnalyzerTools._parse_txt(file_path)
            else:
                return {"error": f"Unsupported file format: {file_extension}"}
                
        except Exception as e:
            return {"error": f"Error parsing resume: {str(e)}"}
    
    @staticmethod
    def _parse_pdf(file_path: Path) -> Dict[str, Any]:
        """Parse PDF resume"""
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            
            return ResumeAnalyzerTools._extract_resume_sections(text)
        except Exception as e:
            return {"error": f"Error parsing PDF: {str(e)}"}
    
    @staticmethod
    def _parse_docx(file_path: Path) -> Dict[str, Any]:
        """Parse DOCX resume"""
        try:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return ResumeAnalyzerTools._extract_resume_sections(text)
        except Exception as e:
            return {"error": f"Error parsing DOCX: {str(e)}"}
    
    @staticmethod
    def _parse_txt(file_path: Path) -> Dict[str, Any]:
        """Parse TXT resume"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            return ResumeAnalyzerTools._extract_resume_sections(text)
        except Exception as e:
            return {"error": f"Error parsing TXT: {str(e)}"}
    
    @staticmethod
    def _extract_resume_sections(text: str) -> Dict[str, Any]:
        """Extract structured information from resume text"""
        # Clean and normalize text
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Extract contact information
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        
        emails = re.findall(email_pattern, text)
        phones = re.findall(phone_pattern, text)
        
        # Extract skills (common technical skills)
        skills_keywords = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node.js',
            'sql', 'mongodb', 'postgresql', 'aws', 'azure', 'docker', 'kubernetes',
            'machine learning', 'ai', 'data analysis', 'project management',
            'agile', 'scrum', 'leadership', 'communication', 'teamwork'
        ]
        
        found_skills = []
        text_lower = text.lower()
        for skill in skills_keywords:
            if skill in text_lower:
                found_skills.append(skill)
        
        # Extract education - look for specific patterns
        education_patterns = [
            r'(?:bachelor|master|phd)[\'s]*\s+degree[^.]*',
            r'degree[^.]*(?:computer science|software engineering|engineering)',
            r'(?:university|college)[^.]*',
            r'(?:stanford|mit|harvard|berkeley)[^.]*'
        ]
        
        education_sections = []
        for pattern in education_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            education_sections.extend(matches)
        
        # Remove duplicates and clean up
        education_sections = list(set([edu.strip() for edu in education_sections if edu.strip()]))
        
        # Extract experience - look for job titles and date patterns
        experience_patterns = [
            r'(?:senior\s+)?(?:python|software|web|full.?stack)\s+developer[^.]*',
            r'(?:engineer|developer|programmer)[^.]*',
            r'\d{4}[-–]\d{4}[^.]*',
            r'\d{4}[-–](?:present|current)[^.]*'
        ]
        
        experience_sections = []
        for pattern in experience_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            experience_sections.extend(matches)
        
        # Remove duplicates and clean up
        experience_sections = list(set([exp.strip() for exp in experience_sections if exp.strip()]))
        
        # Extract years of experience
        years_pattern = r'(\d+)\s+years?'
        years_matches = re.findall(years_pattern, text.lower())
        total_years = sum(int(year) for year in years_matches)
        
        return {
            "contact_info": {
                "emails": emails,
                "phones": phones
            },
            "skills": found_skills,
            "education": education_sections,
            "experience": experience_sections,
            "total_years_experience": total_years,
            "raw_text": text,
            "word_count": len(text.split()),
            "parsing_success": True
        }
    
    @staticmethod
    def analyze_resume_against_jd(resume_data: Dict[str, Any], job_description: str) -> Dict[str, Any]:
        """
        Analyze resume against job description and provide evaluation
        
        Args:
            resume_data: Parsed resume data
            job_description: Job description text
            
        Returns:
            Dictionary containing analysis results and scores
        """
        try:
            # Extract key requirements from job description
            jd_requirements = ResumeAnalyzerTools._extract_jd_requirements(job_description)
            
            # Calculate skill match score
            skill_match_score = ResumeAnalyzerTools._calculate_skill_match(
                resume_data.get('skills', []), 
                jd_requirements.get('required_skills', [])
            )
            
            # Calculate experience relevance score
            experience_score = ResumeAnalyzerTools._calculate_experience_score(
                resume_data.get('experience', []),
                jd_requirements.get('experience_requirements', [])
            )
            
            # Calculate education fit score
            education_score = ResumeAnalyzerTools._calculate_education_score(
                resume_data.get('education', []),
                jd_requirements.get('education_requirements', [])
            )
            
            # Calculate overall fit score
            overall_score = (skill_match_score * 0.4 + 
                           experience_score * 0.4 + 
                           education_score * 0.2)
            
            # Generate detailed analysis
            analysis = ResumeAnalyzerTools._generate_detailed_analysis(
                resume_data, jd_requirements, skill_match_score, 
                experience_score, education_score, overall_score
            )
            
            return {
                "overall_score": round(overall_score, 2),
                "skill_match_score": round(skill_match_score, 2),
                "experience_score": round(experience_score, 2),
                "education_score": round(education_score, 2),
                "detailed_analysis": analysis,
                "recommendations": ResumeAnalyzerTools._generate_recommendations(
                    overall_score, skill_match_score, experience_score, education_score
                ),
                "analysis_success": True
            }
            
        except Exception as e:
            return {"error": f"Error analyzing resume: {str(e)}"}
    
    @staticmethod
    def _extract_jd_requirements(jd_text: str) -> Dict[str, Any]:
        """Extract requirements from job description"""
        jd_lower = jd_text.lower()
        
        # Extract required skills
        skill_patterns = [
            r'required skills?[:\s]+([^.\n]+)',
            r'must have[:\s]+([^.\n]+)',
            r'requirements?[:\s]+([^.\n]+)',
            r'qualifications?[:\s]+([^.\n]+)'
        ]
        
        required_skills = []
        for pattern in skill_patterns:
            matches = re.findall(pattern, jd_lower)
            for match in matches:
                skills = [skill.strip() for skill in match.split(',')]
                required_skills.extend(skills)
        
        # Extract experience requirements
        exp_patterns = [
            r'(\d+)[\s-]+years?[\s-]+experience',
            r'experience[:\s]+([^.\n]+)',
            r'minimum[\s-]+(\d+)[\s-]+years?'
        ]
        
        experience_requirements = []
        for pattern in exp_patterns:
            matches = re.findall(pattern, jd_lower)
            experience_requirements.extend(matches)
        
        # Extract education requirements
        education_patterns = [
            r'bachelor[\s-]+degree',
            r'master[\s-]+degree',
            r'phd[\s-]+degree',
            r'degree[\s-]+in[\s-]+([^.\n]+)'
        ]
        
        education_requirements = []
        for pattern in education_patterns:
            matches = re.findall(pattern, jd_lower)
            education_requirements.extend(matches)
        
        return {
            "required_skills": list(set(required_skills)),
            "experience_requirements": list(set(experience_requirements)),
            "education_requirements": list(set(education_requirements))
        }
    
    @staticmethod
    def _calculate_skill_match(resume_skills: List[str], required_skills: List[str]) -> float:
        """Calculate skill match score (0-100)"""
        if not required_skills:
            return 100.0
        
        if not resume_skills:
            return 0.0
        
        # Normalize skills for comparison
        resume_skills_normalized = [skill.lower().strip() for skill in resume_skills]
        required_skills_normalized = [skill.lower().strip() for skill in required_skills]
        
        # Calculate exact matches
        exact_matches = sum(1 for skill in required_skills_normalized 
                          if skill in resume_skills_normalized)
        
        # Calculate partial matches (substring matching)
        partial_matches = 0
        for req_skill in required_skills_normalized:
            for res_skill in resume_skills_normalized:
                if req_skill in res_skill or res_skill in req_skill:
                    partial_matches += 1
                    break
        
        # Use the higher of exact or partial matches
        matches = max(exact_matches, partial_matches)
        
        return min(100.0, (matches / len(required_skills_normalized)) * 100)
    
    @staticmethod
    def _calculate_experience_score(experience_sections: List[str], requirements: List[str]) -> float:
        """Calculate experience relevance score (0-100)"""
        if not requirements:
            return 100.0
        
        if not experience_sections:
            return 0.0
        
        # Look for years of experience in resume
        years_pattern = r'(\d+)[\s-]+years?'
        total_years = 0
        
        for exp_section in experience_sections:
            if isinstance(exp_section, str):
                matches = re.findall(years_pattern, exp_section.lower())
                for match in matches:
                    total_years += int(match)
        
        # Check if experience meets minimum requirements
        min_required = 0
        for req in requirements:
            if isinstance(req, str) and req.isdigit():
                min_required = max(min_required, int(req))
        
        if min_required == 0:
            return 100.0
        
        if total_years >= min_required:
            return 100.0
        else:
            return max(0.0, (total_years / min_required) * 100)
    
    @staticmethod
    def _calculate_education_score(education_sections: List[str], requirements: List[str]) -> float:
        """Calculate education fit score (0-100)"""
        if not requirements:
            return 100.0
        
        if not education_sections:
            return 0.0
        
        # Check if required education level is met
        education_text = ' '.join(education_sections).lower()
        
        if 'phd' in requirements and 'phd' in education_text:
            return 100.0
        elif 'master' in requirements and ('master' in education_text or 'phd' in education_text):
            return 100.0
        elif 'bachelor' in requirements and any(level in education_text for level in ['bachelor', 'master', 'phd']):
            return 100.0
        else:
            return 50.0  # Partial match
    
    @staticmethod
    def _generate_detailed_analysis(resume_data: Dict[str, Any], jd_requirements: Dict[str, Any],
                                  skill_score: float, exp_score: float, edu_score: float, 
                                  overall_score: float) -> str:
        """Generate detailed analysis text"""
        analysis = f"""
RESUME ANALYSIS REPORT
=====================

OVERALL EVALUATION: {overall_score}/100

SKILLS ANALYSIS: {skill_score}/100
- Required Skills: {', '.join(jd_requirements.get('required_skills', ['None specified']))}
- Candidate Skills: {', '.join(resume_data.get('skills', ['None found']))}
- Assessment: {'Excellent match' if skill_score >= 80 else 'Good match' if skill_score >= 60 else 'Partial match' if skill_score >= 40 else 'Poor match'}

EXPERIENCE ANALYSIS: {exp_score}/100
- Experience Requirements: {', '.join(jd_requirements.get('experience_requirements', ['None specified']))}
- Candidate Experience: {len(resume_data.get('experience', []))} positions identified
- Assessment: {'Meets requirements' if exp_score >= 80 else 'Partially meets requirements' if exp_score >= 60 else 'Below requirements'}

EDUCATION ANALYSIS: {edu_score}/100
- Education Requirements: {', '.join(jd_requirements.get('education_requirements', ['None specified']))}
- Candidate Education: {len(resume_data.get('education', []))} entries found
- Assessment: {'Meets requirements' if edu_score >= 80 else 'Partially meets requirements' if edu_score >= 60 else 'Below requirements'}

RECOMMENDATION: {'Strong Candidate' if overall_score >= 80 else 'Good Candidate' if overall_score >= 60 else 'Consider with reservations' if overall_score >= 40 else 'Not recommended'}
        """
        return analysis.strip()
    
    @staticmethod
    def _generate_recommendations(overall_score: float, skill_score: float, 
                                exp_score: float, edu_score: float) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if overall_score >= 80:
            recommendations.append("Strong candidate - recommend for interview")
        elif overall_score >= 60:
            recommendations.append("Good candidate - consider for interview")
        else:
            recommendations.append("Candidate needs improvement - consider for future positions")
        
        if skill_score < 60:
            recommendations.append("Focus on developing required technical skills")
        
        if exp_score < 60:
            recommendations.append("Consider candidates with more relevant experience")
        
        if edu_score < 60:
            recommendations.append("Verify education requirements are truly necessary")
        
        return recommendations

# Enhanced resume analyzer agent
resume_analyzer_agent = Agent(
    name="resume_analyzer_agent",
    model="gemini-2.0-flash",
    instruction="""You are an expert HR resume analyzer that provides 100% accurate evaluation of candidate resumes against job descriptions.

Your capabilities include:
- Parsing resumes from PDF, DOCX, and TXT formats
- Extracting key information: skills, experience, education, contact details
- Analyzing resume content against job requirements
- Providing detailed scoring across multiple dimensions
- Generating comprehensive evaluation reports
- Offering actionable recommendations

Always maintain objectivity and provide evidence-based analysis. Use the available tools to:
1. Parse resume files to extract structured information
2. Analyze resume fit against job descriptions
3. Generate detailed evaluation reports with scores
4. Provide specific recommendations for hiring decisions

Be thorough in your analysis and ensure all evaluations are supported by concrete evidence from the resume and job description.""",
    description="A comprehensive resume analysis agent that parses, analyzes, and evaluates candidate resumes against job descriptions with high accuracy",
    tools=[],
)
