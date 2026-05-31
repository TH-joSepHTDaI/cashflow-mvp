import pytest
import json
from datetime import datetime, timezone
from pathlib import Path
from app.database import create_db_and_tables


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create database tables before running tests."""
    create_db_and_tables()
    yield


def pytest_sessionfinish(session, exitstatus):
    """Hook called after all tests finish - updates status.json with results."""
    # Get test counts from session
    total = session.testscollected if hasattr(session, 'testscollected') else 0
    passed = len([r for r in session.items if hasattr(r, 'rep_call') and r.rep_call.passed]) if hasattr(session, 'items') else 0
    failed = session.testsfailed if hasattr(session, 'testsfailed') else 0
    skipped = session.testscollected - passed - failed if total > 0 else 0
    
    # Get stats from terminal reporter if available
    stats = session.config.pluginmanager.get_plugin('terminalreporter').stats if session.config.pluginmanager.get_plugin('terminalreporter') else {}
    
    # Count from stats if available (more reliable)
    passed_count = len(stats.get('passed', []))
    failed_count = len(stats.get('failed', []))
    skipped_count = len(stats.get('skipped', []))
    error_count = len(stats.get('error', []))
    
    total_count = passed_count + failed_count + skipped_count + error_count
    
    # Build status string
    if failed_count == 0 and error_count == 0:
        status_str = f"{passed_count} passed"
        if skipped_count > 0:
            status_str += f", {skipped_count} skipped"
    else:
        status_str = f"{passed_count} passed, {failed_count} failed"
        if skipped_count > 0:
            status_str += f", {skipped_count} skipped"
        if error_count > 0:
            status_str += f", {error_count} error"
    
    # Create status data
    status_data = {
        "backend_tests": status_str,
        "last_updated": datetime.now(timezone.utc).astimezone().isoformat(),
        "test_summary": {
            "total": total_count,
            "passed": passed_count,
            "failed": failed_count,
            "skipped": skipped_count,
            "errors": error_count
        }
    }
    
    # Write to status.json in backend directory
    backend_dir = Path(__file__).parent.parent
    status_file = backend_dir / "status.json"
    
    with open(status_file, 'w') as f:
        json.dump(status_data, f, indent=2)
    
    print(f"\n[status.json updated] {status_str}")
