UID: srs-agent-makalah
Title: Software Requirements Specification (SRS) for Agent-Makalah
Author: "ERIK SUPIT"
Version: 1.0
Date: "1 Juni 2025"
Role: SOFTWARE-REQUIREMENTS
Status: FINAL
Domain: SOFTWARE-ENGINEERING
Dependencies:
  - "prd-agent-makalah"
  - "spec-agent-makalah-multi-agent"
  - "sop-tools-agent-makalah"
Anchors:
  - "srs-root"
  - "srs-introduction"
  - "srs-overall-description"
  - "srs-functional-requirements"
  - "srs-nfr"
  - "srs-external-interfaces"
  - "srs-other-requirements"
  - "srs-revision-history"
  # Functional Requirements Anchors (for clarity in document structure)
  - "srs-fr-user-interaction"
  - "srs-fr-new-paper-creation"
  - "srs-fr-existing-paper-analysis"
  - "srs-fr-tool-integration"
  - "srs-fr-error-handling-logging"
Tags:
  - "srs"
  - "requirements"
  - "agent-makalah"
  - "software-engineering"
  - "mvp"
Language: EN
Chained: true
---

> Segment-ID: SRS-INTRO-001
> Source-File: srs-agent-makalah
> Parent-Anchor: srs-root
> Context: Overview of the SRS purpose, scope, definitions, references, and document organization.

## 1. Introduction {#srs-introduction}

**1.1. Purpose of this Document**
This Software Requirements Specification (SRS) serves as the definitive guide for the development of the `Agent-Makalah` system. It details the functional and non-functional requirements that `Agent-Makalah` must satisfy to meet its product vision and goals, as outlined in the `Product Requirement Document (PRD) for Agent-Makalah` (`prd-agent-makalah`). This document is intended for the software development team, quality assurance engineers, project managers, and other stakeholders involved in the design, implementation, and testing of `Agent-Makalah`.

**1.2. Scope of the SRS**
This SRS specifies the requirements for the Minimum Viable Product (MVP) of the `Agent-Makalah` system. It encompasses the core functionalities of academic paper creation (including ideation, literature search, outlining, and drafting) and existing paper analysis, delivered through a multi-agent architecture integrated with the Google Agent Development Kit (ADK). The scope does not cover detailed architectural design, database schemas, or specific implementation choices, which will be addressed in subsequent technical design documents.

**1.3. Definitions, Acronyms, and Abbreviations**
For a comprehensive list of terms, acronyms, and abbreviations used throughout this document, refer to the glossary section of the `Product Requirement Document (PRD) for Agent-Makalah` (`prd-agent-makalah`). Additional definitions specific to software engineering will be implicitly understood by the target audience.
*   **ADK:** Google Agent Development Kit
*   **PRD:** Product Requirement Document
*   **SOP:** Standard Operating Procedure
*   **SRS:** Software Requirements Specification
*   **MVP:** Minimum Viable Product

**1.4. References**
*   `Product Requirement Document (PRD) for Agent-Makalah` (`prd-agent-makalah`): Provides the product vision, high-level features, and business goals.
*   `Specification Document for the Agent-Makalah Multi-Agent Writing System` (`spec-agent-makalah-multi-agent`): Defines the multi-agent architecture and the roles and detailed functions of each sub-agent.
*   `Standard Operating Procedures and Authorized Tools for Agent-Makalah` (`sop-tools-agent-makalah`): Details the specific workflows and tool usage policies for `Agent-Makalah`'s operations.

**1.5. Overview of the Document**
This document is organized into the following sections:
*   Section 2 provides an overall description of `Agent-Makalah` from a software perspective.
*   Section 3 details the functional requirements, specifying what the system must do.
*   Section 4 outlines the non-functional requirements, describing quality attributes and constraints.
*   Section 5 specifies external interface requirements.
*   Section 6 lists other requirements.
*   Section 7 provides the revision history.

---

> Segment-ID: SRS-OVERALL-002
> Source-File: srs-agent-makalah
> Parent-Anchor: srs-root
> Context: Provides a high-level overview of Agent-Makalah from a software perspective, including its context, functions, users, and constraints.

## 2. Overall Description {#srs-overall-description}

**2.1. Product Perspective**
`Agent-Makalah` is an independent software system designed as a multi-agent application built upon the Google Agent Development Kit (ADK). It operates as a sophisticated AI-powered assistant for academic writing and analysis, serving as a distinct entity in its operational environment. The system's primary interaction point is a conversational interface, through which users submit requests and receive outputs. `Agent-Makalah` does not directly control or integrate with a user's local file system or applications beyond the explicitly defined file upload/download mechanisms. Its core functionalities are self-contained within its multi-agent architecture.

**2.2. Product Functions**
At a high level, `Agent-Makalah` provides the following key functions, further detailed in Section 3:
*   **Guided Academic Paper Creation:** Facilitates an end-to-end process from topic ideation to final paper assembly, leveraging specialized sub-agents.
*   **Existing Paper Analysis & Feedback:** Analyzes user-uploaded academic documents and provides structured reports or feedback.
*   **Interactive User Engagement:** Employs a rigorous, conversational dialogue method for clarifying intent, validating outputs, and managing revision cycles.
*   **Knowledge-Based Operations:** Operates by strictly adhering to predefined academic style guides and operational procedures.
*   **Transparent Collaboration:** Maintains a verifiable history of user and agent interactions throughout the workflow.

**2.3. User Characteristics**
The target users of `Agent-Makalah` are university students (undergraduate and postgraduate), researchers, and academics. Key characteristics include:
*   **Varying Levels of Academic Writing Proficiency:** Users may range from novices requiring extensive guidance to experienced researchers seeking efficiency.
*   **Familiarity with Digital Tools:** Users are expected to be familiar with basic computer operations and conversational interfaces.
*   **Desire for Quality & Accountability:** Users seek to produce high-quality academic work while maintaining intellectual integrity and demonstrating their active involvement.
*   **Primary Language:** Users will primarily interact in Bahasa Indonesia, expecting outputs in the same language.

**2.4. General Constraints**
The following high-level constraints apply to the `Agent-Makalah` system MVP:
*   **Language Support:** Primary input and output language is Bahasa Indonesia.
*   **Content Focus:** Strictly limited to academic writing and analysis tasks; not for general creative writing, casual conversation, or non-academic topics.
*   **Platform:** Implementation will primarily leverage Google Agent Development Kit (ADK) constructs and patterns.
*   **Tool Usage:** Only explicitly authorized and defined tools can be invoked by agents.
*   **Offline Capability:** No offline functionality is required; continuous internet connectivity is assumed.
*   **Hardware/Software Environment:** The system is expected to run as a cloud-hosted service accessible via standard web-based client applications. Client-side requirements are minimal (modern web browser).

**2.5. Assumptions and Dependencies**
*   **Existence of External KBs:** It is assumed that relevant Makalah Framework Knowledge Bases (e.g., `makalah-academic-style-guides.txt`) are accessible and stable for agent consumption.
*   **LLM Availability:** Reliable access to a powerful Large Language Model (LLM) backend is assumed for the core AI capabilities of the agents.
*   **Google ADK Stability:** The Google ADK platform and its core functionalities (agent definition, orchestration, tool integration, state management) are assumed to be stable and adequately documented for implementation.
*   **User Compliance:** Users are assumed to respond cooperatively and provide necessary information during interactive clarification and validation loops.
*   **Security of Underlying Platform:** The underlying cloud platform (e.g., GCP) provides foundational security infrastructure.

---

> Segment-ID: SRS-FR-003
> Source-File: srs-agent-makalah
> Parent-Anchor: srs-root
> Context: Details the functional requirements of Agent-Makalah, specifying what the system must do.

## 3. Functional Requirements {#srs-functional-requirements}

This section specifies the detailed functional requirements of the `Agent-Makalah` system. These requirements describe the behaviors and capabilities the system must exhibit to fulfill its product vision and support its defined workflows. They are organized by logical functional areas and map to the roles and functions of the sub-agents defined in `spec-agent-makalah-multi-agent` and the workflows in `sop-tools-agent-makalah`.

