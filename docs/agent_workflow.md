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

## Sub Agent Mandatory Workflow

**ALL Sub Agent tasks involving code changes MUST follow this exact sequence:**

```
1. Modify code
2. Run tests (see Test Requirements below)
3. Verify all tests pass
4. Commit to git
5. Return detailed result report
```

### Test Requirements

#### Backend Changes
```bash
cd backend
pytest -v
```
- Must run full pytest suite
- All tests must pass
- Check backend/status.json is updated

#### Frontend Changes
```bash
cd mobile/cashflow_mvp
flutter analyze
flutter test  # if tests exist
```
- Must run flutter analyze
- Fix all errors before commit
- Run flutter test if test files exist

### Result Report Template

Sub Agent MUST return results in this format:

```markdown
## Task Completion

### Modified Files
- file1.dart - Description of changes
- file2.py - Description of changes

### Test Results
**Backend:**
- Passed: X
- Failed: X
- Total: X
- Status: ✅ All passed / ❌ X failed

**Frontend:**
- Analyze: ✅ No issues / ❌ X issues fixed
- Tests: ✅ X passed / ❌ X failed

### Git Commit
- Hash: abc1234
- Message: "feat: description"

### Status
✅ Complete / ❌ Blocked (reason)
```

## Task Templates for Master Agent

### Backend Modification Template
```markdown
**Task: [Brief Description]**

**Required Steps:**
1. Modify code in backend/
2. Run pytest -v (MUST pass all tests)
3. Verify backend/status.json updated
4. Commit to git
5. Return: Test results + commit hash

**Acceptance Criteria:**
- All 104 tests pass
- No pytest errors
- Git commit successful
```

### Frontend Modification Template
```markdown
**Task: [Brief Description]**

**Required Steps:**
1. Modify code in mobile/cashflow_mvp/
2. Run flutter analyze (MUST have no errors)
3. Run flutter test (if tests exist)
4. Commit to git
5. Return: Analyze results + commit hash

**Acceptance Criteria:**
- flutter analyze: 0 errors
- All existing tests pass
- Git commit successful
```

### Full Stack Modification Template
```markdown
**Task: [Brief Description]**

**Required Steps:**
1. Modify backend code
2. Run pytest -v (MUST pass all tests)
3. Modify frontend code
4. Run flutter analyze (MUST have no errors)
5. Commit all changes to git
6. Return: Backend test results + frontend analyze results + commit hash

**Acceptance Criteria:**
- Backend: All tests pass
- Frontend: 0 analyze errors
- Git commit successful
```

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

❌ **Wrong**:
- Master Agent delegates code change but doesn't require test execution
- Sub Agent modifies code without running tests
- Sub Agent commits code with failing tests

✅ **Correct**:
- Boss: "Optimize Transaction date field"
- Master Agent: Delegate inspection → Delegate modification → Review → Report
- Sub Agent: Modify → Test → Verify → Commit → Report

## Rationale

1. **Traceability** - Each task has clear executor and record
2. **Verifiability** - Sub Agent results can be reviewed
3. **Parallelism** - Multiple Sub Agents can work simultaneously
4. **Clear boundaries** - Master maintains high-level view, Sub focuses on execution
5. **Quality assurance** - Tests are mandatory, not optional

## Enforcement

**Sub Agent MUST:**
- Follow the mandatory workflow sequence
- Run tests before committing
- Report test results in the required format
- Not commit code with failing tests

**Master Agent MUST:**
- Use the provided task templates
- Explicitly require test execution in task descriptions
- Verify test results before accepting completion
