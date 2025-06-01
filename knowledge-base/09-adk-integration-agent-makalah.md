UID: adk-integration-agent-makalah
Title: Google ADK Integration Strategy for Agent-Makalah
Author: "ERIK SUPIT"
Version: 1.0
Date: "1 Juni 2025"
Role: INTEGRATION-GUIDE
Status: DRAFT
Domain: AGENT-IMPLEMENTATION
Dependencies:
  - "spec-agent-makalah-multi-agent"
  - "sop-tools-agent-makalah"
  - "memory-session-agent-makalah" # Added dependency
  - "persona-prompt-agent-makalah" # Added dependency
  - "database-design-agent-makalah" # Added dependency
Anchors:
  - "aim-root"
  - "aim-introduction"
  - "aim-mapping-to-adk"
  - "aim-sub-agents-as-adk-agents"
  - "aim-orchestrator-as-controller"
  - "aim-workflow-orchestration"
  - "aim-sops-in-adk"
  - "aim-task-state-in-workflow"
  - "aim-tool-integration"
  - "aim-makalah-tools-in-adk"
  - "aim-tool-auth-invocation"
  - "aim-state-context-management"
  - "aim-adk-session-state"
  - "aim-passing-context-to-llms"
  - "aim-inter-agent-comm"
  - "aim-error-propagation"
  - "aim-deployment-considerations"
  - "aim-dev-debug-tools"
  - "aim-revision-history"
Tags:
  - "adk-integration"
  - "google-agent-development-kit"
  - "agent-makalah"
  - "multi-agent"
  - "implementation-guide"
  - "mvp"
Language: EN
Chained: true
---

---
> Segment-ID: AIM-INTRO-001
> Source-File: adk-integration-agent-makalah
> Parent-Anchor: aim-root
> Context: Introduces the purpose of this document: guiding the implementation of Agent-Makalah using Google ADK.

## 1. Introduction and Purpose {#aim-introduction}

This document outlines the technical strategy and approach for implementing the `Agent-Makalah` multi-agent system, as defined in `spec-agent-makalah-multi-agent`, using the Google Agent Development Kit (ADK). Its primary purpose is to provide guidance to the AI software development team on how to map the conceptual architecture and functionalities of `Agent-Makalah` and its sub-agents onto the constructs and features offered by the ADK.

The Google ADK has been selected as the target framework due to its robust support for building code-first, model-agnostic, and modular multi-agent systems. Its features for workflow orchestration, tool integration, state management, and inter-agent communication provide a solid foundation for realizing the `Agent-Makalah` vision.

The scope of this integration guide primarily covers the Minimum Viable Product (MVP) implementation of `Agent-Makalah`. It will detail how core components such as sub-agent definitions, Standard Operating Procedures (SOPs detailed in `sop-tools-agent-makalah`), tool usage, session management, and error handling will be realized within the ADK environment. While this document aims to be comprehensive for MVP needs, specific low-level implementation details and code will be further elaborated in subsequent technical design and development phases. This document assumes familiarity with both the `Agent-Makalah` specifications and the fundamental concepts of the Google ADK.

---

> Segment-ID: AIM-MAP-ADK-002
> Source-File: adk-integration-agent-makalah
> Parent-Anchor: aim-root
> Context: Details how Agent-Makalah's sub-agents and the orchestrator role are mapped to Google ADK's agent constructs.

## 2. Mapping `Agent-Makalah` Components to ADK Constructs {#aim-mapping-to-adk}

The multi-agent architecture of `Agent-Makalah`, as detailed in `spec-agent-makalah-multi-agent`, will be realized by mapping its core components onto the agent and control constructs provided by the Google Agent Development Kit (ADK).