---

> Segment-ID: SRS-FR-USER-INTERACTION-003-1
> Source-File: srs-agent-makalah
> Parent-Anchor: srs-functional-requirements
> Context: Functional requirements related to direct user interaction and overall system control, primarily handled by the Orchestrator_Agent.

### 3.1. User Interaction and System Control (`Orchestrator_Agent` Functions) {#srs-fr-user-interaction}

This section details the functional requirements primarily managed by the `Orchestrator_Agent` related to direct user interaction, intent processing, validation, and overall system workflow orchestration.

**3.1.1. User Request Reception & Parsing**
    *   **REQ-UI-001: Receive Initial User Request:** The system SHALL be capable of receiving initial text-based requests from the user through a conversational interface.
        *   **Input:** Raw text string (user request).
        *   **Output:** Internal trigger for request processing.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Orchestrator_Agent` - `RECEIVE_USER_INITIAL_REQUEST`).
    *   **REQ-UI-002: Parse User Request:** The system SHALL parse the received raw text request to extract initial keywords, general intent, and any explicit parameters.
        *   **Input:** Raw text string.
        *   **Output:** Initial parsed intent (structured data).
        *   **Source:** `spec-agent-makalah-multi-agent` (`Orchestrator_Agent` - `RECEIVE_USER_INITIAL_REQUEST`).

**3.1.2. Interactive Intent Clarification & Validation**
    *   **REQ-UI-003: Initiate Intent Clarification Dialogue:** The system SHALL, upon detecting ambiguity or incompleteness in user requests, proactively engage the user in an interactive dialogue to clarify their intent.
        *   **Input:** Initial parsed intent, current conversational context.
        *   **Output:** Trigger for clarification dialogue.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Orchestrator_Agent` - `CLARIFY_USER_INTENT`), `sop-tools-agent-makalah#sop-am-003-root`.
    *   **REQ-UI-004: Formulate Clarification Questions:** The system SHALL be capable of generating precise, persona-aligned (critical/sarcastic as defined for `Orchestrator_Agent`) questions to elicit specific missing or ambiguous information from the user.
        *   **Input:** Identified ambiguity points, current context.
        *   **Output:** Text-based clarification question.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Orchestrator_Agent` - `CLARIFY_USER_INTENT`), `sop-tools-agent-makalah#sop-am-003-root` (Step 3).
    *   **REQ-UI-005: Validate Clarified Input:** The system SHALL validate user responses during clarification against expected formats or logical consistency to ensure precise understanding.
        *   **Input:** User response to clarification, expected data type/format/value.
        *   **Output:** Validated input (structured data) OR invalid input status.
        *   **Source:** `sop-tools-agent-makalah#sop-am-003-root` (Step 2, Step 3).
    *   **REQ-UI-006: Manage Clarification Loop:** The system SHALL manage an interactive clarification loop, allowing for a predefined maximum number of attempts (e.g., 3 retries) to obtain validated input before escalating.
        *   **Input:** Invalid input status, current retry count.
        *   **Output:** Continuation of loop OR escalation signal.
        *   **Source:** `sop-tools-agent-makalah#sop-am-003-root` (Step 3).

**3.1.3. User Validation & Revision Management**
    *   **REQ-UI-007: Present Intermediate Outputs for Validation:** The system SHALL present intermediate outputs from sub-agents (e.g., topic options, reference lists, outlines, drafted sections) to the user for explicit validation or feedback.
        *   **Input:** Intermediate output artifact (structured data).
        *   **Output:** Displayed artifact, prompt for user validation.
        *   **Source:** `sop-tools-agent-makalah#sop-am-005-root` (Step 1).
    *   **REQ-UI-008: Receive User Validation Feedback:** The system SHALL capture user responses to validation prompts, categorizing them as approval, rejection with specific revisions, or ambiguous feedback.
        *   **Input:** User response (text).
        *   **Output:** Categorized feedback (Approved / Rejected with Revisions / Ambiguous).
        *   **Source:** `sop-tools-agent-makalah#sop-am-005-root` (Step 2).
    *   **REQ-UI-009: Manage Revision Iterations:** The system SHALL track and enforce a predefined maximum number of revision attempts for each validation cycle (e.g., 3 retries per artifact).
        *   **Input:** Categorized feedback, current revision count for artifact.
        *   **Output:** Instruction to re-generate/revise (if within limits) OR escalation signal (if max revisions reached).
        *   **Source:** `sop-tools-agent-makalah#sop-am-005-root` (Step 4).
    *   **REQ-UI-010: Escalate Unresolved Validations:** The system SHALL, if user validation cannot be achieved after maximum revision attempts, escalate the issue to the user, providing options (e.g., accept as-is, abandon sub-task, rephrase initial request).
        *   **Input:** Max revisions reached status.
        *   **Output:** Escalation options presented to user, user's chosen path.
        *   **Source:** `sop-tools-agent-makalah#sop-am-005-root` (Step 6).

**3.1.4. Final Product Presentation**
    *   **REQ-UI-011: Present Final Assembled Document:** The system SHALL present the complete, final academic paper or analysis report to the user in a readable format.
        *   **Input:** Final document artifact.
        *   **Output:** Displayed final document.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Orchestrator_Agent` - `PRESENT_FINAL_PRODUCT_TO_USER`).

**3.1.5. Session & Context Management**
    *   **REQ-UI-012: Maintain Conversation Context:** The system SHALL accurately store and retrieve the full conversation history (user inputs and agent outputs) for the duration of a user session.
        *   **Input:** User input, Agent output.
        *   **Output:** Persisted conversation turns.
        *   **Source:** `memory-session-agent-makalah#msam-persist-user-io`.
    *   **REQ-UI-013: Persist Intermediate Artifacts:** The system SHALL persist intermediate validated artifacts (e.g., definitive topic, validated reference list, approved outline, drafted sections) throughout the user's session to support iterative workflows.
        *   **Input:** Intermediate artifact (structured data).
        *   **Output:** Persisted artifact linked to session.
        *   **Source:** `memory-session-agent-makalah#msam-persist-artifacts`.
    *   **REQ-UI-014: Manage Session State:** The system SHALL track the overall state of the user's session, including current active SOP, current SOP step, and sub-agent task statuses.
        *   **Input:** Workflow progression events.
        *   **Output:** Updated session state.
        *   **Source:** `memory-session-agent-makalah#msam-persist-task-state`.
    *   **REQ-UI-015: Clear Working Memory for Sub-Agents:** The system SHALL ensure that sub-agents receive only the context relevant to their immediate task, effectively "clearing" previous working memory for each new invocation to optimize LLM performance and prevent context contamination.
        *   **Input:** Task brief for sub-agent.
        *   **Output:** Context-scoped input to sub-agent.
        *   **Source:** `adk-integration-agent-makalah#aim-passing-context-to-llms`.
    *   **REQ-UI-016: Detect & Initiate Context Recovery:** The system SHALL detect potential context degradation (e.g., based on user confusion, internal inconsistencies) and initiate a context recovery procedure involving user interaction to rebuild understanding.
        *   **Input:** Indicators of context degradation.
        *   **Output:** Trigger for context recovery dialogue.
        *   **Source:** `memory-session-agent-makalah#msam-context-degradation-recovery`.
        
---

> Segment-ID: SRS-FR-NEW-PAPER-003-2
> Source-File: srs-agent-makalah
> Parent-Anchor: srs-functional-requirements
> Context: Functional requirements detailing the end-to-end workflow for creating a new academic paper.

### 3.2. New Paper Creation Workflow {#srs-fr-new-paper-creation}

This section details the functional requirements for the end-to-end workflow of creating a new academic paper, as orchestrated by the `Orchestrator_Agent` and executed by various sub-agents. This workflow aligns with `sop-tools-agent-makalah#sop-am-001-root`.

