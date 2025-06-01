UID: spec-agent-makalah-multi-agent
Title: Specification Document for the Agent-Makalah Multi-Agent Writing System
Author: "ERIK SUPIT"
Version: 1.0
Date: "1 Juni 2025"
Role: AGENT-SPECIFICATION
Status: FINAL
Domain: AGENT-DEFINITION
Dependencies: 
  - "makalah-academic-style-guides"
  - "sop-tools-agent-makalah" # Added dependency
  - "persona-prompt-agent-makalah" # Added dependency
  - "memory-session-agent-makalah" # Added dependency
  - "srs-agent-makalah" # Added dependency
Anchors: 
  - "samma-root"
  - "samma-introduction"
  - "samma-architecture"
  - "samma-sub-agent-definitions"
  - "samma-orchestrator-agent"
  - "samma-brainstorming-agent"
  - "samma-literature-search-agent"
  - "samma-outline-draft-agent"
  - "samma-writer-agent"
  - "samma-analysis-editor-agent"
  - "samma-inter-agent-comm"
  - "samma-adk-integration"
  - "samma-data-handling"
  - "samma-error-handling-agent"
  - "samma-security-compliance"
  - "samma-glossary"
  - "samma-revision-history"
Tags: 
  - "agent-specification"
  - "multi-agent"
  - "agent-makalah"
  - "system-design"
  - "mvp"
Language: EN
Chained: true
---

---

> Segment-ID: SAMMA-INTRO-001
> Source-File: spec-agent-makalah-multi-agent
> Parent-Anchor: samma-root
> Context: Document's overall introduction, purpose, scope, and relation to other framework documents for the MVP.

## 1. Introduction and Purpose

This document provides the initial (MVP - Minimum Viable Product) specification for the `Agent-Makalah` system, a multi-agent solution designed to assist users in the creation and analysis of academic papers. The primary audience for this document is the AI software development team responsible for building and implementing the `Agent-Makalah` system, with a foundational approach geared towards leveraging the capabilities of the Google Agent Development Kit (ADK).

The MVP scope of `Agent-Makalah` encompasses the core processes of academic paper writing, including topic ideation, literature searching, outline creation, prose generation, and the analysis of existing user-uploaded documents. The system aims to produce academic content in Bahasa Indonesia, with a foundational adherence to the stylistic and structural guidelines defined in `makalah-academic-style-guides.txt`. The system is not intended for general-purpose Q&A or tasks beyond its defined academic writing and analysis functions.

This specification serves as a foundational document for the MVP development. It defines the agent roles and core interactions within a multi-agent architecture suitable for the Google ADK. All core principles, data handling policies, error handling mechanisms, context management strategies, and tool usage policies are integral to this MVP and are detailed in their respective governing Knowledge Base documents within the Makalah Framework.

---

> Segment-ID: SAMMA-ARCH-002
> Source-File: spec-agent-makalah-multi-agent
> Parent-Anchor: samma-root
> Context: High-level system architecture of Agent-Makalah, its multi-agent nature, and ADK integration choice.

## 2. System Architecture Overview

The `Agent-Makalah` system is designed as a **multi-agent architecture**, where distinct, specialized agents collaborate to fulfill the complex tasks of academic paper writing and analysis. This modular approach allows for separation of concerns, making the system more manageable, scalable, and maintainable.

The chosen implementation framework for `Agent-Makalah` is the **Google Agent Development Kit (ADK)**. The ADK's inherent support for creating and orchestrating multiple specialized agents makes it a suitable platform for this architecture. Each core function within `Agent-Makalah` (e.g., orchestration, brainstorming, literature search, outlining, writing, editing/analysis) will be handled by a dedicated sub-agent, as detailed in Section 3. These sub-agents will operate in a coordinated manner, primarily managed by the `Orchestrator_Agent`.

The general workflow involves the `Orchestrator_Agent` receiving user requests and then delegating specific tasks to the appropriate sub-agents in a logical sequence. For instance, in a new paper creation task, the `Orchestrator_Agent` might first engage the `Brainstorming_Agent`, then the `Literature_Search_Agent` for references, followed by the `Outline_Draft_Agent` to structure the paper, and finally the `Writer_Agent` to generate the prose. For analysis tasks, the `Orchestrator_Agent` would pass user-uploaded documents to the `Analysis_Editor_Agent`. Communication and data transfer between these agents will be managed according to ADK's capabilities and defined interfaces (detailed further in Section 4).

The `Agent-Makalah` MVP design adheres to key principles such as:
*   **Modularity:** Achieved through the multi-agent design.
*   **Specialized Roles:** Each agent has a clearly defined responsibility.
*   **KB-Guided Behavior:** Agents operate under strict adherence to defined Knowledge Bases, such as `makalah-academic-style-guides.txt` for content generation.
*   **Structured Input/Output:** Where appropriate, agents aim for structured data exchange, and the `Orchestrator_Agent` manages user interaction for clarity and validation.
*   **Orchestrated Workflow:** The `Orchestrator_Agent` ensures a controlled flow of tasks.

---

> Segment-ID: SAMMA-SUBAGENT-DEF-003
> Source-File: spec-agent-makalah-multi-agent
> Parent-Anchor: samma-root
> Context: Main section for defining all core sub-agents that constitute the Agent-Makalah system.

## 3. Core Sub-Agent Definitions

This section provides detailed specifications for each specialized sub-agent within the `Agent-Makalah` multi-agent system. Each sub-agent is designed to perform a distinct set of functions, contributing to the overall goal of academic paper creation and analysis. Their interactions are primarily managed and coordinated by the `Orchestrator_Agent`.

---

> Segment-ID: SAMMA-ORCHESTRATOR-SPEC-003-1
> Source-File: spec-agent-makalah-multi-agent
> Parent-Anchor: samma-sub-agent-definitions
> Context: Detailed specification for the Orchestrator_Agent, the central coordinating agent.

### 3.1 `Orchestrator_Agent` Specification

1.  **Agent Name:** `Orchestrator_Agent`

2.  **Role Description:**
    The `Orchestrator_Agent` is the central agent responsible for managing the entire workflow of academic paper creation and analysis within the `Agent-Makalah` system. It acts as the primary interface with the user, gathers requirements, coordinates tasks among other sub-agents, facilitates user validation of intermediate outputs, and presents the final product. This agent maintains the primary interaction persona defined for `Agent-Makalah` (critically evaluative, with a sarcastic undertone as per `persona-prompt-agent-makalah`).

