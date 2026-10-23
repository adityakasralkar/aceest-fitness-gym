"""Reports the result of a CI run to the AIDevOps monitoring server.

A failed pipeline is sent as CRITICAL (the push cannot be deployed), with the
commit, branch, author, the failed step and the end of its output, so the
problem is traced back to the exact push that caused it. A passing pipeline
is sent as INFO, giving a record of every deployable push.

Never fails the job itself: if AIDevOps is unreachable it only warns.
"""

import json
import os
import re
import urllib.request
from pathlib import Path

URL = os.getenv("AIDEVOPS_URL", "").rstrip("/")
API_KEY = os.getenv("AIDEVOPS_API_KEY", "")
LOG_DIR = Path(os.getenv("CI_LOG_DIR", "ci-logs"))

# Step id -> readable name and how serious its failure is.
STEPS = {
    "install": ("Install dependencies", "CRITICAL"),
    "lint": ("Lint (flake8)", "ERROR"),
    "format": ("Format check (black)", "ERROR"),
    "tests": ("Tests (pytest)", "CRITICAL"),
    "secret_scan": ("Security: secret scan", "CRITICAL"),
    "dependency_audit": ("Security: vulnerable dependencies", "CRITICAL"),
}

# Most specific first: a failed test, a found secret, a vulnerability,
# a lint error, then any error line.
DETAIL_PATTERNS = [
    re.compile(r"^FAILED "),
    re.compile(r"^SECRET FOUND"),
    re.compile(r"Found \d+ known vulnerabilit", re.I),
    re.compile(r":\d+:\d+: [EFWC]\d+ "),
    re.compile(r"error", re.I),
]


def strip_colours(text):
    """Removes terminal colour codes that tools add to their output."""
    return re.sub(r"\x1b\[[0-9;]*m", "", text)


def read_log(step_id):
    try:
        return strip_colours((LOG_DIR / f"{step_id}.log").read_text(errors="replace")).rstrip()
    except OSError:
        return ""


def first_error_line(output):
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    for pattern in DETAIL_PATTERNS:
        for line in lines:
            if pattern.search(line):
                return line[:300]
    return ""


def main():
    if not URL or not API_KEY:
        print("AIDEVOPS_URL or AIDEVOPS_API_KEY not set; skipping report.")
        return

    steps = json.loads(os.getenv("STEPS_JSON") or "{}")
    failed = [step_id for step_id, s in steps.items() if s.get("outcome") == "failure"]

    env = os.environ
    sha = env.get("GITHUB_SHA", "")
    branch = env.get("GITHUB_REF_NAME", "")
    run_url = (
        f"{env.get('GITHUB_SERVER_URL')}/{env.get('GITHUB_REPOSITORY')}"
        f"/actions/runs/{env.get('GITHUB_RUN_ID')}"
    )
    attributes = {
        "ci.pipeline": env.get("GITHUB_WORKFLOW", "CI"),
        "ci.run.id": env.get("GITHUB_RUN_ID", ""),
        "ci.run.url": run_url,
        "vcs.repository": env.get("GITHUB_REPOSITORY", ""),
        "vcs.branch": branch,
        "vcs.commit.sha": sha,
        "vcs.commit.author": env.get("GITHUB_ACTOR", ""),
        "vcs.commit.message": env.get("COMMIT_MESSAGE", "").split("\n")[0][:200],
    }

    if failed:
        logs = []
        for step_id in failed:
            name, severity = STEPS.get(step_id, (step_id, "CRITICAL"))
            full = read_log(step_id)
            detail = first_error_line(full)
            message = f'Pipeline failed at "{name}" for commit {sha[:7]} on {branch}'
            logs.append(
                {
                    "service_name": "aceest-gym-ci",
                    "severity": severity,
                    "message": f"{message}: {detail}" if detail else message,
                    "stack_trace": "\n".join(full.splitlines()[-80:]),
                    "attributes": {**attributes, "ci.failed_step": name},
                }
            )
    else:
        logs = [
            {
                "service_name": "aceest-gym-ci",
                "severity": "INFO",
                "message": f"Pipeline passed for commit {sha[:7]} on {branch}; ready to deploy",
                "attributes": attributes,
            }
        ]

    request = urllib.request.Request(
        f"{URL}/api/v1/telemetry/logs",
        data=json.dumps(logs).encode(),
        headers={"Content-Type": "application/json", "X-API-Key": API_KEY},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            print(f"Reported {len(logs)} result(s) to AIDevOps: HTTP {response.status}")
    except Exception as err:  # noqa: BLE001 - reporting must never fail the job
        print(f"::warning::Could not report to AIDevOps: {err}")


if __name__ == "__main__":
    main()
