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
- **ATS Integration Agent**: Integrates with Applicant Tracking Systems for seamless workflow
- **HR Policy Assistant**: Manages company policies with document upload and AI-powered Q&A
- **Leave Management Agent**: Comprehensive leave request, approval, and tracking system

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

### Employee Self-Service
- **HR Policy Assistant**: Upload, search, and query company policy documents
  - Multi-format document support (PDF, Word, Text)
  - AI-powered policy Q&A with natural language understanding
  - Category-based organization and search
  - Rate limit handling with automatic retry and fallback
  - See [HR_POLICY_ASSISTANT_README.md](HR_POLICY_ASSISTANT_README.md) for details

- **Leave Management System**: Complete leave request and approval workflow
  - Tenure-based leave allocation (15-25 vacation days)
  - Multiple leave types (Vacation, Sick, Personal, Bereavement, Parental, Unpaid)
  - Employee portal for balance checking and request submission
  - Manager dashboard for approvals and team overview
  - Automated balance tracking and weekday-only calculations
  - Leave history and analytics with AI-powered insights
  - See [LEAVE_MANAGEMENT_README.md](LEAVE_MANAGEMENT_README.md) for details

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
   gcloud builds submit --tag gcr.io/zeta-turbine-477404-d9/hr-ai-agent

   # Deploy to Cloud Run
   gcloud run deploy hr-ai-agent \
     --image gcr.io/zeta-turbine-477404-d9/hr-ai-agent \
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
response = hr_root_agent.send_message(
    "Analyze this resume against the Java Developer job description"
)
print(response.text)
```

### Job Description Analysis

```python
from HR_root_agent.agent import hr_root_agent

# Analyze a job description
response = hr_root_agent.send_message(
    "Extract key requirements from this job description"
)
print(response.text)
```

### Interview Scheduling

```python
from HR_root_agent.agent import hr_root_agent

# Schedule an interview
response = hr_root_agent.send_message(
    "Schedule an interview with John Doe for the Software Engineer position"
)
print(response.text)
```

### HR Policy Management

```python
from HR_root_agent.sub_agents.hr_policy_agent.agent import hr_policy_agent

# Query a policy
response = hr_policy_agent.send_message(
    "What is the remote work policy?"
)
print(response.text)
```

### Leave Management

```python
from HR_root_agent.sub_agents.leave_management.agent import leave_management_agent

# Submit a leave request
response = leave_management_agent.send_message(
    "Submit leave request for EMP001 from 2024-12-20 to 2024-12-22 for Vacation reason: Holiday trip"
)
print(response.text)

# Approve a leave request
response = leave_management_agent.send_message(
    "Approve leave request REQ-EMP001-20241220 by manager MGR001"
)
print(response.text)

# Check leave balance
response = leave_management_agent.send_message(
    "What is the leave balance for employee EMP001?"
)
print(response.text)
```

### Demo Scripts

Run the demo scripts to see the agents in action:

```bash
# Resume analysis demo
python resume_analysis_example.py

# Job description demo
python java_developer_jd_demo.py

# HR Policy Assistant demo
python hr_policy_assistant_demo.py

# Leave Management demo
python leave_management_demo.py

# Full system demo
python integration_example.py
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
│       ├── scheduling_agent/  # Calendar scheduling
│       ├── hr_policy_agent/   # HR policy management
│       └── leave_management/  # Leave request system
├── demo_agents.py             # Demo agent implementations
├── main.py                    # Main application entry point
├── streamlit_app.py           # Streamlit web interface (9 sections)
├── requirements.txt           # Project dependencies
├── README.md                  # This file
├── HR_POLICY_ASSISTANT_README.md  # HR Policy documentation
├── LEAVE_MANAGEMENT_README.md     # Leave Management documentation
├── sample_leave_policy.txt    # Sample leave policy document
├── sample_remote_work_policy.txt  # Sample remote work policy
└── leave_management_demo.py   # Leave system demo script
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