**3.2.1. Topic Ideation and Finalization**
    *   **REQ-NPC-001: Determine Brainstorming Need:** The system SHALL determine if a brainstorming session is required based on initial user input clarity or explicit user request.
        *   **Input:** Clarified user intent from `REQ-UI-006`.
        *   **Output:** Decision to initiate brainstorming (boolean).
        *   **Source:** `sop-tools-agent-makalah#sop-am-001-root` (Step 2.1).
    *   **REQ-NPC-002: Initiate Brainstorming Session:** The system SHALL be capable of initiating a brainstorming session with the `Brainstorming_Agent`.
        *   **Input:** Initial topic/area of interest, decision to brainstorm.
        *   **Output:** Command dispatched to `Brainstorming_Agent`.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Orchestrator_Agent` - `INITIATE_BRAINSTORMING_SESSION`).
    *   **REQ-NPC-003: Generate Topic Variations:** The `Brainstorming_Agent` SHALL generate diverse topic variations, research questions, and perspectives based on input and inspiration from web search.
        *   **Input:** Initial topic/area of interest.
        *   **Output:** Proposed topic candidates (structured list).
        *   **Source:** `spec-agent-makalah-multi-agent` (`Brainstorming_Agent` - `EXPLORE_TOPIC_VARIATIONS_WITH_INSPIRATION_SEARCH`).
        *   **Tool Usage:** `tool-makalah-web-search` (as specified in `sop-tools-agent-makalah#stam-tool-web-search`).
    *   **REQ-NPC-004: Analyze Topic Potential:** The `Brainstorming_Agent` SHALL perform a brief analysis of generated topic variations for novelty, relevance, and initial literature availability.
        *   **Input:** Proposed topic candidates.
        *   **Output:** Analysis results (brief, structured).
        *   **Source:** `spec-agent-makalah-multi-agent` (`Brainstorming_Agent` - `ANALYZE_TOPIC_POTENTIAL`).
    *   **REQ-NPC-005: Facilitate Ideation Dialogue:** The `Brainstorming_Agent` SHALL provide discussion points and trigger questions for `Orchestrator_Agent` to use in user dialogue.
        *   **Input:** Proposed topic candidates, analysis results.
        *   **Output:** Discussion prompts.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Brainstorming_Agent` - `FACILITATE_IDEATION_DIALOGUE`).
    *   **REQ-NPC-006: Refine Topic Based on Feedback:** The `Brainstorming_Agent` SHALL refine topic variations based on user feedback (relayed by `Orchestrator_Agent`).
        *   **Input:** User feedback (text).
        *   **Output:** Refined topic candidates.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Brainstorming_Agent` - `REFINE_TOPIC_BASED_ON_FEEDBACK`).
    *   **REQ-NPC-007: Output Definitive Topic:** The `Brainstorming_Agent` SHALL output the single, user-validated definitive topic to `Orchestrator_Agent`.
        *   **Input:** User-validated topic.
        *   **Output:** Definitive topic (string/structured data).
        *   **Source:** `spec-agent-makalah-multi-agent` (`Brainstorming_Agent` - `OUTPUT_DEFINITIVE_TOPIC`).

**3.2.2. Literature Search**
    *   **REQ-NPC-008: Initiate Literature Search:** The system SHALL initiate a literature search task with `Literature_Search_Agent` using the definitive topic.
        *   **Input:** Definitive topic.
        *   **Output:** Command dispatched to `Literature_Search_Agent`.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Orchestrator_Agent` - `CREATE_TASK_BRIEF`).
    *   **REQ-NPC-009: Formulate Search Queries:** The `Literature_Search_Agent` SHALL formulate effective and semantic search queries based on the topic.
        *   **Input:** Definitive topic.
        *   **Output:** Search queries (structured data).
        *   **Source:** `spec-agent-makalah-multi-agent` (`Literature_Search_Agent` - `FORMULATE_SEARCH_QUERIES`).
    *   **REQ-NPC-010: Execute Academic Search:** The `Literature_Search_Agent` SHALL execute searches on authorized academic databases using `tool-makalah-web-search`.
        *   **Input:** Search queries.
        *   **Output:** Raw search results.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Literature_Search_Agent` - `EXECUTE_ACADEMIC_SEARCH`).
        *   **Tool Usage:** `tool-makalah-web-search` (as specified in `sop-tools-agent-makalah#stam-tool-web-search`).
    *   **REQ-NPC-011: Filter & Validate Search Results:** The `Literature_Search_Agent` SHALL filter results by relevance, credibility (peer-reviewed), and publication year (e.g., last 5 years preference) and validate them against `makalah-academic-style-guides.txt`.
        *   **Input:** Raw search results.
        *   **Output:** Filtered & validated references.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Literature_Search_Agent` - `FILTER_AND_VALIDATE_RESULTS`).
    *   **REQ-NPC-012: Extract Reference Metadata:** The `Literature_Search_Agent` SHALL extract key metadata (title, authors, year, journal/conference, DOI/URL) from validated references.
        *   **Input:** Validated references.
        *   **Output:** Extracted metadata.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Literature_Search_Agent` - `EXTRACT_REFERENCE_METADATA`).
    *   **REQ-NPC-013: Generate Reference Summary & Citation:** The `Literature_Search_Agent` SHALL generate a concise summary and format the citation (e.g., APA) for each relevant reference, adhering to `makalah-academic-style-guides.txt`.
        *   **Input:** Extracted metadata, full reference content.
        *   **Output:** Reference summary, formatted citation.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Literature_Search_Agent` - `GENERATE_REFERENCE_SUMMARY`, `CREATE_CITATION_FORMATTED`).
    *   **REQ-NPC-014: Compile & Order Reference List:** The `Literature_Search_Agent` SHALL compile all processed references into a structured list, ordered by relevance.
        *   **Input:** Summaries, citations, metadata.
        *   **Output:** Structured, ordered reference list.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Literature_Search_Agent` - `COMPILE_AND_ORDER_REFERENCE_LIST`).

**3.2.3. Outline Creation**
    *   **REQ-NPC-015: Initiate Outline Creation:** The system SHALL initiate an outline creation task with `Outline_Draft_Agent` using the definitive topic and validated references.
        *   **Input:** Definitive topic, validated references.
        *   **Output:** Command dispatched to `Outline_Draft_Agent`.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Orchestrator_Agent` - `CREATE_TASK_BRIEF`).
    *   **REQ-NPC-016: Analyze Topic and References for Outline:** The `Outline_Draft_Agent` SHALL analyze inputs to understand scope, arguments, and key findings for structuring the paper.
        *   **Input:** Definitive topic, validated references.
        *   **Output:** Internal understanding for outline design.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Outline_Draft_Agent` - `ANALYZE_TOPIC_AND_REFERENCES`).
    *   **REQ-NPC-017: Design Paper Structure:** The `Outline_Draft_Agent` SHALL design a logical and coherent paper structure (chapters, sub-chapters, sequence) adhering to academic structure principles.
        *   **Input:** Internal understanding, academic structure principles.
        *   **Output:** Proposed paper structure.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Outline_Draft_Agent` - `DESIGN_PAPER_STRUCTURE`).
    *   **REQ-NPC-018: Develop Section Outlines:** The `Outline_Draft_Agent` SHALL create detailed outlines of key points for each planned chapter and sub-chapter.
        *   **Input:** Proposed paper structure.
        *   **Output:** Detailed section outlines.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Outline_Draft_Agent` - `DEVELOP_SECTION_OUTLINES`).
    *   **REQ-NPC-019: Draft Key Arguments & Evidence Points:** The `Outline_Draft_Agent` SHALL formulate initial drafts of main arguments, claims, or evidence points for each outline point, referencing literature.
        *   **Input:** Detailed section outlines, relevant references.
        *   **Output:** Drafted key arguments & evidence points.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Outline_Draft_Agent` - `DRAFT_KEY_ARGUMENTS_AND_EVIDENCE_POINTS`).
    *   **REQ-NPC-020: Ensure Logical Flow & Coherence (Outline):** The `Outline_Draft_Agent` SHALL verify logical progression and coherence within the drafted outline and key points.
        *   **Input:** Drafted outline & key points.
        *   **Output:** Validated internal structure.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Outline_Draft_Agent` - `ENSURE_LOGICAL_FLOW_AND_COHERENCE`).
    *   **REQ-NPC-021: Map References to Outline Points:** The `Outline_Draft_Agent` SHALL internally map specific references to outline points for justification and `Writer_Agent`'s use.
        *   **Input:** Drafted outline, references.
        *   **Output:** Internal reference mapping information.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Outline_Draft_Agent` - `MAP_REFERENCES_TO_OUTLINE_POINTS_INTERNAL`).
    *   **REQ-NPC-022: Compile Structured Outline & Draft:** The `Outline_Draft_Agent` SHALL compile all outlining work into a single structured document.
        *   **Input:** All outline components.
        *   **Output:** Structured outline document.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Outline_Draft_Agent` - `COMPILE_STRUCTURED_OUTLINE_AND_DRAFT`).

