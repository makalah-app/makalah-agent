UID: backend-architecture-agent-makalah
Title: Backend Architecture Design for Agent-Makalah
Author: "ERIK SUPIT"
Version: 1.0
Date: "1 Juni 2025"
Role: ARCHITECTURE-DESIGN
Status: DRAFT
Domain: SOFTWARE-ENGINEERING
Dependencies:
  - "srs-agent-makalah"
  - "technology-stack-agent-makalah"
  - "adk-integration-agent-makalah"
Anchors:
  - "baum-root"
  - "baum-introduction"
  - "baum-high-level-arch"
  - "baum-detailed-components"
  - "baum-client-interface"
  - "baum-backend-api"
  - "baum-adk-layer"
  - "baum-adk-orchestrator-deployment"
  - "baum-adk-sub-agents-deployment"
  - "baum-adk-inter-agent-comm"
  - "baum-adk-workflow-mgmt"
  - "baum-data-persistence"
  - "baum-postgresql-db"
  - "baum-redis-cache"
  - "baum-object-storage"
  - "baum-external-integrations"
  - "baum-llm-providers"
  - "baum-web-search-api"
  - "baum-custom-tools"
  - "baum-logging-monitoring"
  - "baum-data-flow"
  - "baum-security-arch"
  - "baum-scalability-reliability"
  - "baum-deployment-strategy"
  - "baum-future-enhancements"
  - "baum-revision-history"
Tags:
  - "backend-architecture"
  - "software-design"
  - "agent-makalah"
  - "cloud-native"
  - "mvp"
Language: EN
Chained: true
---

> Segment-ID: BAUM-INTRO-001
> Source-File: backend-architecture-agent-makalah
> Parent-Anchor: baum-root
> Context: Overview of the backend architecture document's purpose, system context, and architectural goals.

## 1. Introduction {#baum-introduction}

**1.1. Purpose of this Document**
This Backend Architecture Design document provides a comprehensive overview of the technical architecture for the `Agent-Makalah` system. It outlines the major components, their interactions, data flows, and key design considerations, serving as a blueprint for the development team to implement the system. This document translates the functional and non-functional requirements detailed in the `Software Requirements Specification (SRS) for Agent-Makalah` (`srs-agent-makalah`) into a concrete architectural design, leveraging the technology stack defined in `technology-stack-agent-makalah`.

**1.2. System Context**
`Agent-Makalah` is designed as a cloud-native, multi-agent AI system that facilitates academic paper creation and analysis. From an architectural perspective, it sits as a backend service consumed by a user-facing conversational interface. The system's core intelligence and orchestration capabilities reside within its specialized multi-agent structure, built upon the Google Agent Development Kit (ADK). This architecture aims to provide a robust, scalable, and maintainable foundation for `Agent-Makalah`'s MVP and future enhancements.

**1.3. Architectural Goals & Principles**
The design of `Agent-Makalah`'s backend architecture is guided by the following principles and goals:
*   **Modularity:** Emphasizing clear separation of concerns through independent components and microservices (where applicable) for ease of development, testing, and maintenance.
*   **Scalability:** Designing for horizontal scalability, especially for compute-intensive components, to accommodate increasing user load and processing demands.
*   **Reliability:** Ensuring system robustness through resilient component design, effective error handling, and robust data persistence mechanisms.
*   **Security:** Implementing security best practices across all layers, from data storage to tool execution and external API integrations.
*   **Maintainability:** Promoting clean code, clear documentation, and adherence to established development standards to facilitate long-term maintenance and evolution.
*   **Cloud-Native:** Leveraging managed services and serverless paradigms offered by Google Cloud Platform (GCP) for efficiency, reduced operational overhead, and automatic scaling.
*   **ADK-Centric:** Optimizing the architecture to fully leverage the capabilities and patterns provided by the Google Agent Development Kit for multi-agent orchestration and management.

**1.4. References**
*   `Software Requirements Specification (SRS) for Agent-Makalah` (`srs-agent-makalah`): Defines the functional and non-functional requirements.
*   `Technology Stack for Agent-Makalah` (`technology-stack-agent-makalah`): Specifies the chosen technologies and services.
*   `Google ADK Integration Strategy for Agent-Makalah` (`adk-integration-agent-makalah`): Details how `Agent-Makalah` integrates with Google ADK.
*   `Specification Document for the Agent-Makalah Multi-Agent Writing System` (`spec-agent-makalah-multi-agent`): Defines the multi-agent architecture and sub-agent roles.
*   `Standard Operating Procedures and Authorized Tools for Agent-Makalah` (`sop-tools-agent-makalah`): Provides detailed workflows and tool policies.
*   `Agent Memory and Session Management Policy for Agent-Makalah` (`memory-session-agent-makalah`): Details memory, session, and context management.

---

> Segment-ID: BAUM-HIGH-LEVEL-ARCH-002
> Source-File: backend-architecture-agent-makalah
> Parent-Anchor: baum-root
> Context: Provides a conceptual high-level view of Agent-Makalah's backend architecture, detailing main layers and data flows.

## 2. High-Level Architecture View {#baum-high-level-arch}

The `Agent-Makalah` backend architecture is structured into several logical layers, designed to separate concerns, enable scalability, and optimize for the multi-agent paradigm facilitated by Google ADK. At its core, it's a cloud-native, API-driven system.

**2.1. Main Architectural Layers:**

*   **Client Interface Layer:** This is the user-facing component, typically a web-based conversational user interface (UI) or a client application, through which users interact with `Agent-Makalah`. It sends user requests to the backend and displays agent responses.
*   **API Gateway / Backend Application Layer (FastAPI):** This layer acts as the entry point for all client requests. It's built using FastAPI and is responsible for:
    *   Receiving user requests from the Client Interface.
    *   Authentication and basic request validation (MVP).
    *   Routing requests to the appropriate ADK Agent in the layer below.
    *   Managing ADK Sessions for user interactions.
    *   Serving as a proxy between the Client Interface and the ADK Agent Layer.
*   **ADK Agent Layer:** This is the core intelligence and orchestration layer, where all `Agent-Makalah`'s functional logic resides. It consists of:
    *   The `Orchestrator_Agent`: The central controller managing overall workflows and coordinating sub-agents.
    *   Specialized Sub-Agents: `Brainstorming_Agent`, `Literature_Search_Agent`, `Outline_Draft_Agent`, `Writer_Agent`, `Analysis_Editor_Agent`, each performing distinct academic tasks.
    *   These agents are implemented using Google ADK and are deployed as scalable services (e.g., Cloud Run services).
*   **Data Persistence Layer:** This layer is responsible for storing all static and dynamic data required by the system. It includes:
    *   **Relational Database (PostgreSQL/Supabase):** For conversation history, session states, and metadata about artifacts.
    *   **Object Storage (Google Cloud Storage):** For temporary storage of user-uploaded files.
    *   **Caching Layer (Redis/Upstash):** For high-speed temporary data access.
