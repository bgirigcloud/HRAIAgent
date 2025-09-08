# HR Multi-Agent System Restructuring and Advanced Capabilities

## Restructuring Overview

The HR Multi-Agent system has been restructured to follow a more modular and hierarchical approach:

1. **Root Agent**: Serves as the coordinator for all sub-agents
2. **Sub-Agents**: Specialized agents for different HR functions
3. **Streamlit UI**: Interacts with the root agent to access all sub-agent capabilities

## Agent Architecture

### Root Agent
- Located at `HR_root_agent/agent.py`
- Coordinates all sub-agents
- Provides a unified API for the UI

### Sub-Agents
All agents now reside in the `HR_root_agent/sub_agents/` directory:

1. **Job Description Agent** - Generates and analyzes job descriptions
2. **Email Send Agent** - Composes and sends emails
3. **Interview Transcript Agent** - Analyzes interview transcripts
4. **Resume Analyzer Agent** - Analyzes resumes and matches them to job descriptions
5. **Scheduling Agent** - Manages interview scheduling
6. **ATS Agent** - Manages applicant tracking system operations
7. **Onboarding Agent** - Handles employee onboarding processes
8. **Payroll Agent** - Manages payroll processing and reporting

### Advanced Capabilities

Four new advanced capabilities have been added:

#### 1. Neo4j Graph Database (HR_root_agent/sub_agents/neo4j_agent)
- Organizational structure visualization
- Employee relationship mapping
- Reporting chain analysis
- Department connection exploration
- Graph analytics for HR data

#### 2. PGVector Database (HR_root_agent/sub_agents/pgvector_db_agent)
- Vector embedding storage for resumes and job descriptions
- Similarity search for candidate-job matching
- Semantic search across HR documents
- Fast retrieval of similar documents

#### 3. Retrieval Augmented Generation (HR_root_agent/sub_agents/rag_agent)
- Context-aware HR knowledge generation
- Enhanced responses using relevant HR document context
- Improved accuracy in domain-specific responses
- Dynamic knowledge integration from multiple sources

#### 4. Model Context Protocol Server (HR_root_agent/sub_agents/mcp_server_agent)
- Standardized API for HR AI operations
- Integration with external tools and services
- Scalable deployment of HR AI capabilities
- Pluggable architecture for adding new tools

## Integration Flow

The system now follows this integration flow:

1. Streamlit UI calls Root Agent
2. Root Agent delegates to appropriate Sub-Agents
3. Sub-Agents perform specialized tasks
4. Results flow back up to Root Agent
5. Root Agent provides consolidated response to UI

## Environment Setup

New dependencies have been added to support the advanced capabilities:

```
# Neo4j dependencies
neo4j==5.14.1

# PGVector dependencies
psycopg2-binary==2.9.9
numpy==1.26.1

# RAG dependencies
sentence-transformers==2.2.2

# MCP Server dependencies
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.4.2
```

Install using:

```
pip install -r requirements.txt
```

## Configuration

Each advanced capability requires specific configuration:

### Neo4j Configuration
```
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
```

### PGVector Configuration
```
PGVECTOR_HOST=localhost
PGVECTOR_PORT=5432
PGVECTOR_DB=hr_vector_db
PGVECTOR_USER=postgres
PGVECTOR_PASSWORD=postgres
```

### MCP Server Configuration
```
MCP_HOST=0.0.0.0
MCP_PORT=8000
```

Set these in your `.env` file or as environment variables.

## Usage Examples

### Using Neo4j Agent
```python
from HR_root_agent.sub_agents.neo4j_agent import neo4j_agent

# Connect to database
neo4j_agent.connect()

# Get organizational hierarchy
hierarchy = neo4j_agent.get_organizational_hierarchy(department="Engineering")
```

### Using PGVector Agent
```python
from HR_root_agent.sub_agents.pgvector_db_agent import pgvector_db_agent

# Connect to database
pgvector_db_agent.connect()

# Find matching candidates for a job
candidates = pgvector_db_agent.find_matching_candidates(jd_embedding)
```

### Using RAG Agent
```python
from HR_root_agent.sub_agents.rag_agent import rag_agent

# Augment a prompt with relevant context
augmented_prompt = rag_agent.augment_prompt("What skills are needed for a DevOps role?")
```

### Using MCP Server Agent
```python
from HR_root_agent.sub_agents.mcp_server_agent import mcp_server_agent

# Start the MCP server
mcp_server_agent.start_server()
```

## Mock Implementations

For demonstration purposes, mock implementations of all agents are provided in the `demo_agents.py` file. These are used when the actual agent implementations are not available or when running in demo mode.