**3.2.4. Sectional Prose Generation**
    *   **REQ-NPC-023: Initiate Section Writing Task:** The system SHALL initiate a writing task for a specific paper section with `Writer_Agent`.
        *   **Input:** Relevant outline portion, drafted key points, validated references, reference mapping.
        *   **Output:** Command dispatched to `Writer_Agent`.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Orchestrator_Agent` - `CREATE_TASK_BRIEF`).
    *   **REQ-NPC-024: Internalize Section Requirements & Style Guides:** The `Writer_Agent` SHALL understand section requirements and strictly adhere to `makalah-academic-style-guides.txt`.
        *   **Input:** Section requirements, `makalah-academic-style-guides.txt`.
        *   **Output:** Internalized rules for writing.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Writer_Agent` - `INTERNALIZE_SECTION_REQUIREMENTS_AND_STYLE_GUIDES`).
    *   **REQ-NPC-025: Elaborate Points into Academic Prose:** The `Writer_Agent` SHALL develop key points into complete, logical paragraphs in formal academic Bahasa Indonesia, referencing literature.
        *   **Input:** Drafted key points, relevant references.
        *   **Output:** Drafted prose section.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Writer_Agent` - `ELABORATE_POINTS_INTO_ACADEMIC_PROSE`).
    *   **REQ-NPC-026: Integrate Citations Correctly:** The `Writer_Agent` SHALL accurately integrate in-text citations per specified format and `makalah-academic-style-guides.txt`.
        *   **Input:** Drafted prose, reference details.
        *   **Output:** Prose with in-text citations.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Writer_Agent` - `INTEGRATE_CITATIONS_CORRECTLY`).
    *   **REQ-NPC-027: Maintain Section Coherence & Flow:** The `Writer_Agent` SHALL ensure logical flow and smooth transitions within the written section.
        *   **Input:** Drafted prose.
        *   **Output:** Coherent drafted prose.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Writer_Agent` - `MAINTAIN_SECTION_COHERENCE_AND_FLOW`).
    *   **REQ-NPC-028: Adhere to Specific Section Style Rules:** The `Writer_Agent` SHALL apply section-specific stylistic/structural rules from `makalah-academic-style-guides.txt`.
        *   **Input:** Drafted prose, section-specific rules.
        *   **Output:** Stylistically compliant prose.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Writer_Agent` - `ADHERE_TO_SPECIFIC_SECTION_STYLE_RULES`).
    *   **REQ-NPC-029: Prepare Bibliography Data for Section:** The `Writer_Agent` SHALL identify and format reference data cited in its section for later compilation.
        *   **Input:** Cited references.
        *   **Output:** Prepared bibliography data.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Writer_Agent` - `PREPARE_BIBLIOGRAPHY_DATA_FOR_SECTION`).
    *   **REQ-NPC-030: Self-Correct Draft Against Style Guide:** The `Writer_Agent` SHALL perform internal review and correction of its draft for `makalah-academic-style-guides.txt` compliance.
        *   **Input:** Drafted prose.
        *   **Output:** Internally corrected prose.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Writer_Agent` - `SELF_CORRECT_DRAFT_AGAINST_STYLE_GUIDE`).

**3.2.5. Final Assembly**
    *   **REQ-NPC-031: Assemble Final Paper:** The system SHALL assemble all user-validated paper sections into a single, coherent document.
        *   **Input:** Validated paper sections.
        *   **Output:** Assembled paper document.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Orchestrator_Agent` - `ASSEMBLE_FINAL_PRODUCT`).
    *   **REQ-NPC-032: Compile Final Bibliography:** The system SHALL compile a unified, consistently formatted bibliography from all section-specific bibliography data, adhering to `makalah-academic-style-guides.txt`.
        *   **Input:** Prepared bibliography data from all sections.
        *   **Output:** Formatted bibliography.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Orchestrator_Agent` - `ASSEMBLE_FINAL_PRODUCT`).
    *   **REQ-NPC-033: Perform Final Overall Review:** The system SHALL perform a final automated review of the assembled paper for consistency and completeness (e.g., section order, basic formatting).
        *   **Input:** Assembled paper, formatted bibliography.
        *   **Output:** Final review status.
        *   **Source:** `sop-tools-agent-makalah#sop-am-001-root` (Step 6.3).
        
---

> Segment-ID: SRS-FR-EXISTING-PAPER-003-3
> Source-File: srs-agent-makalah
> Parent-Anchor: srs-functional-requirements
> Context: Functional requirements detailing the workflow for analyzing existing user-uploaded academic papers.

### 3.3. Existing Paper Analysis Workflow {#srs-fr-existing-paper-analysis}

This section specifies the functional requirements for the workflow of analyzing existing academic papers uploaded by the user, as orchestrated by the `Orchestrator_Agent` and executed by the `Analysis_Editor_Agent`. This workflow aligns with `sop-tools-agent-makalah#sop-am-002-root`.

**3.3.1. Document Upload & Processing**
    *   **REQ-EPA-001: Receive Uploaded Paper File:** The system SHALL be capable of receiving an uploaded academic paper file from the user.
        *   **Input:** User-uploaded file (e.g., PDF, DOCX, TXT).
        *   **Output:** File reference/path, confirmation of receipt.
        *   **Source:** `sop-tools-agent-makalah#sop-am-002-root` (Step 1.1).
    *   **REQ-EPA-002: Process Uploaded Document:** The `Analysis_Editor_Agent` SHALL access and pre-process the content of the uploaded document (e.g., text extraction from PDF, format normalization) to prepare it for analysis.
        *   **Input:** Uploaded paper file (reference/path).
        *   **Output:** Processed document text.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Analysis_Editor_Agent` - `PROCESS_UPLOADED_DOCUMENT`).
        *   **Tool Usage:** `tool-makalah-browse-files` (as specified in `sop-tools-agent-makalah#stam-tool-browse-files`).

**3.3.2. Analysis Criteria Definition**
    *   **REQ-EPA-003: Clarify Analysis Objectives:** The system SHALL engage with the user to precisely define the scope and objectives of the analysis (e.g., structural check, style evaluation, information extraction, argument review).
        *   **Input:** User request, processed document text.
        *   **Output:** Clearly defined analysis criteria (structured data).
        *   **Source:** `sop-tools-agent-makalah#sop-am-002-root` (Step 1.2), utilizes `sop-tools-agent-makalah#sop-am-003-root`.