*   **External Services Layer:** This layer represents external APIs and services that `Agent-Makalah` integrates with for specialized functionalities not handled internally. It includes:
    *   Large Language Model (LLM) APIs (Gemini, OpenAI).
    *   Web Search APIs (Serper, Google Search).
*   **Logging & Monitoring Infrastructure:** This cross-cutting layer captures operational metrics, application logs, and error traces from all other layers, enabling observability and troubleshooting.

**2.2. Main Data Flows (High-Level):**

1.  **User Request Flow:** User request (Client) -> Backend API -> ADK Agent Layer (`Orchestrator_Agent`).
2.  **Internal Workflow Delegation:** `Orchestrator_Agent` (ADK Agent Layer) -> Sub-Agents (ADK Agent Layer) via ADK's inter-agent communication. Data passed via `session.state`.
3.  **LLM Interaction:** ADK Agent Layer (Sub-Agents) -> External Services Layer (LLM APIs) -> ADK Agent Layer.
4.  **Tool Interaction:** ADK Agent Layer (Sub-Agents) -> External Services Layer (Web Search APIs) OR Data Persistence Layer (Object Storage for files) OR Internal Tool Services (e.g., `tool-makalah-kb-accessor`, `tool-makalah-python-interpreter` if deployed as separate services).
5.  **Data Persistence:** ADK Agent Layer / Backend API -> Data Persistence Layer (Database, Object Storage, Cache).
6.  **Response Flow:** ADK Agent Layer (`Orchestrator_Agent`) -> Backend API -> Client Interface Layer.
7.  **Observability Data:** All layers -> Logging & Monitoring Infrastructure.

This high-level view provides a conceptual understanding of how the different components of `Agent-Makalah` interact to deliver the system's functionalities. More detailed architectural specifics are provided in Section 3.

---

> Segment-ID: BAUM-DETAILED-COMPONENTS-003
> Source-File: backend-architecture-agent-makalah
> Parent-Anchor: baum-root
> Context: Provides detailed specifications for each major component within Agent-Makalah's backend architecture.

## 3. Detailed Component Architecture {#baum-detailed-components}

This section elaborates on the design and responsibilities of each primary component within the `Agent-Makalah` backend architecture, detailing their roles, technologies, and interactions.

### 3.1. Client-Side Interface {#baum-client-interface}

*   **Description:** The Client-Side Interface is the user-facing application that provides the conversational interaction experience for `Agent-Makalah`. It is typically a web-based UI or a client application.
*   **Technology Stack:** Standard web technologies (e.g., HTML, CSS, JavaScript framework like React/Vue/Angular, or a simpler frontend if chosen for MVP) will be used. (Not within the direct scope of backend development, but vital for context.)
*   **Responsibilities:**
    *   Presenting the conversational chat interface to the user.
    *   Capturing user text inputs and uploading file inputs.
    *   Displaying `Agent-Makalah`'s text responses, structured outputs (e.g., formatted reference lists, outlines), and interactive elements (e.g., validation prompts, revision options).
    *   Providing basic task progress indicators.
    *   Communicating with the Backend API Gateway via secure web protocols.
*   **Interaction:** Communicates with the Backend API Gateway using HTTP/S and WebSockets (for real-time chat updates).

### 3.2. Backend API Gateway & Core Application (FastAPI) {#baum-backend-api}

*   **Description:** This component serves as the primary entry point for all external communications to `Agent-Makalah`'s backend. It's a lightweight, high-performance web application built with FastAPI.
*   **Technology Stack:** FastAPI (Python), deployed as a containerized service (Docker) on Google Cloud Run.
*   **Responsibilities:**
    *   **API Gateway:**
        *   Receiving all incoming requests from the Client-Side Interface (user messages, file uploads, validation responses).
        *   Routing requests to the appropriate internal services, primarily the ADK Agent Layer.
        *   Handling rate limiting and basic request validation (e.g., API key presence for MVP).
    *   **Session Management:**
        *   Initiating and managing ADK `Session` lifecycles for each user interaction.
        *   Maintaining the link between the user's client session and the active ADK `Session`.
    *   **Request Pre-processing:**
        *   Performing initial parsing and validation of user inputs before forwarding to the ADK Agent Layer.
        *   Handling file upload streams and securely storing them to Google Cloud Storage (GCS), then passing the GCS reference to the ADK Agent Layer.
    *   **Response Handling:**
        *   Receiving responses and final outputs from the ADK Agent Layer (specifically the `Orchestrator_Agent`).
        *   Formatting responses for client consumption (e.g., converting structured agent output to a displayable JSON format).
        *   Sending responses back to the Client-Side Interface.
    *   **Error Handling:**
        *   Catching and logging API-level errors.
        *   Proxying errors reported by the ADK Agent Layer to the client.
*   **Key API Endpoints (Conceptual):**
    *   `POST /chat`: For submitting user messages and receiving agent responses.
    *   `POST /upload_file`: For users to upload documents for analysis.
    *   `GET /session_status`: (Optional) To query the status of an ongoing session.
*   **Interaction:**
    *   Receives requests from Client-Side Interface (HTTPS/WebSockets).
    *   Communicates with the ADK Agent Layer (potentially via internal HTTP calls if ADK Agents are separate Cloud Run services, or direct function calls if co-located).
    *   Interacts with Data Persistence Layer (PostgreSQL, GCS, Redis) for session state and data storage.
    *   Sends responses back to Client-Side Interface.
    *   **Scalability:** Leverages Cloud Run's auto-scaling capabilities to handle varying loads.

---

> Segment-ID: BAUM-ADK-LAYER-003-3
> Source-File: backend-architecture-agent-makalah
> Parent-Anchor: baum-detailed-components
> Context: Details the core ADK Agent Layer, where Agent-Makalah's multi-agent logic and orchestration reside.

### 3.3. ADK Agent Layer {#baum-adk-layer}

*   **Description:** This layer houses the entire multi-agent system of `Agent-Makalah`, built using the Google Agent Development Kit (ADK). It orchestrates the complex workflows, manages state, and interacts with external services (LLMs, web search) and data persistence.
*   **Technology Stack:** Google ADK (Python), Python 3.9+, deployed as containerized services (Docker) on Google Cloud Run.
*   **Responsibilities (Overall):**
    *   Executing `Agent-Makalah`'s core functional logic.
    *   Coordinating tasks among specialized sub-agents.
    *   Managing session state and context using ADK's native features.
    *   Integrating with external LLM APIs and other tools.
    *   Handling internal error propagation and coordination.

