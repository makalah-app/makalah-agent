UID: sop-tools-agent-makalah
Title: "Standard Operating Procedures and Authorized Tools for Agent-Makalah"
Author: "ERIK SUPIT"
Version: 1.0
Date: "1 Juni 2025"
Role: AGENT-TASK-WORKFLOW-AND-TOOL-POLICY
Status: FINAL
Domain: AGENT-OPERATION
Dependencies:
  - "spec-agent-makalah-multi-agent"
  - "makalah-academic-style-guides"
Anchors:
  - "stam-root" # Root anchor for SOP & Tools doc
  - "stam-sop-introduction"
  # SOP-AM-001 Anchors
  - "sop-am-001-root"
  - "sop-am-001-description"
  - "sop-am-001-preconditions"
  - "sop-am-001-workflow-steps"
  - "sop-am-001-step1-request-clarification"
  - "sop-am-001-step2-topic-ideation"
  - "sop-am-001-step2-sub-brainstorm-needed"
  - "sop-am-001-step2-sub-user-validation-topic"
  - "sop-am-001-step3-literature-search"
  - "sop-am-001-step3-sub-user-validation-references"
  - "sop-am-001-step4-outline-creation"
  - "sop-am-001-step4-sub-user-validation-outline"
  - "sop-am-001-step5-section-drafting"
  - "sop-am-001-step5-sub-user-validation-section"
  - "sop-am-001-step6-final-assembly"
  - "sop-am-001-step7-completion"
  - "sop-am-001-postconditions"
  - "sop-am-001-tools-referenced" # Specific tools within SOP-001 context
  - "sop-am-001-error-handling-general"
  # SOP-AM-002 Anchors
  - "sop-am-002-root"
  - "sop-am-002-description"
  - "sop-am-002-preconditions"
  - "sop-am-002-workflow-steps"
  - "sop-am-002-step1-request-file-criteria"
  - "sop-am-002-step2-file-processing-analysis"
  - "sop-am-002-step3-present-report-validation"
  - "sop-am-002-step3-sub-user-validation-analysis"
  - "sop-am-002-step4-optional-revision-generation"
  - "sop-am-002-step5-completion"
  - "sop-am-002-postconditions"
  - "sop-am-002-tools-referenced"
  - "sop-am-002-error-handling-general"
  # SOP-AM-003 Anchors
  - "sop-am-003-root"
  - "sop-am-003-description"
  - "sop-am-003-preconditions"
  - "sop-am-003-invocation"
  - "sop-am-003-workflow-steps"
  - "sop-am-003-step1-receive-raw-input"
  - "sop-am-003-step2-initial-validation-ambiguity-check"
  - "sop-am-003-step3-interactive-clarification-loop"
  - "sop-am-003-step4-final-validation-and-output"
  - "sop-am-003-postconditions"
  - "sop-am-003-tools-referenced"
  - "sop-am-003-error-handling-general"
  # SOP-AM-004 Anchors
  - "sop-am-004-root"
  - "sop-am-004-description"
  - "sop-am-004-error-classification" # NEW ANCHOR
  - "sop-am-004-preconditions"
  - "sop-am-004-triggering-conditions"
  - "sop-am-004-workflow-steps"
  - "sop-am-004-step1-error-detection-sub-agent"
  - "sop-am-004-step2-error-reporting-to-orchestrator"
  - "sop-am-004-step3-orchestrator-error-assessment"
  - "sop-am-004-step4-fallback-protocol-initiation"
  - "sop-am-004-step5-logging-and-status-update"
  - "sop-am-004-postconditions"
  - "sop-am-004-tools-referenced"
  # SOP-AM-005 Anchors (Interactive User Validation)
  - "sop-am-005-root"
  - "sop-am-005-description"
  - "sop-am-005-preconditions"
  - "sop-am-005-invocation"
  - "sop-am-005-workflow-steps"
  - "sop-am-005-step1-present-output"
  - "sop-am-005-step2-receive-user-feedback"
  - "sop-am-005-step3-process-feedback"
  - "sop-am-005-step4-handle-revision"
  - "sop-am-005-step5-handle-approval"
  - "sop-am-005-step6-handle-max-revisions"
  - "sop-am-005-postconditions"
  - "sop-am-005-tools-referenced"
  # Authorized Tools Anchors
  - "stam-authorized-tools-intro"
  - "stam-tool-kb-accessor"
  - "stam-tool-web-search"
  - "stam-tool-browse-files"
  - "stam-tool-python-interpreter"
  - "stam-tool-validation-module"
  - "stam-general-tool-usage-principles"
Tags:
  - "sop"
  - "tools"
  - "agent-makalah"
  - "workflow"
  - "policy"
  - "multi-agent"
Language: EN
Chained: true
---

---
> Segment-ID: STAM-SOP-INTRO-001
> Source-File: sop-tools-agent-makalah
> Parent-Anchor: stam-root
> Context: General introduction to the Standard Operating Procedures for Agent-Makalah.

## Standard Operating Procedures (SOPs) for `Agent-Makalah` {#stam-sop-introduction}

This document outlines the primary Standard Operating Procedures (SOPs) that govern the workflows and task execution of the `Agent-Makalah` multi-agent system and its constituent sub-agents, as defined in `spec-agent-makalah-multi-agent`. These SOPs provide step-by-step instructions to ensure consistent, efficient, and compliant operation. This document also details the authorized tools for `Agent-Makalah` and their specific usage policies.

---
> Segment-ID: SOP-AM-001-ROOT-DESC
> Source-File: sop-tools-agent-makalah
> Parent-Anchor: stam-sop-introduction
> Context: Overall description and purpose of SOP-AM-001.

## SOP-AM-001: New Paper Creation Workflow {#sop-am-001-root}

