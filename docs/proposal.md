Team name: PersonaSync

Team members: Artie Bowman

# Introduction

People who use more than one AI assistant re-explain who they are and what they are working on every time they switch tools. Each vendor keeps its own memory, and none of it travels. PersonaSync™ is a portable context layer that fixes this: the user authors their persona and personal context once, and that context follows them into whatever AI tool they are using. The framing is "declared, not inferred." The user writes and confirms what the system knows about them; anything an AI suggests is visibly tagged and only becomes part of the record after the user reviews and keeps it.

Phases 1 and 2 already exist and are live at app.personasync.dev. Phase 1 is the persona web app: a persona library plus four context lanes (goals, background, milestones, notes) and a scoring engine that reports how complete and consistent a context is. Phase 2 is the Personal Context Layer (PCL), a developer-facing layer exposed through MCP read tools so other tools can read a user's context in a structured way. PersonaSync is the first consumer of the PCL, not a synonym for it.

This term project is Phase 3: closing the gap between where context is stored and where people actually work. The core deliverable is a delivery client (a browser extension is the leading candidate, with a lightweight macOS menu-bar app as the alternate or follow-on) that detects which AI tool is active, lets the user pick a persona or context slice for the session, formats the context for that tool, injects it, and logs what was shared with which tool. A secondary goal is letting users capture and update context from inside a session without going back to the web app, routed through the same review-and-keep flow.

Beyond the code, the project is a vehicle for the full systems analysis and design process: system request (done, Week 3), requirements determination, use case and activity models, and a Software Requirements Specification with traceability and a change management plan. The SRS is the primary academic deliverable; the working Phase 3 client is what makes the SRS real.

# Anticipated Technologies

* Existing PersonaSync web app and PCL backend (Python, FastMCP for MCP tooling), reused rather than rebuilt
* Browser extension: Chrome Extension Manifest V3, TypeScript/JavaScript, content scripts for detecting and injecting into ChatGPT, Claude, and Gemini web UIs
* Alternate delivery client: macOS menu-bar app (Swift/SwiftUI or an Electron/Tauri shell), evaluated during requirements determination
* Model Context Protocol (MCP) for structured reads from the PCL and for future inputs from other tools (calendars, notes, voice tools)
* REST/JSON API between the client and the PersonaSync backend, with per-user auth
* SQLite/Postgres for the sharing log and persona-per-tool memory
* GitHub for source control, issues, and the SRS; draw.io for UML diagrams; Markdown for all documentation
* Hugging Face Spaces / existing hosting for demos

# Method/Approach

An iterative, use-case-driven approach following the Dennis/Wixom/Tegarden object-oriented method, scaled to a one-person team:

1. **Planning (done):** system request, feasibility, and this proposal.
2. **Analysis (Oct):** requirements determination using the live product and my own usage as the primary source, plus a short competitor review (vendor memory export/import features, MemoryLake, Echo, AI Context Flow). Produce the requirements definition (functional and non-functional), refine the use case and activity diagrams from in-class activity 2, and add class and sequence diagrams for the delivery flow.
3. **Design (late Oct–early Nov):** pick the delivery client (extension vs. menu-bar app) based on the requirements and the third-party terms-of-service constraints, define the client–backend API, and design the sharing log and persona-per-tool memory.
4. **Implementation (Nov):** build in thin vertical slices, each one a complete use case end to end (detect tool → choose persona → deliver → log), so there is always a working demo. Each slice ties back to numbered requirements for traceability.
5. **Verification and SRS (late Nov–Dec):** test each use case against its requirements, finalize the SRS (25+ functional, 25+ non-functional requirements, traceability tables, change management plan), README install instructions, and project website.

Weekly meeting minutes will be kept in /meetings. Because the team is one person, "meetings" will be a weekly planning and review session with the minutes documenting decisions, blockers, and next-week goals.

# Estimated Timeline

| Milestone | Target | Estimated effort |
|---|---|---|
| Repo setup, proposal, use case and activity diagrams | Oct 1 | Done / 1 week |
| Requirements definition (first pass, functional + non-functional) | Oct 14 | 2 weeks |
| Analysis models complete (use case descriptions, class, sequence diagrams) | Oct 28 | 2 weeks |
| Delivery client decision + API and data design | Nov 4 | 1 week |
| Vertical slice 1: detect tool + choose persona + deliver context | Nov 18 | 2 weeks |
| Vertical slice 2: sharing log + persona-per-tool memory + in-session update | Dec 2 | 2 weeks |
| SRS final, traceability, change management plan, README, website | Dec 11 | 1.5 weeks (in parallel with slices) |

# Anticipated Problems

* **One-person team.** Every role is mine, so scope has to stay tight. Mitigation: vertical slices, and the SRS takes priority over polish if time runs short.
* **Third-party terms of service and DOM changes.** ChatGPT, Claude, and Gemini web UIs change without notice and may restrict injection. Mitigation: evaluate the menu-bar app (clipboard/paste-based delivery) as a fallback that does not depend on any vendor's DOM.
* **Extension store review timelines.** Chrome Web Store review can take days to weeks. Mitigation: side-loaded developer builds for the semester demo; store submission is a stretch goal.
* **Privacy and consent.** The system handles personal goals and preferences. Mitigation: design the sharing log and review-and-keep flow in from the start and treat them as non-functional requirements, not add-ons.
* **Scope creep from the existing product.** PersonaSync has a longer roadmap (model-aware translation of context, opt-in usage data). Mitigation: anything not tied to a Phase 3 use case goes in the SRS as a future requirement, not the build.
* **Balancing this with two other graduate courses.** Mitigation: the weekly meeting/minutes cadence doubles as a forcing function for steady progress.
