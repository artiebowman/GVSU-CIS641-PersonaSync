# Overview

This is the prototype Software Requirements Specification (SRS) for PersonaSync™ Phase 3, the CIS 641 term project. PersonaSync lets a user write down who they are and what they are working on once, then carries that context into whatever AI tool they open. Phase 3 is the delivery client: the piece that detects the active AI tool, lets the user pick a persona, formats the context for that tool, inserts it, and logs what was shared. This document lists the first set of functional and non-functional requirements, grouped by feature. Each requirement has an ID (FR for functional, NFR for non-functional) and uses the "shall" form. The final SRS, due in December, will grow this list to at least 25 of each and add traceability tables (which connect each requirement to the design and tests that cover it) and a change management plan.

# Functional Requirements

1. Tool Detection
    1. FR1: The client app shall detect which AI tool is active in the user's browser (ChatGPT, Claude, or Gemini) within two seconds of the user opening it, and shall display the detected tool's name in the client app window.
2. Persona Picker
    1. FR2: When an AI tool is detected, the client app shall display a persona picker listing the user's personas, with the persona most recently used with that tool listed first.
3. Context Delivery
    1. FR3: When the user confirms a persona, the client app shall format that persona's confirmed context to the active tool's prompt format and character limit and shall insert the result into the tool's message box.
4. Sharing Log
    1. FR4: After every delivery, the system shall write a sharing log entry recording the persona, the AI tool, the context sent, and the date and time, and the user shall be able to view this log in the web app.

# Non-Functional Requirements

1. Tool Detection
    1. NFR1 (Operational): The client app shall run on macOS 14 or later and in Chrome 120 or later without requiring any software other than the browser and the client app itself.
2. Context Delivery
    1. NFR2 (Performance): The client app shall complete a context delivery, from the user's confirmation to the text appearing in the AI tool's message box, in three seconds or less for a persona of up to 4,000 characters.
    2. NFR4 (Cultural and Political): The system shall deliver only context the user has reviewed and confirmed, and shall never send a suggestion from an AI or a connected tool to any AI tool until the user has kept it.
3. Sharing Log
    1. NFR3 (Security): The client app shall send all requests to the PersonaSync backend over HTTPS and shall send each request with the signed-in user's credentials, so that no context is readable by anyone other than the signed-in user.

# How to Read This Document

Requirements are grouped by the feature they describe, so a feature can appear under both headings. Non-functional requirements carry the textbook category in parentheses (operational, performance, security, cultural and political). IDs are stable: FR4 stays FR4 when the list grows, so the traceability tables in the final SRS can point back to it.