3.  **Detailed Functions:**
    *   `RECEIVE_USER_INITIAL_REQUEST`: Receives and parses the initial command or request from the user (e.g., "create a paper on topic X," "analyze my uploaded paper Y").
    *   `CLARIFY_USER_INTENT`: Engages in an in-depth dialogue with the user to precisely understand their needs, objectives, and any constraints. Ensures all ambiguities are resolved before proceeding. This interaction is guided by the agent's critical persona, as defined in `persona-prompt-agent-makalah`.
    *   `INITIATE_BRAINSTORMING_SESSION`: If the topic is not yet finalized or if the user requests ideation support, this function activates and interacts with the `Brainstorming_Agent` to explore, develop, and finalize the paper's topic. It receives the definitive topic output from the `Brainstorming_Agent`.
    *   `CREATE_TASK_BRIEF`: Based on the clarified user intent and the definitive topic (if a brainstorming session occurred), this function formulates detailed task briefs or commands for the relevant sub-agents (e.g., literature search commands for `Literature_Search_Agent`, writing prompts for `Writer_Agent`, or analysis parameters for `Analysis_Editor_Agent`).
    *   `MANAGE_SUB_AGENT_WORKFLOW`: Orchestrates the sequential activation and execution of other sub-agents (`Literature_Search_Agent`, `Outline_Draft_Agent`, `Writer_Agent`, `Analysis_Editor_Agent`) according to the specific task type (e.g., new paper creation workflow vs. uploaded paper analysis workflow).
    *   `VALIDATE_SUB_AGENT_OUTPUT_WITH_USER`: Receives outputs from each sub-agent (e.g., reference lists, outlines, drafted sections, analysis reports). It then presents these outputs to the user for validation, employing an interactive validation sub-procedure (referencing `sop-tools-agent-makalah#sop-am-005-root`).
    *   `MANAGE_REVISION_LOOPS`: Manages revision cycles based on user feedback. This includes enforcing a limit on revision iterations (e.g., a maximum of three iterations per stage or sub-agent output). If revisions fail to meet user satisfaction after the set limit, it triggers an escalation protocol or a decision point (e.g., accept as-is, cancel the sub-task, or suggest a fundamental revision of inputs).
    *   `ASSEMBLE_FINAL_PRODUCT`: Consolidates all validated outputs from the various sub-agents into a single, coherent final product (e.g., a complete academic paper or a comprehensive analysis report).
    *   `PRESENT_FINAL_PRODUCT_TO_USER`: Delivers the assembled final product to the user.
    *   `MAINTAIN_PRIMARY_INTERACTION_PERSONA`: Consistently employs the primary interaction persona (e.g., Bahasa Indonesia informal, sarcastic, critical, confrontational, using "Gue-Lo" pronouns, as defined in `persona-prompt-agent-makalah`) in all direct communications with the user.
    *   `HANDLE_USER_UPLOADED_PAPER_FOR_ANALYSIS`: Manages the process of receiving a paper uploaded by the user (via the platform's/ADK's file upload mechanism), passing it to the `Analysis_Editor_Agent`, and managing the subsequent analysis workflow.
    *   `LOG_INTERACTION_AND_PROCESS`: Records all significant user interactions, internal decisions, and process statuses for auditing and debugging purposes.
    *   `MANAGE_SESSION_AND_CONTEXT`: Is responsible for the overall session and context management of the user interaction, coordinating with the ADK's memory mechanisms and adhering to the principles outlined in `memory-session-agent-makalah`.
    *   `ERROR_HANDLING_COORDINATION`: Coordinates the handling of errors originating from sub-agents or internal processes, in accordance with the error handling procedures defined in `sop-tools-agent-makalah#sop-am-004-root`.

4.  **Primary Inputs Received:**
    *   From **User:** Initial commands, responses to clarification questions, validation feedback, uploaded paper files (for analysis).
    *   From **`Brainstorming_Agent`:** Definitive topic proposals or finalized topic to be used for reference searching, outlining, and drafting.
    *   From **`Literature_Search_Agent`:** Structured and cited list of academic references.
    *   From **`Outline_Draft_Agent`:** Detailed paper outline and drafted key argument points.
    *   From **`Writer_Agent`:** Drafted sections of the academic paper (e.g., Abstract, Introduction).
    *   From **`Analysis_Editor_Agent`:** Analysis reports or feedback on uploaded papers.
    *   From **System/ADK:** Error notifications, sub-agent status updates.

5.  **Primary Outputs Produced:**
    *   To **User:** Clarification questions, requests for validation, intermediate outputs from sub-agents (for validation), the final assembled product (complete paper or analysis report), error messages, status updates.
    *   To **`Brainstorming_Agent`:** Command to initiate a brainstorming session, initial topic/area of interest.
    *   To **`Literature_Search_Agent`:** Command for literature search, including the definitive topic and/or keywords.
    *   To **`Outline_Draft_Agent`:** Command to create an outline, including the definitive topic and validated references.
    *   To **`Writer_Agent`:** Command to write a specific paper section, including the relevant outline part and references.
    *   To **`Analysis_Editor_Agent`:** Command to analyze a paper, including the uploaded document file.
    *   To **System/ADK:** Commands to activate/control sub-agents, activity logs.

6.  **Dependencies on Other Agents:**
    *   Commands and receives outputs from: `Brainstorming_Agent`, `Literature_Search_Agent`, `Outline_Draft_Agent`, `Writer_Agent`, `Analysis_Editor_Agent`.
    *   Relies on the successful execution and valid output from all these sub-agents to complete its tasks.

7.  **Primary Tools Used:**
    *   `tool-makalah-validation-module` (conceptual, for internal validation of inputs/outputs).
    *   Google ADK's internal orchestration and workflow management mechanisms (e.g., ADK workflow agents, if the `Orchestrator_Agent` is implemented as such).
    *   Google ADK's inter-agent communication mechanisms.
    *   `tool-makalah-browse-files` (for handling file uploads from the user before passing to `Analysis_Editor_Agent`).
    *   `tool-makalah-kb-accessor` (for accessing KBs related to its own orchestration SOPs, persona definitions, and other internal references).
    
---

> Segment-ID: SAMMA-BRAINSTORM-SPEC-003-2
> Source-File: spec-agent-makalah-multi-agent
> Parent-Anchor: samma-sub-agent-definitions
> Context: Detailed specification for the Brainstorming_Agent, responsible for topic ideation and refinement.

### 3.2 `Brainstorming_Agent` Specification

1.  **Agent Name:** `Brainstorming_Agent`

2.  **Role Description:**
    The `Brainstorming_Agent` is a specialized agent tasked with assisting the user (facilitated by the `Orchestrator_Agent`) in exploring ideas, developing concepts, and finalizing a relevant academic paper topic that demonstrates academic potential and is supported by initial external inspiration.