**3.3.1. `Orchestrator_Agent` Deployment & Role** {#baum-adk-orchestrator-deployment}
    *   **Description:** The `Orchestrator_Agent` serves as the central control and communication hub for the entire `Agent-Makalah` system. It's the primary ADK Agent responsible for directing the workflow based on user intent and managing sub-agent interactions.
    *   **Deployment Model:** Deployed as a dedicated Cloud Run service (or potentially as the main ADK application entry point if other sub-agents are called internally within the same ADK runtime instance).
    *   **Responsibilities:** As detailed in `spec-agent-makalah-multi-agent` (`Orchestrator_Agent` section) and `sop-tools-agent-makalah` (`SOP-AM-001`, `SOP-AM-002`, `SOP-AM-003`, `SOP-AM-004`, `SOP-AM-005` orchestration steps).
    *   **Interaction:** Receives requests from the Backend API Gateway. Calls and receives responses from other sub-agents. Interacts with the Data Persistence Layer.

**3.3.2. Sub-Agents Deployment & Roles** {#baum-adk-sub-agents-deployment}
    *   **Description:** This includes the specialized `Brainstorming_Agent`, `Literature_Search_Agent`, `Outline_Draft_Agent`, `Writer_Agent`, and `Analysis_Editor_Agent`. Each is designed to perform a distinct, focused task within the overall workflow.
    *   **Deployment Model:**
        *   **Option A (Separate Cloud Run Services):** Each sub-agent is deployed as its own distinct Cloud Run service. This provides maximum isolation and independent scalability.
        *   **Option B (Co-located within `Orchestrator_Agent`'s Runtime):** Sub-agents' ADK `Agent` implementations are part of the `Orchestrator_Agent`'s Cloud Run service. `Orchestrator_Agent` invokes them as internal components/functions. This might simplify initial deployment but ties their scaling to the `Orchestrator_Agent`.
        *   **Recommendation for MVP:** Option B is simpler for initial deployment and MVP, especially if inter-agent communication overhead is minimal. Option A can be a future enhancement for larger scale or strict microservices adherence.
    *   **Responsibilities:** As detailed in `spec-agent-makalah-multi-agent` for each respective sub-agent.
    *   **Interaction:** Primarily interacts with the `Orchestrator_Agent` (receiving commands, returning outputs) and external services/tools (LLMs, search APIs, file storage).

**3.3.3. Inter-Agent Communication within ADK** {#baum-adk-inter-agent-comm}
    *   **Mechanism:** Communication relies heavily on the ADK's `session.state` object for explicit data passing and direct method invocation (or ADK's agent-calling patterns).
    *   **Data Flow:**
        *   **`Orchestrator_Agent` to Sub-Agent (Task Brief):** `Orchestrator_Agent` writes task inputs (Task Brief, relevant artifacts, context subset) to specific `session.state` keys. It then invokes the sub-agent.
        *   **Sub-Agent to `Orchestrator_Agent` (Task Output):** Upon completion, the sub-agent writes its output to a designated `session.state` key and returns a completion signal.
    *   **Payload Format:** Data payloads in `session.state` are structured and JSON-serializable (e.g., Python dictionaries, lists of dictionaries) to ensure interoperability.
    *   **Reference:** `adk-integration-agent-makalah#aim-inter-agent-comm` for conceptual details.

**3.3.4. ADK Workflow Management** {#baum-adk-workflow-mgmt}
    *   **Mechanism:** The `Orchestrator_Agent` will manage the sequential workflows (e.g., New Paper Creation, Existing Paper Analysis) using a hybrid approach within ADK.
        *   The main orchestration logic (user interaction, validation loops, branching) resides within the `Orchestrator_Agent`'s custom Python code (as a `CustomAgent`).
        *   It then programmatically calls specific sub-agents as needed.
        *   ADK's `WorkflowAgent`s (e.g., `SequentialAgent`) *could* be used for managing simpler, internal sequences *within* a sub-agent's local execution logic, but the top-level orchestration remains with `Orchestrator_Agent`.
    *   **Responsibility:** The `Orchestrator_Agent` is responsible for updating `session.state` to reflect workflow progress, manage revision iterations, and track the current step within the active SOP.
    *   **Reference:** `adk-integration-agent-makalah#aim-workflow-orchestration` for conceptual details.

---

> Segment-ID: BAUM-DATA-PERSISTENCE-003-4
> Source-File: backend-architecture-agent-makalah
> Parent-Anchor: baum-detailed-components
> Context: Details the architecture of Agent-Makalah's data persistence layer, including database, caching, and object storage.

### 3.4. Data Persistence Layer {#baum-data-persistence}

*   **Description:** This layer is responsible for the reliable, persistent storage and retrieval of all data required by the `Agent-Makalah` system. It supports conversation history, session state, intermediate artifacts, user-uploaded files, and operational metadata. It adheres to the data persistence strategy outlined in `memory-session-agent-makalah#msam-persistence-strategy`.
*   **Technology Stack:** PostgreSQL (via Supabase), Redis (via Upstash), Google Cloud Storage (GCS).

**3.4.1. PostgreSQL Database (Supabase)** {#baum-postgresql-db}
    *   **Purpose:** The primary relational database for structured, long-term persistent data.
    *   **Managed Service:** Supabase is utilized as the managed PostgreSQL provider, simplifying database administration and scaling.
    *   **Key Data Stored:**
        *   **Conversation History:** Full dialogue turns between users and `Orchestrator_Agent`, including timestamps, speaker, raw inputs, and outputs.
        *   **Session Metadata:** Unique Session IDs, session initiation/termination timestamps, associated user IDs.
        *   **Agent State (Persisted):** High-level `Orchestrator_Agent` state information, overall SOP progress, and status of major workflow steps (e.g., "Topic Finalized," "References Validated"). This is a durable copy of critical ADK `session.state` elements.
        *   **Intermediate Artifact Metadata:** References to or metadata about stored intermediate artifacts (e.g., GCS path for a validated outline, ID for a record in a separate artifacts table).
        *   **Uploaded File Metadata:** Details of user-uploaded files (filename, type, size, GCS path).
    *   **Schema Design (Conceptual):** Will include tables for `conversations`, `sessions`, `workflow_progress`, `artifacts_metadata`, `uploaded_files`. Relationships will be defined to link these tables by Session ID and User ID.
    *   **Interaction:** Accessed by the Backend API Gateway (FastAPI) for storing and retrieving session and conversation-related data.

**3.4.2. Redis Cache (Upstash)** {#baum-redis-cache}
    *   **Purpose:** Serves as a high-speed, in-memory data store for caching ephemeral or frequently accessed data to improve performance and responsiveness.
    *   **Managed Service:** Upstash provides a serverless Redis instance, offering scalability and ease of management.
    *   **Key Data Stored (Ephemeral/Cached):**
        *   **Short-Term Session Data:** Rapidly changing session data that doesn't require immediate strong durability (e.g., current revision attempt counter for an active loop within a very short timeframe).
        *   **Rate Limiting Counters:** For managing API call rates to external services.
        *   **Cached LLM Responses:** Potentially, for common or reusable LLM responses that are not persona-sensitive, to reduce LLM API calls and latency (if permissible by policy).
    *   **Interaction:** Accessed by the Backend API Gateway (FastAPI) and potentially directly by ADK Agents for caching operations.

**3.4.3. Object Storage (Google Cloud Storage)** {#baum-object-storage}
    *   **Purpose:** For secure, scalable, and cost-effective storage of large binary objects, specifically user-uploaded academic paper files.
    *   **Service:** Google Cloud Storage (GCS) provides highly durable and available object storage.
    *   **Key Data Stored:**
        *   **User-Uploaded Files:** The original files (PDF, DOCX, TXT) uploaded by users for analysis. These files are typically processed by the `Analysis_Editor_Agent` via `tool-makalah-browse-files`.
        *   **Intermediate Large Artifacts (Optional):** Potentially, very large intermediate artifacts (e.g., a massive consolidated paper draft, detailed analysis reports) that might exceed ADK `session.state` size limits could be temporarily stored here, with their GCS reference stored in PostgreSQL.
    *   **Lifecycle Management:** GCS lifecycle policies will be configured to manage retention (e.g., auto-delete after 24 hours for user-uploaded files, as per `memory-session-agent-makalah`'s data retention policies).
    *   **Interaction:** Uploaded by the Backend API Gateway (FastAPI). Accessed by ADK Agents (via tools like `tool-makalah-browse-files`).

---

> Segment-ID: BAUM-EXTERNAL-SERVICES-003-5
> Source-File: backend-architecture-agent-makalah
> Parent-Anchor: baum-detailed-components
> Context: Details the architecture for integrating Agent-Makalah with external services, including LLM providers and search APIs.

### 3.5. External Service Integrations {#baum-external-integrations}

*   **Description:** This component represents the integration points and mechanisms through which `Agent-Makalah` interacts with third-party external services. These services provide core functionalities (like advanced AI reasoning and comprehensive web search) that are critical to the system but not hosted within `Agent-Makalah`'s direct purview.
*   **Technology Stack:** Python HTTP client libraries (e.g., `httpx`, `requests`), ADK's built-in tool integration, specific service client SDKs.

**3.5.1. Large Language Model (LLM) Providers** {#baum-llm-providers}
    *   **Providers:** Google Gemini API (Primary), OpenAI API (Fallback/Alternative). Specific model versions (e.g., Gemini 1.5 Pro) will be utilized. Access might be mediated through API gateways like OpenRouter for flexibility.
    *   **Integration Point:** Primarily accessed by the LLM-powered ADK Agents (`Orchestrator_Agent`, `Brainstorming_Agent`, `Writer_Agent`, `Analysis_Editor_Agent`) through ADK's native `LlmAgent` constructs. The Backend API Gateway does not directly call LLM APIs for core processing.
    *   **Mechanism:** Agents send structured prompts (text, sometimes structured JSON for function calls) to the LLM APIs and receive JSON responses containing generated text or structured data.
    *   **Security:** API keys and credentials for LLM providers will be managed securely using a secrets management service (e.g., Google Secret Manager) and never hardcoded or exposed in public repositories.
    *   **Error Handling:** Implement retry mechanisms for transient LLM API errors. Handle specific error codes (e.g., rate limits, invalid requests) according to defined fallback policies.

**3.5.2. Web Search API** {#baum-web-search-api}
    *   **Providers:** Serper API (Primary), Google Search API (Alternative/Fallback).
    *   **Integration Point:** Accessed by `Literature_Search_Agent` and `Brainstorming_Agent` (for specific purposes) via the `tool-makalah-web-search` custom ADK tool.
    *   **Mechanism:** The `tool-makalah-web-search` (as a Python function registered in ADK) will make HTTP requests to the chosen Web Search API with formulated queries.
    *   **Security:** API keys for search providers will be securely managed. All search queries will be sanitized and comply with usage policies.
    *   **Error Handling:** Handle rate limits, API failures, and empty results.

**3.5.3. Custom Tool Services (Internal or External)** {#baum-custom-tools}
    *   **Description:** This category includes tools like `tool-makalah-kb-accessor`, `tool-makalah-browse-files`, and `tool-makalah-python-interpreter`. Their "external" nature here depends on their deployment model.
    *   **Deployment Models:**
        *   **Co-located/Internal:** If implemented as Python functions directly within the ADK Agent's codebase and deployed as part of the same Cloud Run service. Communication is direct function call.
        *   **Separate Microservice:** If a tool (e.g., a more complex `tool-makalah-python-interpreter` with a specialized execution environment, or a `tool-makalah-kb-accessor` that talks to a separate content store) is deployed as its own Cloud Run service. Communication would be via internal HTTP API calls.
    *   **Integration Point:** Accessed by various sub-agents via their respective custom ADK tool definitions.
    *   **Security:** Adherence to sandboxing for `tool-makalah-python-interpreter` and strict access controls for `tool-makalah-browse-files` is critical. Authentication/authorization may be required for calls to separate microservice tools.
    *   **Error Handling:** Tool-specific errors (e.g., sandbox violations, file access errors) are captured and reported back to the calling agent.

---

> Segment-ID: BAUM-LOGGING-MONITORING-003-6
> Source-File: backend-architecture-agent-makalah
> Parent-Anchor: baum-detailed-components
> Context: Details the architecture for logging and monitoring across Agent-Makalah components, utilizing GCP services for observability.

### 3.6. Logging & Monitoring Infrastructure {#baum-logging-monitoring}

*   **Description:** A robust logging and monitoring infrastructure is essential for the observability, operational health, and debugging of the `Agent-Makalah` system. This infrastructure will primarily leverage Google Cloud's native services.
*   **Technology Stack:** Google Cloud Logging, Google Cloud Monitoring.

**3.6.1. Logging (`Google Cloud Logging`)**
    *   **Purpose:** To collect, store, and manage all logs generated by `Agent-Makalah`'s components.
    *   **Mechanism:**
        *   Each `Agent-Makalah` component (FastAPI backend, `Orchestrator_Agent`, sub-agents, custom tool services) will be configured to output structured logs (e.g., JSON format) to standard output (stdout/stderr).
        *   Google Cloud Run automatically streams stdout/stderr to Google Cloud Logging.
        *   Logs will include timestamps, severity levels (INFO, WARNING, ERROR), component identifiers, session IDs, and relevant message payloads.
    *   **Key Logged Events:**
        *   All user inputs and `Orchestrator_Agent` outputs (for traceability).
        *   Inter-agent communication events (task delegation, output reception).
        *   Tool invocations, parameters, and results (success/failure).
        *   Error events (P-levels, V-Codes, stack traces if available).
        *   System and application-level events (e.g., service start/stop, configuration changes).
    *   **Log Retention:** Log retention policies will be configured in Cloud Logging (e.g., 30 days default, adjustable).

**3.6.2. Monitoring (`Google Cloud Monitoring`)**
    *   **Purpose:** To collect, analyze, and visualize operational metrics and health status of `Agent-Makalah`'s components.
    *   **Mechanism:**
        *   Cloud Run automatically provides basic metrics (e.g., request count, latency, CPU/memory utilization, error rates) to Google Cloud Monitoring.
        *   Custom metrics can be emitted by the application code (e.g., number of successful paper creations, average revision loops per paper, specific sub-agent task completion rates).
    *   **Key Monitored Metrics:**
        *   Service Availability (Uptime) for Backend API and ADK Agents.
        *   Request Latency for user interactions and inter-agent calls.
        *   Error Rates (HTTP errors, internal application errors, tool failures).
        *   Resource Utilization (CPU, Memory) per service.
        *   LLM API call rates and latency.
        *   Active user sessions.
    *   **Alerting:** Alerting policies will be configured in Cloud Monitoring to notify operations teams of critical issues (e.g., high error rates, service downtime, resource exhaustion).

**3.6.3. Tracing (Post-MVP Consideration)**
    *   **Purpose:** To provide end-to-end visibility of a single user request as it flows through multiple components and agents, aiding in debugging complex distributed issues.
    *   **Mechanism:** Future integration with distributed tracing solutions (e.g., Google Cloud Trace, OpenTelemetry) will be explored for post-MVP.

---

> Segment-ID: BAUM-DATA-FLOW-004
> Source-File: backend-architecture-agent-makalah
> Parent-Anchor: baum-root
> Context: Describes the primary data flows within Agent-Makalah's backend architecture, detailing information movement between components.

## 4. Data Flow Diagrams (Textual Description) {#baum-data-flow}

This section describes the key data flows within the `Agent-Makalah` system, illustrating how information moves between the architectural components. This serves as a textual representation of what would typically be depicted in Data Flow Diagrams (DFD) or sequence diagrams.

**4.1. User Request & Response Flow**

This flow describes the journey of a user's initial request into the system and the eventual delivery of the `Agent-Makalah`'s response.
1.  **User Initiates Request:** User inputs a query (text/file) via the Client Interface.
2.  **Request to Backend API:** Client Interface sends the request (HTTP/S, WebSockets) to the Backend API Gateway (FastAPI).
3.  **Backend API Pre-processing & Session Management:**
    *   FastAPI endpoint receives request, performs initial validation.
    *   Initiates/retrieves ADK `Session` for the user.
    *   If file upload: FastAPI stores file to Google Cloud Storage (GCS) and obtains a reference.
4.  **Backend API to ADK Agent Layer:** FastAPI invokes the `Orchestrator_Agent` (an ADK `Agent`), passing the user's request (text/file reference) and relevant session state (via ADK `session.state`).
5.  **ADK Agent Layer Processing (`Orchestrator_Agent`):**
    *   `Orchestrator_Agent` receives the request.
    *   Clarifies user intent (possibly involving `SOP-AM-003` dialogue loop with user via FastAPI).
    *   Orchestrates the main workflow (`SOP-AM-001` or `SOP-AM-002`) by calling various sub-agents.
    *   Manages user validation loops (`SOP-AM-005` dialogue with user via FastAPI).
6.  **Sub-Agent Execution & Interaction:**
    *   `Orchestrator_Agent` writes task-specific inputs to ADK `session.state` (e.g., topic for `Brainstorming_Agent`, outline for `Writer_Agent`).
    *   `Orchestrator_Agent` calls the relevant sub-agent (e.g., `Brainstorming_Agent`, `Literature_Search_Agent`, `Outline_Draft_Agent`, `Writer_Agent`, `Analysis_Editor_Agent`).
    *   Sub-agent performs its task (e.g., calls LLM API, Web Search API, accesses GCS via `tool-makalah-browse-files`, uses `tool-makalah-python-interpreter`).
    *   Sub-agent writes its output (e.g., topic options, reference list, drafted section, analysis report) back to ADK `session.state`.
    *   Sub-agent signals completion to `Orchestrator_Agent`.
7.  **Data Persistence:** Throughout Step 5 & 6, `Orchestrator_Agent` and sub-agents read from/write to Data Persistence Layer (PostgreSQL for structured data, Redis for cache, GCS for files) via FastAPI or directly through ADK's storage integrations.
8.  **Error Handling & Logging:** Errors detected at any layer (sub-agent, tool, FastAPI) are propagated to `Orchestrator_Agent`. `Orchestrator_Agent` logs the error and initiates fallback (potentially involving user interaction via FastAPI). All key interactions and errors are logged to Google Cloud Logging.
9.  **Response Generation (`Orchestrator_Agent`):** `Orchestrator_Agent` assembles the final response (e.g., complete paper, analysis report) or specific dialogue turn.
10. **Response to Backend API:** `Orchestrator_Agent` returns the response to the Backend API Gateway.
11. **Backend API to Client:** FastAPI formats the response and sends it back to the Client Interface.
12. **Client Displays Response:** Client Interface displays the response to the user.

**4.2. New Paper Creation Workflow Data Flow (Illustrative)**

This flow specifically illustrates the core data movement for creating a new paper, building upon the `sop-tools-agent-makalah#sop-am-001-root`.

*   **User -> `Orchestrator_Agent`:** Initial request, intent clarifications, topic validations, reference validations, outline validations, section draft validations.
*   **`Orchestrator_Agent` -> `Brainstorming_Agent`:** Initial topic idea, user feedback for refinement.
*   **`Brainstorming_Agent` -> Web Search API (via `tool-makalah-web-search`):** Search queries for inspiration.
*   **Web Search API -> `Brainstorming_Agent`:** Raw search results.
*   **`Orchestrator_Agent` -> `Literature_Search_Agent`:** Definitive topic, search command.
*   **`Literature_Search_Agent` -> Web Search API (via `tool-makalah-web-search`):** Academic search queries.
*   **Web Search API -> `Literature_Search_Agent`:** Raw search results.
*   **`Literature_Search_Agent` -> `Orchestrator_Agent`:** Structured, validated reference list.
*   **`Orchestrator_Agent` -> `Outline_Draft_Agent`:** Definitive topic, validated references, outline creation command.
*   **`Outline_Draft_Agent` -> `Orchestrator_Agent`:** Structured outline, draft key points, reference mapping.
*   **`Orchestrator_Agent` -> `Writer_Agent`:** Outline section, draft key points, relevant references, reference mapping, writing command.
*   **`Writer_Agent` -> `Orchestrator_Agent`:** Drafted paper section, bibliography data for section.
*   **All Agents <-> Data Persistence Layer:** Read/write state, artifacts, history (PostgreSQL, GCS, Redis).
*   **All Agents -> Logging/Monitoring:** Send logs and metrics.

**4.3. Existing Paper Analysis Workflow Data Flow (Illustrative)**

This flow illustrates the core data movement for analyzing an existing paper, building upon the `sop-tools-agent-makalah#sop-am-002-root`.

*   **User -> `Orchestrator_Agent`:** Uploaded paper file, analysis request, analysis criteria.
*   **`Orchestrator_Agent` -> GCS:** Uploaded file stored.
*   **`Orchestrator_Agent` -> `Analysis_Editor_Agent`:** File reference (from GCS), analysis criteria, analysis command.
*   **`Analysis_Editor_Agent` -> GCS (via `tool-makalah-browse-files`):** Read uploaded file content.
*   **`Analysis_Editor_Agent` -> LLM API:** Text content for analysis.
*   **`Analysis_Editor_Agent` -> `tool-makalah-python-interpreter`:** Python script/data for complex analysis (optional).
*   **`Analysis_Editor_Agent` -> `Orchestrator_Agent`:** Structured analysis report/feedback.
*   **`Orchestrator_Agent` -> User:** Analysis report presented.

---

> Segment-ID: BAUM-SECURITY-ARCH-005
> Source-File: backend-architecture-agent-makalah
> Parent-Anchor: baum-root
> Context: Details the security architecture considerations for Agent-Makalah's backend, covering data protection, access control, and secure operations.

## 5. Security Architecture Considerations {#baum-security-arch}

Security is a paramount concern in the design and implementation of `Agent-Makalah`, particularly given its handling of user data, academic content, and interactions with external services. This section outlines key security considerations at the architectural level, building upon the high-level requirements in `srs-agent-makalah#srs-nfr-security`.

**5.1. Data Protection at Rest and in Transit**

*   **Data Encryption at Rest:**
    *   **Requirement:** All sensitive data persisted in the Data Persistence Layer (PostgreSQL database for conversation history, session state, artifact metadata; Google Cloud Storage for uploaded files) SHALL be encrypted at rest.
    *   **Mechanism:** Leverage native encryption capabilities provided by managed cloud services (e.g., GCP's default encryption for Cloud SQL/PostgreSQL and GCS, Supabase's encryption).
*   **Data Encryption in Transit:**
    *   **Requirement:** All data transmitted between `Agent-Makalah`'s components (Client-Backend API, Backend API-ADK Agent Layer, ADK Agents-Data Persistence Layer, ADK Agents-External Services) SHALL be encrypted.
    *   **Mechanism:** Enforce TLS 1.2 or higher for all HTTP/S and WebSockets communication. Utilize secure internal channels provided by GCP for inter-service communication (e.g., private IP, VPC network for Cloud Run).

**5.2. Authentication and Authorization**

*   **API Gateway Authentication (Basic for MVP):**
    *   **Requirement:** The Backend API Gateway (FastAPI) SHALL implement basic authentication for controlling access from the Client Interface (e.g., API keys, simple token validation) for MVP.
    *   **Mechanism:** API keys or static tokens managed securely.
*   **Internal Service Authorization:**
    *   **Requirement:** Calls between Backend API Gateway and ADK Agent Layer, and between ADK Agents and Custom Tool Services (if deployed separately), SHALL be authorized.
    *   **Mechanism:** Leverage GCP's Identity and Access Management (IAM) for service accounts (e.g., Cloud Run service identities with specific IAM roles) to control inter-service communication.
*   **Data Access Control:**
    *   **Requirement:** Access to the PostgreSQL database, Redis, and GCS SHALL be restricted to authorized `Agent-Makalah` services only.
    *   **Mechanism:** Utilize database user roles, strong passwords (managed by secrets manager), network firewalls, and GCS bucket IAM policies.

**5.3. Tool Sandboxing & Access Control**

*   **`tool-makalah-python-interpreter` Sandboxing:**
    *   **Requirement:** The Python execution environment SHALL be strictly sandboxed, preventing unauthorized system calls, network access, and arbitrary file system operations.
    *   **Mechanism:** Configure ADK's `CodeExecutionTool` or implement a custom isolated execution environment (e.g., Docker container with strict security policies, gVisor if using GKE for advanced sandboxing).
*   **`tool-makalah-browse-files` Access Restrictions:**
    *   **Requirement:** This tool SHALL only have read-only access to user-uploaded files within a highly restricted, temporary storage location (e.g., a specific GCS bucket directory for current session uploads).
    *   **Mechanism:** Implement strict IAM policies on the GCS bucket for uploaded files, and enforce path validation at the tool's implementation layer.
*   **`tool-makalah-web-search` Domain Filtering:**
    *   **Requirement:** The `tool-makalah-web-search` SHALL enforce strict whitelisting of authorized academic domains/databases and implement filtering for potentially malicious URLs.
    *   **Mechanism:** Implement a configurable list of allowed domains.
*   **Secrets Management:**
    *   **Requirement:** All sensitive credentials (e.g., LLM API keys, database passwords, external service API keys) SHALL be stored and accessed securely.
    *   **Mechanism:** Utilize Google Secret Manager for centralized and encrypted storage of secrets. Applications will retrieve secrets at runtime via IAM-controlled access.

**5.4. Secure Coding Practices & Input Validation**

*   **Requirement:** All `Agent-Makalah` components SHALL adhere to secure coding practices (e.g., OWASP Top 10 mitigation).
*   **Mechanism:** Implement comprehensive input validation and sanitization at all entry points (Backend API, internal ADK Agent inputs, tool inputs) to prevent injection attacks and other vulnerabilities. This aligns with `srs-agent-makalah#srs-nfr-security`.

**5.5. Logging, Monitoring, and Auditing**

*   **Requirement:** Comprehensive, immutable logs of all security-relevant events (e.g., authentication attempts, unauthorized access attempts, tool invocations, critical errors) SHALL be collected.
*   **Mechanism:** Leverage Google Cloud Logging for centralized log collection. Implement alerts in Google Cloud Monitoring for suspicious activities or security policy violations. Regular log reviews will be conducted.

---

> Segment-ID: BAUM-SCALABILITY-RELIABILITY-006
> Source-File: backend-architecture-agent-makalah
> Parent-Anchor: baum-root
> Context: Discusses architectural considerations for ensuring Agent-Makalah's scalability and reliability, leveraging cloud-native features.

## 6. Scalability & Reliability Considerations {#baum-scalability-reliability}

The architecture of `Agent-Makalah` is designed to be inherently scalable and highly reliable, leveraging cloud-native patterns and managed services on Google Cloud Platform (GCP). This is critical for supporting the initial target of 1,000 users and ensuring a stable, performant experience.

**6.1. Scalability Considerations**

*   **Horizontal Scaling for Compute Services:**
    *   **Mechanism:** Core compute components (Backend API Gateway/FastAPI, `Orchestrator_Agent`, and individual sub-agents if deployed as separate Cloud Run services) are deployed on Google Cloud Run. Cloud Run provides automatic horizontal scaling based on request load, scaling instances up or down (even to zero) as needed.
    *   **Benefit:** This ensures that the system can handle varying user loads efficiently without manual intervention, optimizing cost for fluctuating traffic.
*   **Stateless or Near-Stateless Services:**
    *   **Mechanism:** Backend API Gateway and individual ADK Agents (especially if deployed as separate Cloud Run services) are designed to be largely stateless or near-stateless. Critical session state is externalized to the Data Persistence Layer (PostgreSQL, Redis).
    *   **Benefit:** Enables easy horizontal scaling of compute services as instances can be added or removed without concern for local state.
*   **Database Scalability:**
    *   **Mechanism:** PostgreSQL database is provided via Supabase, a managed service designed for scalability. Redis caching via Upstash also offers inherent scalability.
    *   **Benefit:** These managed services handle database scaling, backups, and replication, reducing operational overhead and supporting increased data loads.
*   **LLM Provider Scalability:**
    *   **Mechanism:** Reliance on highly scalable external LLM APIs (Google Gemini API, OpenAI API) which are designed for high throughput.
    *   **Benefit:** Ensures that the core AI capabilities can meet demand as user traffic grows.

**6.2. Reliability Considerations**

*   **Managed Services:**
    *   **Mechanism:** Extensive use of GCP's managed services (Cloud Run, Cloud Storage, Cloud SQL, Cloud Monitoring, Cloud Logging) reduces operational complexity and leverages Google's built-in reliability, redundancy, and disaster recovery capabilities.
    *   **Benefit:** Higher availability and reduced mean time to recovery (MTTR) compared to self-managed infrastructure.
*   **Redundancy and High Availability:**
    *   **Mechanism:** Cloud Run services inherently offer high availability by distributing instances across multiple zones. PostgreSQL (Supabase) and GCS provide built-in data redundancy and replication.
    *   **Benefit:** Protects against single points of failure at the infrastructure level.
*   **Robust Error Handling & Fallbacks:**
    *   **Mechanism:** The multi-agent architecture incorporates a comprehensive error handling strategy (`sop-tools-agent-makalah#sop-am-004-root`), ensuring graceful degradation, recovery attempts, and clear communication to the user during failures.
    *   **Benefit:** Improves user experience by preventing abrupt crashes and guiding users through issues.
*   **Monitoring and Alerting:**
    *   **Mechanism:** Integrated monitoring and logging (Google Cloud Monitoring, Google Cloud Logging) provide real-time visibility into system health, performance bottlenecks, and errors. Proactive alerts notify operations teams of critical issues.
    *   **Benefit:** Enables rapid detection and resolution of operational problems, minimizing downtime.
*   **Idempotent Operations (Where Applicable):**
    *   **Mechanism:** Design critical API endpoints and internal agent operations to be idempotent where feasible. This ensures that repeated requests (e.g., due to network retries) do not result in unintended side effects.
    *   **Benefit:** Improves reliability in distributed systems.

---

> Segment-ID: MCASG-LITREVIEW-STYLE
> Source-File: makalah-academic-style-guides.txt
> Parent-Anchor: {#makalah-academic-style-guides-root}

## Literature Review Writing Style {#makalah-style-litreview-definition}

This section serves as the final document defining the specific style guide for the literature review. Its purpose is to produce literature review text that is thematic, critical, and reinforces the research gap. Agents are required to adhere to these rules. This section links to the root document (`makalah-academic-style-guides#makalah-academic-style-guides-root`), the core academic style definition (`makalah-academic-style-guides#makalah-style-core-definition`), and the introduction style definition (`makalah-academic-style-guides#makalah-style-intro-definition`).

---

> Segment-ID: MCASG-LITREVIEW-STYLE-STRUCTURE
> Source-File: makalah-academic-style-guides.txt
> Parent-Anchor: {#makalah-style-litreview-definition}

### 1. Literature Review Structure: Thematic Focus {#litreview-structure-thematic}

All rules from the Core Academic Writing Style (`makalah-academic-style-guides#makalah-style-core-definition::core-academic-style-rules`) apply to the Literature Review section unless explicitly overridden here.

The literature review must be organized thematically, grouping sources based on related concepts, theories, or variables. A chronological structure is acceptable only if the historical development of the field is central to the argument. The organization must ensure a logical grouping of sources. The review should be structured logically, and subheadings should be used for major themes or variables if appropriate. Do not simply list summaries of papers one by one; instead, group and synthesize them. This segment adheres to compliant token usage and ensures resolvable anchor IDs. It links to the literature review structure (thematic focus) itself at `{#litreview-structure-thematic}`.

---

> Segment-ID: MCASG-LITREVIEW-STYLE-CONTENT
> Source-File: makalah-academic-style-guides.txt
> Parent-Anchor: {#makalah-style-litreview-definition}

### 2. Content Focus: Synthesis over Summary {#litreview-content-synthesis}

The primary goal is synthesis, not just summarizing individual studies. The literature review should not be an annotated bibliography. The generated text must:
*   Compare and contrast findings from different sources.
*   Identify patterns and trends in the literature.
*   Discuss relationships between studies.

Avoid treating each source in isolation; show how they relate to one another. This segment adheres to compliant token usage and ensures resolvable anchor IDs. It links to the literature review structure (thematic focus) at `{#litreview-structure-thematic}`.

---

> Segment-ID: MCASG-LITREVIEW-STYLE-CRITICAL
> Source-File: makalah-academic-style-guides.txt
> Parent-Anchor: {#makalah-style-litreview-definition}

### 3. Critical Analysis {#litreview-critical-analysis}

The review must include a critical analysis of the literature. Evaluate sources by commenting on:
*   Methodological strengths and weaknesses.
*   Key findings and their limitations.
*   Theoretical consistency or contradictions.

Do not simply accept findings at face value; engage critically with the material. This segment adheres to compliant token usage and ensures resolvable anchor IDs. It links to the content focus (synthesis over summary) at `{#litreview-content-synthesis}`.

---

> Segment-ID: MCASG-LITREVIEW-STYLE-GAP
> Source-File: makalah-academic-style-guides.txt
> Parent-Anchor: {#makalah-style-litreview-definition}

### 4. Research Gap Reinforcement {#litreview-gap-reinforcement}

The literature review must clearly lead back to and reinforce the research gap identified in the introduction (`makalah-academic-style-guides#intro-research-gap-focus`). Show how the discussed literature highlights or confirms this gap. Conclude with a clear transition explaining how the current study addresses the identified gap, thereby leading into the methodology section. This segment adheres to compliant token usage and ensures resolvable anchor IDs. It links to the introduction's research gap focus and the literature review style definition at `{#litreview-style-definition}`.

---

> Segment-ID: MCASG-LITREVIEW-STYLE-CITATION
> Source-File: makalah-academic-style-guides.txt
> Parent-Anchor: {#makalah-style-litreview-definition}

### 5. Citation Policy {#litreview-citation-policy}

All claims attributed to sources must be accurately and consistently cited in-text. Integrate citations smoothly into the text. The specific citation format will be handled by the bibliography formatting SOP (`makalah-task-sop#sop-makalah-bibliography-formatting`). Avoid over-reliance on single sources for any given point; synthesize from multiple sources where possible. This segment adheres to compliant token usage and ensures resolvable anchor IDs. It links to the literature review style definition at `{#litreview-style-definition}`.

---

> Segment-ID: MCASG-LITREVIEW-STYLE-FORBIDDEN
> Source-File: makalah-academic-style-guides.txt
> Parent-Anchor: {#makalah-style-litreview-definition}

### 6. Forbidden Elements in Literature Review {#litreview-forbidden-elements}

In addition to the core forbidden elements, the following are specifically forbidden within the Literature Review section:
*   Presenting your own research results (from the current study).
*   Detailed methodology of the current study.
*   Lengthy quotations (paraphrasing is preferred).

For a general list of forbidden words and phrases, refer to the core academic style rules: `makalah-academic-style-guides#core-academic-style-rules::forbidden-elements-core`. This segment adheres to compliant token usage and ensures resolvable anchor IDs. It links to the literature review style definition at `{#litreview-style-definition}`.

---

> Segment-ID: BAUM-DEPLOYMENT-STRAT-007
> Source-File: backend-architecture-agent-makalah
> Parent-Anchor: baum-root
> Context: Outlines the high-level strategy for deploying Agent-Makalah components to Google Cloud Platform.

## 7. Deployment Strategy (High-Level) {#baum-deployment-strategy}

The deployment strategy for `Agent-Makalah` will leverage automated Continuous Integration/Continuous Deployment (CI/CD) practices and cloud-native services offered by Google Cloud Platform (GCP). This ensures efficient, reliable, and consistent delivery of the system to production environments.

**7.1. Code Repository and Version Control:**
*   **Mechanism:** All source code, including FastAPI backend, ADK agent implementations, custom tools, and deployment configurations (e.g., Dockerfiles, Cloud Run YAMLs), will be stored in a centralized Git repository (e.g., GitHub).
*   **Practice:** Version control will strictly adhere to branching strategies (e.g., Git Flow or Trunk-Based Development) and pull request (PR) reviews to maintain code quality and collaboration.

**7.2. Continuous Integration (CI):**
*   **Mechanism:** A CI pipeline (e.g., GitHub Actions, Google Cloud Build) will be triggered automatically upon every code commit to the main branches (e.g., `main`, `develop`).
*   **Activities:** The CI pipeline will perform:
    *   Automated code builds (e.g., Python dependency installation, Docker image creation).
    *   Static code analysis (linters, security checks).
    *   Automated unit and integration tests for all components.
    *   Container image tagging and pushing to a container registry (e.g., Google Container Registry / Artifact Registry).
*   **Benefit:** Ensures code quality, identifies integration issues early, and produces ready-to-deploy artifacts.

**7.3. Continuous Deployment (CD):**
*   **Mechanism:** A CD pipeline will automatically or manually (for production releases) deploy the validated container images to GCP environments.
*   **Activities:**
    *   **Deployment to Staging/Testing:** Automated deployment to a staging environment for further testing (e.g., end-to-end tests, performance tests).
    *   **Deployment to Production:** Manual trigger or automated deployment to the production environment after successful staging tests.
    *   **Rollback Capability:** The deployment mechanism will support quick rollback to previous stable versions in case of critical issues post-deployment.
*   **Services:** Deployment targets will primarily be Google Cloud Run services for the FastAPI backend and individual ADK agents.

**7.4. Environment Management:**
*   **Mechanism:** Separate GCP projects or distinct configurations will be maintained for different environments (e.g., `development`, `staging`, `production`).
*   **Benefit:** Ensures isolation and prevents accidental changes in production.

**7.5. Monitoring and Alerting Post-Deployment:**
*   **Mechanism:** As detailed in Section 3.6, Google Cloud Monitoring and Cloud Logging will be fully utilized post-deployment for continuous operational visibility.
*   **Practice:** Dashboards will be set up to visualize key metrics, and alerts will be configured for critical events (e.g., high error rates, downtime, resource spikes).
*   **Benefit:** Enables proactive issue detection and rapid response.

---

> Segment-ID: BAUM-FUTURE-ARCH-ENHANCEMENTS-008
> Source-File: backend-architecture-agent-makalah
> Parent-Anchor: baum-root
> Context: Outlines potential future architectural enhancements for Agent-Makalah beyond the MVP.

## 8. Future Architectural Enhancements (Post-MVP) {#baum-future-enhancements}

The initial backend architecture for `Agent-Makalah` focuses on robustness and scalability for the MVP. However, the long-term vision includes several architectural enhancements to support increased complexity, higher scale, and new features (as outlined in `prd-agent-makalah#prd-future-considerations`).

**8.1. Microservices Decomposition & Granularization:**
*   **Enhancement:** Further decompose the ADK Agent Layer into more granular microservices. For instance, `Writer_Agent`'s various internal functions (e.g., citation integration, style correction) could become specialized microservices. Similarly, complex tools might evolve into dedicated services.
*   **Benefit:** Enhanced independent scalability, fault isolation, and specialized teams for highly specific components.

**8.2. Advanced Inter-Service Communication:**
*   **Enhancement:** Introduce robust asynchronous communication patterns between services.
*   **Mechanism:** Implement message queues or event streaming platforms (e.g., Google Cloud Pub/Sub, Apache Kafka) for decoupled communication between FastAPI backend, ADK Agents, and data processing pipelines.
*   **Benefit:** Improved responsiveness, resilience to transient failures, and scalability by processing tasks asynchronously.

**8.3. Knowledge Graph & Vector Database Integration:**
*   **Enhancement:** Implement a dedicated Knowledge Graph database and integrate it with a Vector Database.
*   **Mechanism:** Store rich, interconnected academic concepts, entities, and relationships in a graph database (e.g., Neo4j, ArangoDB). Store vector embeddings of academic content and KB snippets in a vector database (e.g., Pinecone, Weaviate, Milvus).
*   **Benefit:** Enables advanced semantic search, contextual understanding, and powers features like the Knowledge Graph Visualization (as per `prd-agent-makalah#prd-future-considerations`). This allows agents to reason over interconnected data more effectively.

**8.4. Real-time Data Processing & Analytics:**
*   **Enhancement:** Introduce real-time data processing capabilities for conversational analytics or immediate feedback loops.
*   **Mechanism:** Utilize stream processing technologies (e.g., Google Cloud Dataflow, Apache Flink) for analyzing live interaction data.
*   **Benefit:** Enables deeper insights into user behavior and potential for dynamic system adjustments.

**8.5. Enhanced Security & Compliance Features:**
*   **Enhancement:** Implement more sophisticated security controls like fine-grained access control policies for specific data attributes, advanced threat detection, and automated compliance auditing.
*   **Mechanism:** Integrate with specialized security services and tools (e.g., GCP Security Command Center).

**8.6. Hybrid Cloud/Multi-Cloud Strategy (If Needed):**
*   **Enhancement:** Explore deploying specific workloads or data to other cloud providers or on-premises environments.
*   **Benefit:** Diversifies infrastructure, potentially optimizes costs, or addresses specific regulatory requirements. (High complexity, usually for very large-scale systems).

This roadmap will be prioritized based on product evolution, user needs, and technological advancements post-MVP.

---

> Segment-ID: BAUM-REVISION-HIST-009
> Source-File: backend-architecture-agent-makalah
> Parent-Anchor: baum-root
> Context: Tracks the version history and changes made to this Backend Architecture Design document.

## 9. Revision History {#baum-revision-history}

| Version | Date       | Author(s)   | Summary of Changes                                                                        |
| :------ | :--------- | :---------- | :---------------------------------------------------------------------------------------- |
| 1.0     | 1 Jun 2025 | ERIK SUPIT  | Initial MVP draft of the Backend Architecture Design for `Agent-Makalah`, detailing components, data flows, security, scalability, and deployment strategy. |
|         |            |             |                                                                                           |
|         |            |             |                                                                                           |