import sys
import pytest

if __name__ == "__main__":
    print("Running Phase 12 Persistent Memory & Personalization Unit Tests...")
    exit_code = pytest.main(["-v", "backend/tests/test_memory.py"])
    sys.exit(exit_code)
