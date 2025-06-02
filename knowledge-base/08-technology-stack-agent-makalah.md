UID: technology-stack-agent-makalah
Title: Technology Stack for Agent-Makalah
Author: "ERIK SUPIT"
Version: 1.0
Date: "1 Juni 2025"
Role: TECHNOLOGY-SPECIFICATION
Status: DRAFT
Domain: SOFTWARE-ENGINEERING
Dependencies:
  - "srs-agent-makalah"
Anchors:
  - "tsam-root"
  - "tsam-introduction"
  - "tsam-core-frameworks"
  - "tsam-agent-dev-kit"
  - "tsam-prog-language"
  - "tsam-web-framework"
  - "tsam-llm-integration"
  - "tsam-primary-llm-providers"
  - "tsam-llm-orchestration"
  - "tsam-data-management"
  - "tsam-relational-db"
  - "tsam-vector-db"
  - "tsam-object-storage"
  - "tsam-caching-realtime"
  - "tsam-caching-layer"
  - "tsam-message-queue"
  - "tsam-external-services"
  - "tsam-web-search-api"
  - "tsam-file-processing-libs"
  - "tsam-deployment-infra"
  - "tsam-cloud-provider"
  - "tsam-containerization"
  - "tsam-compute-services"
  - "tsam-monitoring-logging"
  - "tsam-ci-cd"
  - "tsam-devops-tools"
  - "tsam-version-control"
  - "tsam-project-management"
  - "tsam-revision-history"
Tags:
  - "tech-stack"
  - "backend"
  - "agent-makalah"
  - "software-architecture"
  - "mvp"
Language: EN
Chained: true

---

> Segment-ID: TSAM-INTRO-001
> Source-File: technology-stack-agent-makalah
> Parent-Anchor: tsam-root
> Context: Introduces the purpose and overview of the technology stack chosen for Agent-Makalah.

## 1. Introduction and Purpose {#tsam-introduction}

This document outlines the core technologies and services that will be utilized to build and deploy the `Agent-Makalah` system. It aims to provide a clear technical roadmap for the development team, ensuring consistency, adherence to architectural principles, and compatibility with the requirements specified in `srs-agent-makalah`. The chosen technology stack emphasizes cloud-native principles, scalability to support an initial target of 1,000 users, modularity, and leveraging established open-source technologies alongside Google ADK.

---

> Segment-ID: TSAM-CORE-FRAMEWORKS-002
> Source-File: technology-stack-agent-makalah
> Parent-Anchor: tsam-root
> Context: Details the core development frameworks and languages used for Agent-Makalah.

## 2. Core Development Frameworks {#tsam-core-frameworks}

