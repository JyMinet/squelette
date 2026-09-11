#!/usr/bin/env python3
"""Read-only Git path classification for a governed project."""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
CLASSIFICATIONS = ROOT / "docs" / "governance" / "git-path-classifications.v1.json"
ALLOWED = {
    "TRACKED",
    "INTENTIONALLY_IGNORED",
    "PROJECT_CONTROL_GENERATED",
    "PREEXISTING",
    "CONCURRENT_WORK",
}
GENERATED_RECORD_PATH = re.compile(
    r"^project_control/(?:work-items|conversations|agent-runs)/[^/]+\.json$"
)


@dataclass(frozen=True)
class PathState:
    path: str
    git_status: str
    classification: str
    explanation: str


def run_git(root: Path, args: list[str], *, text: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        check=False,
        capture_output=True,
        text=text,
    )


def repository_identity(root: Path = ROOT) -> dict[str, str]:
    top = run_git(root, ["rev-parse", "--show-toplevel"])
    branch = run_git(root, ["branch", "--show-current"])
    head = run_git(root, ["rev-parse", "HEAD"])
    return {
        "root": top.stdout.strip() if top.returncode == 0 else "UNKNOWN",
        "branch": branch.stdout.strip() or "DETACHED_OR_UNBORN",
        "head": head.stdout.strip() if head.returncode == 0 else "UNBORN",
    }


def load_classifications(root: Path = ROOT) -> dict[str, list[str]]:
    classifications = root / CLASSIFICATIONS.relative_to(ROOT)
    try:
        payload = json.loads(classifications.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {
            "PROJECT_CONTROL_GENERATED": [],
            "PREEXISTING": [],
            "CONCURRENT_WORK": [],
        }
    return {
        name: [str(item) for item in payload.get(name, []) if isinstance(item, str)]
        for name in ("PROJECT_CONTROL_GENERATED", "PREEXISTING", "CONCURRENT_WORK")
    }


def parse_porcelain_z(raw: bytes) -> list[tuple[str, str]]:
    """Parse porcelain v1 -z records; a rename yields its destination AND its origin.

    The origin of a rename is removed from where it was: it is a change of its own and has to
    be classified like any other. A copy leaves its origin untouched, so only the destination
    is reported for it.
    """
    chunks = raw.split(b"\0")
    records: list[tuple[str, str]] = []
    index = 0
    while index < len(chunks):
        chunk = chunks[index]
        index += 1
        if not chunk:
            continue
        decoded = chunk.decode("utf-8", errors="surrogateescape")
        if len(decoded) < 4:
            records.append(("??", decoded))
            continue
        status = decoded[:2]
        path = decoded[3:]
        records.append((status, path))
        if "R" in status or "C" in status:
            origin = chunks[index].decode("utf-8", errors="surrogateescape") if index < len(chunks) else ""
            index += 1  # the source path follows the destination in the same record
            if "R" in status and origin:
                records.append((status, origin))
    return records


def matches(path: str, patterns: Iterable[str]) -> bool:
    for pattern in patterns:
        normalized = pattern.rstrip("/")
        if path == normalized or path.startswith(normalized + "/") or fnmatch.fnmatch(path, pattern):
            return True
    return False


def is_ignored(root: Path, path: str) -> bool:
    result = run_git(root, ["check-ignore", "--quiet", "--", path])
    return result.returncode == 0


def classify_paths(root: Path = ROOT) -> tuple[list[PathState], list[str]]:
    errors: list[str] = []
    status = run_git(root, ["status", "--porcelain=v1", "-z", "--untracked-files=all"], text=False)
    if status.returncode != 0:
        stderr = status.stderr.decode("utf-8", errors="replace") if isinstance(status.stderr, bytes) else str(status.stderr)
        return [], [f"git status failed: {stderr.strip()}"]

    configured = load_classifications(root)
    invalid_generated = [
        path
        for path in configured["PROJECT_CONTROL_GENERATED"]
        if not GENERATED_RECORD_PATH.fullmatch(path)
    ]
    errors.extend(
        f"invalid PROJECT_CONTROL_GENERATED path: {path}"
        for path in invalid_generated
    )
    states: list[PathState] = []
    for git_status, path in parse_porcelain_z(status.stdout):
        if git_status != "??":
            state = PathState(path, git_status, "TRACKED", "Path is present in the Git index.")
        elif is_ignored(root, path):
            state = PathState(path, git_status, "INTENTIONALLY_IGNORED", "Matched a Git ignore rule.")
        elif matches(path, configured["PROJECT_CONTROL_GENERATED"]):
            state = PathState(
                path,
                git_status,
                "PROJECT_CONTROL_GENERATED",
                "Exact path was transactionally created and registered by Project Control.",
            )
        elif matches(path, configured["PREEXISTING"]):
            state = PathState(path, git_status, "PREEXISTING", "Explicitly classified in governance registry.")
        elif matches(path, configured["CONCURRENT_WORK"]):
            state = PathState(path, git_status, "CONCURRENT_WORK", "Explicitly classified in governance registry.")
        else:
            state = PathState(path, git_status, "UNEXPLAINED", "Untracked and not explicitly classified.")
            errors.append(f"UNEXPLAINED path: {path}")
        states.append(state)
    return states, errors


def audit_payload(root: Path = ROOT) -> dict[str, object]:
    root = root.resolve()
    states, errors = classify_paths(root)
    counts: dict[str, int] = {}
    for state in states:
        counts[state.classification] = counts.get(state.classification, 0) + 1
    return {
        "check": "GIT_TRACEABILITY",
        "read_only": True,
        "status": "PASS" if not errors else "FAIL",
        "repository": repository_identity(root),
        "allowed_classifications": sorted(ALLOWED),
        "counts": counts,
        "paths": [asdict(state) for state in states],
        "errors": errors,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable output.")
    args = parser.parse_args(argv)
    payload = audit_payload()
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"GIT_TRACEABILITY: {payload['status']}")
        print("READ_ONLY: true")
        repository = payload["repository"]
        print(f"BRANCH: {repository['branch']}")
        print(f"HEAD: {repository['head']}")
        for state in payload["paths"]:
            print(f"{state['classification']}: {state['path']} [{state['git_status']}]")
        for error in payload["errors"]:
            print(f"ERROR: {error}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
