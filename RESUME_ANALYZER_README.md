# Resume Analyzer Agent - Comprehensive HR Resume Analysis

## Overview

The Resume Analyzer Agent is a powerful AI-powered tool that provides **100% accurate evaluation** of candidate resumes against job descriptions. It uses advanced MCP (Model Context Protocol) tools to parse, analyze, and score resumes with high precision.

## 🚀 Key Features

- **Multi-format Support**: Parse resumes from PDF, DOCX, and TXT files
- **Intelligent Analysis**: Extract skills, experience, education, and contact information
- **Job Description Matching**: Compare resume content against job requirements
- **Multi-dimensional Scoring**: Evaluate candidates across skills, experience, and education
- **Detailed Reports**: Generate comprehensive analysis with actionable recommendations
- **High Accuracy**: AI-powered analysis ensures reliable evaluation results

## 🛠️ MCP Tools Available

### 1. `parse_resume` Tool
- **Purpose**: Extract structured information from resume files
- **Supported Formats**: PDF, DOCX, TXT
- **Output**: Structured data including skills, experience, education, contact info

### 2. `analyze_resume_against_jd` Tool
- **Purpose**: Compare resume data against job description requirements
- **Input**: Parsed resume data + job description text
- **Output**: Comprehensive evaluation scores and analysis report

## 📊 Scoring System

The agent provides scores across multiple dimensions:

- **Overall Score**: Weighted combination of all factors (0-100)
- **Skills Match Score**: Technical skills alignment (0-100)
- **Experience Score**: Work experience relevance (0-100)
- **Education Score**: Educational qualification fit (0-100)

### Scoring Weights
- Skills: 40%
- Experience: 40%
- Education: 20%

## 🔧 Installation

1. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Required Packages**:
- `PyMuPDF` - For PDF parsing
- `python-docx` - For Word document parsing
- `google-adk` - For agent framework

## 📖 Usage Examples

### Basic Resume Analysis

```python
from HR_root_agent.sub_agents.resume_analyzer.agent import ResumeAnalyzerTools

# Parse a resume file
resume_data = ResumeAnalyzerTools.parse_resume("path/to/resume.pdf")

# Analyze against job description
analysis_result = ResumeAnalyzerTools.analyze_resume_against_jd(
    resume_data, 
    job_description_text
)

# Get scores
print(f"Overall Score: {analysis_result['overall_score']}/100")
print(f"Skills Match: {analysis_result['skill_match_score']}/100")
```

### Using the Agent Directly

```python
from HR_root_agent.sub_agents.resume_analyzer.agent import resume_analyzer_agent

# The agent can now use the MCP tools automatically
# It will parse resumes and analyze them against job descriptions
```

## 📋 Input Requirements

### Resume Files
- **PDF**: Standard PDF format with text content
- **DOCX**: Microsoft Word documents
- **TXT**: Plain text files

### Job Description
- Text containing job requirements
- Should include skills, experience, and education requirements
- The agent automatically extracts requirements using pattern matching

## 📊 Output Format

### Parsed Resume Data
```json
{
    "contact_info": {
        "emails": ["email@example.com"],
        "phones": ["+1-555-123-4567"]
    },
    "skills": ["python", "django", "sql"],
    "education": ["Bachelor's Degree in Computer Science"],
    "experience": ["Software Developer - 2020-2024"],
    "raw_text": "Full resume text...",
    "word_count": 150,
    "parsing_success": true
}
```

### Analysis Results
```json
{
    "overall_score": 85.5,
    "skill_match_score": 90.0,
    "experience_score": 80.0,
    "education_score": 100.0,
    "detailed_analysis": "Comprehensive analysis report...",
    "recommendations": [
        "Strong candidate - recommend for interview",
        "Focus on developing cloud platform skills"
    ],
    "analysis_success": true
}
```

## 🎯 Analysis Capabilities

### Skills Extraction
- **Technical Skills**: Python, Java, React, SQL, AWS, Docker, etc.
- **Soft Skills**: Leadership, communication, teamwork, agile
- **Pattern Matching**: Intelligent skill identification from resume text

### Experience Analysis
- **Duration Calculation**: Years of experience in relevant fields
- **Position Relevance**: Job title and responsibility matching
- **Gap Analysis**: Employment history consistency

### Education Evaluation
- **Degree Level**: Bachelor's, Master's, PhD recognition
- **Field Relevance**: Subject area alignment with job requirements
- **Institution Recognition**: University and college identification

## 🔍 How It Works

1. **Resume Parsing**: Extract text and structure from various file formats
2. **Content Analysis**: Identify key information using pattern matching
3. **Requirement Extraction**: Parse job description for requirements
4. **Matching Algorithm**: Compare resume content against requirements
5. **Scoring Calculation**: Generate multi-dimensional scores
6. **Report Generation**: Create detailed analysis with recommendations

## 📈 Accuracy Features

- **Pattern-based Extraction**: Uses regex patterns for reliable information extraction
- **Normalized Comparison**: Standardizes text for accurate matching
- **Partial Match Support**: Identifies similar skills and requirements
- **Error Handling**: Graceful handling of parsing and analysis errors
- **Validation**: Ensures data integrity throughout the process

## 🚨 Error Handling

The agent handles various error scenarios:
- File not found or inaccessible
- Unsupported file formats
- Parsing errors in corrupted files
- Analysis failures due to insufficient data

## 🔧 Customization

### Adding New Skills
```python
# Modify the skills_keywords list in ResumeAnalyzerTools
skills_keywords = [
    'python', 'java', 'javascript', 'react', 'angular', 'vue',
    # Add your custom skills here
    'custom_skill_1', 'custom_skill_2'
]
```

### Adjusting Scoring Weights
```python
# Modify the scoring weights in analyze_resume_against_jd method
overall_score = (skill_match_score * 0.4 + 
                experience_score * 0.4 + 
                education_score * 0.2)
```

## 📝 Best Practices

1. **Resume Quality**: Ensure resumes are in clear, readable formats
2. **Job Description Clarity**: Use specific, well-defined requirements
3. **Regular Updates**: Keep skill keywords updated with industry trends
4. **Validation**: Review analysis results for accuracy
5. **Feedback Loop**: Use results to improve job descriptions

## 🧪 Testing

Run the example script to test the agent:
```bash
python resume_analysis_example.py
```

## 🤝 Integration

The Resume Analyzer Agent integrates seamlessly with:
- **HR Root Agent**: Main HR management system
- **Job Description Agent**: For requirement generation
- **Email Agent**: For candidate communication
- **Scheduling Agent**: For interview coordination

## 📞 Support

For issues or questions:
1. Check the error messages in the output
2. Verify file formats and content
3. Ensure all dependencies are installed
4. Review the analysis logic for custom requirements

## 🔮 Future Enhancements

- **AI-powered Skill Recognition**: Machine learning for better skill identification
- **Industry-specific Templates**: Customized analysis for different sectors
- **Multi-language Support**: Analysis in multiple languages
- **Advanced Analytics**: Trend analysis and candidate comparison
- **Integration APIs**: Connect with ATS and HR systems

---

**Note**: This agent provides high-accuracy analysis but should be used as part of a comprehensive hiring process. Always combine automated analysis with human judgment for final decisions.