*   **2.1. Agent Development Kit:** Google Agent Development Kit (ADK) {#tsam-agent-dev-kit}
    *   **Purpose:** The foundational framework for defining, implementing, and orchestrating the multi-agent system (`Orchestrator_Agent`, `Brainstorming_Agent`, etc.) as specified in `spec-agent-makalah-multi-agent`.
*   **2.2. Programming Language:** Python 3.9+ {#tsam-prog-language}
    *   **Purpose:** The primary language for all backend logic, agent implementations, and custom tools, leveraging Python's rich ecosystem for AI/ML and web development.
*   **2.3. Web Framework (for API/UI Backend):** FastAPI {#tsam-web-framework}
    *   **Purpose:** For building the lightweight, high-performance RESTful API backend that will serve the conversational interface, manage user sessions, handle file uploads, and interact with the ADK agents. FastAPI is chosen for its speed, modern Python features, and developer familiarity.

---

> Segment-ID: TSAM-LLM-INTEGRATION-003
> Source-File: technology-stack-agent-makalah
> Parent-Anchor: tsam-root
> Context: Specifies the Large Language Model (LLM) providers and integration strategy for Agent-Makalah.

## 3. Large Language Model (LLM) Integration {#tsam-llm-integration}

*   **3.1. Primary LLM Providers:** Google Gemini API (Primary), OpenAI API (Fallback/Alternative) {#tsam-primary-llm-providers}
    *   **Purpose:** To provide the core generative AI capabilities for all LLM-powered agents (`Orchestrator_Agent`, `Brainstorming_Agent`, `Writer_Agent`, `Analysis_Editor_Agent`). Utilizing multiple providers offers robustness, fallback options, and flexibility in model access (e.g., via API gateways like OpenRouter for specific model versions).
*   **3.2. LLM Orchestration & Prompt Management:** Handled by Google ADK's `LlmAgent` and custom agent logic. {#tsam-llm-orchestration}
    *   **Purpose:** To manage prompt construction, API calls to LLMs, and parsing of LLM responses within the agent framework.

---

> Segment-ID: TSAM-DATA-MGMT-004
> Source-File: technology-stack-agent-makalah
> Parent-Anchor: tsam-root
> Context: Details the database and storage solutions for Agent-Makalah's data management needs.

## 4. Data Management & Storage {#tsam-data-management}

*   **4.1. Relational Database (for Conversation History, Agent State, Metadata):** PostgreSQL (via Supabase Managed Service) {#tsam-relational-db}
    *   **Purpose:** For persistent storage of structured data including full conversation history, detailed agent states across sessions, metadata for intermediate artifacts (topics, references, outlines), and uploaded file metadata. PostgreSQL is robust and widely supported. Supabase offers a managed solution that simplifies database operations and provides a familiar environment.
*   **4.2. Vector Database (for Semantic Search/KB Retrieval - Future):** (Post-MVP Consideration) {#tsam-vector-db}
    *   **Purpose:** To support advanced semantic search, contextual retrieval, and Knowledge Graph features (as outlined in `prd-agent-makalah#prd-future-considerations`) in future iterations by storing vector embeddings of knowledge bases or content.
*   **4.3. Object Storage (for User-Uploaded Files):** Cloudinary, AWS S3, or similar object storage service {#tsam-object-storage}
    *   **Purpose:** For secure and scalable temporary storage of user-uploaded academic paper files (PDF, DOCX, TXT) before and during processing by `Analysis_Editor_Agent`.

---

> Segment-ID: TSAM-CACHING-REALTIME-005
> Source-File: technology-stack-agent-makalah
> Parent-Anchor: tsam-root
> Context: Defines caching and real-time data solutions for enhancing performance and managing ephemeral data.

## 5. Caching & Real-time Data {#tsam-caching-realtime}

*   **5.1. Caching Layer:** Redis (via Upstash for Serverless Redis) {#tsam-caching-layer}
    *   **Purpose:** For high-speed caching of frequently accessed, ephemeral data (e.g., short-term session data not managed by ADK's core state persistence, potentially cached LLM responses if permissible by policy, rate limiting). Upstash provides a cost-effective and scalable serverless Redis solution ideal for MVP.
*   **5.2. Message Queue (Post-MVP):** (Post-MVP Consideration) {#tsam-message-queue}
    *   **Purpose:** To enable asynchronous communication patterns, decouple services, and handle high-throughput event processing in future, more distributed architectures.

---

> Segment-ID: TSAM-EXTERNAL-SERVICES-006
> Source-File: technology-stack-agent-makalah
> Parent-Anchor: tsam-root
> Context: Lists and describes external APIs and services consumed by Agent-Makalah.

## 6. External Services & APIs {#tsam-external-services}

*   **6.1. Web Search API:** Serper API (Primary), Google Search API (Alternative/Fallback) {#tsam-web-search-api}
    *   **Purpose:** To provide accurate and relevant web search results for `tool-makalah-web-search`, enabling `Brainstorming_Agent` (for inspiration) and `Literature_Search_Agent` (for academic database searches not directly accessible via dedicated APIs). Serper is chosen for its specific focus on structured search results from Google.
*   **6.2. File Processing Libraries:** PyPDF2, python-docx, other relevant Python libraries {#tsam-file-processing-libs}
    *   **Purpose:** For pre-processing user-uploaded document files (e.g., text extraction from PDFs, parsing DOCX) as part of `tool-makalah-browse-files` implementation. These are internal Python libraries used within the agent's logic.

---

> Segment-ID: TSAM-DEPLOYMENT-INFRA-007
> Source-File: technology-stack-agent-makalah
> Parent-Anchor: tsam-root
> Context: Defines the cloud infrastructure and deployment strategy for Agent-Makalah.

## 7. Deployment & Infrastructure {#tsam-deployment-infra}

*   **7.1. Cloud Provider:** Render.com (PaaS) {#tsam-cloud-provider}
    *   **Purpose:** The primary Platform-as-a-Service for hosting, deploying, and managing all `Agent-Makalah` services, leveraging its ease of use, Git-based deployment, and managed services for databases and caching.
*   **7.2. Containerization:** Docker {#tsam-containerization}
    *   **Purpose:** To package `Agent-Makalah`'s FastAPI backend and ADK agent components into consistent, isolated environments for simplified deployment and scalability on Render.com.
*   **7.3. Compute Services (for Backend & Agents):** Render Services (e.g., Web Service for FastAPI, Background Workers for ADK Agents) {#tsam-compute-services}
    *   **Purpose:** For deploying the FastAPI backend and individual ADK agents as scalable services on Render.com. Render Services offer auto-scaling (based on configuration), custom domains, and managed environments suitable for MVP and beyond.
*   **7.4. Monitoring & Logging:** Render built-in Metrics & Logging, with optional integration to external APM/logging services (e.g., Datadog, Sentry) {#tsam-monitoring-logging}
    *   **Purpose:** For collecting application logs, basic metrics, and traces from services running on Render.com. External services can be integrated for more advanced observability if needed.
*   **7.5. Continuous Integration/Continuous Deployment (CI/CD):** GitHub Actions for building Docker images and pushing to a registry; Render.com for auto-deploying from the connected Git repository or Docker registry {#tsam-ci-cd}
    *   **Purpose:** To automate the software delivery pipeline. GitHub Actions can handle build and test automation, while Render.com provides seamless auto-deployment from a linked GitHub repository or a specified Docker image.

---

> Segment-ID: TSAM-DEVOP-TOOLS-008
> Source-File: technology-stack-agent-makalah
> Parent-Anchor: tsam-root
> Context: Lists key development and operations tools used in the Agent-Makalah project.

## 8. Development & Operations (DevOps) Tools {#tsam-devops-tools}

*   **8.1. Version Control:** Git (e.g., GitHub) {#tsam-version-control}
    *   **Purpose:** For collaborative code management, versioning, and change tracking.
*   **8.2. Project Management:** (e.g., Jira, Trello, Asana) {#tsam-project-management}
    *   **Purpose:** For managing tasks, tracking progress, and facilitating team collaboration.

---

> Segment-ID: TSAM-REVISION-HISTORY-009
> Source-File: technology-stack-agent-makalah
> Parent-Anchor: tsam-root
> Context: Tracks the version history and changes made to this Technology Stack document.

## 9. Revision History {#tsam-revision-history}

| Version | Date       | Author(s)   | Summary of Changes                                                                        |
| :------ | :--------- | :---------- | :---------------------------------------------------------------------------------------- |
| 1.0     | 1 Jun 2025 | ERIK SUPIT  | Initial MVP draft of the Technology Stack for `Agent-Makalah`.                            |
|         |            |             |                                                                                           |
|         |            |             |                                                                                           |

---