**3.3.3. Content Analysis & Feedback Generation**
    *   **REQ-EPA-004: Initiate Analysis Task:** The system SHALL initiate an analysis task with the `Analysis_Editor_Agent` using the processed document and defined criteria.
        *   **Input:** Processed document text, analysis criteria.
        *   **Output:** Command dispatched to `Analysis_Editor_Agent`.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Orchestrator_Agent` - `RECEIVE_ANALYSIS_REQUEST_AND_DOCUMENT`).
    *   **REQ-EPA-005: Analyze Document Structure:** The `Analysis_Editor_Agent` SHALL analyze the overall structure of the document (e.g., completeness of sections, logical flow, heading formats) against academic standards or provided criteria.
        *   **Input:** Processed document text.
        *   **Output:** Structural analysis findings.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Analysis_Editor_Agent` - `ANALYZE_DOCUMENT_STRUCTURE`).
    *   **REQ-EPA-006: Evaluate Style Compliance:** The `Analysis_Editor_Agent` SHALL, if requested, evaluate the document's adherence to stylistic and structural guidelines defined in `makalah-academic-style-guides.txt`.
        *   **Input:** Processed document text, request for style evaluation.
        *   **Output:** Style compliance assessment (e.g., specific deviations).
        *   **Source:** `spec-agent-makalah-multi-agent` (`Analysis_Editor_Agent` - `EVALUATE_STYLE_COMPLIANCE`).
    *   **REQ-EPA-007: Assess Argument Strength & Coherence:** The `Analysis_Editor_Agent` SHALL evaluate the clarity, strength, evidentiary support, and logical coherence of arguments presented in the document.
        *   **Input:** Processed document text.
        *   **Output:** Argumentative analysis findings.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Analysis_Editor_Agent` - `ASSESS_ARGUMENT_STRENGTH_AND_COHERENCE`).
    *   **REQ-EPA-008: Review Methodology Soundness:** The `Analysis_Editor_Agent` SHALL, if applicable, review the methodology section for clarity, appropriateness, validity, and potential limitations.
        *   **Input:** Methodology section text.
        *   **Output:** Methodology review findings.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Analysis_Editor_Agent` - `REVIEW_METHODOLOGY_SOUNDNESS`).
    *   **REQ-EPA-009: Evaluate Findings Presentation & Discussion:** The `Analysis_Editor_Agent` SHALL assess how research findings are presented, interpreted, and discussed in relation to literature and study aims.
        *   **Input:** Findings and Discussion sections text.
        *   **Output:** Presentation and discussion evaluation.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Analysis_Editor_Agent` - `EVALUATE_FINDINGS_PRESENTATION_AND_DISCUSSION`).
    *   **REQ-EPA-010: Check Reference Consistency & Format:** The `Analysis_Editor_Agent` SHALL, if requested, review the consistency of in-text citations with the bibliography and adherence to a specified format.
        *   **Input:** Processed document text (citations, bibliography).
        *   **Output:** Reference check findings.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Analysis_Editor_Agent` - `CHECK_REFERENCE_CONSISTENCY_AND_FORMAT`).
    *   **REQ-EPA-011: Extract Specific Information:** The `Analysis_Editor_Agent` SHALL, if requested, extract specific, structured information (e.g., research questions, key findings, conclusions) from the document.
        *   **Input:** Processed document text, extraction criteria.
        *   **Output:** Extracted information (structured data).
        *   **Source:** `spec-agent-makalah-multi-agent` (`Analysis_Editor_Agent` - `EXTRACT_SPECIFIC_INFORMATION`).
    *   **REQ-EPA-012: Identify Areas for Improvement:** The `Analysis_Editor_Agent` SHALL identify specific areas requiring improvement, clarification, or further development within the document.
        *   **Input:** All analysis findings.
        *   **Output:** Identified areas for improvement.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Analysis_Editor_Agent` - `IDENTIFY_AREAS_FOR_IMPROVEMENT`).
    *   **REQ-EPA-013: Generate Analysis Report:** The `Analysis_Editor_Agent` SHALL compile a structured, clear, objective, and constructive analysis report or feedback document.
        *   **Input:** All analysis findings, identified improvement areas.
        *   **Output:** Structured analysis report.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Analysis_Editor_Agent` - `GENERATE_ANALYSIS_REPORT_OR_FEEDBACK`).

**3.3.4. Present Analysis Report and Manage Follow-up**
    *   **REQ-EPA-014: Present Analysis Report to User:** The system SHALL present the generated analysis report to the user for review.
        *   **Input:** Structured analysis report.
        *   **Output:** Displayed analysis report.
        *   **Source:** `sop-tools-agent-makalah#sop-am-002-root` (Step 3.1).
    *   **REQ-EPA-015: Manage Analysis Report Validation/Clarification:** The system SHALL manage user review of the analysis report, allowing for clarification requests and ensuring user acknowledgment.
        *   **Input:** User response to report, current clarification retry count.
        *   **Output:** User-acknowledged report OR signal for further clarification/escalation.
        *   **Source:** `sop-tools-agent-makalah#sop-am-002-root` (Step 3.2), utilizes `sop-tools-agent-makalah#sop-am-005-root`.
    *   **REQ-EPA-016: Branch to Optional Revision/Generation Tasks:** The system SHALL, upon user request, be capable of initiating new paper creation or specific revision tasks based on the analysis report.
        *   **Input:** User request for follow-up, analysis report.
        *   **Output:** Trigger for relevant new SOP (e.g., `sop-tools-agent-makalah#sop-am-001-root` for new sections) or specialized revision flow.
        *   **Source:** `sop-tools-agent-makalah#sop-am-002-root` (Step 4).
        
---

> Segment-ID: SRS-FR-TOOL-INTEG-003-4
> Source-File: srs-agent-makalah
> Parent-Anchor: srs-functional-requirements
> Context: Functional requirements detailing the integration and usage of authorized tools within Agent-Makalah.

### 3.4. Tool Integration Requirements {#srs-fr-tool-integration}

This section specifies the functional requirements for integrating and managing the authorized tools used by `Agent-Makalah`'s sub-agents. The implementation must adhere to the tool policies defined in `sop-tools-agent-makalah#stam-authorized-tools-intro`.

**3.4.1. `tool-makalah-kb-accessor` Integration**
    *   **REQ-TI-001: Access KB Content:** The system SHALL provide a mechanism for sub-agents to securely access and retrieve specific, read-only content from Makalah Framework Knowledge Bases (KBs) given a valid KB UID and Anchor ID.
        *   **Input:** KB UID, Anchor ID.
        *   **Output:** KB segment content (text/structured data) OR error.
        *   **Source:** `sop-tools-agent-makalah#stam-tool-kb-accessor`.
    *   **REQ-TI-002: Enforce Read-Only KB Access:** The system SHALL ensure that `tool-makalah-kb-accessor` only performs read operations and strictly prohibits any write, modify, or delete operations on KB files.
        *   **Input:** Attempted KB operation.
        *   **Output:** Successful read OR access denied/error for unauthorized ops.
        *   **Source:** `sop-tools-agent-makalah#stam-tool-kb-accessor` (Usage Policies).

**3.4.2. `tool-makalah-web-search` Integration**
    *   **REQ-TI-003: Execute Academic Web Search:** The system SHALL be capable of executing search queries on authorized academic databases via `tool-makalah-web-search`.
        *   **Input:** Search query (text), optional domain/database restrictions.
        *   **Output:** Raw search results (e.g., list of URLs, snippets, content).
        *   **Source:** `sop-tools-agent-makalah#stam-tool-web-search`.
    *   **REQ-TI-004: Restrict Web Search Domains:** The system SHALL enforce restrictions on the domains or databases that `tool-makalah-web-search` can access, limiting it primarily to pre-approved academic/scholarly sources.
        *   **Input:** Target domain/URL for search.
        *   **Output:** Permitted search OR access denied.
        *   **Source:** `sop-tools-agent-makalah#stam-tool-web-search` (Usage Policies).
    *   **REQ-TI-005: Prevent Malicious Web Access:** The system SHALL implement measures (e.g., URL filtering, sandboxing) to mitigate risks from accessing potentially malicious external websites.
        *   **Input:** Target URL.
        *   **Output:** Safe access OR blocked access/error.
        *   **Source:** `sop-tools-agent-makalah#stam-tool-web-search` (Usage Policies).

**3.4.3. `tool-makalah-browse-files` Integration**
    *   **REQ-TI-006: Read User-Uploaded Files:** The system SHALL enable agents to read the content of user-uploaded academic paper files using `tool-makalah-browse-files`.
        *   **Input:** Secure file reference/path for uploaded file.
        *   **Output:** File content (text/binary data).
        *   **Source:** `sop-tools-agent-makalah#stam-tool-browse-files`.
    *   **REQ-TI-007: Restrict File System Access:** The system SHALL ensure `tool-makalah-browse-files` is strictly limited to read-only access within designated, secure temporary storage and cannot access arbitrary file system paths.
        *   **Input:** File path request.
        *   **Output:** Permitted read OR access denied/error.
        *   **Source:** `sop-tools-agent-makalah#stam-tool-browse-files` (Usage Policies).

