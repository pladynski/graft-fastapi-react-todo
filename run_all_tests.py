#!/usr/bin/env python3
"""Run backend unit tests. Consumer smoke/e2e need a running Gateway."""
import subprocess
import sys
from pathlib import Path


def main() -> int:
    backend_dir = Path(__file__).parent / "backend"
    print("Running backend TodoService unit tests")
    result = subprocess.run(
        ["python3", "-m", "pytest", "test_todo_service.py", "-v", "--tb=short"],
        cwd=backend_dir,
    )
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