**1. SOP Description and Purpose** {#sop-am-001-description}

This Standard Operating Procedure (SOP) defines the mandatory, end-to-end workflow for the `Agent-Makalah` system to create a new academic paper. It details the sequence of operations, the roles and interactions of its constituent sub-agents (as defined in `spec-agent-makalah-multi-agent`), user validation loops, and adherence to academic standards. This workflow is primarily orchestrated by the `Orchestrator_Agent` and aims to produce a user-validated academic paper compliant with `makalah-academic-style-guides`.

**2. Pre-conditions** {#sop-am-001-preconditions}

*   The `Orchestrator_Agent` (as defined in `spec-agent-makalah-multi-agent`) must be active, initialized, and ready to receive user input.
*   All required sub-agents specified in `spec-agent-makalah-multi-agent` (`Brainstorming_Agent`, `Literature_Search_Agent`, `Outline_Draft_Agent`, `Writer_Agent`) must be available, operational, and correctly configured within the Google Agent Development Kit (ADK) environment.
*   The user must have initiated a request to create a new academic paper.
*   Access to the `makalah-academic-style-guides` Knowledge Base is available for the `Writer_Agent` and other relevant agents.

**3. Workflow Steps** {#sop-am-001-workflow-steps}

The following steps outline the new paper creation process:

**Step 1: Initial User Request Reception and Intent Clarification** {#sop-am-001-step1-request-clarification}
    *   **Primary Agent Responsible:** `Orchestrator_Agent`
    *   **Input:** User's initial, potentially free-form, request to create a new academic paper.
    *   **Process:**
        1.1. The `Orchestrator_Agent` receives the raw user request.
        1.2. The `Orchestrator_Agent` invokes `SOP-AM-003: User Input Clarification and Validation` (detailed herein) to fully understand the user's core intent, desired scope, any initial constraints, and expected output.
    *   **Output:** Clarified and validated user intent for the new paper.
    *   **Error Handling:** If intent cannot be clarified as per `SOP-AM-003` outcome, halt this SOP and report P6 error.

**Step 2: Topic Ideation and Finalization (Brainstorming Phase)** {#sop-am-001-step2-topic-ideation}
    *   **Primary Agent(s) Responsible:** `Orchestrator_Agent` (coordinator), `Brainstorming_Agent` (executor)
    *   **Input:** Clarified user intent (including initial topic idea if any) from Step 1.
    *   **Process:** {#sop-am-001-step2-sub-brainstorm-needed}
        2.1. The `Orchestrator_Agent` determines if a brainstorming session is needed.
        2.2. **If brainstorming is needed:**
            2.2.1. `Orchestrator_Agent` sends `RECEIVE_BRAINSTORMING_REQUEST` to `Brainstorming_Agent`.
            2.2.2. `Brainstorming_Agent` executes internal functions (including `EXPLORE_TOPIC_VARIATIONS_WITH_INSPIRATION_SEARCH` using `tool-makalah-web-search` for inspiration).
            2.2.3. `Brainstorming_Agent` returns proposed topic candidates to `Orchestrator_Agent`.
            2.2.4. `Orchestrator_Agent` invokes `SOP-AM-005: Interactive User Validation Procedure` (detailed herein) presenting topic options to the user.
            2.2.5. **User Validation & Revision Loop Outcome (Topic):** {#sop-am-001-step2-sub-user-validation-topic}
                a. If `SOP-AM-005` returns user approval for a topic, proceed.
                b. If `SOP-AM-005` indicates user requests revisions and max iterations (e.g., 3 for this loop) not reached, `Orchestrator_Agent` relays feedback to `Brainstorming_Agent`. Loop back to 2.2.2.
                c. If `SOP-AM-005` indicates max iterations reached without approval, `Orchestrator_Agent` triggers escalation.
        2.3. **If brainstorming is not needed:** `Orchestrator_Agent` confirms the topic with the user (may use a simplified `SOP-AM-005` for confirmation).
    *   **Output:** A single, definitive, user-validated topic.
    *   **Error Handling:** If a definitive topic cannot be established, halt SOP and report (e.g., P6/P5 error).

**Step 3: Literature Search and Reference Validation** {#sop-am-001-step3-literature-search}
    *   **Primary Agent(s) Responsible:** `Orchestrator_Agent` (coordinator), `Literature_Search_Agent` (executor)
    *   **Input:** Definitive topic from Step 2.
    *   **Process:**
        3.1. `Orchestrator_Agent` sends `RECEIVE_SEARCH_REQUEST` to `Literature_Search_Agent`.
        3.2. `Literature_Search_Agent` executes its functions (using `tool-makalah-web-search`, `tool-makalah-kb-accessor`).
        3.3. `Literature_Search_Agent` returns a structured reference list to `Orchestrator_Agent`.
        3.4. `Orchestrator_Agent` invokes `SOP-AM-005: Interactive User Validation Procedure` presenting the reference list.
        3.5. **User Validation & Revision Loop Outcome (References):** {#sop-am-001-step3-sub-user-validation-references}
            a. If `SOP-AM-005` returns approval, proceed.
            b. If `SOP-AM-005` indicates revisions needed and max iterations (e.g., 3) not reached, `Orchestrator_Agent` relays feedback. Loop back to 3.2.
            c. If `SOP-AM-005` indicates max iterations reached, `Orchestrator_Agent` escalates.
    *   **Output:** A user-validated list of academic references.
    *   **Error Handling:** If a satisfactory reference list cannot be established, halt SOP and report (e.g., P5 "Literature Search Failed").

**Step 4: Outline Creation and Draft Points Validation** {#sop-am-001-step4-outline-creation}
    *   **Primary Agent(s) Responsible:** `Orchestrator_Agent` (coordinator), `Outline_Draft_Agent` (executor)
    *   **Input:** Definitive topic (Step 2), Validated reference list (Step 3).
    *   **Process:**
        4.1. `Orchestrator_Agent` sends `RECEIVE_OUTLINE_REQUEST` to `Outline_Draft_Agent`.
        4.2. `Outline_Draft_Agent` executes its functions (using `tool-makalah-kb-accessor`).
        4.3. `Outline_Draft_Agent` returns outline and draft points to `Orchestrator_Agent`.
        4.4. `Orchestrator_Agent` invokes `SOP-AM-005: Interactive User Validation Procedure` presenting the outline.
        4.5. **User Validation & Revision Loop Outcome (Outline & Draft Points):** {#sop-am-001-step4-sub-user-validation-outline}
            a. If `SOP-AM-005` returns approval, proceed.
            b. If `SOP-AM-005` indicates revisions needed and max iterations (e.g., 3) not reached, `Orchestrator_Agent` relays feedback. Loop back to 4.2.
            c. If `SOP-AM-005` indicates max iterations reached, `Orchestrator_Agent` escalates.
    *   **Output:** A user-validated paper outline and draft key points, with reference mapping.
    *   **Error Handling:** If a satisfactory outline cannot be established, halt SOP and report (e.g., P5 "Outline Creation Failed").

**Step 5: Section-by-Section Paper Drafting and Validation** {#sop-am-001-step5-section-drafting}
    *   **Primary Agent(s) Responsible:** `Orchestrator_Agent` (coordinator), `Writer_Agent` (executor)
    *   **Input:** Definitive topic, Validated references, Validated outline with reference mapping.
    *   **Process:**
        5.1. `Orchestrator_Agent` determines the section to be written.
        5.2. `Orchestrator_Agent` sends `RECEIVE_WRITING_TASK` to `Writer_Agent`.
        5.3. `Writer_Agent` executes its functions (adhering to `makalah-academic-style-guides` via `tool-makalah-kb-accessor`, potentially using `tool-makalah-validation-module`).
        5.4. `Writer_Agent` returns the written section draft to `Orchestrator_Agent`.
        5.5. `Orchestrator_Agent` invokes `SOP-AM-005: Interactive User Validation Procedure` presenting the drafted section.
        5.6. **User Validation & Revision Loop Outcome (Drafted Section):** {#sop-am-001-step5-sub-user-validation-section}
            a. If `SOP-AM-005` returns approval, `Orchestrator_Agent` stores the section.
            b. If `SOP-AM-005` indicates revisions needed and max iterations (e.g., 3 per section) not reached, `Orchestrator_Agent` relays feedback. Loop back to 5.3.
            c. If `SOP-AM-005` indicates max iterations reached, `Orchestrator_Agent` escalates.
        5.7. Repeat steps 5.1-5.6 for all sections.
    *   **Output:** All paper sections written and user-validated.
    *   **Error Handling:** If a critical section fails validation after max revisions, halt SOP and report (e.g., P5 "Section Drafting Failed").

**Step 6: Final Assembly and Presentation** {#sop-am-001-step6-final-assembly}
    *   **Primary Agent Responsible:** `Orchestrator_Agent`
    *   **Input:** All user-validated paper sections.
    *   **Process:**
        6.1. `Orchestrator_Agent` assembles sections.
        6.2. `Orchestrator_Agent` compiles final bibliography (referencing `makalah-academic-style-guides` for formatting).
        6.3. `Orchestrator_Agent` performs final overall review.
        6.4. `Orchestrator_Agent` presents the complete final paper to the user.
    *   **Output:** The complete, assembled academic paper.
    *   **Error Handling:** If assembly fails, report P5 error.

**Step 7: SOP Completion** {#sop-am-001-step7-completion}
    *   **Primary Agent Responsible:** `Orchestrator_Agent`
    *   **Input:** User acknowledgment of final paper.
    *   **Process:** Log SOP completion.
    *   **Output:** SOP status `COMPLETED`.

**4. Post-conditions** {#sop-am-001-postconditions}
*   A new academic paper is created and presented.
*   Interactions and outputs are logged.
*   System ready for new requests.

**5. Tools Referenced (Illustrative within this SOP context)** {#sop-am-001-tools-referenced}
*   `tool-makalah-web-search` (by `Brainstorming_Agent`, `Literature_Search_Agent`)
*   `tool-makalah-kb-accessor` (by various agents)
*   `tool-makalah-validation-module` (conceptual, by `Writer_Agent`)
*(Detailed tool policies are in the "Authorized Tools for Agent-Makalah" section of this document).*

**6. Error Handling (General for this SOP)** {#sop-am-001-error-handling-general}
*   Errors at any step are managed by `Orchestrator_Agent` by invoking relevant fallback protocols as defined in `sop-tools-agent-makalah#sop-am-004-root`. User validation loops have built-in escalation.

---
> Segment-ID: SOP-AM-002-ROOT-DESC
> Source-File: sop-tools-agent-makalah
> Parent-Anchor: stam-sop-introduction
> Context: Overall description and purpose of SOP-AM-002.

## SOP-AM-002: Existing Paper Analysis Workflow {#sop-am-002-root}

**1. SOP Description and Purpose** {#sop-am-002-description}

This Standard Operating Procedure (SOP) defines the mandatory workflow for the `Agent-Makalah` system when a user uploads an existing academic paper or document for analysis, feedback, or information extraction. It details the sequence of operations, primarily involving the `Orchestrator_Agent` and the `Analysis_Editor_Agent` (as defined in `spec-agent-makalah-multi-agent`), including user interaction for defining analysis criteria and validating results.

**2. Pre-conditions** {#sop-am-002-preconditions}

*   The `Orchestrator_Agent` must be active, initialized, and ready to receive user input and file uploads.
*   The `Analysis_Editor_Agent` must be available, operational, and correctly configured.
*   The user must have initiated a request to analyze an existing document and successfully uploaded the document file in a supported format.
*   Access to `makalah-academic-style-guides` is available if style compliance analysis is requested.

**3. Workflow Steps** {#sop-am-002-workflow-steps}

The following steps outline the existing paper analysis process:

**Step 1: Receive User Request, Uploaded File, and Define Analysis Criteria** {#sop-am-002-step1-request-file-criteria}
    *   **Primary Agent Responsible:** `Orchestrator_Agent`
    *   **Input:** User's request, uploaded paper file, initial analysis instructions.
    *   **Process:**
        1.1. `Orchestrator_Agent` confirms receipt and basic validity of the uploaded file (e.g., using `tool-makalah-browse-files` for existence check).
        1.2. `Orchestrator_Agent` invokes `SOP-AM-003: User Input Clarification and Validation` to engage with the user to precisely define the scope, objectives, and specific criteria for the analysis.
    *   **Output:** Uploaded paper file (reference) and user-validated analysis criteria.
    *   **Error Handling:** If file issues or criteria cannot be clarified (per `SOP-AM-003`), halt SOP and report P6/P5 error.

**Step 2: Document Processing and Content Analysis** {#sop-am-002-step2-file-processing-analysis}
    *   **Primary Agent(s) Responsible:** `Orchestrator_Agent` (coordinator), `Analysis_Editor_Agent` (executor)
    *   **Input:** Uploaded paper file, validated analysis criteria from Step 1.
    *   **Process:**
        2.1. `Orchestrator_Agent` sends `RECEIVE_ANALYSIS_REQUEST_AND_DOCUMENT` to `Analysis_Editor_Agent` with the file and criteria.
        2.2. `Analysis_Editor_Agent` executes its internal functions (using `tool-makalah-browse-files`, `tool-makalah-kb-accessor`, optionally `tool-makalah-python-interpreter`).
        2.3. `Analysis_Editor_Agent` compiles and returns the analysis report/feedback to `Orchestrator_Agent`.
    *   **Output:** Structured analysis report/feedback.
    *   **Error Handling:** If `Analysis_Editor_Agent` fails, it reports to `Orchestrator_Agent`, which halts SOP and reports P5 error as defined in `sop-tools-agent-makalah#sop-am-004-root`.

**Step 3: Present Analysis Report and User Validation/Clarification** {#sop-am-002-step3-present-report-validation}
    *   **Primary Agent Responsible:** `Orchestrator_Agent`
    *   **Input:** Analysis report/feedback from Step 2.
    *   **Process:**
        3.1. `Orchestrator_Agent` presents the analysis report to the user.
        3.2. `Orchestrator_Agent` invokes `SOP-AM-005: Interactive User Validation Procedure` for user review and clarification requests on the report. Revisions to the analysis itself are generally not part of this loop unless it's a minor clarification of what the `Analysis_Editor_Agent` already found. {#sop-am-002-step3-sub-user-validation-analysis}
    *   **Output:** User-acknowledged or clarified analysis report.
    *   **Error Handling:** If user interaction leads to an unresolvable state (per `SOP-AM-005`), halt SOP.

**Step 4: (Optional) Initiate Revision or Generation Task Based on Analysis** {#sop-am-002-step4-optional-revision-generation}
    *   **Primary Agent Responsible:** `Orchestrator_Agent`
    *   **Input:** User-acknowledged analysis report (Step 3), new user request for follow-up actions.
    *   **Process:**
        4.1. If the user requests edits, rewrites, or new content based on the analysis.
        4.2. `Orchestrator_Agent` clarifies this new request (potentially invoking `SOP-AM-003`).
        4.3. `Orchestrator_Agent` may then initiate relevant parts of `SOP-AM-001` (e.g., tasking `Writer_Agent`) or a dedicated "Paper Revision SOP" (if defined).
    *   **Output:** Initiation of a new SOP/workflow if requested. Otherwise, skip.

**Step 5: SOP Completion** {#sop-am-002-step5-completion}
    *   **Primary Agent Responsible:** `Orchestrator_Agent`
    *   **Input:** User acknowledgment of report (Step 3) or completion of follow-up (Step 4).
    *   **Process:** Log SOP completion.
    *   **Output:** SOP status `COMPLETED`.

**4. Post-conditions** {#sop-am-002-postconditions}
*   Analysis report presented to the user.
*   Interactions logged.
*   System ready for new requests or follow-up.

**5. Tools Referenced (Illustrative within this SOP context)** {#sop-am-002-tools-referenced}
*   `tool-makalah-browse-files` (by `Analysis_Editor_Agent`, `Orchestrator_Agent`)
*   `tool-makalah-kb-accessor` (by `Analysis_Editor_Agent`)
*   `tool-makalah-python-interpreter` (optional, by `Analysis_Editor_Agent`)
*(Detailed tool policies are in the "Authorized Tools for Agent-Makalah" section of this document).*

---
> Segment-ID: SOP-AM-003-ROOT-DESC
> Source-File: sop-tools-agent-makalah
> Parent-Anchor: stam-sop-introduction
> Context: Overall description and purpose of SOP-AM-003.

## SOP-AM-003: User Input Clarification and Validation {#sop-am-003-root}

**1. SOP Description and Purpose** {#sop-am-003-description}

This Standard Operating Procedure (SOP) defines a reusable, interactive process for the `Orchestrator_Agent` (as defined in `spec-agent-makalah-multi-agent`) to clarify ambiguous user inputs, validate user-provided information against expected formats or constraints, and ensure that user intent is precisely understood before critical actions or sub-agent tasking occurs. This SOP is crucial for preventing errors due to misinterpretation and ensuring alignment with user requirements.

**2. Pre-conditions** {#sop-am-003-preconditions}

*   The `Orchestrator_Agent` is active and engaged in an interaction with the user.
*   The `Orchestrator_Agent` has received a piece of user input that requires clarification/validation.
*   The context of the interaction is available to the `Orchestrator_Agent`.

**3. Invocation** {#sop-am-003-invocation}

This SOP is typically invoked by the `Orchestrator_Agent` during various stages of other primary SOPs (like `SOP-AM-001` or `SOP-AM-002`) when initial user requests are vague, user feedback is ambiguous, or specific information needs confirmation.

**4. Workflow Steps** {#sop-am-003-workflow-steps}

**Step 1: Receive Raw User Input and Context** {#sop-am-003-step1-receive-raw-input}
    *   **Primary Agent Responsible:** `Orchestrator_Agent`
    *   **Input:** Specific raw user input needing clarification/validation, interaction context.
    *   **Process:** Identify input, access context.
    *   **Output:** User input and context ready for analysis.

**Step 2: Initial Validation and Ambiguity Check** {#sop-am-003-step2-initial-validation-ambiguity-check}
    *   **Primary Agent Responsible:** `Orchestrator_Agent`
    *   **Input:** User input and context from Step 1.
    *   **Process:**
        2.1. Internal validation: check for incompleteness, nonsensical input, mismatch with expected info type, identify specific ambiguities.
        2.2. If clear and valid, SOP may conclude, outputting validated input.
    *   **Output:** Assessment of input clarity (Clear/Valid OR Ambiguous/Invalid/Incomplete), specific issues.

**Step 3: Interactive Clarification Loop (if input is not clear/valid)** {#sop-am-003-step3-interactive-clarification-loop}
    *   **Primary Agent Responsible:** `Orchestrator_Agent`
    *   **Input:** Ambiguity assessment from Step 2.
    *   **Process:**
        3.1. Formulate specific clarification question/request to user (using defined persona).
        3.2. Present request to user.
        3.3. Receive user's new response.
        3.4. Re-evaluate new response by looping to Step 2.1.
        3.5. Loop continues until input is clear/valid OR max retries (e.g., 2-3) reached for the same ambiguity point.
    *   **Output:** Clarified user input OR status of failure to clarify.
    *   **Error Handling:** If max retries reached, escalate (e.g., P6 "User Input Unresolvable" handled by calling SOP as defined in `sop-tools-agent-makalah#sop-am-004-root`).

**Step 4: Final Validation and Output** {#sop-am-003-step4-final-validation-and-output}
    *   **Primary Agent Responsible:** `Orchestrator_Agent`
    *   **Input:** Clarified user input.
    *   **Process:** Final internal confirmation, log success.
    *   **Output:** Validated and clarified user input. SOP concludes successfully.

**5. Post-conditions** {#sop-am-003-postconditions}
*   User input is either clarified and validated OR determined unresolvable, triggering escalation.
*   Interactions logged.

**6. Tools Referenced (Illustrative within this SOP context)** {#sop-am-003-tools-referenced}
*   `tool-makalah-validation-module` (Conceptual, for internal checks)
*   `tool-makalah-kb-accessor` (For persona definitions, input format KBs)
*(Detailed tool policies are in the "Authorized Tools for Agent-Makalah" section of this document).*

---
> Segment-ID: SOP-AM-004-ROOT-DESC
> Source-File: sop-tools-agent-makalah
> Parent-Anchor: stam-sop-introduction
> Context: Overall description and purpose of SOP-AM-004.

## SOP-AM-004: Sub-Agent Error Reporting and Handling Coordination {#sop-am-004-root}

**1. SOP Description and Purpose** {#sop-am-004-description}

This SOP defines the process for sub-agents within `Agent-Makalah` to report errors to the `Orchestrator_Agent`, and how the `Orchestrator_Agent` assesses these reports and initiates appropriate fallback actions. This procedure serves as the definitive guide for `Agent-Makalah`'s error handling principles, including error classification and standard fallback protocols.

**1.1. Error Classification (P-Levels & V-Codes)** {#sop-am-004-error-classification}

All errors detected within the `Agent-Makalah` system are classified by Priority Levels (P-Levels) and may be assigned specific Violation Codes (V-Codes) for granular identification.

*   **Priority Levels (P-Levels):** Define the severity and immediate impact of an error, guiding the `Orchestrator_Agent`'s response.
    *   **P1: Critical System Failure.** System-wide outage, core functionality non-operational, data corruption risk. Requires immediate human intervention.
    *   **P2: Major Functional Impairment.** Core workflow blocked for specific users/tasks, significant data integrity risk, no immediate recovery. Requires urgent human intervention.
    *   **P3: Context Loss/Degradation.** Agent loses critical conversational or task context, leading to incoherent behavior or inability to proceed without user re-guidance. Recoverable with user input.
    *   **P4: Minor Functional Impairment.** A non-core sub-task fails, work is partially complete, or a feature is temporarily unavailable. Workaround might exist.
    *   **P5: Operational Failure.** A specific tool invocation or internal processing step fails. Recoverable through retries or alternative paths.
    *   **P6: Input/Intent Ambiguity.** User input is unclear, incomplete, or contradictory; agent cannot proceed without clarification. Recoverable through user interaction.
    *   **P7: Non-Critical Information/Warning.** An anomaly or non-blocking issue that does not prevent task completion, but should be logged or monitored.

*   **Violation Codes (V-Codes):** Provide specific identifiers for common error types, supporting detailed logging and analysis.
    *   **V-001:** Invalid User Input Format.
    *   **V-002:** Ambiguous User Intent.
    *   **V-003:** Maximum Revision Attempts Reached.
    *   **V-004:** Sub-Agent Internal Processing Error.
    *   **V-005:** LLM Generation Failure (e.g., empty response, harmful content filter).
    *   **V-006:** Tool Execution Failure (General).
    *   **V-007:** External API Call Failure (e.g., Web Search API, LLM API network error).
    *   **V-008:** Data Validation Failure (Internal content validation, e.g., generated prose fails style guide check, or generated search results are fabricated).
    *   **V-009:** File Processing Error (e.g., corrupted uploaded file, unsupported file type content).
    *   **V-010:** Insufficient Resources (e.g., memory limit hit during a task).
    *   **V-011:** Knowledge Base Access Failure (e.g., invalid KB ID/Anchor, KB file not found).
    *   **V-012:** Unhandled Exception/Unexpected Error.

**2. Pre-conditions** {#sop-am-004-preconditions}

*   `Orchestrator_Agent` and at least one sub-agent are active in a task.
*   Inter-agent communication is functional.
*   `Orchestrator_Agent` understands error classifications as defined in `sop-tools-agent-makalah#sop-am-004-error-classification`.

**3. Triggering Conditions** {#sop-am-004-triggering-conditions}

A sub-agent encounters an internal operational error it cannot resolve.

**4. Workflow Steps** {#sop-am-004-workflow-steps}

**Step 1: Error Detection within Sub-Agent** {#sop-am-004-step1-error-detection-sub-agent}
    *   **Agent Responsible:** Any specialized sub-agent.
    *   **Input:** Internal error condition.
    *   **Process:** Identify error, attempt limited internal retries (if applicable), prepare error report.
    *   **Output:** Internal error flag set, error report formulated.

**Step 2: Error Reporting to Orchestrator_Agent** {#sop-am-004-step2-error-reporting-to-orchestrator}
    *   **Agent Responsible:** Failing sub-agent.
    *   **Input:** Formulated error report.
    *   **Process:** Halt current task, send error report (including sub-agent ID, identified V-Code, description, context) to `Orchestrator_Agent`. Await instructions.
    *   **Output:** Error report transmitted.

**Step 3: Orchestrator_Agent Error Assessment and Classification** {#sop-am-004-step3-orchestrator-error-assessment}
    *   **Primary Agent Responsible:** `Orchestrator_Agent`
    *   **Input:** Error report from sub-agent.
    *   **Process:** Receive report, classify error (P-level, V-Code) based on the definitions in `sop-tools-agent-makalah#sop-am-004-error-classification`, understand task context.
    *   **Output:** Classified error and contextual understanding.

**Step 4: Fallback Protocol Initiation by Orchestrator_Agent** {#sop-am-004-step4-fallback-protocol-initiation}
    *   **Primary Agent Responsible:** `Orchestrator_Agent`
    *   **Input:** Classified error and context.
    *   **Process:** Initiate appropriate fallback protocol (e.g., inform user, attempt orchestrated retry, request user decision, escalate). Manage user interaction for fallback if needed (may invoke `SOP-AM-003` or `SOP-AM-005`).
    *   **Output:** Fallback protocol initiated; user informed; potential resolution or task halt.

**Step 5: Logging and Status Update** {#sop-am-004-step5-logging-and-status-update}
    *   **Primary Agent Responsible:** `Orchestrator_Agent`
    *   **Input:** Outcome of fallback initiation.
    *   **Process:** Log error, actions, outcome. Update overall task status.
    *   **Output:** Error and actions logged; system status updated. SOP for this error event concludes.

**5. Post-conditions** {#sop-am-004-postconditions}
*   Sub-agent error processed by `Orchestrator_Agent`.
*   Fallback initiated. User informed if necessary. Event logged. Task status updated.

---
> Segment-ID: SOP-AM-005-ROOT-DESC
> Source-File: sop-tools-agent-makalah
> Parent-Anchor: stam-sop-introduction
> Context: Overall description and purpose of SOP-AM-005 for interactive user validation.

## SOP-AM-005: Interactive User Validation Procedure {#sop-am-005-root}

**1. SOP Description and Purpose** {#sop-am-005-description}

This Standard Operating Procedure (SOP), callable by the `Orchestrator_Agent`, defines the standardized interactive process for presenting an intermediate or final output (e.g., proposed topic, reference list, drafted paper section, analysis report) to the user for validation and for handling the user's feedback, including revision requests up to a defined limit.

**2. Pre-conditions** {#sop-am-005-preconditions}

*   The `Orchestrator_Agent` is active and has an output (e.g., from a sub-agent) that requires user validation.
*   The context of the output (what it is, why it was generated) is clear to the `Orchestrator_Agent`.
*   A maximum number of revision iterations for this validation cycle is defined (e.g., 3 times, configurable by the calling SOP or system policy).

**3. Invocation** {#sop-am-005-invocation}

This SOP is invoked by the `Orchestrator_Agent` whenever an output needs explicit user approval before the main workflow can proceed. Examples:
*   After `Brainstorming_Agent` proposes topics (`SOP-AM-001`, Step 2.2.4).
*   After `Literature_Search_Agent` returns references (`SOP-AM-001`, Step 3.4).
*   After `Outline_Draft_Agent` returns an outline (`SOP-AM-001`, Step 4.4).
*   After `Writer_Agent` returns a drafted section (`SOP-AM-001`, Step 5.5).
*   After `Analysis_Editor_Agent` returns an analysis report (`SOP-AM-002`, Step 3.1).

**4. Workflow Steps** {#sop-am-005-workflow-steps}

**Step 1: Present Output and Request Validation** {#sop-am-005-step1-present-output}
    *   **Primary Agent Responsible:** `Orchestrator_Agent`
    *   **Input:** The specific output to be validated, context of the output.
    *   **Process:**
        1.1. The `Orchestrator_Agent` clearly presents the output to the user, using its defined persona.
        1.2. The `Orchestrator_Agent` explicitly requests the user to validate the output (e.g., "Is this topic suitable?", "Are these references relevant?", "Does this drafted section meet your expectations? Please provide feedback or approval."). It may also state the current revision attempt number if it's a loop.
    *   **Output:** Output presented to user, validation requested.

**Step 2: Receive and Parse User Feedback/Validation** {#sop-am-005-step2-receive-user-feedback}
    *   **Primary Agent Responsible:** `Orchestrator_Agent`
    *   **Input:** User's raw response to the validation request.
    *   **Process:**
        2.1. The `Orchestrator_Agent` receives the user's feedback.
        2.2. The `Orchestrator_Agent` parses the feedback to determine if it's an approval, a rejection with specific revision requests, or an ambiguous response. If ambiguous, the `Orchestrator_Agent` may invoke `SOP-AM-003: User Input Clarification and Validation` to clarify the feedback itself.
    *   **Output:** Categorized user feedback (Approval / Rejection with Revisions / Ambiguous-Clarified).

**Step 3: Process Feedback Category** {#sop-am-005-step3-process-feedback}
    *   **Primary Agent Responsible:** `Orchestrator_Agent`
    *   **Input:** Categorized user feedback.
    *   **Process:**
        3.1. **If Approval:** Proceed to Step 5 (Handle Approval).
        3.2. **If Rejection with Revisions:** Proceed to Step 4 (Handle Revision Request).
        3.3. **If Ambiguous (and could not be clarified by `SOP-AM-003` for some reason, or user is uncooperative):** Treat as a failure of this validation SOP instance, escalate to calling SOP with "UserValidationFailed" status.
    *   **Output:** Control flow directed to appropriate next step.

**Step 4: Handle Revision Request** {#sop-am-005-step4-handle-revision}
    *   **Primary Agent Responsible:** `Orchestrator_Agent`
    *   **Input:** User feedback detailing revision requests, current revision iteration count.
    *   **Process:**
        4.1. Check if the maximum number of revision iterations for this validation cycle has been reached.
        4.2. **If max iterations NOT reached:**
            a. Increment revision iteration count.
            b. This SOP concludes with a status of "RevisionsRequested" and passes the specific user feedback back to the calling SOP (e.g., `SOP-AM-001`). The calling SOP is then responsible for relaying this feedback to the appropriate sub-agent to produce a revised output, after which the calling SOP will re-invoke this validation SOP (SOP-AM-005, Step 1) with the revised output.
        4.3. **If max iterations REACHED:** Proceed to Step 6 (Handle Max Revisions Reached).
    *   **Output:** Status "RevisionsRequested" with feedback OR control flow to Step 6.

**Step 5: Handle Approval** {#sop-am-005-step5-handle-approval}
    *   **Primary Agent Responsible:** `Orchestrator_Agent`
    *   **Input:** User approval.
    *   **Process:**
        5.1. Log the user's approval for the specific output.
        5.2. This SOP concludes successfully with a status of "Approved". The calling SOP can now proceed with the validated output.
    *   **Output:** Status "Approved".

**Step 6: Handle Maximum Revisions Reached** {#sop-am-005-step6-handle-max-revisions}
    *   **Primary Agent Responsible:** `Orchestrator_Agent`
    *   **Input:** Indication that max revision iterations were reached without approval.
    *   **Process:**
        6.1. Inform the user that the maximum number of revisions has been reached for this item.
        6.2. Present user with escalation options (defined by the calling SOP or system policy), e.g.:
            a. Accept the last presented output "as-is" with reservations.
            b. Abandon the current sub-task related to this output.
            c. Suggest a more fundamental change to previous inputs/assumptions.
        6.3. Receive user's choice on how to proceed.
        6.4. This SOP concludes with a status reflecting the user's choice (e.g., "ApprovedAsIsAfterMaxRevisions", "SubTaskAbandonedByUser", "EscalationRequired"). The calling SOP handles this status accordingly.
    *   **Output:** Status indicating outcome after max revisions.

**5. Post-conditions** {#sop-am-005-postconditions}
*   The presented output has been either user-approved, user-approved-as-is-after-max-revisions, or a decision has been made to request revisions (within limit) or abandon/escalate if max revisions are hit without approval.
*   All user interactions and decisions within this validation cycle are logged.
*   The calling SOP receives a clear status to determine its next action.

**6. Tools Referenced (Illustrative within this SOP context)** {#sop-am-005-tools-referenced}
*   `tool-makalah-kb-accessor` (by `Orchestrator_Agent` for persona-consistent communication).
*   The core logic relies on the `Orchestrator_Agent`'s ability to manage dialogue and state.

---
> Segment-ID: STAM-TOOLS-006-INTRO
> Source-File: sop-tools-agent-makalah
> Parent-Anchor: stam-root
> Context: Introduction to the authorized tools section for Agent-Makalah, detailing specific tool policies.

## Authorized Tools for `Agent-Makalah` {#stam-authorized-tools-intro}

This section details the authorized tools that the `Agent-Makalah` system and its sub-agents are permitted to use. For each tool, its purpose, primary users (sub-agents within `Agent-Makalah`), key functions, and specific usage policies and constraints are defined herein. Adherence to these policies is mandatory for all operations within `Agent-Makalah`.

---
> Segment-ID: STAM-TOOLS-006-KBACC
> Source-File: sop-tools-agent-makalah
> Parent-Anchor: stam-authorized-tools-intro
> Context: Detailed policy for tool-makalah-kb-accessor within Agent-Makalah.

### Tool: `tool-makalah-kb-accessor` {#stam-tool-kb-accessor}

*   **Purpose:**
    To provide secure, read-only access to the content of Makalah Framework Knowledge Base (KB) documents. This tool is fundamental for enabling agents to operate based on defined principles, styles, procedures, and policies.
*   **Primary Users (Sub-Agents within `Agent-Makalah`):**
    *   `Orchestrator_Agent`: For accessing its own orchestration SOPs, persona definitions, error handling principles, etc.
    *   `Brainstorming_Agent`: For accessing KBs on ideation methodologies or style guides relevant to topic formulation.
    *   `Literature_Search_Agent`: For accessing `makalah-academic-style-guides` (sections on reference search guidelines, source validation, citation format principles) and this document (`sop-tools-agent-makalah` for bibliography formatting SOPs, if moved here, or a dedicated SOP).
    *   `Outline_Draft_Agent`: For accessing `makalah-academic-style-guides` (for general paper structure principles, section-specific structural guidelines).
    *   `Writer_Agent`: (Extensive usage) For continuous and strict reference to all relevant parts of `makalah-academic-style-guides` (overall style, sentence structure, forbidden elements, section-specific rules) and relevant SOPs for bibliography/citation.
    *   `Analysis_Editor_Agent`: For accessing `makalah-academic-style-guides` if style compliance analysis is requested, or other KBs defining analysis rubrics.
*   **Key Functions:**
    *   Retrieves specific KB segment content when provided with a valid `UID#AnchorID` pair.
*   **Usage Policies and Constraints within `Agent-Makalah`:**
    1.  **Read-Only Access:** Absolutely no write, modify, or delete operations are permitted on KB files via this tool.
    2.  **Authorized KBs Only:** Access is restricted to officially registered and loaded Makalah Framework KBs relevant to `Agent-Makalah`'s function.
    3.  **Valid Chaining Required:** All calls to this tool must originate from a legitimate, validated step within an active SOP. The SOP step must justify the need for KB access.
    4.  **Specific Segment Access:** Agents should request specific, anchored segments rather than entire KB documents whenever possible to maintain context relevance and efficiency.
    5.  **Output Handling:** The raw content retrieved must be processed by the calling agent; it should not be directly exposed to the end-user without appropriate formatting or synthesis by the `Orchestrator_Agent`.
    6.  **Error Handling:** Failures to access a KB (e.g., invalid UID/Anchor, file not found) must be reported as an error (typically P5 (V-011) as defined in `sop-tools-agent-makalah#sop-am-004-error-classification`) by the calling agent to the `Orchestrator_Agent` for appropriate fallback action.

---
> Segment-ID: STAM-TOOLS-006-WEBSRCH
> Source-File: sop-tools-agent-makalah
> Parent-Anchor: stam-authorized-tools-intro
> Context: Detailed policy for tool-makalah-web-search within Agent-Makalah.

### Tool: `tool-makalah-web-search` {#stam-tool-web-search}

*   **Purpose:**
    To access and retrieve content from public websites, specifically for academic research, reference searching from authorized databases, and topic inspiration gathering relevant to `Agent-Makalah` tasks.
*   **Primary Users (Sub-Agents within `Agent-Makalah`):**
    *   `Brainstorming_Agent`: For gathering inspiration and initial topic viability checks. Usage is under strict query/domain constraints to focus on ideation.
    *   `Literature_Search_Agent`: (MANDATORY) For comprehensive searching of authorized academic databases (e.g., Google Scholar, JSTOR, Scopus, Garuda, PubMed) as defined in `makalah-academic-style-guides`.
*   **Key Functions:**
    *   Fetches content from a given URL.
    *   Extracts primary textual content and relevant metadata.
    *   Executes search queries against specified search engines or academic databases.
*   **Usage Policies and Constraints within `Agent-Makalah`:**
    1.  **Authorized Domains/Sources:** Primarily restricted to pre-approved academic databases and reputable scholarly sources as listed or guided by `makalah-academic-style-guides#ref-search-authorized-sources`. General web browsing outside these defined needs is prohibited unless an explicit override is active and justified, consistent with system-wide behavioral controls as defined in `persona-prompt-agent-makalah`.
    2.  **Query Formulation:** Search queries must be formulated by the agent based on its task and not directly taken from unvalidated user input without structuring.
    3.  **Rate Limiting & Ethical Use:** Adhere to `robots.txt` and avoid aggressive scraping.
    4.  **Output Validation:** All retrieved content is untrusted. It **must** be processed and validated by the calling agent.
    5.  **Security:** Mitigate risks from accessing external websites (e.g., filter malicious URLs).
    6.  **No Direct User Output:** Raw search results must be synthesized by the agent first.
    7.  **Error Handling:** Failures (URL not found, timeout) must be reported (typically P5) to `Orchestrator_Agent`.

---
> Segment-ID: STAM-TOOLS-006-BRWSFLS
> Source-File: sop-tools-agent-makalah
> Parent-Anchor: stam-authorized-tools-intro
> Context: Detailed policy for tool-makalah-browse-files within Agent-Makalah.

### Tool: `tool-makalah-browse-files` {#stam-tool-browse-files}

*   **Purpose:**
    To allow agents, primarily `Analysis_Editor_Agent`, to access and read user-uploaded files for analysis. `Orchestrator_Agent` may use it for file verification.
*   **Primary Users (Sub-Agents within `Agent-Makalah`):**
    *   `Analysis_Editor_Agent`: (MANDATORY) For reading user-uploaded documents.
    *   `Orchestrator_Agent`: For initial file verification.
*   **Key Functions:**
    *   Reads and returns content of a user-uploaded file given a secure reference.
    *   May provide basic file metadata.
*   **Usage Policies and Constraints within `Agent-Makalah`:**
    1.  **User-Uploaded Files Only:** Exclusively for files explicitly uploaded by the user for the current task.
    2.  **Secure Handling:** Operates on securely managed files (via platform/ADK upload).
    3.  **Read-Only for Content:** No modification, writing, or deletion of user files by sub-agents.
    4.  **Supported File Types:** Restricted to relevant document formats (PDF, DOCX, DOC, TXT). Platform must validate type upon upload.
    5.  **Content Processing:** Extracted content is raw and must be processed by the agent.
    6.  **No Arbitrary File System Access:** Must not allow browsing or access outside the specific uploaded file context.
    7.  **Error Handling:** Inability to access/read must be reported (typically P5) to `Orchestrator_Agent`.

---
> Segment-ID: STAM-TOOLS-006-PYTHON
> Source-File: sop-tools-agent-makalah
> Parent-Anchor: stam-authorized-tools-intro
> Context: Detailed policy for tool-makalah-python-interpreter within Agent-Makalah.

### Tool: `tool-makalah-python-interpreter` {#stam-tool-python-interpreter}

*   **Purpose:**
    To execute Python code in a secure, sandboxed environment for computation, data manipulation, or specialized text analysis beyond native LLM or other tool capabilities.
*   **Primary Users (Sub-Agents within `Agent-Makalah`):**
    *   `Analysis_Editor_Agent` (Optional): For advanced text analytics or custom metric calculations on uploaded papers, using pre-defined, authorized scripts.
*   **Key Functions:**
    *   Accepts Python code string. Executes in sandbox. Returns stdout/stderr.
*   **Usage Policies and Constraints within `Agent-Makalah`:**
    1.  **Strict Sandboxing:** Mandatory. No network access, no general file system access, strict resource limits.
    2.  **Code Origin:** Code must NOT be improvised by LLM. Must be from pre-defined, vetted scripts/libraries or constructed by an agent from validated parameters and templates under SOP.
    3.  **Input/Output Data:** Clearly defined, structured, validated.
    4.  **Purpose Limitation:** Only for tasks genuinely needing Python's capabilities.
    5.  **No Sensitive Data in Code:** Do not embed credentials/PII in code strings.
    6.  **Error Handling:** Execution errors must be caught, logged, reported as tool failure (typically P5) to `Orchestrator_Agent`.
    7.  **Output Validation:** Script output (stdout) is raw and must be validated by calling agent.

---
> Segment-ID: STAM-TOOLS-006-VALIDMOD
> Source-File: sop-tools-agent-makalah
> Parent-Anchor: stam-authorized-tools-intro
> Context: Policy for the conceptual tool-makalah-validation-module within Agent-Makalah.

### Tool: `tool-makalah-validation-module` (Conceptual) {#stam-tool-validation-module}

*   **Purpose:**
    To provide a standardized internal mechanism for various validation tasks (data formats, structural rules, consistency).
*   **Primary Users (Sub-Agents within `Agent-Makalah`):**
    *   `Orchestrator_Agent`: For user inputs, sub-agent outputs.
    *   `Writer_Agent`: Potentially for self-correction against `makalah-academic-style-guides`.
    *   `Analysis_Editor_Agent`: For internal validation of its analysis report.
*   **Key Functions (Conceptual):**
    *   Validate data against schema. Check completeness. Verify formatting. Perform consistency checks.
*   **Usage Policies and Constraints within `Agent-Makalah`:**
    1.  **Internal Component:** Primarily an internal system capability.
    2.  **Rule-Based:** Validation rules must be explicitly defined.
    3.  **Deterministic Output:** Clear pass/fail status and list of errors.
    4.  **Not a Replacement for Complex Judgment:** Handles structural/format validation. Complex semantic/stylistic validation relies on LLM or user.
    5.  **Error Handling:** Internal failures of module itself are P5 system errors.

---
> Segment-ID: STAM-TOOLS-006-GENERALPRINC
> Source-File: sop-tools-agent-makalah
> Parent-Anchor: stam-authorized-tools-intro
> Context: Overarching principles for all tool usage within Agent-Makalah.

## General Tool Usage Principles for `Agent-Makalah` {#stam-general-tool-usage-principles}

In addition to specific tool policies, the following general principles apply to all tool usage within `Agent-Makalah`:

1.  **Authorization by SOP:** Tool use must be explicitly authorized by an active SOP step. No ad-hoc calls.
2.  **Least Privilege:** Agents access only necessary tools.
3.  **Input Validation:** Inputs to tools are validated by the calling agent.
4.  **Output Validation:** Outputs from tools are validated by the calling agent.
5.  **Error Propagation:** Tool failures are reported to `Orchestrator_Agent`.
6.  **Auditability:** All tool invocations and outcomes are logged.
7.  **No Core Framework Modification:** Tools must not modify core system files or KBs (note: `tool-makalah-kb-modifier` is not a standard operational tool for `Agent-Makalah`'s paper writing/analysis tasks, but a specialized tool for framework maintenance, typically by a `Makalah-Creator` profile. Its mention here is for clarity on framework maintenance capabilities, not an operational tool for `Agent-Makalah`).

---