**3.4.4. `tool-makalah-python-interpreter` Integration**
    *   **REQ-TI-008: Execute Python Code in Sandbox:** The system SHALL provide a secure, sandboxed environment for `tool-makalah-python-interpreter` to execute Python code strings.
        *   **Input:** Python code string, optional input data.
        *   **Output:** Python script stdout/stderr OR execution error.
        *   **Source:** `sop-tools-agent-makalah#stam-tool-python-interpreter`.
    *   **REQ-TI-009: Enforce Sandbox Constraints:** The system SHALL strictly enforce sandbox constraints, including no network access, no general file system access, and limits on CPU, memory, and execution time for Python script execution.
        *   **Input:** Python code execution request.
        *   **Output:** Successful execution within limits OR sandbox violation/resource limit error.
        *   **Source:** `sop-tools-agent-makalah#stam-tool-python-interpreter` (Usage Policies).
    *   **REQ-TI-010: Restrict Code Origin:** The system SHALL ensure that Python code executed via `tool-makalah-python-interpreter` originates only from pre-defined, vetted scripts/libraries or from agent-generated code based on specific, validated templates, strictly prohibiting arbitrary LLM-generated code execution.
        *   **Input:** Python code string for execution.
        *   **Output:** Execution permitted OR code origin violation error.
        *   **Source:** `sop-tools-agent-makalah#stam-tool-python-interpreter` (Usage Policies).

**3.4.5. `tool-makalah-validation-module` Integration (Conceptual)**
    *   **REQ-TI-011: Perform Rule-Based Validation:** The system SHALL provide `tool-makalah-validation-module` (as an internal capability) to perform rule-based validation checks on data, formats, or structural adherence as required by agents.
        *   **Input:** Data to validate, validation rules/schema.
        *   **Output:** Validation status (Pass/Fail), list of errors if Fail.
        *   **Source:** `sop-tools-agent-makalah#stam-tool-validation-module`.
        
---

> Segment-ID: SRS-FR-ERROR-LOGGING-003-5
> Source-File: srs-agent-makalah
> Parent-Anchor: srs-functional-requirements
> Context: Functional requirements for error detection, reporting, fallback execution, and logging within Agent-Makalah.

### 3.5. Error Handling & Logging {#srs-fr-error-handling-logging}

This section specifies the functional requirements for `Agent-Makalah`'s error management and logging capabilities, ensuring system robustness and auditability. These requirements align with `sop-tools-agent-makalah#sop-am-004-root` (Sub-Agent Error Reporting and Handling Coordination).

**3.5.1. Error Detection & Reporting**
    *   **REQ-EL-001: Detect Internal Sub-Agent Errors:** The system SHALL detect errors occurring within any specialized sub-agent's execution logic (e.g., failed internal processing, inability to produce output, or validation failures).
        *   **Input:** Sub-agent internal operational status.
        *   **Output:** Internal error flag, preliminary error report.
        *   **Source:** `sop-tools-agent-makalah#sop-am-004-root` (Step 1.1).
    *   **REQ-EL-002: Report Sub-Agent Errors to Orchestrator:** The system SHALL enable any sub-agent detecting an unrecoverable error to report a structured error payload to the `Orchestrator_Agent`.
        *   **Input:** Sub-agent's error report (including V-Code, description, context).
        *   **Output:** Error report received by `Orchestrator_Agent`.
        *   **Source:** `sop-tools-agent-makalah#sop-am-004-root` (Step 2.2).
    *   **REQ-EL-003: Classify Errors:** The `Orchestrator_Agent` SHALL classify received error reports based on predefined priority levels (P1-P7) and specific V-Codes, mapping them to system-wide error definitions. (P-levels and V-Codes are defined in `sop-tools-agent-makalah`).
        *   **Input:** Sub-agent error report.
        *   **Output:** Classified error (P-level, V-Code).
        *   **Source:** `sop-tools-agent-makalah#sop-am-004-root` (Step 3).

**3.5.2. Fallback Protocol Execution**
    *   **REQ-EL-004: Initiate Fallback Protocol:** The `Orchestrator_Agent` SHALL, upon classifying an error, initiate the appropriate fallback protocol corresponding to the error's priority and context.
        *   **Input:** Classified error, current task context.
        *   **Output:** Fallback procedure triggered.
        *   **Source:** `sop-tools-agent-makalah#sop-am-004-root` (Step 4.1).
    *   **REQ-EL-005: Inform User of Errors:** The system SHALL, as part of fallback protocols, inform the user about detected errors using clear, persona-aligned messages and, where appropriate, suggest corrective actions or next steps.
        *   **Input:** Classified error.
        *   **Output:** Error message displayed to user.
        *   **Source:** `sop-tools-agent-makalah#sop-am-004-root` (Step 4.1).
    *   **REQ-EL-006: Manage Recovery/Resolution Attempts:** The system SHALL manage attempts to recover from or resolve errors, which may involve re-invoking sub-agents, requesting user input for clarification (`sop-tools-agent-makalah#sop-am-003-root`), or, in severe cases, halting the overall task.
        *   **Input:** Error state.
        *   **Output:** Task continuation, task halt, or escalation.
        *   **Source:** `sop-tools-agent-makalah#sop-am-004-root` (Step 4.2).

**3.5.3. Audit Logging**
    *   **REQ-EL-007: Log All Agent Interactions:** The system SHALL log all significant user inputs, agent outputs, and inter-agent communications, including timestamps and participant IDs.
        *   **Input:** Interaction event data.
        *   **Output:** Log entry.
        *   **Source:** `spec-agent-makalah-multi-agent` (`Orchestrator_Agent` - `LOG_INTERACTION_AND_PROCESS`).
    *   **REQ-EL-008: Log Tool Invocations:** The system SHALL log all tool invocations made by agents, including tool ID, parameters, and execution outcome (success/failure with error details).
        *   **Input:** Tool invocation data.
        *   **Output:** Log entry.
        *   **Source:** `sop-tools-agent-makalah#stam-general-tool-usage-principles` (Point 6).
    *   **REQ-EL-009: Log Error Events:** The system SHALL log all detected errors, including their classification (P-level, V-Code), source agent, contextual information, and the fallback actions taken.
        *   **Input:** Error event data.
        *   **Output:** Log entry.
        *   **Source:** `sop-tools-agent-makalah#sop-am-004-root` (Step 5.1).
    *   **REQ-EL-010: Ensure Log Traceability:** The system SHALL maintain traceability between logged events and the corresponding user session and task ID, enabling a complete audit trail of the paper creation/analysis process.
        *   **Input:** Log data.
        *   **Output:** Traceable log entries.
        *   **Source:** `prd-agent-makalah#prd-product-uniqueness` (Work Traceability).
        
---

> Segment-ID: SRS-NFR-004
> Source-File: srs-agent-makalah
> Parent-Anchor: srs-root
> Context: Specifies non-functional requirements for Agent-Makalah, detailing quality attributes and system constraints.

## 4. Non-Functional Requirements {#srs-nfr}

This section specifies the non-functional requirements (NFRs) for the `Agent-Makalah` system. These NFRs define the quality attributes and constraints that the system must satisfy to ensure its overall performance, security, usability, reliability, maintainability, deployability, and scalability. They translate the high-level non-functional requirements from `prd-agent-makalah#prd-non-functional-requirements` into more specific, measurable, and testable criteria for the MVP.

### 4.1. Performance {#srs-nfr-performance}

**4.1.1. Responsiveness**
    *   **NFR-PERF-001: Dialogue Turn Latency:** The system SHALL respond to user inputs during interactive dialogues (e.g., intent clarification, validation prompts) within **5 seconds** for 90% of requests, excluding complex LLM generation tasks.
    *   **NFR-PERF-002: Workflow Step Latency (Interactive):** The system SHALL present intermediate outputs for user validation (e.g., topic options, reference lists, outlines, drafted sections) within **15 seconds** for 90% of requests, measured from the moment the previous user input is received to the moment the output is displayed, excluding initial LLM generation time for the artifact itself.
    *   **NFR-PERF-003: Sub-Agent Task Execution Latency (Non-Interactive):** The system SHALL complete non-interactive sub-agent tasks (e.g., executing `tool-makalah-web-search`, internal processing by `Outline_Draft_Agent`) within **30 seconds** for 95% of requests.