3.  **Detailed Functions:**
    *   `RECEIVE_BRAINSTORMING_REQUEST`: Receives a command from the `Orchestrator_Agent` to initiate a brainstorming session, along with the user's initial topic or area of interest.
    *   `EXPLORE_TOPIC_VARIATIONS_WITH_INSPIRATION_SEARCH`: Based on the initial input, utilizes the `tool-makalah-web-search` (under strict query and domain constraints) to gather related inspiration and current trends. Subsequently, generates diverse topic variations, alternative research questions, and different or more specific perspectives.
    *   `ANALYZE_TOPIC_POTENTIAL`: Performs a brief analysis of the generated topic variations, assessing their potential novelty, relevance (based on the gathered inspiration), and a general overview of initial literature availability.
    *   `FACILITATE_IDEATION_DIALOGUE`: Provides discussion points, trigger questions, or inspirational findings to the `Orchestrator_Agent`. These are intended to be used by the `Orchestrator_Agent` to engage in further dialogue with the user to refine and mature the topic ideas. The `Brainstorming_Agent` does not interact directly with the end-user.
    *   `REFINE_TOPIC_BASED_ON_FEEDBACK`: Receives feedback (via the `Orchestrator_Agent`) on the presented topic variations and undertakes further refinement, which may include narrowing or broadening the topic scope, or conducting additional targeted inspiration searches as directed.
    *   `PROPOSE_FINAL_TOPIC_CANDIDATES`: After one or more iterations (as necessary), presents a set of the most robust, relevant, and inspiration-backed topic candidates to the `Orchestrator_Agent`.
    *   `OUTPUT_DEFINITIVE_TOPIC`: Delivers the single, definitive topic that has been agreed upon (following user validation mediated by the `Orchestrator_Agent`) as its final output.

4.  **Primary Inputs Received:**
    *   From **`Orchestrator_Agent`:** Command to start a brainstorming session, user's initial topic/area of interest, user feedback on proposed topic variations.

5.  **Primary Outputs Produced:**
    *   To **`Orchestrator_Agent`:** A list of topic variations (potentially with justifications or inspirational sources), a concise analysis of each topic's potential, discussion points for user dialogue, final topic candidates, and ultimately, the single definitive topic.

6.  **Dependencies on Other Agents:**
    *   Receives commands and feedback exclusively from the `Orchestrator_Agent`.
    *   Its output (the definitive topic) is a critical input for the `Orchestrator_Agent` to subsequently direct the `Literature_Search_Agent`.

7.  **Primary Tools Used:**
    *   `tool-makalah-kb-accessor` (for accessing any KBs related to brainstorming methodologies or ideation guidelines).
    *   `tool-makalah-web-search` (**MANDATORY** for gathering inspiration and conducting a brief analysis of topic potential. Usage is under strict query and domain limitations to prevent functional overlap with the `Literature_Search_Agent` and to maintain focus on ideation rather than in-depth literature research).
    
---

> Segment-ID: SAMMA-LITSEARCH-SPEC-003-3
> Source-File: spec-agent-makalah-multi-agent
> Parent-Anchor: samma-sub-agent-definitions
> Context: Detailed specification for the Literature_Search_Agent, responsible for academic reference retrieval.

### 3.3 `Literature_Search_Agent` Specification

1.  **Agent Name:** `Literature_Search_Agent`

2.  **Role Description:**
    The `Literature_Search_Agent` is a specialized agent responsible for conducting systematic and comprehensive academic literature searches from authorized sources. It generates summaries, extracts metadata, and creates citations based on the definitive topic provided by the `Orchestrator_Agent`.

