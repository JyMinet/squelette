from __future__ import annotations

import copy
import importlib.util
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import tempfile
import unittest
import unittest.mock
from pathlib import Path
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/project_control"
BLOCK_REASON_CODE = "EXTERNAL_SERVICE_ACCESS_REQUIRED"
BLOCK_RESUME_CONDITION = "authorized external service access is available"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def recorded_decision_block(text: str, reference: str) -> str | None:
    """The recorded text of one Human Decision, read by the tests without the controller."""
    match = re.search(
        rf"(?ms)^## {re.escape(reference)}\s*$\n(.*?)(?=^## HD-[0-9]{{3,}}\s*$|\Z)",
        text,
    )
    return None if match is None else match.group(1)


GREEN_TEST_OUTPUT = """\
.............................
----------------------------------------------------------------------
Ran 29 tests in 0.004s

OK
"""


RED_TEST_OUTPUT = """\
======================================================================
FAIL: test_prix_de_revient (tests.test_rapport.RapportTests)
----------------------------------------------------------------------
AssertionError: 'CE TEXTE N EXISTE PAS' not found in the report

----------------------------------------------------------------------
Ran 29 tests in 0.004s

FAILED (failures=1)
"""


def running_in_the_template() -> bool:
    """Is this tree the template itself, or a project derived from it?

    Four checks below replay the template on itself: they read its own roadmap, its own
    generated view or its example. A derived project has none of them, and the copy they
    would work on is that project. They skip there rather than fail on a file whose absence
    is normal."""
    try:
        state = load_json(ROOT / "project_control/project-state.v1.json")
    except (OSError, ValueError):
        return False
    return state.get("repository_role") == "PROJECT_TEMPLATE"


def load_project_control():
    path = ROOT / "scripts/project_control.py"
    spec = importlib.util.spec_from_file_location("project_control_under_test", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load project_control.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def run_git(root: Path, *args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    environment = dict(os.environ)
    if env:
        environment.update(env)
    return subprocess.run(
        ["git", *args], cwd=root, check=False, capture_output=True, text=True, env=environment
    )


def run_control(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-B", "scripts/project_control.py", *args],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )


def stage_explicit_files(root: Path) -> None:
    files = [
        str(path.relative_to(root))
        for path in root.rglob("*")
        if path.is_file() and ".git" not in path.parts
    ]
    if not files:
        return
    # A file the project ignores — a download folder an application drops in the working
    # copy, for instance — is copied along with the tree but must not be staged: `git add`
    # refuses an ignored path and the fixture would fail for a reason foreign to the test.
    ignored = run_git(root, "check-ignore", "--", *files)
    skipped = set(ignored.stdout.splitlines())
    kept = [name for name in files if name not in skipped]
    result = run_git(root, "add", "--", *kept)
    if result.returncode != 0:
        raise AssertionError(result.stdout + result.stderr)


def fixture_copy_ignore():
    """What a fixture copy of the template leaves behind: Git's own folder, caches — and every
    path the template ignores. The copy used to be made of the working folder as it is, ignored
    entries included: a download folder an application drops next to the template, a generated
    view. Two tests were shown to depend on what lay there — one half-written JSON file in an
    ignored folder, and a fixture failed its JSON audit (fourth independent control). A fixture
    is made of what the template holds, not of what happens to sit next to it."""
    ignored: set[str] = set()
    listed = subprocess.run(
        ["git", "ls-files", "--others", "--ignored", "--exclude-standard", "--directory"],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    if listed.returncode == 0:
        ignored = {line.rstrip("/") for line in listed.stdout.splitlines() if line.strip()}
    patterns = shutil.ignore_patterns(".git", "__pycache__", "*.pyc", ".DS_Store")

    def ignore(directory: str, names: list[str]) -> set[str]:
        skipped = set(patterns(directory, names))
        for name in names:
            relative = (Path(directory) / name).resolve().relative_to(ROOT.resolve()).as_posix()
            if relative in ignored:
                skipped.add(name)
        return skipped

    return ignore


def discard_ignored_files(root: Path) -> None:
    """The fixture copies the working folder as it is, ignored entries included — the folder an
    application drops its downloads in, a generated view. A test that removes `.gitignore` would
    make them all visible and be refused for a reason foreign to what it measures, and its result
    would depend on whatever lies next to the template at the time it runs. It discards them first,
    in its own temporary copy, so that only what the test announces is measured."""
    listed = run_git(root, "ls-files", "--others", "--ignored", "--exclude-standard")
    if listed.returncode != 0:
        raise AssertionError(listed.stdout + listed.stderr)
    for name in listed.stdout.splitlines():
        path = root / name
        if path.is_symlink() or path.is_file():
            path.unlink()


class GeneralProjectSkeletonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.control_module = load_project_control()
        cls.work_item = load_json(FIXTURES / "work-item.valid.json")
        cls.conversation = load_json(FIXTURES / "conversation.valid.json")
        cls.agent_run = load_json(FIXTURES / "agent-run.valid.json")

    def skip_unless_template(self, subject: str) -> None:
        if not running_in_the_template():
            self.skipTest(f"{subject} belongs to the template itself; a derived project skips")

    def make_copy(self) -> tuple[tempfile.TemporaryDirectory, Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name) / "project"
        shutil.copytree(ROOT, root, ignore=fixture_copy_ignore())
        self.reset_to_not_started_fixture(root)
        init = run_git(root, "init", "-b", "main")
        self.assertEqual(init.returncode, 0, init.stdout + init.stderr)
        for key, value in (("user.name", "Fixture Owner"), ("user.email", "fixture@example.invalid")):
            configured = run_git(root, "config", key, value)
            self.assertEqual(configured.returncode, 0, configured.stdout + configured.stderr)
        stage_explicit_files(root)
        commit = run_git(
            root,
            "-c",
            "user.name=Fixture Owner",
            "-c",
            "user.email=fixture@example.invalid",
            "commit",
            "-m",
            "fixture: pristine governed skeleton",
        )
        self.assertEqual(commit.returncode, 0, commit.stdout + commit.stderr)
        return temporary, root

    PROJECT_CONTENT_ROOTS = ("applications", "modules", "shared", "contracts", "data", "reports")

    def prune_project_content(self, root: Path) -> None:
        """A NOT_STARTED fixture is a pristine skeleton: the project's own capability, data
        and reports are not part of it, so that a derived project runs this same suite."""
        for directory in self.PROJECT_CONTENT_ROOTS:
            base = root / directory
            if not base.is_dir():
                continue
            for path in sorted(base.rglob("*"), reverse=True):
                if path.is_file() and path.name != "README.md":
                    path.unlink()
                elif path.is_dir() and not any(path.iterdir()):
                    path.rmdir()

    def reset_to_not_started_fixture(self, root: Path) -> None:
        self.prune_project_content(root)
        first_start_path = root / "FIRST_START.md"
        first_start = first_start_path.read_text(encoding="utf-8")
        first_start_path.write_text(
            re.sub(
                r"INITIALIZATION_STATUS:\s*(?:NOT_STARTED|COMPLETE)",
                "INITIALIZATION_STATUS: NOT_STARTED",
                first_start,
                count=1,
            ),
            encoding="utf-8",
        )
        project_state = {
            "$schema": "schemas/project-state.v1.schema.json",
            "schema_version": "1.0.0",
            "repository_role": "PROJECT_TEMPLATE",
            "project_name": "UNKNOWN",
            "project_key": None,
            "project_owner": "UNKNOWN",
            "legacy_baseline": None,
            "authorities_baseline": None,
            "reporting_style": "UNKNOWN",
            "language": "UNKNOWN",
            "initialization": {
                "status": "NOT_STARTED",
                "completion_human_decision_ref": None,
                "completed_at": None,
                "baseline_head": "UNKNOWN",
                "closeout_evidence": [],
            },
        }
        (root / "project_control/project-state.v1.json").write_text(
            json.dumps(project_state, indent=2) + "\n",
            encoding="utf-8",
        )
        roadmap_path = root / "docs/governance/roadmap-state.v1.json"
        roadmap = load_json(roadmap_path)
        roadmap["updated_at"] = "UNKNOWN"
        roadmap["work_items"] = []
        roadmap_path.write_text(json.dumps(roadmap, indent=2) + "\n", encoding="utf-8")
        roadmap_md = root / "docs/governance/ROADMAP.md"
        roadmap_text = self.control_module.render_roadmap_markdown(
            roadmap_md.read_text(encoding="utf-8"),
            [],
        )
        roadmap_md.write_text(
            re.sub(
                r"Status: `[^`]+`",
                "Status: `INITIALIZATION — EMPTY`",
                roadmap_text,
                count=1,
            ),
            encoding="utf-8",
        )
        decisions_path = root / "docs/governance/HUMAN_DECISIONS.md"
        decisions = decisions_path.read_text(encoding="utf-8")
        decisions_path.write_text(
            re.sub(r"(?ms)\n## HD-[0-9]{3,}\s*$.*\Z", "\n", decisions),
            encoding="utf-8",
        )
        registry_path = root / "docs/governance/WORKTREE_REGISTRY.md"
        registry = registry_path.read_text(encoding="utf-8")
        registry_path.write_text(
            re.sub(
                r"(?ms)\n*<!-- PROJECT_CONTROL:WI-[0-9]{3,} START -->.*?"
                r"<!-- PROJECT_CONTROL:WI-[0-9]{3,} END -->\n*",
                "\n",
                registry,
            ),
            encoding="utf-8",
        )
        classifications_path = root / "docs/governance/git-path-classifications.v1.json"
        classifications = load_json(classifications_path)
        for key in ("PROJECT_CONTROL_GENERATED", "PREEXISTING", "CONCURRENT_WORK"):
            classifications[key] = []
        classifications_path.write_text(
            json.dumps(classifications, indent=2) + "\n",
            encoding="utf-8",
        )
        # The Project Owner's ideas, the view settings and the generated view belong to the
        # project: a pristine copy starts without them.
        ideas_path = root / "docs/governance/ideas-state.v1.json"
        ideas = load_json(ideas_path)
        ideas.update(updated_at="UNKNOWN", ideas=[])
        ideas_path.write_text(json.dumps(ideas, indent=2) + "\n", encoding="utf-8")
        ideas_md = root / "docs/governance/IDEAS.md"
        ideas_md.write_text(
            re.sub(
                r"Status: `[^`]+`", "Status: `EMPTY`",
                self.control_module.render_ideas_markdown(ideas_md.read_text(encoding="utf-8"), []),
                count=1,
            ),
            encoding="utf-8",
        )
        (root / "project_control/roadmap-view.v1.json").write_text(
            json.dumps({
                "$schema": "schemas/roadmap-view.v1.schema.json", "schema_version": "1.0.0",
                "style": "FOLLOW_REPORTING_STYLE", "zoom": {"past": "COLLAPSED", "far": "TITLES"},
                "language": "fr", "regeneration": "OFF", "mirrors": [],
            }, indent=2) + "\n",
            encoding="utf-8",
        )
        for generated in ("docs/governance/ROADMAP_VIEW.md", "reports/roadmap/ROADMAP.html", "provenance/roadmap/ROADMAP.html"):
            if (root / generated).is_file():
                (root / generated).unlink()
            if (root / generated).parent.is_dir() and not any((root / generated).parent.iterdir()):
                (root / generated).parent.rmdir()
        for directory in (
            "project_control/work-items",
            "project_control/conversations",
            "project_control/agent-runs",
            "project_control/deployments",
        ):
            for path in (root / directory).glob("*.json"):
                path.unlink()

    def authorized_work_item(self, base_head: str, work_item_id: str = "WI-001") -> dict:
        item = copy.deepcopy(self.work_item)
        item.pop("close_head", None)
        item.update(
            work_item_id=work_item_id,
            display_reference=f"ALPHA-{work_item_id.split('-', 1)[1]}",
            title="First governed change",
            objective="Exercise normal-mode preflight after initialization.",
            status="AUTHORIZED",
            human_decision_refs=["HD-101"],
            conversation_refs=["CONV-101"],
            agent_run_refs=[],
            base_head=base_head,
            start_head="UNKNOWN",
            runtime_target="NOT_APPLICABLE",
            branch=f"work/{work_item_id.lower()}-first-change",
            commits=[],
            authorized_paths=["docs/first-change"],
            applicability={
                "code": "NOT_APPLICABLE",
                "tests": "APPLICABLE",
                "integration": "APPLICABLE",
                "deployment": "NOT_APPLICABLE",
                "runtime_proof": "NOT_APPLICABLE",
            },
            development_status="NOT_APPLICABLE",
            test_status="NOT_REACHED",
            integration_status="NOT_REACHED",
            deployment_status="NOT_APPLICABLE",
            runtime_proof_status="NOT_APPLICABLE",
            evidence={"tests": [], "integration": [], "deployment": [], "runtime_proof": []},
            close_condition="Applicable tests and integration pass.",
        )
        return item

    def configure_ready_for_closeout(self, root: Path, work_item_id: str = "WI-001") -> str:
        base_head = run_git(root, "rev-parse", "HEAD").stdout.strip()
        state = load_json(root / "project_control/project-state.v1.json")
        state.update(
            repository_role="PROJECT",
            project_name="Example Project",
            project_key="ALPHA",
            project_owner="Project Owner",
            reporting_style="TECHNICAL",
            language="FR",
        )
        state["initialization"]["completion_human_decision_ref"] = "HD-101"
        (root / "project_control/project-state.v1.json").write_text(
            json.dumps(state, indent=2) + "\n", encoding="utf-8"
        )

        (root / "docs/governance/PROJECT_CHARTER.md").write_text(
            "# Project Charter\n\nStatus: `VALIDATED`\n\nPROJECT_OWNER: Project Owner\n",
            encoding="utf-8",
        )
        (root / "docs/architecture/PROJECT_ARCHITECTURE_MAP.md").write_text(
            "# Project Architecture Map\n\nStatus: `VALIDATED`\n\n"
            "| Question | Status |\n|---|---|\n| Ownership explicit? | PASS |\n\n"
            "ANTI_OCTOPUS_REVIEW: APPROVED_BY_PROJECT_OWNER\n",
            encoding="utf-8",
        )
        (root / "docs/architecture/INITIAL_ARCHITECTURE.md").write_text(
            "# Initial Architecture\n\nStatus: `VALIDATED`\n", encoding="utf-8"
        )
        (root / "docs/adr/ADR-0001-initial-architecture-boundaries.md").write_text(
            "# ADR-0001\n\nStatus: `ACCEPTED`\n", encoding="utf-8"
        )
        (root / "docs/governance/HUMAN_DECISIONS.md").write_text(
            "# Human Decisions Register\n\n## HD-101\n\n"
            f"Decision: Authorize initialization closeout and {work_item_id}.\n"
            "Authorized by: Project Owner\n",
            encoding="utf-8",
        )

        repository_status = root / "docs/governance/REPOSITORY_STATUS.md"
        repository_status.write_text(
            re.sub(
                r"CANONICAL BRANCH: [^`\n]+",
                "CANONICAL BRANCH: main",
                repository_status.read_text(encoding="utf-8"),
                count=1,
            ),
            encoding="utf-8",
        )
        work_item = self.authorized_work_item(base_head, work_item_id)
        (root / f"project_control/work-items/{work_item_id}.json").write_text(
            json.dumps(work_item, indent=2) + "\n", encoding="utf-8"
        )
        conversation = copy.deepcopy(self.conversation)
        conversation["related_work_items"] = [work_item_id]
        (root / "project_control/conversations/CONV-101.json").write_text(
            json.dumps(conversation, indent=2) + "\n", encoding="utf-8"
        )

        roadmap = load_json(root / "docs/governance/roadmap-state.v1.json")
        roadmap["work_items"] = [
            {
                "work_item_id": work_item_id,
                "display_reference": f"ALPHA-{work_item_id.split('-', 1)[1]}",
                "title": "First governed change",
                "status": "AUTHORIZED",
                "integration_state": "UNMERGED",
                "human_gate": "HD-101",
                "dependencies": [],
            }
        ]
        (root / "docs/governance/roadmap-state.v1.json").write_text(
            json.dumps(roadmap, indent=2) + "\n", encoding="utf-8"
        )
        (root / "docs/governance/ROADMAP.md").write_text(
            "# Roadmap\n\nStatus: `INITIALIZED`\n\n"
            "| Internal ID | Display reference | Work Item | Status | Integration | Human gate | Depends on |\n"
            "|---|---|---|---|---|---|---|\n"
            f"| {work_item_id} | ALPHA-{work_item_id.split('-', 1)[1]} | First governed change | AUTHORIZED | UNMERGED | HD-101 | — |\n",
            encoding="utf-8",
        )
        registry_path = root / "docs/governance/WORKTREE_REGISTRY.md"
        registry_path.write_text(
            self.control_module.render_registry_entry(
                registry_path.read_text(encoding="utf-8"),
                work_item,
                "DECLARED",
            ),
            encoding="utf-8",
        )
        return base_head

    def complete_initialization(self, root: Path, base_head: str) -> None:
        first_start = (root / "FIRST_START.md").read_text(encoding="utf-8")
        (root / "FIRST_START.md").write_text(
            first_start.replace("INITIALIZATION_STATUS: NOT_STARTED", "INITIALIZATION_STATUS: COMPLETE"),
            encoding="utf-8",
        )
        state = load_json(root / "project_control/project-state.v1.json")
        state["initialization"].update(
            status="COMPLETE",
            completed_at="2026-08-20T12:00:00Z",
            baseline_head=base_head,
            closeout_evidence=["project_control.py bootstrap-closeout PASS"],
        )
        (root / "project_control/project-state.v1.json").write_text(
            json.dumps(state, indent=2) + "\n", encoding="utf-8"
        )

    def finish_bootstrap_work_item(self, root: Path, work_item_id: str) -> None:
        path = root / f"project_control/work-items/{work_item_id}.json"
        item = load_json(path)
        item.update(
            status="DONE",
            close_head=run_git(root, "rev-parse", "HEAD").stdout.strip(),
            applicability={
                "code": "NOT_APPLICABLE",
                "tests": "NOT_APPLICABLE",
                "integration": "NOT_APPLICABLE",
                "deployment": "NOT_APPLICABLE",
                "runtime_proof": "NOT_APPLICABLE",
            },
            development_status="NOT_APPLICABLE",
            test_status="NOT_APPLICABLE",
            integration_status="NOT_APPLICABLE",
            deployment_status="NOT_APPLICABLE",
            runtime_proof_status="NOT_APPLICABLE",
        )
        path.write_text(json.dumps(item, indent=2) + "\n", encoding="utf-8")
        roadmap = load_json(root / "docs/governance/roadmap-state.v1.json")
        roadmap["work_items"][0]["status"] = "DONE"
        roadmap["work_items"][0]["integration_state"] = "HISTORICAL"
        (root / "docs/governance/roadmap-state.v1.json").write_text(
            json.dumps(roadmap, indent=2) + "\n", encoding="utf-8"
        )
        roadmap_md = root / "docs/governance/ROADMAP.md"
        roadmap_md.write_text(
            roadmap_md.read_text(encoding="utf-8").replace(
                "| AUTHORIZED | UNMERGED |", "| DONE | HISTORICAL |"
            ),
            encoding="utf-8",
        )
        registry_path = root / "docs/governance/WORKTREE_REGISTRY.md"
        registry_path.write_text(
            self.control_module.render_registry_entry(
                registry_path.read_text(encoding="utf-8"),
                item,
                "CLOSED",
            ),
            encoding="utf-8",
        )

    def commit_fixture(self, root: Path, message: str) -> str:
        stage_explicit_files(root)
        commit = run_git(
            root,
            "-c",
            "user.name=Fixture Owner",
            "-c",
            "user.email=fixture@example.invalid",
            "commit",
            "-m",
            message,
        )
        self.assertEqual(commit.returncode, 0, commit.stdout + commit.stderr)
        return run_git(root, "rev-parse", "HEAD").stdout.strip()

    def commit_fixture_if_needed(self, root: Path, message: str) -> str:
        """Commit when the worktree is dirty; Project Control transitions commit their own records."""
        if run_git(root, "status", "--porcelain=v1", "--untracked-files=all").stdout.strip():
            return self.commit_fixture(root, message)
        return run_git(root, "rev-parse", "HEAD").stdout.strip()

    def make_normal_copy(self) -> tuple[tempfile.TemporaryDirectory, Path]:
        temporary, root = self.make_copy()
        base_head = self.configure_ready_for_closeout(root, "WI-000")
        closeout = run_control(
            root,
            "bootstrap-closeout",
            "--path",
            "FIRST_START.md",
            "--path",
            "project_control/project-state.v1.json",
        )
        self.assertEqual(closeout.returncode, 0, closeout.stdout + closeout.stderr)
        self.finish_bootstrap_work_item(root, "WI-000")
        self.complete_initialization(root, base_head)
        self.commit_fixture(root, "fixture: complete governed initialization")
        audit = run_control(root, "audit")
        self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)
        return temporary, root

    def create_lifecycle_work_item(
        self,
        root: Path,
        work_item_id: str,
        decision_id: str,
        runtime_target: str = "NOT_APPLICABLE",
        *,
        base_head: str | None = None,
        branch: str | None = None,
        authorized_path: str | None = None,
        code: str = "NOT_APPLICABLE",
        tests: str = "APPLICABLE",
        integration: str = "APPLICABLE",
        deployment: str | None = None,
        runtime_proof: str | None = None,
        depends_on: tuple[str, ...] = (),
    ) -> subprocess.CompletedProcess[str]:
        default_runtime = "NOT_APPLICABLE" if runtime_target == "NOT_APPLICABLE" else "APPLICABLE"
        deployment = default_runtime if deployment is None else deployment
        runtime_proof = default_runtime if runtime_proof is None else runtime_proof
        arguments = [
            "create-work-item",
            work_item_id,
            "--title",
            f"Lifecycle {work_item_id}",
            "--objective",
            f"Exercise the governed lifecycle for {work_item_id}.",
            "--owner",
            "Project Owner",
            "--human-decision",
            decision_id,
            "--decision",
            f"Authorize {work_item_id} lifecycle execution.",
            "--authorized-by",
            "Project Owner",
            "--path",
            authorized_path or f"reports/{work_item_id}.txt",
            "--path",
            f"reports/evidence/{work_item_id}",
            "--conflict-gate",
            "INDEPENDENT",
            "--direct-impact",
            f"reports/{work_item_id}.txt",
            "--indirect-impact",
            "Project lifecycle test",
            "--authority-impact",
            "NONE",
            "--concurrent-work-impact",
            "NONE",
            "--code",
            code,
            "--tests",
            tests,
            "--integration",
            integration,
            "--deployment",
            deployment,
            "--runtime-proof",
            runtime_proof,
            "--runtime-target",
            runtime_target,
            "--close-condition",
            "Tests and integration evidence pass.",
        ]
        for dependency in depends_on:
            arguments.extend(["--depends-on", dependency])
        if base_head is not None:
            arguments.extend(["--base-head", base_head])
        if branch is not None:
            arguments.extend(["--branch", branch])
        return run_control(root, *arguments)

    def lifecycle_arguments(self, work_item_id: str, decision_id: str) -> list[str]:
        """The `create-work-item` arguments of the helper above, for a caller that runs it itself."""
        return [
            "create-work-item", work_item_id,
            "--title", f"Lifecycle {work_item_id}",
            "--objective", f"Exercise the governed lifecycle for {work_item_id}.",
            "--owner", "Project Owner",
            "--human-decision", decision_id,
            "--decision", f"Authorize {work_item_id} lifecycle execution.",
            "--authorized-by", "Project Owner",
            "--path", f"reports/{work_item_id}.txt",
            "--path", f"reports/evidence/{work_item_id}",
            "--conflict-gate", "INDEPENDENT",
            "--direct-impact", f"reports/{work_item_id}.txt",
            "--indirect-impact", "Project lifecycle test",
            "--authority-impact", "NONE",
            "--concurrent-work-impact", "NONE",
            "--code", "NOT_APPLICABLE",
            "--tests", "APPLICABLE",
            "--integration", "APPLICABLE",
            "--deployment", "NOT_APPLICABLE",
            "--runtime-proof", "NOT_APPLICABLE",
            "--runtime-target", "NOT_APPLICABLE",
            "--close-condition", "Tests and integration evidence pass.",
        ]

    def merge_fixture_branch(self, root: Path, branch: str, message: str) -> None:
        switched = run_git(root, "switch", "main")
        self.assertEqual(switched.returncode, 0, switched.stdout + switched.stderr)
        merged = run_git(
            root,
            "-c",
            "user.name=Fixture Owner",
            "-c",
            "user.email=fixture@example.invalid",
            "merge",
            "--no-ff",
            "-m",
            message,
            branch,
        )
        self.assertEqual(merged.returncode, 0, merged.stdout + merged.stderr)

    def write_committed_evidence(
        self, root: Path, work_item_id: str, revision: str = "", artifacts: dict[str, str] | None = None,
    ) -> dict[str, str]:
        """Create synthetic fixture evidence for the exact committed integration.

        `artifacts` replaces the text of one gate's artifact, to record what a real run printed;
        a list records several pieces for that gate, as a real closure often bundles them."""
        subject = run_git(root, "rev-parse", "HEAD").stdout.strip()
        item = load_json(root / f"project_control/work-items/{work_item_id}.json")
        target = item["runtime_target"]
        controlled = target == "CONTROLLED_NON_PRODUCTION_RUNTIME"
        levels = {
            "tests": "TESTED",
            "integration": "INTEGRATED",
            "deployment": "DEPLOYED_IN_CONTROLLED_ENVIRONMENT" if controlled else "DEPLOYED",
            "runtime_proof": "RUNTIME_PROVEN" if controlled else "PRODUCTION_VERIFIED",
        }
        paths = {}
        directory = root / f"reports/evidence/{work_item_id}"
        directory.mkdir(parents=True, exist_ok=True)
        for gate, level in levels.items():
            if item["applicability"][gate] != "APPLICABLE":
                continue
            pieces = (artifacts or {}).get(gate) or [
                f"Synthetic test fixture: {gate} PASS for {subject}; no real deployment.\n"
            ]
            if isinstance(pieces, str):
                pieces = [pieces]
            written = []
            for index, text in enumerate(pieces):
                suffix = "" if len(pieces) == 1 else f"-{index + 1}"
                artifact = directory / f"{gate}{revision}{suffix}.txt"
                artifact.write_text(text, encoding="utf-8")
                written.append(artifact)
            report = {
                "schema_version": "1.0.0",
                "work_item_id": work_item_id,
                "gate": gate,
                "result": "PASS",
                "level": level,
                "subject_commit": subject,
                "runtime_target": target,
                "recorded_at": datetime.now(timezone.utc).isoformat(),
                "summary": f"Synthetic {gate} evidence for lifecycle regression.",
                "artifacts": [{
                    "path": str(piece.relative_to(root)),
                    "sha256": hashlib.sha256(piece.read_bytes()).hexdigest(),
                } for piece in written],
            }
            path = directory / f"{gate}{revision}.json"
            path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
            paths[gate] = str(path.relative_to(root))
        self.commit_fixture(root, f"fixture: record {work_item_id} evidence")
        return paths

    def close_with_evidence_and_commit(
        self, root: Path, work_item_id: str, evidence: dict[str, str | list[str]], commit: str,
    ) -> subprocess.CompletedProcess[str]:
        """`close` with an explicit development commit, the way an agent cites its work."""
        options = {
            "tests": "--test-evidence", "integration": "--integration-evidence",
            "deployment": "--deployment-evidence", "runtime_proof": "--runtime-evidence",
        }
        args = ["close", work_item_id, "--commit", commit]
        for gate, references in evidence.items():
            for path in references if isinstance(references, list) else [references]:
                args.extend([options[gate], path])
        return run_control(root, *args)

    def close_with_evidence(
        self, root: Path, work_item_id: str, evidence: dict[str, str | list[str]],
    ) -> subprocess.CompletedProcess[str]:
        options = {
            "tests": "--test-evidence", "integration": "--integration-evidence",
            "deployment": "--deployment-evidence", "runtime_proof": "--runtime-evidence",
        }
        args = ["close", work_item_id]
        for gate, references in evidence.items():
            for path in references if isinstance(references, list) else [references]:
                args.extend([options[gate], path])
        return run_control(root, *args)

    def prepare_integrated_item(
        self, runtime_target: str = "NOT_APPLICABLE",
    ) -> tuple[tempfile.TemporaryDirectory, Path, dict[str, str]]:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        created = self.create_lifecycle_work_item(root, "WI-001", "HD-102", runtime_target)
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        started = self.start_command(root, "WI-001")
        self.assertEqual(started.returncode, 0, started.stdout + started.stderr)
        branch = run_git(root, "branch", "--show-current").stdout.strip()
        (root / "reports/WI-001.txt").write_text("governed fixture change\n", encoding="utf-8")
        self.commit_fixture(root, "fixture: complete authorized change")
        self.merge_fixture_branch(root, branch, "fixture: integrate authorized change")
        evidence = self.write_committed_evidence(root, "WI-001")
        return temporary, root, evidence

    def snapshot_repository(self, root: Path) -> tuple:
        """Observe files and Git identity to prove read-only and rollback behavior."""
        files = {
            str(path.relative_to(root)): path.read_bytes()
            for path in root.rglob("*")
            if path.is_file() and ".git" not in path.parts
        }
        return (
            files,
            run_git(root, "branch", "--show-current").stdout,
            run_git(root, "rev-parse", "HEAD").stdout,
            run_git(root, "status", "--porcelain=v1", "--untracked-files=all").stdout,
        )

    def record_lifecycle_human_decision(
        self,
        root: Path,
        decision_id: str,
        work_item_id: str,
        decision: str,
        *,
        related_work_item: str | None = None,
        action: str = "BLOCK",
        reason_code: str = BLOCK_REASON_CODE,
        resume_condition: str = BLOCK_RESUME_CONDITION,
        chosen_option: str = "AUTHORIZE",
        duplicate_chosen_option: str | None = None,
        commit: bool = True,
    ) -> None:
        item = load_json(root / f"project_control/work-items/{work_item_id}.json")
        conversation_refs = item.get("conversation_refs", [])
        conversation_ref = conversation_refs[0] if conversation_refs else "NOT_APPLICABLE"
        related = related_work_item or work_item_id
        decisions_path = root / "docs/governance/HUMAN_DECISIONS.md"
        decisions = decisions_path.read_text(encoding="utf-8")
        self.assertNotRegex(decisions, rf"(?m)^## {re.escape(decision_id)}\s*$")
        self.assertIn(action, {"BLOCK", "RESUME"})
        if action == "BLOCK":
            lifecycle_contract = (
                "Project Control action: BLOCK\n"
                f"Block reason code: {reason_code}\n"
                f"Resume condition recorded: {resume_condition}\n"
            )
        else:
            lifecycle_contract = (
                "Project Control action: RESUME\n"
                f"Resume condition confirmed: {resume_condition}\n"
            )
        chosen_option_lines = f"Chosen option: {chosen_option}\n"
        if duplicate_chosen_option is not None:
            chosen_option_lines += f"Chosen option: {duplicate_chosen_option}\n"
        block = (
            f"\n## {decision_id}\n\n"
            f"Date: {self.control_module.today_iso()}\n"
            f"Decision: {decision}\n"
            "Context: Project Control lifecycle transition request.\n"
            "Options considered: AUTHORIZE | REJECT\n"
            f"{chosen_option_lines}"
            "Reason: Explicit human authorization supplied to Project Control.\n"
            f"Scope: {work_item_id} — {item['title']}\n"
            "Reversible: YES\n"
            f"Conversation reference: {conversation_ref}\n"
            "Related ADR: NOT_APPLICABLE\n"
            f"Related Work Item: {related}\n"
            f"{lifecycle_contract}"
            "Authorized by: Project Owner\n"
        )
        decisions_path.write_text(
            decisions.rstrip() + "\n" + block,
            encoding="utf-8",
        )
        if commit:
            self.commit_fixture(root, f"chore: record {decision_id} for {work_item_id}")

    def block_lifecycle_work_item(
        self,
        root: Path,
        work_item_id: str,
        decision_id: str,
        *,
        reason_code: str = BLOCK_REASON_CODE,
        resume_condition: str = BLOCK_RESUME_CONDITION,
    ) -> subprocess.CompletedProcess[str]:
        return run_control(
            root,
            "block",
            work_item_id,
            "--human-decision",
            decision_id,
            "--reason-code",
            reason_code,
            "--resume-condition",
            resume_condition,
        )

    def resume_lifecycle_work_item(
        self,
        root: Path,
        work_item_id: str,
        decision_id: str,
        *,
        provider: str = "FixtureAgent",
        planned_paths: tuple[str, ...] = (),
    ) -> subprocess.CompletedProcess[str]:
        arguments = [
            "resume",
            work_item_id,
            "--human-decision",
            decision_id,
            "--agent-provider",
            provider,
        ]
        for path in planned_paths:
            arguments.extend(["--path", path])
        digest = self.authorities_digest(root, work_item_id)
        if digest:
            arguments.extend(["--authorities-digest", digest])
        return run_control(root, *arguments)

    def lifecycle_snapshot(self, root: Path) -> tuple[dict[str, bytes], str, str]:
        paths = [
            root / "docs/governance/HUMAN_DECISIONS.md",
            root / "docs/governance/ROADMAP.md",
            root / "docs/governance/roadmap-state.v1.json",
            root / "docs/governance/WORKTREE_REGISTRY.md",
            root / "docs/governance/git-path-classifications.v1.json",
            *sorted((root / "project_control/work-items").glob("*.json")),
            *sorted((root / "project_control/agent-runs").glob("*.json")),
        ]
        files = {
            str(path.relative_to(root)): path.read_bytes()
            for path in paths
            if path.is_file()
        }
        branch = run_git(root, "branch", "--show-current").stdout.strip()
        refs = run_git(
            root,
            "for-each-ref",
            "--format=%(refname):%(objectname)",
            "refs/heads",
        ).stdout
        return files, branch, refs

    def create_and_start_lifecycle_work_item(
        self,
        root: Path,
        work_item_id: str = "WI-001",
        decision_id: str = "HD-102",
        **kwargs,
    ) -> dict:
        created = self.create_lifecycle_work_item(
            root,
            work_item_id,
            decision_id,
            **kwargs,
        )
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        started = self.start_command(root, work_item_id)
        self.assertEqual(started.returncode, 0, started.stdout + started.stderr)
        return load_json(root / f"project_control/work-items/{work_item_id}.json")

    def create_start_and_close_lifecycle_work_item(
        self,
        root: Path,
        work_item_id: str = "WI-001",
        decision_id: str = "HD-102",
        **kwargs,
    ) -> dict:
        """A Work Item taken through its whole lifecycle, as a project's own history holds it."""
        item = self.create_and_start_lifecycle_work_item(root, work_item_id, decision_id, **kwargs)
        self.switch_to_canonical(root)
        self.merge_fixture_branch(root, item["branch"], f"fixture: integrate {work_item_id}")
        evidence = self.write_committed_evidence(root, work_item_id)
        closed = self.close_with_evidence(root, work_item_id, evidence)
        self.assertEqual(closed.returncode, 0, closed.stdout + closed.stderr)
        return load_json(root / f"project_control/work-items/{work_item_id}.json")

    def authorities_digest(self, root: Path, work_item_id: str) -> str | None:
        """MANIFEST_DIGEST of the Work Item's routed authorities, as an agent obtains it."""
        manifest = run_control(root, "context-manifest", work_item_id)
        if manifest.returncode != 0:
            return None
        for line in manifest.stdout.splitlines():
            if line.startswith("MANIFEST_DIGEST: "):
                return line.split(": ", 1)[1].strip()
        return None

    def start_command(self, root: Path, work_item_id: str, *extra: str) -> subprocess.CompletedProcess[str]:
        """`start` the way an agent runs it: after context-manifest, with its digest."""
        arguments = ["start", work_item_id, *extra]
        digest = self.authorities_digest(root, work_item_id)
        if digest:
            arguments.extend(["--authorities-digest", digest])
        return run_control(root, *arguments)

    def switch_to_canonical(self, root: Path, canonical: str = "main") -> str:
        switched = run_git(root, "switch", canonical)
        self.assertEqual(switched.returncode, 0, switched.stdout + switched.stderr)
        return run_git(root, "rev-parse", "HEAD").stdout.strip()

    def fast_forward_fixture_branch(self, root: Path, branch: str) -> str:
        switched = run_git(root, "switch", "main")
        self.assertEqual(switched.returncode, 0, switched.stdout + switched.stderr)
        merged = run_git(root, "merge", "--ff-only", branch)
        self.assertEqual(merged.returncode, 0, merged.stdout + merged.stderr)
        return run_git(root, "rev-parse", "HEAD").stdout.strip()

    def prepare_clean_blocked_started_work_item(
        self,
        root: Path,
        *,
        work_item_id: str = "WI-001",
        creation_decision: str = "HD-102",
        block_decision: str = "HD-103",
    ) -> dict:
        self.create_and_start_lifecycle_work_item(
            root,
            work_item_id,
            creation_decision,
        )
        self.switch_to_canonical(root)
        self.record_lifecycle_human_decision(
            root,
            block_decision,
            work_item_id,
            f"Authorize blocking {work_item_id} on its external dependency.",
        )
        blocked = self.block_lifecycle_work_item(
            root,
            work_item_id,
            block_decision,
        )
        self.assertEqual(blocked.returncode, 0, blocked.stdout + blocked.stderr)
        return load_json(root / f"project_control/work-items/{work_item_id}.json")

    def prepare_clean_blocked_authorized_work_item(
        self,
        root: Path,
        *,
        work_item_id: str = "WI-001",
        creation_decision: str = "HD-102",
        block_decision: str = "HD-103",
    ) -> dict:
        created = self.create_lifecycle_work_item(
            root,
            work_item_id,
            creation_decision,
        )
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        self.record_lifecycle_human_decision(
            root,
            block_decision,
            work_item_id,
            f"Authorize blocking {work_item_id} before its first Agent Run.",
        )
        blocked = self.block_lifecycle_work_item(
            root,
            work_item_id,
            block_decision,
        )
        self.assertEqual(blocked.returncode, 0, blocked.stdout + blocked.stderr)
        return load_json(root / f"project_control/work-items/{work_item_id}.json")

    def test_foundation_02_normal_mode_without_active_work_item_refuses_business_write(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        business_path = root / "modules/example.py"
        business_path.write_text("VALUE = 'unauthorized'\n", encoding="utf-8")
        staged = run_git(root, "add", "--", "modules/example.py")
        self.assertEqual(staged.returncode, 0, staged.stdout + staged.stderr)

        refused = run_control(root, "audit")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("FAIL: BUSINESS_CHANGE_AUTHORIZATION", refused.stdout)
        self.assertIn("found []", refused.stdout)
        self.assertNotIn("UNEXPLAINED path", refused.stdout)

    def test_foundation_03_active_preflight_allows_business_write_in_work_item_scope(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        created = self.create_lifecycle_work_item(
            root,
            "WI-001",
            "HD-102",
            authorized_path="modules/example.py",
            code="APPLICABLE",
        )
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        started = self.start_command(root, "WI-001", "--path", "modules/example.py")
        self.assertEqual(started.returncode, 0, started.stdout + started.stderr)
        business_path = root / "modules/example.py"
        business_path.write_text("VALUE = 'authorized'\n", encoding="utf-8")
        staged = run_git(root, "add", "--", "modules/example.py")
        self.assertEqual(staged.returncode, 0, staged.stdout + staged.stderr)

        preflight = run_control(
            root,
            "preflight",
            "WI-001",
            "--path",
            "modules/example.py",
        )
        self.assertEqual(preflight.returncode, 0, preflight.stdout + preflight.stderr)
        self.assertIn("PASS: AUTHORIZED_PATHS", preflight.stdout)

    def test_foundation_04_active_preflight_refuses_business_write_outside_work_item_scope(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        created = self.create_lifecycle_work_item(
            root,
            "WI-001",
            "HD-102",
            authorized_path="modules/allowed.py",
            code="APPLICABLE",
        )
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        started = self.start_command(root, "WI-001", "--path", "modules/allowed.py")
        self.assertEqual(started.returncode, 0, started.stdout + started.stderr)
        outside_path = root / "modules/outside.py"
        outside_path.write_text("VALUE = 'outside'\n", encoding="utf-8")
        staged = run_git(root, "add", "--", "modules/outside.py")
        self.assertEqual(staged.returncode, 0, staged.stdout + staged.stderr)

        refused = run_control(root, "preflight", "WI-001")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("FAIL: AUTHORIZED_PATHS", refused.stdout)
        self.assertIn(
            "path outside Work Item authorization: modules/outside.py",
            refused.stdout,
        )

    def test_block_resume_01_block_closes_active_or_partial_run_without_faking_runtime(self) -> None:
        for original_result in ("IN_PROGRESS", "PARTIAL"):
            with self.subTest(original_result=original_result):
                temporary, root = self.make_normal_copy()
                self.addCleanup(temporary.cleanup)
                item = self.create_and_start_lifecycle_work_item(
                    root,
                    runtime_target="CONTROLLED_NON_PRODUCTION_RUNTIME",
                    code="APPLICABLE",
                    deployment="APPLICABLE",
                    runtime_proof="APPLICABLE",
                )
                self.switch_to_canonical(root)  # records live on the canonical branch only
                item_path = root / "project_control/work-items/WI-001.json"
                item.update(
                    development_status="DEVELOPED",
                    test_status="TESTED",
                    integration_status="INTEGRATED",
                    deployment_status="DEPLOYED_IN_CONTROLLED_ENVIRONMENT",
                    runtime_proof_status="FAILED",
                )
                item["evidence"]["tests"] = ["unit tests passed"]
                item["evidence"]["integration"] = ["integration checks passed"]
                item["evidence"]["deployment"] = ["controlled deployment prepared"]
                item["evidence"]["runtime_proof"] = ["service credentials unavailable"]
                item_path.write_text(json.dumps(item, indent=2) + "\n", encoding="utf-8")
                run_ref = item["agent_run_refs"][-1]
                run_path = root / f"project_control/agent-runs/{run_ref}.json"
                run = load_json(run_path)
                run["result"] = original_result
                partial_completed_at = "2026-08-22T12:13:41Z"
                if original_result == "PARTIAL":
                    run["completed_at"] = partial_completed_at
                    run["report_reference"] = "project_control/work-items/WI-001.json"
                run_path.write_text(json.dumps(run, indent=2) + "\n", encoding="utf-8")
                self.commit_fixture(root, "fixture: simulate execution state on canonical")

                self.record_lifecycle_human_decision(
                    root,
                    "HD-103",
                    "WI-001",
                    "Authorize WI-001 to enter BLOCKED on its external credential dependency.",
                )
                blocked = self.block_lifecycle_work_item(root, "WI-001", "HD-103")
                self.assertEqual(blocked.returncode, 0, blocked.stdout + blocked.stderr)

                blocked_item = load_json(item_path)
                self.assertEqual(blocked_item["status"], "BLOCKED")
                self.assertEqual(blocked_item["runtime_proof_status"], "FAILED")
                self.assertEqual(
                    blocked_item["evidence"]["runtime_proof"],
                    ["service credentials unavailable"],
                )
                self.assertNotEqual(blocked_item["runtime_proof_status"], "RUNTIME_PROVEN")
                self.assertNotEqual(blocked_item["runtime_proof_status"], "PRODUCTION_VERIFIED")
                self.assertEqual(blocked_item["human_decision_refs"][-1], "HD-103")
                self.assertEqual(len(blocked_item["block_records"]), 1)
                block_record = blocked_item["block_records"][0]
                self.assertEqual(block_record["type"], "EXTERNAL_DEPENDENCY")
                self.assertEqual(block_record["reason_code"], BLOCK_REASON_CODE)
                self.assertEqual(block_record["human_decision_id"], "HD-103")
                self.assertEqual(block_record["agent_run_ref"], run_ref)
                self.assertEqual(block_record["resume_condition"], BLOCK_RESUME_CONDITION)
                self.assertTrue(block_record["blocked_at"])
                self.assertIsNone(block_record["resolved_at"])
                self.assertIsNone(block_record["resolution_human_decision_id"])

                blocked_run = load_json(run_path)
                self.assertEqual(blocked_run["result"], "BLOCKED")
                self.assertTrue(blocked_run["completed_at"])
                if original_result == "PARTIAL":
                    self.assertEqual(blocked_run["completed_at"], partial_completed_at)
                self.assertEqual(
                    blocked_run["report_reference"],
                    "project_control/work-items/WI-001.json",
                )
                registry = (root / "docs/governance/WORKTREE_REGISTRY.md").read_text(
                    encoding="utf-8"
                )
                self.assertIn("WORK_ITEM_ID: WI-001", registry)
                self.assertIn("STATUS: BLOCKED", registry)
                roadmap = load_json(root / "docs/governance/roadmap-state.v1.json")
                summary = next(
                    value for value in roadmap["work_items"] if value["work_item_id"] == "WI-001"
                )
                self.assertEqual(summary["status"], "BLOCKED")
                self.assertNotEqual(summary["integration_state"], "ACTIVE_WORK")

                audit = run_control(root, "audit")
                self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)
                preflight = run_control(root, "preflight", "WI-001")
                self.assertNotEqual(preflight.returncode, 0)
                self.assertIn("FAIL: WORK_ITEM_AUTHORIZED", preflight.stdout)

    def test_block_resume_02_authorized_block_uses_separate_optional_external_history(self) -> None:
        schema = load_json(ROOT / "project_control/schemas/work-item.v1.schema.json")
        self.assertIn("block_records", schema["properties"])
        self.assertNotIn("block_records", schema["required"])
        record_schema = schema["properties"]["block_records"]["items"]
        self.assertEqual(record_schema["properties"]["type"]["const"], "EXTERNAL_DEPENDENCY")
        for field in (
            "type",
            "reason_code",
            "blocked_at",
            "human_decision_id",
            "agent_run_ref",
            "resume_condition",
            "resolved_at",
            "resolution_human_decision_id",
        ):
            self.assertIn(field, record_schema["required"])

        legacy = copy.deepcopy(self.work_item)
        legacy.pop("block_records", None)
        self.assertEqual(self.control_module.validate_work_item(legacy, "ALPHA"), [])

        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        created = self.create_lifecycle_work_item(
            root,
            "WI-001",
            "HD-102",
            depends_on=("WI-000",),
        )
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        item_path = root / "project_control/work-items/WI-001.json"
        created_item = load_json(item_path)
        self.assertEqual(created_item["block_records"], [])
        self.assertEqual(created_item["dependencies"], ["WI-000"])
        self.assertEqual(created_item["agent_run_refs"], [])

        self.record_lifecycle_human_decision(
            root,
            "HD-103",
            "WI-001",
            "Authorize blocking the authorized WI-001 before its first Agent Run.",
        )
        blocked = self.block_lifecycle_work_item(root, "WI-001", "HD-103")
        self.assertEqual(blocked.returncode, 0, blocked.stdout + blocked.stderr)
        blocked_item = load_json(item_path)
        self.assertEqual(blocked_item["status"], "BLOCKED")
        self.assertEqual(blocked_item["start_head"], "UNKNOWN")
        self.assertEqual(blocked_item["agent_run_refs"], [])
        self.assertEqual(blocked_item["dependencies"], ["WI-000"])
        self.assertEqual(len(blocked_item["block_records"]), 1)
        self.assertEqual(blocked_item["block_records"][0]["type"], "EXTERNAL_DEPENDENCY")
        self.assertIsNone(blocked_item["block_records"][0]["agent_run_ref"])
        invalid_run_reference = copy.deepcopy(blocked_item)
        invalid_run_reference["block_records"][0]["agent_run_ref"] = (
            "NOT_A_RUN_PREFIX"
        )
        self.assertTrue(
            any(
                "agent_run_ref" in error
                for error in self.control_module.validate_work_item(
                    invalid_run_reference,
                    "ALPHA",
                    "main",
                )
            )
        )
        roadmap = load_json(root / "docs/governance/roadmap-state.v1.json")
        summary = next(
            value for value in roadmap["work_items"] if value["work_item_id"] == "WI-001"
        )
        self.assertEqual(summary["integration_state"], "UNMERGED")
        audit = run_control(root, "audit")
        self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)

    def test_block_resume_03_block_requires_new_existing_linked_human_decision(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        self.create_and_start_lifecycle_work_item(root)
        self.switch_to_canonical(root)

        for decision_id in ("HD-999", "HD-102"):
            with self.subTest(decision_id=decision_id):
                before = self.lifecycle_snapshot(root)
                refused = self.block_lifecycle_work_item(root, "WI-001", decision_id)
                self.assertNotEqual(refused.returncode, 0)
                self.assertEqual(self.lifecycle_snapshot(root), before)

        self.record_lifecycle_human_decision(
            root,
            "HD-103",
            "WI-001",
            "Authorize blocking WI-001.",
            related_work_item="WI-999",
        )
        before = self.lifecycle_snapshot(root)
        refused = self.block_lifecycle_work_item(root, "WI-001", "HD-103")
        self.assertNotEqual(refused.returncode, 0)
        self.assertEqual(self.lifecycle_snapshot(root), before)
        item = load_json(root / "project_control/work-items/WI-001.json")
        self.assertEqual(item["status"], "IN_PROGRESS")
        self.assertNotIn("HD-103", item["human_decision_refs"])

    def test_block_resume_04_block_requires_reason_code_and_resume_condition_atomically(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        self.create_and_start_lifecycle_work_item(root)
        self.switch_to_canonical(root)
        self.record_lifecycle_human_decision(
            root,
            "HD-103",
            "WI-001",
            "Authorize blocking WI-001 on the declared external dependency.",
        )
        refused_commands = (
            (
                "block",
                "WI-001",
                "--human-decision",
                "HD-103",
                "--resume-condition",
                BLOCK_RESUME_CONDITION,
            ),
            (
                "block",
                "WI-001",
                "--human-decision",
                "HD-103",
                "--reason-code",
                BLOCK_REASON_CODE,
            ),
            (
                "block",
                "WI-001",
                "--human-decision",
                "HD-103",
                "--reason-code",
                "not-machine-readable",
                "--resume-condition",
                BLOCK_RESUME_CONDITION,
            ),
            (
                "block",
                "WI-001",
                "--human-decision",
                "HD-103",
                "--reason-code",
                BLOCK_REASON_CODE,
                "--resume-condition",
                " ",
            ),
        )
        for arguments in refused_commands:
            with self.subTest(arguments=arguments):
                before = self.lifecycle_snapshot(root)
                refused = run_control(root, *arguments)
                self.assertNotEqual(refused.returncode, 0)
                self.assertEqual(self.lifecycle_snapshot(root), before)

        blocked = self.block_lifecycle_work_item(root, "WI-001", "HD-103")
        self.assertEqual(blocked.returncode, 0, blocked.stdout + blocked.stderr)

    def test_block_resume_05_blocked_work_item_does_not_prevent_another_start(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        self.create_and_start_lifecycle_work_item(root)
        self.switch_to_canonical(root)
        self.record_lifecycle_human_decision(
            root,
            "HD-103",
            "WI-001",
            "Authorize blocking WI-001 while its external dependency is unresolved.",
        )
        blocked = self.block_lifecycle_work_item(root, "WI-001", "HD-103")
        self.assertEqual(blocked.returncode, 0, blocked.stdout + blocked.stderr)
        self.assertEqual(run_git(root, "status", "--porcelain=v1", "--untracked-files=all").stdout, "")

        created = self.create_lifecycle_work_item(root, "WI-002", "HD-104")
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        started = self.start_command(root, "WI-002")
        self.assertEqual(started.returncode, 0, started.stdout + started.stderr)
        self.assertEqual(
            load_json(root / "project_control/work-items/WI-001.json")["status"],
            "BLOCKED",
        )
        self.assertEqual(
            load_json(root / "project_control/work-items/WI-002.json")["status"],
            "IN_PROGRESS",
        )
        registry = (root / "docs/governance/WORKTREE_REGISTRY.md").read_text(
            encoding="utf-8"
        )
        self.assertEqual(registry.count("STATUS: ACTIVE"), 1)
        preflight = run_control(root, "preflight", "WI-002")
        self.assertEqual(preflight.returncode, 0, preflight.stdout + preflight.stderr)
        self.assertIn("PASS: SINGLE_ACTIVE_WORK_ITEM", preflight.stdout)

    def test_block_resume_06_resume_rejects_a_non_blocked_work_item_atomically(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        created = self.create_lifecycle_work_item(root, "WI-001", "HD-102")
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        self.record_lifecycle_human_decision(
            root,
            "HD-103",
            "WI-001",
            "Confirm the resume condition and authorize WI-001 to resume.",
            action="RESUME",
        )
        before = self.lifecycle_snapshot(root)
        refused = self.resume_lifecycle_work_item(root, "WI-001", "HD-103")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("must be BLOCKED", refused.stdout)
        self.assertEqual(self.lifecycle_snapshot(root), before)
        self.assertEqual(
            load_json(root / "project_control/work-items/WI-001.json")["status"],
            "AUTHORIZED",
        )

    def test_block_resume_07_resume_requires_new_existing_linked_human_decision(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        self.create_and_start_lifecycle_work_item(root)
        self.switch_to_canonical(root)
        self.record_lifecycle_human_decision(
            root,
            "HD-103",
            "WI-001",
            "Authorize blocking WI-001.",
        )
        blocked = self.block_lifecycle_work_item(root, "WI-001", "HD-103")
        self.assertEqual(blocked.returncode, 0, blocked.stdout + blocked.stderr)

        for decision_id in ("HD-999", "HD-103"):
            with self.subTest(decision_id=decision_id):
                before = self.lifecycle_snapshot(root)
                refused = self.resume_lifecycle_work_item(root, "WI-001", decision_id)
                self.assertNotEqual(refused.returncode, 0)
                self.assertEqual(self.lifecycle_snapshot(root), before)

        self.record_lifecycle_human_decision(
            root,
            "HD-104",
            "WI-001",
            "Confirm the resume condition and authorize WI-001 to resume.",
            related_work_item="WI-999",
            action="RESUME",
        )
        before = self.lifecycle_snapshot(root)
        refused = self.resume_lifecycle_work_item(root, "WI-001", "HD-104")
        self.assertNotEqual(refused.returncode, 0)
        self.assertEqual(self.lifecycle_snapshot(root), before)
        item_after = load_json(root / "project_control/work-items/WI-001.json")
        self.assertEqual(item_after["status"], "BLOCKED")
        self.assertIsNone(item_after["block_records"][-1]["resolved_at"])

    def test_block_resume_08_resume_fast_forwards_branch_and_preserves_history(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        item = self.create_and_start_lifecycle_work_item(
            root,
            runtime_target="CONTROLLED_NON_PRODUCTION_RUNTIME",
            deployment="APPLICABLE",
            runtime_proof="APPLICABLE",
        )
        branch_tip_after_start = run_git(root, "rev-parse", item["branch"]).stdout.strip()
        self.switch_to_canonical(root)  # records are edited and committed on the canonical branch only
        item_path = root / "project_control/work-items/WI-001.json"
        item["runtime_proof_status"] = "FAILED"
        item["evidence"]["runtime_proof"] = ["service credentials unavailable"]
        item_path.write_text(json.dumps(item, indent=2) + "\n", encoding="utf-8")
        initial_start_head = item["start_head"]
        first_run_ref = item["agent_run_refs"][0]
        integrated_head = self.commit_fixture(root, "test: prepare integrated WI-001")

        self.record_lifecycle_human_decision(
            root,
            "HD-103",
            "WI-001",
            "Authorize blocking WI-001 on its external service dependency.",
        )
        blocked = self.block_lifecycle_work_item(root, "WI-001", "HD-103")
        self.assertEqual(blocked.returncode, 0, blocked.stdout + blocked.stderr)
        blocked_tip = run_git(root, "rev-parse", "HEAD").stdout.strip()
        self.assertNotEqual(blocked_tip, integrated_head)  # block committed its records itself
        self.assertEqual(
            run_git(root, "rev-parse", item["branch"]).stdout.strip(),
            branch_tip_after_start,  # the Work Item branch never carries records
        )
        self.assertEqual(
            run_git(root, "merge-base", "--is-ancestor", item["branch"], "main").returncode,
            0,
        )

        self.record_lifecycle_human_decision(
            root,
            "HD-104",
            "WI-001",
            "Confirm the recorded resume condition is satisfied and authorize WI-001 to resume.",
            action="RESUME",
        )
        canonical_tip = run_git(root, "rev-parse", "HEAD").stdout.strip()
        self.assertNotEqual(canonical_tip, blocked_tip)
        resumed = self.resume_lifecycle_work_item(
            root,
            "WI-001",
            "HD-104",
            planned_paths=("reports/WI-001.txt",),
        )
        self.assertEqual(resumed.returncode, 0, resumed.stdout + resumed.stderr)
        self.assertIn("fast-forwarded", resumed.stdout)
        resumed_tip = run_git(root, "rev-parse", "main").stdout.strip()
        self.assertEqual(run_git(root, "rev-parse", f"{resumed_tip}^").stdout.strip(), canonical_tip)
        resumed_item = load_json(item_path)
        self.assertEqual(resumed_item["status"], "IN_PROGRESS")
        self.assertEqual(resumed_item["start_head"], initial_start_head)
        self.assertEqual(resumed_item["runtime_proof_status"], "FAILED")
        self.assertEqual(
            resumed_item["evidence"]["runtime_proof"],
            ["service credentials unavailable"],
        )
        self.assertEqual(resumed_item["human_decision_refs"][-2:], ["HD-103", "HD-104"])
        self.assertEqual(len(resumed_item["block_records"]), 1)
        resolved_record = copy.deepcopy(resumed_item["block_records"][0])
        self.assertEqual(resolved_record["agent_run_ref"], first_run_ref)
        self.assertTrue(resolved_record["resolved_at"])
        self.assertEqual(resolved_record["resolution_human_decision_id"], "HD-104")
        self.assertEqual(
            run_git(root, "branch", "--show-current").stdout.strip(),
            item["branch"],
        )
        self.assertEqual(run_git(root, "rev-parse", "HEAD").stdout.strip(), resumed_tip)
        self.assertEqual(run_git(root, "rev-parse", item["branch"]).stdout.strip(), resumed_tip)

        self.assertEqual(resumed_item["agent_run_refs"], [first_run_ref, "RUN-WI-001-002"])
        first_run = load_json(root / f"project_control/agent-runs/{first_run_ref}.json")
        second_run = load_json(root / "project_control/agent-runs/RUN-WI-001-002.json")
        self.assertEqual(first_run["result"], "BLOCKED")
        self.assertTrue(first_run["completed_at"])
        self.assertEqual(first_run["start_head"], initial_start_head)
        self.assertEqual(second_run["result"], "IN_PROGRESS")
        self.assertIsNone(second_run["completed_at"])
        self.assertEqual(second_run["start_head"], canonical_tip)
        self.assertEqual(second_run["branch"], item["branch"])
        self.assertEqual(second_run["base_head"], resumed_item["base_head"])
        registry = (root / "docs/governance/WORKTREE_REGISTRY.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("STATUS: ACTIVE", registry)
        audit = run_control(root, "audit")
        self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)
        preflight = run_control(root, "preflight", "WI-001", "--path", "reports/WI-001.txt")
        self.assertEqual(preflight.returncode, 0, preflight.stdout + preflight.stderr)

        resumed_item_bytes = item_path.read_bytes()
        invalid_resolution_time = copy.deepcopy(resumed_item)
        invalid_resolution_time["block_records"][0]["resolved_at"] = (
            "2000-01-01T00:00:00Z"
        )
        item_path.write_text(
            json.dumps(invalid_resolution_time, indent=2) + "\n",
            encoding="utf-8",
        )
        temporal_audit = run_control(root, "audit")
        self.assertNotEqual(temporal_audit.returncode, 0)
        self.assertIn("FAIL: SCHEMA_VALIDATION", temporal_audit.stdout)
        item_path.write_bytes(resumed_item_bytes)

        removed_run_mapping = copy.deepcopy(resumed_item)
        removed_run_mapping["block_records"][0]["agent_run_ref"] = None
        item_path.write_text(
            json.dumps(removed_run_mapping, indent=2) + "\n",
            encoding="utf-8",
        )
        mapping_audit = run_control(root, "audit")
        self.assertNotEqual(mapping_audit.returncode, 0)
        self.assertIn("FAIL: SCHEMA_VALIDATION", mapping_audit.stdout)
        item_path.write_bytes(resumed_item_bytes)

        first_run_path = root / f"project_control/agent-runs/{first_run_ref}.json"
        first_run_bytes = first_run_path.read_bytes()
        for historical_result in ("IN_PROGRESS", "PARTIAL"):
            with self.subTest(historical_result=historical_result):
                reactivated_first_run = load_json(first_run_path)
                reactivated_first_run["result"] = historical_result
                if historical_result == "IN_PROGRESS":
                    reactivated_first_run["completed_at"] = None
                first_run_path.write_text(
                    json.dumps(reactivated_first_run, indent=2) + "\n",
                    encoding="utf-8",
                )
                reactivated_audit = run_control(root, "audit")
                self.assertNotEqual(reactivated_audit.returncode, 0)
                self.assertIn("FAIL: SCHEMA_VALIDATION", reactivated_audit.stdout)
                first_run_path.write_bytes(first_run_bytes)

        self.switch_to_canonical(root)
        self.record_lifecycle_human_decision(
            root,
            "HD-105",
            "WI-001",
            "Authorize a second block after the resumed dependency becomes unavailable again.",
        )
        blocked_again = self.block_lifecycle_work_item(root, "WI-001", "HD-105")
        self.assertEqual(blocked_again.returncode, 0, blocked_again.stdout + blocked_again.stderr)
        twice_blocked = load_json(item_path)
        self.assertEqual(twice_blocked["status"], "BLOCKED")
        self.assertEqual(len(twice_blocked["block_records"]), 2)
        self.assertEqual(twice_blocked["block_records"][0], resolved_record)
        self.assertIsNone(twice_blocked["block_records"][1]["resolved_at"])
        self.assertEqual(twice_blocked["block_records"][1]["human_decision_id"], "HD-105")
        self.assertEqual(
            twice_blocked["block_records"][1]["agent_run_ref"],
            "RUN-WI-001-002",
        )
        self.assertEqual(
            load_json(root / "project_control/agent-runs/RUN-WI-001-002.json")["result"],
            "BLOCKED",
        )
        twice_blocked_bytes = item_path.read_bytes()
        invalid_history_order = copy.deepcopy(twice_blocked)
        invalid_history_order["block_records"][1]["blocked_at"] = (
            "2000-01-01T00:00:00Z"
        )
        item_path.write_text(
            json.dumps(invalid_history_order, indent=2) + "\n",
            encoding="utf-8",
        )
        order_audit = run_control(root, "audit")
        self.assertNotEqual(order_audit.returncode, 0)
        self.assertIn("FAIL: SCHEMA_VALIDATION", order_audit.stdout)
        item_path.write_bytes(twice_blocked_bytes)
        second_block_audit = run_control(root, "audit")
        self.assertEqual(
            second_block_audit.returncode,
            0,
            second_block_audit.stdout + second_block_audit.stderr,
        )

    def test_block_resume_09_close_rejects_blocked_without_mutation(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        self.create_and_start_lifecycle_work_item(root)
        self.switch_to_canonical(root)
        self.record_lifecycle_human_decision(
            root,
            "HD-103",
            "WI-001",
            "Authorize blocking WI-001.",
        )
        blocked = self.block_lifecycle_work_item(root, "WI-001", "HD-103")
        self.assertEqual(blocked.returncode, 0, blocked.stdout + blocked.stderr)
        before = self.lifecycle_snapshot(root)
        refused = run_control(
            root,
            "close",
            "WI-001",
            "--test-evidence",
            "tests passed",
            "--integration-evidence",
            "integration passed",
        )
        self.assertNotEqual(refused.returncode, 0)
        self.assertEqual(self.lifecycle_snapshot(root), before)
        self.assertEqual(
            load_json(root / "project_control/work-items/WI-001.json")["status"],
            "BLOCKED",
        )

    def test_block_resume_10_audit_rejects_incoherent_block_history(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        created = self.create_lifecycle_work_item(root, "WI-001", "HD-102")
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        self.record_lifecycle_human_decision(
            root,
            "HD-103",
            "WI-001",
            "Authorize blocking WI-001.",
        )
        blocked = self.block_lifecycle_work_item(root, "WI-001", "HD-103")
        self.assertEqual(blocked.returncode, 0, blocked.stdout + blocked.stderr)
        item_path = root / "project_control/work-items/WI-001.json"
        coherent_bytes = item_path.read_bytes()
        coherent = load_json(item_path)
        corruptions = {
            "missing record": lambda item: item.update(block_records=[]),
            "missing reason": lambda item: item["block_records"][-1].update(reason_code=""),
            "missing decision": lambda item: item["block_records"][-1].update(
                human_decision_id="HD-999"
            ),
            "missing condition": lambda item: item["block_records"][-1].update(
                resume_condition=""
            ),
            "resolved while blocked": lambda item: item["block_records"][-1].update(
                resolved_at="2026-08-22T13:00:00Z",
                resolution_human_decision_id="HD-103",
            ),
            "two unresolved records": lambda item: item["block_records"].append(
                copy.deepcopy(item["block_records"][-1])
            ),
        }
        for label, corrupt in corruptions.items():
            with self.subTest(label=label):
                candidate = copy.deepcopy(coherent)
                corrupt(candidate)
                item_path.write_text(json.dumps(candidate, indent=2) + "\n", encoding="utf-8")
                audit = run_control(root, "audit")
                self.assertNotEqual(audit.returncode, 0)
                self.assertIn("FAIL: SCHEMA_VALIDATION", audit.stdout)
                item_path.write_bytes(coherent_bytes)

        audit = run_control(root, "audit")
        self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)

    def test_block_resume_11_audit_rejects_orphan_and_nonreciprocal_agent_runs(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        item = self.create_and_start_lifecycle_work_item(root)
        item_path = root / "project_control/work-items/WI-001.json"
        run_path = root / f"project_control/agent-runs/{item['agent_run_refs'][0]}.json"
        item_bytes = item_path.read_bytes()
        run_bytes = run_path.read_bytes()

        orphaned_item = load_json(item_path)
        orphaned_item["agent_run_refs"] = []
        item_path.write_text(
            json.dumps(orphaned_item, indent=2) + "\n",
            encoding="utf-8",
        )
        orphan_audit = run_control(root, "audit")
        self.assertNotEqual(orphan_audit.returncode, 0)
        self.assertIn("FAIL: SCHEMA_VALIDATION", orphan_audit.stdout)
        item_path.write_bytes(item_bytes)

        nonreciprocal_run = load_json(run_path)
        nonreciprocal_run["work_item_id"] = "WI-000"
        run_path.write_text(
            json.dumps(nonreciprocal_run, indent=2) + "\n",
            encoding="utf-8",
        )
        nonreciprocal_audit = run_control(root, "audit")
        self.assertNotEqual(nonreciprocal_audit.returncode, 0)
        self.assertIn("FAIL: SCHEMA_VALIDATION", nonreciprocal_audit.stdout)
        run_path.write_bytes(run_bytes)

        audit = run_control(root, "audit")
        self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)

    def test_block_resume_12_resume_branch_absence_depends_on_prior_start(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        blocked_item = self.prepare_clean_blocked_started_work_item(root)
        branch = blocked_item["branch"]
        deleted = run_git(root, "branch", "-d", branch)
        self.assertEqual(deleted.returncode, 0, deleted.stdout + deleted.stderr)
        self.record_lifecycle_human_decision(
            root,
            "HD-104",
            "WI-001",
            "Confirm the resume condition and authorize the previously started WI-001 to resume.",
            action="RESUME",
        )
        before = self.lifecycle_snapshot(root)
        refused = self.resume_lifecycle_work_item(root, "WI-001", "HD-104")
        self.assertNotEqual(refused.returncode, 0)
        self.assertEqual(self.lifecycle_snapshot(root), before)
        self.assertNotEqual(
            run_git(root, "show-ref", "--verify", "--quiet", f"refs/heads/{branch}").returncode,
            0,
        )
        still_blocked = load_json(root / "project_control/work-items/WI-001.json")
        self.assertEqual(still_blocked["status"], "BLOCKED")
        self.assertEqual(still_blocked["agent_run_refs"], ["RUN-WI-001-001"])

        authorized_temporary, authorized_root = self.make_normal_copy()
        self.addCleanup(authorized_temporary.cleanup)
        created = self.create_lifecycle_work_item(
            authorized_root,
            "WI-001",
            "HD-102",
        )
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        authorized_item_path = (
            authorized_root / "project_control/work-items/WI-001.json"
        )
        authorized_item = load_json(authorized_item_path)
        self.assertEqual(authorized_item["start_head"], "UNKNOWN")
        self.assertEqual(authorized_item["agent_run_refs"], [])
        self.assertNotEqual(
            run_git(
                authorized_root,
                "show-ref",
                "--verify",
                "--quiet",
                f"refs/heads/{authorized_item['branch']}",
            ).returncode,
            0,
        )
        self.record_lifecycle_human_decision(
            authorized_root,
            "HD-103",
            "WI-001",
            "Authorize blocking authorized WI-001 before its first run.",
        )
        blocked = self.block_lifecycle_work_item(
            authorized_root,
            "WI-001",
            "HD-103",
        )
        self.assertEqual(blocked.returncode, 0, blocked.stdout + blocked.stderr)
        self.record_lifecycle_human_decision(
            authorized_root,
            "HD-104",
            "WI-001",
            "Confirm the resume condition and authorize first start of WI-001.",
            action="RESUME",
        )
        canonical_tip = run_git(authorized_root, "rev-parse", "HEAD").stdout.strip()
        resumed = self.resume_lifecycle_work_item(
            authorized_root,
            "WI-001",
            "HD-104",
        )
        self.assertEqual(resumed.returncode, 0, resumed.stdout + resumed.stderr)
        resumed_item = load_json(authorized_item_path)
        self.assertEqual(resumed_item["status"], "IN_PROGRESS")
        self.assertEqual(resumed_item["start_head"], canonical_tip)
        self.assertEqual(resumed_item["agent_run_refs"], ["RUN-WI-001-001"])
        first_run = load_json(
            authorized_root / "project_control/agent-runs/RUN-WI-001-001.json"
        )
        self.assertEqual(first_run["result"], "IN_PROGRESS")
        self.assertEqual(first_run["start_head"], canonical_tip)
        audit = run_control(authorized_root, "audit")
        self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)

    def test_block_resume_13_resume_restores_git_when_file_rollback_raises(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        blocked_item = self.prepare_clean_blocked_started_work_item(root)
        branch = blocked_item["branch"]
        historical_branch_tip = run_git(root, "rev-parse", branch).stdout.strip()
        self.record_lifecycle_human_decision(
            root,
            "HD-104",
            "WI-001",
            "Confirm the resume condition and authorize WI-001 to resume.",
            action="RESUME",
        )
        canonical_tip = run_git(root, "rev-parse", "HEAD").stdout.strip()
        self.assertNotEqual(historical_branch_tip, canonical_tip)
        digest = self.authorities_digest(root, "WI-001")
        self.assertIsNotNone(digest)
        control = self.control_module.ProjectControl(root)

        def injected_post_write_failure() -> None:
            raise self.control_module.ProjectControlError("injected post-write failure")

        real_rollback = self.control_module.FileTransaction.rollback

        def rollback_then_raise(transaction) -> None:
            real_rollback(transaction)
            raise OSError("injected file rollback failure")

        control.verify_post_mutation = injected_post_write_failure
        self.control_module.FileTransaction.rollback = rollback_then_raise
        try:
            with self.assertRaises(Exception) as raised:
                control.resume_work_item(
                    "WI-001",
                    [],
                    "FixtureAgent",
                    "HD-104",
                    digest,
                )
        finally:
            self.control_module.FileTransaction.rollback = real_rollback
        self.assertIn("injected", str(raised.exception))
        self.assertEqual(run_git(root, "branch", "--show-current").stdout.strip(), "main")
        self.assertEqual(run_git(root, "rev-parse", "main").stdout.strip(), canonical_tip)
        self.assertEqual(run_git(root, "rev-parse", branch).stdout.strip(), historical_branch_tip)
        rolled_back_item = load_json(root / "project_control/work-items/WI-001.json")
        self.assertEqual(rolled_back_item["status"], "BLOCKED")
        self.assertIsNone(rolled_back_item["block_records"][-1]["resolved_at"])
        self.assertFalse(
            (root / "project_control/agent-runs/RUN-WI-001-002.json").exists()
        )
        audit = run_control(root, "audit")
        self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)

    def test_block_resume_14_reject_chosen_option_cannot_authorize_transitions(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        self.create_and_start_lifecycle_work_item(root)
        self.switch_to_canonical(root)
        self.record_lifecycle_human_decision(
            root,
            "HD-103",
            "WI-001",
            "Reject blocking WI-001.",
            chosen_option="REJECT",
        )
        before_block = self.lifecycle_snapshot(root)
        refused_block = self.block_lifecycle_work_item(root, "WI-001", "HD-103")
        self.assertNotEqual(refused_block.returncode, 0)
        self.assertEqual(self.lifecycle_snapshot(root), before_block)
        self.assertEqual(
            load_json(root / "project_control/work-items/WI-001.json")["status"],
            "IN_PROGRESS",
        )

        resume_temporary, resume_root = self.make_normal_copy()
        self.addCleanup(resume_temporary.cleanup)
        self.prepare_clean_blocked_started_work_item(resume_root)
        self.record_lifecycle_human_decision(
            resume_root,
            "HD-104",
            "WI-001",
            "Reject resuming WI-001.",
            action="RESUME",
            chosen_option="REJECT",
        )
        before_resume = self.lifecycle_snapshot(resume_root)
        refused_resume = self.resume_lifecycle_work_item(
            resume_root,
            "WI-001",
            "HD-104",
        )
        self.assertNotEqual(refused_resume.returncode, 0)
        self.assertEqual(self.lifecycle_snapshot(resume_root), before_resume)
        resume_item = load_json(
            resume_root / "project_control/work-items/WI-001.json"
        )
        self.assertEqual(resume_item["status"], "BLOCKED")
        self.assertIsNone(resume_item["block_records"][-1]["resolved_at"])

    def test_block_resume_15_resume_rejects_branch_that_lost_agent_run_commit(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        blocked_item = self.prepare_clean_blocked_started_work_item(root)
        branch = blocked_item["branch"]
        switched = run_git(root, "switch", branch)
        self.assertEqual(switched.returncode, 0, switched.stdout + switched.stderr)
        committed = run_git(
            root,
            "-c",
            "user.name=Fixture Owner",
            "-c",
            "user.email=fixture@example.invalid",
            "commit",
            "--allow-empty",
            "-m",
            "test: historical Agent Run-only commit",
        )
        self.assertEqual(committed.returncode, 0, committed.stdout + committed.stderr)
        run_only_commit = run_git(root, "rev-parse", "HEAD").stdout.strip()
        switched = run_git(root, "switch", "main")
        self.assertEqual(switched.returncode, 0, switched.stdout + switched.stderr)

        run_ref = blocked_item["agent_run_refs"][0]
        run_path = root / f"project_control/agent-runs/{run_ref}.json"
        run = load_json(run_path)
        run["commits"] = [run_only_commit]
        run_path.write_text(json.dumps(run, indent=2) + "\n", encoding="utf-8")
        item_path = root / "project_control/work-items/WI-001.json"
        self.assertEqual(load_json(item_path)["commits"], [])
        self.record_lifecycle_human_decision(
            root,
            "HD-104",
            "WI-001",
            "Confirm the resume condition and authorize WI-001 to resume.",
            action="RESUME",
        )
        canonical_tip = run_git(root, "rev-parse", "HEAD").stdout.strip()
        rewritten = run_git(root, "branch", "-f", branch, "main")
        self.assertEqual(rewritten.returncode, 0, rewritten.stdout + rewritten.stderr)
        self.assertEqual(run_git(root, "rev-parse", branch).stdout.strip(), canonical_tip)
        self.assertNotEqual(
            run_git(
                root,
                "merge-base",
                "--is-ancestor",
                run_only_commit,
                branch,
            ).returncode,
            0,
        )

        before = self.lifecycle_snapshot(root)
        refused = self.resume_lifecycle_work_item(root, "WI-001", "HD-104")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn(run_only_commit, refused.stdout)
        self.assertEqual(self.lifecycle_snapshot(root), before)
        still_blocked = load_json(item_path)
        self.assertEqual(still_blocked["status"], "BLOCKED")
        self.assertEqual(still_blocked["agent_run_refs"], [run_ref])
        self.assertFalse(
            (root / "project_control/agent-runs/RUN-WI-001-002.json").exists()
        )

    def test_block_resume_16_authorized_resume_accepts_only_absent_or_canonical_tip_branch(self) -> None:
        for relation in ("AHEAD", "DIVERGENT"):
            with self.subTest(relation=relation):
                temporary, root = self.make_normal_copy()
                self.addCleanup(temporary.cleanup)
                blocked_item = self.prepare_clean_blocked_authorized_work_item(root)
                branch = blocked_item["branch"]
                self.record_lifecycle_human_decision(
                    root,
                    "HD-104",
                    "WI-001",
                    "Confirm the resume condition and authorize first start of WI-001.",
                    action="RESUME",
                )
                canonical_tip = run_git(root, "rev-parse", "HEAD").stdout.strip()
                start_point = "main" if relation == "AHEAD" else "main~1"
                created_branch = run_git(root, "switch", "-c", branch, start_point)
                self.assertEqual(
                    created_branch.returncode,
                    0,
                    created_branch.stdout + created_branch.stderr,
                )
                advanced = run_git(
                    root,
                    "-c",
                    "user.name=Fixture Owner",
                    "-c",
                    "user.email=fixture@example.invalid",
                    "commit",
                    "--allow-empty",
                    "-m",
                    f"test: {relation.lower()} preexisting authorized branch",
                )
                self.assertEqual(advanced.returncode, 0, advanced.stdout + advanced.stderr)
                switched = run_git(root, "switch", "main")
                self.assertEqual(switched.returncode, 0, switched.stdout + switched.stderr)
                branch_tip = run_git(root, "rev-parse", branch).stdout.strip()
                self.assertNotEqual(branch_tip, canonical_tip)
                if relation == "AHEAD":
                    self.assertEqual(
                        run_git(
                            root,
                            "merge-base",
                            "--is-ancestor",
                            "main",
                            branch,
                        ).returncode,
                        0,
                    )
                else:
                    self.assertNotEqual(
                        run_git(
                            root,
                            "merge-base",
                            "--is-ancestor",
                            "main",
                            branch,
                        ).returncode,
                        0,
                    )
                    self.assertNotEqual(
                        run_git(
                            root,
                            "merge-base",
                            "--is-ancestor",
                            branch,
                            "main",
                        ).returncode,
                        0,
                    )
                before = self.lifecycle_snapshot(root)
                refused = self.resume_lifecycle_work_item(root, "WI-001", "HD-104")
                self.assertNotEqual(refused.returncode, 0)
                self.assertEqual(self.lifecycle_snapshot(root), before)
                still_blocked = load_json(
                    root / "project_control/work-items/WI-001.json"
                )
                self.assertEqual(still_blocked["status"], "BLOCKED")
                self.assertEqual(still_blocked["start_head"], "UNKNOWN")
                self.assertEqual(still_blocked["agent_run_refs"], [])

        equal_temporary, equal_root = self.make_normal_copy()
        self.addCleanup(equal_temporary.cleanup)
        equal_item = self.prepare_clean_blocked_authorized_work_item(equal_root)
        self.record_lifecycle_human_decision(
            equal_root,
            "HD-104",
            "WI-001",
            "Confirm the resume condition and authorize first start of WI-001.",
            action="RESUME",
        )
        canonical_tip = run_git(equal_root, "rev-parse", "HEAD").stdout.strip()
        created_equal_branch = run_git(
            equal_root,
            "branch",
            equal_item["branch"],
            "main",
        )
        self.assertEqual(
            created_equal_branch.returncode,
            0,
            created_equal_branch.stdout + created_equal_branch.stderr,
        )
        self.assertEqual(
            run_git(equal_root, "rev-parse", equal_item["branch"]).stdout.strip(),
            canonical_tip,
        )
        resumed = self.resume_lifecycle_work_item(
            equal_root,
            "WI-001",
            "HD-104",
        )
        self.assertEqual(resumed.returncode, 0, resumed.stdout + resumed.stderr)
        resumed_item = load_json(
            equal_root / "project_control/work-items/WI-001.json"
        )
        self.assertEqual(resumed_item["status"], "IN_PROGRESS")
        self.assertEqual(resumed_item["start_head"], canonical_tip)
        self.assertEqual(resumed_item["agent_run_refs"], ["RUN-WI-001-001"])

    def test_block_resume_17_duplicate_conflicting_lifecycle_field_is_refused(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        self.create_and_start_lifecycle_work_item(root)
        self.switch_to_canonical(root)
        self.record_lifecycle_human_decision(
            root,
            "HD-103",
            "WI-001",
            "Contradictory authorization for blocking WI-001.",
            chosen_option="AUTHORIZE",
            duplicate_chosen_option="REJECT",
        )
        before_block = self.lifecycle_snapshot(root)
        refused_block = self.block_lifecycle_work_item(root, "WI-001", "HD-103")
        self.assertNotEqual(refused_block.returncode, 0)
        self.assertEqual(self.lifecycle_snapshot(root), before_block)

        resume_temporary, resume_root = self.make_normal_copy()
        self.addCleanup(resume_temporary.cleanup)
        self.prepare_clean_blocked_started_work_item(resume_root)
        self.record_lifecycle_human_decision(
            resume_root,
            "HD-104",
            "WI-001",
            "Contradictory authorization for resuming WI-001.",
            action="RESUME",
            chosen_option="AUTHORIZE",
            duplicate_chosen_option="REJECT",
        )
        before_resume = self.lifecycle_snapshot(resume_root)
        refused_resume = self.resume_lifecycle_work_item(
            resume_root,
            "WI-001",
            "HD-104",
        )
        self.assertNotEqual(refused_resume.returncode, 0)
        self.assertEqual(self.lifecycle_snapshot(resume_root), before_resume)
        blocked_item = load_json(
            resume_root / "project_control/work-items/WI-001.json"
        )
        self.assertEqual(blocked_item["status"], "BLOCKED")
        self.assertIsNone(blocked_item["block_records"][-1]["resolved_at"])

    def test_resume_requires_current_execution_evidence_and_preserves_failed_report(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        item = self.create_and_start_lifecycle_work_item(
            root, runtime_target="CONTROLLED_NON_PRODUCTION_RUNTIME",
        )
        old_evidence = self.write_committed_evidence(root, "WI-001")
        directory = root / "reports/evidence/WI-001"
        failed_artifact = directory / "runtime-failed.txt"
        failed_artifact.write_text("Synthetic failure: external service unavailable.\n")
        failed_report = load_json(root / old_evidence["runtime_proof"])
        failed_report.update(
            result="FAIL", summary="Synthetic failure before blocking.",
            artifacts=[{
                "path": "reports/evidence/WI-001/runtime-failed.txt",
                "sha256": hashlib.sha256(failed_artifact.read_bytes()).hexdigest(),
            }],
        )
        failed_path = "reports/evidence/WI-001/runtime-failed.json"
        (root / failed_path).write_text(json.dumps(failed_report, indent=2) + "\n")
        self.commit_fixture(root, "fixture: preserve failed observation")
        self.fast_forward_fixture_branch(root, item["branch"])
        # The record itself is only edited on the canonical branch.
        item["runtime_proof_status"] = "FAILED"
        item["evidence"]["runtime_proof"] = [failed_path]
        item_path = root / "project_control/work-items/WI-001.json"
        item_path.write_text(json.dumps(item, indent=2) + "\n")
        self.commit_fixture(root, "fixture: record failed observation on canonical")
        self.record_lifecycle_human_decision(root, "HD-103", "WI-001", "Authorize external dependency block.")
        blocked = self.block_lifecycle_work_item(root, "WI-001", "HD-103")
        self.assertEqual(blocked.returncode, 0, blocked.stdout + blocked.stderr)
        first_run_path = root / f"project_control/agent-runs/{item['agent_run_refs'][0]}.json"
        blocked_run_bytes = first_run_path.read_bytes()
        failed_bytes = (root / failed_path).read_bytes()
        before_status = self.snapshot_repository(root)
        status = run_control(root, "status", "--json")
        self.assertEqual(status.returncode, 0, status.stdout + status.stderr)
        view = next(v for v in json.loads(status.stdout)["work_items"] if v["work_item_id"] == "WI-001")
        self.assertEqual(view["block"]["resume_condition"], BLOCK_RESUME_CONDITION)
        self.assertEqual(self.snapshot_repository(root), before_status)
        self.record_lifecycle_human_decision(
            root, "HD-104", "WI-001", "Confirm service availability and authorize resume.", action="RESUME",
        )
        resume_head = run_git(root, "rev-parse", "HEAD").stdout.strip()
        resumed = self.resume_lifecycle_work_item(root, "WI-001", "HD-104")
        self.assertEqual(resumed.returncode, 0, resumed.stdout + resumed.stderr)
        resumed_item = load_json(item_path)
        self.assertEqual(resumed_item["start_head"], item["start_head"])
        self.assertEqual(resumed_item["runtime_proof_status"], "FAILED")
        control = self.control_module.ProjectControl(root)
        self.assertEqual(control.latest_run_start_head(resumed_item), resume_head)
        with self.assertRaisesRegex(self.control_module.ProjectControlError, "between start_head"):
            control.validate_evidence(resumed_item, "tests", old_evidence["tests"], resume_head)
        # A later fix must not invalidate the retained, explicitly failed historical report.
        (root / "reports/WI-001.txt").write_text("Corrected behavior after authorized resume.\n")
        self.commit_fixture(root, "fixture: correct behavior after resume")
        self.fast_forward_fixture_branch(root, item["branch"])
        fresh_evidence = self.write_committed_evidence(root, "WI-001", revision="-resumed")
        closed = self.close_with_evidence(root, "WI-001", fresh_evidence)
        self.assertEqual(closed.returncode, 0, closed.stdout + closed.stderr)
        closed_item = load_json(item_path)
        self.assertEqual(closed_item["evidence"]["runtime_proof"], [failed_path, fresh_evidence["runtime_proof"]])
        self.assertEqual(closed_item["runtime_proof_status"], "RUNTIME_PROVEN")
        self.assertEqual(first_run_path.read_bytes(), blocked_run_bytes)
        self.assertEqual((root / failed_path).read_bytes(), failed_bytes)
        audit = run_control(root, "audit")
        self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)

    def test_custom_canonical_branch_allows_main_as_work_branch(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        renamed = run_git(root, "branch", "-m", "canonical")
        self.assertEqual(renamed.returncode, 0, renamed.stdout + renamed.stderr)
        path = root / "docs/governance/REPOSITORY_STATUS.md"
        path.write_text(path.read_text().replace("CANONICAL BRANCH: main", "CANONICAL BRANCH: canonical"))
        self.commit_fixture(root, "fixture: declare custom canonical branch")
        created = self.create_lifecycle_work_item(
            root, "WI-001", "HD-102", branch="main", code="APPLICABLE",
            authorized_path="modules/example.py", tests="NOT_APPLICABLE", integration="NOT_APPLICABLE",
        )
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        started = self.start_command(root, "WI-001")
        self.assertEqual(started.returncode, 0, started.stdout + started.stderr)
        self.assertEqual(run_git(root, "branch", "--show-current").stdout.strip(), "main")
        (root / "modules/example.py").write_text("VALUE = 1\n")
        commit = self.commit_fixture(root, "fixture: implement authorized module")
        # close runs on the declared canonical branch, once the work branch is integrated.
        switched = run_git(root, "switch", "canonical")
        self.assertEqual(switched.returncode, 0, switched.stdout + switched.stderr)
        merged = run_git(root, "merge", "--ff-only", "main")
        self.assertEqual(merged.returncode, 0, merged.stdout + merged.stderr)
        closed = run_control(root, "close", "WI-001", "--commit", commit)
        self.assertEqual(closed.returncode, 0, closed.stdout + closed.stderr)
        self.assertEqual(run_git(root, "branch", "--show-current").stdout.strip(), "canonical")
        audit = run_control(root, "audit")
        self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)

    def prepare_blocked_branch_with_own_commit_and_integrated_sibling(
        self, root: Path, *, shared_path: str | None = None,
    ) -> tuple[dict, str, str]:
        """WI-001 commits partial work, is blocked, then WI-002 is integrated and closed on main.

        Records live on the canonical branch only: no manual synchronisation is needed.
        """
        item = self.create_and_start_lifecycle_work_item(
            root, "WI-001", "HD-102", authorized_path=shared_path or "reports/WI-001.txt",
        )
        (root / (shared_path or "reports/WI-001.txt")).write_text("partial work before block\n", encoding="utf-8")
        old_tip = self.commit_fixture(root, "feat: WI-001 partial work")
        self.switch_to_canonical(root)
        self.record_lifecycle_human_decision(root, "HD-103", "WI-001", "Authorize blocking WI-001.")
        blocked = self.block_lifecycle_work_item(root, "WI-001", "HD-103")
        self.assertEqual(blocked.returncode, 0, blocked.stdout + blocked.stderr)
        audit = run_control(root, "audit")
        self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)
        created = self.create_lifecycle_work_item(
            root, "WI-002", "HD-104", authorized_path=shared_path or "reports/WI-002.txt",
        )
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        started = self.start_command(root, "WI-002")
        self.assertEqual(started.returncode, 0, started.stdout + started.stderr)
        sibling_branch = run_git(root, "branch", "--show-current").stdout.strip()
        (root / (shared_path or "reports/WI-002.txt")).write_text("WI-002 change\n", encoding="utf-8")
        self.commit_fixture(root, "feat: WI-002 change")
        self.merge_fixture_branch(root, sibling_branch, "merge: integrate WI-002")
        evidence = self.write_committed_evidence(root, "WI-002")
        closed = self.close_with_evidence(root, "WI-002", evidence)
        self.assertEqual(closed.returncode, 0, closed.stdout + closed.stderr)
        self.record_lifecycle_human_decision(root, "HD-105", "WI-001", "Confirm resume of WI-001.", action="RESUME")
        canonical_tip = run_git(root, "rev-parse", "HEAD").stdout.strip()
        self.assertEqual(run_git(root, "status", "--porcelain=v1", "--untracked-files=all").stdout, "")
        self.assertEqual(run_git(root, "rev-parse", item["branch"]).stdout.strip(), old_tip)
        self.assertNotEqual(run_git(root, "merge-base", "--is-ancestor", old_tip, canonical_tip).returncode, 0)
        self.assertNotEqual(run_git(root, "merge-base", "--is-ancestor", canonical_tip, old_tip).returncode, 0)
        return item, old_tip, canonical_tip

    def test_resume_aligns_diverged_branch_by_merge_and_closes(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        item, old_tip, canonical_tip = self.prepare_blocked_branch_with_own_commit_and_integrated_sibling(root)
        branch = item["branch"]

        resumed = self.resume_lifecycle_work_item(root, "WI-001", "HD-105")
        self.assertEqual(resumed.returncode, 0, resumed.stdout + resumed.stderr)
        self.assertIn("merge commit", resumed.stdout)
        self.assertEqual(run_git(root, "branch", "--show-current").stdout.strip(), branch)
        merge_commit = run_git(root, "rev-parse", "HEAD").stdout.strip()
        resumed_tip = run_git(root, "rev-parse", "main").stdout.strip()
        # resume committed its records on the canonical branch first, then merged that tip into the branch.
        self.assertEqual(run_git(root, "rev-parse", f"{resumed_tip}^").stdout.strip(), canonical_tip)
        parents = run_git(root, "rev-list", "--parents", "-n", "1", merge_commit).stdout.split()[1:]
        self.assertEqual(sorted(parents), sorted([old_tip, resumed_tip]))
        self.assertEqual(run_git(root, "merge-base", "--is-ancestor", old_tip, "HEAD").returncode, 0)
        # Business changes are merged; the Work Item's own partial work is preserved.
        self.assertEqual((root / "reports/WI-002.txt").read_text(encoding="utf-8"), "WI-002 change\n")
        self.assertEqual((root / "reports/WI-001.txt").read_text(encoding="utf-8"), "partial work before block\n")
        # Administrative records come from the canonical branch, then the resume transaction applies.
        for path in ("project_control/work-items/WI-001.json", "project_control/work-items/WI-002.json",
                     "docs/governance/roadmap-state.v1.json"):
            canonical_version = run_git(root, "show", f"{resumed_tip}:{path}").stdout
            merged_version = run_git(root, "show", f"{merge_commit}:{path}").stdout
            self.assertEqual(canonical_version, merged_version, path)
        self.assertEqual(load_json(root / "project_control/work-items/WI-002.json")["status"], "DONE")
        resumed_item = load_json(root / "project_control/work-items/WI-001.json")
        self.assertEqual(resumed_item["status"], "IN_PROGRESS")
        self.assertEqual(len(resumed_item["agent_run_refs"]), 2)
        self.assertEqual(resumed_item["block_records"][-1]["resolution_human_decision_id"], "HD-105")
        second_run = load_json(root / f"project_control/agent-runs/{resumed_item['agent_run_refs'][-1]}.json")
        self.assertEqual(second_run["start_head"], canonical_tip)
        preflight = run_control(root, "preflight", "WI-001", "--path", "reports/WI-001.txt")
        self.assertEqual(preflight.returncode, 0, preflight.stdout + preflight.stderr)
        audit = run_control(root, "audit")
        self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)

        # Finish the resumed Work Item: correct, integrate, prove, close. The branch is clean after resume.
        self.assertEqual(run_git(root, "status", "--porcelain=v1", "--untracked-files=all").stdout, "")
        (root / "reports/WI-001.txt").write_text("work completed after resume\n", encoding="utf-8")
        self.commit_fixture(root, "feat: WI-001 completed")
        self.merge_fixture_branch(root, branch, "merge: integrate WI-001")
        evidence = self.write_committed_evidence(root, "WI-001")
        closed = self.close_with_evidence(root, "WI-001", evidence)
        self.assertEqual(closed.returncode, 0, closed.stdout + closed.stderr)
        self.assertEqual(load_json(root / "project_control/work-items/WI-001.json")["status"], "DONE")
        audit = run_control(root, "audit")
        self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)

    def test_resume_refuses_business_conflict_and_restores_git_state(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        item, old_tip, canonical_tip = self.prepare_blocked_branch_with_own_commit_and_integrated_sibling(
            root, shared_path="reports/shared.txt",
        )
        before = self.lifecycle_snapshot(root)
        refused = self.resume_lifecycle_work_item(root, "WI-001", "HD-105")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("business conflicts", refused.stdout + refused.stderr)
        self.assertIn("reports/shared.txt", refused.stdout + refused.stderr)
        self.assertEqual(self.lifecycle_snapshot(root), before)
        self.assertEqual(run_git(root, "branch", "--show-current").stdout.strip(), "main")
        self.assertEqual(run_git(root, "rev-parse", "HEAD").stdout.strip(), canonical_tip)
        self.assertEqual(run_git(root, "rev-parse", item["branch"]).stdout.strip(), old_tip)
        self.assertNotEqual(run_git(root, "rev-parse", "-q", "--verify", "MERGE_HEAD").returncode, 0)
        self.assertEqual(run_git(root, "status", "--porcelain=v1", "--untracked-files=all").stdout, "")
        self.assertEqual(load_json(root / "project_control/work-items/WI-001.json")["status"], "BLOCKED")

    def test_records_live_on_canonical_branch_only(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        item = self.create_and_start_lifecycle_work_item(root)
        branch = item["branch"]
        # The Work Item branch starts at the records commit and never carries administrative changes.
        self.assertEqual(run_git(root, "diff", "--name-only", "main", branch, "--", "project_control", "docs/governance").stdout, "")
        self.assertEqual(run_git(root, "status", "--porcelain=v1", "--untracked-files=all").stdout, "")
        # S-04: from the canonical branch, status is exact.
        self.switch_to_canonical(root)
        status = run_control(root, "status", "--json")
        self.assertEqual(status.returncode, 0, status.stdout + status.stderr)
        view = next(v for v in json.loads(status.stdout)["work_items"] if v["work_item_id"] == "WI-001")
        self.assertEqual(view["status"], "IN_PROGRESS")
        # S-01: a second start from the canonical branch sees the active Work Item and refuses.
        created = self.create_lifecycle_work_item(root, "WI-002", "HD-103")
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        before = self.snapshot_repository(root)
        refused = self.start_command(root, "WI-002")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("SINGLE_ACTIVE_WORK_ITEM", refused.stdout + refused.stderr)
        self.assertEqual(self.snapshot_repository(root), before)
        # An administrative change on the Work Item branch is refused by preflight and by the hook.
        switched = run_git(root, "switch", branch)
        self.assertEqual(switched.returncode, 0, switched.stdout + switched.stderr)
        self.install_commit_hook(root)
        roadmap = root / "docs/governance/ROADMAP.md"
        roadmap.write_text(roadmap.read_text(encoding="utf-8") + "\n<!-- edited on the work branch -->\n", encoding="utf-8")
        preflight = run_control(root, "preflight", "WI-001")
        self.assertNotEqual(preflight.returncode, 0)
        self.assertIn("FAIL: WORK_BRANCH_RECORDS_READ_ONLY", preflight.stdout)
        staged = run_git(root, "add", "--", "docs/governance/ROADMAP.md")
        self.assertEqual(staged.returncode, 0, staged.stdout + staged.stderr)
        head_before = run_git(root, "rev-parse", "HEAD").stdout
        committed = run_git(root, "commit", "-q", "-m", "records on the work branch")
        self.assertNotEqual(committed.returncode, 0)
        self.assertIn("WORK_BRANCH_RECORDS_READ_ONLY", committed.stdout + committed.stderr)
        self.assertEqual(run_git(root, "rev-parse", "HEAD").stdout, head_before)

    def test_start_rolls_back_its_records_commit_when_the_branch_preflight_fails(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        created = self.create_lifecycle_work_item(root, "WI-001", "HD-102")
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        item = load_json(root / "project_control/work-items/WI-001.json")
        canonical_tip = run_git(root, "rev-parse", "HEAD").stdout.strip()
        control = self.control_module.ProjectControl(root)
        real_preflight = control.preflight_findings

        def failing_branch_preflight(work_item_id, planned_paths=(), start_head_override=None, expected_branch=None):
            findings = real_preflight(work_item_id, planned_paths, start_head_override, expected_branch)
            if expected_branch is None:
                self.control_module.add(findings, "INJECTED_BRANCH_FAILURE", False, "injected after the records commit")
            return findings

        control.preflight_findings = failing_branch_preflight
        digest = control.work_item_manifest(item)["manifest_digest"]
        with self.assertRaisesRegex(self.control_module.ProjectControlError, "INJECTED_BRANCH_FAILURE"):
            control.start_work_item("WI-001", [], "FixtureAgent", digest)
        self.assertEqual(run_git(root, "branch", "--show-current").stdout.strip(), "main")
        self.assertEqual(run_git(root, "rev-parse", "main").stdout.strip(), canonical_tip)
        self.assertNotEqual(run_git(root, "show-ref", "--verify", "--quiet", f"refs/heads/{item['branch']}").returncode, 0)
        self.assertEqual(run_git(root, "status", "--porcelain=v1", "--untracked-files=all").stdout, "")
        self.assertEqual(load_json(root / "project_control/work-items/WI-001.json")["status"], "AUTHORIZED")
        self.assertFalse((root / "project_control/agent-runs/RUN-WI-001-001.json").exists())
        audit = run_control(root, "audit")
        self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)

    def test_runtime_target_requires_runtime_proof_but_deployment_stays_separate(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        for label, target, deployment, runtime_proof in (
            ("deployment without runtime proof", "PRODUCTION", "APPLICABLE", "NOT_APPLICABLE"),
            ("deployment without runtime target", "NOT_APPLICABLE", "APPLICABLE", "NOT_APPLICABLE"),
            ("runtime proof without runtime target", "NOT_APPLICABLE", "NOT_APPLICABLE", "APPLICABLE"),
        ):
            with self.subTest(label=label):
                before = self.lifecycle_snapshot(root)
                refused = self.create_lifecycle_work_item(
                    root, "WI-001", "HD-102", target, deployment=deployment, runtime_proof=runtime_proof,
                )
                self.assertNotEqual(refused.returncode, 0)
                self.assertEqual(self.lifecycle_snapshot(root), before)
        created = self.create_lifecycle_work_item(
            root, "WI-001", "HD-102", "PRODUCTION", deployment="NOT_APPLICABLE", runtime_proof="APPLICABLE",
        )
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        started = self.start_command(root, "WI-001")
        self.assertEqual(started.returncode, 0, started.stdout + started.stderr)
        branch = run_git(root, "branch", "--show-current").stdout.strip()
        (root / "reports/WI-001.txt").write_text("proof campaign notes\n", encoding="utf-8")
        self.commit_fixture(root, "fixture: proof campaign")
        self.merge_fixture_branch(root, branch, "fixture: integrate proof campaign")
        evidence = self.write_committed_evidence(root, "WI-001")
        self.assertNotIn("deployment", evidence)
        self.assertIn("runtime_proof", evidence)
        closed = self.close_with_evidence(root, "WI-001", evidence)
        self.assertEqual(closed.returncode, 0, closed.stdout + closed.stderr)
        item = load_json(root / "project_control/work-items/WI-001.json")
        self.assertEqual(item["status"], "DONE")
        self.assertEqual(item["deployment_status"], "NOT_APPLICABLE")
        self.assertEqual(item["runtime_proof_status"], "PRODUCTION_VERIFIED")
        audit = run_control(root, "audit")
        self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)

    def test_create_work_item_authorizes_its_evidence_directory(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        created = run_control(
            root, "create-work-item", "WI-001", "--title", "Change without explicit evidence path",
            "--objective", "Prove that evidence preparation never fails the preflight.",
            "--owner", "Project Owner", "--human-decision", "HD-102", "--decision", "Authorize WI-001.",
            "--authorized-by", "Project Owner", "--path", "reports/WI-001.txt",
            "--conflict-gate", "INDEPENDENT", "--direct-impact", "reports/WI-001.txt",
            "--indirect-impact", "none", "--authority-impact", "NONE", "--concurrent-work-impact", "NONE",
            "--code", "NOT_APPLICABLE", "--tests", "APPLICABLE", "--integration", "APPLICABLE",
            "--deployment", "NOT_APPLICABLE", "--runtime-proof", "NOT_APPLICABLE",
            "--runtime-target", "NOT_APPLICABLE", "--close-condition", "Tests and integration pass.",
        )
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        item = load_json(root / "project_control/work-items/WI-001.json")
        self.assertEqual(item["authorized_paths"], ["reports/WI-001.txt", "reports/evidence/WI-001"])
        started = self.start_command(root, "WI-001")
        self.assertEqual(started.returncode, 0, started.stdout + started.stderr)
        draft_directory = root / "reports/evidence/WI-001"
        draft_directory.mkdir(parents=True)
        (draft_directory / "tests-draft.txt").write_text("draft evidence\n", encoding="utf-8")
        staged = run_git(root, "add", "--", "reports/evidence/WI-001/tests-draft.txt")
        self.assertEqual(staged.returncode, 0, staged.stdout + staged.stderr)
        preflight = run_control(root, "preflight", "WI-001")
        self.assertEqual(preflight.returncode, 0, preflight.stdout + preflight.stderr)
        self.assertIn("PASS: AUTHORIZED_PATHS", preflight.stdout)

    BASELINE_DECISION_TEXTS = {
        "legacy_baseline": (
            "Legacy baseline commit",
            "Adopt the current Project Control contract on the existing history at {head}.",
            "Controller upgrade on a project with prior Work Items.",
            "Historical closures are preserved as recorded, never reconstructed.",
            "all Work Items recorded at the baseline",
        ),
        "authorities_baseline": (
            "Authorities baseline commit",
            "Adopt the proof of reading of authorities on the Agent Runs recorded at {head}.",
            "Controller upgrade to a version that records authorities_read on Agent Runs.",
            "A closed Agent Run cannot receive a proof of reading; it stays as recorded.",
            "all Agent Runs recorded at the baseline",
        ),
    }

    def record_baseline_decision(
        self, root: Path, kind: str, head: str, decision_id: str, *, names: bool = True,
    ) -> None:
        """Record the decision that freezes history at `head` — naming the commit, as a
        declaration requires, unless the test wants a decision that does not."""
        field, decision, context, reason, scope = self.BASELINE_DECISION_TEXTS[kind]
        decisions_path = root / "docs/governance/HUMAN_DECISIONS.md"
        decisions_path.write_text(
            decisions_path.read_text(encoding="utf-8").rstrip() + "\n"
            f"\n## {decision_id}\n\n"
            f"Date: {self.control_module.today_iso()}\n"
            f"Decision: {decision.format(head=head)}\n"
            + (f"{field}: {head}\n" if names else "")
            + f"Context: {context}\n"
            "Options considered: FREEZE_HISTORY | RECONSTRUCT_HISTORY\n"
            "Chosen option: FREEZE_HISTORY\n"
            f"Reason: {reason}\n"
            f"Scope: {scope}\n"
            "Reversible: NO\n"
            "Conversation reference: CONV-101\n"
            "Related ADR: NOT_APPLICABLE\n"
            "Related Work Item: NOT_APPLICABLE\n"
            "Authorized by: Project Owner\n",
            encoding="utf-8",
        )

    def declare_baseline(self, root: Path, kind: str, head: str, decision_id: str) -> str:
        """Record the decision and declare the frozen history of `kind` in project-state."""
        self.record_baseline_decision(root, kind, head, decision_id)
        state_path = root / "project_control/project-state.v1.json"
        state = load_json(state_path)
        state[kind] = {"head": head, "human_decision_ref": decision_id}
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        label = kind.replace("_", " ")
        return self.commit_fixture(root, f"chore: declare {label} {head[:12]} ({decision_id})")

    def declare_legacy_baseline(self, root: Path, head: str, decision_id: str) -> str:
        """Record the adoption decision and declare the frozen history in project-state."""
        return self.declare_baseline(root, "legacy_baseline", head, decision_id)

    def rewrite_chosen_option(self, root: Path, decision_id: str, value: str) -> None:
        """Give a recorded decision the vocabulary of its own time, in its `Chosen option` field."""
        path = root / "docs/governance/HUMAN_DECISIONS.md"
        text = path.read_text(encoding="utf-8")
        block = recorded_decision_block(text, decision_id)
        self.assertIsNotNone(block, f"{decision_id} is recorded")
        rewritten = re.sub(r"(?m)^Chosen option:.*$", f"Chosen option: {value}", block)
        path.write_text(text.replace(block, rewritten), encoding="utf-8")

    def declare_authorities_baseline(self, root: Path, head: str, decision_id: str) -> str:
        """Record the decision that adopts the proof of reading on existing Agent Runs and declare it."""
        return self.declare_baseline(root, "authorities_baseline", head, decision_id)

    def add_decision_line(self, root: Path, decision_id: str, line: str) -> None:
        """Give a recorded decision one more field, as a human would when writing it."""
        path = root / "docs/governance/HUMAN_DECISIONS.md"
        text = path.read_text(encoding="utf-8")
        block = recorded_decision_block(text, decision_id)
        self.assertIsNotNone(block, f"{decision_id} is recorded")
        amended = block.replace("\nAuthorized by:", f"\n{line}\nAuthorized by:", 1)
        self.assertNotEqual(amended, block)
        path.write_text(text.replace(block, amended), encoding="utf-8")

    def test_a_baseline_leaves_only_on_a_decision_that_names_the_removal(self) -> None:
        """Step 2 of the scenario the third control executed: a Work Item legitimately authorised
        to write the project state sets the adoption baseline to null and commits — an ordinary
        write in an authorised file, after which nothing protects the closures behind the line.
        The gate refuses that commit now, with a real `git commit`, unless a decision of the
        active Work Item, committed on the canonical branch, names the removal and the commit."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        frozen = run_git(root, "rev-parse", "HEAD").stdout.strip()
        self.declare_legacy_baseline(root, frozen, "HD-105")
        self.install_commit_hook(root)
        item = self.create_and_start_lifecycle_work_item(
            root, "WI-001", "HD-102", authorized_path="project_control/project-state.v1.json", code="APPLICABLE",
        )
        state_path = root / "project_control/project-state.v1.json"
        state = load_json(state_path)
        state["legacy_baseline"] = None
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        staged = run_git(root, "add", "--", "project_control/project-state.v1.json")
        self.assertEqual(staged.returncode, 0, staged.stdout + staged.stderr)
        before = run_git(root, "rev-parse", "HEAD").stdout.strip()
        refused = run_git(root, "commit", "-q", "-m", "chore: drop the adoption baseline")
        self.assertNotEqual(refused.returncode, 0, "the commit that un-freezes history must be refused")
        output = refused.stdout + refused.stderr
        self.assertIn("FAIL: BASELINE_CHANGE_MANDATED", output)
        self.assertIn(f"`Legacy baseline removed: {frozen}`", output)
        self.assertEqual(run_git(root, "rev-parse", "HEAD").stdout.strip(), before, "HEAD did not move")
        # The same removal, once the Work Item's decision names it — recorded on the canonical
        # branch and brought into the branch, since a decision on disk mandates nothing.
        restored = run_git(root, "restore", "--source=HEAD", "--staged", "--worktree", "--",
                           "project_control/project-state.v1.json")
        self.assertEqual(restored.returncode, 0, restored.stdout + restored.stderr)
        self.switch_to_canonical(root)
        self.add_decision_line(root, "HD-102", f"Legacy baseline removed: {frozen}")
        self.commit_fixture(root, "chore: HD-102 names the baseline it removes")
        checkout = run_git(root, "switch", item["branch"])
        self.assertEqual(checkout.returncode, 0, checkout.stdout + checkout.stderr)
        aligned = run_git(root, "merge", "--ff-only", "main")
        self.assertEqual(aligned.returncode, 0, aligned.stdout + aligned.stderr)
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        run_git(root, "add", "--", "project_control/project-state.v1.json")
        accepted = run_git(root, "commit", "-q", "-m", "chore: drop the adoption baseline (HD-102)")
        self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)
        self.assertIn(f"legacy baseline {frozen} removed on HD-102", accepted.stdout + accepted.stderr)

    def test_a_baseline_never_recedes(self) -> None:
        """The line of the past advances; it never moves back or sideways. A Work Item that moves
        the adoption baseline to a commit that does not descend from the current one is refused
        by the gate, even with a decision naming that commit; moved forward, on a decision that
        names the new commit, it passes."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        first = run_git(root, "rev-parse", "HEAD").stdout.strip()
        (root / "reports/notes.md").write_text("later\n", encoding="utf-8")
        later = self.commit_fixture(root, "docs: later")
        self.declare_legacy_baseline(root, later, "HD-105")
        (root / "reports/notes.md").write_text("even later\n", encoding="utf-8")
        even_later = self.commit_fixture(root, "docs: even later")
        self.record_baseline_decision(root, "legacy_baseline", first, "HD-106")
        self.record_baseline_decision(root, "legacy_baseline", even_later, "HD-107")
        self.commit_fixture(root, "chore: two decisions, one for each direction")
        self.install_commit_hook(root)
        self.create_and_start_lifecycle_work_item(
            root, "WI-001", "HD-102", authorized_path="project_control/project-state.v1.json", code="APPLICABLE",
        )
        state_path = root / "project_control/project-state.v1.json"
        state = load_json(state_path)
        state["legacy_baseline"] = {"head": first, "human_decision_ref": "HD-106"}
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        run_git(root, "add", "--", "project_control/project-state.v1.json")
        refused = run_git(root, "commit", "-q", "-m", "chore: move the baseline back")
        self.assertNotEqual(refused.returncode, 0, "a baseline moved backwards must be refused")
        output = refused.stdout + refused.stderr
        self.assertIn("FAIL: BASELINE_CHANGE_MANDATED", output)
        self.assertIn("a baseline never recedes", output)
        state["legacy_baseline"] = {"head": even_later, "human_decision_ref": "HD-107"}
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        run_git(root, "add", "--", "project_control/project-state.v1.json")
        accepted = run_git(root, "commit", "-q", "-m", "chore: move the baseline forward (HD-107)")
        self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)
        self.assertIn(f"legacy baseline moves from {later} to {even_later}", accepted.stdout + accepted.stderr)

    def test_the_frozen_history_can_no_longer_be_defrozen_through_the_governed_path(self) -> None:
        """The scenario of the third independent control, replayed as it was executed — no
        override, no edit of the controller, no rewrite of Git history: (1) a Work Item authorised
        on the project state, (2) the baseline set to null and committed, (3) a frozen closure
        modified on the canonical branch, (4) the baseline re-declared on the rewritten commit with
        the same old decision. Every step passed. It stops at step 2 now — a real `git commit`,
        refused — and the line, left in place, keeps protecting the closure behind it."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        done = self.create_start_and_close_lifecycle_work_item(root, "WI-001", "HD-102")
        self.assertEqual(done["status"], "DONE")
        frozen = run_git(root, "rev-parse", "HEAD").stdout.strip()
        self.declare_legacy_baseline(root, frozen, "HD-105")
        self.install_commit_hook(root)
        # (1) A Work Item legitimately authorised to write the project state.
        item = self.create_and_start_lifecycle_work_item(
            root, "WI-002", "HD-103", authorized_path="project_control/project-state.v1.json", code="APPLICABLE",
        )
        # (2) The baseline set to null: the ordinary write that used to open everything.
        state_path = root / "project_control/project-state.v1.json"
        state = load_json(state_path)
        state["legacy_baseline"] = None
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        run_git(root, "add", "--", "project_control/project-state.v1.json")
        head_before = run_git(root, "rev-parse", "HEAD").stdout.strip()
        refused = run_git(root, "commit", "-q", "-m", "chore: open the past")
        self.assertNotEqual(refused.returncode, 0, "step 2 must be refused")
        self.assertIn("FAIL: BASELINE_CHANGE_MANDATED", refused.stdout + refused.stderr)
        self.assertEqual(run_git(root, "rev-parse", "HEAD").stdout.strip(), head_before)
        restored = run_git(root, "restore", "--source=HEAD", "--staged", "--worktree", "--",
                           "project_control/project-state.v1.json")
        self.assertEqual(restored.returncode, 0, restored.stdout + restored.stderr)
        # (3) With the line in place, the frozen closure cannot be touched: the audit refuses it.
        self.switch_to_canonical(root)
        record_path = root / "project_control/work-items/WI-001.json"
        record = load_json(record_path)
        record["objective"] = "A rewritten past."
        record_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        audit = run_control(root, "audit")
        self.assertNotEqual(audit.returncode, 0)
        self.assertIn("WI-001: legacy DONE record changed; historical bytes must be preserved", audit.stdout)
        restored = run_git(root, "restore", "--source=HEAD", "--worktree", "--", "project_control/work-items/WI-001.json")
        self.assertEqual(restored.returncode, 0, restored.stdout + restored.stderr)
        # (4) And the old decision cannot re-declare the line elsewhere.
        (root / "reports/notes.md").write_text("later\n", encoding="utf-8")
        later = self.commit_fixture(root, "reports: later")
        state = load_json(state_path)
        state["legacy_baseline"] = {"head": later, "human_decision_ref": "HD-105"}
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        audit = run_control(root, "audit")
        self.assertNotEqual(audit.returncode, 0)
        self.assertIn(f"legacy baseline {later} is not named by its Human Decision HD-105", audit.stdout)
        self.assertIn(item["work_item_id"], "WI-002")

    def prepare_an_edited_integration_merge(self, root: Path) -> tuple[str, str, dict]:
        """A frozen closure, a declared baseline, and a Work Item branch that legitimately touched
        the project state; then an integration merge left open before its commit, ready to be
        edited — the recipe of the fourth independent control (F12-01). Returns the frozen commit,
        the fixture's first commit and the project state as the branch produced it."""
        first = run_git(root, "rev-parse", "HEAD").stdout.strip()
        done = self.create_start_and_close_lifecycle_work_item(root, "WI-001", "HD-102")
        self.assertEqual(done["status"], "DONE")
        frozen = run_git(root, "rev-parse", "HEAD").stdout.strip()
        self.declare_legacy_baseline(root, frozen, "HD-105")
        self.install_commit_hook(root)
        item = self.create_and_start_lifecycle_work_item(
            root, "WI-002", "HD-103", authorized_path="project_control/project-state.v1.json", code="APPLICABLE",
        )
        state_path = root / "project_control/project-state.v1.json"
        state = load_json(state_path)
        state["language"] = "EN"
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        run_git(root, "add", "--", "project_control/project-state.v1.json")
        committed = run_git(root, "commit", "-q", "-m", "chore: the language, legitimately")
        self.assertEqual(committed.returncode, 0, committed.stdout + committed.stderr)
        self.switch_to_canonical(root)
        opened = run_git(root, "merge", "--no-ff", "--no-commit", item["branch"])
        self.assertEqual(opened.returncode, 0, opened.stdout + opened.stderr)
        self.assertTrue((root / ".git/MERGE_HEAD").exists(), "the merge is open, its commit not made")
        return frozen, first, state

    def commit_the_edited_merge(self, root: Path, state: dict) -> subprocess.CompletedProcess[str]:
        state_path = root / "project_control/project-state.v1.json"
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        staged = run_git(root, "add", "--", "project_control/project-state.v1.json")
        self.assertEqual(staged.returncode, 0, staged.stdout + staged.stderr)
        return run_git(root, "-c", "user.name=Fixture Owner", "-c", "user.email=fixture@example.invalid",
                       "commit", "-q", "-m", "merge: integrate WI-002")

    def test_a_baseline_cannot_be_removed_by_editing_an_integration_merge(self) -> None:
        """The fourth independent control removed the baseline where the gate did not look: a
        Work Item legitimately touched the project state, and the merge that integrated it into
        the canonical branch was edited before its commit — the baseline set to null on the way.
        The integration check only refused *new paths*; a path the branch touched could carry
        any content. A frozen closure was then rewritten, audit green. Refused now, twice over:
        the merge result must be the branch's, and a baseline leaves only on a decision, merge
        or not. The same merge, unedited, still integrates."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        frozen, _, state = self.prepare_an_edited_integration_merge(root)
        head_before = run_git(root, "rev-parse", "HEAD").stdout.strip()
        edited = dict(state, legacy_baseline=None)
        refused = self.commit_the_edited_merge(root, edited)
        self.assertNotEqual(refused.returncode, 0, "an edited integration merge must be refused")
        output = refused.stdout + refused.stderr
        self.assertIn("FAIL: BASELINE_CHANGE_MANDATED", output)
        self.assertIn(f"`Legacy baseline removed: {frozen}`", output)
        self.assertIn("the merge result differs from the branch for: ['project_control/project-state.v1.json']", output)
        self.assertEqual(run_git(root, "rev-parse", "HEAD").stdout.strip(), head_before, "HEAD did not move")
        # Unedited, the same integration passes: the merge carries exactly what the branch produced.
        accepted = self.commit_the_edited_merge(root, state)
        self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)
        self.assertEqual(load_json(root / "project_control/project-state.v1.json")["legacy_baseline"]["head"], frozen)
        audit = run_control(root, "audit")
        self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)
        self.assertIn(f"legacy Work Item(s) frozen at {frozen}", audit.stdout)

    def test_a_baseline_cannot_recede_through_an_integration_merge(self) -> None:
        """The same open merge, edited to move the baseline back to an ancestor: refused, with the
        reason the gate gives on a Work Item branch — a baseline never recedes."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        first = run_git(root, "rev-parse", "HEAD").stdout.strip()
        self.record_baseline_decision(root, "legacy_baseline", first, "HD-106")
        self.commit_fixture(root, "chore: a decision naming the first commit, recorded ahead")
        _, _, state = self.prepare_an_edited_integration_merge(root)
        head_before = run_git(root, "rev-parse", "HEAD").stdout.strip()
        receded = dict(state, legacy_baseline={"head": first, "human_decision_ref": "HD-106"})
        refused = self.commit_the_edited_merge(root, receded)
        self.assertNotEqual(refused.returncode, 0, "a baseline moved back through a merge must be refused")
        output = refused.stdout + refused.stderr
        self.assertIn("FAIL: BASELINE_CHANGE_MANDATED", output)
        self.assertIn("a baseline never recedes", output)
        self.assertEqual(run_git(root, "rev-parse", "HEAD").stdout.strip(), head_before)

    def test_an_interruption_leaves_no_temporary_file_behind(self) -> None:
        """A transaction writes each file through a temporary next to its target, then renames it.
        Interrupted between the two — a keyboard interrupt is not an Exception — the temporary
        stayed: unexplained for the traceability audit, refusing the next transition until
        someone found it (fourth independent control, F14-01). The interruption still
        propagates; the temporary does not survive it."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        module = self.control_module
        transaction = module.FileTransaction(root)
        target = root / "docs/governance/HUMAN_DECISIONS.md"
        before = target.read_bytes()
        with unittest.mock.patch.object(module.os, "replace", side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                transaction.write_bytes("docs/governance/HUMAN_DECISIONS.md", before + b"\n## HD-900\n")
        leftovers = sorted(p.name for p in target.parent.iterdir() if p.name.startswith(".HUMAN_DECISIONS.md."))
        self.assertEqual(leftovers, [], "the temporary file must not survive the interruption")
        self.assertEqual(target.read_bytes(), before, "the target is untouched")
        status = run_git(root, "status", "--porcelain", "--untracked-files=all")
        self.assertEqual(status.stdout.strip(), "", status.stdout)

    def test_a_fixture_copy_carries_nothing_the_template_ignores(self) -> None:
        """A fixture is made of what the template holds, not of what sits next to it: the
        download folder an application drops in the working folder, a generated view. Copied
        along, they made two tests depend on their content — a half-written JSON file there,
        and a fixture failed its JSON audit (fourth independent control). After the copy, Git
        finds nothing ignored in it."""
        temporary, root = self.make_copy()
        self.addCleanup(temporary.cleanup)
        listed = run_git(root, "ls-files", "--others", "--ignored", "--exclude-standard")
        self.assertEqual(listed.returncode, 0, listed.stdout + listed.stderr)
        self.assertEqual(listed.stdout.strip(), "", f"ignored entries travelled into the fixture: {listed.stdout}")

    def test_a_rejected_decision_declares_no_baseline(self) -> None:
        """A decision whose chosen option is REJECT carries the anchor field like any other; it
        used to declare a baseline all the same. A refusal declares nothing."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        head = run_git(root, "rev-parse", "HEAD").stdout.strip()
        self.declare_legacy_baseline(root, head, "HD-105")
        self.rewrite_chosen_option(root, "HD-105", "REJECT")
        refused = run_control(root, "audit")
        self.assertNotEqual(refused.returncode, 0, "a rejected decision must not declare a baseline")
        self.assertIn(f"legacy baseline {head} cites HD-105, a rejected decision: a refusal declares nothing", refused.stdout)
        self.rewrite_chosen_option(root, "HD-105", "FREEZE_HISTORY")
        accepted = run_control(root, "audit")
        self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)

    def test_a_decision_that_chooses_twice_declares_no_baseline(self) -> None:
        """`Chosen option: REJECT` written twice in the decision a baseline cites: the field,
        read as one value, was None — which is not REJECT — and the refusal passed for a choice;
        the baseline moved to the commit that twice-rejected decision named, through audit,
        commit and merge (fifth independent control, F-05). A decision chooses once: two lines,
        REJECT or not, declare nothing."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        head = run_git(root, "rev-parse", "HEAD").stdout.strip()
        self.declare_legacy_baseline(root, head, "HD-105")
        self.rewrite_chosen_option(root, "HD-105", "REJECT")
        self.add_decision_line(root, "HD-105", "Chosen option: REJECT")
        refused = run_control(root, "audit")
        self.assertNotEqual(refused.returncode, 0, "a decision that rejects twice must not declare a baseline")
        self.assertIn(
            f"legacy baseline {head} cites HD-105, whose `Chosen option` is written 2 times (REJECT, REJECT): "
            "a decision chooses once, and this one declares nothing", refused.stdout,
        )
        # Twice the right vocabulary is not a choice either.
        self.rewrite_chosen_option(root, "HD-105", "FREEZE_HISTORY")
        refused = run_control(root, "audit")
        self.assertNotEqual(refused.returncode, 0, "two identical choices are still two lines")
        self.assertIn("written 2 times (FREEZE_HISTORY, FREEZE_HISTORY)", refused.stdout)
        # One line, the decision's own vocabulary: the declaration stands.
        path = root / "docs/governance/HUMAN_DECISIONS.md"
        text = path.read_text(encoding="utf-8")
        block = recorded_decision_block(text, "HD-105")
        single = block.replace("\nChosen option: FREEZE_HISTORY\nAuthorized by:", "\nAuthorized by:", 1)
        self.assertNotEqual(single, block)
        path.write_text(text.replace(block, single), encoding="utf-8")
        accepted = run_control(root, "audit")
        self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)

    def test_the_gate_never_touches_a_worktree_that_is_not_its_own(self) -> None:
        """The sweep of 3.18.2 recognised the controller's throwaway checkouts by the name of
        their folder and their age. The fifth independent control gave a review worktree a
        folder with that name, an uncommitted note inside it and another beside it, aged the
        checkout, and committed a report: the worktree and the whole folder were gone, both
        notes with them (F-01). A name is not ownership. The same fixture, the same commit:
        nothing of it is touched."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        self.install_commit_hook(root)
        head = run_git(root, "rev-parse", "HEAD").stdout.strip()
        holder = Path(tempfile.mkdtemp(prefix="project-control-upgrade-review-"))
        self.addCleanup(lambda: shutil.rmtree(holder, ignore_errors=True))
        review = holder / "human-review"
        added = run_git(root, "worktree", "add", "--quiet", "-b", "human-review", str(review), head)
        self.assertEqual(added.returncode, 0, added.stdout + added.stderr)
        self.addCleanup(lambda: run_git(root, "worktree", "remove", "--force", str(review)))
        (review / "uncommitted-review.txt").write_text("not committed\n", encoding="utf-8")
        (holder / "meeting-notes.txt").write_text("notes beside the checkout\n", encoding="utf-8")
        old_age = time.time() - 2 * 3600
        os.utime(review, (old_age, old_age))
        (root / "reports/notes.md").write_text("a report\n", encoding="utf-8")
        run_git(root, "add", "--", "reports/notes.md")
        committed = run_git(root, "-c", "user.name=Fixture Owner", "-c", "user.email=fixture@example.invalid",
                            "commit", "-q", "-m", "reports: a note")
        self.assertEqual(committed.returncode, 0, committed.stdout + committed.stderr)
        remaining = run_git(root, "worktree", "list", "--porcelain").stdout
        self.assertIn(str(review), remaining, "a worktree that is not the controller's is never touched")
        self.assertEqual((review / "uncommitted-review.txt").read_text(encoding="utf-8"), "not committed\n")
        self.assertEqual((holder / "meeting-notes.txt").read_text(encoding="utf-8"), "notes beside the checkout\n")
        self.assertEqual(run_git(root, "rev-parse", "--verify", "--quiet", "refs/heads/human-review").returncode, 0)

    def test_the_gate_removes_its_own_dead_throwaway_checkouts_and_leaves_a_running_one(self) -> None:
        """The gate and the upgrade rehearsal each make a throwaway checkout and remove it when
        they end. A command killed in flight — a close cut short by a tool's time limit, in a
        real project — leaves one behind, registered in the worktree list until someone notices.
        The controller sweeps its own at the next gate, and what is its own is proved, not
        guessed: a marker it writes when it makes the holder, and keeps locked while it runs. A
        marked checkout whose lock is free belongs to a dead command and goes, with its marker
        and its holder, which held nothing else. A marked checkout still locked stays, however
        old: the fifth independent control suspended a rehearsal, aged its checkout, and a
        second command removed it from under the first (F-01) — age proves nothing about a
        command that is merely slow."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        self.install_commit_hook(root)
        head = run_git(root, "rev-parse", "HEAD").stdout.strip()
        control = self.control_module.ProjectControl(root)

        def linked_worktree(checkout: Path) -> None:
            added = run_git(root, "worktree", "add", "--quiet", "--detach", str(checkout), head)
            self.assertEqual(added.returncode, 0, added.stdout + added.stderr)
            self.addCleanup(lambda: run_git(root, "worktree", "remove", "--force", str(checkout)))

        # A command that died: the marker is there, its lock went with the process.
        dead, dead_claim = control.open_throwaway("project-control-staged-", "staged")
        self.addCleanup(lambda: shutil.rmtree(dead.parent, ignore_errors=True))
        linked_worktree(dead)
        dead_claim.close()
        # A command still running, its checkout older than any limit: the lock is held.
        live, live_claim = control.open_throwaway("project-control-upgrade-", "rehearsal")
        self.addCleanup(lambda: shutil.rmtree(live.parent, ignore_errors=True))
        self.addCleanup(live_claim.close)
        linked_worktree(live)
        old_age = time.time() - 2 * 3600
        os.utime(live, (old_age, old_age))
        (root / "reports/notes.md").write_text("a report\n", encoding="utf-8")
        run_git(root, "add", "--", "reports/notes.md")
        committed = run_git(root, "-c", "user.name=Fixture Owner", "-c", "user.email=fixture@example.invalid",
                            "commit", "-q", "-m", "reports: a note")
        self.assertEqual(committed.returncode, 0, committed.stdout + committed.stderr)
        remaining = run_git(root, "worktree", "list", "--porcelain").stdout
        self.assertNotIn(str(dead), remaining, "the dead command's checkout is removed")
        self.assertFalse(dead.parent.exists(), "with its marker and its holder, which held nothing else")
        self.assertIn(str(live), remaining, "a checkout whose command still runs stays, whatever its age")
        self.assertTrue(live.exists())
        self.assertTrue((live.parent / self.control_module.THROWAWAY_MARKER_NAME).is_file(), "its marker with it")

    def test_a_json_file_the_project_ignores_does_not_fail_its_json_check(self) -> None:
        """The JSON check read every `*.json` under the tree, `.git` excepted: a half-written
        download an application dropped in an ignored folder failed it, and removing that one
        ignored file made it pass (fifth independent control, F-06 — the debt the fourth pass had
        found, settled for the fixture copies and not for this check). What the project holds is
        what Git sees, ignored files excepted; the check reads those and nothing else."""
        temporary, root = self.make_copy()
        self.addCleanup(temporary.cleanup)
        ignored = root / "Claude outputs/incomplete-download.json"
        ignored.parent.mkdir(parents=True, exist_ok=True)
        ignored.write_bytes(b'{"download":')
        checked = run_git(root, "check-ignore", "--quiet", "--", "Claude outputs/incomplete-download.json")
        self.assertEqual(checked.returncode, 0, "the fixture's file is one the project ignores")
        self.assertEqual(run_git(root, "status", "--porcelain").stdout.strip(), "", "and Git reports nothing")
        checked = subprocess.run(
            [sys.executable, "-B", "-m", "unittest", "-q",
             "tests.test_template.GeneralProjectSkeletonTests.test_all_json_and_schema_documents_parse"],
            cwd=root, capture_output=True, text=True, check=False,
        )
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        self.assertNotIn("JSONDecodeError", checked.stdout + checked.stderr)

    def test_the_published_copy_carries_nothing_private_and_leaves_the_core_untouched(self) -> None:
        """The public repository is a mirror produced by a script from the private one, never
        edited by hand: the tracked tree at a revision, with the owner's machine paths, his
        e-mail address, the name of the project adopted with its history and the backup
        repository replaced — and nothing else. The copy must carry none of them, in contents
        or in file names; the core must be byte-identical to what the revision holds, since the
        code is published as it is or not at all; and an anonymised report says it is one."""
        self.skip_unless_template("the publication export works on the template's own provenance")
        script = ROOT / "provenance/maintenance/publication/export_public.py"
        if not script.is_file():
            # The public mirror is a template too, and does not carry the tool that made it.
            self.skipTest("the publication export stays in the private template")
        spec = importlib.util.spec_from_file_location("export_public_under_test", script)
        publication = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(publication)
        # What must not survive is read from the script, never written here: this file is core,
        # and a test that spelled the forbidden strings out was itself what the export refused
        # to publish. The suite of 3.19.0 did not see it — the export reads a committed
        # revision, and the test file that named them was committed after the suite ran. So the
        # working tree is read first: no core file may carry what the export would rewrite.
        core = load_json(ROOT / "provenance/core-manifest.v1.json")["core"]
        for relative in core:
            text = (ROOT / relative).read_text(encoding="utf-8")
            for pattern, replacement in publication.REPLACEMENTS:
                self.assertEqual(re.subn(pattern, replacement, text)[1], 0,
                                 f"{relative} carries what the export would rewrite ({pattern}): it could not be published")
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        target = Path(temporary.name) / "public"
        exported = subprocess.run([sys.executable, "-B", str(script), "HEAD", str(target)],
                                  cwd=ROOT, capture_output=True, text=True, check=False)
        self.assertEqual(exported.returncode, 0, exported.stdout + exported.stderr)
        self.assertIn("EXPORTED HEAD", exported.stdout)
        forbidden = tuple(publication.FORBIDDEN)
        acronym = re.compile(r"\b(" + "|".join(re.escape(word) for word in publication.FORBIDDEN_WORDS) + r")\b")
        self.assertGreaterEqual(len(forbidden) + len(publication.FORBIDDEN_WORDS), 8, "the script still says what must not survive")
        for path in sorted(p for p in target.rglob("*") if p.is_file()):
            relative = path.relative_to(target).as_posix()
            data = path.read_bytes()
            for needle in forbidden:
                self.assertNotIn(needle.encode("utf-8"), data, f"{needle} survives in {relative}")
                self.assertNotIn(needle, relative)
            self.assertIsNone(acronym.search(data.decode("utf-8", "ignore")), f"the acronym survives in {relative}")
            self.assertIsNone(acronym.search(relative), f"the acronym survives in the name {relative}")
        self.assertFalse((target / "provenance/maintenance/publication").exists(),
                         "the export tool names what the copy must not carry: it stays private")
        manifest = load_json(target / "provenance/core-manifest.v1.json")
        for relative in list(manifest["core"]) + ["provenance/core-manifest.v1.json"]:
            at_head = run_git(ROOT, "show", f"HEAD:{relative}")
            self.assertEqual(at_head.returncode, 0, relative)
            self.assertEqual((target / relative).read_text(encoding="utf-8"), at_head.stdout, f"core file changed by the export: {relative}")
        report = target / "provenance/maintenance/2026-09-11-controle-independant-3.18.0.md"
        self.assertTrue(report.read_text(encoding="utf-8").startswith("> *Copie anonymisée pour la publication"))
        self.assertIn("Jeoffrey", (target / "LICENSE").read_text(encoding="utf-8"), "the licence keeps its author")
        self.assertIn("d'Alpha", (target / "provenance/CHANGELOG.md").read_text(encoding="utf-8"), "the prose still reads")

    def test_a_decision_that_declared_one_baseline_cannot_declare_another(self) -> None:
        """Step 4 of the scenario the third independent control executed: a baseline is declared
        again on a later commit, citing the decision that declared the previous line. The
        controller checked that the commit exists and that a structured decision accompanies
        the declaration — never that *that* decision speaks of *that* commit. It does now: a
        declaration is anchored to the decision that names it, field by kind."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        first = run_git(root, "rev-parse", "HEAD").stdout.strip()
        self.declare_legacy_baseline(root, first, "HD-105")
        accepted = run_control(root, "audit")
        self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)
        (root / "docs/notes.md").write_text("a later commit the old decision never spoke of\n", encoding="utf-8")
        later = self.commit_fixture(root, "docs: a later commit")
        state_path = root / "project_control/project-state.v1.json"
        state = load_json(state_path)
        state["legacy_baseline"] = {"head": later, "human_decision_ref": "HD-105"}
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        refused = run_control(root, "audit")
        self.assertNotEqual(refused.returncode, 0, "the old decision must not declare a new line")
        self.assertIn(f"legacy baseline {later} is not named by its Human Decision HD-105", refused.stdout)
        self.assertIn(f"(it names {first})", refused.stdout)
        # The anchor is specific to its kind: the decision that names the adoption baseline does
        # not thereby name a proof-of-reading baseline, even on the same commit.
        state["legacy_baseline"] = {"head": first, "human_decision_ref": "HD-105"}
        state["authorities_baseline"] = {"head": first, "human_decision_ref": "HD-105"}
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        refused = run_control(root, "audit")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn(f"authorities baseline {first} is not named by its Human Decision HD-105", refused.stdout)
        self.assertIn("`Authorities baseline commit: ", refused.stdout)
        self.assertIn("PASS: LEGACY_EVIDENCE_FROZEN", refused.stdout)

    def test_legacy_baseline_freezes_history_and_requires_new_proof_forward(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        # WI-001: closed, then rewritten the way older projects recorded closures —
        # free-text evidence and no close_head.
        created = self.create_lifecycle_work_item(root, "WI-001", "HD-102")
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        started = self.start_command(root, "WI-001")
        self.assertEqual(started.returncode, 0, started.stdout + started.stderr)
        branch = run_git(root, "branch", "--show-current").stdout.strip()
        (root / "reports/WI-001.txt").write_text("historical change\n", encoding="utf-8")
        self.commit_fixture(root, "fixture: historical change")
        self.merge_fixture_branch(root, branch, "fixture: integrate historical change")
        closed = self.close_with_evidence(root, "WI-001", self.write_committed_evidence(root, "WI-001"))
        self.assertEqual(closed.returncode, 0, closed.stdout + closed.stderr)
        # WI-002: blocked with a free-text failed check, as older projects recorded it.
        item = self.create_and_start_lifecycle_work_item(root, "WI-002", "HD-103")
        self.switch_to_canonical(root)
        legacy_reference = "historical failed check before credentials became available"
        item["test_status"] = "FAILED"
        item["evidence"]["tests"] = [legacy_reference]
        item2_path = root / "project_control/work-items/WI-002.json"
        item2_path.write_text(json.dumps(item, indent=2) + "\n", encoding="utf-8")
        self.commit_fixture(root, "fixture: historical failed check on canonical")
        self.record_lifecycle_human_decision(root, "HD-104", "WI-002", "Authorize blocking WI-002 on its external dependency.")
        blocked = self.block_lifecycle_work_item(root, "WI-002", "HD-104")
        self.assertEqual(blocked.returncode, 0, blocked.stdout + blocked.stderr)
        item_path = root / "project_control/work-items/WI-001.json"
        historical = load_json(item_path)
        historical.pop("close_head")
        historical["evidence"]["tests"] = ["python3 -B -m unittest discover -s tests: 12/12 PASS"]
        historical["evidence"]["integration"] = ["merged into main by the Project Owner; contract checks PASS"]
        item_path.write_text(json.dumps(historical, indent=2) + "\n", encoding="utf-8")
        baseline = self.commit_fixture(root, "fixture: closure recorded before the current contract")
        # Without a declared baseline the current contract refuses that closure: nothing is inferred.
        refused = run_control(root, "audit")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("WI-001: close_head is missing or not in current history", refused.stdout)
        frozen_bytes = item_path.read_bytes()
        self.declare_legacy_baseline(root, baseline, "HD-105")
        audit = run_control(root, "audit")
        self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)
        self.assertIn(f"PASS: LEGACY_RECORDS_PRESENT — 3 legacy Work Item(s) frozen at {baseline}", audit.stdout)
        status = run_control(root, "status", "--json")
        self.assertEqual(status.returncode, 0, status.stdout + status.stderr)
        payload = json.loads(status.stdout)
        self.assertEqual(payload["legacy_baseline"], baseline)
        validation = {view["work_item_id"]: view["evidence_validation"] for view in payload["work_items"]}
        self.assertEqual(validation, {"WI-000": "LEGACY_PRESERVED", "WI-001": "LEGACY_PRESERVED", "WI-002": "PENDING"})
        self.assertIn("(dont 2 figés avant la baseline d'adoption)", run_control(root, "status").stdout)
        # Frozen history: a byte change or the removal of a historical record is refused.
        item_path.write_bytes(frozen_bytes + b"\n")
        tampered = run_control(root, "audit")
        self.assertNotEqual(tampered.returncode, 0)
        self.assertIn("FAIL: LEGACY_EVIDENCE_FROZEN — WI-001: legacy DONE record changed", tampered.stdout)
        item_path.unlink()
        removed = run_control(root, "audit")
        self.assertNotEqual(removed.returncode, 0)
        self.assertIn("FAIL: LEGACY_RECORDS_PRESENT — WI-001: legacy Work Item is missing", removed.stdout)
        item_path.write_bytes(frozen_bytes)
        restored = run_control(root, "audit")
        self.assertEqual(restored.returncode, 0, restored.stdout + restored.stderr)
        # Forward: the resumed historical Work Item keeps its prefix and needs new verifiable evidence.
        self.record_lifecycle_human_decision(
            root, "HD-106", "WI-002", "Confirm the dependency and authorize resume.", action="RESUME",
        )
        resumed = self.resume_lifecycle_work_item(root, "WI-002", "HD-106")
        self.assertEqual(resumed.returncode, 0, resumed.stdout + resumed.stderr)
        resumed_item = load_json(item2_path)
        self.assertEqual(resumed_item["test_status"], "FAILED")
        self.assertEqual(resumed_item["evidence"]["tests"], [legacy_reference])
        (root / "reports/WI-002.txt").write_text("corrected after resume\n", encoding="utf-8")
        self.commit_fixture(root, "fixture: complete resumed change")
        self.merge_fixture_branch(root, item["branch"], "fixture: integrate resumed change")
        new_evidence = self.write_committed_evidence(root, "WI-002")
        claim_only = self.close_with_evidence(
            root, "WI-002", {"tests": "new unverifiable claim", "integration": new_evidence["integration"]},
        )
        self.assertNotEqual(claim_only.returncode, 0)
        self.assertEqual(load_json(item2_path)["status"], "IN_PROGRESS")
        closed = self.close_with_evidence(root, "WI-002", new_evidence)
        self.assertEqual(closed.returncode, 0, closed.stdout + closed.stderr)
        done = load_json(item2_path)
        self.assertEqual(done["status"], "DONE")
        self.assertEqual(done["test_status"], "TESTED")
        self.assertEqual(done["evidence"]["tests"], [legacy_reference, new_evidence["tests"]])
        payload = json.loads(run_control(root, "status", "--json").stdout)
        self.assertEqual(
            next(view["evidence_validation"] for view in payload["work_items"] if view["work_item_id"] == "WI-002"),
            "STRUCTURED_VERIFIED",
        )
        # The historical prefix of a resumed Work Item is not removable either.
        done["evidence"]["tests"].pop(0)
        item2_path.write_text(json.dumps(done, indent=2) + "\n", encoding="utf-8")
        corrupted = run_control(root, "audit")
        self.assertNotEqual(corrupted.returncode, 0)
        self.assertIn("WI-002: legacy tests evidence history changed", corrupted.stdout)

    def test_legacy_baseline_must_be_declared_by_a_recorded_decision_in_current_history(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        state_path = root / "project_control/project-state.v1.json"
        state = load_json(state_path)
        head = run_git(root, "rev-parse", "HEAD").stdout.strip()
        unknown = "0123456789abcdef0123456789abcdef01234567"
        cases = (
            ("commit outside history", {"head": unknown, "human_decision_ref": "HD-101"},
             f"legacy baseline {unknown} is missing or not in current history"),
            ("unrecorded decision", {"head": head, "human_decision_ref": "HD-999"},
             "legacy baseline requires a recorded Human Decision: HD-999"),
            ("malformed head", {"head": "HEAD", "human_decision_ref": "HD-101"}, "pattern mismatch"),
            ("missing declaration", None, "missing legacy_baseline"),
            # The decision is recorded and valid — but it does not say which commit it freezes.
            ("decision that does not name the commit", {"head": head, "human_decision_ref": "HD-101"},
             f"legacy baseline {head} is not named by its Human Decision HD-101"),
        )
        for label, declared, message in cases:
            with self.subTest(label=label):
                state.pop("legacy_baseline", None)
                if declared is not None:
                    state["legacy_baseline"] = declared
                state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
                before = self.snapshot_repository(root)
                for command in (("audit",), ("status", "--json")):
                    refused = run_control(root, *command)
                    self.assertNotEqual(refused.returncode, 0, label)
                    output = refused.stdout + refused.stderr
                    self.assertNotIn("Traceback", output)
                    self.assertIn(message, output)
                    if command[0] == "status":
                        self.assertEqual(json.loads(refused.stdout)["audit_status"], "FAIL")
                self.assertEqual(self.snapshot_repository(root), before)
        # A valid declaration — one whose decision names the commit — is accepted exactly as
        # declared; HEAD is never substituted for it.
        state.pop("legacy_baseline", None)
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        self.declare_legacy_baseline(root, head, "HD-105")
        audit = run_control(root, "audit")
        self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)
        self.assertIn(f"PASS: LEGACY_EVIDENCE_FROZEN — 1 legacy Work Item(s) frozen at {head}", audit.stdout)
        # A record cannot opt out of strict evidence through an extra field.
        for name in ("legacy_evidence", "skip_evidence_validation", "legacy_baseline"):
            with self.subTest(field=name):
                altered = copy.deepcopy(self.work_item)
                altered[name] = True
                errors = self.control_module.validate_work_item(altered, "ALPHA")
                self.assertTrue(any(name in error for error in errors), errors)

    # --- Proof of reading (P3): routed authorities hashed, presented at start/resume, kept current ---

    def test_context_manifest_is_deterministic_and_follows_the_work_item_scopes(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        created = self.create_lifecycle_work_item(root, "WI-001", "HD-102", authorized_path="modules/domain/engine.py")
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        first = run_control(root, "context-manifest", "WI-001")
        second = run_control(root, "context-manifest", "WI-001")
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        self.assertIn("CONTEXT_MANIFEST: WI-001 | scopes: development", first.stdout)
        digest_lines = [line for line in first.stdout.splitlines() if line.startswith("MANIFEST_DIGEST: ")]
        self.assertEqual(len(digest_lines), 1)
        self.assertEqual(digest_lines, [line for line in second.stdout.splitlines() if line.startswith("MANIFEST_DIGEST: ")])
        listed = [line.split()[1] for line in first.stdout.splitlines() if line.startswith("AUTHORITY: ")]
        self.assertIn("docs/governance/PROJECT_CHARTER.md", listed)
        self.assertIn("docs/governance/HUMAN_DECISIONS.md", listed)
        self.assertIn("project_control/schemas/work-item.v1.schema.json", listed, "development scope routed")
        for bookkeeping in ("docs/governance/ROADMAP.md", "docs/governance/WORKTREE_REGISTRY.md", "project_control/project-state.v1.json"):
            self.assertNotIn(bookkeeping, listed, "records kept by Project Control are not part of the proof")
        payload = json.loads(run_control(root, "context-manifest", "WI-001", "--json").stdout)
        self.assertEqual(payload["manifest_digest"], digest_lines[0].split(": ", 1)[1])
        self.assertEqual(self.control_module.manifest_digest(payload["entries"]), payload["manifest_digest"])
        # A changed authority changes the digest; an explicit scope adds its documents.
        charter = root / "docs/governance/PROJECT_CHARTER.md"
        charter.write_text(charter.read_text(encoding="utf-8") + "\nAmended.\n", encoding="utf-8")
        changed = self.authorities_digest(root, "WI-001")
        self.assertNotEqual(changed, payload["manifest_digest"])
        with_runtime = json.loads(run_control(root, "context-manifest", "WI-001", "--scope", "runtime", "--json").stdout)
        # The runtime scope adds the documents the fixture itself routes there: the expectation
        # follows the routing of the copy under test, never the template's own document set.
        routing = load_json(root / "docs/agent-governance/mandatory-documents.v1.json")
        runtime_only = [
            path for path in routing["scopes"]["runtime"]
            if path not in routing["base"] and (root / path).is_file()
        ]
        self.assertTrue(runtime_only, "the fixture routes at least one runtime-only authority")
        for path in runtime_only:
            self.assertIn(path, [entry["path"] for entry in with_runtime["entries"]])

    def test_start_and_resume_require_the_current_authorities_digest(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        created = self.create_lifecycle_work_item(root, "WI-001", "HD-102")
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        before = self.snapshot_repository(root)
        # S-01: no digest, or a digest that is not the current manifest, refuses the start.
        refused = run_control(root, "start", "WI-001")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("start requires --authorities-digest", refused.stdout)
        self.assertIsNone(re.search(r"\b[0-9a-f]{64}\b", refused.stdout), "the expected digest is never leaked by the refusal")
        self.assertEqual(self.snapshot_repository(root), before)
        stale = run_control(root, "start", "WI-001", "--authorities-digest", "0" * 64)
        self.assertNotEqual(stale.returncode, 0)
        self.assertIn("does not match the current authorities", stale.stdout)
        self.assertIsNone(re.search(r"\b[1-9a-f][0-9a-f]{63}\b", stale.stdout), "the refusal echoes neither the expected digest")
        self.assertEqual(self.snapshot_repository(root), before)
        expected = json.loads(run_control(root, "context-manifest", "WI-001", "--json").stdout)
        started = self.start_command(root, "WI-001")
        self.assertEqual(started.returncode, 0, started.stdout + started.stderr)
        run = load_json(root / "project_control/agent-runs/RUN-WI-001-001.json")
        self.assertEqual(run["authorities_read"]["manifest_digest"], expected["manifest_digest"])
        self.assertEqual(run["authorities_read"]["entries"], expected["entries"])
        preflight = run_control(root, "preflight", "WI-001")
        self.assertEqual(preflight.returncode, 0, preflight.stdout + preflight.stderr)
        for check in ("PRESENT", "COMPLETE", "CURRENT"):
            self.assertIn(f"PASS: AUTHORITY_MANIFEST_{check}", preflight.stdout)
        # S-03: a resumed Work Item starts a new run that must present the current digest again.
        self.switch_to_canonical(root)
        self.record_lifecycle_human_decision(root, "HD-103", "WI-001", "Authorize blocking WI-001 on its external dependency.")
        blocked = self.block_lifecycle_work_item(root, "WI-001", "HD-103")
        self.assertEqual(blocked.returncode, 0, blocked.stdout + blocked.stderr)
        self.record_lifecycle_human_decision(root, "HD-104", "WI-001", "Confirm the dependency and authorize resume.", action="RESUME")
        before = self.snapshot_repository(root)
        blind = run_control(root, "resume", "WI-001", "--human-decision", "HD-104", "--agent-provider", "FixtureAgent")
        self.assertNotEqual(blind.returncode, 0)
        self.assertIn("resume requires --authorities-digest", blind.stdout)
        self.assertEqual(self.snapshot_repository(root), before)
        resumed = self.resume_lifecycle_work_item(root, "WI-001", "HD-104")
        self.assertEqual(resumed.returncode, 0, resumed.stdout + resumed.stderr)
        second_run = load_json(root / "project_control/agent-runs/RUN-WI-001-002.json")
        self.assertIn("docs/governance/HUMAN_DECISIONS.md", [entry["path"] for entry in second_run["authorities_read"]["entries"]])
        self.assertNotEqual(second_run["authorities_read"]["manifest_digest"], run["authorities_read"]["manifest_digest"],
                            "the new decisions changed the authorities, and the new run read them")

    def test_changed_authority_blocks_preflight_and_close_until_reacknowledged(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        item = self.create_and_start_lifecycle_work_item(root, "WI-001", "HD-102")
        branch = item["branch"]
        # S-02: the Charter changes on the canonical branch during the session.
        self.switch_to_canonical(root)
        charter = root / "docs/governance/PROJECT_CHARTER.md"
        charter.write_text(charter.read_text(encoding="utf-8") + "\nScope narrowed by the Project Owner.\n", encoding="utf-8")
        self.commit_fixture(root, "fixture: Charter amended during the session")
        switched = run_git(root, "switch", branch)
        self.assertEqual(switched.returncode, 0, switched.stdout + switched.stderr)
        merged = run_git(root, "merge", "--ff-only", "main")
        self.assertEqual(merged.returncode, 0, merged.stdout + merged.stderr)
        preflight = run_control(root, "preflight", "WI-001")
        self.assertNotEqual(preflight.returncode, 0)
        self.assertIn("FAIL: AUTHORITY_MANIFEST_CURRENT", preflight.stdout)
        self.assertIn("docs/governance/PROJECT_CHARTER.md", preflight.stdout)
        status = json.loads(run_control(root, "status", "--json").stdout)
        self.assertEqual(next(view["authorities"] for view in status["work_items"] if view["work_item_id"] == "WI-001"), "STALE")
        # Work continues only after an explicit re-reading, recorded on the run from the canonical branch.
        (root / "reports/WI-001.txt").write_text("work after the amendment\n", encoding="utf-8")
        self.commit_fixture(root, "fixture: work on the branch")
        self.merge_fixture_branch(root, branch, "fixture: integrate WI-001")
        evidence = self.write_committed_evidence(root, "WI-001")
        refused = self.close_with_evidence(root, "WI-001", evidence)
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("AUTHORITY_MANIFEST_AT_CLOSE", refused.stdout)
        self.assertEqual(load_json(root / "project_control/work-items/WI-001.json")["status"], "IN_PROGRESS")
        stale_digest = run_control(root, "acknowledge-authorities", "WI-001", "--authorities-digest", "0" * 64)
        self.assertNotEqual(stale_digest.returncode, 0)
        acknowledged = run_control(root, "acknowledge-authorities", "WI-001", "--authorities-digest", self.authorities_digest(root, "WI-001"))
        self.assertEqual(acknowledged.returncode, 0, acknowledged.stdout + acknowledged.stderr)
        self.assertIn("chore(project-control): acknowledge authorities WI-001", run_git(root, "log", "-1", "--format=%s").stdout)
        run = load_json(root / "project_control/agent-runs/RUN-WI-001-001.json")
        self.assertEqual(run["authorities_read"]["manifest_digest"], self.authorities_digest(root, "WI-001"))
        closed = self.close_with_evidence(root, "WI-001", evidence)
        self.assertEqual(closed.returncode, 0, closed.stdout + closed.stderr)
        audit = run_control(root, "audit")
        self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)

    def test_an_authority_the_work_item_is_authorized_to_write_does_not_stale_its_own_proof(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        self.create_and_start_lifecycle_work_item(root, "WI-001", "HD-102", authorized_path="docs/governance/PROJECT_CHARTER.md")
        charter = root / "docs/governance/PROJECT_CHARTER.md"
        charter.write_text(charter.read_text(encoding="utf-8") + "\nAmended under WI-001.\n", encoding="utf-8")
        preflight = run_control(root, "preflight", "WI-001", "--path", "docs/governance/PROJECT_CHARTER.md")
        self.assertEqual(preflight.returncode, 0, preflight.stdout + preflight.stderr)
        self.assertIn("PASS: AUTHORITY_MANIFEST_CURRENT", preflight.stdout)
        # An authority outside the authorization still has to be re-read.
        definition = root / "docs/governance/DEFINITION_OF_DONE.md"
        definition.write_text(definition.read_text(encoding="utf-8") + "\nChanged by someone else.\n", encoding="utf-8")
        stale = run_control(root, "preflight", "WI-001", "--path", "docs/governance/PROJECT_CHARTER.md")
        self.assertNotEqual(stale.returncode, 0)
        self.assertIn("FAIL: AUTHORITY_MANIFEST_CURRENT", stale.stdout)
        self.assertIn("docs/governance/DEFINITION_OF_DONE.md", stale.stdout)
        self.assertNotIn("PROJECT_CHARTER.md']", stale.stdout)

    def test_agent_runs_before_the_adoption_baseline_are_exempt_from_the_proof_of_reading(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        self.create_and_start_lifecycle_work_item(root, "WI-001", "HD-102")
        self.switch_to_canonical(root)
        run_path = root / "project_control/agent-runs/RUN-WI-001-001.json"
        run = load_json(run_path)
        run.pop("authorities_read")
        run_path.write_text(json.dumps(run, indent=2) + "\n", encoding="utf-8")
        baseline = self.commit_fixture(root, "fixture: historical Agent Run without a proof of reading")
        refused = run_control(root, "audit")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("Agent Run RUN-WI-001-001: authorities_read is required after the adoption baseline", refused.stdout)
        self.declare_legacy_baseline(root, baseline, "HD-105")
        accepted = run_control(root, "audit")
        self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)

    def test_a_decision_frozen_at_the_adoption_baseline_keeps_its_own_vocabulary(self) -> None:
        """A project adopting the controller brings decisions written before its rules existed.

        The adoption baseline freezes that history: a `Chosen option` recorded in the project's
        own words, before the baseline, is read as written. Everything else a decision must
        carry is still required."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        self.create_start_and_close_lifecycle_work_item(root, "WI-001", "HD-102")
        self.rewrite_chosen_option(root, "HD-102", "PILOT_SELECTION = APPROVED for the three listed companies")
        baseline = self.commit_fixture(root, "fixture: a closure recorded in the vocabulary of its time")
        refused = run_control(root, "audit")
        self.assertNotEqual(refused.returncode, 0, "without a baseline the current rule applies")
        self.assertIn("HD-102: Chosen option is not AUTHORIZE", refused.stdout)
        self.declare_legacy_baseline(root, baseline, "HD-105")
        accepted = run_control(root, "audit")
        self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)
        # The exemption is narrow: it waives the later wording, not what a decision must carry.
        path = root / "docs/governance/HUMAN_DECISIONS.md"
        text = path.read_text(encoding="utf-8")
        block = recorded_decision_block(text, "HD-102")
        path.write_text(text.replace(block, re.sub(r"(?m)^Authorized by:.*$", "Authorized by: UNKNOWN", block)), encoding="utf-8")
        self.commit_fixture(root, "fixture: the frozen decision loses its authorizer")
        unsigned = run_control(root, "audit")
        self.assertNotEqual(unsigned.returncode, 0)
        self.assertIn("HD-102: Authorized by is missing or UNKNOWN", unsigned.stdout)

    def test_a_decision_rewritten_since_the_adoption_baseline_loses_its_exemption(self) -> None:
        """The exemption follows the state, not the name: rewriting a frozen decision brings it
        back under the current rule, as the proof of reading already does for Agent Runs."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        self.create_start_and_close_lifecycle_work_item(root, "WI-001", "HD-102")
        self.rewrite_chosen_option(root, "HD-102", "PILOT_SELECTION = APPROVED for the three listed companies")
        baseline = self.commit_fixture(root, "fixture: a closure recorded in the vocabulary of its time")
        self.declare_legacy_baseline(root, baseline, "HD-105")
        self.assertEqual(run_control(root, "audit").returncode, 0)
        # Recording a later decision must not, by itself, revoke the exemption of an earlier one.
        self.assertIn("## HD-105", (root / "docs/governance/HUMAN_DECISIONS.md").read_text(encoding="utf-8"))
        self.rewrite_chosen_option(root, "HD-102", "PILOT_SELECTION = APPROVED for four listed companies")
        self.commit_fixture(root, "fixture: the frozen decision is rewritten")
        rewritten = run_control(root, "audit")
        self.assertNotEqual(rewritten.returncode, 0)
        self.assertIn("HD-102: Chosen option is not AUTHORIZE", rewritten.stdout)

    def test_a_decision_recorded_after_the_adoption_baseline_still_needs_authorize(self) -> None:
        """The baseline freezes what precedes it and nothing else: a decision recorded afterwards
        is a decision of today, and a recorded refusal never becomes a mandate."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        adoption = run_git(root, "rev-parse", "HEAD").stdout.strip()
        self.declare_legacy_baseline(root, adoption, "HD-105")
        self.create_and_start_lifecycle_work_item(root, "WI-001", "HD-102")
        self.switch_to_canonical(root)
        self.rewrite_chosen_option(root, "HD-102", "PILOT_SELECTION = APPROVED for the three listed companies")
        self.commit_fixture(root, "fixture: a decision recorded after the adoption baseline")
        refused = run_control(root, "audit")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("HD-102: Chosen option is not AUTHORIZE", refused.stdout)

    def test_a_note_about_the_expected_status_does_not_validate_a_draft(self) -> None:
        """A document may explain what the controller expects of it — that is what a newcomer
        needs. Explaining it must not satisfy it: the check reads the line that declares the
        status, never a later mention of it."""
        temporary, root = self.make_copy()
        self.addCleanup(temporary.cleanup)
        self.configure_ready_for_closeout(root, "WI-001")
        ready = run_control(root, "bootstrap-closeout", "--path", "FIRST_START.md",
                            "--path", "project_control/project-state.v1.json")
        self.assertEqual(ready.returncode, 0, ready.stdout + ready.stderr)
        (root / "docs/architecture/INITIAL_ARCHITECTURE.md").write_text(
            "# Initial Architecture\n\nStatus: `DRAFT — PROJECT_OWNER_VALIDATION_REQUIRED`\n\n"
            "> À la clôture de l'initialisation, le contrôleur exige exactement "
            "`` Status: `VALIDATED` `` sur la ligne ci-dessus.\n",
            encoding="utf-8",
        )
        refused = run_control(root, "bootstrap-closeout", "--path", "FIRST_START.md",
                              "--path", "project_control/project-state.v1.json")
        self.assertNotEqual(refused.returncode, 0, "a draft that quotes the expected status stays a draft")
        self.assertIn("validated initial architecture", refused.stdout)
        # And the note alone, on a document that really is validated, changes nothing.
        (root / "docs/architecture/INITIAL_ARCHITECTURE.md").write_text(
            "# Initial Architecture\n\nStatus: `VALIDATED`\n\n"
            "> À la clôture de l'initialisation, le contrôleur exige exactement "
            "`` Status: `VALIDATED` `` sur la ligne ci-dessus.\n",
            encoding="utf-8",
        )
        accepted = run_control(root, "bootstrap-closeout", "--path", "FIRST_START.md",
                               "--path", "project_control/project-state.v1.json")
        self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)

    def test_close_reads_its_mandate_in_full_whatever_the_baseline_froze(self) -> None:
        """The adoption baseline freezes closures, not the right to close. A Work Item still open
        at that commit follows the current contract at its next closure — the doctrine says so,
        and a recorded refusal must never be the mandate of a closure made today."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        item = self.create_and_start_lifecycle_work_item(root, "WI-001", "HD-102")
        self.switch_to_canonical(root)
        # The mandate becomes a refusal, and that state is declared as frozen history.
        self.rewrite_chosen_option(root, "HD-102", "REJECT")
        baseline = self.commit_fixture(root, "fixture: the mandate now records a refusal")
        self.declare_legacy_baseline(root, baseline, "HD-105")
        self.merge_fixture_branch(root, item["branch"], "fixture: integrate WI-001")
        evidence = self.write_committed_evidence(root, "WI-001")
        # The exemption does not reach an open Work Item: the audit sees the refusal again, and
        # every transition of today is refused with it — acknowledging, then closing.
        audited = run_control(root, "audit")
        self.assertNotEqual(audited.returncode, 0)
        self.assertIn("HD-102: Chosen option is not AUTHORIZE", audited.stdout)
        acknowledged = run_control(root, "acknowledge-authorities", "WI-001",
                                   "--authorities-digest", self.authorities_digest(root, "WI-001") or "0" * 64)
        self.assertNotEqual(acknowledged.returncode, 0)
        refused = self.close_with_evidence(root, "WI-001", evidence)
        self.assertNotEqual(refused.returncode, 0, "a recorded refusal closes nothing")
        self.assertEqual(
            load_json(root / "project_control/work-items/WI-001.json")["status"], "IN_PROGRESS")
        # The same Work Item closes as soon as its mandate authorizes again: it is the recorded
        # refusal that blocks, not the baseline.
        self.rewrite_chosen_option(root, "HD-102", "AUTHORIZE")
        self.commit_fixture(root, "fixture: the mandate authorizes again")
        acknowledged = run_control(root, "acknowledge-authorities", "WI-001",
                                   "--authorities-digest", self.authorities_digest(root, "WI-001"))
        self.assertEqual(acknowledged.returncode, 0, acknowledged.stdout + acknowledged.stderr)
        accepted = self.close_with_evidence(root, "WI-001", evidence)
        self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)

    def test_a_run_that_passes_while_printing_an_expected_error_is_not_refused(self) -> None:
        """A test that checks an invalid input is rejected prints a diagnostic and passes. Refusing
        its proof punished an honest campaign; only what a run says about its own outcome counts."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        item = self.create_and_start_lifecycle_work_item(root, "WI-001", "HD-102")
        self.switch_to_canonical(root)
        self.merge_fixture_branch(root, item["branch"], "fixture: integrate WI-001")
        diagnostic = (
            "test_rejects_an_invalid_row (tests.test_import.ImportTests) ... ok\n"
            "ERROR: ligne 4 refusée — colonne « quantité » absente\n"
            "Traceback (most recent call last):\n"
            "  File \"import.py\", line 12, in read\n"
            "ValueError: colonne manquante\n"
            "diagnostic attendu du lot 2 : errors=1, corrigé par le lot 3\n"
            "----------------------------------------------------------------------\n"
            "Ran 12 tests in 0.031s\n\nOK\n"
        )
        evidence = self.write_committed_evidence(root, "WI-001", artifacts={"tests": diagnostic})
        accepted = self.close_with_evidence(root, "WI-001", evidence)
        self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)
        self.assertEqual(load_json(root / "project_control/work-items/WI-001.json")["status"], "DONE")

    def test_the_only_output_of_a_program_that_died_is_not_a_proof_of_success(self) -> None:
        """Reading only verdict lines let a proof cite, as its single artifact, the output of a
        program that really failed: a diagnostic and nothing else. A diagnostic alone is all a dead
        program had time to say; beside a verdict of success it is the expected noise of a test that
        checks an invalid input is rejected — the case the test above keeps green."""
        for name, artifact in (
            ("an ERROR and nothing else",
             "ERROR: campagne échouée : contrôle 2 + 2 == 5 refusé\n"),
            ("a traceback and nothing else",
             "Traceback (most recent call last):\n"
             "  File \"check.py\", line 3, in <module>\n"
             "    assert 2 + 2 == 5\n"
             "AssertionError\n"),
        ):
            with self.subTest(name):
                temporary, root = self.make_normal_copy()
                self.addCleanup(temporary.cleanup)
                item = self.create_and_start_lifecycle_work_item(root, "WI-001", "HD-102")
                self.switch_to_canonical(root)
                self.merge_fixture_branch(root, item["branch"], "fixture: integrate WI-001")
                lying = self.write_committed_evidence(root, "WI-001", artifacts={"tests": artifact})
                refused = self.close_with_evidence(root, "WI-001", lying)
                self.assertNotEqual(refused.returncode, 0, "the sole output of a failed run proves nothing")
                self.assertTrue("every text artifact it cites reports a failure" in refused.stdout,
                                refused.stdout[:400])
                self.assertEqual(
                    load_json(root / "project_control/work-items/WI-001.json")["status"], "IN_PROGRESS")

    def test_an_upgrade_is_rehearsed_before_it_is_written(self) -> None:
        """The command that upgrades a project runs under the project's current controller, which
        knows nothing of the rules the new version brings. Applied blind, the upgrade completed
        and left the project refused by its own audit — the wall met at 3.8.0 with three
        registers, and again with the baselines a decision must now name. The upgrade is
        rehearsed first: the new controller's audit runs on a throwaway checkout carrying the
        new core, what it refuses is reported, and --apply refuses while it does."""
        def a_rule_this_project_does_not_satisfy(source: Path) -> None:
            controller = source / "scripts/project_control.py"
            content = controller.read_text(encoding="utf-8")
            marker = '    ".gitignore",\n    "README.md", "FIRST_START.md", "AGENTS.md", "applications/README.md",'
            self.assertEqual(content.count(marker), 1)
            controller.write_text(content.replace(
                marker, '    ".gitignore", "docs/governance/DATA_RETENTION.md",\n'
                        '    "README.md", "FIRST_START.md", "AGENTS.md", "applications/README.md",', 1,
            ), encoding="utf-8")

        upstream = self.make_template_source("9.9.9", a_rule_this_project_does_not_satisfy)
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        before = self.snapshot_repository(root)
        report = run_control(root, "template-upgrade", "--source", str(upstream))
        self.assertNotEqual(report.returncode, 0, "the rehearsal must refuse what the new audit refuses")
        self.assertIn("PASS: REQUIRED_FILES", report.stdout, "the current controller cannot know the new rule")
        self.assertIn("FAIL: UPGRADE_REHEARSAL", report.stdout)
        self.assertIn("MANDATORY_FILES", report.stdout)
        self.assertIn("docs/governance/DATA_RETENTION.md", report.stdout)
        refused = run_control(root, "template-upgrade", "--source", str(upstream), "--apply")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("FAIL: APPLY — refused", refused.stdout)
        self.assertEqual(self.snapshot_repository(root), before, "a refused upgrade writes nothing")
        worktrees = run_git(root, "worktree", "list", "--porcelain").stdout
        self.assertEqual(worktrees.count("worktree "), 1, f"the rehearsal leaves no checkout behind: {worktrees}")
        # Once the project satisfies the rule — committed, since the rehearsal audits what the
        # project holds — the upgrade passes its rehearsal and applies.
        (root / "docs/governance/DATA_RETENTION.md").write_text("# Data retention\n", encoding="utf-8")
        self.commit_fixture(root, "docs: what the new version requires")
        applied = run_control(root, "template-upgrade", "--source", str(upstream), "--apply")
        self.assertEqual(applied.returncode, 0, applied.stdout + applied.stderr)
        self.assertIn("PASS: UPGRADE_REHEARSAL — the new controller's audit passes on a throwaway checkout", applied.stdout)
        self.assertIn("PASS: APPLY", applied.stdout)
        self.assertEqual(run_git(root, "worktree", "list", "--porcelain").stdout.count("worktree "), 1)

    def test_an_upgrade_that_only_changes_the_gate_is_rehearsed_and_accepted(self) -> None:
        """A source whose only change is the commit gate: on a project that has the gate
        installed, the rehearsal's audit fails on COMMIT_GATE alone — the installed copy no
        longer matches the new reference — and that check is exempt, because the apply
        reinstalls the gate itself. The audit still exits non-zero for it, and that exit status
        used to be read as a second, generic failure: a legitimate upgrade refused (fourth
        independent control, F13-01)."""
        def only_the_gate(source: Path) -> None:
            hook = source / "scripts/hooks/pre-commit"
            hook.write_text(hook.read_text(encoding="utf-8") + "# the gate, commented once more\n", encoding="utf-8")

        upstream = self.make_template_source("9.9.9", only_the_gate)
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        self.install_commit_hook(root)
        applied = run_control(root, "template-upgrade", "--source", str(upstream), "--apply")
        self.assertEqual(applied.returncode, 0, applied.stdout + applied.stderr)
        self.assertIn("PASS: UPGRADE_REHEARSAL", applied.stdout)
        self.assertIn("exempt: ['COMMIT_GATE']", applied.stdout)
        self.assertIn("PASS: APPLY", applied.stdout)
        self.assertIn("PASS: COMMIT_GATE_REINSTALLED", applied.stdout)
        audit = run_control(root, "audit")
        self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)
        self.assertIn("PASS: COMMIT_GATE — gate installed outside the worktree", audit.stdout)

    def test_a_rehearsal_rerun_after_an_uncommitted_apply_still_audits_with_the_new_controller(self) -> None:
        """A core written on the disk but not yet committed — by an older controller that did not
        rehearse — left the rehearsal with nothing to write: every core path was already identical
        on the disk, so the throwaway checkout of HEAD kept the *old* controller, whose audit was
        run while the new one was announced (fourth independent control, F13-02). The rehearsal
        is measured against HEAD now, whatever the disk holds."""
        def a_rule_this_project_does_not_satisfy(source: Path) -> None:
            controller = source / "scripts/project_control.py"
            content = controller.read_text(encoding="utf-8")
            marker = '    ".gitignore",\n    "README.md", "FIRST_START.md", "AGENTS.md", "applications/README.md",'
            self.assertEqual(content.count(marker), 1)
            controller.write_text(content.replace(
                marker, '    ".gitignore", "docs/governance/DATA_RETENTION.md",\n'
                        '    "README.md", "FIRST_START.md", "AGENTS.md", "applications/README.md",', 1,
            ), encoding="utf-8")

        upstream = self.make_template_source("9.9.9", a_rule_this_project_does_not_satisfy)
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        # The blind apply of an older controller: the new core on the disk, nothing committed —
        # keeping, as an apply does, the project's own initialization marker in FIRST_START.md.
        manifest = load_json(upstream / self.CORE_MANIFEST)
        for relative in list(manifest["core"]) + [self.CORE_MANIFEST]:
            if relative == "FIRST_START.md":
                continue
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(upstream / relative, target)
        head_before = run_git(root, "rev-parse", "HEAD").stdout.strip()
        rerun = run_control(root, "template-upgrade", "--source", str(upstream), "--apply")
        self.assertNotEqual(rerun.returncode, 0, "the rerun must audit with the new controller, and refuse")
        self.assertIn("PASS: UPGRADE_PLAN — 9.9.9 -> 9.9.9: identical 24", rerun.stdout)
        self.assertIn("FAIL: UPGRADE_REHEARSAL", rerun.stdout)
        self.assertIn("docs/governance/DATA_RETENTION.md", rerun.stdout)
        self.assertIn("FAIL: APPLY — refused", rerun.stdout)
        self.assertEqual(run_git(root, "rev-parse", "HEAD").stdout.strip(), head_before)
        self.assertEqual(run_git(root, "worktree", "list", "--porcelain").stdout.count("worktree "), 1)

    def test_an_upgrade_names_and_seeds_the_files_the_new_version_requires(self) -> None:
        """A newer version may make mandatory a file the project does not have and the core does
        not carry — the project's own ideas list, its view settings. Missing, they fail the audit,
        and the commands meant to create them refuse for want of them: the project can neither
        audit nor commit, and copying them onto the Work Item branch is refused because they are
        administrative records. The upgrade names them and writes them where records live."""
        upstream = self.make_template_source("9.9.9")
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        required = ["docs/governance/IDEAS.md", "docs/governance/ideas-state.v1.json",
                    "project_control/roadmap-view.v1.json"]
        removed = run_git(root, "rm", "-q", "--", *required)
        self.assertEqual(removed.returncode, 0, removed.stdout + removed.stderr)
        self.commit_fixture(root, "fixture: a project older than these mandatory files")
        # The report names them, and the upgrade refuses rather than leave the project stuck.
        report = run_control(root, "template-upgrade", "--source", str(upstream))
        self.assertNotEqual(report.returncode, 0)
        self.assertIn("FAIL: REQUIRED_FILES", report.stdout)
        for path in required:
            self.assertTrue(path in report.stdout, f"{path} is not named: {report.stdout[:400]}")
        self.assertIn("--seed-required", report.stdout)
        refused = run_control(root, "template-upgrade", "--source", str(upstream), "--apply")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("FAIL: APPLY", refused.stdout)
        # They are records: the Work Item branch is not where they are written.
        switched = run_git(root, "switch", "-c", "work/wi-001-upgrade")
        self.assertEqual(switched.returncode, 0, switched.stdout + switched.stderr)
        on_branch = run_control(root, "template-upgrade", "--source", str(upstream), "--seed-required")
        self.assertNotEqual(on_branch.returncode, 0)
        self.assertIn("administrative records are written on main only", on_branch.stdout)
        self.assertFalse((root / required[0]).exists(), "a refusal writes nothing")
        # On the canonical branch they are written, blank, exactly as the template holds them.
        self.switch_to_canonical(root)
        seeded = run_control(root, "template-upgrade", "--source", str(upstream), "--seed-required")
        self.assertEqual(seeded.returncode, 0, seeded.stdout + seeded.stderr)
        self.assertIn("READ_ONLY: false", seeded.stdout)
        for path in required:
            self.assertTrue((root / path).is_file(), path)
            self.assertEqual((root / path).read_bytes(), (upstream / path).read_bytes())
        # An existing file is never replaced, and the upgrade now has what it needs — once the
        # seeds are committed: the rehearsal below audits what the project holds, not what lies
        # uncommitted on its disk.
        again = run_control(root, "template-upgrade", "--source", str(upstream), "--seed-required")
        self.assertEqual(again.returncode, 0, again.stdout + again.stderr)
        self.assertIn("nothing to seed", again.stdout)
        uncommitted = run_control(root, "template-upgrade", "--source", str(upstream))
        self.assertNotEqual(uncommitted.returncode, 0)
        self.assertIn("FAIL: UPGRADE_REHEARSAL", uncommitted.stdout)
        self.assertIn("MANDATORY_FILES", uncommitted.stdout)
        self.commit_fixture(root, "chore: seed the files 9.9.9 requires")
        applied = run_control(root, "template-upgrade", "--source", str(upstream), "--apply")
        self.assertEqual(applied.returncode, 0, applied.stdout + applied.stderr)
        self.assertIn("PASS: REQUIRED_FILES", applied.stdout)

    def test_a_proof_cannot_contradict_the_artifact_it_cites(self) -> None:
        """A proof that claims PASS while the output it cites ends on FAILED is the lie a real
        project produced: the controller checked the hash, the commit and the integration, and
        never read what the artifact said."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        item = self.create_and_start_lifecycle_work_item(root, "WI-001", "HD-102")
        self.switch_to_canonical(root)
        self.merge_fixture_branch(root, item["branch"], "fixture: integrate WI-001")
        lying = self.write_committed_evidence(root, "WI-001", artifacts={"tests": RED_TEST_OUTPUT})
        refused = self.close_with_evidence(root, "WI-001", lying)
        self.assertNotEqual(refused.returncode, 0)
        output = refused.stdout + refused.stderr
        self.assertIn("result is PASS but every text artifact it cites reports a failure", output)
        self.assertIn("FAILED (failures=1)", output, "the refusal quotes the line it read")
        self.assertEqual(
            load_json(root / "project_control/work-items/WI-001.json")["status"],
            "IN_PROGRESS",
            "a refused closure leaves the Work Item where it was",
        )
        # The same Work Item closes once its proof cites the run that actually passed. A failed
        # run is recorded as its own evidence; it does not become a success by rewriting.
        honest = self.write_committed_evidence(root, "WI-001", revision="-2")
        accepted = self.close_with_evidence(root, "WI-001", honest)
        self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)

    def test_a_proof_may_keep_the_run_that_failed_beside_the_one_that_passed(self) -> None:
        """The doctrine asks for the failed run to stay visible, explained, never hidden. A closure
        of a real project bundled ten pieces, one of them the log of a first run that failed on
        file locks and a second showing the same cases passing in isolation. Refusing that would
        punish exactly the honesty the doctrine demands: only a proof whose every readable piece
        reports a failure contradicts itself."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        item = self.create_and_start_lifecycle_work_item(root, "WI-001", "HD-102")
        self.switch_to_canonical(root)
        self.merge_fixture_branch(root, item["branch"], "fixture: integrate WI-001")
        bundled = self.write_committed_evidence(
            root, "WI-001", artifacts={"tests": [RED_TEST_OUTPUT, GREEN_TEST_OUTPUT]},
        )
        accepted = self.close_with_evidence(root, "WI-001", bundled)
        self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)
        self.assertEqual(load_json(root / "project_control/work-items/WI-001.json")["status"], "DONE")
        # The failed run is still there, byte for byte: nothing was cleaned up to make it pass.
        kept = (root / "reports/evidence/WI-001/tests-1.txt").read_text(encoding="utf-8")
        self.assertIn("FAILED (failures=1)", kept)

    def test_the_documented_models_are_the_text_the_controller_accepts(self) -> None:
        """A model that the product's own parser refuses is a manufacturing fault: it is copied
        verbatim, and the refusal then says the record is missing while it is there."""
        self.skip_unless_template("the models shipped with the template")
        decisions = (ROOT / "docs/governance/HUMAN_DECISIONS.md").read_text(encoding="utf-8")
        blocks = re.findall(r"(?ms)^```text\n(.*?)^```", decisions)
        self.assertGreaterEqual(len(blocks), 2, "the register documents a plain model and an out-of-folder one")
        for index, block in enumerate(blocks):
            recorded = block.replace("HD-NNN", "HD-001").replace("WI-NNN", "WI-001")
            self.assertEqual(
                self.control_module.human_decision_errors(recorded, "HD-001"), [],
                f"model {index + 1} of HUMAN_DECISIONS.md must be accepted as written",
            )
        registry = (ROOT / "docs/governance/WORKTREE_REGISTRY.md").read_text(encoding="utf-8")
        block = re.search(r"(?ms)^```text\n(.*?)^```", registry)
        self.assertIsNotNone(block, "the registry documents a model")
        entry = block.group(1).replace("WI-NNN", "WI-001")
        match = self.control_module.REGISTRY_ENTRY_PATTERN.search(entry)
        self.assertIsNotNone(match, "the model must carry the markers the controller looks for")
        self.assertEqual(match.group(1), "WI-001")
        fields = dict(
            line.split(": ", 1) for line in match.group(2).splitlines() if ": " in line
        )
        for key in ("WORK_ITEM_ID", "DISPLAY_REFERENCE", "BASE_HEAD", "START_HEAD",
                    "AUTHORIZED_SCOPE", "BRANCH", "STATUS", "CLOSE_CONDITION"):
            self.assertIn(key, fields, "the model must carry every field the controller reads")
        self.assertEqual(fields["WORK_ITEM_ID"], "WI-001")

    def test_the_refusals_name_the_format_they_expect(self) -> None:
        """Telling someone that what he just wrote is missing, without telling him what was
        expected, is what makes him conclude the tool is broken."""
        source = (ROOT / "scripts/project_control.py").read_text(encoding="utf-8")
        for expected in (
            "expected the Markdown heading",
            "expected the block",
            "must read exactly",
            "recorded_at must be a past ISO timestamp carrying a timezone",
        ):
            self.assertTrue(expected in source, f"a refusal must say: {expected}")
        first_start = (ROOT / "FIRST_START.md").read_text(encoding="utf-8")
        self.assertTrue("PROJECT_CONTROL_HOOK_OVERRIDE" in first_start,
                        "the document that asks for the commit must name the mandate that allows it")
        adoption = (ROOT / "ADOPTION.md").read_text(encoding="utf-8")
        self.assertTrue("FIRST_START.md" in adoption,
                        "the file called ADOPTION must point a new project to its own door")

    def test_an_idea_is_not_a_work_item_and_an_inherited_view_is_not_stale(self) -> None:
        """Two small honesty defects: a borrowed field label, and a copy told to regenerate a view
        that is not its own yet. Both are read on a copy of this tree, so the check belongs to the
        template: a derived project has no generated view to inherit yet."""
        self.skip_unless_template("the view a fresh copy inherits")
        temporary, root = self.make_copy()
        self.addCleanup(temporary.cleanup)
        payload = json.loads(run_control(root, "status", "--json").stdout)
        self.assertEqual(payload["mode"], "BOOTSTRAP_MODE")
        self.assertEqual(payload["roadmap_view"], "STALE", "the inherited view no longer matches this copy")
        printed = run_control(root, "status").stdout
        self.assertNotIn("périmée", printed)
        self.assertIn("pas encore la tienne", printed)
        recorded = self.add_idea(root, "on pourrait garder une trace des idées")
        self.assertEqual(recorded.returncode, 0, recorded.stdout + recorded.stderr)
        self.assertIn("IDEA_ID: ID-001", recorded.stdout)
        self.assertNotIn("WORK_ITEM_ID:", recorded.stdout)

    def test_the_checks_that_replay_the_template_skip_in_a_derived_project(self) -> None:
        """Four checks read the template's own roadmap, view or example. In a derived project
        those files are absent by design: the checks skip, they do not fail."""
        self.skip_unless_template("replaying the suite of the template")
        replayed = [
            "test_roadmap_view_is_generated_from_the_files_in_a_stable_sourced_form",
            "test_the_demo_states_the_exact_reach_of_the_proof_of_reading",
            "test_plain_style_adds_no_path_of_its_own_outside_the_technical_block",
            "test_the_view_never_claims_that_tests_passed",
        ]
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        derived = Path(temporary.name) / "project"
        (derived / "project_control").mkdir(parents=True)
        for directory in ("tests", "scripts"):
            shutil.copytree(ROOT / directory, derived / directory, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        state = load_json(ROOT / "project_control/project-state.v1.json")
        state["repository_role"] = "PROJECT"
        (derived / "project_control/project-state.v1.json").write_text(
            json.dumps(state, indent=2) + "\n", encoding="utf-8"
        )
        result = subprocess.run(
            [sys.executable, "-B", "-m", "unittest", *(f"test_template.GeneralProjectSkeletonTests.{name}" for name in replayed)],
            cwd=derived / "tests", check=False, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(f"OK (skipped={len(replayed)})", result.stderr, result.stdout + result.stderr)

    def test_authorities_baseline_exempts_agent_runs_recorded_before_the_proof_of_reading(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        # The adoption baseline is declared first, before this project's own Agent Runs: the
        # legacy exemption cannot cover what comes next.
        adoption = run_git(root, "rev-parse", "HEAD").stdout.strip()
        self.declare_legacy_baseline(root, adoption, "HD-105")
        # WI-001 lived under a controller without proof of reading: its Agent Run carries no
        # authorities_read and, once recorded, acknowledge-authorities can never repair it.
        item = self.create_and_start_lifecycle_work_item(root, "WI-001", "HD-102")
        self.switch_to_canonical(root)
        run_path = root / "project_control/agent-runs/RUN-WI-001-001.json"
        run = load_json(run_path)
        run.pop("authorities_read")
        run_path.write_text(json.dumps(run, indent=2) + "\n", encoding="utf-8")
        frozen = self.commit_fixture(root, "fixture: Agent Run recorded before the proof of reading")
        refused = run_control(root, "audit")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("Agent Run RUN-WI-001-001: authorities_read is required after the adoption baseline", refused.stdout)
        self.assertIn("exempt only through authorities_baseline", refused.stdout)
        self.assertNotIn("PASS: AUTHORITIES_BASELINE", refused.stdout.replace("PASS: AUTHORITIES_BASELINE — no authorities baseline declared", ""))
        repair = run_control(root, "acknowledge-authorities", "WI-001", "--authorities-digest", "0" * 64)
        self.assertNotEqual(repair.returncode, 0)
        # The declared baseline freezes the Agent Runs present at that commit; nothing is inferred.
        self.declare_authorities_baseline(root, frozen, "HD-107")
        exempt = [
            path for path in run_git(root, "ls-tree", "-r", "--name-only", frozen, "--", "project_control/agent-runs").stdout.splitlines()
            if path.endswith(".json")
        ]
        accepted = run_control(root, "audit")
        self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)
        self.assertIn(f"PASS: AUTHORITIES_BASELINE — {len(exempt)} Agent Run(s) exempt from authorities_read at {frozen}", accepted.stdout)
        payload = json.loads(run_control(root, "status", "--json").stdout)
        self.assertEqual(payload["authorities_baseline"], frozen)
        self.assertEqual(payload["legacy_baseline"], adoption)
        # The Work Item still in progress closes only after recording its own reading — which the
        # passing audit now allows — exactly the path of an upgrade Work Item.
        self.merge_fixture_branch(root, item["branch"], "fixture: integrate WI-001")
        evidence = self.write_committed_evidence(root, "WI-001")
        unread = self.close_with_evidence(root, "WI-001", evidence)
        self.assertNotEqual(unread.returncode, 0)
        self.assertIn("AUTHORITY_MANIFEST_AT_CLOSE", unread.stdout + unread.stderr)
        acknowledged = run_control(root, "acknowledge-authorities", "WI-001", "--authorities-digest", self.authorities_digest(root, "WI-001"))
        self.assertEqual(acknowledged.returncode, 0, acknowledged.stdout + acknowledged.stderr)
        closed = self.close_with_evidence(root, "WI-001", evidence)
        self.assertEqual(closed.returncode, 0, closed.stdout + closed.stderr)
        self.assertEqual(load_json(root / "project_control/work-items/WI-001.json")["status"], "DONE")
        # Forward: an Agent Run recorded after the baseline still needs its own proof of reading.
        self.create_and_start_lifecycle_work_item(root, "WI-002", "HD-103")
        self.switch_to_canonical(root)
        later_path = root / "project_control/agent-runs/RUN-WI-002-001.json"
        later = load_json(later_path)
        later.pop("authorities_read")
        later_path.write_text(json.dumps(later, indent=2) + "\n", encoding="utf-8")
        forward = run_control(root, "audit")
        self.assertNotEqual(forward.returncode, 0)
        self.assertIn("Agent Run RUN-WI-002-001: authorities_read is required after the adoption baseline", forward.stdout)
        self.assertNotIn("RUN-WI-001-001", forward.stdout)
        committed = json.loads(run_git(root, "show", "HEAD:project_control/agent-runs/RUN-WI-002-001.json").stdout)
        later_path.write_text(json.dumps(committed, indent=2) + "\n", encoding="utf-8")
        restored = run_control(root, "audit")
        self.assertEqual(restored.returncode, 0, restored.stdout + restored.stderr)
        # Declarations that cannot be trusted are refused nominatively, without a traceback or a write.
        state_path = root / "project_control/project-state.v1.json"
        state = load_json(state_path)
        unknown = "0123456789abcdef0123456789abcdef01234567"
        cases = (
            ("commit outside history", {"head": unknown, "human_decision_ref": "HD-107"},
             f"authorities baseline {unknown} is missing or not in current history"),
            ("unrecorded decision", {"head": frozen, "human_decision_ref": "HD-999"},
             "authorities baseline requires a recorded Human Decision: HD-999"),
            ("malformed head", {"head": "HEAD", "human_decision_ref": "HD-107"}, "pattern mismatch"),
            ("missing declaration", None, "missing authorities_baseline"),
        )
        for label, declared, message in cases:
            with self.subTest(label=label):
                state.pop("authorities_baseline", None)
                if declared is not None:
                    state["authorities_baseline"] = declared
                state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
                before = self.snapshot_repository(root)
                for command in (("audit",), ("status", "--json")):
                    bad = run_control(root, *command)
                    self.assertNotEqual(bad.returncode, 0, label)
                    output = bad.stdout + bad.stderr
                    self.assertNotIn("Traceback", output)
                    self.assertIn(message, output)
                self.assertEqual(self.snapshot_repository(root), before)
        state["authorities_baseline"] = {"head": frozen, "human_decision_ref": "HD-107"}
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        self.assertEqual(run_control(root, "audit").returncode, 0)
        # NOT_STARTED cannot declare a baseline at all (a fresh copy declares null).
        not_started = copy.deepcopy(state)
        not_started["initialization"] = {
            "status": "NOT_STARTED", "completion_human_decision_ref": None, "completed_at": None,
            "baseline_head": "UNKNOWN", "closeout_evidence": [],
        }
        not_started["legacy_baseline"] = None
        not_started["authorities_baseline"] = {"head": frozen, "human_decision_ref": "HD-107"}
        self.assertIn(
            "project-state: NOT_STARTED cannot declare an authorities_baseline",
            self.control_module.validate_project_state(not_started, "NOT_STARTED"),
        )

    def test_reporting_style_is_chosen_by_the_project_owner_and_shown_first_by_status(self) -> None:
        # A fresh copy has not asked the question yet: UNKNOWN is the only honest value there.
        temporary, root = self.make_copy()
        self.addCleanup(temporary.cleanup)
        state_path = root / "project_control/project-state.v1.json"
        self.assertEqual(load_json(state_path)["reporting_style"], "UNKNOWN")
        audit = run_control(root, "bootstrap-audit")
        self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)
        self.assertIn("PASS: REPORTING_STYLE — reporting_style=UNKNOWN", audit.stdout)
        self.assertIn("Retour au Project Owner : non choisi (UNKNOWN)", run_control(root, "status").stdout)
        # Initialization cannot close until the Project Owner has chosen.
        self.configure_ready_for_closeout(root, "WI-001")
        state = load_json(state_path)
        state["reporting_style"] = "UNKNOWN"
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        refused = run_control(root, "bootstrap-closeout", "--path", "FIRST_START.md", "--path", "project_control/project-state.v1.json")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("closeout requires the Project Owner's reporting_style (TECHNICAL or PLAIN)", refused.stdout)
        state["reporting_style"] = "PLAIN"
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        accepted = run_control(root, "bootstrap-closeout", "--path", "FIRST_START.md", "--path", "project_control/project-state.v1.json")
        self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)
        # An initialized project shows the choice first, in the owner's words, and in JSON.
        temporary2, normal = self.make_normal_copy()
        self.addCleanup(temporary2.cleanup)
        text = run_control(normal, "status").stdout.splitlines()
        self.assertTrue(text[1].startswith("Retour au Project Owner : technique (TECHNICAL)"), text[:3])
        self.assertEqual(json.loads(run_control(normal, "status", "--json").stdout)["reporting_style"], "TECHNICAL")
        normal_state_path = normal / "project_control/project-state.v1.json"
        normal_state = load_json(normal_state_path)
        normal_state["reporting_style"] = "PLAIN"
        normal_state_path.write_text(json.dumps(normal_state, indent=2) + "\n", encoding="utf-8")
        plain = run_control(normal, "status")
        self.assertEqual(plain.returncode, 0, plain.stdout + plain.stderr)
        self.assertIn("Retour au Project Owner : simple (PLAIN) — ce qui s'est passé, ce que ça change, ce qu'il doit faire", plain.stdout)
        # After COMPLETE, UNKNOWN, an unknown label or a missing field is refused nominatively —
        # the message a 3.6.x project meets after template-upgrade, before its Human Decision.
        for label, value, message in (
            ("not chosen", "UNKNOWN", "COMPLETE requires reporting_style TECHNICAL or PLAIN"),
            ("unknown label", "VERBOSE", "project-state.reporting_style: invalid enum value 'VERBOSE'"),
            ("missing field", None, "missing reporting_style"),
        ):
            with self.subTest(label=label):
                normal_state.pop("reporting_style", None)
                if value is not None:
                    normal_state["reporting_style"] = value
                normal_state_path.write_text(json.dumps(normal_state, indent=2) + "\n", encoding="utf-8")
                before = self.snapshot_repository(normal)
                for command in (("audit",), ("status", "--json")):
                    bad = run_control(normal, *command)
                    self.assertNotEqual(bad.returncode, 0, label)
                    output = bad.stdout + bad.stderr
                    self.assertNotIn("Traceback", output)
                    self.assertIn(message, output)
                self.assertEqual(self.snapshot_repository(normal), before)
        normal_state["reporting_style"] = "TECHNICAL"
        normal_state_path.write_text(json.dumps(normal_state, indent=2) + "\n", encoding="utf-8")
        self.assertEqual(run_control(normal, "audit").returncode, 0)

    # --- Roadmap view and ideas (P12, P6): computed from the files, never decided ---

    VIEW_MARKDOWN = "docs/governance/ROADMAP_VIEW.md"
    VIEW_HTML = "reports/roadmap/ROADMAP.html"

    def view_marker(self, root: Path, relative: str) -> dict[str, str]:
        text = (root / relative).read_text(encoding="utf-8")
        marker = re.match(r"<!-- ROADMAP_VIEW sources_digest=([0-9a-f]{64}) generated_at=(\S+) head=([0-9a-f]{40}) -->", text)
        self.assertIsNotNone(marker, text[:200])
        return {"sources_digest": marker.group(1), "generated_at": marker.group(2), "head": marker.group(3)}

    def add_idea(self, root: Path, quote: str, *extra: str) -> subprocess.CompletedProcess[str]:
        return run_control(root, "idea", "add", "--quote", quote, "--source", "discussion de test, 2026-09-08", *extra)

    def test_roadmap_view_is_generated_from_the_files_in_a_stable_sourced_form(self) -> None:
        self.skip_unless_template("the generated view of the template")
        # A fresh copy plays the template's role: its view comes from provenance/ and goes there.
        temporary, root = self.make_copy()
        self.addCleanup(temporary.cleanup)
        before = self.snapshot_repository(root)
        checked = run_control(root, "roadmap-view")
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        self.assertIn("READ_ONLY: true", checked.stdout)
        self.assertIn("nothing written", checked.stdout)
        self.assertEqual(self.snapshot_repository(root), before, "without --write nothing is written")
        modelled = run_control(root, "roadmap-view", "--json")
        self.assertEqual(modelled.returncode, 0, modelled.stdout + modelled.stderr)
        view = json.loads(modelled.stdout)
        self.assertEqual(view["role"], "PROJECT_TEMPLATE")
        self.assertEqual(view["style"], "PLAIN", "reporting_style UNKNOWN renders plainly")
        for section in ("now", "waiting_for_owner", "next_steps", "later", "ideas", "past", "stats", "versions"):
            self.assertIn(section, view, section)
        for entry in view["now"]:
            self.assertTrue(entry.get("source"), f"every line of Maintenant cites its source: {entry}")
        for entry in view["waiting_for_owner"] + view["next_steps"] + view["later"]:
            self.assertTrue(entry.get("source"), f"every planned line cites its source: {entry}")
        self.assertEqual(view["verification"]["head"], run_git(root, "rev-parse", "HEAD").stdout.strip())
        self.assertRegex(view["verification"]["sources_digest"], r"^[0-9a-f]{64}$")
        self.assertTrue(all(chantier.get("scope") is None or (root / chantier["scope"]).is_file() for chantier in view["chantiers"]),
                        "every chantier with a scope points to a file of the repository")
        # --write renders both forms in Bootstrap Mode without committing; status sees them.
        (root / "provenance/ROADMAP_VIEW.md").unlink()
        self.assertIn("Vue roadmap : absente", run_control(root, "status").stdout)
        written = run_control(root, "roadmap-view", "--write")
        self.assertEqual(written.returncode, 0, written.stdout + written.stderr)
        self.assertIn("written: provenance/roadmap/ROADMAP.html, provenance/ROADMAP_VIEW.md", written.stdout)
        self.assertEqual(run_git(root, "rev-parse", "HEAD").stdout.strip(), view["verification"]["head"], "Bootstrap Mode: no commit")
        marker = self.view_marker(root, "provenance/ROADMAP_VIEW.md")
        self.assertEqual(marker["sources_digest"], view["verification"]["sources_digest"])
        self.assertIn("Vue roadmap : à jour", run_control(root, "status").stdout)
        page = (root / "provenance/roadmap/ROADMAP.html").read_text(encoding="utf-8")
        markdown = (root / "provenance/ROADMAP_VIEW.md").read_text(encoding="utf-8")
        self.assertTrue(page.startswith("<!doctype html>"))
        for heading in ("Maintenant", "Ce qui t’attend", "Prochaines étapes", "Plus loin", "Tes idées, et ce qu’elles sont devenues", "Pour les techniciens"):
            self.assertIn(heading, page, heading)
            self.assertIn(heading, markdown, heading)
        head = view["verification"]["head"]
        plain_body = markdown.split("\n", 1)[1].split("## Pour les techniciens", 1)[0]
        self.assertNotIn(head, plain_body, "PLAIN keeps commits out of the reading; they stay in the marker and the technical fold")
        self.assertIn(head, markdown.split("## Pour les techniciens", 1)[1])
        # The forced technical style is one rendering; it does not change the project.
        technical = run_control(root, "roadmap-view", "--json", "--style", "TECHNICAL")
        self.assertEqual(technical.returncode, 0, technical.stdout + technical.stderr)
        self.assertEqual(json.loads(technical.stdout)["style"], "TECHNICAL")
        self.assertEqual(load_json(root / "provenance/roadmap-view.v1.json")["style"], load_json(ROOT / "provenance/roadmap-view.v1.json")["style"])
        # Invalid settings are an audit error; a stale view never is.
        settings_path = root / "provenance/roadmap-view.v1.json"
        settings = load_json(settings_path)
        settings["regeneration"] = "WEEKLY"
        settings_path.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
        refused = run_control(root, "bootstrap-audit")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("FAIL: ROADMAP_VIEW", refused.stdout)
        self.assertNotIn("Traceback", refused.stdout + refused.stderr)
        # Valid again, but genuinely different from what the committed view was generated from:
        # a real change of a source, not an incidental difference of formatting.
        settings["regeneration"] = "DAILY"
        settings["zoom"] = {"past": "EXPANDED", "far": "DETAIL"}
        settings_path.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
        stale = run_control(root, "bootstrap-audit")
        self.assertEqual(stale.returncode, 0, stale.stdout + stale.stderr)
        self.assertIn("PASS: ROADMAP_VIEW — settings valid (regeneration DAILY); generated view is stale", stale.stdout)
        self.assertIn("Vue roadmap : périmée", run_control(root, "status").stdout)

    def test_ideas_are_recorded_in_the_owners_words_in_two_synchronized_committed_forms(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        head = run_git(root, "rev-parse", "HEAD").stdout.strip()
        added = self.add_idea(root, "Un tableau de bord que tout le monde peut lire")
        self.assertEqual(added.returncode, 0, added.stdout + added.stderr)
        self.assertIn("ID-001", added.stdout)
        self.assertIn("committed on the canonical branch", added.stdout)
        new_head = run_git(root, "rev-parse", "HEAD").stdout.strip()
        self.assertNotEqual(new_head, head)
        self.assertEqual(run_git(root, "log", "-1", "--format=%s").stdout.strip(), "chore(project-control): idea ID-001 EVOKED")
        self.assertEqual(run_git(root, "status", "--porcelain=v1", "--untracked-files=all").stdout, "", "the commit leaves a clean worktree")
        committed_paths = run_git(root, "show", "--name-only", "--format=", "HEAD").stdout.split()
        self.assertEqual(sorted(committed_paths), ["docs/governance/IDEAS.md", "docs/governance/ideas-state.v1.json"])
        state = load_json(root / "docs/governance/ideas-state.v1.json")
        self.assertEqual([idea["idea_id"] for idea in state["ideas"]], ["ID-001"])
        self.assertEqual(state["ideas"][0]["quote"], "Un tableau de bord que tout le monde peut lire")
        self.assertEqual(state["ideas"][0]["state"], "EVOKED")
        ideas_md = (root / "docs/governance/IDEAS.md").read_text(encoding="utf-8")
        self.assertIn("| ID-001 |", ideas_md)
        self.assertIn("Status: `1 IDEA(S)`", ideas_md)
        self.assertEqual(run_control(root, "audit").returncode, 0)
        # The idea evolves; a target must exist; DISCARDED names the discarding decision.
        planned = run_control(root, "idea", "set", "ID-001", "--state", "PLANNED", "--target", "WI-000", "--note", "portée par le premier chantier")
        self.assertEqual(planned.returncode, 0, planned.stdout + planned.stderr)
        self.assertEqual(run_git(root, "log", "-1", "--format=%s").stdout.strip(), "chore(project-control): idea ID-001 PLANNED")
        before = self.snapshot_repository(root)
        unknown_target = run_control(root, "idea", "set", "ID-001", "--target", "WI-999")
        self.assertNotEqual(unknown_target.returncode, 0)
        self.assertIn("target WI-999 is not in the roadmap", unknown_target.stdout)
        undated = run_control(root, "idea", "set", "ID-001", "--state", "DISCARDED", "--target", "")
        self.assertNotEqual(undated.returncode, 0)
        self.assertIn("DISCARDED requires the target that names the discarding decision", undated.stdout)
        missing = run_control(root, "idea", "set", "ID-042", "--state", "LATER")
        self.assertNotEqual(missing.returncode, 0)
        self.assertIn("unknown idea: ID-042", missing.stdout)
        self.assertEqual(self.snapshot_repository(root), before, "a refused idea changes nothing")
        # Records live on the canonical branch: a work branch and a dirty worktree are refused.
        created = self.create_lifecycle_work_item(root, "WI-001", "HD-102")
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        started = self.start_command(root, "WI-001")
        self.assertEqual(started.returncode, 0, started.stdout + started.stderr)
        on_branch = self.snapshot_repository(root)
        refused = self.add_idea(root, "Une idée dite depuis une branche de travail")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("canonical branch divergence", refused.stdout)
        self.assertEqual(self.snapshot_repository(root), on_branch)
        self.switch_to_canonical(root)
        (root / "reports/scratch.txt").write_text("uncommitted\n", encoding="utf-8")
        dirty = self.add_idea(root, "Une idée sur un worktree sale")
        self.assertNotEqual(dirty.returncode, 0)
        self.assertIn("reports/scratch.txt", dirty.stdout, "the unexplained change is named, nothing is written")
        (root / "reports/scratch.txt").unlink()
        self.assertEqual(run_git(root, "status", "--porcelain=v1", "--untracked-files=all").stdout, "")
        # Both forms must agree: a hand-edited Markdown row is an audit error, fail-closed.
        ideas_path = root / "docs/governance/IDEAS.md"
        ideas_path.write_text(ideas_path.read_text(encoding="utf-8").replace("| PLANNED |", "| REALIZED |"), encoding="utf-8")
        desynchronized = run_control(root, "audit")
        self.assertNotEqual(desynchronized.returncode, 0)
        self.assertIn("FAIL: IDEAS — ID-001: state differs between Markdown and JSON", desynchronized.stdout)
        run_git(root, "restore", "--", "docs/governance/IDEAS.md")
        self.assertEqual(run_control(root, "audit").returncode, 0)
        # In Bootstrap Mode the idea is written with the initialization, not committed alone.
        temporary2, fresh = self.make_copy()
        self.addCleanup(temporary2.cleanup)
        fresh_head = run_git(fresh, "rev-parse", "HEAD").stdout.strip()
        written = self.add_idea(fresh, "Une idée dite pendant l’interview", "--stated-at", "2026-09-01")
        self.assertEqual(written.returncode, 0, written.stdout + written.stderr)
        self.assertIn("Bootstrap Mode: commit it with the initialization", written.stdout)
        self.assertEqual(run_git(fresh, "rev-parse", "HEAD").stdout.strip(), fresh_head)
        self.assertEqual(load_json(fresh / "docs/governance/ideas-state.v1.json")["ideas"][0]["stated_at"], "2026-09-01")
        self.assertEqual(run_control(fresh, "bootstrap-audit").returncode, 0)

    def test_roadmap_view_of_a_project_is_committed_by_project_control_only_when_its_sources_change(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        self.assertIn("Vue roadmap : absente", run_control(root, "status").stdout)
        head = run_git(root, "rev-parse", "HEAD").stdout.strip()
        written = run_control(root, "roadmap-view", "--write")
        self.assertEqual(written.returncode, 0, written.stdout + written.stderr)
        self.assertIn(f"written: {self.VIEW_HTML}, {self.VIEW_MARKDOWN}", written.stdout)
        self.assertIn(f"{self.VIEW_MARKDOWN} committed on main", written.stdout)
        first_view_head = run_git(root, "rev-parse", "HEAD").stdout.strip()
        self.assertNotEqual(first_view_head, head)
        self.assertEqual(run_git(root, "log", "-1", "--format=%s").stdout.strip(), "chore(project-control): roadmap view")
        self.assertEqual(run_git(root, "show", "--name-only", "--format=", "HEAD").stdout.split(), [self.VIEW_MARKDOWN])
        self.assertEqual(run_git(root, "status", "--porcelain=v1", "--untracked-files=all").stdout, "", "the page is ignored by Git")
        self.assertTrue((root / self.VIEW_HTML).is_file())
        self.assertEqual(self.view_marker(root, self.VIEW_MARKDOWN)["head"], head, "the view describes the state it was computed from")
        self.assertIn("Vue roadmap : à jour", run_control(root, "status").stdout)
        self.assertEqual(run_control(root, "audit").returncode, 0)
        # The project's view shows its own Work Items and nothing of the template's roadmap.
        view = json.loads(run_control(root, "roadmap-view", "--json").stdout)
        self.assertEqual(view["role"], "PROJECT")
        self.assertEqual(view["title"], "ROADMAP EXAMPLE PROJECT")
        self.assertEqual([item["work_item_id"] for item in view["work_items"]], ["WI-000"])
        self.assertEqual(view["chantiers"], [])
        self.assertEqual(view["style"], "TECHNICAL", "the settings follow the project's reporting style")
        markdown = (root / self.VIEW_MARKDOWN).read_text(encoding="utf-8")
        self.assertNotIn("P12", markdown)
        self.assertNotIn("provenance/roadmap-template", markdown)
        self.assertIn("WI-000", markdown)
        # Unchanged sources: nothing new is committed, the page is simply refreshed.
        again = run_control(root, "roadmap-view", "--write")
        self.assertEqual(again.returncode, 0, again.stdout + again.stderr)
        self.assertIn(f"{self.VIEW_MARKDOWN} unchanged: sources digest already current", again.stdout)
        self.assertEqual(run_git(root, "rev-parse", "HEAD").stdout.strip(), first_view_head)
        # A forced style renders the page only: the committed view keeps the project's style.
        forced = run_control(root, "roadmap-view", "--write", "--style", "PLAIN")
        self.assertEqual(forced.returncode, 0, forced.stdout + forced.stderr)
        self.assertIn("the committed view follows the project's reporting style", forced.stdout)
        self.assertEqual(run_git(root, "rev-parse", "HEAD").stdout.strip(), first_view_head)
        self.assertIn("Vue roadmap : à jour", run_control(root, "status").stdout)
        # A new idea changes the sources: the view is stale, then regenerated and committed.
        added = self.add_idea(root, "Une idée qui change la vue")
        self.assertEqual(added.returncode, 0, added.stdout + added.stderr)
        self.assertIn("Vue roadmap : périmée", run_control(root, "status").stdout)
        self.assertEqual(run_control(root, "audit").returncode, 0, "a stale view is never an audit error")
        regenerated = run_control(root, "roadmap-view", "--write")
        self.assertEqual(regenerated.returncode, 0, regenerated.stdout + regenerated.stderr)
        self.assertIn(f"{self.VIEW_MARKDOWN} committed on main", regenerated.stdout)
        self.assertIn("Une idée qui change la vue", (root / self.VIEW_MARKDOWN).read_text(encoding="utf-8"))
        self.assertIn("Vue roadmap : à jour", run_control(root, "status").stdout)
        # From a work branch the committed view is not rewritten: records live on the canonical branch.
        created = self.create_lifecycle_work_item(root, "WI-001", "HD-102")
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        started = self.start_command(root, "WI-001")
        self.assertEqual(started.returncode, 0, started.stdout + started.stderr)
        branch_head = run_git(root, "rev-parse", "HEAD").stdout.strip()
        refused = run_control(root, "roadmap-view", "--write")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("canonical branch divergence", refused.stdout)
        self.assertEqual(run_git(root, "rev-parse", "HEAD").stdout.strip(), branch_head)
        self.assertEqual(run_git(root, "status", "--porcelain=v1", "--untracked-files=all").stdout, "")
        # An explicit path is a plain write, on the caller's responsibility, never committed.
        explicit = run_control(root, "roadmap-view", "--markdown", "reports/roadmap/preview.md")
        self.assertEqual(explicit.returncode, 0, explicit.stdout + explicit.stderr)
        self.assertTrue((root / "reports/roadmap/preview.md").is_file())
        self.assertEqual(run_git(root, "rev-parse", "HEAD").stdout.strip(), branch_head)
        (root / "reports/roadmap/preview.md").unlink()

    # --- Double stop: a decision that leaves the granted folder needs two confirmations ---

    def test_out_of_folder_decision_requires_two_distinct_confirmations(self) -> None:
        validator = self.control_module.human_decision_errors
        base = (
            "## HD-201\n\nDate: 2026-09-07\nDecision: Adopt the skeleton core in another repository.\n"
            "Scope: core files\nReversible: YES\nRelated Work Item: NOT_APPLICABLE\n"
        )
        authorized = "Authorized by: Project Owner\n"
        cases = (
            ("inside the repository, nothing more required", base + authorized, []),
            ("explicit NOT_APPLICABLE scope", base + "Folder scope: NOT_APPLICABLE\n" + authorized, []),
            ("out of folder without confirmations", base + "Folder scope: /Users/owner/Projets/other-project\n" + authorized,
             ["requires Confirmation 1", "requires Confirmation 2"]),
            ("out of folder with one confirmation",
             base + "Folder scope: /Users/owner/Projets/other-project\nConfirmation 1: Oui, sur other-project, branche dédiée.\n" + authorized,
             ["requires Confirmation 2"]),
            ("two identical confirmations",
             base + "Folder scope: /Users/owner/Projets/other-project\nConfirmation 1: ok\nConfirmation 2: ok\n" + authorized,
             ["must be distinct human statements"]),
            ("UNKNOWN confirmation",
             base + "Folder scope: /Users/owner/Projets/other-project\nConfirmation 1: Oui, other-project.\nConfirmation 2: UNKNOWN\n" + authorized,
             ["requires Confirmation 2"]),
            ("UNKNOWN folder",
             base + "Folder scope: UNKNOWN\nConfirmation 1: Oui, other-project.\nConfirmation 2: Confirmé, other-project, copie seulement.\n" + authorized,
             ["must name the target folder"]),
            ("two distinct confirmations",
             base + "Folder scope: /Users/owner/Projets/other-project\nConfirmation 1: Oui, sur other-project, branche dédiée.\n"
             "Confirmation 2: Confirmé : other-project, branche wi-061, aucune intégration ni push.\n" + authorized,
             []),
        )
        for label, text, expected in cases:
            with self.subTest(label=label):
                errors = validator(text, "HD-201")
                self.assertEqual(len(errors), len(expected), (label, errors))
                for fragment in expected:
                    self.assertTrue(any(fragment in error for error in errors), (label, errors))
                self.assertEqual(self.control_module.human_decision_is_valid(text, "HD-201"), not expected)

    def test_work_item_backed_by_an_out_of_folder_decision_fails_preflight_until_confirmed(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        created = self.create_lifecycle_work_item(root, "WI-001", "HD-102")
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        decisions_path = root / "docs/governance/HUMAN_DECISIONS.md"
        original = decisions_path.read_text(encoding="utf-8")
        # The decision now claims to reach another folder without the two confirmations.
        amended = original.replace("Authorized by: Project Owner\n", "Folder scope: /Users/owner/Projets/other-project\nAuthorized by: Project Owner\n")
        self.assertNotEqual(amended, original)
        decisions_path.write_text(amended, encoding="utf-8")
        self.commit_fixture(root, "fixture: decision reaches another folder without confirmations")
        preflight = run_control(root, "preflight", "WI-001")
        self.assertNotEqual(preflight.returncode, 0)
        self.assertIn("FAIL: HUMAN_AUTHORIZATION", preflight.stdout)
        self.assertIn("HD-102: out-of-folder decision requires Confirmation 1", preflight.stdout)
        refused = self.start_command(root, "WI-001")
        self.assertNotEqual(refused.returncode, 0)
        self.assertEqual(run_git(root, "branch", "--show-current").stdout.strip(), "main")
        audit = run_control(root, "audit")
        self.assertNotEqual(audit.returncode, 0)
        self.assertIn("invalid Human Decision — HD-102: out-of-folder decision requires Confirmation 2", audit.stdout)
        # Two distinct recorded confirmations make the decision usable again.
        confirmed = amended.replace(
            "Folder scope: /Users/owner/Projets/other-project\n",
            "Folder scope: /Users/owner/Projets/other-project\n"
            "Confirmation 1: Oui, sur other-project, branche dédiée.\n"
            "Confirmation 2: Confirmé : other-project, aucune intégration ni push par l'agent.\n",
        )
        decisions_path.write_text(confirmed, encoding="utf-8")
        self.commit_fixture(root, "fixture: two distinct confirmations recorded")
        preflight = run_control(root, "preflight", "WI-001")
        self.assertIn("PASS: HUMAN_AUTHORIZATION — human_decision_refs=['HD-102']", preflight.stdout)
        started = self.start_command(root, "WI-001")
        self.assertEqual(started.returncode, 0, started.stdout + started.stderr)

    # --- Core manifest and template-upgrade (P2, étape 1b) ---

    CORE_MANIFEST = "provenance/core-manifest.v1.json"

    def make_template_source(self, version: str, mutate=None) -> Path:
        """A tree of the template, optionally altered, with its manifest regenerated at `version`."""
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        source = Path(temporary.name) / f"template-{version}"
        shutil.copytree(ROOT, source, ignore=fixture_copy_ignore())
        # The source is a template tree by definition, even when this suite runs inside a
        # derived project: only the template may regenerate a manifest.
        state_path = source / "project_control/project-state.v1.json"
        state = load_json(state_path)
        state["repository_role"] = "PROJECT_TEMPLATE"
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        if mutate is not None:
            mutate(source)
        written = run_control(source, "core-manifest", "--write", "--version", version)
        self.assertEqual(written.returncode, 0, written.stdout + written.stderr)
        return source

    def create_core_upgrade_work_item(self, root: Path, work_item_id: str = "WI-001", decision_id: str = "HD-102") -> str:
        created = run_control(
            root, "create-work-item", work_item_id, "--title", "Upgrade the skeleton core",
            "--objective", "Bring the core files to the current template version.",
            "--owner", "Project Owner", "--human-decision", decision_id,
            "--decision", f"Authorize {work_item_id}: core upgrade from the template.",
            "--authorized-by", "Project Owner",
            "--path", "CLAUDE.md", "--path", "FIRST_START.md", "--path", "ADOPTION.md",
            "--path", "scripts", "--path", "tests", "--path", "project_control/schemas",
            "--path", "project_control/README.md", "--path", "docs/governance/DEFINITION_OF_DONE.md",
            "--path", "docs/agent-governance/AGENTS.core.md", "--path", self.CORE_MANIFEST,
            "--conflict-gate", "INDEPENDENT", "--direct-impact", "core files",
            "--indirect-impact", "every agent session", "--authority-impact", "AGENTS.core.md",
            "--concurrent-work-impact", "NONE", "--code", "NOT_APPLICABLE",
            "--tests", "APPLICABLE", "--integration", "APPLICABLE",
            "--deployment", "NOT_APPLICABLE", "--runtime-proof", "NOT_APPLICABLE",
            "--runtime-target", "NOT_APPLICABLE", "--close-condition", "Template tests pass on the upgraded core.",
        )
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        started = self.start_command(root, work_item_id)
        self.assertEqual(started.returncode, 0, started.stdout + started.stderr)
        return run_git(root, "branch", "--show-current").stdout.strip()

    def test_core_manifest_describes_the_tree_and_the_decided_core_set(self) -> None:
        manifest = load_json(ROOT / self.CORE_MANIFEST)
        self.assertEqual(manifest["schema_version"], "1.0.0")
        self.assertRegex(manifest["skeleton_version"], r"^[0-9]+\.[0-9]+\.[0-9]+$")
        expected = self.control_module.core_files(ROOT)
        self.assertEqual(sorted(manifest["core"]), expected, "regenerate the manifest: core-manifest --write --version")
        for path, digest in manifest["core"].items():
            self.assertEqual(self.control_module.core_digest(ROOT, path), digest, path)
        # TPL-D-007: the decided core set, nothing more.
        self.assertTrue({"CLAUDE.md", "FIRST_START.md", "ADOPTION.md", "scripts/project_control.py",
                         "scripts/check_git_traceability.py", "scripts/hooks/pre-commit", "tests/test_template.py",
                         "project_control/README.md", "docs/governance/DEFINITION_OF_DONE.md",
                         "docs/agent-governance/AGENTS.core.md"} <= set(manifest["core"]))
        for outside in ("AGENTS.md", "README.md", "project_control/project-state.v1.json",
                        "docs/governance/HUMAN_DECISIONS.md", "provenance/CHANGELOG.md", "runtime_proof/README.md"):
            self.assertNotIn(outside, manifest["core"])
        checked = run_control(ROOT, "core-manifest")
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        self.assertIn("PASS: CORE_ALIGNED — tree matches the manifest", checked.stdout)

    def test_audit_requires_core_manifest_and_agents_core_reference(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        agents = root / "AGENTS.md"
        fixture = root / "tests/fixtures/project_control/agent-run.valid.json"
        manifest = root / self.CORE_MANIFEST
        originals = {path: path.read_bytes() for path in (agents, fixture, manifest)}
        reference = "`AGENTS_CORE: docs/agent-governance/AGENTS.core.md`"
        cases = (
            ("missing core file", fixture, None, "CORE_MANIFEST — core file missing: tests/fixtures/project_control/agent-run.valid.json"),
            ("no core reference", agents, originals[agents].replace(reference.encode(), b"(core reference removed)"), "must declare `AGENTS_CORE: docs/agent-governance/AGENTS.core.md` exactly once; found 0"),
            ("duplicate core reference", agents, originals[agents] + f"\n{reference}\n".encode(), "exactly once; found 2"),
            ("wrong core path", agents, originals[agents].replace(b"AGENTS.core.md`", b"OTHER.md`"), "declares AGENTS_CORE docs/agent-governance/OTHER.md; expected"),
            ("invalid manifest", manifest, b"{\"schema_version\": \"1.0.0\"}\n", "skeleton_version must be MAJOR.MINOR.PATCH"),
        )
        for label, path, content, message in cases:
            with self.subTest(label=label):
                if content is None:
                    path.unlink()
                else:
                    path.write_bytes(content)
                before = self.snapshot_repository(root)
                refused = run_control(root, "audit")
                self.assertNotEqual(refused.returncode, 0, label)
                self.assertIn(message, refused.stdout)
                self.assertNotIn("Traceback", refused.stdout + refused.stderr)
                self.assertEqual(self.snapshot_repository(root), before)
                path.write_bytes(originals[path])
        restored = run_control(root, "audit")
        self.assertEqual(restored.returncode, 0, restored.stdout + restored.stderr)
        self.assertIn("PASS: CORE_MANIFEST — skeleton_version", restored.stdout)

    def test_template_upgrade_reports_no_drift_on_a_fresh_copy_and_refuses_bootstrap_apply(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        manifest = load_json(ROOT / self.CORE_MANIFEST)
        version, core_count = manifest["skeleton_version"], len(manifest["core"])
        before = self.snapshot_repository(root)
        report = run_control(root, "template-upgrade", "--source", str(ROOT))
        self.assertEqual(report.returncode, 0, report.stdout + report.stderr)
        self.assertIn("READ_ONLY: true", report.stdout)
        self.assertIn(f"PASS: UPGRADE_PLAN — {version} -> {version}: identical {core_count}, updated [], added [], removed upstream [], modified locally []", report.stdout)
        self.assertIn("PASS: DRY_RUN — nothing written", report.stdout)
        self.assertEqual(self.snapshot_repository(root), before)
        status = json.loads(run_control(root, "status", "--json").stdout)
        self.assertEqual(status["skeleton_version"], version)
        self.assertEqual(status["core_drift"], {})
        self.assertIn(f"Squelette : {version} | core aligné", run_control(root, "status").stdout)
        # Bootstrap Mode never receives a core upgrade: a NOT_STARTED copy is simply re-copied.
        bootstrap_temporary, bootstrap_root = self.make_copy()
        self.addCleanup(bootstrap_temporary.cleanup)
        before = self.snapshot_repository(bootstrap_root)
        refused = run_control(bootstrap_root, "template-upgrade", "--source", str(ROOT), "--apply")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("FAIL: APPLY — template-upgrade --apply requires NORMAL_MODE", refused.stdout)
        self.assertEqual(self.snapshot_repository(bootstrap_root), before)

    def test_template_upgrade_updates_intact_core_refuses_modified_files_and_never_touches_records(self) -> None:
        def next_version(source: Path) -> None:
            readme = source / "project_control/README.md"
            readme.write_text(readme.read_text(encoding="utf-8") + "\nUpstream addition for the upgrade test.\n", encoding="utf-8")
            (source / "tests/fixtures/project_control/extra.valid.json").write_text("{}\n", encoding="utf-8")
            (source / "ADOPTION.md").unlink()

        upstream = self.make_template_source("9.9.9", next_version)
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        self.create_core_upgrade_work_item(root)
        records_before = self.lifecycle_snapshot(root)[0]
        before = self.snapshot_repository(root)
        report = run_control(root, "template-upgrade", "--source", str(upstream))
        self.assertEqual(report.returncode, 0, report.stdout + report.stderr)
        self.assertIn("updated ['project_control/README.md'], added ['tests/fixtures/project_control/extra.valid.json'], removed upstream ['ADOPTION.md'], modified locally []", report.stdout)
        self.assertEqual(self.snapshot_repository(root), before, "a dry run writes nothing")
        applied = run_control(root, "template-upgrade", "--source", str(upstream), "--apply")
        self.assertEqual(applied.returncode, 0, applied.stdout + applied.stderr)
        self.assertIn("READ_ONLY: false", applied.stdout)
        self.assertIn("PASS: APPLY — 2 core file(s) written, manifest now 9.9.9; removed upstream and left in place for a human decision: ['ADOPTION.md']", applied.stdout)
        self.assertEqual((root / "project_control/README.md").read_bytes(), (upstream / "project_control/README.md").read_bytes())
        self.assertEqual((root / "tests/fixtures/project_control/extra.valid.json").read_text(encoding="utf-8"), "{}\n")
        self.assertTrue((root / "ADOPTION.md").is_file(), "removed upstream is reported, never deleted")
        self.assertEqual((root / self.CORE_MANIFEST).read_bytes(), (upstream / self.CORE_MANIFEST).read_bytes())
        self.assertTrue(os.access(root / "scripts/hooks/pre-commit", os.X_OK))
        self.assertIn("INITIALIZATION_STATUS: COMPLETE", (root / "FIRST_START.md").read_text(encoding="utf-8"),
                      "the project's initialization marker survives the upgrade")
        self.assertEqual(self.lifecycle_snapshot(root)[0], records_before, "records are never touched")
        status = json.loads(run_control(root, "status", "--json").stdout)
        self.assertEqual(status["skeleton_version"], "9.9.9")
        self.assertEqual(status["core_drift"], {})
        staged = run_git(root, "add", "--", "tests/fixtures/project_control/extra.valid.json")
        self.assertEqual(staged.returncode, 0, staged.stdout + staged.stderr)
        preflight = run_control(root, "preflight", "WI-001", "--path", "project_control/README.md",
                                "--path", "tests/fixtures/project_control/extra.valid.json", "--path", self.CORE_MANIFEST)
        self.assertEqual(preflight.returncode, 0, preflight.stdout + preflight.stderr)
        self.commit_fixture(root, "fixture: upgrade core to 9.9.9")
        audit = run_control(root, "audit")
        self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)
        # A locally modified core file is refused and listed; nothing is written without --overwrite.
        definition = root / "docs/governance/DEFINITION_OF_DONE.md"
        definition.write_text(definition.read_text(encoding="utf-8") + "\nLocal deviation.\n", encoding="utf-8")
        self.commit_fixture(root, "fixture: local deviation on a core file")
        self.assertEqual(json.loads(run_control(root, "status", "--json").stdout)["core_drift"],
                         {"docs/governance/DEFINITION_OF_DONE.md": "MODIFIED_LOCALLY"})

        def patch_version(source: Path) -> None:
            next_version(source)
            upstream_definition = source / "docs/governance/DEFINITION_OF_DONE.md"
            upstream_definition.write_text(upstream_definition.read_text(encoding="utf-8") + "\nUpstream clarification.\n", encoding="utf-8")

        patched = self.make_template_source("9.9.10", patch_version)
        before = self.snapshot_repository(root)
        refused = run_control(root, "template-upgrade", "--source", str(patched), "--apply")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("FAIL: LOCAL_CORE_INTACT — modified locally, refused without --overwrite: ['docs/governance/DEFINITION_OF_DONE.md']", refused.stdout)
        self.assertIn("FAIL: APPLY — refused", refused.stdout)
        self.assertEqual(self.snapshot_repository(root), before)
        unmatched = run_control(root, "template-upgrade", "--source", str(patched), "--overwrite", "CLAUDE.md")
        self.assertNotEqual(unmatched.returncode, 0)
        self.assertIn("--overwrite names no protected file: ['CLAUDE.md']", unmatched.stdout)
        overwritten = run_control(root, "template-upgrade", "--source", str(patched), "--apply",
                                  "--overwrite", "docs/governance/DEFINITION_OF_DONE.md")
        self.assertEqual(overwritten.returncode, 0, overwritten.stdout + overwritten.stderr)
        self.assertEqual(definition.read_bytes(), (patched / "docs/governance/DEFINITION_OF_DONE.md").read_bytes())
        self.assertEqual(json.loads(run_control(root, "status", "--json").stdout)["skeleton_version"], "9.9.10")
        self.commit_fixture(root, "fixture: upgrade core to 9.9.10")
        # A downgrade is not an upgrade.
        downgrade = run_control(root, "template-upgrade", "--source", str(upstream))
        self.assertNotEqual(downgrade.returncode, 0)
        self.assertIn("FAIL: UPGRADE_DIRECTION — source 9.9.9 is older than the project's 9.9.10", downgrade.stdout)
        # A source whose own core is not intact is refused.
        (patched / "CLAUDE.md").write_text("tampered\n", encoding="utf-8")
        tampered = run_control(root, "template-upgrade", "--source", str(patched))
        self.assertNotEqual(tampered.returncode, 0)
        self.assertIn("FAIL: SOURCE_MANIFEST — source core is not intact: {'CLAUDE.md': 'MODIFIED_LOCALLY'}", tampered.stdout)

    def test_core_manifest_write_is_reserved_to_the_template(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        before = self.snapshot_repository(root)
        refused = run_control(root, "core-manifest", "--write", "--version", "1.0.0")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("reserved to the template", refused.stdout + refused.stderr)
        self.assertNotIn("Traceback", refused.stdout + refused.stderr)
        self.assertEqual(self.snapshot_repository(root), before)
        checked = run_control(root, "core-manifest")
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        self.assertIn("PASS: CORE_ALIGNED", checked.stdout)

    def install_commit_hook(self, root: Path) -> None:
        """Install the gate the way a project does: a copy outside the worktree."""
        installed = run_control(root, "install-gate")
        self.assertEqual(installed.returncode, 0, installed.stdout + installed.stderr)
        state = json.loads(run_control(root, "status", "--json").stdout)["hooks"]
        self.assertEqual(state, "INSTALLED", installed.stdout)

    def record_plain_human_decision(self, root: Path, reference: str, body: str) -> None:
        """A Human Decision written by hand, as Project Control documents it."""
        path = root / "docs/governance/HUMAN_DECISIONS.md"
        path.write_text(path.read_text(encoding="utf-8").rstrip() + f"\n\n## {reference}\n\n" + body, encoding="utf-8")
        self.commit_fixture(root, f"fixture: record {reference}")

    def create_simple_work_item(self, root: Path, work_item_id: str, decision: str, path: str):
        return run_control(
            root, "create-work-item", work_item_id, "--title", f"Fixture {work_item_id}",
            "--objective", "Exercise one authorization rule.", "--owner", "Project Owner",
            "--human-decision", decision, "--branch", f"work/{work_item_id.lower()}", "--path", path,
            "--conflict-gate", "INDEPENDENT", "--direct-impact", path, "--indirect-impact", "none",
            "--authority-impact", "NONE", "--concurrent-work-impact", "NONE",
            "--code", "APPLICABLE", "--tests", "NOT_APPLICABLE", "--integration", "APPLICABLE",
            "--deployment", "NOT_APPLICABLE", "--runtime-proof", "NOT_APPLICABLE",
            "--runtime-target", "NOT_APPLICABLE", "--close-condition", "Integrated.",
        )

    def test_hook_gates_bootstrap_commits_and_needs_a_mandate_for_core_paths(self) -> None:
        temporary, root = self.make_copy()
        self.addCleanup(temporary.cleanup)
        self.install_commit_hook(root)
        (root / "docs/governance/PROJECT_CHARTER.md").write_text("# Charter\n\nStatus: `DRAFT`\n", encoding="utf-8")
        staged = run_git(root, "add", "--", "docs/governance/PROJECT_CHARTER.md")
        self.assertEqual(staged.returncode, 0, staged.stdout + staged.stderr)
        allowed = run_git(root, "commit", "-q", "-m", "init: charter draft")
        self.assertEqual(allowed.returncode, 0, allowed.stdout + allowed.stderr)
        (root / "scripts/extra.py").write_text("VALUE = 1\n", encoding="utf-8")
        staged = run_git(root, "add", "--", "scripts/extra.py")
        self.assertEqual(staged.returncode, 0, staged.stdout + staged.stderr)
        head_before = run_git(root, "rev-parse", "HEAD").stdout
        refused = run_git(root, "commit", "-q", "-m", "core change without mandate")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("BOOTSTRAP_CHANGE_SCOPE", refused.stdout + refused.stderr)
        self.assertEqual(run_git(root, "rev-parse", "HEAD").stdout, head_before)
        overridden = run_git(
            root, "commit", "-q", "-m", "core change under explicit mandate",
            env={"PROJECT_CONTROL_HOOK_OVERRIDE": "mandat de maintenance du template"},
        )
        self.assertEqual(overridden.returncode, 0, overridden.stdout + overridden.stderr)
        self.assertIn("HOOK_OVERRIDE", overridden.stdout + overridden.stderr)
        self.assertNotEqual(run_git(root, "rev-parse", "HEAD").stdout, head_before)

    def test_the_gate_is_installed_where_git_will_look_even_in_a_linked_worktree(self) -> None:
        """A linked worktree has a Git directory of its own, but Git reads hooks from the common
        one. Installing into the worktree's own directory wrote a gate nobody would ever run and
        reported success — and the commit the control refused entered history all the same. A
        protection that lies about its own presence is worse than an absent one."""
        temporary, root = self.make_copy()
        self.addCleanup(temporary.cleanup)
        linked = root.parent / "linked-worktree"
        added = run_git(root, "worktree", "add", "--quiet", str(linked), "-b", "work/linked")
        self.assertEqual(added.returncode, 0, added.stdout + added.stderr)
        installed = run_control(linked, "install-gate")
        self.assertEqual(installed.returncode, 0, installed.stdout + installed.stderr)
        # Git itself says which file it will run; the gate has to be that file.
        executed = run_git(linked, "rev-parse", "--git-path", "hooks/pre-commit")
        self.assertEqual(executed.returncode, 0, executed.stdout + executed.stderr)
        target = Path(executed.stdout.strip())
        if not target.is_absolute():
            target = linked / target
        self.assertTrue(target.is_file(), f"Git runs {target}; the gate was installed elsewhere")
        self.assertEqual(json.loads(run_control(linked, "status", "--json").stdout)["hooks"], "INSTALLED")
        # And it really runs: a core path without a mandate is refused, HEAD does not move.
        (linked / "scripts/extra.py").write_text("VALUE = 1\n", encoding="utf-8")
        staged = run_git(linked, "add", "--", "scripts/extra.py")
        self.assertEqual(staged.returncode, 0, staged.stdout + staged.stderr)
        head_before = run_git(linked, "rev-parse", "HEAD").stdout
        refused = run_git(linked, "commit", "-q", "-m", "core change from a linked worktree")
        self.assertNotEqual(refused.returncode, 0, "the gate must run in a linked worktree too")
        self.assertEqual(run_git(linked, "rev-parse", "HEAD").stdout, head_before)

    def test_a_commit_is_refused_when_the_staged_state_cannot_be_read(self) -> None:
        """The gate audits the tree the commit would create by materialising the index. When that
        could not be done it fell back on the working tree and announced PASS: a guarantee that
        cancels itself the moment it is inconvenienced, on exactly the state it could not read.
        Fail closed — with the mandated door left open for an environment that cannot make a
        temporary checkout."""
        temporary, root = self.make_copy()
        self.addCleanup(temporary.cleanup)
        self.install_commit_hook(root)
        (root / "docs/governance/PROJECT_CHARTER.md").write_text("# Charter\n\nStatus: `DRAFT`\n", encoding="utf-8")
        staged = run_git(root, "add", "--", "docs/governance/PROJECT_CHARTER.md")
        self.assertEqual(staged.returncode, 0, staged.stdout + staged.stderr)
        # Make the temporary checkout impossible without touching the gate or the controller.
        common = run_git(root, "rev-parse", "--git-common-dir")
        self.assertEqual(common.returncode, 0, common.stdout + common.stderr)
        git_dir = Path(common.stdout.strip())
        if not git_dir.is_absolute():
            git_dir = root / git_dir
        (git_dir / "worktrees").write_text("not a directory\n", encoding="utf-8")
        head_before = run_git(root, "rev-parse", "HEAD").stdout
        refused = run_git(root, "commit", "-q", "-m", "charter draft while the staged state is unreadable")
        self.assertNotEqual(refused.returncode, 0, "what cannot be read is refused, not waved through")
        self.assertIn("STAGED_STATE_AUDITED", refused.stdout + refused.stderr)
        self.assertEqual(run_git(root, "rev-parse", "HEAD").stdout, head_before)
        # The mandated door still opens, and says so in the transcript.
        overridden = run_git(
            root, "commit", "-q", "-m", "charter draft under explicit mandate",
            env={"PROJECT_CONTROL_HOOK_OVERRIDE": "environnement sans checkout temporaire"},
        )
        self.assertEqual(overridden.returncode, 0, overridden.stdout + overridden.stderr)
        self.assertIn("HOOK_OVERRIDE", overridden.stdout + overridden.stderr)
        self.assertNotEqual(run_git(root, "rev-parse", "HEAD").stdout, head_before)

    def test_hook_protects_canonical_branch_and_enforces_work_item_scope(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        self.install_commit_hook(root)
        status = run_control(root, "status", "--json")
        self.assertEqual(status.returncode, 0, status.stdout + status.stderr)
        self.assertEqual(json.loads(status.stdout)["hooks"], "INSTALLED")

        business = root / "modules/example.py"
        business.write_text("VALUE = 'unauthorized'\n", encoding="utf-8")
        staged = run_git(root, "add", "--", "modules/example.py")
        self.assertEqual(staged.returncode, 0, staged.stdout + staged.stderr)
        head_before = run_git(root, "rev-parse", "HEAD").stdout
        refused = run_git(root, "commit", "-q", "-m", "development on canonical")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("CANONICAL_BRANCH_PROTECTED", refused.stdout + refused.stderr)
        self.assertEqual(run_git(root, "rev-parse", "HEAD").stdout, head_before)
        unstaged = run_git(root, "reset", "-q", "--", "modules/example.py")
        self.assertEqual(unstaged.returncode, 0, unstaged.stdout + unstaged.stderr)
        business.unlink()

        (root / "reports/note.md").write_text("administrative note\n", encoding="utf-8")
        staged = run_git(root, "add", "--", "reports/note.md")
        self.assertEqual(staged.returncode, 0, staged.stdout + staged.stderr)
        allowed = run_git(root, "commit", "-q", "-m", "report on canonical")
        self.assertEqual(allowed.returncode, 0, allowed.stdout + allowed.stderr)

        self.create_and_start_lifecycle_work_item(
            root, "WI-001", "HD-102", authorized_path="modules/example.py", code="APPLICABLE",
        )
        outside = root / "modules/outside.py"
        outside.write_text("VALUE = 'outside'\n", encoding="utf-8")
        staged = run_git(root, "add", "--", "modules/outside.py")
        self.assertEqual(staged.returncode, 0, staged.stdout + staged.stderr)
        head_before = run_git(root, "rev-parse", "HEAD").stdout
        refused = run_git(root, "commit", "-q", "-m", "outside the Work Item scope")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("BUSINESS_CHANGE_AUTHORIZATION", refused.stdout + refused.stderr)
        self.assertEqual(run_git(root, "rev-parse", "HEAD").stdout, head_before)
        unstaged = run_git(root, "reset", "-q", "--", "modules/outside.py")
        self.assertEqual(unstaged.returncode, 0, unstaged.stdout + unstaged.stderr)
        outside.unlink()

        business.write_text("VALUE = 'authorized'\n", encoding="utf-8")
        stage_explicit_files(root)
        allowed = run_git(root, "commit", "-q", "-m", "authorized change with its records")
        self.assertEqual(allowed.returncode, 0, allowed.stdout + allowed.stderr)
        gate = run_control(root, "pre-commit")
        self.assertEqual(gate.returncode, 0, gate.stdout + gate.stderr)
        self.assertIn("READ_ONLY: true", gate.stdout)

    # --- Portée d'un Work Item : renommages, gate de commit, gate absente (revue 3.9.0) ---

    def test_a_rename_out_of_the_authorized_scope_is_refused(self) -> None:
        """A rename removes its origin: authorizing the destination never authorizes that removal."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        self.install_commit_hook(root)
        self.create_and_start_lifecycle_work_item(
            root, "WI-001", "HD-102", authorized_path="modules/allowed", code="APPLICABLE",
        )
        (root / "modules/allowed").mkdir(parents=True, exist_ok=True)
        moved = run_git(root, "mv", "--", "templates/README.md", "modules/allowed/README.md")
        self.assertEqual(moved.returncode, 0, moved.stdout + moved.stderr)

        refused = run_control(root, "preflight", "WI-001")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("path outside Work Item authorization: templates/README.md", refused.stdout)
        head_before = run_git(root, "rev-parse", "HEAD").stdout
        blocked = run_git(root, "commit", "-q", "-m", "rename out of the authorized scope")
        self.assertNotEqual(blocked.returncode, 0)
        self.assertIn("templates/README.md", blocked.stdout + blocked.stderr)
        self.assertEqual(run_git(root, "rev-parse", "HEAD").stdout, head_before)
        self.assertTrue((root / "modules/allowed/README.md").exists())

        traceability = subprocess.run(
            [sys.executable, "-B", "scripts/check_git_traceability.py", "--json"],
            cwd=root, check=False, capture_output=True, text=True,
        )
        classified = {entry["path"] for entry in json.loads(traceability.stdout)["paths"]}
        self.assertIn("templates/README.md", classified)
        self.assertIn("modules/allowed/README.md", classified)

    def test_commit_gate_applies_the_work_item_scope_to_every_staged_path(self) -> None:
        """The gate refuses what the preflight refuses, inside the business roots or outside them."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        self.install_commit_hook(root)
        self.create_and_start_lifecycle_work_item(
            root, "WI-001", "HD-102", authorized_path="modules/allowed", code="APPLICABLE",
        )
        (root / "scripts/project_extra.py").write_text("VALUE = 1\n", encoding="utf-8")
        staged = run_git(root, "add", "--", "scripts/project_extra.py")
        self.assertEqual(staged.returncode, 0, staged.stdout + staged.stderr)
        refused = run_control(root, "preflight", "WI-001")
        self.assertNotEqual(refused.returncode, 0)
        head_before = run_git(root, "rev-parse", "HEAD").stdout
        blocked = run_git(root, "commit", "-q", "-m", "outside the scope and outside modules/")
        self.assertNotEqual(blocked.returncode, 0)
        output = blocked.stdout + blocked.stderr
        self.assertIn("WORK_BRANCH_AUTHORIZED_PATHS", output)
        self.assertIn("path outside Work Item authorization: scripts/project_extra.py", output)
        self.assertEqual(run_git(root, "rev-parse", "HEAD").stdout, head_before)
        unstaged = run_git(root, "reset", "-q", "--", "scripts/project_extra.py")
        self.assertEqual(unstaged.returncode, 0, unstaged.stdout + unstaged.stderr)
        (root / "scripts/project_extra.py").unlink()

        (root / "modules/allowed").mkdir(parents=True, exist_ok=True)
        (root / "modules/allowed/feature.py").write_text("VALUE = 'authorized'\n", encoding="utf-8")
        staged = run_git(root, "add", "--", "modules/allowed/feature.py")
        self.assertEqual(staged.returncode, 0, staged.stdout + staged.stderr)
        allowed = run_git(root, "commit", "-q", "-m", "authorized change inside the scope")
        self.assertEqual(allowed.returncode, 0, allowed.stdout + allowed.stderr)

    def test_the_gate_survives_the_removal_of_its_versioned_reference(self) -> None:
        """Installed outside the worktree, the gate is not part of what a commit writes."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        self.install_commit_hook(root)
        self.create_and_start_lifecycle_work_item(
            root, "WI-001", "HD-102", authorized_path="modules/allowed", code="APPLICABLE",
        )
        (root / "modules/allowed").mkdir(parents=True, exist_ok=True)
        moved = run_git(root, "mv", "--", "scripts/hooks/pre-commit", "modules/allowed/pre-commit")
        self.assertEqual(moved.returncode, 0, moved.stdout + moved.stderr)
        head_before = run_git(root, "rev-parse", "HEAD").stdout
        blocked = run_git(root, "commit", "-q", "-m", "carry the gate away")
        self.assertNotEqual(blocked.returncode, 0, "the installed copy still runs and refuses")
        self.assertEqual(run_git(root, "rev-parse", "HEAD").stdout, head_before)
        restored = run_git(root, "mv", "--", "modules/allowed/pre-commit", "scripts/hooks/pre-commit")
        self.assertEqual(restored.returncode, 0, restored.stdout + restored.stderr)

        # An installed copy that no longer matches its reference is an audit failure.
        installed = root / ".git/hooks/pre-commit"
        installed.write_text(installed.read_text(encoding="utf-8") + "\n# altered\n", encoding="utf-8")
        self.assertEqual(json.loads(run_control(root, "status", "--json").stdout)["hooks"], "MISMATCH")
        audit = run_control(root, "audit")
        self.assertNotEqual(audit.returncode, 0)
        self.assertIn("COMMIT_GATE", audit.stdout)

        # The historical in-tree mode still works and is reported as such.
        installed.unlink()
        configured = run_git(root, "config", "core.hooksPath", "scripts/hooks")
        self.assertEqual(configured.returncode, 0, configured.stdout + configured.stderr)
        self.assertEqual(json.loads(run_control(root, "status", "--json").stdout)["hooks"], "IN_TREE")

    def test_a_decision_that_records_a_refusal_authorizes_nothing(self) -> None:
        """`Chosen option: REJECT` is the trace of a refusal, never an authorization."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        self.record_plain_human_decision(root, "HD-201", (
            "Date: 2026-09-09\nDecision: Fixture decision, refused.\nChosen option: REJECT\n"
            "Related Work Item: WI-001\nFolder scope: NOT_APPLICABLE\nAuthorized by: Project Owner\n"
        ))
        refused = self.create_simple_work_item(root, "WI-001", "HD-201", "modules/allowed")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("Chosen option is not AUTHORIZE", refused.stdout)
        self.assertFalse((root / "project_control/work-items/WI-001.json").exists())

    def test_an_empty_field_is_an_absent_value_not_the_next_line(self) -> None:
        """A value is read on the line of its own field; an empty field authorizes nothing."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        self.record_plain_human_decision(root, "HD-202", (
            "Date: 2026-09-09\nDecision:\nContext: the decision line above is empty.\n"
            "Chosen option: AUTHORIZE\nRelated Work Item: WI-001\nFolder scope: NOT_APPLICABLE\n"
            "Authorized by: Project Owner\n"
        ))
        refused = self.create_simple_work_item(root, "WI-001", "HD-202", "modules/allowed")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("Decision is missing or UNKNOWN", refused.stdout)

        self.record_plain_human_decision(root, "HD-203", (
            "Date: 2026-09-09\nDecision: Fixture decision leaving the granted folder.\n"
            "Chosen option: AUTHORIZE\nRelated Work Item: WI-002\nFolder scope: /fixture/elsewhere\n"
            "Confirmation 1:\nConfirmation 2:\nAuthorized by: Project Owner\n"
        ))
        out_of_folder = self.create_simple_work_item(root, "WI-002", "HD-203", "modules/allowed")
        self.assertNotEqual(out_of_folder.returncode, 0)
        self.assertIn("out-of-folder decision requires Confirmation 1", out_of_folder.stdout)
        self.assertIn("out-of-folder decision requires Confirmation 2", out_of_folder.stdout)

    def test_a_symlink_staged_then_hidden_in_the_worktree_is_still_refused(self) -> None:
        """The control reads the index too: what the commit carries is what is checked."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        self.install_commit_hook(root)
        self.create_and_start_lifecycle_work_item(
            root, "WI-001", "HD-102", authorized_path="modules/allowed", code="APPLICABLE",
        )
        directory = root / "modules/allowed"
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "target.txt").write_text("target\n", encoding="utf-8")
        os.symlink("target.txt", directory / "link.txt")
        staged = run_git(root, "add", "--", "modules/allowed/target.txt", "modules/allowed/link.txt")
        self.assertEqual(staged.returncode, 0, staged.stdout + staged.stderr)
        self.assertNotEqual(run_control(root, "preflight", "WI-001").returncode, 0)

        (directory / "link.txt").unlink()
        (directory / "link.txt").write_text("an ordinary file now\n", encoding="utf-8")
        hidden = run_control(root, "preflight", "WI-001")
        self.assertNotEqual(hidden.returncode, 0, "a symlink kept in the index is still a symlink")
        self.assertIn("staged but not in the worktree", hidden.stdout)
        head_before = run_git(root, "rev-parse", "HEAD").stdout
        blocked = run_git(root, "commit", "-q", "-m", "hidden symlink")
        self.assertNotEqual(blocked.returncode, 0)
        self.assertEqual(run_git(root, "rev-parse", "HEAD").stdout, head_before)

    def test_authorizing_a_parent_folder_requires_the_authorities_of_its_children(self) -> None:
        """The duty to read covers every scope the authorization can write into."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        self.record_plain_human_decision(root, "HD-204", (
            "Date: 2026-09-09\nDecision: Fixture authorization on the docs tree.\n"
            "Chosen option: AUTHORIZE\nRelated Work Item: WI-001\nFolder scope: NOT_APPLICABLE\n"
            "Authorized by: Project Owner\n"
        ))
        created = self.create_simple_work_item(root, "WI-001", "HD-204", "docs")
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        required = run_control(root, "context-manifest", "WI-001")
        self.assertEqual(required.returncode, 0, required.stdout + required.stderr)
        for authority in (
            "docs/architecture/PROJECT_ARCHITECTURE_MAP.md",
            "docs/architecture/INITIAL_ARCHITECTURE.md",
            "docs/agent-governance/AGENTS.core.md",
        ):
            self.assertIn(authority, required.stdout, "a child scope of docs/ must be routed")
        widened = run_control(root, "context-manifest", "WI-001", "--scope", "architecture", "--scope", "governance")
        self.assertEqual(required.stdout.count("AUTHORITY:"), widened.stdout.count("AUTHORITY:"))

    def test_removing_the_commit_gate_cannot_stay_unnoticed(self) -> None:
        """Legacy in-tree mode: the gate cannot refuse its own removal — the next control does."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        configured = run_git(root, "config", "core.hooksPath", "scripts/hooks")
        self.assertEqual(configured.returncode, 0, configured.stdout + configured.stderr)
        self.create_and_start_lifecycle_work_item(
            root, "WI-001", "HD-102", authorized_path="modules/allowed", code="APPLICABLE",
        )
        (root / "modules/allowed").mkdir(parents=True, exist_ok=True)
        moved = run_git(root, "mv", "--", "scripts/hooks/pre-commit", "modules/allowed/pre-commit")
        self.assertEqual(moved.returncode, 0, moved.stdout + moved.stderr)
        refused = run_control(root, "preflight", "WI-001")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("scripts/hooks/pre-commit", refused.stdout)

        removal = run_git(root, "commit", "-q", "-m", "the gate carries away its own file")
        self.assertEqual(removal.returncode, 0, "in-tree mode: an absent hook cannot run")
        audit = run_control(root, "audit")
        self.assertNotEqual(audit.returncode, 0)
        self.assertIn("MANDATORY_FILES", audit.stdout)
        status = run_control(root, "status", "--json")
        self.assertEqual(json.loads(status.stdout)["hooks"], "NOT_INSTALLED")
        # Installed outside the worktree, the same removal is refused: see the test above.

    def test_a_new_not_started_copy_passes_bootstrap_audit(self) -> None:
        temporary, root = self.make_copy()
        self.addCleanup(temporary.cleanup)
        findings = self.control_module.ProjectControl(root).bootstrap_findings()
        self.assertTrue(all(item.status == "PASS" for item in findings), findings)

    def test_b_charter_write_is_allowed_in_bootstrap_mode(self) -> None:
        self.assertEqual(
            self.control_module.bootstrap_path_errors(["docs/governance/PROJECT_CHARTER.md"]),
            [],
        )

    def test_c_business_module_write_is_refused_in_bootstrap_mode(self) -> None:
        errors = self.control_module.bootstrap_path_errors(["modules/payments/engine.py"])
        self.assertTrue(any("bootstrap-forbidden" in error for error in errors))

    def test_d_first_human_decision_path_is_allowed(self) -> None:
        self.assertEqual(
            self.control_module.bootstrap_path_errors(["docs/governance/HUMAN_DECISIONS.md"]),
            [],
        )

    def test_e_first_work_item_creation_is_allowed_and_valid(self) -> None:
        temporary, root = self.make_copy()
        self.addCleanup(temporary.cleanup)
        self.configure_ready_for_closeout(root)
        control = self.control_module.ProjectControl(root)
        self.assertEqual(control.project_control_errors(), [])
        self.assertEqual(control.roadmap_errors(), [])
        self.assertEqual(
            self.control_module.bootstrap_path_errors(["project_control/work-items/WI-001.json"]),
            [],
        )

    def test_f_closeout_requires_complete_deliverables(self) -> None:
        temporary, root = self.make_copy()
        self.addCleanup(temporary.cleanup)
        control = self.control_module.ProjectControl(root)
        self.assertTrue(control.closeout_readiness())
        self.configure_ready_for_closeout(root)
        self.assertEqual(control.closeout_readiness(), [])

    def test_g_bootstrap_is_refused_after_complete(self) -> None:
        temporary, root = self.make_copy()
        self.addCleanup(temporary.cleanup)
        base_head = self.configure_ready_for_closeout(root)
        self.complete_initialization(root, base_head)
        findings = self.control_module.ProjectControl(root).bootstrap_findings(
            ["docs/governance/PROJECT_CHARTER.md"]
        )
        self.assertTrue(any(item.check == "BOOTSTRAP_MODE" and item.status == "FAIL" for item in findings))

    def test_h_normal_work_without_known_work_item_is_refused(self) -> None:
        temporary, root = self.make_copy()
        self.addCleanup(temporary.cleanup)
        findings = self.control_module.ProjectControl(root).preflight_findings("WI-999")
        self.assertTrue(any(item.check == "WORK_ITEM_EXISTS" and item.status == "FAIL" for item in findings))
        self.assertTrue(any(item.check == "NORMAL_MODE" and item.status == "FAIL" for item in findings))

    def test_i_authorized_normal_work_item_passes_preflight(self) -> None:
        temporary, root = self.make_copy()
        self.addCleanup(temporary.cleanup)
        base_head = self.configure_ready_for_closeout(root)
        self.complete_initialization(root, base_head)
        stage_explicit_files(root)
        commit = run_git(
            root,
            "-c",
            "user.name=Fixture Owner",
            "-c",
            "user.email=fixture@example.invalid",
            "commit",
            "-m",
            "fixture: complete initialization",
        )
        self.assertEqual(commit.returncode, 0, commit.stdout + commit.stderr)
        initialization_head = run_git(root, "rev-parse", "HEAD").stdout.strip()
        started = self.start_command(root, "WI-001")
        self.assertEqual(started.returncode, 0, started.stdout + started.stderr)
        item = load_json(root / "project_control/work-items/WI-001.json")
        self.assertEqual(item["base_head"], base_head)
        self.assertEqual(item["start_head"], initialization_head)
        self.assertIn("INITIALIZATION_STATUS: COMPLETE", (root / "FIRST_START.md").read_text())
        findings = self.control_module.ProjectControl(root).preflight_findings(
            "WI-001", ["docs/first-change/README.md"]
        )
        self.assertTrue(all(item.status == "PASS" for item in findings), findings)

    def test_p_create_work_item_breaks_preflight_creation_circularity(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        created = self.create_lifecycle_work_item(root, "WI-001", "HD-102")
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        item = load_json(root / "project_control/work-items/WI-001.json")
        self.assertEqual(item["status"], "AUTHORIZED")
        self.assertTrue(item["conversation_refs"])
        self.assertFalse((root / ".git/refs/heads/work/wi-001-lifecycle-wi-001").exists())
        audit = run_control(root, "audit")
        self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)

    def test_q_start_creates_branch_before_full_preflight(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        created = self.create_lifecycle_work_item(root, "WI-001", "HD-102")
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        started = self.start_command(root, "WI-001")
        self.assertEqual(started.returncode, 0, started.stdout + started.stderr)
        item = load_json(root / "project_control/work-items/WI-001.json")
        self.assertEqual(item["status"], "IN_PROGRESS")
        self.assertEqual(run_git(root, "branch", "--show-current").stdout.strip(), item["branch"])
        preflight = run_control(root, "preflight", "WI-001", "--path", "reports/WI-001.txt")
        self.assertEqual(preflight.returncode, 0, preflight.stdout + preflight.stderr)

    def test_r_generated_records_are_expected_but_unknown_path_fails(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        created = self.create_lifecycle_work_item(root, "WI-001", "HD-102")
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        trace = run_control(root, "audit")
        self.assertEqual(trace.returncode, 0, trace.stdout + trace.stderr)
        classifications = load_json(root / "docs/governance/git-path-classifications.v1.json")
        self.assertIn(
            "project_control/work-items/WI-001.json",
            classifications["PROJECT_CONTROL_GENERATED"],
        )
        (root / "mystery.txt").write_text("not created by Project Control\n", encoding="utf-8")
        refused = run_control(root, "audit")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("UNEXPLAINED path: mystery.txt", refused.stdout)

    def test_s_normal_mode_at_rest_accepts_only_done_work_items(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        created = self.create_lifecycle_work_item(root, "WI-001", "HD-102")
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        started = self.start_command(root, "WI-001")
        self.assertEqual(started.returncode, 0, started.stdout + started.stderr)
        branch = run_git(root, "branch", "--show-current").stdout.strip()
        self.commit_fixture_if_needed(root, "test: prepare WI-001 integration")
        self.merge_fixture_branch(root, branch, "merge: integrate WI-001 for idle audit")
        evidence = self.write_committed_evidence(root, "WI-001")
        tests_only = run_control(
            root,
            "close",
            "WI-001",
            "--test-evidence",
            evidence["tests"],
        )
        self.assertNotEqual(tests_only.returncode, 0)
        self.assertEqual(
            load_json(root / "project_control/work-items/WI-001.json")["status"],
            "IN_PROGRESS",
        )
        closed = run_control(
            root,
            "close",
            "WI-001",
            "--test-evidence",
            evidence["tests"],
            "--integration-evidence",
            evidence["integration"],
        )
        self.assertEqual(closed.returncode, 0, closed.stdout + closed.stderr)
        records = [
            load_json(path)
            for path in sorted((root / "project_control/work-items").glob("*.json"))
        ]
        self.assertFalse(
            [item for item in records if item["status"] in {"AUTHORIZED", "IN_PROGRESS"}]
        )
        audit = run_control(root, "audit")
        self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)

    def test_t_end_to_end_two_work_items_and_two_idle_audits(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)

        created_one = self.create_lifecycle_work_item(root, "WI-001", "HD-102")
        self.assertEqual(created_one.returncode, 0, created_one.stdout + created_one.stderr)
        started_one = self.start_command(root, "WI-001")
        self.assertEqual(started_one.returncode, 0, started_one.stdout + started_one.stderr)
        preflight_one = run_control(root, "preflight", "WI-001", "--path", "reports/WI-001.txt")
        self.assertEqual(preflight_one.returncode, 0, preflight_one.stdout + preflight_one.stderr)
        (root / "reports/WI-001.txt").write_text("integration fixture\n", encoding="utf-8")
        first_branch = run_git(root, "branch", "--show-current").stdout.strip()
        self.commit_fixture(root, "test: exercise WI-001")
        self.merge_fixture_branch(root, first_branch, "merge: integrate WI-001")
        first_evidence = self.write_committed_evidence(root, "WI-001")
        closed_one = run_control(
            root,
            "close",
            "WI-001",
            "--test-evidence",
            first_evidence["tests"],
            "--integration-evidence",
            first_evidence["integration"],
        )
        self.assertEqual(closed_one.returncode, 0, closed_one.stdout + closed_one.stderr)
        first_idle_audit = run_control(root, "audit")
        self.assertEqual(first_idle_audit.returncode, 0, first_idle_audit.stdout + first_idle_audit.stderr)
        self.assertEqual(run_git(root, "status", "--porcelain=v1", "--untracked-files=all").stdout, "")

        created_two = self.create_lifecycle_work_item(root, "WI-002", "HD-103")
        self.assertEqual(created_two.returncode, 0, created_two.stdout + created_two.stderr)
        started_two = self.start_command(root, "WI-002")
        self.assertEqual(started_two.returncode, 0, started_two.stdout + started_two.stderr)
        second_branch = run_git(root, "branch", "--show-current").stdout.strip()
        self.commit_fixture_if_needed(root, "test: exercise WI-002")
        self.merge_fixture_branch(root, second_branch, "merge: integrate WI-002")
        second_evidence = self.write_committed_evidence(root, "WI-002")
        closed_two = run_control(
            root,
            "close",
            "WI-002",
            "--test-evidence",
            second_evidence["tests"],
            "--integration-evidence",
            second_evidence["integration"],
        )
        self.assertEqual(closed_two.returncode, 0, closed_two.stdout + closed_two.stderr)

        records = [
            load_json(path)
            for path in sorted((root / "project_control/work-items").glob("*.json"))
        ]
        self.assertFalse(
            [item for item in records if item["status"] in {"AUTHORIZED", "IN_PROGRESS"}]
        )
        final_audit = run_control(root, "audit")
        self.assertEqual(final_audit.returncode, 0, final_audit.stdout + final_audit.stderr)

    def test_u_failed_start_rolls_back_branch_and_lifecycle_state(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        created = self.create_lifecycle_work_item(root, "WI-001", "HD-102")
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        item = load_json(root / "project_control/work-items/WI-001.json")
        branch = item["branch"]
        refused = self.start_command(root, "WI-001", "--path", "modules/outside-scope.py")
        self.assertNotEqual(refused.returncode, 0)
        self.assertEqual(run_git(root, "branch", "--show-current").stdout.strip(), "main")
        self.assertNotEqual(
            run_git(root, "show-ref", "--verify", "--quiet", f"refs/heads/{branch}").returncode,
            0,
        )
        self.assertEqual(
            load_json(root / "project_control/work-items/WI-001.json")["status"],
            "AUTHORIZED",
        )
        self.assertEqual(list((root / "project_control/agent-runs").glob("RUN-*.json")), [])

    def test_v_failed_creation_writes_no_administrative_consequence(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        decisions_before = (root / "docs/governance/HUMAN_DECISIONS.md").read_bytes()
        roadmap_before = (root / "docs/governance/roadmap-state.v1.json").read_bytes()
        (root / "unexplained.txt").write_text("unknown\n", encoding="utf-8")
        refused = self.create_lifecycle_work_item(root, "WI-001", "HD-102")
        self.assertNotEqual(refused.returncode, 0)
        self.assertFalse((root / "project_control/work-items/WI-001.json").exists())
        self.assertEqual((root / "docs/governance/HUMAN_DECISIONS.md").read_bytes(), decisions_before)
        self.assertEqual((root / "docs/governance/roadmap-state.v1.json").read_bytes(), roadmap_before)

    def test_not_started_fixture_prunes_project_capability_data_and_reports(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name) / "derived"
        shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc", ".DS_Store"))
        project_files = (
            "modules/domain/src/engine.py", "modules/domain/tests/test_engine.py", "applications/cli/main.py",
            "shared/util.py", "contracts/domain.v1.json", "data/generated/cache.json", "reports/closeout.json",
        )
        for relative in project_files:
            (root / relative).parent.mkdir(parents=True, exist_ok=True)
            (root / relative).write_text("project content\n", encoding="utf-8")
        self.reset_to_not_started_fixture(root)
        for relative in project_files:
            self.assertFalse((root / relative).exists(), relative)
        self.assertFalse((root / "modules/domain").exists(), "emptied directories disappear")
        for directory in self.PROJECT_CONTENT_ROOTS:
            self.assertTrue((root / directory / "README.md").is_file(), directory)
        self.assertEqual(self.control_module.ProjectControl(root).business_files(), [])

    def test_w_not_started_fixture_is_independent_from_initialized_source_state(self) -> None:
        temporary, root = self.make_copy()
        self.addCleanup(temporary.cleanup)
        base_head = self.configure_ready_for_closeout(root, "WI-777")
        self.complete_initialization(root, base_head)
        self.reset_to_not_started_fixture(root)
        self.assertIn(
            "INITIALIZATION_STATUS: NOT_STARTED",
            (root / "FIRST_START.md").read_text(encoding="utf-8"),
        )
        self.assertEqual(
            load_json(root / "project_control/project-state.v1.json")["initialization"]["status"],
            "NOT_STARTED",
        )
        self.assertEqual(load_json(root / "docs/governance/roadmap-state.v1.json")["work_items"], [])
        self.assertEqual(list((root / "project_control/work-items").glob("*.json")), [])
        self.assertNotRegex(
            (root / "docs/governance/HUMAN_DECISIONS.md").read_text(encoding="utf-8"),
            r"(?m)^## HD-[0-9]{3,}\s*$",
        )

    def test_start_uses_committed_authorization_head_and_keeps_provenance(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        created = self.create_lifecycle_work_item(root, "WI-001", "HD-102")
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        item_path = root / "project_control/work-items/WI-001.json"
        original = load_json(item_path)
        self.assertEqual(original["start_head"], "UNKNOWN")
        # create-work-item committed the authorization itself on the canonical branch.
        authorization_head = run_git(root, "rev-parse", "HEAD").stdout.strip()
        self.assertEqual(run_git(root, "status", "--porcelain=v1", "--untracked-files=all").stdout, "")
        self.assertIn("chore(project-control): create WI-001", run_git(root, "log", "-1", "--format=%s").stdout)
        self.assertNotEqual(original["base_head"], authorization_head)
        started = self.start_command(root, "WI-001")
        self.assertEqual(started.returncode, 0, started.stdout + started.stderr)
        item = load_json(item_path)
        self.assertEqual(item["base_head"], original["base_head"])
        self.assertEqual(item["start_head"], authorization_head)
        # start committed its records on the canonical branch, then opened the branch from that commit.
        records_commit = run_git(root, "rev-parse", "main").stdout.strip()
        self.assertEqual(run_git(root, "rev-parse", f"{records_commit}^").stdout.strip(), authorization_head)
        self.assertIn("chore(project-control): start WI-001", run_git(root, "log", "-1", "--format=%s", "main").stdout)
        self.assertEqual(run_git(root, "rev-parse", "HEAD").stdout.strip(), records_commit)
        self.assertEqual(run_git(root, "branch", "--show-current").stdout.strip(), item["branch"])
        self.assertEqual(run_git(root, "status", "--porcelain=v1", "--untracked-files=all").stdout, "")
        self.assertEqual(
            run_git(root, "show", f"main:project_control/work-items/WI-001.json").stdout,
            item_path.read_text(encoding="utf-8"),
        )
        run = load_json(root / f"project_control/agent-runs/{item['agent_run_refs'][0]}.json")
        self.assertEqual(run["base_head"], original["base_head"])
        self.assertEqual(run["start_head"], authorization_head)

    def test_start_refuses_noncanonical_current_branch_without_mutation(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        created = self.create_lifecycle_work_item(root, "WI-001", "HD-102")
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        switched = run_git(root, "switch", "-c", "unrelated-work")
        self.assertEqual(switched.returncode, 0, switched.stdout + switched.stderr)
        before = self.snapshot_repository(root)
        refused = self.start_command(root, "WI-001")
        self.assertNotEqual(refused.returncode, 0)
        self.assertEqual(self.snapshot_repository(root), before)
        self.assertIn("canonical", (refused.stdout + refused.stderr).lower())

    def test_start_refuses_base_outside_canonical_ancestry(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        created = self.create_lifecycle_work_item(root, "WI-001", "HD-102")
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        tree = run_git(root, "rev-parse", "HEAD^{tree}").stdout.strip()
        unrelated = run_git(
            root, "-c", "user.name=Fixture Owner", "-c", "user.email=fixture@example.invalid",
            "commit-tree", tree, "-m", "fixture: unrelated provenance",
        )
        self.assertEqual(unrelated.returncode, 0, unrelated.stdout + unrelated.stderr)
        item_path = root / "project_control/work-items/WI-001.json"
        item = load_json(item_path)
        item["base_head"] = unrelated.stdout.strip()
        item_path.write_text(json.dumps(item, indent=2) + "\n", encoding="utf-8")
        registry = root / "docs/governance/WORKTREE_REGISTRY.md"
        registry.write_text(
            self.control_module.render_registry_entry(registry.read_text(), item, "DECLARED"),
            encoding="utf-8",
        )
        self.commit_fixture(root, "fixture: record non-ancestor baseline")
        before = self.snapshot_repository(root)
        refused = self.start_command(root, "WI-001")
        self.assertNotEqual(refused.returncode, 0)
        self.assertEqual(self.snapshot_repository(root), before)
        self.assertIn("ancestor", (refused.stdout + refused.stderr).lower())

    def test_start_refuses_preexisting_branch_at_another_tip(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        created = self.create_lifecycle_work_item(root, "WI-001", "HD-102")
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        item = load_json(root / "project_control/work-items/WI-001.json")
        branch = run_git(root, "branch", item["branch"], item["base_head"])
        self.assertEqual(branch.returncode, 0, branch.stdout + branch.stderr)
        advanced = run_git(root, "commit", "--allow-empty", "-q", "-m", "fixture: advance canonical authorization baseline")
        self.assertEqual(advanced.returncode, 0, advanced.stdout + advanced.stderr)
        before = self.snapshot_repository(root)
        old_tip = run_git(root, "rev-parse", item["branch"]).stdout
        refused = self.start_command(root, "WI-001")
        self.assertNotEqual(refused.returncode, 0)
        self.assertEqual(self.snapshot_repository(root), before)
        self.assertEqual(run_git(root, "rev-parse", item["branch"]).stdout, old_tip)

    def test_close_refuses_nonexistent_evidence_and_preserves_lifecycle(self) -> None:
        _, root, evidence = self.prepare_integrated_item()
        evidence["tests"] = "reports/evidence/WI-001/missing.json"
        before = self.snapshot_repository(root)
        refused = self.close_with_evidence(root, "WI-001", evidence)
        self.assertNotEqual(refused.returncode, 0)
        self.assertEqual(self.snapshot_repository(root), before)

    def test_close_requires_declared_canonical_branch_for_integration(self) -> None:
        _, root, evidence = self.prepare_integrated_item()
        switched = run_git(root, "switch", "-c", "looks-integrated-but-not-canonical")
        self.assertEqual(switched.returncode, 0, switched.stdout + switched.stderr)
        before = self.snapshot_repository(root)
        refused = self.close_with_evidence(root, "WI-001", evidence)
        self.assertNotEqual(refused.returncode, 0)
        self.assertEqual(self.snapshot_repository(root), before)
        self.assertIn("canonical", (refused.stdout + refused.stderr).lower())

    def test_close_rejects_failed_or_mismatched_evidence(self) -> None:
        _, root, evidence = self.prepare_integrated_item()
        report_path = root / evidence["tests"]
        original = load_json(report_path)
        cases = {
            "failed result": {"result": "FAIL"},
            "unsupported version": {"schema_version": "banana"},
            "wrong work item": {"work_item_id": "WI-999"},
            "wrong gate": {"gate": "integration"},
            "wrong runtime target": {"runtime_target": "PRODUCTION"},
            "unknown subject commit": {"subject_commit": "0" * 40},
            "missing timezone": {"recorded_at": "2026-09-06T10:00:00"},
            "missing artifact": {"artifacts": [{"path": "reports/evidence/WI-001/missing.txt", "sha256": "0" * 64}]},
            "wrong artifact hash": {"artifacts": [{"path": original["artifacts"][0]["path"], "sha256": "0" * 64}]},
        }
        for label, changes in cases.items():
            with self.subTest(label=label):
                report = copy.deepcopy(original)
                report.update(changes)
                reference = f"reports/evidence/WI-001/invalid-{label.replace(' ', '-')}.json"
                report_path = root / reference
                report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
                self.commit_fixture(root, f"fixture: {label}")
                before = self.snapshot_repository(root)
                refused = self.close_with_evidence(root, "WI-001", {**evidence, "tests": reference})
                self.assertNotEqual(refused.returncode, 0, refused.stdout + refused.stderr)
                self.assertNotIn("immutable", refused.stdout)
                self.assertEqual(self.snapshot_repository(root), before)
                self.assertEqual(load_json(root / "project_control/work-items/WI-001.json")["status"], "IN_PROGRESS")

    def test_close_rejects_uncommitted_report_and_artifact_changes(self) -> None:
        _, root, evidence = self.prepare_integrated_item()
        report_path = root / evidence["tests"]
        report = load_json(report_path)
        artifact = root / report["artifacts"][0]["path"]
        for path in (report_path, artifact):
            with self.subTest(path=str(path.relative_to(root))):
                original = path.read_bytes()
                path.write_bytes(original + b"\n")
                before = self.snapshot_repository(root)
                refused = self.close_with_evidence(root, "WI-001", evidence)
                self.assertNotEqual(refused.returncode, 0)
                self.assertEqual(self.snapshot_repository(root), before)
                path.write_bytes(original)

    def test_close_rejects_evidence_predating_a_business_change(self) -> None:
        _, root, evidence = self.prepare_integrated_item()
        (root / "reports/WI-001.txt").write_text("changed after evidence was recorded\n", encoding="utf-8")
        self.commit_fixture(root, "fixture: change business content after qualification")
        before = self.snapshot_repository(root)
        refused = self.close_with_evidence(root, "WI-001", evidence)
        self.assertNotEqual(refused.returncode, 0)
        self.assertEqual(self.snapshot_repository(root), before)

    def test_controlled_runtime_closes_without_claiming_production(self) -> None:
        _, root, evidence = self.prepare_integrated_item("CONTROLLED_NON_PRODUCTION_RUNTIME")
        closed = self.close_with_evidence(root, "WI-001", evidence)
        self.assertEqual(closed.returncode, 0, closed.stdout + closed.stderr)
        item = load_json(root / "project_control/work-items/WI-001.json")
        self.assertEqual(item["status"], "DONE")
        self.assertEqual(item["deployment_status"], "DEPLOYED_IN_CONTROLLED_ENVIRONMENT")
        self.assertEqual(item["runtime_proof_status"], "RUNTIME_PROVEN")
        self.assertNotEqual(item["runtime_proof_status"], "PRODUCTION_VERIFIED")

    def test_production_rejects_controlled_runtime_level(self) -> None:
        _, root, evidence = self.prepare_integrated_item("PRODUCTION")
        path = root / evidence["runtime_proof"]
        report = load_json(path)
        report["level"] = "RUNTIME_PROVEN"
        reference = "reports/evidence/WI-001/runtime-wrong-level.json"
        path = root / reference
        path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        self.commit_fixture(root, "fixture: insufficient production proof")
        before = self.snapshot_repository(root)
        refused = self.close_with_evidence(root, "WI-001", {**evidence, "runtime_proof": reference})
        self.assertNotEqual(refused.returncode, 0)
        self.assertEqual(self.snapshot_repository(root), before)

    def test_production_requires_and_accepts_explicit_production_evidence(self) -> None:
        _, root, evidence = self.prepare_integrated_item("PRODUCTION")
        closed = self.close_with_evidence(root, "WI-001", evidence)
        self.assertEqual(closed.returncode, 0, closed.stdout + closed.stderr)
        item = load_json(root / "project_control/work-items/WI-001.json")
        self.assertEqual(item["deployment_status"], "DEPLOYED")
        self.assertEqual(item["runtime_proof_status"], "PRODUCTION_VERIFIED")
        status = run_control(root, "status", "--json")
        self.assertEqual(status.returncode, 0, status.stdout + status.stderr)
        view = next(item for item in json.loads(status.stdout)["work_items"] if item["work_item_id"] == "WI-001")
        self.assertEqual(view["missing_gates"], [])

    def test_schema_rejects_invalid_version_and_null_required_text(self) -> None:
        cases = (
            ("work item version", self.work_item, "schema_version", "banana", self.control_module.validate_work_item),
            ("work item owner", self.work_item, "owner", None, self.control_module.validate_work_item),
            ("work item title", self.work_item, "title", None, self.control_module.validate_work_item),
            ("conversation title", self.conversation, "title", None, self.control_module.validate_conversation_reference),
            ("agent run version", self.agent_run, "schema_version", "banana", self.control_module.validate_agent_run),
        )
        for label, record, field, value, validator in cases:
            with self.subTest(label=label):
                altered = copy.deepcopy(record)
                altered[field] = value
                if validator == self.control_module.validate_work_item:
                    errors = validator(altered, "ALPHA")
                else:
                    errors = validator(altered)
                self.assertTrue(errors, f"Invalid {label} was accepted")
                self.assertTrue(any(field in error for error in errors), errors)

    def test_status_json_reports_project_and_next_action_without_writing(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        before = self.snapshot_repository(root)
        status = run_control(root, "status", "--json")
        self.assertEqual(status.returncode, 0, status.stdout + status.stderr)
        payload = json.loads(status.stdout)
        self.assertEqual(payload["mode"], "NORMAL_MODE")
        self.assertEqual(payload["project_name"], "Example Project")
        self.assertEqual(payload["branch"], "main")
        self.assertEqual(payload["head"], run_git(root, "rev-parse", "HEAD").stdout.strip())
        self.assertIn("work_items", payload)
        self.assertTrue(payload["next_action"])
        self.assertEqual(payload["audit_status"], "PASS")
        self.assertEqual(self.snapshot_repository(root), before)

    def test_status_json_reports_invalid_state_with_failure_exit(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        path = root / "project_control/project-state.v1.json"
        state = load_json(path)
        state["schema_version"] = "banana"
        path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        before = self.snapshot_repository(root)
        status = run_control(root, "status", "--json")
        self.assertNotEqual(status.returncode, 0)
        payload = json.loads(status.stdout)
        self.assertEqual(payload["audit_status"], "FAIL")
        self.assertEqual(self.snapshot_repository(root), before)

    def test_status_and_audit_reject_nonobject_work_item_without_traceback(self) -> None:
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        (root / "project_control/work-items/WI-000.json").write_text("[]\n", encoding="utf-8")
        before = self.snapshot_repository(root)
        for command in (("audit",), ("status", "--json")):
            with self.subTest(command=command):
                refused = run_control(root, *command)
                self.assertNotEqual(refused.returncode, 0)
                self.assertNotIn("Traceback", refused.stdout + refused.stderr)
                if command[0] == "status":
                    self.assertEqual(json.loads(refused.stdout)["audit_status"], "FAIL")
                self.assertEqual(self.snapshot_repository(root), before)

    def test_close_keeps_failed_history_before_a_later_successful_revision(self) -> None:
        _, root, old_evidence = self.prepare_integrated_item()
        report = load_json(root / old_evidence["tests"])
        failed_artifact = root / "reports/evidence/WI-001/tests-failed.txt"
        failed_artifact.write_text("Synthetic failure before the business correction.\n", encoding="utf-8")
        report["result"] = "FAIL"
        report["summary"] = "Synthetic failed check preserved before correction."
        report["artifacts"] = [{
            "path": str(failed_artifact.relative_to(root)),
            "sha256": hashlib.sha256(failed_artifact.read_bytes()).hexdigest(),
        }]
        failed_reference = "reports/evidence/WI-001/tests-failed.json"
        failed_path = root / failed_reference
        failed_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        self.commit_fixture(root, "fixture: preserve failed evidence on revision A")
        failed_before = failed_path.read_bytes()
        item_path = root / "project_control/work-items/WI-001.json"
        item = load_json(item_path)
        item["test_status"] = "FAILED"
        item["evidence"]["tests"] = [failed_reference]
        item_path.write_text(json.dumps(item, indent=2) + "\n", encoding="utf-8")
        (root / "reports/WI-001.txt").write_text("business revision B fixes the failed check\n", encoding="utf-8")
        self.commit_fixture(root, "fixture: correct business content after failed revision A")
        new_evidence = self.write_committed_evidence(root, "WI-001", revision="-corrected")
        closed = self.close_with_evidence(root, "WI-001", new_evidence)
        self.assertEqual(closed.returncode, 0, closed.stdout + closed.stderr)
        item = load_json(item_path)
        self.assertEqual(item["status"], "DONE")
        self.assertEqual(item["test_status"], "TESTED")
        self.assertEqual(item["evidence"]["tests"], [failed_reference, new_evidence["tests"]])
        self.assertEqual(failed_path.read_bytes(), failed_before)
        self.assertEqual(load_json(failed_path)["result"], "FAIL")
        self.assertNotEqual(load_json(failed_path)["subject_commit"], load_json(root / new_evidence["tests"])["subject_commit"])
        audit = run_control(root, "audit")
        self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)

    def test_close_refuses_recommitted_historical_failure_even_with_corrected_hashes(self) -> None:
        _, root, evidence = self.prepare_integrated_item()
        failed = load_json(root / evidence["tests"])
        failed_reference = "reports/evidence/WI-001/failed-before-rewrite.json"
        artifact_reference = "reports/evidence/WI-001/failed-before-rewrite.txt"
        artifact = root / artifact_reference
        artifact.write_text("Synthetic original failure.\n")
        failed.update(result="FAIL", artifacts=[{
            "path": artifact_reference, "sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(),
        }])
        path = root / failed_reference
        path.write_text(json.dumps(failed, indent=2) + "\n")
        self.commit_fixture(root, "fixture: record immutable failed evidence")
        item_path = root / "project_control/work-items/WI-001.json"
        item = load_json(item_path)
        item["test_status"] = "FAILED"
        item["evidence"]["tests"] = [failed_reference]
        item_path.write_text(json.dumps(item, indent=2) + "\n")
        artifact.write_text("Rewritten history that now claims success.\n")
        failed.update(result="PASS", summary="Altered historical result")
        failed["artifacts"][0]["sha256"] = hashlib.sha256(artifact.read_bytes()).hexdigest()
        path.write_text(json.dumps(failed, indent=2) + "\n")
        self.commit_fixture(root, "fixture: tamper with committed failure and matching hashes")
        fresh = self.write_committed_evidence(root, "WI-001", revision="-after-tampering")
        before = self.snapshot_repository(root)
        refused = self.close_with_evidence(root, "WI-001", fresh)
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("immutable after its first commit", refused.stdout)
        self.assertEqual(self.snapshot_repository(root), before)

    def test_evidence_immutability_detects_rewrite_through_merge(self) -> None:
        temporary, root = self.make_copy()
        self.addCleanup(temporary.cleanup)
        reference = "reports/evidence/WI-001/observations.txt"
        artifact = root / reference
        artifact.parent.mkdir(parents=True, exist_ok=True)
        self.assertEqual(run_git(root, "switch", "-c", "first-evidence").returncode, 0)
        artifact.write_text("Original observations.\n")
        self.commit_fixture(root, "fixture: first evidence")
        self.merge_fixture_branch(root, "first-evidence", "fixture: merge new evidence")
        control = self.control_module.ProjectControl(root)
        head = run_git(root, "rev-parse", "HEAD").stdout.strip()
        self.assertEqual(control.evidence_file(reference, "WI-001", head)[1], artifact.read_bytes())
        self.assertEqual(run_git(root, "switch", "-c", "unrelated-change").returncode, 0)
        (root / "reports/unrelated.md").write_text("Unrelated report.\n")
        self.commit_fixture(root, "fixture: unrelated commit")
        self.merge_fixture_branch(root, "unrelated-change", "fixture: unchanged evidence merge")
        head = run_git(root, "rev-parse", "HEAD").stdout.strip()
        self.assertEqual(control.evidence_file(reference, "WI-001", head)[1], artifact.read_bytes())
        self.assertEqual(run_git(root, "switch", "-c", "rewritten-evidence").returncode, 0)
        artifact.write_text("Rewritten observations concealed by a merge.\n")
        self.commit_fixture(root, "fixture: rewrite historical evidence")
        self.merge_fixture_branch(root, "rewritten-evidence", "fixture: merge altered evidence")
        head = run_git(root, "rev-parse", "HEAD").stdout.strip()
        with self.assertRaisesRegex(self.control_module.ProjectControlError, "immutable after its first commit"):
            control.evidence_file(reference, "WI-001", head)

    def test_j_arbitrary_project_key_builds_display_reference(self) -> None:
        self.assertEqual(
            self.control_module.display_reference_for("WI-001", "MEDIASRV"),
            "MEDIASRV-001",
        )
        item = copy.deepcopy(self.work_item)
        item["display_reference"] = "MEDIASRV-001"
        self.assertEqual(self.control_module.validate_work_item(item, "MEDIASRV"), [])

    def test_k_absent_project_key_uses_internal_reference(self) -> None:
        self.assertEqual(self.control_module.display_reference_for("WI-001", None), "WI-001")
        item = copy.deepcopy(self.work_item)
        item["display_reference"] = "WI-001"
        self.assertEqual(self.control_module.validate_work_item(item, None), [])

    def test_l_no_historical_work_or_human_decision_is_preloaded(self) -> None:
        temporary, root = self.make_copy()
        self.addCleanup(temporary.cleanup)
        roadmap = load_json(root / "docs/governance/roadmap-state.v1.json")
        self.assertEqual(roadmap["work_items"], [])
        self.assertNotIn("lots", roadmap)
        human_text = (root / "docs/governance/HUMAN_DECISIONS.md").read_text(encoding="utf-8")
        self.assertNotRegex(human_text, r"(?m)^## HD-[0-9]{3,}\s*$")

    def test_m_no_project_name_specific_remote_control_is_active(self) -> None:
        script = (ROOT / "scripts/project_control.py").read_text(encoding="utf-8").lower()
        forbidden_name = "crypto" + "-tactique"
        self.assertNotIn(forbidden_name, script)
        self.assertNotIn("remote points to", script)

    def test_n_conversation_work_item_agent_run_links_pass(self) -> None:
        errors = self.control_module.validate_record_links(
            [self.work_item],
            [self.conversation],
            [self.agent_run],
            human_decisions_text=(
                "## HD-101\n\nDecision: Authorize fixture.\nAuthorized by: Project Owner\n"
            ),
        )
        self.assertEqual(errors, [])

    def test_o_done_without_applicable_evidence_is_refused(self) -> None:
        item = copy.deepcopy(self.work_item)
        item["evidence"]["tests"] = []
        errors = self.control_module.validate_work_item(item, "ALPHA")
        self.assertTrue(any("tests requires evidence" in error for error in errors))

    def test_done_with_unknown_applicability_is_refused(self) -> None:
        item = copy.deepcopy(self.work_item)
        item["applicability"]["deployment"] = "UNKNOWN"
        errors = self.control_module.validate_work_item(item, "ALPHA")
        self.assertTrue(any("UNKNOWN applicability" in error for error in errors))

    def test_provider_agnostic_conversation_and_agent_records(self) -> None:
        self.assertEqual(self.control_module.validate_conversation_reference(self.conversation), [])
        self.assertEqual(self.control_module.validate_agent_run(self.agent_run), [])
        self.assertEqual(self.conversation["provider"], "GenericConversationSystem")
        self.assertEqual(self.agent_run["provider"], "GenericAgentSystem")

    def test_all_json_and_schema_documents_parse(self) -> None:
        """Every JSON document the project holds parses, and every schema has the expected shape.
        What the project holds is what Git sees — tracked, or present and not ignored — never a
        file the project ignores: a half-written download in an ignored folder failed this check
        (fourth independent control, then again at the fifth, F-06)."""
        listed = subprocess.run(
            ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", "*.json"],
            cwd=ROOT, capture_output=True, check=False,
        )
        self.assertEqual(listed.returncode, 0, listed.stderr.decode("utf-8", "replace"))
        documents = sorted(ROOT / entry.decode("utf-8", "surrogateescape") for entry in listed.stdout.split(b"\0") if entry)
        schemas = []
        for path in documents:
            payload = load_json(path)
            if path.name.endswith(".schema.json"):
                schemas.append(path)
                self.assertEqual(
                    self.control_module.schema_shape_errors(payload, str(path.relative_to(ROOT))),
                    [],
                )
        self.assertGreaterEqual(len(schemas), 5)

    def test_definition_of_done_keeps_levels_distinct(self) -> None:
        text = (ROOT / "docs/governance/DEFINITION_OF_DONE.md").read_text(encoding="utf-8")
        for level in (
            "DEVELOPED", "TESTED", "INTEGRATED", "QUALIFIED", "CANONICAL",
            "DEPLOYED_IN_CONTROLLED_ENVIRONMENT", "RUNTIME_PROVEN",
            "DEPLOYED", "PRODUCTION_VERIFIED",
        ):
            self.assertIn(f"`{level}`", text)
        self.assertIn("DONE != TESTS_PASS", text)
        self.assertIn("`RUNTIME_PROVEN` ne vaut jamais `PRODUCTION_VERIFIED`", text)

    def test_repository_contains_no_symlink(self) -> None:
        links = [path for path in ROOT.rglob("*") if ".git" not in path.parts and path.is_symlink()]
        self.assertEqual(links, [])

    # --- hello-squelette: the README shows what the controller really prints ---

    def test_a_new_version_tag_makes_the_generated_view_stale(self) -> None:
        """The view names the promoted version from the tags: a new tag changes what it says."""
        temporary, root = self.make_copy()
        self.addCleanup(temporary.cleanup)
        written = run_control(root, "roadmap-view", "--write")
        self.assertEqual(written.returncode, 0, written.stdout + written.stderr)
        self.assertIn("Vue roadmap : à jour", run_control(root, "status").stdout)
        before = json.loads(run_control(root, "roadmap-view", "--json").stdout)["verification"]
        tagged = run_git(root, "tag", "-a", "v9.9.9", "-m", "fixture")
        self.assertEqual(tagged.returncode, 0, tagged.stdout + tagged.stderr)
        after = json.loads(run_control(root, "roadmap-view", "--json").stdout)["verification"]
        self.assertNotEqual(before["sources_digest"], after["sources_digest"],
                            "the tags the view displays belong to its freshness")
        self.assertIn("Vue roadmap : périmée", run_control(root, "status").stdout)
        # Committing is not tagging: a plain commit must not make the view stale, or regenerating
        # it would stale it again at once, without end.
        again = run_control(root, "roadmap-view", "--write")
        self.assertEqual(again.returncode, 0, again.stdout + again.stderr)
        self.assertIn("Vue roadmap : à jour", run_control(root, "status").stdout)
        (root / "docs/governance/PROJECT_CHARTER.md").write_text("# Charter\n\nfixture\n", encoding="utf-8")
        self.commit_fixture(root, "fixture: a commit that changes no view source")
        self.assertIn("Vue roadmap : à jour", run_control(root, "status").stdout)

    def test_the_view_never_claims_that_tests_passed(self) -> None:
        """The controller runs its own checks, never the test suite: it may count the tests it can
        see, never declare their result."""
        self.skip_unless_template("the generated view of the template")
        temporary, root = self.make_copy()
        self.addCleanup(temporary.cleanup)
        written = run_control(root, "roadmap-view", "--write")
        self.assertEqual(written.returncode, 0, written.stdout + written.stderr)
        view = json.loads(run_control(root, "roadmap-view", "--json").stdout)
        self.assertEqual(view["verification"]["audit_status"], "PASS")
        self.assertGreater(view["verification"]["tests_count"], 0, "the declared tests are counted")
        markdown = (root / "provenance/ROADMAP_VIEW.md").read_text(encoding="utf-8")
        page = (root / "provenance/roadmap/ROADMAP.html").read_text(encoding="utf-8")
        # Only what the view reports about itself is under test: the past may quote, and correct,
        # the wording that used to be wrong.
        reported = markdown.split("## Vérification", 1)[1].split("## Tes idées", 1)[0]
        for rendered in (reported, page.split("Tes idées", 1)[0]):
            self.assertNotIn("toutes réussies", rendered,
                             "no rendering may announce a test result the controller never obtained")
            self.assertIn("non exécutés par cette vue", rendered)

    def test_plain_style_adds_no_path_of_its_own_outside_the_technical_block(self) -> None:
        """PLAIN promises plain language; the cells the view composes itself must honour it."""
        self.skip_unless_template("the roadmap of the template")
        temporary, root = self.make_copy()
        self.addCleanup(temporary.cleanup)
        written = run_control(root, "roadmap-view", "--write", "--style", "PLAIN")
        self.assertEqual(written.returncode, 0, written.stdout + written.stderr)
        markdown = (root / "provenance/ROADMAP_VIEW.md").read_text(encoding="utf-8")
        reading, _, technical = markdown.partition("## Pour les techniciens")
        scopes = [item["scope"] for item in json.loads(run_control(root, "roadmap-view", "--json").stdout)["chantiers"]
                  if item.get("scope")]
        self.assertTrue(scopes, "the template declares scoped chantiers")
        for scope in scopes:
            self.assertNotIn(scope, reading, "a file path is a technical identifier the view adds itself")
            self.assertIn(scope, technical, "moved out of the table, the path stays available")
        technical_style = run_control(root, "roadmap-view", "--json", "--style", "TECHNICAL")
        self.assertEqual(technical_style.returncode, 0, technical_style.stdout + technical_style.stderr)

    def test_removing_the_readme_markers_does_not_silence_the_demo_check(self) -> None:
        """The README block is the guarantee itself: without its markers the check must fail, not pass."""
        demo = ROOT / "examples/hello-squelette/demo.py"
        state = load_json(ROOT / "project_control/project-state.v1.json")
        if not demo.exists() or state.get("repository_role") != "PROJECT_TEMPLATE":
            self.skipTest("hello-squelette is replayed from the template itself only")
        if shutil.which("python3") is None:
            self.skipTest("the commit gate installed by the demo needs python3 on PATH")
        temporary, root = self.make_copy()
        self.addCleanup(temporary.cleanup)
        readme = root / "README.md"
        text = readme.read_text(encoding="utf-8")
        self.assertIn("<!-- hello-squelette:begin -->", text)
        readme.write_text(
            text.replace("<!-- hello-squelette:begin -->\n", "").replace("<!-- hello-squelette:end -->\n", ""),
            encoding="utf-8",
        )
        checked = subprocess.run(
            [sys.executable, "-B", str(root / "examples/hello-squelette/demo.py"), "--check"],
            cwd=root, check=False, capture_output=True, text=True,
        )
        self.assertNotEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        self.assertIn("no <!-- hello-squelette:begin -->", checked.stdout)

    def test_the_demo_states_the_exact_reach_of_the_proof_of_reading(self) -> None:
        """The proof establishes that the work started from the current authorities — not that
        anyone read them. The showcase must not promise more than the mechanism delivers."""
        self.skip_unless_template("the hello-squelette example")
        demo = (ROOT / "examples/hello-squelette/demo.py").read_text(encoding="utf-8")
        transcript = (ROOT / "examples/hello-squelette/TRANSCRIPT.md")
        self.assertNotIn("an agent that has not read cannot", demo)
        self.assertIn("No mechanism can prove that a mind was changed by reading.", demo)
        if transcript.is_file():
            self.assertNotIn("an agent that has not read cannot", transcript.read_text(encoding="utf-8"))

    INTERRUPTION_HARNESS = """
import sys, os, importlib.util
root = sys.argv[1]
os.chdir(root)
spec = importlib.util.spec_from_file_location("pc", os.path.join(root, "scripts", "project_control.py"))
mod = importlib.util.module_from_spec(spec); sys.modules["pc"] = mod; spec.loader.exec_module(mod)
original = mod.ProjectControl.preflight_findings
state = {"n": 0}
def interrupted(self, *a, **k):
    state["n"] += 1
    if state["n"] >= 2:
        raise KeyboardInterrupt("Ctrl-C at the worst moment")
    return original(self, *a, **k)
mod.ProjectControl.preflight_findings = interrupted
try:
    mod.main(sys.argv[2:])
except KeyboardInterrupt:
    print("INTERRUPTED")
"""

    def test_an_interruption_leaves_no_half_finished_transition(self) -> None:
        """Ctrl-C is not an ordinary failure to Python: `except Exception` never sees it. A
        transition caught mid-flight must roll back exactly as any other failure does, or the
        project is left with records saying IN_PROGRESS and a branch nobody authorized."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        created = self.create_lifecycle_work_item(root, "WI-001", "HD-102")
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        digest = self.authorities_digest(root, "WI-001")
        self.assertTrue(digest)
        holder = tempfile.TemporaryDirectory()
        self.addCleanup(holder.cleanup)
        harness = Path(holder.name) / "interruption_harness.py"
        harness.write_text(self.INTERRUPTION_HARNESS, encoding="utf-8")
        head_before = run_git(root, "rev-parse", "HEAD").stdout.strip()
        record_before = (root / "project_control/work-items/WI-001.json").read_bytes()
        branches_before = run_git(root, "branch", "--list").stdout
        interrupted = subprocess.run(
            [sys.executable, "-B", str(harness), str(root), "start", "WI-001", "--authorities-digest", digest],
            cwd=root, check=False, capture_output=True, text=True,
        )
        self.assertIn("INTERRUPTED", interrupted.stdout, interrupted.stdout + interrupted.stderr)
        self.assertEqual(run_git(root, "rev-parse", "HEAD").stdout.strip(), head_before, "the records commit is undone")
        self.assertEqual((root / "project_control/work-items/WI-001.json").read_bytes(), record_before,
                         "the Work Item is not left IN_PROGRESS by an interrupted start")
        self.assertEqual(run_git(root, "branch", "--list").stdout, branches_before, "no branch survives the interruption")
        self.assertEqual(run_git(root, "status", "--porcelain=v1").stdout, "")
        self.assertEqual(run_control(root, "audit").returncode, 0)

    def test_an_upgrade_never_overwrites_a_file_the_project_owns(self) -> None:
        """A new core version may claim a path the project already uses. The old manifest knows
        nothing of that path, so no drift is reported for it — and the file would be replaced
        without a word."""
        def claim_a_project_path(source: Path) -> None:
            (source / "tests/fixtures/project_control/collision.valid.json").write_text('{"upstream": true}\n', encoding="utf-8")

        upstream = self.make_template_source("9.9.9", claim_a_project_path)
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        self.create_core_upgrade_work_item(root)
        owned = root / "tests/fixtures/project_control/collision.valid.json"
        owned.write_text('{"mine": "written long before"}\n', encoding="utf-8")
        self.commit_fixture(root, "fixture: the project writes its own file on that path")
        mine = owned.read_bytes()
        report = run_control(root, "template-upgrade", "--source", str(upstream))
        self.assertNotEqual(report.returncode, 0, report.stdout)
        self.assertIn("the project owns these paths, refused without --overwrite", report.stdout)
        self.assertIn("tests/fixtures/project_control/collision.valid.json", report.stdout)
        applied = run_control(root, "template-upgrade", "--source", str(upstream), "--apply")
        self.assertNotEqual(applied.returncode, 0)
        self.assertEqual(owned.read_bytes(), mine, "the project's file is untouched")
        # Named explicitly, the same upgrade proceeds: the human decided, not the tool.
        forced = run_control(root, "template-upgrade", "--source", str(upstream), "--apply",
                             "--overwrite", "tests/fixtures/project_control/collision.valid.json")
        self.assertEqual(forced.returncode, 0, forced.stdout + forced.stderr)
        self.assertEqual(owned.read_bytes(), (upstream / "tests/fixtures/project_control/collision.valid.json").read_bytes())

    def test_an_integration_merge_passes_and_carries_only_what_its_branch_changed(self) -> None:
        """The doctrine promises that an integration merge is not development. It must pass —
        and it must not become a door for a change the branch never made."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        self.install_commit_hook(root)
        item = self.create_and_start_lifecycle_work_item(
            root, "WI-001", "HD-102", authorized_path="modules/allowed", code="APPLICABLE",
        )
        (root / "modules/allowed").mkdir(parents=True, exist_ok=True)
        (root / "modules/allowed/feature.py").write_text("VALUE = 1\n", encoding="utf-8")
        run_git(root, "add", "--", "modules/allowed/feature.py")
        committed = run_git(root, "commit", "-q", "-m", "feat: the authorized work")
        self.assertEqual(committed.returncode, 0, committed.stdout + committed.stderr)
        self.switch_to_canonical(root)
        merged = run_git(root, "merge", "--no-commit", "--no-ff", str(item["branch"]))
        self.assertEqual(merged.returncode, 0, merged.stdout + merged.stderr)
        gate = run_control(root, "pre-commit")
        self.assertEqual(gate.returncode, 0, gate.stdout + gate.stderr)
        # A path the branch never touched cannot ride along under the name of integration.
        (root / "modules/allowed/passenger.py").write_text("SMUGGLED = 1\n", encoding="utf-8")
        run_git(root, "add", "--", "modules/allowed/passenger.py")
        refused = run_control(root, "pre-commit")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("an integration merge carries only what its branch changed", refused.stdout)
        self.assertIn("modules/allowed/passenger.py", refused.stdout)
        run_git(root, "rm", "-f", "--quiet", "--", "modules/allowed/passenger.py")
        landed = run_git(root, "commit", "--no-edit", "-q")
        self.assertEqual(landed.returncode, 0, landed.stdout + landed.stderr)

    def test_two_transactions_at_once_are_serialised_and_leave_a_coherent_state(self) -> None:
        """Two sessions writing records at the same time used to interleave: both could fail leaving
        a roadmap that cites a Work Item whose record no longer exists, and the rollback of one could
        restore a file to the state it had before the other's committed change. Records are written
        one transaction at a time; whoever arrives second is refused, plainly, having written
        nothing."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        started = time.time()
        processes = [
            subprocess.Popen(
                [sys.executable, "-B", "scripts/project_control.py", *self.lifecycle_arguments(
                    f"WI-{index:03d}", f"HD-3{index:02d}")],
                cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            )
            for index in (1, 2)
        ]
        results = [process.communicate() for process in processes]
        codes = [process.returncode for process in processes]
        self.assertEqual(sorted(codes), [0, 0], "".join(out + err for out, err in results))
        self.assertLess(time.time() - started, 120, "the lock must not deadlock")
        # Whatever the order, the repository is coherent: every Work Item the registers cite has
        # its record, and the audit agrees.
        for index in (1, 2):
            self.assertTrue((root / f"project_control/work-items/WI-{index:03d}.json").is_file())
        audit = run_control(root, "audit")
        self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)
        self.assertEqual(run_git(root, "status", "--porcelain").stdout, "", "both transactions committed")

    def test_a_rollback_never_undoes_what_another_session_committed(self) -> None:
        """The rollback restored the bytes captured when a file was first touched. If anything had
        written to that file since — another session's committed decision — restoring erased it.
        A file that no longer holds what this transaction wrote is not this transaction's to undo."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        sys.path.insert(0, str(root / "scripts"))
        for name in [key for key in sys.modules if key == "project_control"]:
            del sys.modules[name]
        try:
            import project_control as controller
        finally:
            sys.path.pop(0)
        target = root / "reports/concurrency.txt"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("origine\n", encoding="utf-8")
        transaction = controller.FileTransaction(root)
        transaction.write_text("reports/concurrency.txt", "écrit par la transaction\n")
        # Someone else writes and keeps that write: the file no longer holds what we wrote.
        target.write_text("committé par l'autre session\n", encoding="utf-8")
        transaction.rollback()
        self.assertEqual(target.read_text(encoding="utf-8"), "committé par l'autre session\n",
                         "an aborted transaction must not erase another session's work")
        self.assertIn(str(target), transaction.abandoned)
        # Its own writes, untouched by anyone, are still undone.
        second = controller.FileTransaction(root)
        second.write_text("reports/concurrency.txt", "seconde écriture\n")
        second.rollback()
        self.assertEqual(target.read_text(encoding="utf-8"), "committé par l'autre session\n")
        self.assertEqual(second.abandoned, [])

    def test_a_project_without_its_gitignore_is_refused_before_it_breaks(self) -> None:
        """Copying the visible entries of the template leaves `.gitignore` behind — its name starts
        with a dot. Initialization used to complete without it, and the project broke afterwards:
        the first generated view wrote an HTML page nothing ignored. It is required now, so it is
        refused in the one place a newcomer is still reading the instructions, and it may be written
        during initialization instead of being forbidden there."""
        temporary, root = self.make_copy()
        self.addCleanup(temporary.cleanup)
        # Removing `.gitignore` would also unmask whatever the template ignores; that is not what
        # this test measures, so the copy is emptied of it first.
        discard_ignored_files(root)
        removed = run_git(root, "rm", "-q", "--cached", "--", ".gitignore")
        self.assertEqual(removed.returncode, 0, removed.stdout + removed.stderr)
        (root / ".gitignore").unlink()
        refused = run_control(root, "bootstrap-audit")
        self.assertNotEqual(refused.returncode, 0, "the audit must say it before the project breaks")
        self.assertIn("FAIL: MANDATORY_FILES", refused.stdout)
        self.assertIn(".gitignore", refused.stdout)
        self.assertNotIn("FAIL: BOOTSTRAP_CHANGE_SCOPE", refused.stdout, "only the missing file is refused")
        # And an agent may write it during initialization, where it used to be forbidden.
        (root / ".gitignore").write_text("__pycache__/\nreports/roadmap/*.html\n", encoding="utf-8")
        declared = run_control(root, "bootstrap-preflight", "--path", ".gitignore")
        self.assertEqual(declared.returncode, 0, declared.stdout + declared.stderr)
        staged = run_git(root, "add", "--", ".gitignore")
        self.assertEqual(staged.returncode, 0, staged.stdout + staged.stderr)
        accepted = run_control(root, "bootstrap-audit")
        self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)

    def test_a_merge_passenger_hidden_from_the_disk_is_still_refused(self) -> None:
        """The passenger the test above refuses while it is visible was let through by deleting it
        from the disk and leaving its content in the index. The gate compared HEAD to the working
        tree, which no longer held it — while the commit carries the index, which still did. What
        the merge would write is the index, and that is what has to be read."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        self.install_commit_hook(root)
        item = self.create_and_start_lifecycle_work_item(
            root, "WI-001", "HD-102", authorized_path="modules/allowed", code="APPLICABLE",
        )
        (root / "modules/allowed").mkdir(parents=True, exist_ok=True)
        (root / "modules/allowed/feature.py").write_text("VALUE = 1\n", encoding="utf-8")
        run_git(root, "add", "--", "modules/allowed/feature.py")
        committed = run_git(root, "commit", "-q", "-m", "feat: the authorized work")
        self.assertEqual(committed.returncode, 0, committed.stdout + committed.stderr)
        self.switch_to_canonical(root)
        merged = run_git(root, "merge", "--no-commit", "--no-ff", str(item["branch"]))
        self.assertEqual(merged.returncode, 0, merged.stdout + merged.stderr)
        passenger = root / "modules/not-authorized/passenger.py"
        passenger.parent.mkdir(parents=True, exist_ok=True)
        passenger.write_text("SMUGGLED = 1\n", encoding="utf-8")
        run_git(root, "add", "--", "modules/not-authorized/passenger.py")
        # Hidden from the disk, kept in the index: this is exactly what the commit would write.
        passenger.unlink()
        refused = run_control(root, "pre-commit")
        self.assertNotEqual(refused.returncode, 0, "the index is what the merge commit carries")
        self.assertIn("an integration merge carries only what its branch changed", refused.stdout)
        self.assertIn("modules/not-authorized/passenger.py", refused.stdout)
        head_before = run_git(root, "rev-parse", "HEAD").stdout
        blocked = run_git(root, "commit", "--no-edit", "-q")
        self.assertNotEqual(blocked.returncode, 0, "and the real commit is refused too")
        self.assertEqual(run_git(root, "rev-parse", "HEAD").stdout, head_before)
        # Removed from the index as well, the plain integration lands.
        run_git(root, "rm", "-f", "--quiet", "--ignore-unmatch", "--cached", "--", "modules/not-authorized/passenger.py")
        landed = run_git(root, "commit", "--no-edit", "-q")
        self.assertEqual(landed.returncode, 0, landed.stdout + landed.stderr)

    def test_an_integration_merge_edited_under_a_name_git_quotes_is_refused(self) -> None:
        """The content rule read the paths of a merge from `git diff --name-only`, which quotes
        and escapes a name it finds unusual — an accent, a tab. Under `"r\\303\\251sum\\303\\251.py"`
        no blob could be found on either side, two empty answers compared equal, and a value
        added to the merge result under that name was committed as integration, audit green
        (fifth independent control, F-02). Paths are now read as the files are named, and a
        lookup that fails refuses instead of comparing. Same edit, same names: refused; the
        merge unedited still lands, with what the branch produced."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        run_git(root, "config", "core.quotePath", "true")  # Git's default, pinned against local settings
        self.install_commit_hook(root)
        item = self.create_and_start_lifecycle_work_item(
            root, "WI-001", "HD-102", authorized_path="modules/noms", code="APPLICABLE",
        )
        names = ["modules/noms/a\tb.py", "modules/noms/résumé.py"]
        (root / "modules/noms").mkdir(parents=True, exist_ok=True)
        for name in names:
            (root / name).write_text('VALUE = "FROM_AUTHORIZED_BRANCH"\n', encoding="utf-8")
        staged = run_git(root, "add", "--", *names)
        self.assertEqual(staged.returncode, 0, staged.stdout + staged.stderr)
        committed = run_git(root, "commit", "-q", "-m", "feat: two files Git will quote")
        self.assertEqual(committed.returncode, 0, committed.stdout + committed.stderr)
        self.switch_to_canonical(root)
        opened = run_git(root, "merge", "--no-commit", "--no-ff", str(item["branch"]))
        self.assertEqual(opened.returncode, 0, opened.stdout + opened.stderr)
        gate = run_control(root, "pre-commit")
        self.assertEqual(gate.returncode, 0, gate.stdout + gate.stderr)
        # The reviewer's edit: only the value changes, under names Git renders escaped.
        for name in names:
            (root / name).write_text('VALUE = "ADDED_DURING_MERGE"\n', encoding="utf-8")
        staged = run_git(root, "add", "--", *names)
        self.assertEqual(staged.returncode, 0, staged.stdout + staged.stderr)
        refused = run_control(root, "pre-commit")
        self.assertNotEqual(refused.returncode, 0, "an edit under a quoted name is still an edit")
        self.assertIn(f"the merge result differs from the branch for: {sorted(names)}", refused.stdout)
        head_before = run_git(root, "rev-parse", "HEAD").stdout
        blocked = run_git(root, "commit", "--no-edit", "-q")
        self.assertNotEqual(blocked.returncode, 0, "and the real commit is refused too")
        self.assertEqual(run_git(root, "rev-parse", "HEAD").stdout, head_before)
        # Restored to what the branch produced, the same integration lands.
        restored = run_git(root, "restore", "--source=MERGE_HEAD", "--staged", "--worktree", "--", *names)
        self.assertEqual(restored.returncode, 0, restored.stdout + restored.stderr)
        landed = run_git(root, "commit", "--no-edit", "-q")
        self.assertEqual(landed.returncode, 0, landed.stdout + landed.stderr)
        for name in names:
            self.assertEqual(run_git(root, "show", f"HEAD:{name}").stdout, 'VALUE = "FROM_AUTHORIZED_BRANCH"\n')

    def test_a_closure_accepts_the_authorized_commit_of_a_file_git_quotes(self) -> None:
        """`close --commit` listed the paths a commit touched the same way, and a commit that
        wrote exactly the authorized `modules/noms/résumé.py` was refused as touching nothing the
        Work Item was authorized to change — until `core.quotePath` was switched off locally
        (fifth independent control, F-04). Whether a closure is honest cannot depend on a local
        display setting: read as named, the path is the authorized one and the closure is DONE."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        run_git(root, "config", "core.quotePath", "true")
        name = "modules/noms/résumé.py"
        created = self.create_lifecycle_work_item(
            root, "WI-001", "HD-102", authorized_path=name, code="APPLICABLE",
            tests="NOT_APPLICABLE", integration="NOT_APPLICABLE",
        )
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        started = self.start_command(root, "WI-001")
        self.assertEqual(started.returncode, 0, started.stdout + started.stderr)
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_text('VALUE = "FROM_AUTHORIZED_BRANCH"\n', encoding="utf-8")
        commit = self.commit_fixture(root, "feat: the authorized file, accent included")
        self.switch_to_canonical(root)
        merged = run_git(root, "merge", "--ff-only", str(load_json(root / "project_control/work-items/WI-001.json")["branch"]))
        self.assertEqual(merged.returncode, 0, merged.stdout + merged.stderr)
        closed = run_control(root, "close", "WI-001", "--commit", commit)
        self.assertEqual(closed.returncode, 0, closed.stdout + closed.stderr)
        record = load_json(root / "project_control/work-items/WI-001.json")
        self.assertEqual(record["status"], "DONE")
        self.assertEqual(record["commits"], [commit])
        audit = run_control(root, "audit")
        self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)

    def test_a_rename_on_the_branch_merges_with_a_canonical_change_to_the_old_name(self) -> None:
        """A branch renames a file it is authorized on, without changing a line; meanwhile the
        canonical branch changes the first line of that file under its old name. Git merges the
        two correctly — the change lands in the renamed file — and the content rule refused the
        result: the renamed file's blob was not the branch's, and the old name, changed on the
        canonical side, was not linked to the new one (fifth independent control, F-03). A
        rename is one change with two names; a canonical change to either is a change to the
        path, and Git's result is a resolution, integrated as such."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        old_name, new_name = "docs/merge-fixture/file.txt", "docs/merge-fixture/renamed.txt"
        (root / old_name).parent.mkdir(parents=True, exist_ok=True)
        (root / old_name).write_text("one\ntwo\nthree\n", encoding="utf-8")
        self.commit_fixture(root, "fixture: a file the branch will rename")
        item = self.create_and_start_lifecycle_work_item(
            root, "WI-001", "HD-102", authorized_path="docs/merge-fixture", code="APPLICABLE",
        )
        moved = run_git(root, "mv", "--", old_name, new_name)
        self.assertEqual(moved.returncode, 0, moved.stdout + moved.stderr)
        self.commit_fixture(root, "refactor: rename without changing a line")
        self.switch_to_canonical(root)
        (root / old_name).write_text("ONE\ntwo\nthree\n", encoding="utf-8")
        self.commit_fixture(root, "fixture: a canonical change to the old name")
        self.install_commit_hook(root)
        opened = run_git(root, "merge", "--no-commit", "--no-ff", str(item["branch"]))
        self.assertEqual(opened.returncode, 0, opened.stdout + opened.stderr)
        self.assertEqual((root / new_name).read_text(encoding="utf-8"), "ONE\ntwo\nthree\n", "Git followed the rename")
        self.assertFalse((root / old_name).exists())
        gate = run_control(root, "pre-commit")
        self.assertEqual(gate.returncode, 0, gate.stdout + gate.stderr)
        landed = run_git(root, "commit", "--no-edit", "-q")
        self.assertEqual(landed.returncode, 0, landed.stdout + landed.stderr)
        self.assertEqual(run_git(root, "show", f"HEAD:{new_name}").stdout, "ONE\ntwo\nthree\n")
        self.assertNotEqual(run_git(root, "cat-file", "-e", f"HEAD:{old_name}").returncode, 0)

    def test_a_frozen_agent_run_loses_its_exemption_when_it_is_rewritten(self) -> None:
        """The adoption baseline freezes a state, not a list of names: an exemption granted by
        name would travel with the name to work done today."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        adoption = run_git(root, "rev-parse", "HEAD").stdout.strip()
        self.declare_legacy_baseline(root, adoption, "HD-105")
        self.create_and_start_lifecycle_work_item(root, "WI-001", "HD-102")
        self.switch_to_canonical(root)
        run_path = root / "project_control/agent-runs/RUN-WI-001-001.json"
        run = load_json(run_path)
        run.pop("authorities_read")
        run_path.write_text(json.dumps(run, indent=2) + "\n", encoding="utf-8")
        frozen = self.commit_fixture(root, "fixture: Agent Run without proof of reading")
        self.declare_authorities_baseline(root, frozen, "HD-107")
        self.assertEqual(run_control(root, "audit").returncode, 0, "the frozen run is exempt as it stands")
        # Rewritten, the same file is no longer the history that was frozen.
        rewritten = load_json(run_path)
        rewritten["work_item_id"] = "WI-001"
        rewritten["started_at"] = "2099-01-01T00:00:00Z"
        run_path.write_text(json.dumps(rewritten, indent=2) + "\n", encoding="utf-8")
        self.commit_fixture(root, "fixture: rewrite the exempt Agent Run")
        refused = run_control(root, "audit")
        self.assertNotEqual(refused.returncode, 0, refused.stdout)
        self.assertIn("authorities_read is required", refused.stdout)
        self.assertIn("no longer historical", refused.stdout)

    def test_a_refused_view_write_leaves_the_page_untouched(self) -> None:
        """`roadmap-view --write` announces read-only when it refuses; it must not have rewritten
        the page on its way to that refusal."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        written = run_control(root, "roadmap-view", "--write")
        self.assertEqual(written.returncode, 0, written.stdout + written.stderr)
        page = root / self.VIEW_HTML
        self.assertTrue(page.is_file(), page)
        before = page.read_bytes()
        # From a Work Item branch the committed view is refused; nothing at all may be written.
        self.create_and_start_lifecycle_work_item(root, "WI-001", "HD-102")
        refused = run_control(root, "roadmap-view", "--write")
        self.assertNotEqual(refused.returncode, 0, refused.stdout)
        self.assertIn("canonical branch divergence", refused.stdout)
        self.assertEqual(page.read_bytes(), before, "a refusal writes nothing, not even the untracked page")

    def test_the_language_is_chosen_by_the_project_owner_like_the_reporting_style(self) -> None:
        """The controller speaks the language the Project Owner chose. Nothing is assumed: until the
        question is answered the choice is UNKNOWN, and the initialization cannot close."""
        temporary, root = self.make_copy()
        self.addCleanup(temporary.cleanup)
        state_path = root / "project_control/project-state.v1.json"
        self.assertEqual(load_json(state_path)["language"], "UNKNOWN", "a new copy assumes no language")
        audit = run_control(root, "bootstrap-audit")
        self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)
        self.assertIn("PASS: LANGUAGE — language=UNKNOWN", audit.stdout)
        # UNKNOWN blocks the closeout exactly as an unchosen reporting style does.
        state = load_json(state_path)
        state["language"] = "UNKNOWN"
        state["reporting_style"] = "PLAIN"
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        refused = run_control(root, "bootstrap-closeout", "--path", "FIRST_START.md")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("closeout requires the Project Owner's language (FR or EN)", refused.stdout)
        # An unknown value is refused by the schema, like any closed vocabulary.
        state["language"] = "ESPERANTO"
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        invalid = run_control(root, "bootstrap-audit")
        self.assertNotEqual(invalid.returncode, 0)
        self.assertIn("project-state.language: invalid enum value 'ESPERANTO'", invalid.stdout)

    def test_status_speaks_the_chosen_language_and_the_check_names_never_do(self) -> None:
        """Prose addressed to a human follows the choice; identifiers do not. A check name or a
        refusal message that changed with the language would break every tool that reads them."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        state_path = root / "project_control/project-state.v1.json"
        state = load_json(state_path)
        self.assertEqual(state["language"], "FR", "the fixture project speaks French")
        french = run_control(root, "status")
        self.assertEqual(french.returncode, 0, french.stdout + french.stderr)
        self.assertIn("Projet : ", french.stdout)
        self.assertIn("Langue : français (FR)", french.stdout)
        state["language"] = "EN"
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        english = run_control(root, "status")
        self.assertEqual(english.returncode, 0, english.stdout + english.stderr)
        self.assertIn("Project: ", english.stdout)
        self.assertIn("Language: english (EN)", english.stdout)
        self.assertNotIn("Projet : ", english.stdout)
        self.assertNotIn("Contrôles : ", english.stdout)
        # The audit says the same thing in both languages: its vocabulary is not prose.
        for expected in ("PASS: LANGUAGE", "PASS: REPORTING_STYLE", "PASS: CORE_MANIFEST"):
            self.assertIn(expected, run_control(root, "audit").stdout, expected)
        refused = run_control(root, "core-manifest", "--write", "--version", "1.0.0")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("reserved to the template", refused.stdout + refused.stderr,
                      "refusal messages are identifiers of behaviour, not prose: they stay in English")

    def test_the_roadmap_view_follows_the_language_and_never_translates_the_owner(self) -> None:
        """The view is written in the chosen language — but the Project Owner's own words are
        shown as he wrote them: the view displays, it does not rewrite him."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        quote = "Une idée que le Project Owner a dite en français"
        added = run_control(root, "idea", "add", "--quote", quote, "--source", "fixture")
        self.assertEqual(added.returncode, 0, added.stdout + added.stderr)
        written = run_control(root, "roadmap-view", "--write")
        self.assertEqual(written.returncode, 0, written.stdout + written.stderr)
        french = (root / self.VIEW_MARKDOWN).read_text(encoding="utf-8")
        self.assertIn("## Maintenant", french)
        self.assertIn("## Vérification", french)
        state_path = root / "project_control/project-state.v1.json"
        state = load_json(state_path)
        state["language"] = "EN"
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        self.commit_fixture(root, "fixture: the Project Owner switches to English")
        again = run_control(root, "roadmap-view", "--write")
        self.assertEqual(again.returncode, 0, again.stdout + again.stderr)
        english = (root / self.VIEW_MARKDOWN).read_text(encoding="utf-8")
        self.assertIn("## Right now", english)
        self.assertIn("## Verification", english)
        self.assertNotIn("## Maintenant", english)
        self.assertNotIn("## Vérification", english)
        self.assertIn(quote, english, "the Project Owner's own words are never translated")
        page = (root / self.VIEW_HTML).read_text(encoding="utf-8")
        self.assertIn("What awaits you", page)
        self.assertNotIn("Ce qui t’attend", page)

    def test_the_gate_judges_what_the_commit_would_create_not_the_working_tree(self) -> None:
        """The gate announced "the staged state" while reading the files on disk. They are not the
        same thing: an index can hold a falsified record while the file on disk is clean, and the
        commit carries the index."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        self.install_commit_hook(root)
        path = root / "docs/governance/roadmap-state.v1.json"
        honest = path.read_text(encoding="utf-8")
        falsified = json.loads(honest)
        falsified["work_items"] = falsified.get("work_items", []) + [{
            "work_item_id": "WI-999", "display_reference": "X-999", "title": "a Work Item nobody authorized",
            "status": "DONE", "integration_state": "HISTORICAL", "human_gate": "HD-999",
        }]
        path.write_text(json.dumps(falsified, indent=2) + "\n", encoding="utf-8")
        staged = run_git(root, "add", "--", "docs/governance/roadmap-state.v1.json")
        self.assertEqual(staged.returncode, 0, staged.stdout + staged.stderr)
        path.write_text(honest, encoding="utf-8")  # the file on disk is honest again
        self.assertIn("WI-999", run_git(root, "show", ":docs/governance/roadmap-state.v1.json").stdout)
        self.assertNotIn("WI-999", path.read_text(encoding="utf-8"))
        gate = run_control(root, "pre-commit")
        self.assertNotEqual(gate.returncode, 0, gate.stdout)
        self.assertIn("in the staged state", gate.stdout)
        self.assertIn("WI-999", gate.stdout)
        head_before = run_git(root, "rev-parse", "HEAD").stdout
        refused = run_git(root, "commit", "-q", "-m", "a record the working tree does not show")
        self.assertNotEqual(refused.returncode, 0, "the gate must refuse the real commit too")
        self.assertEqual(run_git(root, "rev-parse", "HEAD").stdout, head_before)

    def test_a_refused_creation_leaves_no_half_staged_index(self) -> None:
        """A project that ignores `*.json` is ordinary. Its records are Project Control's own and
        must be staged whatever the project ignores; and a failure must restore the index, not
        only the files."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        self.install_commit_hook(root)
        ignore = root / ".gitignore"
        ignore.write_text(ignore.read_text(encoding="utf-8") + "\n*.json\n", encoding="utf-8")
        run_git(root, "add", "--", ".gitignore")
        committed = subprocess.run(
            ["git", "commit", "-q", "-m", "fixture: a broad .gitignore, as many real projects have"],
            cwd=root, check=False, capture_output=True, text=True,
            env=dict(os.environ, PROJECT_CONTROL_HOOK_OVERRIDE="fixture: the project's own .gitignore"),
        )
        self.assertEqual(committed.returncode, 0, committed.stdout + committed.stderr)
        created = self.create_lifecycle_work_item(root, "WI-001", "HD-102")
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        self.assertEqual(run_git(root, "status", "--porcelain=v1").stdout, "", "no residue in index or worktree")
        self.assertTrue((root / "project_control/work-items/WI-001.json").is_file())
        self.assertIn("WI-001", run_git(root, "show", "HEAD:project_control/work-items/WI-001.json").stdout,
                      "the record the roadmap cites is in the commit")
        self.assertEqual(run_control(root, "audit").returncode, 0)

    def test_a_commit_that_predates_the_work_item_is_not_its_development_proof(self) -> None:
        """`close` recorded any commit that existed and was an ancestor of HEAD. The repository's
        very first commit satisfied both, and closed the Work Item as DEVELOPED."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        oldest = run_git(root, "rev-list", "--max-parents=0", "HEAD").stdout.split()[0]
        item = self.create_and_start_lifecycle_work_item(
            root, "WI-001", "HD-102", authorized_path="modules/allowed", code="APPLICABLE",
        )
        (root / "modules/allowed").mkdir(parents=True, exist_ok=True)
        (root / "modules/allowed/feature.py").write_text("VALUE = 1\n", encoding="utf-8")
        run_git(root, "add", "--", "modules/allowed/feature.py")
        self.assertEqual(run_git(root, "commit", "-q", "-m", "feat: the authorized work").returncode, 0)
        real = run_git(root, "rev-parse", "HEAD").stdout.strip()
        self.switch_to_canonical(root)
        self.merge_fixture_branch(root, item["branch"], "fixture: integrate WI-001")
        evidence = self.write_committed_evidence(root, "WI-001")
        refused = self.close_with_evidence_and_commit(root, "WI-001", evidence, oldest)
        self.assertNotEqual(refused.returncode, 0, refused.stdout)
        self.assertIn("commit predates the Work Item", refused.stdout)
        record = load_json(root / "project_control/work-items/WI-001.json")
        self.assertEqual(record["status"], "IN_PROGRESS", "a refused close changes nothing")
        # The commit of the authorized work closes it, as it always did.
        closed = self.close_with_evidence_and_commit(root, "WI-001", evidence, real)
        self.assertEqual(closed.returncode, 0, closed.stdout + closed.stderr)
        closed_record = load_json(root / "project_control/work-items/WI-001.json")
        self.assertEqual(closed_record["status"], "DONE")
        self.assertEqual(closed_record["commits"], [real])

    def test_an_up_to_date_backup_reads_as_good_in_both_languages(self) -> None:
        """The banner tested a French prefix of a translated label: in English an identical
        backup was flagged as an alert."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        bare = Path(tempfile.mkdtemp(prefix="skeleton-backup-")) / "backup.git"
        self.addCleanup(shutil.rmtree, str(bare.parent), True)
        self.assertEqual(run_git(root, "init", "--bare", "--quiet", str(bare)).returncode, 0)
        self.assertEqual(run_git(root, "remote", "add", "backup", str(bare)).returncode, 0)
        self.assertEqual(run_git(root, "push", "--quiet", "backup", "main").returncode, 0)
        state_path = root / "project_control/project-state.v1.json"
        for language, label in (("FR", "identiques"), ("EN", "identical")):
            state = load_json(state_path)
            state["language"] = language
            state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
            view = json.loads(run_control(root, "roadmap-view", "--json").stdout)
            banner = {row[0]: row for row in view["verification"]["banner"]}
            row = next(row for key, row in banner.items() if row[1].startswith(label))
            self.assertEqual(row[2], "ok", f"{language}: an up-to-date backup is not an alert — {row}")

    def test_the_view_adds_no_french_of_its_own_to_an_english_rendering(self) -> None:
        """The virtual source of the version tags was a French string hard-coded by the controller
        — its own prose, not the Project Owner's words."""
        temporary, root = self.make_normal_copy()
        self.addCleanup(temporary.cleanup)
        state_path = root / "project_control/project-state.v1.json"
        state = load_json(state_path)
        state["language"] = "EN"
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        view = json.loads(run_control(root, "roadmap-view", "--json").stdout)
        paths = [entry["path"] for entry in view["verification"]["sources"]]
        self.assertIn("(repository version tags)", paths)
        self.assertNotIn("(versions taguées du dépôt)", paths)

    def test_hello_squelette_transcript_and_readme_block_match_the_controller(self) -> None:
        """The demo replays one governed change in a temporary copy; its committed transcript and the
        README block must be exactly what the controller prints today, or the maintainer regenerates
        them (`demo.py --write`). Only the template replays itself: a derived project skips."""
        demo = ROOT / "examples/hello-squelette/demo.py"
        state = load_json(ROOT / "project_control/project-state.v1.json")
        if not demo.exists() or state.get("repository_role") != "PROJECT_TEMPLATE":
            self.skipTest("hello-squelette is replayed from the template itself only")
        if shutil.which("python3") is None:
            self.skipTest("the commit hook installed by the demo needs python3 on PATH")
        checked = subprocess.run(
            [sys.executable, "-B", str(demo), "--check"], cwd=ROOT, check=False, capture_output=True, text=True,
        )
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        self.assertIn("match the controller's output", checked.stdout)


if __name__ == "__main__":
    unittest.main()
