# Agent-Makalah Backend System

![Python](https://img.shields.io/badge/python-v3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-framework-green.svg)
![Google Cloud](https://img.shields.io/badge/Google%20Cloud-platform-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-database-336791.svg)

An innovative AI-powered academic writing assistant designed to transform the academic paper writing and analysis process. Unlike traditional AI writing tools that act as mere "paper jockeys," Agent-Makalah aims to be a collaborative sparring partner, enhancing users' critical reasoning skills while providing verifiable evidence of their active intellectual involvement.

## 🎯 Project Vision

Agent-Makalah is specifically designed for **Bahasa Indonesia academic writing**, targeting:
- University students (undergraduate and postgraduate)
- Researchers and academics
- Academic professionals
- Initial target: 1,000 users

## 🚀 Key Features

### 📝 New Academic Paper Creation
Complete guided workflow from concept to final paper:
- **Topic Ideation & Finalization** - Interactive brainstorming sessions
- **Literature Search & Curation** - Comprehensive academic source identification
- **Outline & Structure Development** - Logical paper organization
- **Section-by-Section Content Generation** - Human-like prose in Bahasa Indonesia
- **Final Assembly** - Complete compilation with unified bibliography

### 🔍 Existing Paper Analysis & Feedback
Document analysis and constructive feedback:
- **Document Upload & Processing** - Support for PDF, DOCX, TXT
- **Configurable Analysis** - User-specified criteria and evaluation
- **Detailed Report Generation** - Comprehensive improvement recommendations

### 🤝 Interactive User Engagement
- **Rigorous Clarification Dialogues** - Proactive questioning for precise inputs
- **User Validation Loops** - Explicit approval/revision cycles
- **Progress Communication** - Clear status updates throughout workflows
- **Revision Management** - Limited iteration cycles (max 3 attempts per stage)

## 🏗️ System Architecture

### Core Technology Stack
- **Agent Framework**: Google Agent Development Kit (ADK)
- **Programming Language**: Python 3.9+
- **Web Framework**: FastAPI
- **Cloud Provider**: Google Cloud Platform (GCP)
- **Database**: PostgreSQL (via Supabase)
- **Object Storage**: Google Cloud Storage (GCS)
- **Caching**: Redis (via Upstash)

### Multi-Agent Architecture
The system implements six specialized agents:

1. **Orchestrator_Agent** - Central controller and workflow coordinator
2. **Brainstorming_Agent** - Topic ideation and exploration
3. **Literature_Search_Agent** - Academic literature research
4. **Outline_Draft_Agent** - Structure and outline development
5. **Writer_Agent** - Content generation and prose writing
6. **Analysis_Editor_Agent** - Document analysis and feedback

### External Integrations
- **LLM Providers**: Google Gemini API (Primary), OpenAI API (Fallback)
- **Web Search**: Serper API (Primary), Google Search API (Fallback)
- **File Processing**: PyPDF2, python-docx libraries

## 📁 Project Structure

```
agent-makalah-backend/
├── src/                    # Source code
│   ├── agents/            # Multi-agent implementations
│   ├── api/               # FastAPI routes and endpoints
│   ├── core/              # Core business logic
│   ├── models/            # Database models
│   └── utils/             # Utility functions
├── tests/                 # Test suites
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── e2e/               # End-to-end tests
├── docs/                  # Documentation
│   ├── api/               # API documentation
│   ├── architecture/      # System architecture docs
│   └── deployment/        # Deployment guides
├── scripts/               # Utility scripts
├── .taskmaster/           # Taskmaster AI project management
├── .cursor/               # Cursor IDE configurations
└── knowledge-base/        # Project documentation and requirements
```

## 🛠️ Development Setup

### Prerequisites
- Python 3.9+
- Docker
- Google Cloud SDK
- PostgreSQL (local development)
- Redis (local development)

### Quick Start
```bash
# Clone the repository
git clone https://github.com/your-username/agent-makalah-backend.git
cd agent-makalah-backend

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys and configuration

# Run database migrations
alembic upgrade head

# Start the development server
uvicorn src.main:app --reload
```

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY` - OpenAI API key for LLM access
- `GOOGLE_GEMINI_API_KEY` - Google Gemini API key
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `SERPER_API_KEY` - Serper search API key
- `GCS_BUCKET_NAME` - Google Cloud Storage bucket

### MCP (Model Context Protocol) Setup
For Cursor IDE integration with Taskmaster AI:

1. Copy the MCP configuration template:
   ```bash
   cp .cursor/mcp.json.example .cursor/mcp.json
   ```

2. Edit `.cursor/mcp.json` and replace `your-openai-api-key-here` with your actual OpenAI API key

3. Restart Cursor IDE to load the MCP server

**Note**: The actual `.cursor/mcp.json` file is gitignored for security reasons.

### API Documentation
Once the server is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test types
pytest tests/unit/          # Unit tests
pytest tests/integration/   # Integration tests
pytest tests/e2e/          # End-to-end tests

# Run with coverage
pytest --cov=src tests/
```

## 📊 Performance Targets

- **Response Time**: < 5 seconds for interactive dialogues
- **File Processing**: < 30 seconds for standard documents
- **Scalability**: Support 1,000 concurrent users
- **Uptime**: 99.5% target
- **Error Rate**: < 1%

## 🔒 Security & Privacy

- Data encryption at rest and in transit
- Secure file upload and storage
- User privacy compliance
- Sandboxed tool execution
- Comprehensive logging and monitoring

## 📈 Academic Quality Standards

### Bahasa Indonesia Academic Writing
- Strict adherence to Indonesian academic conventions
- Natural, sophisticated prose generation
- Avoidance of robotic or predictable patterns
- Cultural and linguistic nuance preservation

### Quality Assurance
- Human-like output that passes academic scrutiny
- Consistent style across all generated content
- Proper citation and referencing formats
- Academic integrity maintenance

## 🚀 Deployment

### Google Cloud Run (Production)
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/agent-makalah-backend
gcloud run deploy --image gcr.io/PROJECT_ID/agent-makalah-backend --platform managed
```

### Docker (Local/Development)
```bash
# Build image
docker build -t agent-makalah-backend .

# Run container
docker run -p 8000:8000 --env-file .env agent-makalah-backend
```

## 📝 Development Workflow

This project uses **Taskmaster AI** for project management and task tracking:

```bash
# View current tasks
task-master list

# Work on next task
task-master next

# Update task status
task-master set-status --id=1 --status=done
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 Roadmap

### Phase 1: Core Infrastructure (Weeks 1-2) ✅
- [x] Project repository setup
- [ ] FastAPI backend setup
- [ ] PostgreSQL database configuration
- [ ] Basic authentication and session management

### Phase 2: ADK Agent Framework (Weeks 3-4)
- [ ] Orchestrator_Agent implementation
- [ ] Basic multi-agent communication
- [ ] Session state management
- [ ] Error handling framework

### Phase 3: Specialized Agents (Weeks 5-7)
- [ ] Brainstorming_Agent development
- [ ] Literature_Search_Agent implementation
- [ ] Outline_Draft_Agent creation
- [ ] Writer_Agent development
- [ ] Analysis_Editor_Agent implementation

### Phase 4: Workflow Integration (Weeks 8-9)
- [ ] End-to-end paper creation workflow
- [ ] Document analysis workflow
- [ ] User validation and revision loops
- [ ] Interactive clarification system

### Phase 5: Testing & Optimization (Weeks 10-11)
- [ ] Comprehensive testing suite
- [ ] Performance optimization
- [ ] Security hardening
- [ ] Documentation completion

### Phase 6: Deployment & Launch (Week 12)
- [ ] Production deployment
- [ ] Monitoring setup
- [ ] User acceptance testing
- [ ] MVP launch

## 🆘 Support

For support, please contact:
- **Author**: Erik Supit
- **Email**: [your-email@domain.com]
- **Project Issues**: [GitHub Issues](https://github.com/your-username/agent-makalah-backend/issues)

---

**Built with ❤️ for Indonesian Academic Community** 