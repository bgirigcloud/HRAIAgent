# HR AI Agent System

A comprehensive multi-agent system for Human Resources operations using Google's Agent Development Kit (ADK). This system leverages AI to automate and enhance various HR processes including resume analysis, job description parsing, interview transcription analysis, and more.

## 🤖 System Overview

The HR AI Agent system is a collection of specialized sub-agents that work together to provide a complete solution for HR departments. The system is built using Google's Agent Development Kit (ADK) and leverages Gemini models for intelligent processing of HR-related tasks.

## 📋 Features

### Core HR Agents

- **Root Agent**: Orchestrates all sub-agents and provides a unified interface
- **Resume Analyzer Agent**: Analyzes candidate resumes and provides scoring against job requirements
- **Job Description Agent**: Parses and analyzes job descriptions to extract key requirements
- **Interview Transcript Agent**: Analyzes interview transcripts to identify key insights
- **Email Send Agent**: Handles email communications with candidates
- **Scheduling Agent**: Manages interview scheduling and calendar integration

### Additional Agents (Demo Mode)

- **Payroll Assistant**: Helps with payroll processing tasks
- **Neo4j Graph Database Assistant**: Manages organizational structure in graph database
- **Vector Database Assistant**: Handles vector similarity search for HR documents
- **RAG Knowledge Assistant**: Provides retrieval augmented generation for HR knowledge
- **MCP Server Assistant**: Manages Model Context Protocol server operations

## 🔍 Key Capabilities

### Resume Analysis
- Multi-format resume parsing (PDF, Word, Text)
- Skills extraction and matching
- Experience evaluation
- Education assessment
- Multi-dimensional scoring system (0-100)

### Job Description Processing
- Automatic requirement parsing
- Skills, experience, and education requirement extraction
- Pattern matching and intelligent analysis

### Interview Assistance
- Transcript analysis
- Key insights extraction
- Candidate evaluation

### Integration Capabilities
- Google Calendar integration for scheduling
- Email system integration
- ATS (Applicant Tracking System) integration

## 🚀 Deployment

### Local Deployment

1. **Clone the repository**
   ```bash
   git clone https://github.com/bgirigcloud/HRAIAgent.git
   cd HRAIAgent
   ```

2. **Set up environment**
   ```bash
   # Create virtual environment
   python -m venv .venv

   # Activate the environment
   # Windows:
   .venv\Scripts\Activate.ps1
   # macOS/Linux:
   source .venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Configure API Keys**
   - Create a `.env` file in the root directory
   - Add your Google API key:
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```
   - For Google Calendar integration, add OAuth credentials:
     ```
     GOOGLE_CLIENT_ID=your_client_id
     GOOGLE_CLIENT_SECRET=your_client_secret
     ```

4. **Run the application**
   ```bash
   # Run the main application
   python main.py

   # Or run the Streamlit interface
   python -m streamlit run streamlit_app.py --server.port=8505
   ```

### Cloud Run Deployment

1. **Install Google Cloud SDK**
   - Download and install from: https://cloud.google.com/sdk/docs/install

2. **Initialize Google Cloud**
   ```bash
   gcloud init
   gcloud auth login
   ```

3. **Build and deploy to Cloud Run**
   ```bash
   # Build the Docker image
   gcloud builds submit --tag gcr.io/your-project-id/hr-ai-agent

   # Deploy to Cloud Run
   gcloud run deploy hr-ai-agent \
     --image gcr.io/your-project-id/hr-ai-agent \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars="GOOGLE_API_KEY=your_api_key"
   ```

4. **Set up continuous deployment (optional)**
   - Connect your GitHub repository to Cloud Build
   - Configure automatic deployments on new commits

## 📋 Usage Examples

### Resume Analysis

```python
from HR_root_agent.agent import hr_root_agent

# Analyze a resume against a job description
response = hr_root_agent.run(
    "Analyze this resume against the Java Developer job description",
    context={
        "resume_path": "path/to/resume.pdf",
        "job_description_path": "path/to/job_description.txt"
    }
)
print(response)
```

### Job Description Analysis

```python
from HR_root_agent.agent import hr_root_agent

# Analyze a job description
response = hr_root_agent.run(
    "Extract key requirements from this job description",
    context={
        "job_description_path": "path/to/job_description.txt"
    }
)
print(response)
```

### Interview Scheduling

```python
from HR_root_agent.agent import hr_root_agent

# Schedule an interview
response = hr_root_agent.run(
    "Schedule an interview with John Doe for the Software Engineer position",
    context={
        "candidate_email": "john.doe@example.com",
        "position": "Software Engineer",
        "interviewer_email": "hiring.manager@company.com"
    }
)
print(response)
```

## 🛠️ Project Structure

```
HRAIAgent/
├── HR_root_agent/             # Main agent orchestrator
│   ├── agent.py               # Root agent implementation
│   ├── main.py                # Entry point
│   └── sub_agents/            # Specialized sub-agents
│       ├── ats_tool/          # ATS integration tools
│       ├── email_send_agent/  # Email functionality
│       ├── interview_transcript_agent/ # Interview analysis
│       ├── job_description/   # Job description processing
│       ├── resume_analyzer/   # Resume analysis
│       └── scheduling_agent/  # Calendar scheduling
├── demo_agents.py             # Demo agent implementations
├── main.py                    # Main application entry point
├── streamlit_app.py           # Streamlit web interface
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## 📜 Requirements

- Python 3.9+
- Google API key with access to Gemini models
- For Google Calendar integration: Google OAuth credentials
- Required Python packages (see requirements.txt)

## 🔒 Security and Privacy

- All API keys and credentials should be stored in environment variables or secure secret management
- Resume data is processed locally and not stored permanently unless explicitly configured
- OAuth tokens are stored securely and refreshed as needed

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For questions and support, please open an issue in the GitHub repository or contact the repository owner.

---

Built with ❤️ using Google's Agent Development Kit (ADK)