**4.1.2. Throughput**
    *   **NFR-PERF-004: Concurrent Users (MVP):** The system SHALL support at least **10 concurrent active users** during MVP launch, capable of performing various tasks without significant degradation in responsiveness (as defined in NFR-PERF-001 and NFR-PERF-002).

### 4.2. Security {#srs-nfr-security}

**4.2.1. Data Protection**
    *   **NFR-SEC-001: Encryption at Rest:** The system SHALL encrypt all persisted user data (chat history, uploaded files, intermediate artifacts) at rest using industry-standard encryption algorithms (e.g., AES-256). (Specific data protection policies are detailed in `memory-session-agent-makalah` and `database-design-agent-makalah`).
    *   **NFR-SEC-002: Encryption in Transit:** All data transmitted between user clients, the `Agent-Makalah` backend, and integrated services SHALL be encrypted using secure communication protocols (e.g., TLS 1.2 or higher).
    *   **NFR-SEC-003: Access Control for Persisted Data:** The system SHALL implement strict role-based access control (RBAC) for all persisted user data, ensuring that only authorized agents and backend services can access specific data components for legitimate purposes. (Specific data protection policies are detailed in `memory-session-agent-makalah` and `database-design-agent-makalah`).

**4.2.2. Tool Usage Security**
    *   **NFR-SEC-004: Sandbox Isolation (Code Execution):** The `tool-makalah-python-interpreter` SHALL operate within a strictly isolated and sandboxed environment that prevents network access, general file system access, and unauthorized system calls.
    *   **NFR-SEC-005: Restricted File Access (Browsing):** The `tool-makalah-browse-files` SHALL be restricted to read-only access within predefined, secure temporary storage paths for user-uploaded files, explicitly preventing arbitrary file system navigation.
    *   **NFR-SEC-006: Web Search Domain Restrictions:** The `tool-makalah-web-search` SHALL enforce domain/URL whitelisting or strict filtering to limit access primarily to pre-approved academic/scholarly sources and mitigate risks from malicious sites.
    *   **NFR-SEC-007: Code Origin Validation (Python):** The system SHALL only execute Python code via `tool-makalah-python-interpreter` that originates from predefined, vetted scripts or agent-generated code derived from validated templates, strictly prohibiting arbitrary code execution from untrusted sources.

**4.2.3. Input Validation & Sanitization**
    *   **NFR-SEC-008: Input Sanitization:** The system SHALL sanitize all user inputs to prevent common web vulnerabilities (e.g., SQL injection, XSS) and other forms of malicious input.

**4.2.4. Agent Behavior & Output Control**
    *   **NFR-SEC-009: Harmful Content Mitigation:** The system SHALL implement mechanisms to mitigate the generation or promotion of illegal, unethical, or harmful content outside approved, controlled academic override scopes, even when operating with an LLM.

---

> Segment-ID: SRS-NFR-004-3
> Source-File: srs-agent-makalah
> Parent-Anchor: srs-root
> Context: Specifies non-functional requirements for Agent-Makalah, detailing quality attributes and system constraints. (Continued)

### 4.3. Usability {#srs-nfr-usability}

**4.3.1. User Experience**
    *   **NFR-USAB-001: Intuitive Interaction Flow:** The system SHALL guide the user through the academic paper creation and analysis workflows in a clear, logical, and intuitive conversational manner.
    *   **NFR-USAB-002: Persona Consistency:** The `Orchestrator_Agent` SHALL maintain a consistent persona (critical/sarcastic, Bahasa Indonesia informal) across all user interactions, including clarification requests, feedback presentation, and error messages.
    *   **NFR-USAB-003: Clear Communication:** The system SHALL provide clear, unambiguous, and concise responses, including task updates, progress indicators, and status messages.

**4.3.2. Learnability**
    *   **NFR-USAB-004: Guidance for Complex Tasks:** The system SHALL provide sufficient prompts and contextual guidance during complex or multi-step tasks (e.g., during brainstorming or outline validation) to help users understand the expected input and next steps.

### 4.4. Reliability {#srs-nfr-reliability}

**4.4.1. Error Handling and Recovery**
    *   **NFR-RELI-001: Graceful Error Handling:** The system SHALL gracefully handle all anticipated errors and exceptions, preventing unhandled crashes or indefinite hangs.
    *   **NFR-RELI-002: Automated Error Reporting:** The system SHALL automatically report all detected errors (P1-P7, with V-Codes) to an internal logging system without requiring manual intervention. (P-levels and V-Codes are defined in `sop-tools-agent-makalah`).
    *   **NFR-RELI-003: Error Recovery Effectiveness:** For P3-P6 errors, the system SHALL attempt to recover or provide explicit recovery options to the user, with a success rate of at least 80% for user-recoverable errors. (P-levels are defined in `sop-tools-agent-makalah`).
    *   **NFR-RELI-004: Data Integrity on Error:** The system SHALL ensure that data corruption is prevented or detected during error conditions, maintaining the integrity of persisted conversation history and intermediate artifacts.

**4.4.2. Uptime**
    *   **NFR-RELI-005: System Availability (MVP):** The `Agent-Makalah` system SHALL be available for users at least **95%** of the time, excluding scheduled maintenance.

**4.4.3. Consistency**
    *   **NFR-RELI-006: Output Consistency:** For identical inputs and contexts, the system SHALL produce functionally identical or highly similar outputs (e.g., outlines, analysis reports) in at least 90% of cases, assuming the underlying LLM's stochasticity is managed.
    *   **NFR-RELI-007: Stylistic Consistency:** The system SHALL maintain consistent adherence to `makalah-academic-style-guides.txt` across all generated academic prose outputs for similar sections or tasks.

### 4.5. Maintainability {#srs-nfr-maintainability}

**4.5.1. Code Quality & Modularity**
    *   **NFR-MAINT-001: Modular Architecture:** The system SHALL adhere to a modular, multi-agent architecture as designed, ensuring clear separation of concerns for easier maintenance and upgrades.
    *   **NFR-MAINT-002: Code Standards:** All code SHALL adhere to agreed-upon coding standards, conventions, and best practices (e.g., PEP 8 for Python, clear documentation/docstrings).
    *   **NFR-MAINT-003: Testability:** Individual agents and core system components SHALL be designed to be independently testable (unit, integration tests).

**4.5.2. Logging & Debugging**
    *   **NFR-MAINT-004: Comprehensive Logging:** The system SHALL provide comprehensive, structured logging for all key operations, inter-agent communications, tool invocations, and error events to facilitate debugging and monitoring.
    *   **NFR-MAINT-005: Debugging Support:** The system SHALL support local debugging capabilities leveraging ADK's development tools.

### 4.6. Deployability {#srs-nfr-deployability}

**4.6.1. Deployment Automation**
    *   **NFR-DEPL-001: Containerization:** All `Agent-Makalah` components (sub-agents) SHALL be containerized (e.g., Docker) to ensure consistent deployment across environments.
    *   **NFR-DEPL-002: Cloud Platform Compatibility:** The system SHALL be deployable on Google Cloud Platform (GCP), leveraging containerization for ease of management.

### 4.7. Scalability {#srs-nfr-scalability}

**4.7.1. Agent Scaling**
    *   **NFR-SCAL-001: Horizontal Scaling (Basic MVP):** The system SHALL be designed to allow for basic horizontal scaling of compute-intensive sub-agents (e.g., `Writer_Agent`, `Literature_Search_Agent`) to handle increased concurrent requests, though precise throughput targets for scaled environments are post-MVP.

---

> Segment-ID: SRS-EI-005
> Source-File: srs-agent-makalah
> Parent-Anchor: srs-root
> Context: Specifies the external interfaces of Agent-Makalah, covering user, hardware, software, and communication interactions.

