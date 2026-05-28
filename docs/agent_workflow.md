# Agent Workflow

## Master Agent vs Sub Agent Responsibilities

### Master Agent
- Receive high-level requirements from user/Boss
- Analyze and decompose tasks
- Delegate tasks to Sub Agent(s)
- Review and validate Sub Agent results
- Integrate and report to user

### Sub Agent
- Execute specific technical tasks
- Code inspection, modification, testing
- Return detailed result reports

## When Sub Agent Is Required

The following scenarios **MUST** go through Sub Agent:

1. **Code modifications** - Any add/delete/modify of code files
2. **Test execution** - Running test suites
3. **Code review** - Inspecting potential issues (type errors, design flaws)
4. **Multi-step tasks** - Workflows requiring analysis → modify → validate

## Correct Workflow Example

```
Boss: "Optimize Transaction.date field type"
    ↓
Master Agent: Analyze requirement
    ↓
Master Agent → spawn Sub Agent:
    "Inspect current Transaction model date field implementation,
     analyze issues with using str, propose improvement plan"
    ↓
Sub Agent returns analysis report
    ↓
Master Agent → spawn Sub Agent:
    "Change date: str to date: Date type,
     update all related files, run tests to ensure pass"
    ↓
Sub Agent completes modification and testing
    ↓
Master Agent reviews results
    ↓
Master Agent reports completion to Boss
```

## Anti-Patterns (To Avoid)

❌ **Wrong**:
- Boss: "date should use date type"
- Master Agent: Directly modify code → directly test → done

✅ **Correct**:
- Boss: "Optimize Transaction date field"
- Master Agent: Delegate inspection → Delegate modification → Review → Report

## Rationale

1. **Traceability** - Each task has clear executor and record
2. **Verifiability** - Sub Agent results can be reviewed
3. **Parallelism** - Multiple Sub Agents can work simultaneously
4. **Clear boundaries** - Master maintains high-level view, Sub focuses on execution