**2.1. Sub-Agents as Distinct ADK `Agent`s** {#aim-sub-agents-as-adk-agents}

Each specialized sub-agent within the `Agent-Makalah` system will be implemented as a distinct, individual `Agent` construct within the ADK. This includes:
*   `Orchestrator_Agent`
*   `Brainstorming_Agent`
*   `Literature_Search_Agent`
*   `Outline_Draft_Agent`
*   `Writer_Agent`
*   `Analysis_Editor_Agent`

This one-to-one mapping offers several advantages:
*   **Modularity and Encapsulation:** Each ADK `Agent` will encapsulate the specific logic, functions, and potentially state of its corresponding `Agent-Makalah` sub-agent. This promotes clean separation of concerns.
*   **Independent Development & Testing:** Individual sub-agents (as ADK `Agent`s) can be developed, unit-tested, and versioned with greater independence.
*   **Reusability:** Specialized ADK `Agent`s, once developed, could potentially be reused in other multi-agent systems if their functions are generic enough (though `Agent-Makalah` sub-agents are fairly specialized).
*   **Clearer Orchestration:** The `Orchestrator_Agent` can manage interactions with other sub-agents by invoking them as distinct entities within the ADK environment.

The specific type of ADK `Agent` (e.g., `CustomAgent`, `LlmAgent`) used for each sub-agent will depend on its primary function. For instance, `Writer_Agent` and `Brainstorming_Agent` will likely be implemented as `LlmAgent`s, while others might be `CustomAgent`s wrapping specific business logic or tool interactions.

**2.2. `Orchestrator_Agent` as the Primary Controller in ADK** {#aim-orchestrator-as-controller}

The `Orchestrator_Agent`, also implemented as an ADK `Agent` (likely a `CustomAgent` or an `LlmAgent` with significant custom logic), will serve as the central nervous system of `Agent-Makalah`. Its responsibilities include:
*   **User Interface Gateway:** Handling all direct interactions with the user.
*   **Workflow Management:** Initiating and sequencing the execution of other sub-agents based on the defined SOPs (e.g., `SOP-AM-001`, `SOP-AM-002` from `sop-tools-agent-makalah`).
*   **Task Delegation:** Formulating and dispatching specific task briefs to the appropriate sub-agents.
*   **Data Aggregation and Mediation:** Receiving outputs from sub-agents, managing user validation loops, and routing data between sub-agents as needed.
*   **State Management:** Maintaining the overall state of the user's session and task progress within the ADK `Session` and `State` constructs.
*   **Error Coordination:** Receiving error reports from sub-agents and initiating appropriate fallback procedures.

The `Orchestrator_Agent` will be the entry point for user requests and the final point for delivering results, ensuring a cohesive experience despite the underlying distributed nature of the sub-agents. Its implementation will likely involve significant custom Python code to manage the complex logic of task coordination and state transitions.

---

> Segment-ID: AIM-WORKFLOW-ORCH-003
> Source-File: adk-integration-agent-makalah
> Parent-Anchor: aim-root
> Context: Describes how Agent-Makalah's SOPs will be implemented and managed using Google ADK's orchestration capabilities.

## 3. Workflow Orchestration in ADK {#aim-workflow-orchestration}

The sequential and iterative workflows defined for `Agent-Makalah` (e.g., `SOP-AM-001: New Paper Creation Workflow` and `SOP-AM-002: Existing Paper Analysis Workflow` from `sop-tools-agent-makalah`) will be managed using ADK's orchestration capabilities. The `Orchestrator_Agent` will be the primary entity responsible for overseeing these workflows.

**3.1. Implementing SOPs using ADK Orchestration Patterns** {#aim-sops-in-adk}

There are several potential patterns within ADK to implement the multi-step SOPs of `Agent-Makalah`. The final choice for MVP should prioritize simplicity and clarity, while allowing for future complexity.

*   **Option A: Utilizing ADK's Built-in `WorkflowAgent`s:**
    *   ADK provides `WorkflowAgent`s (e.g., `SequentialAgent`, `LoopAgent`, `ParallelAgent`) that are ideal for expressing predefined, deterministic sequences of tasks.
    *   For `SOP-AM-001` (New Paper Creation) and `SOP-AM-002` (Existing Paper Analysis), a `SequentialAgent` could be configured. Each "step" in the `Agent-Makalah` SOP (e.g., Topic Ideation, Literature Search) would correspond to invoking a specific sub-agent (e.g., `Brainstorming_Agent`, `Literature_Search_Agent`) within this `SequentialAgent`.
    *   The `Orchestrator_Agent` would be responsible for initiating the appropriate `WorkflowAgent` and passing the initial context.
    *   **Pros for MVP:** Clear structure, easy to define linear flows, ADK handles basic step management.
    *   **Cons:** Complex interactive loops (like user validation/revision) might require breaking out of the `WorkflowAgent` or using `LoopAgent` constructs, potentially complicating the flow if not handled carefully.

*   **Option B: Custom Orchestration Logic within `Orchestrator_Agent` (as a `CustomAgent`):**
    *   The `Orchestrator_Agent` (implemented as an ADK `CustomAgent` or an `LlmAgent` with extensive custom code) can contain all the workflow logic directly within its `_run_async_impl` method (or similar custom entry point).
    *   This logic would directly call other sub-agents, manage state transitions, handle user interactions (including `SOP-AM-003` and `SOP-AM-005` calls), and implement revision loops programmatically.
    *   **Pros for MVP:** Maximum flexibility and control over the workflow, easier integration of complex user validation loops, and error handling coordination.
    *   **Cons:** Requires more custom code development and careful state management by the `Orchestrator_Agent`.

*   **Recommendation for MVP:** A hybrid approach is likely most effective. The `Orchestrator_Agent` (as a `CustomAgent`) will manage the overall complex logic, especially user interaction and revision loops. It will then invoke other specialized sub-agents. For simpler, sequential internal steps *within* a sub-agent's function, ADK's `WorkflowAgent`s might be considered, but the primary orchestration will reside in the `Orchestrator_Agent`'s custom logic. This ensures full control over the iterative human-in-the-loop validation processes.

**3.2. Managing Task State and Workflow Progress in ADK** {#aim-task-state-in-workflow}

The `Orchestrator_Agent` will leverage ADK's `Session` and `State` management (as detailed in Section 5) to accurately track the progress of the active SOPs.
*   **Persistent State:** Key information such as the current step in `SOP-AM-001` (e.g., "Step 3: Literature Search"), the status of delegated sub-agent tasks, current revision iteration counts, and validated intermediate artifacts will be stored in the `session.state` associated with the user's ADK `Session`.
*   **State Updates:** After each major step completion or user validation, the `Orchestrator_Agent` will update the `session.state` to reflect the latest progress. This allows for potential session resume and accurate logging.
*   **Context for Sub-Agents:** When invoking a sub-agent, the `Orchestrator_Agent` will pass a relevant subset of the `session.state` (or a concise task brief derived from it) to ensure the sub-agent has the necessary context without being overloaded.


---

> Segment-ID: AIM-TOOL-INTEGRATION-004
> Source-File: adk-integration-agent-makalah
> Parent-Anchor: aim-root
> Context: Describes the strategy for integrating Agent-Makalah's authorized tools into the Google ADK environment, including implementation patterns and invocation mechanisms.

## 4. Tool Integration and Management in ADK {#aim-tool-integration}

The specialized functionalities of `Agent-Makalah`'s sub-agents rely heavily on the invocation of various tools. This section outlines the strategy for integrating these authorized tools into the Google Agent Development Kit (ADK) ecosystem, ensuring their secure and efficient utilization. All tool usage must strictly adhere to the policies defined in `sop-tools-agent-makalah`, specifically the "Authorized Tools for Agent-Makalah" section.

**4.1. Implementing Makalah Tools in ADK** {#aim-makalah-tools-in-adk}

Each authorized tool will be implemented or integrated into ADK using the most appropriate ADK construct. The choice depends on the tool's nature and ADK's native capabilities.

*   **`tool-makalah-kb-accessor`:**
    *   **ADK Implementation:** This tool, responsible for read-only access to Makalah KBs, will likely be implemented as a custom Python function or a small service that can be exposed as an ADK tool. It will query a structured data store (where KBs are physically located).
    *   **Invocation:** Agents (e.g., `Writer_Agent`) will invoke this custom tool with specific UID#AnchorID parameters to retrieve relevant KB segments.

*   **`tool-makalah-web-search`:**
    *   **ADK Implementation:** ADK offers built-in search capabilities or integration patterns for external search APIs. This tool could leverage ADK's native search features if they meet the requirements for academic database access and strict domain/query control. Alternatively, it can be implemented as a custom tool that wraps a specific academic search API (e.g., Google Scholar API, institutional database APIs).
    *   **Invocation:** `Brainstorming_Agent` and `Literature_Search_Agent` will invoke this tool with carefully formulated queries and domain restrictions.

*   **`tool-makalah-browse-files`:**
    *   **ADK Implementation:** This tool, for reading user-uploaded files, will be implemented as a custom ADK tool. It will interface with the secure file storage mechanism provided by the backend application/platform where user uploads are temporarily kept.
    *   **Invocation:** `Analysis_Editor_Agent` (and potentially `Orchestrator_Agent` for verification) will invoke this tool with secure references to the uploaded files. Its read-only and path-restricted nature will be enforced at the tool's implementation layer.

*   **`tool-makalah-python-interpreter`:**
    *   **ADK Implementation:** ADK provides a `CodeExecutionTool` or similar constructs for executing code. This tool will directly map to and utilize ADK's built-in code execution capabilities.
    *   **Security:** Critical emphasis will be placed on configuring ADK's code execution environment with **strict sandboxing**, no network access, no general filesystem access, and tight resource/time limits, as mandated in `sop-tools-agent-makalah`. Only vetted code patterns or approved scripts will be permitted.
    *   **Invocation:** `Analysis_Editor_Agent` will invoke this tool when complex data processing or analytical scripting is required.

*   **`tool-makalah-validation-module` (Conceptual):**
    *   **ADK Implementation:** This conceptual tool will likely be implemented as internal Python functions within the respective agents (e.g., `Writer_Agent`'s `SELF_CORRECT_DRAFT_AGAINCE_STYLE_GUIDE` function) rather than a standalone ADK tool. If shared validation logic becomes complex, it could evolve into a reusable internal library or a dedicated ADK tool.
    *   **Purpose:** To perform rule-based validation checks on data, outputs, or adherence to specific formats.

**4.2. Tool Authorization and Invocation within ADK** {#aim-tool-auth-invocation}

*   **Registration:** All custom tools will be registered with their respective ADK `Agent`s, providing clear docstrings or function signatures that describe their purpose, parameters, and expected outputs. This allows LLM-powered agents to correctly understand and utilize them.
*   **Access Control:** ADK's framework or underlying backend security mechanisms will ensure that only authorized `Agent`s (sub-agents) can invoke specific tools. This aligns with the least privilege principle outlined in `sop-tools-agent-makalah`.
*   **Invocation Pattern:** Agents will invoke tools by calling them as functions within their code, typically based on the tool's name and expected parameters. ADK handles the routing and execution of these calls.
*   **Input/Output Handling:**
    *   Inputs to tools will be carefully constructed and validated by the calling agent before invocation.
    *   Outputs from tools will be received by the calling agent and subjected to further validation and processing (as detailed in `sop-tools-agent-makalah`'s general tool principles).

**4.3. Error Handling for Tool Execution:**

Tool execution failures within ADK (e.g., API errors, sandboxed code errors, file access issues) will be propagated back to the calling sub-agent. The sub-agent will then report these failures to the `Orchestrator_Agent` using the error reporting mechanisms defined in `sop-tools-agent-makalah#sop-am-004-root`, triggering appropriate fallback protocols. ADK's tool decorator patterns (e.g., `@adk_tool`) can assist in standardizing error responses from tools.

---

> Segment-ID: AIM-STATE-CONTEXT-005
> Source-File: adk-integration-agent-makalah
> Parent-Anchor: aim-root
> Context: Details how Agent-Makalah leverages Google ADK's Session and State features for comprehensive context and memory management, crucial for iterative workflows.

## 5. State and Context Management with ADK Features {#aim-state-context-management}

Effective management of session state and conversational context is paramount for `Agent-Makalah` to provide a coherent, iterative, and productive user experience. This section details how the principles outlined in `memory-session-agent-makalah` will be implemented by leveraging Google ADK's native `Session` and `State` management capabilities.

**5.1. Leveraging ADK `Session` and `State` Constructs** {#aim-adk-session-state}

*   **ADK `Session` for User Interactions:** Each distinct user interaction with `Agent-Makalah` will be tied to an ADK `Session`. This `Session` will serve as the primary container for all data, state, and conversational context related to that user's ongoing task (e.g., creating a new paper, analyzing an existing one). The lifecycle of this ADK `Session` will align with `memory-session-agent-makalah#msam-session-init-term`.
*   **ADK `State` for Persistent Context:** The `session.state` object within each ADK `Session` will be the central repository for persisting various forms of contextual data. This includes:
    *   **Conversation Context (`memory-session-agent-makalah#msam-conversation-context`):** The full history of user inputs and `Orchestrator_Agent` outputs within the session.
    *   **Intermediate Artifacts (`memory-session-agent-makalah#msam-persist-artifacts`):** User-validated work products like the definitive topic, validated reference lists, approved outlines, and drafted paper sections.
    *   **Task State and Workflow Progress (`memory-session-agent-makalah#msam-persist-task-state`):** The overall progress of the current SOP (e.g., current step, sub-agent task statuses, revision counts).
*   **Serialization Requirement:** Data stored in `session.state` must be JSON-serializable (strings, numbers, booleans, simple lists, and dictionaries). Complex Python objects will need to be converted to a serializable format (e.g., dictionary representation) before storage, or only their unique identifiers will be stored, with the full object retrieved from a separate persistent store if necessary.
*   **State Scoping:** ADK allows for scoping state keys (e.g., session-scoped, user-scoped). `Agent-Makalah` will primarily use session-scoped state for task-specific data, ensuring data isolation between concurrent sessions.

**5.2. Passing Context to LLM-Powered Agents** {#aim-passing-context-to-llms}

A critical aspect of multi-agent LLM systems is providing each LLM-powered sub-agent with the precise context it needs for its current task, without exceeding token limits (which constitute the LLM's `Working Memory` as per `memory-session-agent-makalah#msam-working-memory`).
*   **Task Brief as Context Container:** The `Orchestrator_Agent` will act as the orchestrator of context. Before invoking a sub-agent (e.g., `Writer_Agent`, `Brainstorming_Agent`), it will extract only the strictly necessary and relevant information from the broader `session.state` and compile it into a concise "Task Brief" (a structured dictionary or string).
*   **Token Limit Awareness:** The `Orchestrator_Agent`'s logic will be designed to be mindful of the estimated token count of the generated Task Brief. If a brief is too large (e.g., passing a very long literature review to the `Writer_Agent` for context), the `Orchestrator_Agent` will employ strategies such as:
    *   **Intelligent Truncation:** Cutting off less critical information.
    *   **Contextual Summarization:** Generating a brief summary of lengthy sections (e.g., a summary of a detailed literature review rather than the full text if the `Writer_Agent` only needs key themes for a specific paragraph). This would be a specialized capability of the `Orchestrator_Agent` or a utility function it utilizes.
*   **Explicit Contextual Prompts:** The actual prompt sent to the LLM backend (via the ADK `Agent` construct) will include explicit directives for the LLM to strictly adhere to the provided Task Brief and to ignore any "prior knowledge" from outside this specific context to prevent context contamination.

**5.3. Context Degradation and Recovery (ADK Integration)**

The detection mechanisms for context degradation (e.g., repeated user clarifications, inconsistent agent behavior) outlined in `memory-session-agent-makalah#msam-context-degrad-recov-006` will be implemented within the `Orchestrator_Agent`'s logic.
*   When degradation is detected, the `Orchestrator_Agent` will initiate a context recovery procedure, using ADK's `Session` and `State` features to prompt the user for necessary information to rebuild the accurate context. This aligns with the interactive validation SOP (`SOP-AM-005`).
*   The `Orchestrator_Agent` will update the ADK `session.state` based on the user's input to restore context accuracy.

---

> Segment-ID: AIM-INTERAGENT-COMM-006
> Source-File: adk-integration-agent-makalah
> Parent-Anchor: aim-root
> Context: Details the technical strategy for inter-agent communication within Agent-Makalah using Google ADK's features, emphasizing data exchange patterns.

## 6. Inter-Agent Communication Strategy in ADK {#aim-inter-agent-comm}

Effective and reliable communication between the `Orchestrator_Agent` and its specialized sub-agents is fundamental for the `Agent-Makalah` system's operation. This section outlines the primary technical strategies for inter-agent communication within the Google ADK environment.

**6.1. Primary Communication Mechanism: `session.state` and Method Invocation**

The primary method for passing data and coordinating tasks between agents in `Agent-Makalah` will leverage ADK's `session.state` in conjunction with direct method invocation or ADK's agent-calling patterns.
*   **Data Passing via `session.state`:**
    *   The `Orchestrator_Agent` will primarily use the ADK `session.state` as a shared blackboard or staging area for task inputs and outputs.
    *   Before invoking a sub-agent, the `Orchestrator_Agent` will write the necessary input context (e.g., the Task Brief, relevant validated artifacts) into specific, well-defined keys within `session.state`.
    *   The invoked sub-agent will then read its required inputs from these predefined `session.state` keys.
    *   Upon completion of its task, the sub-agent will write its output (e.g., drafted section, reference list) into another designated key within `session.state`.
    *   The `Orchestrator_Agent` will monitor these keys or be notified of sub-agent completion to retrieve the results.
    *   **Advantage:** This pattern allows for explicit state management and persistence of intermediate results, aligning with the needs for iterative workflows and revision loops. All data passed is automatically managed by ADK's state persistence.
*   **Method Invocation/Agent Calls:**
    *   The `Orchestrator_Agent` will invoke sub-agents by calling their designated entry points or `run` methods within the ADK framework. This might involve directly calling an ADK `Agent` instance (if they are within the same process) or using ADK's mechanisms for distributed agent communication (e.g., HTTP calls to `/run` endpoints if agents are served independently).
    *   The exact parameters passed in the method call itself will be minimal, primarily signaling the task ID or directly pointing to the relevant state keys in `session.state` where the full input context resides.

**6.2. Data Payload Formats for Inter-Agent Exchange**

Data exchanged between agents will adhere to structured, easily parseable formats to ensure interoperability and efficiency. While specific schemas will be defined during the detailed technical design, the conceptual formats include:
*   **Task Briefs (Orchestrator to Sub-Agent):** Typically a dictionary containing the task ID, task-specific parameters (e.g., "section_to_write": "Introduction"), and references to or direct inclusion of essential context data (e.g., "outline_fragment": {...}, "references": [...] ).
*   **Artifacts (Sub-Agent to Orchestrator):** Complex structured data representing the output of a sub-agent's work (e.g., the nested dictionary/JSON for a paper outline, a list of dictionaries for references, a string for a drafted section, a detailed dictionary/JSON for an analysis report). These should conform to the conceptual formats described in `spec-agent-makalah-multi-agent#samma-interagent-comm-004` (Section 4.3).
*   **Status/Error Messages:** Standardized messages indicating task completion status (success/failure) and structured error reports (e.g., including V-Code, description, context) as per `sop-tools-agent-makalah#sop-am-004-root`.

**6.3. ADK-Specific Communication Features:**

*   **ADK Tool Definition for Agents:** A sub-agent itself can be defined as a "tool" for another agent (e.g., `Literature_Search_Agent` can be a tool for `Orchestrator_Agent`). This approach might simplify some invocation patterns and leverage ADK's tool calling mechanisms for inter-agent communication.
*   **Agent-to-Agent (A2A) Protocol (Post-MVP consideration):** If `Agent-Makalah` agents eventually run as truly independent, distributed services, the ADK's A2A protocol would become more relevant for formalized discovery and interaction between them. For MVP, direct invocation (possibly within a single ADK application) is likely sufficient.

**6.4. Security for Inter-Agent Communication:**

*   **Internal Communication:** As communication will primarily occur within the ADK's managed environment (and often within the same ADK `Session` or application deployment), the inherent security features of ADK will be leveraged.
*   **Data Integrity:** All data written to and read from `session.state` should implicitly maintain its integrity, as managed by ADK.
*   **No Sensitive Data Exposure:** Agents must not include sensitive data (e.g., user credentials, external API keys) directly in `session.state` or communication payloads unless absolutely necessary and securely handled (e.g., encrypted, ephemeral). Such data should be managed by secure secrets management services.

---

> Segment-ID: AIM-ERROR-PROPAGATION-007
> Source-File: adk-integration-agent-makalah
> Parent-Anchor: aim-root
> Context: Details the strategy for error detection, reporting, and propagation within Agent-Makalah's ADK environment, ensuring robust error handling.

## 7. Error Handling Propagation in ADK {#aim-error-propagation}

Effective error handling is paramount for the stability and reliability of the `Agent-Makalah` multi-agent system. This section outlines how errors originating from specialized sub-agents will be detected, reported, and propagated to the `Orchestrator_Agent` within the Google ADK environment, ensuring adherence to the error management principles outlined in `sop-tools-agent-makalah#sop-am-004-root` (Sub-Agent Error Reporting and Handling Coordination).

**7.1. Error Detection within ADK Agents (Sub-Agents):**

*   Each sub-agent, implemented as an ADK `Agent`, is responsible for its own internal error detection. This includes:
    *   **Tool Execution Failures:** Errors returned by invoked tools (e.g., `tool-makalah-web-search` timeout, `tool-makalah-python-interpreter` runtime error). ADK's tool invocation mechanisms (e.g., `tool_context.call`) are expected to return explicit error signals.
    *   **Internal Processing Failures:** Logic errors within the sub-agent's `_run_async_impl` method (or similar processing logic), invalid input parsing, or inability to produce a valid output based on its specified functions.
    *   **Validation Failures:** If a sub-agent performs internal validation of its own output (e.g., `Writer_Agent`'s `SELF_CORRECT_DRAFT_AGAINCE_STYLE_GUIDE`), and this validation fails.

**7.2. Error Reporting from Sub-Agent to `Orchestrator_Agent`:**

Upon detecting an unrecoverable error (i.e., one that cannot be resolved by immediate, limited retries within the sub-agent), the sub-agent will formally report the error to the `Orchestrator_Agent`.
*   **Mechanism:** This reporting will primarily occur by the sub-agent returning an explicit error object or status to the `Orchestrator_Agent` via the ADK communication channel (e.g., writing an error status to a designated `session.state` key and returning an error signal from its `_run_async_impl` method).
*   **Error Payload:** The error payload from the sub-agent to the `Orchestrator_Agent` will be structured, ideally including:
    *   The originating sub-agent's identifier.
    *   A descriptive error message.
    *   Relevant diagnostic information (e.g., the specific tool that failed, input parameters that caused the issue, stack trace if permissible in a secure environment for debugging).
    *   A Makalah Framework-specific V-Code (e.g., V-006 for tool failure, V-011 for KB access failure) and a suggested P-level priority (e.g., P5 for most operational failures), as defined in `sop-tools-agent-makalah#sop-am-004-error-classification`.

**7.3. `Orchestrator_Agent`'s Central Error Handling Role:**

The `Orchestrator_Agent` is the central error coordinator.
*   **Error Reception & Classification:** It receives error reports from sub-agents. It then classifies these errors (assigning a definitive P-level priority and V-Code) based on its own logic that embodies `sop-tools-agent-makalah#sop-am-004-error-classification` principles.
*   **Fallback Protocol Initiation:** Based on the error classification and the current overall task context, the `Orchestrator_Agent` will initiate the appropriate fallback protocol. This includes:
    *   Informing the user (using its persona, as defined in `persona-prompt-agent-makalah`).
    *   Attempting recovery (e.g., requesting clarification from user via `SOP-AM-003`).
    *   Rerouting the workflow.
    *   Halting the task.
    *   As a last resort, escalating to critical system-wide fallbacks (P1/P2).
*   **Leveraging ADK for Control:** ADK's control flow mechanisms (e.g., exceptions raised within an `Agent`'s `_run_async_impl` or explicit return of error statuses) can be used to propagate error signals up the orchestration chain to the `Orchestrator_Agent`.

**7.4. Standardization for Robustness:**

*   **Standardized Error Responses from Tools:** Tools themselves, especially custom ones, should adhere to a standardized error response format (e.g., using `adk_tool` decorators or custom Python exceptions that translate into predictable error payloads). This simplifies parsing for the calling agent.
*   **Consistent V-Code Usage:** Consistent application and reporting of Makalah Framework V-Codes (`sop-tools-agent-makalah#sop-am-004-error-classification` will detail these) across all agents and tool implementations are vital for structured error management and debugging.
*   **ADK Observability:** ADK's logging and tracing features will be utilized to capture error events, allowing developers to monitor and debug failures effectively.

---

> Segment-ID: AIM-DEPLOYMENT-008
> Source-File: adk-integration-agent-makalah
> Parent-Anchor: aim-root
> Context: Discusses high-level deployment considerations for Agent-Makalah using Google ADK, focusing on MVP requirements.

## 8. Deployment Considerations (High-Level for MVP) {#aim-deployment-considerations}

The Google Agent Development Kit (ADK) offers inherent flexibility in deployment, allowing `Agent-Makalah` to be run in various environments. This section outlines high-level considerations for deploying the `Agent-Makalah` system, with a focus on supporting the Minimum Viable Product (MVP) development and eventual production needs.

**8.1. Deployment Model:**

*   **Local Development & Testing:** During the development and testing phases, `Agent-Makalah` and its sub-agents can be run locally on developer workstations. ADK's local runtime and debugging UI are essential for this purpose. This allows for rapid iteration and troubleshooting of individual agents and their interactions.
*   **Cloud-Based Deployment (for Production/Staging):** For production environments and potentially for staging/testing environments, `Agent-Makalah` should be deployed to a scalable and robust cloud platform. Given ADK's Google origin, Google Cloud Platform (GCP) is the recommended target.
    *   **Containerization:** Agents (implemented as Python applications) can be containerized using Docker. This ensures consistency across different environments and simplifies deployment.
    *   **Managed Services:** GCP services such as Cloud Run (for serverless container deployment), Cloud Functions (for simpler, event-driven agent invocations if applicable), or Google Kubernetes Engine (GKE) for more complex, orchestrated deployments, can be leveraged to host the ADK agents. The choice will depend on expected traffic, scalability needs, and operational complexity.
    *   **Persistent Storage:** Databases (e.g., Cloud SQL for PostgreSQL, Cloud Datastore/Firestore for NoSQL needs) will be used for persisting chat history, agent states, and intermediate artifacts as per `memory-session-agent-makalah` and `database-design-agent-makalah`. Cloud Storage can be used for temporary storage of user-uploaded files.

**8.2. Scalability and Resource Management:**

*   **Agent Scaling:** ADK's design and cloud-native deployment options allow for individual sub-agents (as independent microservices or functions) to be scaled independently based on demand. For instance, the `Writer_Agent` might require more resources or concurrent instances than the `Brainstorming_Agent` during peak usage.
*   **Resource Limits:** Proper resource allocation (CPU, memory) and auto-scaling configurations should be implemented in the deployment environment to optimize cost and performance.

**8.3. Networking and Access Control:**

*   **Secure Endpoints:** The primary interface for `Agent-Makalah` (typically through the `Orchestrator_Agent`'s endpoint) must be secured with appropriate authentication and authorization mechanisms (e.g., API keys, OAuth 2.0).
*   **Internal Communication:** Inter-agent communication within the cloud environment should leverage secure internal networking (e.g., VPC networks) provided by the cloud platform, minimizing exposure to the public internet.
*   **Firewall Rules:** Strict firewall rules should be configured to allow only necessary inbound and outbound traffic for agent services.

**8.4. Monitoring and Logging:**

*   Cloud-native monitoring and logging solutions (e.g., Google Cloud Logging, Cloud Monitoring) should be integrated to collect agent logs, performance metrics, and error traces. This is crucial for operational visibility, troubleshooting, and adherence to `sop-tools-agent-makalah#sop-am-004-root`'s error reporting and logging requirements.

**8.5. Continuous Integration/Continuous Deployment (CI/CD):**

*   A CI/CD pipeline should be established to automate the building, testing, and deployment of agent code. This ensures consistent and reliable releases.

---

> Segment-ID: AIM-DEV-DEBUG-009
> Source-File: adk-integration-agent-makalah
> Parent-Anchor: aim-root
> Context: Highlights the tools and practices for developing and debugging Agent-Makalah effectively within the Google ADK environment.

## 9. Development and Debugging with ADK Tools {#aim-dev-debug-tools}

Effective development and debugging are crucial for building a robust multi-agent system like `Agent-Makalah`. The Google ADK provides several features and patterns that facilitate these processes. This section outlines the key tools and approaches for development and debugging.

**9.1. ADK's Local Runtime and Debugging UI:**

*   **Local Development Environment:** Developers will set up their local environments to run `Agent-Makalah`'s sub-agents directly. ADK provides a local runtime that simulates the agent execution environment.
*   **Interactive Debugging UI:** ADK often comes with a local debugging user interface. This UI allows developers to:
    *   Monitor the flow of execution between agents.
    *   Inspect the `session.state` at various points in the workflow.
    *   View agent inputs and outputs.
    *   Observe tool invocations and their results.
    *   Step through complex workflows, aiding in understanding how different agents collaborate and how context is propagated.
*   **Benefits:** This local setup provides rapid feedback during development, enabling quick iteration and troubleshooting of individual agent logic and inter-agent communication.

**9.2. Structured Logging:**

*   **Agent-Specific Logging:** Each ADK `Agent` (sub-agent) should implement robust, structured logging within its own code. This includes logging:
    *   Inputs received for a task.
    *   Outputs produced.
    *   Key internal decisions made by the LLM or custom logic.
    *   Tool invocations and their responses.
    *   Error details (as per `sop-tools-agent-makalah#sop-am-004-root`).
*   **Centralized Logging (Cloud):** When deployed to a cloud environment (e.g., GCP), these logs will be ingested into a centralized logging solution (e.g., Google Cloud Logging). This allows for system-wide visibility, aggregation of logs from multiple agents, and easy filtering/searching for specific events or errors.

**9.3. Tracing and Observability (Post-MVP Consideration):**

*   For more advanced debugging and performance monitoring in complex production environments, tracing capabilities (e.g., OpenTelemetry integration if supported by ADK) could be implemented in post-MVP versions. This allows for end-to-end visibility of a request as it flows through multiple agents and services.
*   Monitoring tools would also track agent latency, resource usage, and error rates to identify bottlenecks or performance issues.

**9.4. Unit and Integration Testing:**

*   **Code-First Approach:** Given ADK's code-first nature, standard software development practices for unit and integration testing will be crucial.
*   **Unit Tests:** Individual agent functions, custom tools, and core orchestration logic within the `Orchestrator_Agent` should have comprehensive unit tests.
*   **Integration Tests:** Tests should verify the correct interaction between two or more sub-agents, and the overall end-to-end workflows (e.g., `SOP-AM-001`). Mocking of external dependencies (like LLM APIs, external tools) will be necessary during testing.
*   **Automated Testing:** Integration with CI/CD pipelines will automate these tests, ensuring code quality and preventing regressions.

**9.5. Interactive Development and Iteration:**

*   ADK's design encourages an iterative development cycle. Developers can rapidly prototype agent behaviors, test them locally, gather feedback, and refine. This is particularly valuable for optimizing LLM prompting strategies and complex decision flows.

---

> Segment-ID: AIM-REVISION-HIST-010
> Source-File: adk-integration-agent-makalah
> Parent-Anchor: aim-root
> Context: Tracks the version history and changes made to this Google ADK Integration Strategy document.

## 10. Revision History {#aim-revision-history}

| Version | Date       | Author(s)   | Summary of Changes                                                                        |
| :------ | :--------- | :---------- | :---------------------------------------------------------------------------------------- |
| 1.0     | 1 Jun 2025 | ERIK SUPIT  | Initial MVP draft of the Google ADK Integration Strategy for Agent-Makalah, covering agent mapping, orchestration, tool, state, communication, error handling, and deployment considerations. |
|         |            |             |                                                                                           |
|         |            |             |                                                                                           |