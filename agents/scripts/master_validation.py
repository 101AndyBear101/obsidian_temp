#!/usr/bin/env python3
"""
Run all vault validation scripts and report results.

Usage: python agents/scripts/master_validation.py
"""

import importlib
import os
import sys
import time

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT_ROOT = os.path.abspath(os.path.join(SCRIPTS_DIR, "..", ".."))


def main():
    scripts = sorted(
        f[:-3] for f in os.listdir(SCRIPTS_DIR)
        if f.endswith("_validation.py") and f != "master_validation.py"
    )

    if not scripts:
        print("No validation scripts found.")
        sys.exit(1)

    results = {}
    total_start = time.time()

    for name in scripts:
        path = os.path.join(SCRIPTS_DIR, name + ".py")

        start = time.time()
        try:
            import subprocess
            result = subprocess.run(
                [sys.executable, path],
                capture_output=True,
                text=True,
                cwd=VAULT_ROOT,
            )
            elapsed = time.time() - start
            success = result.returncode == 0
            output = result.stdout + result.stderr
        except Exception as e:
            elapsed = time.time() - start
            success = False
            output = str(e)

        results[name] = {
            "success": success,
            "time": elapsed,
            "output": output.strip(),
        }

        status = "PASS" if success else "FAIL"
        print(f"[{status}] {name} ({elapsed:.2f}s)")

    print()
    print("=" * 50)
    passed = sum(1 for r in results.values() if r["success"])
    failed = sum(1 for r in results.values() if not r["success"])
    total_time = time.time() - total_start
    print(f"Results: {passed} passed, {failed} failed ({total_time:.2f}s total)")
    print()

    if failed > 0:
        for name, r in results.items():
            if not r["success"]:
                print(f"--- {name} FAILURES ---")
                print(r["output"][:2000])
                print()
        sys.exit(1)
    else:
        print("All validations passed.")


if __name__ == "__main__":
    main()