3.  **Detailed Functions:**
    *   `RECEIVE_SEARCH_REQUEST`: Receives a literature search command from the `Orchestrator_Agent`, which includes the definitive topic and/or specific keywords.
    *   `FORMULATE_SEARCH_QUERIES`: Based on the definitive topic and provided keywords, this function breaks down and formulates effective, semantic, and efficient search queries suitable for academic databases.
    *   `EXECUTE_ACADEMIC_SEARCH`: Utilizes the `tool-makalah-web-search` to perform searches across authorized academic databases (e.g., Garuda, Google Scholar, JSTOR, Scopus, PubMed), adhering to the source priorities defined in `makalah-academic-style-guides.txt#makalah-ref-search-guide` and `makalah-academic-style-guides.txt#ref-search-authorized-sources`.
    *   `FILTER_AND_VALIDATE_RESULTS`: Filters the search results based on criteria such as relevance to the topic, source credibility (peer-reviewed status), and publication year (with a preference for the last 5 years unless a source is historically essential), as per `makalah-academic-style-guides.txt#ref-search-filtering-validation`. It actively avoids non-academic sources.
    *   `EXTRACT_REFERENCE_METADATA`: From the validated results, extracts key metadata including TITLE, AUTHOR(S) (and their affiliations/UNIVERSITY if available and relevant), PUBLICATION YEAR, journal/conference name, volume, issue, page numbers, and URL/DOI.
    *   `GENERATE_REFERENCE_SUMMARY`: For each relevant reference, creates a concise summary (abstract or key findings summary) highlighting its main contributions and its specific relevance to the given topic.
    *   `CREATE_CITATION_FORMATTED`: Generates citations in the specified format (defaulting to APA, or another format if defined and supported by the agent's KB/capabilities) for each reference. This process refers to `makalah-academic-style-guides.txt#litreview-citation-policy` and the final assembly step `sop-tools-agent-makalah#sop-am-001-step6-final-assembly` for formatting principles.
    *   `COMPILE_AND_ORDER_REFERENCE_LIST`: Gathers all processed references (metadata, summary, citation) into a structured list. The references within this list are ordered based on their assessed strength of relevance to the topic.
    *   `OUTPUT_REFERENCE_LIST_TO_ORCHESTRATOR`: Delivers the structured and ordered list of academic references to the `Orchestrator_Agent` for user validation.

4.  **Primary Inputs Received:**
    *   From **`Orchestrator_Agent`:** Command for literature search, the definitive topic, specific keywords (if any).

5.  **Primary Outputs Produced:**
    *   To **`Orchestrator_Agent`:** A structured list of academic references, ordered by relevance. Each reference item includes:
        *   Complete metadata: TITLE, AUTHOR(S) (with affiliation/UNIVERSITY if available), PUBLICATION YEAR, journal/conference name, volume, issue, pages.
        *   A summary of the literature outlining its main contribution.
        *   A brief statement on its relevance to the user's topic.
        *   A citation in the specified format.
        *   A URL/DOI for accessing the source.

6.  **Dependencies on Other Agents:**
    *   Receives commands and topic/keyword inputs from the `Orchestrator_Agent`.
    *   Its output (the list of references) is used by the `Orchestrator_Agent` for user validation and is subsequently passed to the `Outline_Draft_Agent` and `Writer_Agent`.

7.  **Primary Tools Used:**
    *   `tool-makalah-web-search` (**MANDATORY** for accessing academic databases).
    *   `tool-makalah-kb-accessor` (for accessing guidelines on reference searching, validation criteria, and citation formatting from `makalah-academic-style-guides.txt` and `sop-tools-agent-makalah`).
    
---

> Segment-ID: SAMMA-OUTDRAFT-SPEC-003-4
> Source-File: spec-agent-makalah-multi-agent
> Parent-Anchor: samma-sub-agent-definitions
> Context: Detailed specification for the Outline_Draft_Agent, responsible for creating the paper's structure and initial draft points.

### 3.4 `Outline_Draft_Agent` Specification

1.  **Agent Name:** `Outline_Draft_Agent`

2.  **Role Description:**
    The `Outline_Draft_Agent` is a specialized agent responsible for designing a logical and well-structured academic paper outline. It also creates an initial draft comprising key argument points for the outline, based on the definitive topic and the user-validated list of academic references provided by the `Orchestrator_Agent`.

3.  **Detailed Functions:**
    *   `RECEIVE_OUTLINE_REQUEST`: Receives a command from the `Orchestrator_Agent` to create an outline and draft points, along with the definitive topic and the user-validated list of academic references.
    *   `ANALYZE_TOPIC_AND_REFERENCES`: Conducts an in-depth analysis of the topic and thoroughly reviews the provided reference list to understand the scope, main arguments, key findings, and relevant evidence.
    *   `DESIGN_PAPER_STRUCTURE`: Designs a coherent and logical structure for the paper, determining the main chapters/sections, sub-sections, and the overall sequence for presenting ideas. This process refers to general principles of academic paper structure (e.g., as indicated in `makalah-academic-style-guides.txt` for common section structures like Introduction, Literature Review, Methodology, etc.) and adapts them to the specific needs of the topic.
    *   `DEVELOP_SECTION_OUTLINES`: For each planned chapter and sub-section, creates a detailed outline of key points to be discussed.
    *   `DRAFT_KEY_ARGUMENTS_AND_EVIDENCE_POINTS`: For each point within the outline, formulates an initial draft of the main arguments, claims, or evidentiary points that will be elaborated upon, referencing relevant literature from the provided list.
    *   `ENSURE_LOGICAL_FLOW_AND_COHERENCE`: Ensures a clear logical progression and coherence between sections and points within the drafted outline.
    *   `MAP_REFERENCES_TO_OUTLINE_POINTS_INTERNAL`: Internally maps specific references to the outline points they support. This mapping information is crucial for ensuring that claims are substantiated and will be passed to the `Writer_Agent` via the `Orchestrator_Agent` along with the outline.
    *   `COMPILE_STRUCTURED_OUTLINE_AND_DRAFT`: Consolidates all work into a single, structured document containing the complete outline and the drafted key points for each section.
    *   `OUTPUT_OUTLINE_DRAFT_TO_ORCHESTRATOR`: Submits the structured outline and draft points document to the `Orchestrator_Agent` for user validation.

4.  **Primary Inputs Received:**
    *   From **`Orchestrator_Agent`:** Command to create an outline, the definitive topic, the user-validated list of academic references.

5.  **Primary Outputs Produced:**
    *   To **`Orchestrator_Agent`:** A structured document containing:
        *   A detailed paper outline (chapters, sub-sections, key points).
        *   An initial draft of key arguments, claims, or evidence points for each part of the outline.
        *   Associated reference mapping information (to be passed to the `Writer_Agent`).

6.  **Dependencies on Other Agents:**
    *   Receives commands and inputs (topic, references) from the `Orchestrator_Agent`.
    *   Its output (outline, draft points, and reference mapping) is used by the `Orchestrator_Agent` for user validation and is subsequently a critical input for the `Writer_Agent`.

7.  **Primary Tools Used:**
    *   `tool-makalah-kb-accessor` (for accessing KBs related to academic outlining principles, standard paper structures from `makalah-academic-style-guides.txt`, or any SOPs relevant to outline creation).
    
---

> Segment-ID: SAMMA-WRITER-SPEC-003-5
> Source-File: spec-agent-makalah-multi-agent
> Parent-Anchor: samma-sub-agent-definitions
> Context: Detailed specification for the Writer_Agent, responsible for generating academic prose.

### 3.5 `Writer_Agent` Specification

1.  **Agent Name:** `Writer_Agent`

2.  **Role Description:**
    The `Writer_Agent` is a specialized agent responsible for elaborating the structured outline and drafted key points into complete, coherent, and formal academic prose for each section of the paper. It operates under strict adherence to the stylistic and formatting guidelines defined in `makalah-academic-style-guides.txt`.

3.  **Detailed Functions:**
    *   `RECEIVE_WRITING_TASK`: Receives a command from the `Orchestrator_Agent` to write a specific section of the academic paper (e.g., Abstract, Introduction, Literature Review, Methodology, Findings, Discussion, Conclusion). This command includes the relevant outline portion for that section, drafted key points, the validated list of academic references, and the mapping of references to outline points.
    *   `INTERNALIZE_SECTION_REQUIREMENTS_AND_STYLE_GUIDES`: Thoroughly understands the specific requirements for the assigned section (based on the outline and key points) and **mandatorily** loads and adheres to all relevant rules from `makalah-academic-style-guides.txt`. This includes general academic writing principles (e.g., inductive narrative style, sentence structure variation, vocabulary use, forbidden elements) and section-specific guidelines (e.g., `abstract-structure-mandate`, `intro-content-rules`, `findings-forbidden-elements`).
    *   `ELABORATE_POINTS_INTO_ACADEMIC_PROSE`: Develops each drafted key point from the outline into complete, logical paragraphs written in formal academic Bahasa Indonesia. Ensures all arguments are well-supported, referencing appropriate literature as indicated by the received reference mapping.
    *   `INTEGRATE_CITATIONS_CORRECTLY`: Accurately and smoothly integrates in-text citations according to the specified format (defaulting to APA), referencing `makalah-academic-style-guides.txt#litreview-citation-policy` and `sop-tools-agent-makalah#sop-am-001-step6-final-assembly` for detailed formatting rules.
    *   `MAINTAIN_SECTION_COHERENCE_AND_FLOW`: Ensures a logical flow and smooth transitions between paragraphs and sub-sections within the written section, maintaining a consistent academic tone.
    *   `ADHERE_TO_SPECIFIC_SECTION_STYLE_RULES`: Strictly applies all specific stylistic and structural rules from `makalah-academic-style-guides.txt` pertinent to the section being written (e.g., `abstract-forbidden-elements`, `intro-research-gap-focus`, `discussion-interpretation-rules`).
    *   `PREPARE_BIBLIOGRAPHY_DATA_FOR_SECTION`: Identifies all references cited within the written section and formats their data according to the final assembly step `sop-tools-agent-makalah#sop-am-001-step6-final-assembly`. This data is prepared for later compilation into a full bibliography by the `Orchestrator_Agent` or during a finalization step.
    *   `SELF_CORRECT_DRAFT_AGAINST_STYLE_GUIDE`: Performs an internal review and correction of the generated draft to ensure maximum compliance with `makalah-academic-style-guides.txt` before submission.
    *   `OUTPUT_WRITTEN_SECTION_TO_ORCHESTRATOR`: Submits the complete written draft of the assigned paper section to the `Orchestrator_Agent` for user validation.

4.  **Primary Inputs Received:**
    *   From **`Orchestrator_Agent`:** Command to write a specific paper section, the relevant outline portion, drafted key points, the validated list of academic references, and the mapping of references to outline points.

5.  **Primary Outputs Produced:**
    *   To **`Orchestrator_Agent`:** A complete, written draft of the assigned paper section in formal academic Bahasa Indonesia, including all necessary in-text citations, and prepared data for bibliography compilation. The output must strictly adhere to all relevant guidelines in `makalah-academic-style-guides.txt`.

6.  **Dependencies on Other Agents:**
    *   Receives comprehensive inputs (outline, key points, references, reference mapping) from the `Orchestrator_Agent` (originating from `Outline_Draft_Agent` and `Literature_Search_Agent`).
    *   Its output (drafted paper section) is used by the `Orchestrator_Agent` for user validation and subsequent assembly into the full paper.

7.  **Primary Tools Used:**
    *   `tool-makalah-kb-accessor` (**MANDATORY** for continuous access and strict adherence to all sections of `makalah-academic-style-guides.txt`, and for referencing `sop-tools-agent-makalah` regarding bibliography and citation formatting).
    *   `tool-makalah-validation-module` (conceptual, to assist in the `SELF_CORRECT_DRAFT_AGAINST_STYLE_GUIDE` function, if a style validation module can be practically implemented).
    
---

> Segment-ID: SAMMA-ANALYSIS-SPEC-003-6
> Source-File: spec-agent-makalah-multi-agent
> Parent-Anchor: samma-sub-agent-definitions
> Context: Detailed specification for the Analysis_Editor_Agent, responsible for analyzing and providing feedback on existing documents.

### 3.6 `Analysis_Editor_Agent` Specification

1.  **Agent Name:** `Analysis_Editor_Agent`

2.  **Role Description:**
    The `Analysis_Editor_Agent` is a specialized agent designed to perform in-depth analysis of existing academic papers or documents (uploaded by the user). It provides constructive feedback, extracts specific information, or evaluates the document against defined criteria, as directed by the `Orchestrator_Agent`.

3.  **Detailed Functions:**
    *   `RECEIVE_ANALYSIS_REQUEST_AND_DOCUMENT`: Receives a command from the `Orchestrator_Agent` to analyze a paper, along with the user-uploaded document file (in a supported format like DOC, PDF, TXT) and specific parameters or criteria for the analysis.
    *   `PROCESS_UPLOADED_DOCUMENT`: Utilizes the `tool-makalah-browse-files` to access and read the content of the uploaded document. Performs necessary pre-processing, such as text extraction from PDF files or normalization of text format, to prepare the content for analysis.
    *   `ANALYZE_DOCUMENT_STRUCTURE`: Analyzes the overall structure of the document, including the presence and completeness of standard academic sections (e.g., Abstract, Introduction, Methodology, Results, Discussion, Conclusion), logical ordering of chapters/sub-chapters, and formatting of headings, based on general academic standards or specific user-provided criteria.
    *   `ANALYZE_CONTENT_AGAINST_CRITERIA`: Conducts a detailed content analysis based on the parameters set by the `Orchestrator_Agent`. This analysis can include, but is not limited to:
        *   `EVALUATE_STYLE_COMPLIANCE`: Assessing the document's adherence to `makalah-academic-style-guides.txt`, if requested and relevant to the document type.
        *   `ASSESS_ARGUMENT_STRENGTH_AND_COHERENCE`: Evaluating the clarity, strength, evidentiary support, and logical coherence of arguments presented within the document.
        *   `REVIEW_METHODOLOGY_SOUNDNESS`: Examining the methodology section for clarity, appropriateness to the research objectives, validity, reliability, and potential limitations (if this information is present and analysis is requested).
        *   `EVALUATE_FINDINGS_PRESENTATION_AND_DISCUSSION`: Assessing how research findings are presented (e.g., clarity, use of data/visuals), interpreted, and discussed in relation to existing literature and the study's aims.
        *   `CHECK_REFERENCE_CONSISTENCY_AND_FORMAT`: Reviewing the consistency of in-text citations with the bibliography and the adherence to a specified citation format (referencing `makalah-academic-style-guides.txt#litreview-citation-policy` and `sop-tools-agent-makalah#sop-am-001-step6-final-assembly` if applicable).
    *   `EXTRACT_SPECIFIC_INFORMATION`: If instructed, extracts specific, structured information from the paper, such as identified research questions, stated research gaps, primary methodologies employed, participant/sample characteristics, key findings, main conclusions, or recommendations.
    *   `IDENTIFY_AREAS_FOR_IMPROVEMENT`: Based on the comprehensive analysis, identifies specific sections or aspects of the paper that may require improvement, clarification, or further development within the document.
    *   `GENERATE_ANALYSIS_REPORT_OR_FEEDBACK`: Compiles a structured, clear, objective, and constructive analysis report or feedback document. This report details the findings of the analysis and, if requested, provides actionable recommendations for improvement.
    *   `OUTPUT_ANALYSIS_TO_ORCHESTRATOR`: Submits the comprehensive analysis report or feedback to the `Orchestrator_Agent`.

4.  **Primary Inputs Received:**
    *   From **`Orchestrator_Agent`:** Command to analyze a document, the user-uploaded document file, specific analysis parameters or criteria (e.g., focus on methodology, style analysis, extraction of key findings).

5.  **Primary Outputs Produced:**
    *   To **`Orchestrator_Agent`:** A structured analysis report or feedback document regarding the uploaded paper. The content of this report will be tailored to the requested analysis parameters and may include:
        *   A comprehensive evaluation of the document's structure, style, argumentation, methodology, findings, and references.
        *   A list of accurately extracted key information points.
        *   Specific identification of areas needing improvement, along with concrete suggestions (if requested).

6.  **Dependencies on Other Agents:**
    *   Receives commands, document files, and analysis parameters from the `Orchestrator_Agent`.
    *   Its output (the analysis report) is used by the `Orchestrator_Agent` to be relayed to the user or as a basis for further instructions or tasks.

7.  **Primary Tools Used:**
    *   `tool-makalah-browse-files` (**MANDATORY** for accessing and reading the content of user-uploaded document files).
    *   `tool-makalah-kb-accessor` (for accessing `makalah-academic-style-guides.txt` if style analysis is required, or other KBs containing analysis criteria or editorial guidelines).
    *   `tool-makalah-python-interpreter` (optional, for executing custom text analysis scripts, performing plagiarism checks (if such a feature is developed and permitted), or handling more complex data processing from the paper's content that is beyond basic LLM analysis capabilities).
    *   `tool-makalah-validation-module` (conceptual, for internal validation of the consistency and completeness of the analysis report before submission).
    
---

> Segment-ID: SAMMA-INTERAGENT-COMM-004
> Source-File: spec-agent-makalah-multi-agent
> Parent-Anchor: samma-root
> Context: Describes how sub-agents communicate, the role of the Orchestrator_Agent in workflow management, and standard data exchange formats.

## 4. Inter-Agent Communication and Workflow

The `Agent-Makalah` system functions through the coordinated efforts of its specialized sub-agents, with the `Orchestrator_Agent` serving as the central hub for communication and workflow management. This section outlines the general principles of their interaction.

**4.1. Orchestration Model:**

The `Orchestrator_Agent` is responsible for initiating tasks, controlling the sequence of sub-agent activation, and managing the flow of data between them. It does not directly execute the core tasks of literature search, outlining, writing, or detailed analysis itself but delegates these to the respective specialized agents. The workflow is generally sequential for a given primary task (e.g., new paper creation or existing paper analysis), with the `Orchestrator_Agent` awaiting the successful completion and validated output of one sub-agent before activating the next in the chain.

**4.2. Communication Mechanism:**

Inter-agent communication within the Google Agent Development Kit (ADK) will primarily be managed through ADK's built-in mechanisms for agent interaction. This may involve:
*   **Direct Agent-to-Agent (A2A) calls:** Where the `Orchestrator_Agent` explicitly invokes functions or services exposed by the sub-agents.
*   **Message Passing/Queuing:** If ADK provides or integrates with such systems, this could be used for asynchronous task delegation and result retrieval.
*   **Shared State/Context (Managed by ADK):** Leveraging ADK's session and state management features to pass data or signal task completion.

The specific ADK mechanisms will be determined during the detailed technical design phase, but the logical flow of information will follow the inputs and outputs defined for each agent in Section 3.

**4.3. Standard Data Exchange Formats (Conceptual):**

To ensure seamless interaction, data exchanged between agents should ideally adhere to predefined, structured formats. While the exact schemas will be defined during technical design, conceptual examples include:
*   **Topic Definition:** A structured object containing the finalized topic string, keywords, and potentially a brief abstract or scope note from `Brainstorming_Agent` to `Orchestrator_Agent`.
*   **Reference List:** A list of structured objects, where each object contains fields for all extracted metadata (title, authors, year, source, URL/DOI), the generated summary, and the formatted citation, passed from `Literature_Search_Agent` to `Orchestrator_Agent`.
*   **Outline Document:** A structured document (e.g., JSON or XML representation of a hierarchical outline) containing chapters, sub-chapters, key points, and associated reference mappings, passed from `Outline_Draft_Agent` to `Orchestrator_Agent`.
*   **Drafted Section:** Text content for a paper section, along with any specific formatting requirements or metadata (like cited references within that section), passed from `Writer_Agent` to `Orchestrator_Agent`.
*   **Analysis Report:** A structured document containing findings, feedback, and extracted information, passed from `Analysis_Editor_Agent` to `Orchestrator_Agent`.

These formats will be designed to be easily parsable and usable by the receiving agent.

**4.4. Primary Workflow Examples:**

*   **Workflow 1: New Paper Creation**
    1.  User provides initial request to `Orchestrator_Agent`.
    2.  `Orchestrator_Agent` clarifies intent and (if needed) initiates `Brainstorming_Agent`.
    3.  `Brainstorming_Agent` returns definitive topic to `Orchestrator_Agent`.
    4.  `Orchestrator_Agent` tasks `Literature_Search_Agent` with the topic.
    5.  `Literature_Search_Agent` returns reference list to `Orchestrator_Agent`.
    6.  `Orchestrator_Agent` validates references with user.
    7.  `Orchestrator_Agent` tasks `Outline_Draft_Agent` with topic and validated references.
    8.  `Outline_Draft_Agent` returns outline/draft points to `Orchestrator_Agent`.
    9.  `Orchestrator_Agent` validates outline/draft points with user.
    10. `Orchestrator_Agent` tasks `Writer_Agent` section by section with outline, references, and reference mapping.
    11. `Writer_Agent` returns written section to `Orchestrator_Agent`.
    12. `Orchestrator_Agent` validates section with user (looping for revisions if necessary).
    13. Steps 10-12 repeat for all sections.
    14. `Orchestrator_Agent` assembles final paper and presents to user.

*   **Workflow 2: Existing Paper Analysis/Editing**
    1.  User uploads paper and provides analysis/editing request to `Orchestrator_Agent`.
    2.  `Orchestrator_Agent` clarifies intent and analysis criteria.
    3.  `Orchestrator_Agent` tasks `Analysis_Editor_Agent` with the paper and criteria.
    4.  `Analysis_Editor_Agent` returns analysis report/feedback to `Orchestrator_Agent`.
    5.  `Orchestrator_Agent` presents report/feedback to user.
    6.  (Optional) User requests specific revisions based on feedback. `Orchestrator_Agent` might then task `Writer_Agent` (or a more specialized editing agent if developed later) with specific sections and the feedback from `Analysis_Editor_Agent` as input.

These workflows are subject to revision loops and error handling procedures at each step, managed by the `Orchestrator_Agent`.

---

> Segment-ID: SAMMA-ADK-INTEGRATION-005
> Source-File: spec-agent-makalah-multi-agent
> Parent-Anchor: samma-root
> Context: Specifies how the Agent-Makalah multi-agent architecture and its components will be mapped to and leverage the features of the Google Agent Development Kit (ADK).

## 5. Integration with Google Agent Development Kit (ADK)

The `Agent-Makalah` system is designed to be implemented using the Google Agent Development Kit (ADK), leveraging its capabilities for building and managing modular, multi-agent systems. This section outlines the proposed integration strategy.

**5.1. Mapping Sub-Agents to ADK `Agent` Constructs:**

Each specialized sub-agent defined in Section 3 (`Orchestrator_Agent`, `Brainstorming_Agent`, `Literature_Search_Agent`, `Outline_Draft_Agent`, `Writer_Agent`, `Analysis_Editor_Agent`) will be implemented as a distinct `Agent` within the ADK framework. This allows for:
*   **Clear separation of concerns:** Each ADK `Agent` will encapsulate the logic and responsibilities of its corresponding `Agent-Makalah` sub-agent.
*   **Independent development and testing:** Individual agents can be developed, tested, and versioned more easily.
*   **Reusability:** Specialized ADK `Agent`s, once developed, could potentially be reused in other multi-agent systems if their functions are generic enough (though `Agent-Makalah` sub-agents are fairly specialized).
*   **Clearer Orchestration:** The `Orchestrator_Agent` can manage interactions with other sub-agents by invoking them as distinct entities within the ADK environment.

The specific type of ADK `Agent` (e.g., `CustomAgent`, `LlmAgent`) used for each sub-agent will depend on its primary function. For instance, `Writer_Agent` and `Brainstorming_Agent` will likely be implemented as `LlmAgent`s, while others might be `CustomAgent`s wrapping specific business logic or tool interactions.

**5.2. Orchestration within ADK:**

The `Orchestrator_Agent`, implemented as an ADK `Agent`, will be responsible for managing the overall workflow and coordinating the other sub-agents. This can be achieved in ADK through:
*   **ADK Workflow Agents:** Utilizing ADK's built-in workflow agents (e.g., Sequential, Parallel, Loop) that are ideal for expressing predefined, deterministic sequences of tasks. The `Orchestrator_Agent` could configure and trigger these workflow agents.
*   **LLM-driven Routing/Orchestration:** For more dynamic scenarios or complex decision-making in the workflow, the `Orchestrator_Agent` (as an LLM-powered ADK `Agent`) could itself determine the next sub-agent to call based on the current state and user input.
The choice between these (or a hybrid approach) will be finalized during the detailed technical design phase, based on the complexity of the orchestration logic required.

**5.3. Tool Integration with ADK's Ecosystem:**

The tools defined for `Agent-Makalah` (e.g., `tool-makalah-web-search`, `tool-makalah-browse-files`, `tool-makalah-kb-accessor`, `tool-makalah-python-interpreter`) will be integrated into the ADK environment. This can be achieved by:
*   **Implementing them as custom tools within ADK:** ADK allows developers to define and register custom functions or services as tools that agents can invoke.
*   **Utilizing ADK's native tool capabilities:** For functionalities like web search or code execution, ADK may offer built-in or easily integrable tool options that can be adapted or wrapped.
Each sub-agent will be granted access only to the specific tools required for its functions, managed through ADK's permissioning or configuration mechanisms, aligning with the tool policies defined in `sop-tools-agent-makalah`.

**5.4. Session and State Management with ADK:**

`Agent-Makalah`'s requirement for context and memory management will be supported by ADK's `Session` and `State` management features, adhering to the principles outlined in `memory-session-agent-makalah`.
*   **ADK Sessions:** Each user interaction with `Agent-Makalah` will likely correspond to an ADK `Session`.
*   **ADK State:** The `Orchestrator_Agent` will utilize ADK's state persistence mechanisms to maintain the overall progress of a task (e.g., current stage in paper writing, intermediate results from sub-agents, user validation status). Individual sub-agents might also use ADK state for their internal processing needs during their activation period.
The specific strategy for mapping context management principles (like context degradation detection and refresh triggers) to ADK's state capabilities will be a key part of the technical design, detailed in `memory-session-agent-makalah`.

**5.5. Inter-Agent Communication in ADK:**

As mentioned in Section 4.2, communication between the `Orchestrator_Agent` and other sub-agents (all implemented as ADK `Agent`s) will utilize ADK's supported inter-agent communication protocols. This ensures that data (task briefs, results, feedback) is passed reliably and efficiently.

**5.6. Deployment Considerations:**

While detailed deployment is outside the scope of this agent specification, the choice of ADK allows for flexible deployment options, including local deployment for development/testing and cloud-based deployment (e.g., on Google Cloud) for production, as supported by ADK.

**5.7. Leveraging ADK's Debugging and Observability:**

The development team will utilize ADK's local debugging UI and any observability features (logging, tracing) to facilitate development, testing, and troubleshooting of the `Agent-Makalah` system.

---

> Segment-ID: SAMMA-DATA-HANDLING-006
> Source-File: spec-agent-makalah-multi-agent
> Parent-Anchor: samma-root
> Context: Provides a high-level overview of how user data (chat history, uploaded files) will be managed, with a reference to the forthcoming detailed Data Policy document.

## 6. Data Handling and Persistence (Brief Overview)

The `Agent-Makalah` system will interact with user data, primarily in the form of chat history (user inputs and agent responses) and user-uploaded document files (e.g., papers for analysis). The management, persistence, and retention of this data are critical aspects of the system's design and will be governed by policies detailed in `memory-session-agent-makalah` and `database-design-agent-makalah`.

This section provides a conceptual overview:

**6.1. Chat History:**
*   **Persistence:** User-agent chat interactions will be persisted to maintain conversation context and for potential future reference or auditing, as permitted by the user and defined in `memory-session-agent-makalah`.
*   **Access:** The `Orchestrator_Agent` and relevant ADK session/memory mechanisms will access this history to ensure contextual continuity, guided by the principles of context management.

**6.2. User-Uploaded Files:**
*   **Purpose:** Files uploaded by the user (e.g., for analysis by the `Analysis_Editor_Agent`) will be temporarily stored to allow processing by authorized agents and tools (specifically `tool-makalah-browse-files`).
*   **Persistence & Retention:** Uploaded files will be subject to a strict retention policy (e.g., auto-deletion after a defined period, such as 24 hours post-processing, or upon session termination), as detailed in `memory-session-agent-makalah` and `database-design-agent-makalah`.
*   **Security:** Secure storage and access control mechanisms will be implemented for uploaded files.

**6.3. Data Security and Privacy:**
All data handling will be designed with security and user privacy as key considerations. Access to user data will be restricted to authorized agents and processes for legitimate task execution, in line with security requirements outlined in `srs-agent-makalah`.

---

> Segment-ID: SAMMA-ERROR-HANDLING-AGENT-007
> Source-File: spec-agent-makalah-multi-agent
> Parent-Anchor: samma-root
> Context: Outlines how errors and exceptions will be managed at the Agent-Makalah system level, referencing the comprehensive Makalah Error Handling KB.

## 7. Error Handling and Fallbacks (Agent-Level)

The `Agent-Makalah` system, being a complex multi-agent application, requires a robust error handling and fallback strategy to ensure operational stability and a predictable user experience. The comprehensive error handling policies, V-Codes, and prioritized fallback protocols are detailed in `sop-tools-agent-makalah#sop-am-004-root`. This section outlines the agent-level approach.

**7.1. Error Detection and Reporting:**
*   Each sub-agent (`Brainstorming_Agent`, `Literature_Search_Agent`, `Outline_Draft_Agent`, `Writer_Agent`, `Analysis_Editor_Agent`) is responsible for detecting errors within its own execution scope (e.g., tool failures, inability to process input, internal validation failures).
*   Upon detecting an error, a sub-agent must report the error status and relevant diagnostic information (e.g., a specific V-Code if applicable) to the `Orchestrator_Agent`. Sub-agents should generally not attempt to handle complex errors autonomously beyond simple, predefined retries for transient issues.

**7.2. Orchestrator_Agent's Role in Error Management:**
*   The `Orchestrator_Agent` acts as the primary coordinator for error handling within the `Agent-Makalah` system.
*   Upon receiving an error report from a sub-agent, or detecting an error in its own processes (e.g., workflow management failure, user validation failure), the `Orchestrator_Agent` will classify the error based on its priority (P1-P7) and V-Code (if applicable) as defined in `sop-tools-agent-makalah#sop-am-004-root`.
*   It will then initiate the appropriate fallback protocol (e.g., P6 for input ambiguity, P5 for execution failures, P3 for context loss) as mandated by `sop-tools-agent-makalah#sop-am-004-root`.

**7.3. Fallback Protocols:**
*   The fallback protocols may involve:
    *   Requesting clarification or corrected input from the user (e.g., P6 via `sop-tools-agent-makalah#sop-am-005-root`).
    *   Attempting a context refresh (P3, guided by `memory-session-agent-makalah#msam-context-degradation-recovery`).
    *   Logging the error and attempting to continue with a degraded functionality (for lower priority errors, if permissible by policy and persona).
    *   Halting the current task or sub-task and informing the user.
    *   In critical cases (P1, P2), halting system operations and indicating the need for external intervention.
*   The tone and content of error messages presented to the user will be governed by the `Orchestrator_Agent`'s persona as guided by `persona-prompt-agent-makalah`, and the severity of the error as guided by `sop-tools-agent-makalah#sop-am-004-root`.

**7.4. Adherence to Error Handling Protocols:**
The implementation of error handling within `Agent-Makalah` and its sub-agents **must** strictly adhere to the definitions, priorities, V-Codes, and fallback procedures specified in `sop-tools-agent-makalah#sop-am-004-root`. This ensures consistent and predictable error management across the Makalah Framework.

---

> Segment-ID: SAMMA-SECURITY-COMPLIANCE-008
> Source-File: spec-agent-makalah-multi-agent
> Parent-Anchor: samma-root
> Context: Highlights key security and compliance considerations for the development and operation of Agent-Makalah.

## 8. Security and Compliance Considerations

The development and operation of the `Agent-Makalah` system must incorporate security best practices and adhere to relevant compliance requirements. While detailed security architecture and compliance checklists are beyond the scope of this agent specification document, the following key considerations must be addressed during design and implementation.

**8.1. Data Security:**
*   **User-Uploaded Files:** As outlined in Section 6 and detailed in `memory-session-agent-makalah` and `database-design-agent-makalah`, user-uploaded documents must be handled securely. This includes secure storage, controlled access (e.g., only accessible by the `Analysis_Editor_Agent` via `tool-makalah-browse-files` when explicitly tasked), and secure deletion according to the defined retention policy.
*   **Chat History:** Persisted chat history must be protected against unauthorized access and modification. Database security measures (encryption at rest, access controls) should be implemented as detailed in `database-design-agent-makalah`.
*   **Data Transmission:** All data, especially user inputs and agent outputs containing potentially sensitive academic or personal information, should be transmitted over secure channels (e.g., HTTPS for web interfaces), as defined in `srs-agent-makalah`.

**8.2. Tool Usage Security:**
*   **Sandboxing:** Tools with execution capabilities, particularly `tool-makalah-python-interpreter`, must operate within a strictly sandboxed environment to prevent malicious code from affecting the host system or accessing unauthorized resources, as specified in `sop-tools-agent-makalah#stam-tool-python-interpreter`. Resource limits (CPU, memory, execution time) must be enforced.
*   **Web Search (`tool-makalah-web-search`):** Access to external websites must be managed carefully. While the primary use is for academic databases, mechanisms to prevent access to known malicious sites or unintended data scraping should be considered, potentially through domain whitelisting/blacklisting managed by `sop-tools-agent-makalah#stam-tool-web-search`.
*   **File Access (`tool-makalah-browse-files`):** This tool must be strictly limited to read-only access within user-permitted and clearly defined (e.g., whitelisted) directory paths, as specified in `sop-tools-agent-makalah#stam-tool-browse-files`. It must not allow arbitrary filesystem navigation.

**8.3. Input Validation and Sanitization:**
*   All inputs received from users or external tools must be rigorously validated and, where appropriate, sanitized to prevent injection attacks (e.g., SQL injection, cross-site scripting if a web interface is involved) or other exploits that could compromise system integrity or security. This aligns with `srs-agent-makalah#srs-nfr-security`.

**8.4. Agent Behavior and Output Control:**
*   `Agent-Makalah` aims for academic rigor. Mechanisms must be in place to ensure the agent does not inadvertently generate or promote harmful content. The `Orchestrator_Agent` plays a key role in ensuring outputs align with the active operational context and persona as defined in `persona-prompt-agent-makalah`.
*   Strict prohibitions on certain types of content remain.

**8.5. Compliance with Makalah Framework:**
*   The entire `Agent-Makalah` system, including all its sub-agents, must be developed in compliance with the overarching principles and policies of the Makalah Framework, as reflected in its governing KB documents (`srs-agent-makalah`, `sop-tools-agent-makalah`, `persona-prompt-agent-makalah`, `memory-session-agent-makalah`, etc.).

**8.6. Audit Logging:**
*   Comprehensive audit logging, as mentioned for `Orchestrator_Agent` and detailed in `memory-session-agent-makalah` and `sop-tools-agent-makalah#sop-am-004-root`, is crucial for security monitoring, incident response, and compliance verification. Logs should be securely stored and access-controlled.

**8.7. ADK Security Features:**
*   The development team should leverage any built-in security features, best practices, and guidelines provided by the Google Agent Development Kit (ADK) during implementation.

This list is not exhaustive, and a thorough security review should be part of the development lifecycle.

---

> Segment-ID: SAMMA-GLOSSARY-009
> Source-File: spec-agent-makalah-multi-agent
> Parent-Anchor: samma-root
> Context: Definitions for terms, acronyms, or specific concepts used within this Agent-Makalah specification document.

## 9. Glossary of Terms

This section defines key terms and acronyms used throughout this document to ensure clarity and consistent understanding.

*   **Agent-Makalah:** The overall multi-agent system specified in this document, designed for academic paper writing and analysis.
*   **Sub-Agent:** A specialized, individual agent within the `Agent-Makalah` system (e.g., `Orchestrator_Agent`, `Writer_Agent`).
*   **ADK (Google Agent Development Kit):** The primary software development framework chosen for implementing `Agent-Makalah`.
*   **MVP (Minimum Viable Product):** The initial, core version of `Agent-Makalah` focused on delivering fundamental functionalities.
*   **KB (Knowledge Base):** Refers to the structured documents (like this one, `makalah-academic-style-guides.txt`, etc.) that define the rules, policies, and knowledge for the Makalah Framework and its agents.
*   **Orchestration:** The process, managed by the `Orchestrator_Agent`, of coordinating the tasks and workflows of various sub-agents.
*   **Task Brief:** A set of specific instructions or parameters given by the `Orchestrator_Agent` to a sub-agent to perform a particular task.
*   **Definitive Topic:** The finalized and user-validated academic paper topic, typically an output of the `Brainstorming_Agent` or clarified by the `Orchestrator_Agent`.
*   **Academic Style Guides (`makalah-academic-style-guides.txt`):** The primary KB document dictating the stylistic, structural, and formatting rules for academic content produced by `Agent-Makalah`.

*(This glossary can be expanded as more specific terms are introduced or require definition during the detailed design and development phases).*
---

---
> Segment-ID: SAMMA-REVISION-HISTORY-010
> Source-File: spec-agent-makalah-multi-agent
> Parent-Anchor: samma-root
> Context: Tracks changes and versions of this specification document.

## 10. Revision History {#samma-revision-history}

| Version | Date       | Author(s)   | Summary of Changes                                     |
| :------ | :--------- | :---------- | :----------------------------------------------------- |
| 1.0     | 1 Jun 2025 | ERIK SUPIT  | Initial MVP draft of the agent specification document. |
|         |            |             |                                                        |
|         |            |             |                                                        |