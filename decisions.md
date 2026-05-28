# Decisions

## 001 - Use SQLite for MVP
Reason:
SQLite is simpler for local MVP development.

## 002 - Use FastAPI for backend
Reason:
Simple API development and easy testing.

## 003 - Agent Workflow: Master/Sub Agent Pattern
Reason:
Ensure clear responsibility separation and traceability.

Rules:
- Master Agent: Analyze, delegate, review, report
- Sub Agent: Execute specific tasks (code changes, testing, analysis)
- No direct execution by Master Agent for code modifications

See: docs/agent_workflow.md