## 5. External Interface Requirements {#srs-external-interfaces}

This section specifies the interfaces between the `Agent-Makalah` system and external entities, including users, hardware, other software systems, and communication protocols.

### 5.1. User Interfaces {#srs-ei-user-interfaces}

**5.1.1. Conversational Interface**
    *   **REQ-UIF-001: Text-Based Dialogue:** The system SHALL interact with users primarily through a text-based conversational interface (e.g., chat window).
    *   **REQ-UIF-002: Persona Adherence:** All system responses, prompts, and questions SHALL strictly adhere to the `Orchestrator_Agent`'s defined persona (critical/sarcastic, Bahasa Indonesia informal) as specified in `spec-agent-makalah-multi-agent`.
    *   **REQ-UIF-003: Structured Output Presentation:** The system SHALL present complex outputs (e.g., reference lists, outlines, analysis reports) in a structured, readable format (e.g., Markdown) for clarity.
    *   **REQ-UIF-004: Progress Indicators:** The system SHALL provide clear indicators of task progress during long-running operations (e.g., "Searching literature...", "Drafting section...").
    *   **REQ-UIF-005: File Upload Mechanism:** The system SHALL provide a mechanism for users to upload academic paper files (PDF, DOCX, TXT) for analysis.

### 5.2. Hardware Interfaces {#srs-ei-hardware-interfaces}

*   **REQ-HW-001: Standard Server Hardware:** The system SHALL operate on standard cloud server hardware (e.g., virtual machines in GCP) without requiring specialized or proprietary hardware components.
*   **REQ-HW-002: Storage Access:** The system SHALL require access to persistent storage for databases (for chat history, metadata) and file storage (for uploaded documents).

### 5.3. Software Interfaces {#srs-ei-software-interfaces}

*   **REQ-SW-001: Google ADK APIs:** The system SHALL utilize Google Agent Development Kit (ADK) APIs for agent definition, orchestration, tool integration, and state management.
*   **REQ-SW-002: Large Language Model (LLM) APIs:** The system SHALL integrate with and make API calls to an external Large Language Model (LLM) service (e.g., Google Gemini, OpenAI GPT) for its core AI reasoning and generation capabilities.
*   **REQ-SW-003: Database APIs:** The system SHALL interact with a chosen database management system (DBMS) via its standard APIs for persistence of conversation history, session state, and intermediate artifacts.
*   **REQ-SW-004: External Search APIs:** The system SHALL interact with APIs of authorized academic search databases (e.g., Google Scholar, JSTOR, PubMed) via `tool-makalah-web-search`.
*   **REQ-SW-005: File Storage APIs:** The system SHALL interact with file storage APIs for secure handling of user-uploaded documents.
*   **REQ-SW-006: Internal Tool Interfaces:** The system SHALL provide well-defined internal interfaces for its authorized custom tools (`tool-makalah-kb-accessor`, `tool-makalah-browse-files`, `tool-makalah-python-interpreter`, `tool-makalah-validation-module`) to be invoked by agents.

### 5.4. Communications Interfaces {#srs-ei-communications-interfaces}

*   **REQ-COMM-001: Standard Web Protocols:** The system SHALL communicate with client applications via standard web protocols (e.g., HTTP/S, WebSockets) for real-time conversational interaction.
*   **REQ-COMM-002: Internal API Communication:** Inter-agent communication within the ADK environment SHALL occur via secure internal API calls or message passing mechanisms provided by ADK.
*   **REQ-COMM-003: External API Communication:** The system SHALL communicate with external services (LLM, search databases) using their respective standard API protocols (e.g., RESTful API calls over HTTPS).

---

> Segment-ID: SRS-OR-006
> Source-File: srs-agent-makalah
> Parent-Anchor: srs-root
> Context: Specifies other requirements not covered in previous sections, including database, installation, configuration, and documentation needs.

## 6. Other Requirements {#srs-or-other-requirements}

This section specifies various other requirements that are essential for the `Agent-Makalah` project, covering aspects not explicitly detailed in the functional, non-functional, or external interface sections.

### 6.1. Database Requirements {#srs-or-database}

*   **REQ-DB-001: Conversation History Storage:** The system SHALL use a relational database (e.g., PostgreSQL) for persistent storage of conversation history, including raw user inputs, `Orchestrator_Agent` outputs, timestamps, and session IDs.
*   **REQ-DB-002: Session State Storage:** The system SHALL utilize the ADK's `State` management, which persists to a backend data store, for storing `Agent-Makalah`'s overall session state, current SOP progress, and intermediate artifact metadata.
*   **REQ-DB-003: Artifact Metadata Storage:** The system SHALL store metadata for intermediate artifacts (e.g., definitive topic, validated reference list, outline structure, draft section versions) in the database, linked to the corresponding session ID.
*   **REQ-DB-004: Uploaded File Metadata Storage:** The system SHALL store metadata for user-uploaded files (e.g., filename, type, size, upload timestamp, internal storage path, associated user/session ID) in the database.
*   **REQ-DB-005: KB Content Management (Read-Only by Agents):** The Makalah Framework Knowledge Bases (KBs) SHALL be stored in a structured, accessible format (e.g., YAML files or a dedicated content management system) allowing read-only access by `tool-makalah-kb-accessor`. Changes to KBs are managed through a separate, controlled process, outside `Agent-Makalah`'s operational requirements.

### 6.2. Installation & Configuration Requirements {#srs-or-install-config}

*   **REQ-IC-001: Cloud-Native Deployment:** The system SHALL be deployable as a cloud-native application, leveraging containerization (e.g., Docker images for each ADK Agent) and managed services (e.g., on Google Cloud Run or GKE).
*   **REQ-IC-002: Environment Configuration:** The system SHALL allow for configurable environment variables for sensitive information (e.g., LLM API keys, database connection strings) and operational parameters (e.g., session timeout duration, max revision attempts).
*   **REQ-IC-003: Logging Configuration:** The system SHALL allow for configurable logging levels (e.g., DEBUG, INFO, WARNING, ERROR) for different modules/agents.

### 6.3. User Documentation Requirements (High-Level) {#srs-or-user-docs}

*   **REQ-UD-001: User Manual/Guide:** A comprehensive user manual SHALL be provided, explaining how to interact with `Agent-Makalah`, its capabilities, workflow expectations, and how to interpret outputs and provide effective feedback.
*   **REQ-UD-002: Ethical Usage Guidelines:** User documentation SHALL include clear guidelines on the ethical and responsible use of `Agent-Makalah` for academic purposes, emphasizing user involvement and intellectual accountability.
*   **REQ-UD-003: Privacy Policy:** A clear privacy policy SHALL be provided, detailing how user data is collected, stored, used, and protected.

### 6.4. Legal and Compliance Requirements {#srs-or-legal-compliance}

*   **REQ-LC-001: Data Privacy Compliance:** The system SHALL adhere to relevant data privacy regulations (e.g., GDPR, local privacy laws) in its handling of user personal data.
*   **REQ-LC-002: Academic Integrity:** The system SHALL incorporate features and interaction patterns designed to promote and uphold academic integrity, as a core tenet of `Agent-Makalah`'s philosophy.
*   **REQ-LC-003: Copyright Compliance:** The system SHALL be designed to operate within legal frameworks related to copyright, particularly concerning its use of web-scraped content (if applicable, for `tool-makalah-web-search`) and generated content.

---

> Segment-ID: SRS-REVISION-HIST-007
> Source-File: srs-agent-makalah
> Parent-Anchor: srs-root
> Context: Tracks the version history and changes made to this Software Requirements Specification document.

## 7. Revision History {#srs-revision-history}

| Version | Date       | Author(s)   | Summary of Changes                                                                        |
| :------ | :--------- | :---------- | :---------------------------------------------------------------------------------------- |
| 1.0     | 1 Jun 2025 | ERIK SUPIT  | Initial MVP draft of the Software Requirements Specification for `Agent-Makalah`.         |
|         |            |             |                                                                                           |
|         |            |             |                                                                                           |