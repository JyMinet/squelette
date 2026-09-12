#!/usr/bin/env python3
"""Fail-closed governance and transactional Work Item lifecycle controls.

Audit and preflight commands are read-only. Lifecycle commands mutate only the
explicit governance records they own and roll those writes back on failure.
"""

from __future__ import annotations

import argparse
import contextlib
from datetime import date, datetime, timezone
import fcntl
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import shutil
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import IO, AbstractSet, Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]

WORK_ITEM_ID = re.compile(r"^WI-[0-9]{3,}$")
HUMAN_DECISION_ID = re.compile(r"^HD-[0-9]{3,}$")
# A baseline is anchored to the decision that declares it: the decision names the commit, and
# the controller refuses a declaration whose commit is not the one its decision cites. A decision
# that authorised line A can no longer be used to declare line B (P17). Removing a baseline is a
# gesture of its own, named the same way.
BASELINE_DECISION_FIELDS = {
    "legacy_baseline": ("Legacy baseline commit", "Legacy baseline removed"),
    "authorities_baseline": ("Authorities baseline commit", "Authorities baseline removed"),
}
SHA40 = re.compile(r"^[a-f0-9]{40}$")
PROJECT_KEY = re.compile(r"^[A-Z][A-Z0-9_-]{0,31}$")
RECORD_REFERENCE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
BRANCH_NAME = re.compile(r"^(?![./])(?!.*(?:\.\.|//|@\{|\\))[A-Za-z0-9._/-]+(?<![./])$")

REASON_CODE = re.compile(r"^[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)*$")
AGENT_RUN_REFERENCE = re.compile(r"^RUN-[A-Za-z0-9._-]+$")
BUSINESS_ROOTS = ("applications", "modules", "shared")
BLOCK_RECORD_FIELDS = {
    "type", "reason_code", "blocked_at", "human_decision_id", "agent_run_ref",
    "resume_condition", "resolved_at", "resolution_human_decision_id",
}

WORK_ITEM_STATUSES = {
    "PROPOSED", "AUTHORIZED", "IN_PROGRESS", "IMPLEMENTED", "INTEGRATED",
    "DEPLOYED", "RUNTIME_PROVEN", "DONE", "BLOCKED", "REJECTED", "SUPERSEDED",
}
PREFLIGHT_STATUSES = {"AUTHORIZED", "IN_PROGRESS"}
INTEGRATION_STATES = {"UNMERGED", "ACTIVE_WORK", "INTEGRATED", "HISTORICAL"}
CONFLICT_STATES = {"INDEPENDENT", "DEPENDENT", "OVERLAPPING", "CONFLICTING"}
APPLICABILITY = {"APPLICABLE", "NOT_APPLICABLE", "UNKNOWN"}
IMPACT_FIELDS = (
    "direct_impact", "indirect_impact", "authority_impact", "concurrent_work_impact",
)
EVIDENCE_GATES = ("tests", "integration", "deployment", "runtime_proof")
RUNTIME_TARGETS = {"NOT_APPLICABLE", "CONTROLLED_NON_PRODUCTION_RUNTIME", "PRODUCTION"}

HOOKS_PATH = "scripts/hooks"

# The versioned core of the template (TPL-D-007): what template-upgrade updates and
# verifies in a derived project. Everything else belongs to the project.
CORE_ROOTS = (
    "CLAUDE.md", "FIRST_START.md", "ADOPTION.md", "scripts", "tests/test_template.py",
    "tests/fixtures/project_control", "project_control/schemas", "project_control/README.md",
    "docs/governance/DEFINITION_OF_DONE.md", "docs/agent-governance/AGENTS.core.md",
    "docs/agent-governance/ROADMAP_VIEW.md",
)
CORE_MANIFEST_PATH = "provenance/core-manifest.v1.json"
HUMAN_DECISIONS_PATH = "docs/governance/HUMAN_DECISIONS.md"

# Routed authorities per affected scope (P3): the scopes of a Work Item are derived from its
# authorized paths; a path may fall into several scopes. Base authorities always apply.
PATH_SCOPES = (
    ("applications/", "development"), ("modules/", "development"), ("shared/", "development"),
    ("scripts/", "development"), ("tests/", "development"), ("project_control/", "development"),
    ("contracts/", "contracts"), ("data/", "data"),
    ("docs/governance/", "governance"), ("docs/adr/", "governance"), ("docs/agent-governance/", "governance"),
    ("docs/architecture/", "architecture"),
    ("runtime_proof/", "runtime"), ("project_control/deployments/", "runtime"),
)
# Routed for reading but kept by Project Control itself, hence excluded from the proof of
# reading: every transition would otherwise invalidate the manifest. Human Decisions stay in.
MANIFEST_EXCLUDED_PATHS = {
    "docs/governance/ROADMAP.md",
    "docs/governance/roadmap-state.v1.json",
    "docs/governance/WORKTREE_REGISTRY.md",
    "docs/governance/git-path-classifications.v1.json",
    "project_control/project-state.v1.json",
    "docs/governance/IDEAS.md",
    "docs/governance/ideas-state.v1.json",
    "docs/governance/ROADMAP_VIEW.md",
    "project_control/roadmap-view.v1.json",
}

# The generated roadmap view (P12, P6): the Project Owner's ideas live in two synchronized
# forms like the roadmap; the view itself is computed from the repository's files and
# never decides anything. The template keeps its own roadmap under provenance/.
IDEA_ID = re.compile(r"^ID-[0-9]{3,}$")
IDEA_STATES = (
    "EVOKED", "TO_CLARIFY", "TO_SET", "SCOPED", "PLANNED", "IN_PROGRESS",
    "REALIZED", "APPLIED", "INTEGRATED", "LATER", "DISCARDED",
)
IDEAS_JSON_PATH = "docs/governance/ideas-state.v1.json"
IDEAS_MD_PATH = "docs/governance/IDEAS.md"
VIEW_SETTINGS_PATH = "project_control/roadmap-view.v1.json"
VIEW_MARKDOWN_PATH = "docs/governance/ROADMAP_VIEW.md"
VIEW_HTML_PATH = "reports/roadmap/ROADMAP.html"
TEMPLATE_ROADMAP_PATH = "provenance/roadmap-template.v1.json"
# Not a file: the entry that carries the Git state the generated view displays.
VERSION_TAGS_SOURCE = "(repository version tags)"
TEMPLATE_VIEW_SETTINGS_PATH = "provenance/roadmap-view.v1.json"
TEMPLATE_VIEW_MARKDOWN_PATH = "provenance/ROADMAP_VIEW.md"
TEMPLATE_VIEW_HTML_PATH = "provenance/roadmap/ROADMAP.html"
REGENERATION_LABELS = {
    "OFF": "non (à la demande)", "HOURLY": "toutes les heures", "EVERY_4_HOURS": "toutes les 4 heures", "DAILY": "chaque jour",
}
VERSION_TAG = re.compile(r"^v?([0-9]+)\.([0-9]+)\.([0-9]+)$")
AGENTS_CORE_PATH = "docs/agent-governance/AGENTS.core.md"
SKELETON_VERSION = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
SHA256_HEX = re.compile(r"^[a-f0-9]{64}$")


def evidence_directory(work_item_id: str) -> str:
    return f"reports/evidence/{work_item_id}"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


INITIALIZATION_MARKER = re.compile(rb"INITIALIZATION_STATUS:[ \t]*(NOT_STARTED|COMPLETE)")


def core_digest(root: Path, path: str) -> str:
    """SHA-256 of a core file as the manifest records it.

    FIRST_START.md is core doctrine that also carries the project's own initialization
    marker; the marker is normalized before hashing so that initializing a project does
    not count as modifying the core, and template-upgrade preserves it when writing."""
    content = (root / path).read_bytes()
    if path == "FIRST_START.md":
        content = INITIALIZATION_MARKER.sub(b"INITIALIZATION_STATUS: <PROJECT>", content, count=1)
    return hashlib.sha256(content).hexdigest()


def upgraded_content(root: Path, source: Path, path: str) -> bytes:
    """Bytes template-upgrade writes for a core path: the source file, with the project's
    initialization marker kept in FIRST_START.md."""
    content = (source / path).read_bytes()
    if path == "FIRST_START.md" and (root / path).is_file():
        local_marker = INITIALIZATION_MARKER.search((root / path).read_bytes())
        if local_marker is not None:
            content = INITIALIZATION_MARKER.sub(local_marker.group(0), content, count=1)
    return content


def blob_digest(content: bytes) -> str:
    """The identifier Git gives a blob holding `content` — comparable to `git rev-parse REV:path`."""
    return hashlib.sha1(b"blob " + str(len(content)).encode("ascii") + b"\0" + content).hexdigest()


def core_files(root: Path) -> list[str]:
    """Repository-relative core paths present under CORE_ROOTS, sorted, without caches."""
    files: list[str] = []
    for entry in CORE_ROOTS:
        path = root / entry
        if path.is_file():
            files.append(entry)
        elif path.is_dir():
            files.extend(
                child.relative_to(root).as_posix()
                for child in sorted(path.rglob("*"))
                if child.is_file() and "__pycache__" not in child.parts and child.suffix != ".pyc"
            )
    return sorted(files)


def build_core_manifest(root: Path, version: str) -> dict[str, Any]:
    if not SKELETON_VERSION.fullmatch(version):
        raise ProjectControlError(f"skeleton version must be MAJOR.MINOR.PATCH, got {version!r}")
    return {
        "schema_version": "1.0.0",
        "skeleton_version": version,
        "core": {path: core_digest(root, path) for path in core_files(root)},
    }


def load_core_manifest(root: Path) -> dict[str, Any]:
    """The committed core manifest of a tree, shape-validated; never inferred."""
    payload = load_json(root / CORE_MANIFEST_PATH)
    if not isinstance(payload, dict) or payload.get("schema_version") != "1.0.0":
        raise ProjectControlError(f"invalid core manifest: schema_version must be 1.0.0 ({CORE_MANIFEST_PATH})")
    version = payload.get("skeleton_version")
    if not isinstance(version, str) or not SKELETON_VERSION.fullmatch(version):
        raise ProjectControlError(f"invalid core manifest: skeleton_version must be MAJOR.MINOR.PATCH ({CORE_MANIFEST_PATH})")
    core = payload.get("core")
    if not isinstance(core, dict) or not core or any(
        not isinstance(path, str) or safe_relative_path(path) != path
        or not isinstance(digest, str) or not SHA256_HEX.fullmatch(digest)
        for path, digest in core.items()
    ):
        raise ProjectControlError(f"invalid core manifest: core must map safe paths to SHA-256 digests ({CORE_MANIFEST_PATH})")
    return payload


def core_drift(root: Path, manifest: dict[str, Any]) -> dict[str, str]:
    """Core paths whose tree state differs from the manifest: MISSING or MODIFIED_LOCALLY."""
    drift: dict[str, str] = {}
    for path, digest in sorted(manifest["core"].items()):
        local = root / path
        if not local.is_file() or local.is_symlink():
            drift[path] = "MISSING"
        elif core_digest(root, path) != digest:
            drift[path] = "MODIFIED_LOCALLY"
    return drift


def version_tuple(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("."))


def scopes_for_paths(paths: Iterable[str]) -> list[str]:
    """The scopes an authorization touches — those it sits in, and those it contains.

    Authorizing a parent directory grants writing over every scope below it: the proof of
    reading has to cover them too, otherwise the right to write is wider than the duty to read.
    """
    scopes: set[str] = set()
    for raw in paths:
        path = safe_relative_path(str(raw)) or ""
        if not path:
            continue
        for prefix, scope in PATH_SCOPES:
            inside = path == prefix.rstrip("/") or path.startswith(prefix)
            contains = prefix.startswith(path.rstrip("/") + "/")
            if inside or contains:
                scopes.add(scope)
    return sorted(scopes)


def manifest_digest(entries: Sequence[dict[str, str]]) -> str:
    lines = "".join(f"{entry['path']} {entry['sha256']}\n" for entry in sorted(entries, key=lambda e: e["path"]))
    return hashlib.sha256(lines.encode("utf-8")).hexdigest()


def gate_levels(runtime_target: str) -> dict[str, str]:
    controlled = runtime_target == "CONTROLLED_NON_PRODUCTION_RUNTIME"
    return {
        "tests": "TESTED", "integration": "INTEGRATED",
        "deployment": "DEPLOYED_IN_CONTROLLED_ENVIRONMENT" if controlled else "DEPLOYED",
        "runtime_proof": "RUNTIME_PROVEN" if controlled else "PRODUCTION_VERIFIED",
    }

LANGUAGES = {"FR", "EN"}


def speak(language: str, key: str, **values: Any) -> str:
    """The one sentence `key` names, written in `language`.

    Only prose addressed to the Project Owner lives here. Check names, report lines and refusal
    messages are identifiers, not text: they stay in English, whatever the chosen language."""
    entry = SPEECH.get(key)
    if entry is None:
        return key
    return entry.get(language, entry["FR"]).format(**values)


SPEECH: dict[str, dict[str, str]] = {
    # --- status ---------------------------------------------------------------------
    "status.project": {"FR": "Projet : {name} | {mode}", "EN": "Project: {name} | {mode}"},
    "status.reporting": {"FR": "Retour au Project Owner : {label}", "EN": "Reporting to the Project Owner: {label}"},
    "status.language": {"FR": "Langue : {label}", "EN": "Language: {label}"},
    "status.branch": {"FR": "Branche : {branch} | HEAD : {head}", "EN": "Branch: {branch} | HEAD: {head}"},
    "status.checks": {"FR": "Contrôles : {status}", "EN": "Checks: {status}"},
    "status.gate": {"FR": "Garde-fou de commit : {state}", "EN": "Commit gate: {state}"},
    "gate.INSTALLED": {"FR": "installé hors de l'arbre de travail", "EN": "installed outside the worktree"},
    "gate.IN_TREE": {"FR": "installé dans l'arbre : un commit peut l'emporter — install-gate",
                     "EN": "installed inside the tree: a commit can carry it away — install-gate"},
    "gate.MISMATCH": {"FR": "la copie installée diffère de la référence — install-gate",
                      "EN": "the installed copy differs from the reference — install-gate"},
    "gate.NOT_INSTALLED": {"FR": "non installé — python3 -B scripts/project_control.py install-gate",
                           "EN": "not installed — python3 -B scripts/project_control.py install-gate"},
    "status.skeleton": {"FR": "Squelette : {version} | {core}", "EN": "Skeleton: {version} | {core}"},
    "core.aligned": {"FR": "core aligné", "EN": "core aligned"},
    "core.drift": {"FR": "core modifié localement : {paths}", "EN": "core modified locally: {paths}"},
    "status.view": {"FR": "Vue roadmap : {state}", "EN": "Roadmap view: {state}"},
    "view.CURRENT": {"FR": "à jour", "EN": "current"},
    "view.STALE": {"FR": "périmée — roadmap-view --write", "EN": "stale — roadmap-view --write"},
    "view.MISSING": {"FR": "absente — roadmap-view --write", "EN": "absent — roadmap-view --write"},
    "view.UNKNOWN": {"FR": "indéterminée", "EN": "undetermined"},
    "view.INHERITED": {"FR": "pas encore la tienne — elle sera générée après l'initialisation",
                       "EN": "not yours yet — it is generated after initialization"},
    "status.done": {"FR": "Travaux terminés : {done}{legacy} | Bloqués : {blocked}",
                    "EN": "Work Items done: {done}{legacy} | Blocked: {blocked}"},
    "status.legacy": {"FR": " (dont {frozen} figés avant la baseline d'adoption)",
                      "EN": " ({frozen} of them frozen before the adoption baseline)"},
    "status.item": {"FR": "{id} — {title} : {status}", "EN": "{id} — {title}: {status}"},
    "status.objective": {"FR": "  Objectif : {objective}", "EN": "  Objective: {objective}"},
    "status.item_branch": {"FR": "  Branche : {branch} | Cible : {target}", "EN": "  Branch: {branch} | Target: {target}"},
    "status.missing": {"FR": "  Vérifications manquantes : {gates}", "EN": "  Missing checks: {gates}"},
    "status.none_declared": {"FR": "aucune déclarée", "EN": "none declared"},
    "status.authorities": {"FR": "  Autorités lues : {state}", "EN": "  Authorities read: {state}"},
    "authorities.CURRENT": {"FR": "à jour", "EN": "current"},
    "authorities.STALE": {"FR": "modifiées depuis la lecture — acknowledge-authorities",
                          "EN": "changed since they were read — acknowledge-authorities"},
    "authorities.MISSING": {"FR": "non enregistrées", "EN": "not recorded"},
    "authorities.UNKNOWN": {"FR": "indéterminées", "EN": "undetermined"},
    "status.block": {"FR": "  Blocage : {code}", "EN": "  Blocked: {code}"},
    "status.resume": {"FR": "  Condition de reprise : {condition}", "EN": "  Resume condition: {condition}"},
    "status.error": {"FR": "Erreur : {error}", "EN": "Error: {error}"},
    "status.next": {"FR": "Prochaine action : {action}", "EN": "Next action: {action}"},
    "status.broken": {"FR": "Corriger les records invalides avant de poursuivre.",
                      "EN": "Fix the invalid records before going further."},
    # --- next action ----------------------------------------------------------------
    "next.audit": {"FR": "Corriger les erreurs d'audit avant toute écriture.",
                   "EN": "Fix the audit failures before writing anything."},
    "next.bootstrap": {"FR": "Initialiser le projet avec FIRST_START.md et valider le périmètre avec le propriétaire.",
                       "EN": "Initialize the project with FIRST_START.md and settle the scope with its owner."},
    "next.in_progress": {"FR": "Reprendre le Work Item en cours sur sa branche après preflight ; compléter ses preuves manquantes.",
                         "EN": "Resume the Work Item in progress on its branch after preflight; complete its missing evidence."},
    "next.authorized": {"FR": "Démarrer un Work Item autorisé dont les dépendances sont DONE, depuis la branche canonique.",
                        "EN": "Start an authorized Work Item whose dependencies are DONE, from the canonical branch."},
    "next.blocked": {"FR": "Vérifier la condition de reprise, enregistrer une nouvelle décision humaine, puis utiliser resume depuis la branche canonique propre.",
                     "EN": "Check the resume condition, record a new Human Decision, then run resume from a clean canonical checkout."},
    "next.idle": {"FR": "Projet au repos ; attendre un objectif autorisé.",
                  "EN": "Project at rest; wait for an authorized objective."},
    # --- roadmap view: the banner ---------------------------------------------------
    "banner.checked_on": {"FR": "Vérifié le", "EN": "Checked on"},
    "banner.how": {"FR": "Comment", "EN": "How"},
    "banner.how_detail": {"FR": "le dossier du projet a été lu par le contrôleur, sans rien y modifier",
                          "EN": "the controller read the project folder without changing anything in it"},
    "banner.version": {"FR": "Version", "EN": "Version"},
    "banner.backups": {"FR": "Sauvegardes", "EN": "Backups"},
    "banner.checks": {"FR": "Vérifications", "EN": "Checks"},
    "banner.refresh": {"FR": "Mise à jour", "EN": "Refresh"},
    "banner.on_demand": {"FR": " ; à la demande dans la discussion ROADMAP",
                         "EN": "; on demand in the ROADMAP conversation"},
    "checks.pass": {"FR": "les contrôles du dossier passent", "EN": "the folder's checks pass"},
    "checks.fail": {"FR": "des contrôles du dossier échouent", "EN": "some of the folder's checks fail"},
    "checks.tests": {"FR": " · {tests} essais automatiques présents, non exécutés par cette vue",
                     "EN": " · {tests} automated tests present, not run by this view"},
    "checks.sentence_pass": {"FR": "Les contrôles du dossier passent tous ; les essais automatiques, eux, ne sont pas exécutés par cette vue.",
                             "EN": "The folder's checks all pass; the automated tests, however, are not run by this view."},
    "checks.sentence_fail": {"FR": "Des contrôles du dossier échouent : voir le repli technique.",
                             "EN": "Some of the folder's checks fail: see the technical fold."},
    "source.audit": {"FR": "contrôleur, audit du dossier", "EN": "controller, audit of the folder"},
    # --- roadmap view: the skeleton's own dashboard ----------------------------------
    "tpl.eyebrow": {"FR": "Squelette de projet · tableau de bord", "EN": "Project skeleton · dashboard"},
    "tpl.lede": {"FR": "Où en est le squelette, ce qui vient ensuite, ce qui attend le Project Owner, et ce que sont devenues ses idées. Ce tableau montre ce qui est écrit dans les fichiers du dossier ; il ne décide rien.",
                 "EN": "Where the skeleton stands, what comes next, what awaits the Project Owner, and what became of his ideas. This dashboard shows what the folder's files say; it decides nothing."},
    "tpl.promoted": {"FR": "promue", "EN": "promoted"},
    "tpl.upcoming": {"FR": "à venir", "EN": "upcoming"},
    "tpl.version_text": {"FR": "{current}, la dernière promue", "EN": "{current}, the latest promoted"},
    "tpl.off_version": {"FR": " — attention : le dossier n’est pas sur cette version",
                        "EN": " — careful: the folder is not on this version"},
    "tpl.untagged": {"FR": " — le commit courant n’est pas tagué", "EN": " — the current commit carries no tag"},
    "tpl.now_version": {"FR": "La version {current} est la dernière promue", "EN": "Version {current} is the latest promoted"},
    "tpl.now_on_it": {"FR": " ; le dossier est bien sur elle.", "EN": "; the folder is on it."},
    "tpl.now_preparing": {"FR": " ; la {next} se prépare.", "EN": "; {next} is being prepared."},
    "tpl.now_off_it": {"FR": " ; le dossier n’est pas sur elle.", "EN": "; the folder is not on it."},
    "tpl.no_branch": {"FR": "Aucune branche de travail ouverte : tout est intégré.",
                      "EN": "No work branch open: everything is integrated."},
    "tpl.open_branches": {"FR": "Branches de travail non intégrées : {branches}.",
                          "EN": "Work branches not integrated: {branches}."},
    "source.tags": {"FR": "dossier du squelette (tags)", "EN": "skeleton folder (tags)"},
    "source.remotes": {"FR": "dossier du squelette (remotes)", "EN": "skeleton folder (remotes)"},
    "source.branches": {"FR": "dossier du squelette (branches)", "EN": "skeleton folder (branches)"},
    "stat.version": {"FR": "Version actuelle", "EN": "Current version"},
    "stat.version_tagged": {"FR": "promue et taguée", "EN": "promoted and tagged"},
    "stat.version_last_tag": {"FR": "dernière version taguée", "EN": "latest tagged version"},
    "stat.version_from_file": {"FR": "d’après le fichier de roadmap du squelette", "EN": "from the skeleton's roadmap file"},
    "stat.decisions": {"FR": "Décisions prises", "EN": "Decisions taken"},
    "stat.decisions_sub": {"FR": "consignées dans le journal du squelette", "EN": "recorded in the skeleton's journal"},
    "stat.checks": {"FR": "Contrôles du dossier", "EN": "Folder checks"},
    "stat.checks_pass": {"FR": "tout passe", "EN": "all pass"},
    "stat.checks_fail": {"FR": "à corriger", "EN": "to fix"},
    "stat.checks_sub": {"FR": "{tests} essais automatiques présents, non exécutés par cette vue",
                        "EN": "{tests} automated tests present, not run by this view"},
    "stat.open": {"FR": "Chantiers ouverts dans le dossier", "EN": "Workstreams open in the folder"},
    "stat.open_sub": {"FR": "branches non intégrées", "EN": "branches not integrated"},
    "stat.open_none": {"FR": "tout ce qui a été fait est intégré", "EN": "everything done is integrated"},
    # --- roadmap view: remote backups ------------------------------------------------
    "backups.up_to_date": {"FR": "à jour", "EN": "up to date"},
    "backups.same": {"FR": "identiques ({reference})", "EN": "identical ({reference})"},
    "backups.behind": {"FR": "en retard : {remotes}", "EN": "behind: {remotes}"},
    "backups.none": {"FR": "aucune sauvegarde distante connue", "EN": "no remote backup known"},
    "backups.same_sentence": {"FR": "Les sauvegardes distantes sont identiques à la branche principale ({reference}).",
                              "EN": "The remote backups match the main branch ({reference})."},
    "backups.behind_sentence": {"FR": "Des sauvegardes distantes sont en retard sur la branche principale : {remotes}.",
                                "EN": "Some remote backups are behind the main branch: {remotes}."},
    "backups.none_sentence": {"FR": "Aucune sauvegarde distante n’est connue depuis ce dossier.",
                              "EN": "No remote backup is known from this folder."},
    "regeneration.OFF": {"FR": "non (à la demande)", "EN": "no (on demand)"},
    "regeneration.HOURLY": {"FR": "toutes les heures", "EN": "every hour"},
    "regeneration.EVERY_4_HOURS": {"FR": "toutes les 4 heures", "EN": "every 4 hours"},
    "regeneration.DAILY": {"FR": "chaque jour", "EN": "every day"},
    # --- roadmap view: a governed project's dashboard --------------------------------
    "prj.eyebrow": {"FR": "Projet gouverné · tableau de bord", "EN": "Governed project · dashboard"},
    "prj.lede": {"FR": "Où en est le projet, ce qui vient ensuite, ce qui attend le Project Owner, et ce que sont devenues ses idées. Ce tableau montre ce qui est écrit dans les fichiers du dossier ; il ne décide rien.",
                 "EN": "Where the project stands, what comes next, what awaits the Project Owner, and what became of his ideas. This dashboard shows what the folder's files say; it decides nothing."},
    "prj.not_initialized": {"FR": "Le projet n’est pas encore initialisé : l’interview du Project Owner et la clôture de FIRST_START restent à faire.",
                            "EN": "The project is not initialized yet: the Project Owner's interview and the FIRST_START closeout are still to do."},
    "prj.skeleton": {"FR": "Le projet suit le squelette {skeleton}", "EN": "The project follows skeleton {skeleton}"},
    "prj.skeleton_aligned": {"FR": ", modèle aligné.", "EN": ", template aligned."},
    "prj.skeleton_drift": {"FR": ", avec {count} fichier(s) du modèle modifié(s) localement.",
                           "EN": ", with {count} template file(s) modified locally."},
    "prj.in_progress": {"FR": "Chantier en cours : {title} ({reference}). Vérifications manquantes : {missing}.",
                        "EN": "Work Item in progress: {title} ({reference}). Missing checks: {missing}."},
    "prj.blocked": {"FR": "Chantier bloqué : {title} ({reference}) — reprise quand : {condition}.",
                    "EN": "Work Item blocked: {title} ({reference}) — resumes when: {condition}."},
    "prj.unknown_condition": {"FR": "condition inconnue", "EN": "condition unknown"},
    "prj.at_rest": {"FR": "Aucun chantier en cours : le projet est au repos", "EN": "No Work Item in progress: the project is at rest"},
    "prj.at_rest_authorized": {"FR": " avec des chantiers autorisés à démarrer.", "EN": " with Work Items authorized to start."},
    "prj.at_rest_plain": {"FR": ".", "EN": "."},
    "prj.style": {"FR": "Style de retour au Project Owner : {style}.", "EN": "Reporting style to the Project Owner: {style}."},
    "prj.style_plain": {"FR": "simple", "EN": "plain"},
    "prj.style_technical": {"FR": "technique", "EN": "technical"},
    "prj.style_unset": {"FR": "pas encore choisi", "EN": "not chosen yet"},
    "authorities.line_current": {"FR": "autorités lues à jour", "EN": "authorities read are current"},
    "authorities.line_stale": {"FR": "autorités modifiées depuis la lecture", "EN": "authorities changed since they were read"},
    "authorities.line_missing": {"FR": "lecture des autorités non enregistrée", "EN": "reading of the authorities not recorded"},
    "wait.style": {"FR": "Choisir le style de retour", "EN": "Choose the reporting style"},
    "wait.style_detail": {"FR": "technique (rapports détaillés) ou simple (ce qui s’est passé, ce que ça change, ce qu’il doit faire).",
                          "EN": "technical (detailed reports) or plain (what happened, what it changes, what he has to do)."},
    "wait.language": {"FR": "Choisir la langue", "EN": "Choose the language"},
    "wait.language_detail": {"FR": "français ou anglais : la langue dans laquelle le contrôleur s’adresse au Project Owner.",
                             "EN": "French or English: the language the controller speaks to the Project Owner in."},
    "wait.init": {"FR": "Terminer l’initialisation", "EN": "Finish the initialization"},
    "wait.init_detail": {"FR": "répondre à l’interview, valider le cadre et la première autorisation.",
                         "EN": "answer the interview, settle the frame and the first authorization."},
    "wait.audit": {"FR": "Faire corriger les erreurs de vérification", "EN": "Have the failing checks fixed"},
    "wait.audit_detail": {"FR": "aucune écriture n’est possible tant qu’elles restent.",
                          "EN": "no write is possible while they remain."},
    "wait.resume": {"FR": "Décider la reprise de « {title} »", "EN": "Decide the resumption of \u201c{title}\u201d"},
    "wait.resume_detail": {"FR": "condition : {condition} ; une nouvelle décision enregistrée est nécessaire.",
                           "EN": "condition: {condition}; a newly recorded decision is required."},
    "wait.unknown": {"FR": "inconnue", "EN": "unknown"},
    "wait.drift": {"FR": "Décider du sort des fichiers du modèle modifiés localement",
                   "EN": "Decide what becomes of the template files modified locally"},
    "wait.idea_clarify": {"FR": "Préciser l’idée « {quote} »", "EN": "Clarify the idea \u201c{quote}\u201d"},
    "wait.idea_settle": {"FR": "Régler « {quote} »", "EN": "Settle \u201c{quote}\u201d"},
    "wait.idea_evoked": {"FR": "Dire ce que devient l’idée « {quote} »", "EN": "Say what becomes of the idea \u201c{quote}\u201d"},
    "wait.idea_evoked_detail": {"FR": "cadrer, planifier, remettre à plus tard ou écarter.",
                                "EN": "scope it, plan it, defer it or discard it."},
    "next.finish": {"FR": "Terminer « {title} »", "EN": "Finish \u201c{title}\u201d"},
    "next.finish_detail": {"FR": "vérifications manquantes : {missing}.", "EN": "missing checks: {missing}."},
    "next.start": {"FR": "Démarrer « {title} » ({reference})", "EN": "Start \u201c{title}\u201d ({reference})"},
    "next.start_detail": {"FR": "dépendances : {deps} ; décision {decision}.", "EN": "dependencies: {deps}; decision {decision}."},
    "next.no_dependency": {"FR": "aucune", "EN": "none"},
    "idea.title": {"FR": "Idée « {quote} »", "EN": "Idea \u201c{quote}\u201d"},
    "later.proposed": {"FR": "{title} ({reference}) — proposé", "EN": "{title} ({reference}) — proposed"},
    "past.decision": {"FR": "décision : {decision}", "EN": "decision: {decision}"},
    "past.decisions_title": {"FR": "Décisions humaines enregistrées ({count})", "EN": "Human Decisions recorded ({count})"},
    "past.unknown_date": {"FR": "date inconnue", "EN": "date unknown"},
    "stat.done": {"FR": "Chantiers terminés", "EN": "Work Items done"},
    "stat.done_sub": {"FR": "clos avec leurs preuves", "EN": "closed with their evidence"},
    "stat.open_items": {"FR": "Chantiers ouverts", "EN": "Work Items open"},
    "stat.open_items_sub": {"FR": "{active} en cours, {blocked} bloqué(s), {authorized} autorisé(s)",
                            "EN": "{active} in progress, {blocked} blocked, {authorized} authorized"},
    "stat.decisions_project_sub": {"FR": "enregistrées dans le registre des décisions", "EN": "recorded in the decision register"},
    "stat.ideas": {"FR": "Idées vivantes", "EN": "Live ideas"},
    "stat.ideas_sub": {"FR": "sur {total} enregistrée(s)", "EN": "out of {total} recorded"},
    "prj.version_text": {"FR": "squelette {skeleton}", "EN": "skeleton {skeleton}"},
    "prj.version_project": {"FR": " · projet {tag}", "EN": " · project {tag}"},
    "source.core_manifest": {"FR": "manifeste du core (provenance)", "EN": "core manifest (provenance)"},
    "source.core_manifest_short": {"FR": "manifeste du core", "EN": "core manifest"},
    "source.project_remotes": {"FR": "dossier du projet (remotes)", "EN": "project folder (remotes)"},
    "source.record": {"FR": "record {id}", "EN": "record {id}"},
    "source.branch": {"FR": "branche {branch}", "EN": "branch {branch}"},
    "source.interview": {"FR": "FIRST_START.md, interview", "EN": "FIRST_START.md, interview"},
    "sources.version_tags": {"FR": "(versions taguées du dépôt)", "EN": "(repository version tags)"},
}


def regeneration_label(value: str, language: str) -> str:
    key = f"regeneration.{value}"
    return speak(language, key) if key in SPEECH else REGENERATION_LABELS.get(value, value)
# The label is written in the language it names: a Project Owner reading it should not have to
# know the other one. UNKNOWN speaks both, because nobody has chosen yet.
LANGUAGE_LABELS = {
    "FR": "français (FR)",
    "EN": "english (EN)",
    "UNKNOWN": "non choisie (UNKNOWN) — à fixer avec le Project Owner / not chosen yet",
}

REPORTING_STYLE_LABELS_EN = {
    "TECHNICAL": "technical (TECHNICAL)",
    "PLAIN": "plain (PLAIN) — what happened, what it changes, what he has to do",
    "UNKNOWN": "not chosen (UNKNOWN) — to settle with the Project Owner before closing the initialization",
}


def reporting_style_label(style: str, language: str) -> str:
    table = REPORTING_STYLE_LABELS_EN if language == "EN" else REPORTING_STYLE_LABELS
    return table.get(style, style)

REPORTING_STYLES = {"TECHNICAL", "PLAIN"}
REPORTING_STYLE_LABELS = {
    "TECHNICAL": "technique (TECHNICAL)",
    "PLAIN": "simple (PLAIN) — ce qui s'est passé, ce que ça change, ce qu'il doit faire",
    "UNKNOWN": "non choisi (UNKNOWN) — à fixer avec le Project Owner avant la clôture de l'initialisation",
}

ADMINISTRATIVE_EXACT_PATHS = {
    "docs/governance/HUMAN_DECISIONS.md",
    "docs/governance/ROADMAP.md",
    "docs/governance/roadmap-state.v1.json",
    "docs/governance/WORKTREE_REGISTRY.md",
    "docs/governance/git-path-classifications.v1.json",
    IDEAS_JSON_PATH,
    IDEAS_MD_PATH,
    VIEW_SETTINGS_PATH,
    VIEW_MARKDOWN_PATH,
}

BOOTSTRAP_EXACT_PATHS = {
    ".gitignore",
    "README.md",
    "FIRST_START.md",
    "docs/governance/PROJECT_CHARTER.md",
    "docs/governance/HUMAN_DECISIONS.md",
    "docs/governance/ROADMAP.md",
    "docs/governance/roadmap-state.v1.json",
    "docs/governance/REPOSITORY_STATUS.md",
    "docs/governance/STORAGE_POLICY.md",
    "docs/governance/MIGRATION_RULES.md",
    "docs/governance/WORKTREE_REGISTRY.md",
    "docs/governance/git-path-classifications.v1.json",
    "project_control/project-state.v1.json",
    IDEAS_JSON_PATH,
    IDEAS_MD_PATH,
    VIEW_SETTINGS_PATH,
    VIEW_MARKDOWN_PATH,
}
BOOTSTRAP_TREE_PATHS = {
    "docs/architecture": {".md", ".json"},
    "docs/adr": {".md", ".json"},
    "project_control/work-items": {".json"},
    "project_control/conversations": {".json"},
    "project_control/agent-runs": {".json"},
    "provenance": {".md", ".json"},
}
BOOTSTRAP_FORBIDDEN_PREFIXES = (
    "applications/", "modules/", "shared/", "contracts/", "data/",
    "project_control/deployments/", "project_control/schemas/", "scripts/",
    "tests/", "templates/",
)
ACTIVE_CORE_ROOTS = (
    "AGENTS.md", "FIRST_START.md", "README.md", "applications", "contracts",
    "data", "docs", "modules", "project_control", "scripts", "shared",
)
FORBIDDEN_CORE_PATTERNS: dict[str, re.Pattern[str]] = {}

REQUIRED_FILES = (
    # `.gitignore` is the project's, not the core's — but the project cannot work without it: the
    # generated roadmap view writes an HTML page nothing else ignores, and a copy made by selecting
    # the visible entries of the template leaves it behind, because its name starts with a dot.
    # Missing, initialization used to complete and the project broke afterwards. Required here, it
    # is refused early, in the one place a newcomer is still reading the instructions.
    ".gitignore",
    "README.md", "FIRST_START.md", "AGENTS.md", "applications/README.md",
    "modules/README.md", "shared/README.md", "contracts/README.md", "data/README.md",
    "docs/governance/PROJECT_CHARTER.md", "docs/governance/HUMAN_DECISIONS.md",
    "docs/governance/ROADMAP.md", "docs/governance/roadmap-state.v1.json",
    "docs/governance/REPOSITORY_STATUS.md", "docs/governance/MIGRATION_RULES.md",
    "docs/governance/STORAGE_POLICY.md", "docs/governance/RECOVERY.md",
    "docs/governance/DEFINITION_OF_DONE.md", "docs/governance/WORKTREE_REGISTRY.md",
    "docs/architecture/PROJECT_ARCHITECTURE_MAP.md",
    "docs/architecture/INITIAL_ARCHITECTURE.md",
    "docs/agent-governance/mandatory-documents.v1.json", "docs/agent-governance/AGENTS.core.md",
    "provenance/core-manifest.v1.json", "docs/adr/README.md",
    "docs/adr/ADR-0001-initial-architecture-boundaries.md", "project_control/README.md",
    "project_control/project-state.v1.json",
    "project_control/schemas/project-state.v1.schema.json",
    "project_control/schemas/roadmap-state.v1.schema.json",
    "project_control/schemas/work-item.v1.schema.json",
    "project_control/schemas/conversation-reference.v1.schema.json",
    "project_control/schemas/agent-run.v1.schema.json",
    "project_control/schemas/evidence.v1.schema.json",
    "project_control/schemas/ideas-state.v1.schema.json",
    "project_control/schemas/roadmap-view.v1.schema.json",
    "project_control/schemas/template-roadmap.v1.schema.json",
    "project_control/work-items/README.md", "project_control/conversations/README.md",
    "project_control/agent-runs/README.md", "project_control/deployments/README.md",
    "provenance/README.md", "reports/README.md", "scripts/check_git_traceability.py",
    "scripts/hooks/pre-commit", "scripts/roadmap_view.py",
    "docs/agent-governance/ROADMAP_VIEW.md",
    IDEAS_JSON_PATH, IDEAS_MD_PATH, VIEW_SETTINGS_PATH,
    "tests/test_template.py",
)


@dataclass(frozen=True)
class Finding:
    check: str
    status: str
    detail: str


class ProjectControlError(RuntimeError):
    """A fail-closed lifecycle refusal suitable for concise CLI reporting."""


ADMINISTRATIVE_LOCK_NAME = "project-control.lock"
# Throwaway checkouts the controller creates for itself — the staged state a commit would
# write, the rehearsal of an upgrade — each live in a holder folder of their own, next to a
# marker file the controller writes at creation and keeps locked for as long as its command
# runs. A command killed in flight leaves its checkout behind, registered in the repository's
# worktree list until someone notices. The controller sweeps its own at the next gate or
# rehearsal: a checkout whose holder carries the marker, naming this repository, with the lock
# free — which the operating system grants only once the command that held it is dead. The
# name of a folder, the age of a checkout, what sits next to it: none of them proves ownership,
# and none of them is a criterion (fifth independent control, F-01).
THROWAWAY_MARKER_NAME = "PROJECT_CONTROL_THROWAWAY"
ADMINISTRATIVE_LOCK_WAIT_SECONDS = 15.0
# Re-entrant per process: a transaction opened while another is already held by this same process
# must not deadlock on itself. `flock` is per open file description, so a second handle in the same
# process would block forever. The depth counter keeps one real lock per process.
_ADMINISTRATIVE_LOCK: dict[str, Any] = {"handle": None, "depth": 0}


# Commands that read the project's registers and write them back. They are serialised as a whole:
# a lock taken only around the write would leave the read outside it, which is where two sessions
# lost each other's work.
MUTATING_COMMANDS = frozenset({
    "create-work-item", "start", "block", "resume", "close", "acknowledge-authorities",
    "idea", "install-gate",
})
# These write only when asked to; a read-only invocation must never wait behind a writer.
CONDITIONALLY_MUTATING = {
    "roadmap-view": lambda args: bool(
        getattr(args, "write", False) or getattr(args, "html", None) or getattr(args, "markdown", None)),
    "core-manifest": lambda args: bool(getattr(args, "write", False)),
    "template-upgrade": lambda args: bool(
        getattr(args, "apply", False) or getattr(args, "seed_required", False)),
}


def command_mutates(args: Any) -> bool:
    """Does this invocation write the project's registers?"""
    if args.command in MUTATING_COMMANDS:
        return True
    decide = CONDITIONALLY_MUTATING.get(args.command)
    return bool(decide and decide(args))


def hold_administrative_lock(root: Path) -> None:
    """Take the repository's administrative lock for the rest of this process.

    Released when the process ends: a command is short, and the lock has to outlive every
    transaction it opens. `FileTransaction` takes it too, re-entrantly, for any caller that did not
    come through the command line."""
    keeper = FileTransaction.__new__(FileTransaction)
    keeper.root = root
    keeper.holds_lock = False
    keeper.acquire_lock()
    _ADMINISTRATIVE_LOCK["keeper"] = keeper


def git_common_dir(root: Path) -> Path | None:
    """The repository's COMMON Git directory, resolved without calling Git.

    A linked worktree has a Git directory of its own; what is shared between every checkout of the
    repository is the common one. The administrative lock has to live there, so that two sessions
    working from two checkouts of the same repository contend for the same lock — and outside the
    worktree, where no commit can carry it and no traceability check has to explain it."""
    marker = root / ".git"
    if marker.is_dir():
        git_dir = marker
    elif marker.is_file():
        try:
            declaration = marker.read_text(encoding="utf-8").strip()
        except OSError:
            return None
        if not declaration.startswith("gitdir:"):
            return None
        git_dir = Path(declaration.split(":", 1)[1].strip())
        if not git_dir.is_absolute():
            git_dir = (root / git_dir).resolve()
    else:
        return None
    shared = git_dir / "commondir"
    if shared.is_file():
        try:
            declared = Path(shared.read_text(encoding="utf-8").strip())
        except OSError:
            return git_dir
        return declared if declared.is_absolute() else (git_dir / declared).resolve()
    return git_dir


class FileTransaction:
    """Atomic per-file writes with all-or-nothing rollback across owned paths."""

    def __init__(self, root: Path):
        self.root = root
        self.originals: dict[Path, bytes | None] = {}
        self.original_modes: dict[Path, int] = {}
        self.written: dict[Path, bytes] = {}
        self.abandoned: list[str] = []
        self.finished = False
        self.holds_lock = False
        self.acquire_lock()

    def acquire_lock(self) -> None:
        """Hold the repository's administrative lock for the whole transaction.

        Two sessions writing records at the same time used to interleave: both could fail leaving a
        roadmap that cites a Work Item whose record no longer exists, and the rollback of one could
        restore a file to the state it had before the other's committed change. Nothing in a
        per-file transaction can see that; only serialising the whole transaction can."""
        common = git_common_dir(self.root)
        if common is None:
            return
        if _ADMINISTRATIVE_LOCK["depth"]:
            _ADMINISTRATIVE_LOCK["depth"] += 1
            self.holds_lock = True
            return
        path = common / ADMINISTRATIVE_LOCK_NAME
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            handle = open(path, "a+")
        except OSError as exc:
            raise ProjectControlError(f"cannot open the administrative lock {path}: {exc}") from exc
        deadline = time.monotonic() + ADMINISTRATIVE_LOCK_WAIT_SECONDS
        while True:
            try:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError:
                if time.monotonic() >= deadline:
                    handle.close()
                    raise ProjectControlError(
                        "another Project Control transaction is writing this repository's records "
                        f"(lock held for more than {ADMINISTRATIVE_LOCK_WAIT_SECONDS:.0f}s at {path}). "
                        "Records are written one transaction at a time: wait for the other session "
                        "to finish, then run this command again. Nothing was written"
                    )
                time.sleep(0.1)
        _ADMINISTRATIVE_LOCK["handle"] = handle
        _ADMINISTRATIVE_LOCK["depth"] = 1
        self.holds_lock = True

    def release_lock(self) -> None:
        if not self.holds_lock:
            return
        self.holds_lock = False
        _ADMINISTRATIVE_LOCK["depth"] -= 1
        if _ADMINISTRATIVE_LOCK["depth"] > 0:
            return
        handle = _ADMINISTRATIVE_LOCK["handle"]
        _ADMINISTRATIVE_LOCK["handle"] = None
        if handle is None:
            return
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        except OSError:
            pass
        handle.close()

    def write_bytes(self, relative_path: str, content: bytes, mode: int | None = None) -> None:
        path = self.root / relative_path
        if path not in self.originals:
            self.originals[path] = path.read_bytes() if path.exists() else None
            if path.exists():
                self.original_modes[path] = path.stat().st_mode
        path.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
        try:
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())
            if mode is not None:
                os.chmod(temporary_name, mode & 0o777)
            os.replace(temporary_name, path)
            self.written[path] = content
        except BaseException:
            # A keyboard interrupt is not an Exception. Caught only as one, it left the temporary
            # file next to its target — unexplained, and refusing the next audit and the next
            # transition until someone found it (fourth independent control, F14-01).
            try:
                os.unlink(temporary_name)
            except FileNotFoundError:
                pass
            raise

    def write_text(self, relative_path: str, content: str) -> None:
        self.write_bytes(relative_path, content.encode("utf-8"))

    def write_json(self, relative_path: str, payload: Any) -> None:
        self.write_text(relative_path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")

    def commit(self) -> None:
        self.finished = True
        self.release_lock()

    def rollback(self) -> None:
        """Undo this transaction's own writes — and only those.

        Restoring blindly puts back the bytes captured when the file was first touched, which is
        wrong the moment anything else has written to it since: an aborted transaction could erase
        a change another session had already committed. A file that no longer holds what this
        transaction wrote is not this transaction's to undo; it is left alone and named."""
        if self.finished:
            return
        for path, original in reversed(list(self.originals.items())):
            expected = self.written.get(path)
            if expected is not None:
                try:
                    current = path.read_bytes() if path.exists() else None
                except OSError:
                    current = None
                if current != expected:
                    self.abandoned.append(str(path))
                    continue
            if original is None:
                try:
                    path.unlink()
                except FileNotFoundError:
                    pass
            else:
                path.write_bytes(original)
                if path in self.original_modes:
                    os.chmod(path, self.original_modes[path] & 0o777)
        self.finished = True
        self.release_lock()


def add(findings: list[Finding], check: str, passed: bool, detail: str) -> None:
    findings.append(Finding(check, "PASS" if passed else "FAIL", detail))


def display_reference_for(work_item_id: str, project_key: str | None) -> str:
    if project_key in (None, ""):
        return work_item_id
    return f"{project_key}-{work_item_id.split('-', 1)[1]}"


def safe_relative_path(value: str) -> str | None:
    candidate = PurePosixPath(value.replace("\\", "/"))
    if candidate.is_absolute() or not candidate.parts or ".." in candidate.parts:
        return None
    normalized = candidate.as_posix()
    if normalized == ".":
        return None
    return normalized or None


def clean_cli_text(value: str, label: str) -> str:
    cleaned = value.strip()
    if not cleaned or "\n" in cleaned or "\r" in cleaned or "|" in cleaned:
        raise ProjectControlError(f"{label} must be a non-empty single line without '|'")
    return cleaned


def today_iso() -> str:
    return date.today().isoformat()


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


REGISTRY_ENTRY_PATTERN = re.compile(
    r"<!-- PROJECT_CONTROL:(WI-[0-9]{3,}) START -->\n(.*?)"
    r"<!-- PROJECT_CONTROL:\1 END -->",
    re.DOTALL,
)

# A run reports its outcome on two levels, and reading only one of them gets it wrong both ways.
# `EVIDENCE_FAILURE_VERDICTS` are the lines where a run states its own failure: they settle the
# question whatever else the artifact holds. `EVIDENCE_FAILURE_DIAGNOSTICS` are per-item lines —
# `ERROR:`, `FAIL:`, a traceback, a non-zero counter. Alone they mean a failure; beside a verdict
# of success they are the expected noise of a test that checks an invalid input is rejected.
# Reading diagnostics as verdicts refused honest proofs (3.15.0); ignoring them let the sole
# output of a program that really failed pass for a proof of success (3.15.3). Hence the two lists.
EVIDENCE_FAILURE_VERDICTS = (
    re.compile(r"(?m)^[ \t]*FAILED\b"),
    re.compile(r"(?m)^=+.*\b[1-9][0-9]* (?:failed|error)"),
)
EVIDENCE_FAILURE_DIAGNOSTICS = (
    re.compile(r"(?m)^[ \t]*(?:FAIL|ERROR)[: \t]"),
    re.compile(r"(?m)^Traceback \(most recent call last\):"),
    re.compile(r"(?m)^.*\b(?:failures|errors)=[1-9][0-9]*"),
)
# A run that says it succeeded. Never a summary that counts failures beside its passes: those are
# read as verdicts of failure above, and this list is only consulted once none of them matched.
EVIDENCE_SUCCESS_VERDICTS = (
    re.compile(r"(?m)^[ \t]*OK\b"),
    re.compile(r"(?m)^[ \t]*PASS(?:ED)?\b"),
    re.compile(r"(?m)^=+.*\b[1-9][0-9]* passed\b"),
)


def is_text_artifact(data: bytes) -> bool:
    """Can this artifact be read at all? A binary piece vouches for nothing, either way."""
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return True


def failure_marker_in(data: bytes) -> str | None:
    """The line of an artifact that reports a failure, or None when it reports none.

    A proof that claims PASS while everything it shows reports a failure is the case this
    catches: an author who copies the output of a run without reading it. It is not a verdict on
    the run — the controller never executes a project's tests, and it never will — and it is
    deliberately narrow: a proof may carry a failed run beside what passed, because keeping the
    failure visible is what the doctrine asks for. Only a proof whose every readable piece
    reports a failure contradicts itself.

    A verdict of failure settles it. A diagnostic settles it only when the artifact carries no
    verdict of success: `ERROR: line 4 refused` inside a run that ends on `OK` is what a passing
    test prints, while the same line alone is all a program that died had to say."""
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return None

    def quoted(match: re.Match[str]) -> str:
        # Quote the whole line: a refusal that answers "FAILED" tells the reader nothing he
        # can look up, where "FAILED (failures=1)" points straight at the run.
        start = text.rfind("\n", 0, match.start()) + 1
        end = text.find("\n", match.end())
        return text[start:end if end != -1 else len(text)].strip()[:200]

    for pattern in EVIDENCE_FAILURE_VERDICTS:
        match = pattern.search(text)
        if match:
            return quoted(match)
    if any(pattern.search(text) for pattern in EVIDENCE_SUCCESS_VERDICTS):
        return None
    for pattern in EVIDENCE_FAILURE_DIAGNOSTICS:
        match = pattern.search(text)
        if match:
            return quoted(match)
    return None


def declared_status(text: str) -> str | None:
    """The status a document declares about itself: the value of its own `Status:` line.

    A document may perfectly well *mention* the status the controller expects — a note that tells
    a newcomer what to write is exactly that. Searching the whole text made such a note satisfy
    the check it was explaining. Only the line that declares the status counts, and only the
    first one: what follows is prose about it."""
    match = re.search(r"(?m)^Status:[ \t]*(\S.*)$", text)
    if match is None:
        return None
    return match.group(1).strip().strip("`").strip()


def decision_block(text: str, reference: str) -> str | None:
    """The recorded text of one Human Decision, from its heading to the next one."""
    match = re.search(
        rf"(?ms)^## {re.escape(reference)}\s*$\n(.*?)(?=^## HD-[0-9]{{3,}}\s*$|\Z)",
        text,
    )
    return None if match is None else match.group(1)


def human_decision_errors(text: str, reference: str, *, as_mandate: bool = True) -> list[str]:
    """Why a recorded Human Decision is not usable as an authorization (empty when it is).

    `as_mandate` is the ordinary case: the decision is cited as the mandate of a Work Item
    or of one of its transitions, and its documented vocabulary is `Chosen option: AUTHORIZE`.
    A decision recorded with another vocabulary of its own — the adoption of a legacy
    baseline chooses between `FREEZE_HISTORY` and `RECONSTRUCT_HISTORY` — is read with
    `as_mandate=False`: every other requirement still applies."""
    block = decision_block(text, reference)
    if block is None:
        return [f"{reference}: not recorded"]
    errors: list[str] = []
    decision = re.search(r"(?m)^Decision:[ \t]*(\S.*)$", block)
    authorizer = re.search(r"(?m)^Authorized by:[ \t]*(\S.*)$", block)
    if not decision or decision.group(1).strip() == "UNKNOWN":
        errors.append(f"{reference}: Decision is missing or UNKNOWN")
    if not authorizer or authorizer.group(1).strip() == "UNKNOWN":
        errors.append(f"{reference}: Authorized by is missing or UNKNOWN")
    chosen = [value.strip() for value in re.findall(r"(?m)^Chosen option:[ \t]*(\S.*)$", block)]
    refused = [value for value in chosen if value.upper() != "AUTHORIZE"] if as_mandate else []
    if refused:
        # A decision that records another option than AUTHORIZE — REJECT, DEFER — is the trace
        # of a refusal: reading it as an authorization would turn a "no" into a "yes".
        errors.append(f"{reference}: Chosen option is not AUTHORIZE: {', '.join(refused)}")
    errors.extend(f"{reference}: {error}" for error in out_of_folder_decision_errors(block))
    return errors


def human_decision_is_valid(text: str, reference: str, *, as_mandate: bool = True) -> bool:
    return not human_decision_errors(text, reference, as_mandate=as_mandate)


def out_of_folder_decision_errors(block: str) -> list[str]:
    """Double stop: a decision whose scope leaves the granted folder (another repository,
    directory, project or remote) is valid only with two distinct recorded confirmations.

    The scope is declared explicitly with `Folder scope:`; absent or NOT_APPLICABLE means the
    decision stays inside the repository and needs nothing more."""
    scope = re.search(r"(?m)^Folder scope:[ \t]*(\S.*)$", block)
    if scope is None or scope.group(1).strip() in {"NOT_APPLICABLE", "NONE"}:
        return []
    target = scope.group(1).strip()
    errors: list[str] = []
    if target == "UNKNOWN":
        errors.append("Folder scope must name the target folder, not UNKNOWN")
    confirmations = []
    for index in (1, 2):
        found = re.search(rf"(?m)^Confirmation {index}:[ \t]*(\S.*)$", block)
        value = found.group(1).strip() if found else ""
        if not value or value == "UNKNOWN":
            errors.append(f"out-of-folder decision requires Confirmation {index}")
        confirmations.append(value)
    if all(confirmations) and confirmations[0] == confirmations[1]:
        errors.append("the two confirmations must be distinct human statements")
    return errors


def human_decision_relates_to_work_item(
    text: str,
    reference: str,
    work_item_id: str,
) -> bool:
    return human_decision_field(text, reference, "Related Work Item") == work_item_id

def human_decision_field(
    text: str,
    reference: str,
    field: str,
) -> str | None:
    match = re.search(
        rf"(?ms)^## {re.escape(reference)}\s*$\n(.*?)(?=^## HD-[0-9]{{3,}}\s*$|\Z)",
        text,
    )
    if match is None:
        return None
    values = re.findall(
        rf"(?m)^{re.escape(field)}:[ \t]*(\S.*)$",
        match.group(1),
    )
    if len(values) != 1:
        return None
    return values[0].strip()


def human_decision_field_values(text: str, reference: str, field: str) -> list[str] | None:
    """Every value a recorded decision gives a field, in order; None when the decision is not
    recorded. `human_decision_field` answers None both for a field that is absent and for one
    written twice, and a check that only asked "is the value REJECT?" let a decision written
    `Chosen option: REJECT` twice pass as if it had chosen nothing (fifth independent control,
    F-05). A check that must see every line reads them here."""
    match = re.search(
        rf"(?ms)^## {re.escape(reference)}\s*$\n(.*?)(?=^## HD-[0-9]{{3,}}\s*$|\Z)",
        text,
    )
    if match is None:
        return None
    return [value.strip() for value in re.findall(rf"(?m)^{re.escape(field)}:[ \t]*(\S.*)$", match.group(1))]

def parse_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else None

def is_timestamp(value: Any) -> bool:
    return parse_timestamp(value) is not None

def initial_gate_status(applicability: str, applicable_status: str = "NOT_REACHED") -> str:
    return "NOT_APPLICABLE" if applicability == "NOT_APPLICABLE" else applicable_status


def roadmap_dependency_text(dependencies: Iterable[str]) -> str:
    values = list(dependencies)
    return ", ".join(values) if values else "—"


def render_roadmap_markdown(text: str, summaries: Sequence[dict[str, Any]]) -> str:
    lines = text.splitlines()
    header_index = next(
        (index for index, line in enumerate(lines) if line.startswith("| Internal ID |")),
        None,
    )
    if header_index is None or header_index + 1 >= len(lines) or not lines[header_index + 1].startswith("|---"):
        raise ProjectControlError("ROADMAP.md does not contain the managed Work Items table")
    row_start = header_index + 2
    row_end = row_start
    while row_end < len(lines) and re.match(r"^\| WI-[0-9]{3,} \|", lines[row_end]):
        row_end += 1
    rows = []
    for summary in summaries:
        rows.append(
            f"| {summary['work_item_id']} | {summary['display_reference']} | "
            f"{summary['title']} | {summary['status']} | {summary['integration_state']} | "
            f"{summary['human_gate']} | {roadmap_dependency_text(summary.get('dependencies', []))} |"
        )
    return "\n".join([*lines[:row_start], *rows, *lines[row_end:]]) + "\n"


def render_registry_entry(
    text: str,
    item: dict[str, Any],
    status: str,
) -> str:
    work_item_id = item["work_item_id"]
    marker_start = f"<!-- PROJECT_CONTROL:{work_item_id} START -->"
    marker_end = f"<!-- PROJECT_CONTROL:{work_item_id} END -->"
    scope = ", ".join(item.get("authorized_paths", []))
    block = (
        f"{marker_start}\n"
        f"WORK_ITEM_ID: {work_item_id}\n"
        f"DISPLAY_REFERENCE: {item['display_reference']}\n"
        f"BASE_HEAD: {item['base_head']}\n"
        f"START_HEAD: {item['start_head']}\n"
        f"AUTHORIZED_SCOPE: {scope}\n"
        f"BRANCH: {item['branch']}\n"
        f"STATUS: {status}\n"
        f"CLOSE_CONDITION: {item['close_condition']}\n"
        f"{marker_end}"
    )
    pattern = re.compile(re.escape(marker_start) + r".*?" + re.escape(marker_end), re.DOTALL)
    if pattern.search(text):
        return pattern.sub(block, text)
    return text.rstrip() + "\n\n" + block + "\n"


def ideas_cell(value: Any) -> str:
    """One Markdown table cell of IDEAS.md: pipes and line breaks cannot survive a table."""
    text = "" if value is None else str(value)
    return text.replace("|", "¦").replace("\r", " ").replace("\n", " ").strip() or "—"


def render_ideas_markdown(text: str, ideas: Sequence[dict[str, Any]]) -> str:
    """Rewrite the managed ideas table of IDEAS.md from the machine state, keeping the prose."""
    lines = text.splitlines()
    header_index = next((index for index, line in enumerate(lines) if line.startswith("| ID | Date |")), None)
    if header_index is None or header_index + 1 >= len(lines) or not lines[header_index + 1].startswith("|---"):
        raise ProjectControlError("IDEAS.md does not contain the managed ideas table")
    row_start = header_index + 2
    row_end = row_start
    while row_end < len(lines) and re.match(r"^\| ID-[0-9]{3,} \|", lines[row_end]):
        row_end += 1
    rows = [
        f"| {idea['idea_id']} | {ideas_cell(idea['stated_at'])} | {ideas_cell(idea['quote'])} | "
        f"{idea['state']} | {ideas_cell(idea.get('target'))} | {ideas_cell(idea['source'])} |"
        for idea in ideas
    ]
    status = "EMPTY" if not ideas else f"{len(ideas)} IDEA(S)"
    rendered = "\n".join([*lines[:row_start], *rows, *lines[row_end:]]) + "\n"
    return re.sub(r"(?m)^Status: `[^`]*`", f"Status: `{status}`", rendered, count=1)


def parse_ideas_table(text: str) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    for line in text.splitlines():
        if not re.match(r"^\| ID-[0-9]{3,} \|", line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 6:
            continue
        idea_id, stated_at, quote, state, target, source = cells[:6]
        rows[idea_id] = {"stated_at": stated_at, "quote": quote, "state": state, "target": target, "source": source}
    return rows


def bootstrap_path_errors(paths: Iterable[str]) -> list[str]:
    errors: list[str] = []
    for raw in sorted(set(paths)):
        path = safe_relative_path(raw)
        if path is None:
            errors.append(f"unsafe bootstrap path: {raw}")
            continue
        if any(path.startswith(prefix) for prefix in BOOTSTRAP_FORBIDDEN_PREFIXES):
            errors.append(f"bootstrap-forbidden path: {path}")
            continue
        if path in BOOTSTRAP_EXACT_PATHS:
            continue
        allowed = any(
            path.startswith(prefix + "/") and Path(path).suffix in suffixes
            for prefix, suffixes in BOOTSTRAP_TREE_PATHS.items()
        )
        if not allowed:
            errors.append(f"path outside bootstrap allowlist: {path}")
    return errors


def normal_path_errors(paths: Iterable[str], authorized_paths: Iterable[str]) -> list[str]:
    declared = [safe_relative_path(value) for value in authorized_paths]
    declared = [value for value in declared if value]
    errors: list[str] = []
    for raw in sorted(set(paths)):
        path = safe_relative_path(raw)
        if path is None:
            errors.append(f"unsafe normal-mode path: {raw}")
            continue
        matched = any(path == item or path.startswith(item.rstrip("/") + "/") for item in declared)
        if not matched:
            errors.append(f"path outside Work Item authorization: {path}")
    return errors


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def schema_shape_errors(schema: Any, label: str) -> list[str]:
    if not isinstance(schema, dict):
        return [f"{label}: schema root is not an object"]
    missing = [key for key in ("$schema", "$id", "title", "type", "required", "properties") if key not in schema]
    errors = [f"{label}: missing {key}" for key in missing]
    if schema.get("type") != "object":
        errors.append(f"{label}: root type must be object")
    if not isinstance(schema.get("required"), list):
        errors.append(f"{label}: required must be a list")
    if not isinstance(schema.get("properties"), dict):
        errors.append(f"{label}: properties must be an object")
    return errors


def schema_record_errors(value: Any, schema: dict[str, Any], label: str) -> list[str]:
    """Validate the documented schema subset used by the core, without dependencies."""
    supported = {"$schema", "$id", "title", "description", "type", "required", "properties",
                 "additionalProperties", "const", "enum", "pattern", "minLength", "items",
                 "minItems", "uniqueItems", "minimum", "format"}
    unknown = set(schema) - supported
    if unknown:
        return [f"{label}: unsupported schema keywords {sorted(unknown)}"]
    errors: list[str] = []
    if "format" in schema and schema["format"] != "date-time":
        return [f"{label}: unsupported schema format {schema['format']!r}"]
    checks = {"object": lambda v: isinstance(v, dict), "array": lambda v: isinstance(v, list),
              "string": lambda v: isinstance(v, str), "null": lambda v: v is None,
              "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
              "boolean": lambda v: isinstance(v, bool)}
    types = schema.get("type", [])
    types = [types] if isinstance(types, str) else types
    if any(t not in checks for t in types):
        return [f"{label}: unsupported schema type"]
    if types and not any(checks[t](value) for t in types):
        return [f"{label}: expected type {types}"]
    if "const" in schema and (type(value) is not type(schema["const"]) or value != schema["const"]):
        errors.append(f"{label}: expected constant {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{label}: invalid enum value {value!r}")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{label}: string is too short")
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            errors.append(f"{label}: pattern mismatch")
        if schema.get("format") == "date-time" and parse_timestamp(value) is None:
            errors.append(f"{label}: expected timezone-aware date-time")
    if isinstance(value, int) and not isinstance(value, bool) and value < schema.get("minimum", value):
        errors.append(f"{label}: below minimum")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{label}: too few items")
        if schema.get("uniqueItems") and len({json.dumps(v, sort_keys=True) for v in value}) != len(value):
            errors.append(f"{label}: duplicate items")
        if "items" in schema:
            for i, child in enumerate(value):
                errors.extend(schema_record_errors(child, schema["items"], f"{label}[{i}]"))
    if isinstance(value, dict):
        errors.extend(f"{label}: missing {key}" for key in schema.get("required", []) if key not in value)
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            errors.extend(f"{label}: unexpected property {key}" for key in value if key not in properties)
        for key in value.keys() & properties.keys():
            errors.extend(schema_record_errors(value[key], properties[key], f"{label}.{key}"))
    return errors


def core_schema_errors(record: Any, name: str) -> list[str]:
    return schema_record_errors(record, load_json(ROOT / f"project_control/schemas/{name}.v1.schema.json"), name)


def required_field_errors(record: Any, fields: Iterable[str], label: str) -> list[str]:
    if not isinstance(record, dict):
        return [f"{label}: record is not an object"]
    return [f"{label}: missing {field}" for field in fields if field not in record]


def validate_project_state(state: Any, first_start_status: str | None = None) -> list[str]:
    shape_errors = core_schema_errors(state, "project-state")
    if shape_errors:
        return shape_errors
    required = (
        "$schema", "schema_version", "repository_role", "project_name", "project_key",
        "project_owner", "initialization", "legacy_baseline", "authorities_baseline", "reporting_style",
        "language",
    )
    errors = required_field_errors(state, required, "project-state")
    if errors or not isinstance(state, dict):
        return errors
    # The adoption baseline is declared, never inferred: null for a project without prior
    # history, otherwise the commit and the Human Decision that froze that history.
    legacy_baseline = state.get("legacy_baseline")
    if legacy_baseline is not None and not isinstance(legacy_baseline, dict):
        errors.append("project-state: legacy_baseline must be null or an object")
    # The proof-of-reading baseline follows the same rule: declared by a Human Decision when a
    # project adopts the proof of reading with Agent Runs already recorded, null otherwise.
    authorities_baseline = state.get("authorities_baseline")
    if authorities_baseline is not None and not isinstance(authorities_baseline, dict):
        errors.append("project-state: authorities_baseline must be null or an object")
    if state.get("repository_role") not in {"PROJECT_TEMPLATE", "PROJECT"}:
        errors.append("project-state: invalid repository_role")
    if not isinstance(state.get("project_name"), str) or not state.get("project_name"):
        errors.append("project-state: project_name must be a non-empty string")
    key = state.get("project_key")
    if key is not None and (not isinstance(key, str) or not PROJECT_KEY.fullmatch(key)):
        errors.append("project-state: project_key must be null or a generic uppercase key")
    if not isinstance(state.get("project_owner"), str) or not state.get("project_owner"):
        errors.append("project-state: project_owner must be known or explicitly UNKNOWN")
    # The Project Owner chooses how agents report back — TECHNICAL or PLAIN — during the
    # initialization interview; UNKNOWN only says the question has not been asked yet.
    if state.get("reporting_style") not in REPORTING_STYLES and state.get("reporting_style") != "UNKNOWN":
        errors.append("project-state: reporting_style must be TECHNICAL, PLAIN or UNKNOWN")
    # The Project Owner also chooses the language the controller speaks to him in — the same
    # interview, the same rule: UNKNOWN only says the question has not been asked yet.
    if state.get("language") not in LANGUAGES and state.get("language") != "UNKNOWN":
        errors.append("project-state: language must be FR, EN or UNKNOWN")
    initialization = state.get("initialization")
    if not isinstance(initialization, dict):
        return errors + ["project-state: initialization must be an object"]
    init_required = {
        "status", "completion_human_decision_ref", "completed_at", "baseline_head",
        "closeout_evidence",
    }
    errors.extend(
        f"project-state: initialization missing {key}"
        for key in sorted(init_required - set(initialization))
    )
    status = initialization.get("status")
    if status not in {"NOT_STARTED", "COMPLETE"}:
        errors.append("project-state: initialization status must be NOT_STARTED or COMPLETE")
    if first_start_status is not None and status != first_start_status:
        errors.append(
            f"project-state: initialization status {status} differs from FIRST_START {first_start_status}"
        )
    decision_ref = initialization.get("completion_human_decision_ref")
    if decision_ref is not None and not HUMAN_DECISION_ID.fullmatch(str(decision_ref)):
        errors.append("project-state: invalid completion_human_decision_ref")
    evidence = initialization.get("closeout_evidence")
    if not isinstance(evidence, list):
        errors.append("project-state: closeout_evidence must be a list")
    if status == "NOT_STARTED":
        if initialization.get("completed_at") is not None:
            errors.append("project-state: NOT_STARTED cannot have completed_at")
        if initialization.get("baseline_head") != "UNKNOWN":
            errors.append("project-state: NOT_STARTED baseline_head must be UNKNOWN")
        if legacy_baseline is not None:
            errors.append("project-state: NOT_STARTED cannot declare a legacy_baseline")
        if authorities_baseline is not None:
            errors.append("project-state: NOT_STARTED cannot declare an authorities_baseline")
    if status == "COMPLETE":
        if state.get("project_name") == "UNKNOWN" or state.get("project_owner") == "UNKNOWN":
            errors.append("project-state: COMPLETE requires known project_name and project_owner")
        if state.get("reporting_style") not in REPORTING_STYLES:
            errors.append("project-state: COMPLETE requires reporting_style TECHNICAL or PLAIN, chosen by the Project Owner")
        if state.get("language") not in LANGUAGES:
            errors.append("project-state: COMPLETE requires language FR or EN, chosen by the Project Owner")
        if not HUMAN_DECISION_ID.fullmatch(str(decision_ref or "")):
            errors.append("project-state: COMPLETE requires a Human Decision reference")
        if not initialization.get("completed_at"):
            errors.append("project-state: COMPLETE requires completed_at")
        if not SHA40.fullmatch(str(initialization.get("baseline_head", ""))):
            errors.append("project-state: COMPLETE requires a 40-character baseline_head")
        if not evidence:
            errors.append("project-state: COMPLETE requires closeout evidence")
    return errors


def validate_work_item(record: Any, project_key: str | None = None,
                       canonical_branch: str | None = None) -> list[str]:
    shape_errors = core_schema_errors(record, "work-item")
    if shape_errors:
        return shape_errors
    required = (
        "$schema", "schema_version", "work_item_id", "display_reference", "title",
        "objective", "owner", "status", "human_decision_refs", "conversation_refs",
        "agent_run_refs", "dependencies", "base_head", "branch", "commits",
        "authorized_paths", "conflict_gate", *IMPACT_FIELDS, "applicability",
        "development_status", "test_status", "integration_status", "deployment_status",
        "runtime_proof_status", "evidence", "close_condition",
    )
    errors = required_field_errors(record, required, "Work Item")
    if errors or not isinstance(record, dict):
        return errors
    work_item_id = str(record.get("work_item_id", ""))
    if not WORK_ITEM_ID.fullmatch(work_item_id):
        errors.append(f"Work Item: invalid internal ID {work_item_id}")
    expected = display_reference_for(work_item_id, project_key) if WORK_ITEM_ID.fullmatch(work_item_id) else None
    if expected and record.get("display_reference") != expected:
        errors.append(f"Work Item {work_item_id}: display_reference must be {expected}")
    if record.get("status") not in WORK_ITEM_STATUSES:
        errors.append(f"Work Item {work_item_id}: unknown status {record.get('status')}")
    if record.get("conflict_gate") not in CONFLICT_STATES:
        errors.append(f"Work Item {work_item_id}: invalid conflict_gate")
    for name, pattern in (("human_decision_refs", HUMAN_DECISION_ID), ("dependencies", WORK_ITEM_ID)):
        value = record.get(name)
        if not isinstance(value, list) or any(not pattern.fullmatch(str(item)) for item in value):
            errors.append(f"Work Item {work_item_id}: invalid {name}")
    for name in ("conversation_refs", "agent_run_refs", "commits", "authorized_paths"):
        if not isinstance(record.get(name), list):
            errors.append(f"Work Item {work_item_id}: {name} must be a list")
    authorized_paths = record.get("authorized_paths", [])
    if isinstance(authorized_paths, list) and (
        not authorized_paths or any(safe_relative_path(str(item)) is None for item in authorized_paths)
    ):
        errors.append(f"Work Item {work_item_id}: authorized_paths must contain safe repository-relative paths")
    branch = str(record.get("branch", ""))
    if branch == "UNKNOWN" or not BRANCH_NAME.fullmatch(branch):
        errors.append(f"Work Item {work_item_id}: invalid branch")
    if record.get("base_head") != "UNKNOWN" and not SHA40.fullmatch(str(record.get("base_head", ""))):
        errors.append(f"Work Item {work_item_id}: invalid base_head")
    commits = record.get("commits", [])
    if isinstance(commits, list) and any(not SHA40.fullmatch(str(item)) for item in commits):
        errors.append(f"Work Item {work_item_id}: invalid commit hash")
    block_records = record.get("block_records", [])
    if not isinstance(block_records, list):
        errors.append(f"Work Item {work_item_id}: block_records must be a list")
        block_records = []
    unresolved_blocks: list[int] = []
    blocked_run_refs: set[str] = set()
    previous_blocked_at: datetime | None = None
    previous_resolved_at: datetime | None = None
    for index, block_record in enumerate(block_records):
        label = f"Work Item {work_item_id}: block_records[{index}]"
        if not isinstance(block_record, dict):
            errors.append(f"{label} must be an object")
            continue
        if set(block_record) != BLOCK_RECORD_FIELDS:
            errors.append(f"{label} must contain exactly {sorted(BLOCK_RECORD_FIELDS)}")
            continue
        if block_record.get("type") != "EXTERNAL_DEPENDENCY":
            errors.append(f"{label}.type must be EXTERNAL_DEPENDENCY")
        if not REASON_CODE.fullmatch(str(block_record.get("reason_code", ""))):
            errors.append(f"{label}.reason_code must be machine-readable uppercase snake case")
        blocked_time = parse_timestamp(block_record.get("blocked_at"))
        if blocked_time is None:
            errors.append(f"{label}.blocked_at must be a timezone-aware timestamp")
        if previous_blocked_at is not None and blocked_time is not None:
            if blocked_time < previous_blocked_at:
                errors.append(f"{label}.blocked_at precedes the prior block record")
            if previous_resolved_at is None:
                errors.append(f"{label} follows an unresolved prior block record")
            elif blocked_time < previous_resolved_at:
                errors.append(f"{label}.blocked_at precedes the prior resolution")
        block_decision = str(block_record.get("human_decision_id", ""))
        if not HUMAN_DECISION_ID.fullmatch(block_decision):
            errors.append(f"{label}.human_decision_id must match HD-NNN")
        elif block_decision not in record.get("human_decision_refs", []):
            errors.append(f"{label}.human_decision_id must be linked by the Work Item")
        agent_run_ref = block_record.get("agent_run_ref")
        if agent_run_ref is not None:
            if (
                not isinstance(agent_run_ref, str)
                or not AGENT_RUN_REFERENCE.fullmatch(agent_run_ref)
            ):
                errors.append(
                    f"{label}.agent_run_ref must be null or a RUN-prefixed reference"
                )
            elif agent_run_ref not in record.get("agent_run_refs", []):
                errors.append(f"{label}.agent_run_ref must be linked by the Work Item")
            elif agent_run_ref in blocked_run_refs:
                errors.append(f"{label}.agent_run_ref was already used by a prior block")
            else:
                blocked_run_refs.add(agent_run_ref)
        resume_condition = block_record.get("resume_condition")
        if not isinstance(resume_condition, str) or not resume_condition.strip():
            errors.append(f"{label}.resume_condition must be non-empty")
        resolved_at = block_record.get("resolved_at")
        resolution_decision = block_record.get("resolution_human_decision_id")
        if resolved_at is None and resolution_decision is None:
            unresolved_blocks.append(index)
            resolved_time = None
        elif resolved_at is None or resolution_decision is None:
            errors.append(
                f"{label} must set resolved_at and resolution_human_decision_id together"
            )
            resolved_time = parse_timestamp(resolved_at)
        else:
            resolved_time = parse_timestamp(resolved_at)
            if resolved_time is None:
                errors.append(f"{label}.resolved_at must be a timezone-aware timestamp")
            elif blocked_time is not None and resolved_time < blocked_time:
                errors.append(f"{label}.resolved_at precedes blocked_at")
            resolution_ref = str(resolution_decision)
            if not HUMAN_DECISION_ID.fullmatch(resolution_ref):
                errors.append(f"{label}.resolution_human_decision_id must match HD-NNN")
            elif resolution_ref not in record.get("human_decision_refs", []):
                errors.append(
                    f"{label}.resolution_human_decision_id must be linked by the Work Item"
                )
            if resolution_ref == block_decision:
                errors.append(f"{label} requires a new Human Decision for resolution")
        previous_blocked_at = blocked_time
        previous_resolved_at = resolved_time
    if record.get("status") == "BLOCKED":
        if len(unresolved_blocks) != 1:
            errors.append(
                f"Work Item {work_item_id}: BLOCKED requires exactly one unresolved block record"
            )
        elif unresolved_blocks[0] != len(block_records) - 1:
            errors.append(
                f"Work Item {work_item_id}: the unresolved block record must be the latest record"
            )
    elif unresolved_blocks:
        errors.append(
            f"Work Item {work_item_id}: only BLOCKED may retain an unresolved block record"
        )
    for field in IMPACT_FIELDS:
        value = record.get(field)
        if not isinstance(value, list) or not value or any(not isinstance(item, str) or not item for item in value):
            errors.append(f"Work Item {work_item_id}: {field} must be a non-empty list")
    applicability = record.get("applicability")
    if not isinstance(applicability, dict) or set(applicability) != {"code", *EVIDENCE_GATES}:
        errors.append(f"Work Item {work_item_id}: incomplete applicability")
        applicability = {}
    elif any(value not in APPLICABILITY for value in applicability.values()):
        errors.append(f"Work Item {work_item_id}: invalid applicability value")
    evidence = record.get("evidence")
    if not isinstance(evidence, dict) or set(evidence) != set(EVIDENCE_GATES):
        errors.append(f"Work Item {work_item_id}: incomplete evidence map")
        evidence = {}
    elif any(not isinstance(value, list) for value in evidence.values()):
        errors.append(f"Work Item {work_item_id}: evidence values must be lists")

    if record.get("status") in PREFLIGHT_STATUSES and not record.get("human_decision_refs"):
        errors.append(f"Work Item {work_item_id}: authorized work requires a Human Decision")

    start_head = record.get("start_head")
    if record.get("status") == "AUTHORIZED" and start_head != "UNKNOWN":
        errors.append(f"Work Item {work_item_id}: AUTHORIZED requires start_head=UNKNOWN")
    if record.get("agent_run_refs") and not SHA40.fullmatch(str(start_head)):
        errors.append(f"Work Item {work_item_id}: started work requires start_head")
    runtime_target = record["runtime_target"]
    # One-way coupling: no runtime target => no runtime gates; a runtime target requires the
    # runtime proof gate, while the deployment gate stays declared separately (a proof campaign
    # on an existing deployment is admissible; a deployment without runtime proof is not).
    if runtime_target == "NOT_APPLICABLE":
        for gate in ("deployment", "runtime_proof"):
            if applicability.get(gate) != "NOT_APPLICABLE":
                errors.append(f"Work Item {work_item_id}: runtime_target=NOT_APPLICABLE requires {gate}=NOT_APPLICABLE")
            if record.get(gate + "_status") != "NOT_APPLICABLE":
                errors.append(f"Work Item {work_item_id}: invalid {gate} status for runtime_target=NOT_APPLICABLE")
    else:
        if applicability.get("runtime_proof") != "APPLICABLE":
            errors.append(f"Work Item {work_item_id}: runtime_target={runtime_target} requires runtime_proof=APPLICABLE")
        for gate in ("deployment", "runtime_proof"):
            gate_applicability = applicability.get(gate)
            if gate_applicability == "APPLICABLE":
                allowed = {gate_levels(runtime_target)[gate], "FAILED", "NOT_REACHED", "UNKNOWN"}
            elif gate_applicability == "NOT_APPLICABLE":
                allowed = {"NOT_APPLICABLE"}
            else:
                allowed = {"NOT_REACHED", "UNKNOWN"}
            if record.get(gate + "_status") not in allowed:
                errors.append(f"Work Item {work_item_id}: invalid {gate} status for runtime_target={runtime_target}")

    if record.get("status") == "DONE":
        # close_head is checked against Git history by ProjectControl.done_evidence_errors,
        # which also knows whether the closure predates the project's adoption baseline.
        if any(value == "UNKNOWN" for value in applicability.values()):
            errors.append(f"Work Item {work_item_id}: DONE forbids UNKNOWN applicability")
        if record.get("owner") == "UNKNOWN":
            errors.append(f"Work Item {work_item_id}: DONE requires an owner")
        if not record.get("human_decision_refs"):
            errors.append(f"Work Item {work_item_id}: DONE requires a Human Decision")
        if not record.get("conversation_refs"):
            errors.append(f"Work Item {work_item_id}: DONE requires a conversation reference")
        code_applicable = applicability.get("code")
        if code_applicable == "APPLICABLE":
            if record.get("development_status") != "DEVELOPED":
                errors.append(f"Work Item {work_item_id}: applicable code requires DEVELOPED")
            if not record.get("commits"):
                errors.append(f"Work Item {work_item_id}: applicable code requires at least one commit")
            if not record.get("agent_run_refs"):
                errors.append(f"Work Item {work_item_id}: applicable code requires an Agent Run")
            forbidden_branches = {"UNKNOWN", canonical_branch} if canonical_branch else {"main", "master", "UNKNOWN"}
            if record.get("branch") in forbidden_branches:
                errors.append(f"Work Item {work_item_id}: applicable code requires a non-canonical branch")
        elif code_applicable == "NOT_APPLICABLE" and record.get("development_status") != "NOT_APPLICABLE":
            errors.append(f"Work Item {work_item_id}: non-applicable code must be NOT_APPLICABLE")
        gate_rules = {
            "tests": ("test_status", "TESTED"),
            "integration": ("integration_status", "INTEGRATED"),
            "deployment": ("deployment_status", gate_levels(runtime_target)["deployment"]),
            "runtime_proof": ("runtime_proof_status", gate_levels(runtime_target)["runtime_proof"]),
        }
        for gate, (status_field, passed_status) in gate_rules.items():
            applicability_value = applicability.get(gate)
            status_value = record.get(status_field)
            if applicability_value == "APPLICABLE":
                if status_value != passed_status:
                    errors.append(f"Work Item {work_item_id}: {gate} requires {status_field}={passed_status}")
                if not evidence.get(gate):
                    errors.append(f"Work Item {work_item_id}: {gate} requires evidence")
            elif applicability_value == "NOT_APPLICABLE" and status_value != "NOT_APPLICABLE":
                errors.append(f"Work Item {work_item_id}: non-applicable {gate} must be NOT_APPLICABLE")
        if record.get("close_condition") in {"", "UNKNOWN", None}:
            errors.append(f"Work Item {work_item_id}: DONE requires a close condition")
    return errors


def validate_conversation_reference(record: Any) -> list[str]:
    shape_errors = core_schema_errors(record, "conversation-reference")
    if shape_errors:
        return shape_errors
    required = (
        "$schema", "schema_version", "conversation_ref", "provider", "workspace", "title",
        "date", "purpose", "related_work_items", "external_reference", "summary_reference",
    )
    errors = required_field_errors(record, required, "Conversation")
    if errors or not isinstance(record, dict):
        return errors
    if not record.get("conversation_ref") or not record.get("provider"):
        errors.append("Conversation: provider and conversation_ref are required")
    related = record.get("related_work_items")
    if not isinstance(related, list) or any(not WORK_ITEM_ID.fullmatch(str(item)) for item in related):
        errors.append("Conversation: invalid related_work_items")
    if not re.fullmatch(r"UNKNOWN|[0-9]{4}-[0-9]{2}-[0-9]{2}", str(record.get("date", ""))):
        errors.append("Conversation: date must be YYYY-MM-DD or UNKNOWN")
    secret_keys = {
        key.lower() for key in record
        if any(token in key.lower() for token in ("secret", "password", "token", "api_key", "private_key"))
    }
    if secret_keys:
        errors.append(f"Conversation: forbidden secret-like fields {sorted(secret_keys)}")
    return errors


def validate_agent_run(record: Any) -> list[str]:
    shape_errors = core_schema_errors(record, "agent-run")
    if shape_errors:
        return shape_errors
    required = (
        "$schema", "schema_version", "agent_run_ref", "provider", "work_item_id",
        "requested_scope", "base_head", "branch", "started_at", "completed_at", "result",
        "commits", "report_reference",
    )
    errors = required_field_errors(record, required, "Agent Run")
    if errors or not isinstance(record, dict):
        return errors
    if not record.get("agent_run_ref") or not record.get("provider"):
        errors.append("Agent Run: provider and agent_run_ref are required")
    if not WORK_ITEM_ID.fullmatch(str(record.get("work_item_id", ""))):
        errors.append("Agent Run: invalid work_item_id")
    if record.get("base_head") != "UNKNOWN" and not SHA40.fullmatch(str(record.get("base_head", ""))):
        errors.append("Agent Run: invalid base_head")
    commits = record.get("commits")
    if not isinstance(commits, list) or any(not SHA40.fullmatch(str(item)) for item in commits):
        errors.append("Agent Run: invalid commits")
    if record.get("result") not in {"IN_PROGRESS", "SUCCEEDED", "FAILED", "PARTIAL", "BLOCKED", "UNKNOWN"}:
        errors.append("Agent Run: invalid result")
    return errors


def validate_record_links(
    work_items: Sequence[dict[str, Any]],
    conversations: Sequence[dict[str, Any]],
    agent_runs: Sequence[dict[str, Any]],
    human_decisions_text: str,
    frozen_decisions: AbstractSet[str] = frozenset(),
    legacy_done_ids: AbstractSet[str] = frozenset(),
) -> list[str]:
    errors: list[str] = []
    works = {item.get("work_item_id"): item for item in work_items}
    convs = {item.get("conversation_ref"): item for item in conversations}
    runs = {item.get("agent_run_ref"): item for item in agent_runs}
    decisions = set(re.findall(r"(?m)^## (HD-[0-9]{3,})\s*$", human_decisions_text))
    for work_id, work in works.items():
        for ref in work.get("human_decision_refs", []):
            if ref not in decisions:
                errors.append(
                    f"Work Item {work_id}: missing Human Decision {ref}: "
                    f"expected the Markdown heading `## {ref}` in {HUMAN_DECISIONS_PATH} "
                    "(see its Modèle section)"
                )
            else:
                # The exemption covers frozen history and nothing else: a decision recorded
                # before the adoption baseline, cited by a Work Item that was already closed
                # there. A Work Item still open at the baseline follows the current contract at
                # its next closure — the doctrine says so, and this is where it is enforced.
                exempt = ref in frozen_decisions and work_id in legacy_done_ids
                errors.extend(
                    f"Work Item {work_id}: invalid Human Decision — {error}"
                    for error in human_decision_errors(
                        human_decisions_text, ref, as_mandate=not exempt
                    )
                )
        for ref in work.get("conversation_refs", []):
            conversation = convs.get(ref)
            if conversation is None:
                errors.append(f"Work Item {work_id}: missing Conversation {ref}")
            elif work_id not in conversation.get("related_work_items", []):
                errors.append(f"Work Item {work_id}: Conversation {ref} is not reciprocal")
        run_refs = work.get("agent_run_refs", [])
        for run_index, ref in enumerate(run_refs):
            run = runs.get(ref)
            if run is None:
                errors.append(f"Work Item {work_id}: missing Agent Run {ref}")
            elif run.get("work_item_id") != work_id:
                errors.append(f"Work Item {work_id}: Agent Run {ref} is not reciprocal")
            else:
                if run.get("base_head") != work.get("base_head"):
                    errors.append(f"Work Item {work_id}: Agent Run {ref} base_head differs")
                if run_index == 0 and run.get("start_head") != work.get("start_head"):
                    errors.append(
                        f"Work Item {work_id}: first Agent Run {ref} start_head differs"
                    )
                if run.get("branch") != work.get("branch"):
                    errors.append(f"Work Item {work_id}: Agent Run {ref} branch differs")
                if run.get("requested_scope") != work.get("authorized_paths"):
                    errors.append(f"Work Item {work_id}: Agent Run {ref} requested_scope differs")
        work_block_records = work.get("block_records", [])
        first_block_precedes_first_run = bool(
            work_block_records
            and isinstance(work_block_records[0], dict)
            and work_block_records[0].get("agent_run_ref") is None
        )
        mapped_blocked_run_refs: set[str] = set()
        for block_index, block_record in enumerate(work_block_records):
            if not isinstance(block_record, dict):
                continue
            blocked_run_ref = block_record.get("agent_run_ref")
            expected_run_index = (
                block_index - 1 if first_block_precedes_first_run else block_index
            )
            expected_blocked_run_ref = (
                None
                if expected_run_index < 0
                else (
                    run_refs[expected_run_index]
                    if expected_run_index < len(run_refs)
                    else "MISSING_EXPECTED_AGENT_RUN"
                )
            )
            if blocked_run_ref != expected_blocked_run_ref:
                errors.append(
                    f"Work Item {work_id}: block_records[{block_index}].agent_run_ref "
                    f"must preserve lifecycle order; expected {expected_blocked_run_ref}"
                )
            if blocked_run_ref is not None:
                mapped_blocked_run_refs.add(str(blocked_run_ref))
                blocked_run = runs.get(blocked_run_ref)
                if blocked_run is None:
                    errors.append(
                        f"Work Item {work_id}: block_records[{block_index}] missing "
                        f"Agent Run {blocked_run_ref}"
                    )
                elif blocked_run.get("result") != "BLOCKED":
                    errors.append(
                        f"Work Item {work_id}: block_records[{block_index}] Agent Run "
                        f"{blocked_run_ref} must remain BLOCKED"
                    )
            for field in ("human_decision_id", "resolution_human_decision_id"):
                decision_ref = block_record.get(field)
                if decision_ref is None:
                    continue
                if decision_ref not in decisions:
                    errors.append(
                        f"Work Item {work_id}: block_records[{block_index}] missing "
                        f"Human Decision {decision_ref}"
                    )
                elif not human_decision_is_valid(
                    human_decisions_text,
                    str(decision_ref),
                    as_mandate=not (str(decision_ref) in frozen_decisions and work_id in legacy_done_ids),
                ):
                    errors.append(
                        f"Work Item {work_id}: block_records[{block_index}] invalid "
                        f"Human Decision {decision_ref}"
                    )
                elif not human_decision_relates_to_work_item(
                    human_decisions_text,
                    str(decision_ref),
                    str(work_id),
                ):
                    errors.append(
                        f"Work Item {work_id}: block_records[{block_index}] Human Decision "
                        f"{decision_ref} is not related to the Work Item"
                    )
                elif human_decision_field(
                    human_decisions_text,
                    str(decision_ref),
                    "Chosen option",
                ) != "AUTHORIZE":
                    errors.append(
                        f"Work Item {work_id}: block_records[{block_index}] Human Decision "
                        f"{decision_ref} does not choose AUTHORIZE"
                    )
                elif field == "human_decision_id" and (
                    human_decision_field(
                        human_decisions_text,
                        str(decision_ref),
                        "Project Control action",
                    )
                    != "BLOCK"
                    or human_decision_field(
                        human_decisions_text,
                        str(decision_ref),
                        "Block reason code",
                    )
                    != block_record.get("reason_code")
                    or human_decision_field(
                        human_decisions_text,
                        str(decision_ref),
                        "Resume condition recorded",
                    )
                    != block_record.get("resume_condition")
                ):
                    errors.append(
                        f"Work Item {work_id}: block_records[{block_index}] Human Decision "
                        f"{decision_ref} does not authorize the exact block"
                    )
                elif field == "resolution_human_decision_id" and (
                    human_decision_field(
                        human_decisions_text,
                        str(decision_ref),
                        "Project Control action",
                    )
                    != "RESUME"
                    or human_decision_field(
                        human_decisions_text,
                        str(decision_ref),
                        "Resume condition confirmed",
                    )
                    != block_record.get("resume_condition")
                ):
                    errors.append(
                        f"Work Item {work_id}: block_records[{block_index}] Human Decision "
                        f"{decision_ref} does not confirm the exact resume condition"
                    )
        linked_runs = [runs.get(ref) for ref in run_refs if runs.get(ref) is not None]
        actual_blocked_run_refs = {
            str(ref)
            for ref in run_refs
            if runs.get(ref) is not None and runs[ref].get("result") == "BLOCKED"
        }
        if actual_blocked_run_refs != mapped_blocked_run_refs:
            errors.append(
                f"Work Item {work_id}: BLOCKED Agent Runs and block record mappings "
                "must be reciprocal"
            )
        if work.get("status") == "BLOCKED" and linked_runs:
            if any(run.get("result") == "IN_PROGRESS" for run in linked_runs):
                errors.append(f"Work Item {work_id}: BLOCKED forbids an active Agent Run")
            if linked_runs[-1].get("result") != "BLOCKED":
                errors.append(f"Work Item {work_id}: BLOCKED requires the latest Agent Run BLOCKED")
        block_records = work.get("block_records", [])
        if work.get("status") == "IN_PROGRESS" and block_records:
            unresolved = [
                block_record
                for block_record in block_records
                if isinstance(block_record, dict) and block_record.get("resolved_at") is None
            ]
            if not unresolved:
                active_runs = [
                    run for run in linked_runs if run.get("result") == "IN_PROGRESS"
                ]
                if len(active_runs) != 1 or not linked_runs or active_runs[0] is not linked_runs[-1]:
                    errors.append(
                        f"Work Item {work_id}: resumed IN_PROGRESS requires exactly one "
                        "new latest active Agent Run"
                    )
                else:
                    latest_resolution = parse_timestamp(
                        block_records[-1].get("resolved_at")
                        if isinstance(block_records[-1], dict)
                        else None
                    )
                    resumed_at = parse_timestamp(linked_runs[-1].get("started_at"))
                    if (
                        latest_resolution is not None
                        and resumed_at is not None
                        and resumed_at < latest_resolution
                    ):
                        errors.append(
                            f"Work Item {work_id}: resumed Agent Run predates block resolution"
                        )
    for ref, conversation in convs.items():
        for work_id in conversation.get("related_work_items", []):
            if work_id not in works:
                errors.append(f"Conversation {ref}: missing Work Item {work_id}")
    for ref, run in runs.items():
        work_id = run.get("work_item_id")
        if work_id not in works:
            errors.append(f"Agent Run {ref}: missing Work Item {work_id}")
            continue
        if ref not in works[work_id].get("agent_run_refs", []):
            errors.append(f"Agent Run {ref}: Work Item {work_id} does not reference the run")
        extra = set(run.get("commits", [])) - set(works[work_id].get("commits", []))
        if works[work_id].get("status") == "DONE" and extra:
            errors.append(f"Agent Run {ref}: commits absent from Work Item {work_id}: {sorted(extra)}")
    return errors


class ProjectControl:
    def __init__(self, root: Path = ROOT):
        self.root = root.resolve()
        self.first_start = self.root / "FIRST_START.md"
        self.project_state_path = self.root / "project_control/project-state.v1.json"
        self.roadmap_json = self.root / "docs/governance/roadmap-state.v1.json"
        self.roadmap_md = self.root / "docs/governance/ROADMAP.md"
        self.human_decisions = self.root / HUMAN_DECISIONS_PATH
        self.worktree_registry = self.root / "docs/governance/WORKTREE_REGISTRY.md"
        self.classifications_path = self.root / "docs/governance/git-path-classifications.v1.json"
        self.routing_json = self.root / "docs/agent-governance/mandatory-documents.v1.json"
        self.ideas_json = self.root / IDEAS_JSON_PATH
        self.ideas_md = self.root / IDEAS_MD_PATH
        self.last_alignment: dict[str, str | None] = {"mode": "NONE", "commit": None}

    def run_git(self, args: Sequence[str], text: bool = True) -> subprocess.CompletedProcess:
        return subprocess.run(["git", *args], cwd=self.root, check=False, capture_output=True, text=text)

    def repository_context(self) -> dict[str, str]:
        top = self.run_git(["rev-parse", "--show-toplevel"])
        branch = self.run_git(["branch", "--show-current"])
        head = self.run_git(["rev-parse", "HEAD"])
        return {
            "root": top.stdout.strip() if top.returncode == 0 else "UNKNOWN",
            "branch": branch.stdout.strip() or "DETACHED_OR_UNBORN",
            "head": head.stdout.strip() if head.returncode == 0 else "UNBORN",
        }

    def changed_paths(self) -> list[str]:
        """Every path the working state changes — a rename counts on BOTH sides.

        A rename removes its origin: classifying only the destination let a Work Item move a
        file out of a location it was never authorized to touch while every scope check
        passed. A copy leaves its origin intact, so only its destination is a change.
        """
        result = self.run_git(["status", "--porcelain=v1", "-z", "--untracked-files=all"], text=False)
        if result.returncode != 0:
            return ["<git-status-failed>"]
        chunks = result.stdout.split(b"\0")
        paths: list[str] = []
        index = 0
        while index < len(chunks):
            chunk = chunks[index]
            index += 1
            if not chunk:
                continue
            decoded = chunk.decode("utf-8", errors="surrogateescape")
            status = decoded[:2]
            paths.append(decoded[3:] if len(decoded) >= 4 else decoded)
            if "R" in status or "C" in status:
                origin = chunks[index].decode("utf-8", errors="surrogateescape") if index < len(chunks) else ""
                index += 1
                if "R" in status and origin:
                    paths.append(origin)
        return paths

    def first_start_status(self) -> str:
        try:
            text = self.first_start.read_text(encoding="utf-8")
        except OSError:
            return "INVALID"
        match = re.search(r"INITIALIZATION_STATUS:\s*(NOT_STARTED|COMPLETE)", text)
        return match.group(1) if match else "INVALID"

    def project_state(self) -> dict[str, Any]:
        return load_json(self.project_state_path)

    def canonical_branch(self) -> str:
        try:
            text = (self.root / "docs/governance/REPOSITORY_STATUS.md").read_text(encoding="utf-8")
        except OSError as exc:
            raise ProjectControlError(f"cannot read canonical branch declaration: {exc}") from exc
        matches = re.findall(
            r"(?m)^[ \t]*`CANONICAL BRANCH:\s*([^`\r\n]+)`[ \t]*$",
            text,
        )
        if len(matches) != 1:
            raise ProjectControlError(
                "canonical branch declaration must appear exactly once; "
                f"found {len(matches)}"
            )
        branch = matches[0].strip()
        if (
            branch in {"UNKNOWN", "NOT_YET_ESTABLISHED", ""}
            or not BRANCH_NAME.fullmatch(branch)
            or self.run_git(["check-ref-format", "--branch", branch]).returncode != 0
        ):
            raise ProjectControlError(f"invalid canonical branch declaration: {branch}")
        return branch

    def record_files(self, directory: str) -> list[Path]:
        return sorted((self.root / directory).glob("*.json"))

    def records(self, directory: str) -> list[dict[str, Any]]:
        records = [load_json(path) for path in self.record_files(directory)]
        schema_names = {"project_control/work-items": "work-item",
                        "project_control/conversations": "conversation-reference",
                        "project_control/agent-runs": "agent-run"}
        for record in records:
            errors = core_schema_errors(record, schema_names[directory])
            if errors:
                raise ProjectControlError("invalid record: " + "; ".join(errors))
        return records

    def parse_roadmap_table(self) -> dict[str, dict[str, str]]:
        rows: dict[str, dict[str, str]] = {}
        for line in self.roadmap_md.read_text(encoding="utf-8").splitlines():
            if not re.match(r"^\| WI-[0-9]{3,} \|", line):
                continue
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) < 7:
                continue
            work_id, display, title, status, integration, human_gate, dependencies = cells[:7]
            rows[work_id] = {
                "display_reference": display, "title": title, "status": status,
                "integration_state": integration, "human_gate": human_gate,
                "dependencies": [] if dependencies == "—" else [value.strip() for value in dependencies.split(",")],
            }
        return rows

    def common_findings(self, include_traceability: bool = True) -> list[Finding]:
        findings: list[Finding] = []
        context = self.repository_context()
        add(findings, "GIT_REPOSITORY", context["root"] == str(self.root), f"root={context['root']}")
        missing = [path for path in REQUIRED_FILES if not (self.root / path).is_file()]
        add(findings, "MANDATORY_FILES", not missing, "all mandatory files present" if not missing else f"missing: {missing}")
        json_errors: list[str] = []
        schema_errors: list[str] = []
        for path in sorted(self.root.rglob("*.json")):
            if ".git" in path.parts:
                continue
            try:
                payload = load_json(path)
            except (OSError, json.JSONDecodeError, ProjectControlError) as exc:
                json_errors.append(f"{path.relative_to(self.root)}: {exc}")
                continue
            if path.name.endswith(".schema.json"):
                schema_errors.extend(schema_shape_errors(payload, str(path.relative_to(self.root))))
        add(findings, "JSON_SYNTAX", not json_errors, "all JSON files parse" if not json_errors else "; ".join(json_errors))
        add(findings, "SCHEMA_FOUNDATION", not schema_errors, "all schemas expose object contracts" if not schema_errors else "; ".join(schema_errors))

        routing_errors: list[str] = []
        try:
            routing = load_json(self.routing_json)
            routed = list(routing.get("base", []))
            for documents in routing.get("scopes", {}).values():
                if isinstance(documents, list):
                    routed.extend(documents)
                else:
                    routing_errors.append("scope value is not a list")
            for value in routed:
                path = safe_relative_path(str(value))
                if path is None or not (self.root / path).is_file():
                    routing_errors.append(f"invalid routed authority: {value}")
                elif path.startswith("templates/"):
                    routing_errors.append(f"optional template routed as authority: {path}")
        except (OSError, json.JSONDecodeError, ProjectControlError) as exc:
            routing_errors.append(str(exc))
        add(findings, "DOCUMENT_ROUTING", not routing_errors, "all authorities resolve inside core" if not routing_errors else "; ".join(routing_errors))

        roadmap_errors = self.roadmap_errors()
        add(findings, "ROADMAP", not roadmap_errors, "human and machine roadmaps are synchronized" if not roadmap_errors else "; ".join(roadmap_errors))
        ideas_errors = self.ideas_errors()
        add(findings, "IDEAS", not ideas_errors, "human and machine idea lists are synchronized" if not ideas_errors else "; ".join(ideas_errors))
        view_summary, view_errors = self.roadmap_view_audit()
        add(findings, "ROADMAP_VIEW", not view_errors, view_summary if not view_errors else "; ".join(view_errors))
        registry_errors = self.registry_errors()
        add(
            findings,
            "WORKTREE_REGISTRY",
            not registry_errors,
            "all declared branches have one synchronized lifecycle entry"
            if not registry_errors
            else "; ".join(registry_errors),
        )
        record_errors = self.project_control_errors()
        add(findings, "SCHEMA_VALIDATION", not record_errors, "Project Control records and links validate" if not record_errors else "; ".join(record_errors))
        legacy_summary, legacy_present, legacy_frozen = self.legacy_audit()
        add(findings, "LEGACY_RECORDS_PRESENT", not legacy_present, legacy_summary if not legacy_present else "; ".join(legacy_present))
        add(findings, "LEGACY_EVIDENCE_FROZEN", not legacy_frozen, legacy_summary if not legacy_frozen else "; ".join(legacy_frozen))
        authorities_summary, authorities_errors = self.authorities_baseline_audit()
        add(findings, "AUTHORITIES_BASELINE", not authorities_errors, authorities_summary if not authorities_errors else "; ".join(authorities_errors))
        language = self.language()
        language_ok = language in LANGUAGES or (language == "UNKNOWN" and self.operating_mode() == "BOOTSTRAP_MODE")
        add(findings, "LANGUAGE", language_ok,
            f"language={language} — {LANGUAGE_LABELS.get(language, language)}" if language_ok
            else f"language={language}; the Project Owner chooses FR or EN (FIRST_START interview or Human Decision)")
        style = self.reporting_style()
        style_ok = style in REPORTING_STYLES or (style == "UNKNOWN" and self.operating_mode() == "BOOTSTRAP_MODE")
        add(findings, "REPORTING_STYLE", style_ok,
            f"reporting_style={style} — {REPORTING_STYLE_LABELS.get(style, style)}" if style_ok
            else f"reporting_style={style}; the Project Owner chooses TECHNICAL or PLAIN (FIRST_START interview or Human Decision)")
        generality_errors = self.generality_errors()
        add(findings, "GENERAL_PURPOSE_CORE", not generality_errors, "no active legacy or domain-specific dependency" if not generality_errors else "; ".join(generality_errors))
        core_errors = self.core_manifest_errors()
        add(findings, "CORE_MANIFEST", not core_errors,
            f"skeleton_version {self.core_status()['skeleton_version']}; core files present; AGENTS.md includes the core"
            if not core_errors else "; ".join(core_errors))
        if self.operating_mode() == "BOOTSTRAP_MODE":
            business_files = self.business_files()
            add(
                findings,
                "NO_ACTIVE_BUSINESS_CAPABILITY",
                not business_files,
                "applications/modules/shared contain documentation only"
                if not business_files
                else f"active paths: {business_files}",
            )
        else:
            authorization_errors = self.business_change_authorization_errors()
            add(
                findings,
                "BUSINESS_CHANGE_AUTHORIZATION",
                not authorization_errors,
                "no current business changes or all changes belong to the unique active Work Item"
                if not authorization_errors
                else "; ".join(authorization_errors),
            )
        symlinks = [str(path.relative_to(self.root)) for path in self.root.rglob("*") if ".git" not in path.parts and path.is_symlink()]
        gate = self.commit_gate_state()
        add(findings, "COMMIT_GATE", gate != "MISMATCH", {
            "INSTALLED": "gate installed outside the worktree and identical to its reference",
            "IN_TREE": f"gate run from {HOOKS_PATH} inside the worktree: a commit can remove it — install-gate",
            "NOT_INSTALLED": "no commit gate installed — install-gate",
            "MISMATCH": f"the installed gate differs from {HOOKS_PATH}/pre-commit or is not executable — install-gate",
        }[gate])
        indexed = self.indexed_symlinks()
        hidden = sorted(set(indexed) - set(symlinks))
        add(findings, "NO_SYMLINKS", not symlinks and not indexed,
            "no repository symlink in the worktree or the index" if not symlinks and not indexed
            else "; ".join(part for part in (
                f"worktree symlinks: {symlinks}" if symlinks else "",
                f"symlinks staged but not in the worktree: {hidden}" if hidden else "",
            ) if part))
        initialization_errors = self.initialization_state_errors()
        add(findings, "INITIALIZATION_STATE", not initialization_errors, f"mode={self.operating_mode()}" if not initialization_errors else "; ".join(initialization_errors))
        if include_traceability:
            trace_errors = self.traceability_errors()
            add(findings, "GIT_TRACEABILITY", not trace_errors, "all changed paths classified" if not trace_errors else "; ".join(trace_errors))
        return findings

    def roadmap_errors(self) -> list[str]:
        errors: list[str] = []
        try:
            state = load_json(self.roadmap_json)
            rows = self.parse_roadmap_table()
        except (OSError, json.JSONDecodeError, ProjectControlError) as exc:
            return [str(exc)]
        shape_errors = core_schema_errors(state, "roadmap-state")
        if shape_errors:
            return shape_errors
        if "lots" in state:
            errors.append("legacy lots collection is forbidden")
        summaries = state.get("work_items")
        if not isinstance(summaries, list):
            return errors + ["roadmap work_items must be a list"]
        ids = [item.get("work_item_id") for item in summaries if isinstance(item, dict)]
        if len(ids) != len(set(ids)):
            errors.append("duplicate roadmap Work Item IDs")
        for summary in summaries:
            if not isinstance(summary, dict):
                errors.append("roadmap Work Item is not an object")
                continue
            work_id = str(summary.get("work_item_id", ""))
            if not WORK_ITEM_ID.fullmatch(work_id):
                errors.append(f"invalid roadmap Work Item ID: {work_id}")
            if summary.get("status") not in WORK_ITEM_STATUSES:
                errors.append(f"{work_id}: invalid status")
            if summary.get("integration_state") not in INTEGRATION_STATES:
                errors.append(f"{work_id}: invalid integration_state")
            row = rows.get(work_id)
            if row is None:
                errors.append(f"{work_id}: missing from ROADMAP.md")
                continue
            for key in ("display_reference", "title", "status", "integration_state", "human_gate"):
                if str(summary.get(key)) != row.get(key):
                    errors.append(f"{work_id}: {key} differs between Markdown and JSON")
            if summary.get("dependencies") != row.get("dependencies"):
                errors.append(f"{work_id}: dependencies differ between Markdown and JSON")
        extra = set(rows) - set(ids)
        if extra:
            errors.append(f"Markdown-only Work Items: {sorted(extra)}")
        return errors

    # --- Ideas (P12): what the Project Owner said, in two synchronized forms. ---
    # --- An idea decides nothing; it points to the Work Item, version or decision ---
    # --- that carries it, and leaves the list only as REALIZED or DISCARDED.      ---

    def load_ideas(self) -> dict[str, Any]:
        state = load_json(self.ideas_json)
        errors = core_schema_errors(state, "ideas-state")
        if errors:
            raise ProjectControlError("invalid ideas state: " + "; ".join(errors))
        return state

    def idea_target_errors(self, idea_id: str, target: Any, state: str, roadmap_ids: set[str]) -> list[str]:
        if target is None:
            return [f"{idea_id}: DISCARDED requires the target that names the discarding decision"] if state == "DISCARDED" else []
        value = str(target)
        if WORK_ITEM_ID.fullmatch(value):
            return [] if value in roadmap_ids else [f"{idea_id}: target {value} is not in the roadmap"]
        if HUMAN_DECISION_ID.fullmatch(value):
            try:
                text = self.human_decisions.read_text(encoding="utf-8")
            except OSError as exc:
                return [f"{idea_id}: cannot read Human Decisions: {exc}"]
            return [] if human_decision_field(text, value, "Decision") is not None else [f"{idea_id}: target {value} is not recorded"]
        return []

    def ideas_errors(self) -> list[str]:
        try:
            state = load_json(self.ideas_json)
            rows = parse_ideas_table(self.ideas_md.read_text(encoding="utf-8"))
            roadmap = load_json(self.roadmap_json)
        except (OSError, json.JSONDecodeError, ProjectControlError) as exc:
            return [str(exc)]
        shape_errors = core_schema_errors(state, "ideas-state")
        if shape_errors:
            return shape_errors
        if list(state.get("idea_state_values", [])) != list(IDEA_STATES):
            return ["ideas-state: idea_state_values must list the closed idea states in order"]
        roadmap_ids = {
            str(item.get("work_item_id")) for item in roadmap.get("work_items", []) if isinstance(item, dict)
        } if isinstance(roadmap, dict) else set()
        errors: list[str] = []
        ideas = state.get("ideas", [])
        ids = [idea.get("idea_id") for idea in ideas]
        if len(ids) != len(set(ids)):
            errors.append("duplicate idea IDs")
        for idea in ideas:
            idea_id = str(idea.get("idea_id"))
            errors.extend(self.idea_target_errors(idea_id, idea.get("target"), str(idea.get("state")), roadmap_ids))
            row = rows.get(idea_id)
            if row is None:
                errors.append(f"{idea_id}: missing from IDEAS.md")
                continue
            expected = {
                "stated_at": ideas_cell(idea.get("stated_at")), "quote": ideas_cell(idea.get("quote")),
                "state": str(idea.get("state")), "target": ideas_cell(idea.get("target")),
                "source": ideas_cell(idea.get("source")),
            }
            for key, value in expected.items():
                if row.get(key) != value:
                    errors.append(f"{idea_id}: {key} differs between Markdown and JSON")
        extra = set(rows) - set(str(value) for value in ids)
        if extra:
            errors.append(f"Markdown-only ideas: {sorted(extra)}")
        return errors

    def next_idea_id(self, state: dict[str, Any]) -> str:
        numbers = [int(str(idea.get("idea_id"))[3:]) for idea in state.get("ideas", []) if IDEA_ID.fullmatch(str(idea.get("idea_id")))]
        return f"ID-{(max(numbers) + 1 if numbers else 1):03d}"

    def record_idea(self, args: argparse.Namespace) -> str:
        """`idea add` / `idea set`: write both forms; commit them on the canonical branch in NORMAL_MODE."""
        mode = self.operating_mode()
        if mode not in {"NORMAL_MODE", "BOOTSTRAP_MODE"}:
            raise ProjectControlError(f"idea requires a valid FIRST_START status, got {mode}")
        state = self.load_ideas()
        ideas: list[dict[str, Any]] = list(state.get("ideas", []))
        roadmap_ids = {str(item.get("work_item_id")) for item in load_json(self.roadmap_json).get("work_items", [])}
        if args.idea_command == "add":
            idea_id = self.next_idea_id(state)
            stated_at = args.stated_at or today_iso()
            if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", stated_at):
                raise ProjectControlError("--stated-at must be YYYY-MM-DD")
            idea = {
                "idea_id": idea_id, "stated_at": stated_at,
                "quote": clean_cli_text(args.quote, "--quote"), "source": clean_cli_text(args.source, "--source"),
                "state": args.state, "target": clean_cli_text(args.target, "--target") if args.target else None,
                "note": clean_cli_text(args.note, "--note") if args.note else "",
            }
            ideas.append(idea)
        else:
            idea_id = args.idea_id.upper()
            matches = [index for index, idea in enumerate(ideas) if idea.get("idea_id") == idea_id]
            if len(matches) != 1:
                raise ProjectControlError(f"unknown idea: {idea_id}")
            idea = dict(ideas[matches[0]])
            if args.state:
                idea["state"] = args.state
            if args.target is not None:
                idea["target"] = clean_cli_text(args.target, "--target") if args.target else None
            if args.note is not None:
                idea["note"] = clean_cli_text(args.note, "--note") if args.note else ""
            ideas[matches[0]] = idea
        if idea["state"] not in IDEA_STATES:
            raise ProjectControlError(f"invalid idea state: {idea['state']}")
        target_errors = self.idea_target_errors(idea_id, idea.get("target"), idea["state"], roadmap_ids)
        if target_errors:
            raise ProjectControlError("; ".join(target_errors))
        canonical_branch: str | None = None
        if mode == "NORMAL_MODE":
            self.validate_clean_administrative_baseline()
            canonical_branch, _ = self.require_canonical_checkout("idea")
            self.require_clean_worktree("idea")
        state["ideas"] = sorted(ideas, key=lambda value: value["idea_id"])
        state["updated_at"] = now_iso()
        transaction = FileTransaction(self.root)
        committed: tuple[str, str] | None = None
        try:
            transaction.write_json(IDEAS_JSON_PATH, state)
            transaction.write_text(IDEAS_MD_PATH, render_ideas_markdown(self.ideas_md.read_text(encoding="utf-8"), state["ideas"]))
            errors = self.ideas_errors()
            if errors:
                raise ProjectControlError("idea refused: " + "; ".join(errors))
            if canonical_branch is not None:
                committed = self.commit_records(transaction, f"chore(project-control): idea {idea_id} {idea['state']}")
            transaction.commit()
        except BaseException as exc:
            if committed is not None:
                rollback_errors = self.uncommit_records(transaction, str(canonical_branch), *committed)
                if rollback_errors:
                    raise ProjectControlError(f"idea failed: {exc}; ROLLBACK FAILED: {'; '.join(rollback_errors)}") from exc
            else:
                transaction.rollback()
            raise
        return idea_id

    # --- Roadmap view (P12, P6): computed from the repository's files, rendered by ---
    # --- scripts/roadmap_view.py; it displays and never decides.                    ---

    def repository_role(self) -> str:
        try:
            return str(self.project_state().get("repository_role", "UNKNOWN"))
        except (OSError, json.JSONDecodeError, ProjectControlError):
            return "UNKNOWN"

    def view_paths(self) -> dict[str, str]:
        if self.repository_role() == "PROJECT_TEMPLATE":
            return {"settings": TEMPLATE_VIEW_SETTINGS_PATH, "markdown": TEMPLATE_VIEW_MARKDOWN_PATH,
                    "html": TEMPLATE_VIEW_HTML_PATH, "roadmap": TEMPLATE_ROADMAP_PATH}
        return {"settings": VIEW_SETTINGS_PATH, "markdown": VIEW_MARKDOWN_PATH, "html": VIEW_HTML_PATH, "roadmap": ""}

    def load_view_settings(self) -> dict[str, Any]:
        path = self.root / self.view_paths()["settings"]
        if not path.is_file():
            path = self.root / VIEW_SETTINGS_PATH
        settings = load_json(path)
        errors = core_schema_errors(settings, "roadmap-view")
        if errors:
            raise ProjectControlError("invalid roadmap view settings: " + "; ".join(errors))
        return settings

    def load_template_roadmap(self) -> dict[str, Any] | None:
        path = self.root / TEMPLATE_ROADMAP_PATH
        if self.repository_role() != "PROJECT_TEMPLATE" or not path.is_file():
            return None
        roadmap = load_json(path)
        errors = core_schema_errors(roadmap, "template-roadmap")
        if errors:
            raise ProjectControlError("invalid template roadmap: " + "; ".join(errors))
        return roadmap

    def template_roadmap_errors(self) -> list[str]:
        try:
            roadmap = self.load_template_roadmap()
        except (OSError, json.JSONDecodeError, ProjectControlError) as exc:
            return [str(exc)]
        if roadmap is None:
            return []
        errors: list[str] = []
        ids = [item.get("id") for item in roadmap.get("chantiers", [])]
        if len(ids) != len(set(ids)):
            errors.append("template roadmap: duplicate chantier IDs")
        idea_ids = [idea.get("idea_id") for idea in roadmap.get("ideas", [])]
        if len(idea_ids) != len(set(idea_ids)):
            errors.append("template roadmap: duplicate idea IDs")
        for item in roadmap.get("chantiers", []):
            scope = item.get("scope")
            if scope is not None and (safe_relative_path(str(scope)) is None or not (self.root / str(scope)).is_file()):
                errors.append(f"template roadmap: {item.get('id')} scope file missing: {scope}")
        versions = {version.get("version") for version in roadmap.get("versions", [])}
        if roadmap.get("template", {}).get("current_version") not in versions:
            errors.append("template roadmap: current_version is not listed in versions")
        for idea in roadmap.get("ideas", []):
            if idea.get("state") == "DISCARDED" and not idea.get("target"):
                errors.append(f"template roadmap: {idea.get('idea_id')} DISCARDED requires a target")
        return errors

    def roadmap_view_audit(self) -> tuple[str, list[str]]:
        try:
            settings = self.load_view_settings()
        except (OSError, json.JSONDecodeError, ProjectControlError) as exc:
            return str(exc), [str(exc)]
        errors = self.template_roadmap_errors()
        if errors:
            return "; ".join(errors), errors
        state = self.roadmap_view_state()
        labels = {"CURRENT": "generated view is current", "STALE": "generated view is stale — run roadmap-view --write",
                  "MISSING": "no generated view yet — run roadmap-view --write"}
        return f"settings valid (regeneration {settings.get('regeneration')}); {labels[state]}", []

    def roadmap_view_sources(self) -> list[str]:
        paths = self.view_paths()
        if self.repository_role() == "PROJECT_TEMPLATE":
            candidates = [TEMPLATE_ROADMAP_PATH, paths["settings"], "provenance/CHANGELOG.md", CORE_MANIFEST_PATH]
        else:
            candidates = [
                "docs/governance/roadmap-state.v1.json", "docs/governance/ROADMAP.md",
                "docs/governance/HUMAN_DECISIONS.md", IDEAS_JSON_PATH, IDEAS_MD_PATH,
                "project_control/project-state.v1.json", paths["settings"],
                "docs/governance/REPOSITORY_STATUS.md", CORE_MANIFEST_PATH,
                *(str(path.relative_to(self.root)) for path in self.record_files("project_control/work-items")),
            ]
        return sorted(path for path in dict.fromkeys(candidates) if (self.root / path).is_file())

    def displayed_version_tags(self) -> str:
        """The version tags the view displays, as a stable text.

        The view names the promoted version from the repository's tags, not from a file. A tag
        added, moved or deleted therefore changes what the view says without changing a single
        source file — so it belongs to the freshness digest. The current commit and the remote
        heads are deliberately left out: committing the view would then make it stale at once,
        and pushing it again after every regeneration, with no end."""
        return "\n".join(f"{tag['tag']}@{tag['commit']}" for tag in self.version_tags())

    def roadmap_view_sources_digest(self) -> tuple[str, list[dict[str, str]]]:
        entries = [{"path": path, "sha256": file_sha256(self.root / path)} for path in self.roadmap_view_sources()]
        entries.append({
            "path": speak(self.speech(), "sources.version_tags"),
            "sha256": hashlib.sha256(self.displayed_version_tags().encode("utf-8")).hexdigest(),
        })
        return manifest_digest(entries), entries

    def roadmap_view_is_inherited(self) -> bool:
        """Was the generated view produced at a commit this repository does not have?

        A copy exported from another tree carries that tree's view. Its marker names the commit it
        was generated at; when that commit is unknown here, the file describes somewhere else."""
        markdown = self.root / self.view_paths()["markdown"]
        if not markdown.is_file():
            return False
        try:
            marker = self.roadmap_view_module().parse_view_marker(markdown.read_text(encoding="utf-8"))
        except OSError:
            return False
        head = (marker or {}).get("head", "")
        if not SHA40.fullmatch(str(head)):
            return False
        return self.run_git(["cat-file", "-e", f"{head}^{{commit}}"]).returncode != 0

    def roadmap_view_state(self) -> str:
        """CURRENT, STALE or MISSING: does the committed Markdown view match the sources?"""
        markdown = self.root / self.view_paths()["markdown"]
        if not markdown.is_file():
            return "MISSING"
        module = self.roadmap_view_module()
        try:
            marker = module.parse_view_marker(markdown.read_text(encoding="utf-8"))
        except OSError:
            return "MISSING"
        if marker is None:
            return "MISSING"
        return "CURRENT" if marker["sources_digest"] == self.roadmap_view_sources_digest()[0] else "STALE"

    def roadmap_view_module(self) -> Any:
        cached = getattr(self, "_roadmap_view_module", None)
        if cached is not None:
            return cached
        path = self.root / "scripts/roadmap_view.py"
        spec = importlib.util.spec_from_file_location("governed_roadmap_view", path)
        if spec is None or spec.loader is None:
            raise ProjectControlError("cannot load scripts/roadmap_view.py")
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        self._roadmap_view_module = module
        return module

    def git_lines(self, args: Sequence[str]) -> list[str]:
        result = self.run_git(list(args))
        return result.stdout.splitlines() if result.returncode == 0 else []

    def git_paths(self, args: Sequence[str]) -> list[str]:
        """Paths listed by a Git command, read as they are: the command is run with `-z`, so a
        name Git would otherwise quote and escape — an accent, a space, a tab — comes back
        exactly as the file is named. Read from `git diff --name-only` without `-z`, a name such
        as `résumé.py` came back as `"r\\303\\251sum\\303\\251.py"`, every later lookup on it
        failed, and two failures compared equal (fifth independent control, F-02 and F-04)."""
        result = self.run_git([*args, "-z"], text=False)
        if result.returncode != 0:
            return []
        return [entry.decode("utf-8", "surrogateescape") for entry in result.stdout.split(b"\0") if entry]

    def version_tags(self) -> list[dict[str, Any]]:
        """Annotated or lightweight version tags of the repository, oldest first."""
        tags: list[dict[str, Any]] = []
        for line in self.git_lines(["for-each-ref", "--format=%(refname:short)\t%(creatordate:short)\t%(*objectname)%(objectname)", "refs/tags"]):
            parts = line.split("\t")
            if len(parts) < 3 or not VERSION_TAG.fullmatch(parts[0]):
                continue
            commit = self.run_git(["rev-list", "-n", "1", parts[0]]).stdout.strip()
            tags.append({"version": parts[0].lstrip("v"), "tag": parts[0], "date": parts[1], "commit": commit})
        tags.sort(key=lambda tag: version_tuple(tag["version"]))
        return tags

    def remote_heads(self, branch: str) -> dict[str, str]:
        heads: dict[str, str] = {}
        for line in self.git_lines(["for-each-ref", "--format=%(refname:short)\t%(objectname)", "refs/remotes"]):
            name, _, head = line.partition("\t")
            if name.endswith(f"/{branch}"):
                heads[name.rsplit("/", 1)[0]] = head
        return heads

    def commit_date(self, commit: str) -> str:
        lines = self.git_lines(["log", "-1", "--format=%cs", commit]) if SHA40.fullmatch(str(commit)) else []
        return lines[0] if lines else ""

    def human_decision_entries(self) -> list[dict[str, str]]:
        try:
            text = self.human_decisions.read_text(encoding="utf-8")
        except OSError:
            return []
        entries = []
        for match in re.finditer(r"(?ms)^## (HD-[0-9]{3,})\s*$\n(.*?)(?=^## HD-[0-9]{3,}\s*$|\Z)", text):
            block = match.group(2)
            decision = re.search(r"(?m)^Decision:[ \t]*(\S.*)$", block)
            date = re.search(r"(?m)^Date:[ \t]*(\S.*)$", block)
            entries.append({"id": match.group(1), "decision": decision.group(1).strip() if decision else "UNKNOWN",
                            "date": date.group(1).strip() if date else ""})
        return entries

    def roadmap_view_model(self, style_override: str | None = None) -> dict[str, Any]:
        """The data the renderers turn into the page and the Markdown view."""
        module = self.roadmap_view_module()
        settings = self.load_view_settings()
        role = self.repository_role()
        context = self.repository_context()
        style = style_override or settings.get("style", "FOLLOW_REPORTING_STYLE")
        if style == "FOLLOW_REPORTING_STYLE":
            style = "TECHNICAL" if self.reporting_style() == "TECHNICAL" else "PLAIN"
        findings = self.bootstrap_findings() if self.operating_mode() == "BOOTSTRAP_MODE" else self.audit_findings()
        failures = [f"{item.check}: {item.detail}" for item in findings if item.status == "FAIL"]
        audit_status = "FAIL" if failures else "PASS"
        core = self.core_status()
        digest, sources = self.roadmap_view_sources_digest()
        tags = self.version_tags()
        current_tag = next((tag for tag in reversed(tags) if tag["commit"] == context["head"]), None)
        # Backups are judged on the canonical branch: a work branch is not pushed before promotion.
        try:
            canonical_branch, canonical_head = self.canonical_tip()
        except ProjectControlError:
            canonical_branch, canonical_head = context["branch"], context["head"]
            if role == "PROJECT_TEMPLATE":
                # The template declares no canonical branch (a new copy does); its own baseline is main.
                main_head = self.run_git(["rev-parse", "--verify", "refs/heads/main"])
                if main_head.returncode == 0 and SHA40.fullmatch(main_head.stdout.strip()):
                    canonical_branch, canonical_head = "main", main_head.stdout.strip()
        remotes = self.remote_heads(canonical_branch) if canonical_branch not in {"", "DETACHED_OR_UNBORN"} else {}
        behind = sorted(name for name, head in remotes.items() if head != canonical_head)
        canonical_tag = next((tag for tag in reversed(tags) if tag["commit"] == canonical_head), None)
        generated_at = now_iso()
        verification: dict[str, Any] = {
            "head": context["head"], "branch": context["branch"], "audit_status": audit_status,
            "canonical_branch": canonical_branch, "canonical_head": canonical_head,
            "skeleton_version": core.get("skeleton_version"), "core_aligned": not core.get("core_drift"),
            "hooks": self.commit_gate_state(), "remotes": remotes,
            "version_tag": current_tag["tag"] if current_tag else None, "tests_count": None,
            "sources_digest": digest, "sources": sources,
        }
        tests_file = self.root / "tests/test_template.py"
        if tests_file.is_file():
            verification["tests_count"] = len(re.findall(r"(?m)^\s*def test_", tests_file.read_text(encoding="utf-8", errors="replace")))
        tongue = self.speech()
        regeneration = regeneration_label(str(settings.get("regeneration")), tongue)
        reference = canonical_tag["tag"] if canonical_tag else speak(tongue, "backups.up_to_date")
        self._backups_ok = bool(remotes) and not behind
        self._backups_none = not remotes
        backups = (speak(tongue, "backups.same", reference=reference) if self._backups_ok
                   else (speak(tongue, "backups.behind", remotes=", ".join(behind)) if behind
                         else speak(tongue, "backups.none")))
        self._backups_sentence = (
            speak(tongue, "backups.same_sentence", reference=reference) if self._backups_ok
            else (speak(tongue, "backups.behind_sentence", remotes=", ".join(behind)) if behind
                  else speak(tongue, "backups.none_sentence"))
        )
        view: dict[str, Any] = {
            "schema_version": module.VIEW_SCHEMA_VERSION, "generated_at": generated_at, "role": role,
            "style": style, "style_forced": bool(style_override), "language": tongue, "zoom": settings.get("zoom", {}),
            "mirrors": settings.get("mirrors", []),
            "settings": {"regeneration_label": regeneration, "language_label": LANGUAGE_LABELS.get(tongue, tongue)},
            "verification": verification, "technical_notes": failures,
        }
        template_roadmap = self.load_template_roadmap()
        if template_roadmap is not None:
            self._template_view(view, template_roadmap, backups, module)
        else:
            self._project_view(view, backups, module)
        return view

    def _banner(self, view: dict[str, Any], version: str, backups: str) -> list[list[str]]:
        verification = view["verification"]
        audit_ok = verification["audit_status"] == "PASS"
        tests = verification.get("tests_count")
        # The controller runs its checks, never the test suite: saying "all passed" from an audit
        # that never executed a test is an assertion nobody verified.
        tongue = self.speech()
        checks = speak(tongue, "checks.pass" if audit_ok else "checks.fail") + (
            speak(tongue, "checks.tests", tests=tests) if tests else "")
        # The state is already known: testing a translated prefix made an up-to-date backup
        # read as an alert in English.
        backups_ok = self._backups_ok
        return [
            [speak(tongue, "banner.checked_on"), self.roadmap_view_module().written_date(view["generated_at"], tongue), "v"],
            [speak(tongue, "banner.how"), speak(tongue, "banner.how_detail"), "v"],
            [speak(tongue, "banner.version"), version, "v"],
            [speak(tongue, "banner.backups"), backups, "ok" if backups_ok else "ko"],
            [speak(tongue, "banner.checks"), checks, "ok" if audit_ok else "ko"],
            [speak(tongue, "banner.refresh"), view["settings"]["regeneration_label"] + speak(tongue, "banner.on_demand"), "v"],
        ]

    def _template_view(self, view: dict[str, Any], roadmap: dict[str, Any], backups: str, module: Any) -> None:
        template = roadmap["template"]
        verification = view["verification"]
        # The promoted versions are the repository's tags, never the file's claim: a version
        # listed in the roadmap but not yet tagged is the next one, until the Project Owner tags it.
        promoted = {tag["version"] for tag in self.version_tags()}
        current = max(promoted, key=version_tuple) if promoted else template["current_version"]
        listed = [item for item in roadmap["versions"] if version_tuple(item["version"]) <= version_tuple(current)]
        pending = [item for item in roadmap["versions"] if version_tuple(item["version"]) > version_tuple(current)]
        if not any(item["version"] == current for item in listed):
            listed.append({"version": current, "date": next((tag["date"] for tag in self.version_tags() if tag["version"] == current), ""), "label": speak(self.speech(), "tpl.promoted"), "decisions": []})
            listed.sort(key=lambda item: version_tuple(item["version"]))
        tag = verification.get("version_tag")
        on_current = bool(tag) and tag.lstrip("v") == current
        tongue = self.speech()
        version_text = speak(tongue, "tpl.version_text", current=current) + (
            "" if on_current else (speak(tongue, "tpl.off_version") if tag else speak(tongue, "tpl.untagged")))
        next_version = roadmap.get("next_version")
        if pending:
            first = min(pending, key=lambda item: version_tuple(item["version"]))
            next_version = {"version": first["version"], "date": speak(tongue, "tpl.upcoming"), "label": first["label"]}
        view.update({
            "title": f"ROADMAP {template['name'].upper()}", "eyebrow": speak(tongue, "tpl.eyebrow"),
            "lede": speak(tongue, "tpl.lede"),
            "versions": [{"version": item["version"], "date": item["date"], "label": item["label"], "current": item["version"] == current} for item in listed],
            "next_version": next_version, "chantiers": roadmap["chantiers"], "ideas": roadmap["ideas"],
            "waiting_for_owner": roadmap["waiting_for_owner"], "next_steps": roadmap["next_steps"], "later": roadmap["later"],
            "past": roadmap["past"], "work_items": [],
        })
        decisions = sorted({decision for item in roadmap["versions"] for decision in item["decisions"]} | {decision for item in roadmap["chantiers"] for decision in item["decisions"]})
        open_branches = [line.strip().lstrip("* ") for line in self.git_lines(["branch", "--no-merged", verification.get("canonical_branch") or "HEAD"])]
        now: list[dict[str, Any]] = [
            {"text": speak(tongue, "tpl.now_version", current=current) + (
                speak(tongue, "tpl.now_on_it") if on_current
                else (speak(tongue, "tpl.now_preparing", next=next_version["version"]) if next_version and pending
                      else speak(tongue, "tpl.now_off_it"))),
             "tone": "good" if on_current else "warn", "source": speak(tongue, "source.tags"), "technical": f"HEAD {verification['head']}"},
            {"text": self._backups_sentence, "tone": "good" if self._backups_ok else "warn", "source": speak(tongue, "source.remotes")},
            {"text": speak(tongue, "checks.sentence_pass" if verification["audit_status"] == "PASS" else "checks.sentence_fail"),
             "tone": "good" if verification["audit_status"] == "PASS" else "warn", "source": speak(tongue, "source.audit")},
            {"text": (speak(tongue, "tpl.no_branch") if not open_branches
                      else speak(tongue, "tpl.open_branches", branches=", ".join(open_branches))),
             "tone": "good" if not open_branches else "warn", "source": speak(tongue, "source.branches")},
            *roadmap.get("now", []),
        ]
        view["now"] = now
        view["stats"] = [
            {"label": speak(tongue, "stat.version"), "value": current,
             "sub": speak(tongue, "stat.version_tagged") if on_current
             else (speak(tongue, "stat.version_last_tag") if promoted else speak(tongue, "stat.version_from_file"))},
            {"label": speak(tongue, "stat.decisions"), "value": str(len(decisions)), "sub": speak(tongue, "stat.decisions_sub")},
            {"label": speak(tongue, "stat.checks"),
             "value": speak(tongue, "stat.checks_pass" if verification["audit_status"] == "PASS" else "stat.checks_fail"),
             "sub": speak(tongue, "stat.checks_sub", tests=verification.get("tests_count") or "—")},
            {"label": speak(tongue, "stat.open"), "value": str(len(open_branches)),
             "sub": speak(tongue, "stat.open_sub") if open_branches else speak(tongue, "stat.open_none")},
        ]
        verification["banner"] = self._banner(view, version_text, backups)

    def _project_view(self, view: dict[str, Any], backups: str, module: Any) -> None:
        verification = view["verification"]
        project = self.project_state()
        name = str(project.get("project_name", "UNKNOWN"))
        mode = self.operating_mode()
        style = self.reporting_style()
        try:
            items = self.records("project_control/work-items")
        except ProjectControlError:
            items = []
        try:
            ideas = list(self.load_ideas().get("ideas", []))
        except (OSError, json.JSONDecodeError, ProjectControlError):
            ideas = []
        try:
            roadmap_rows = {row["work_item_id"]: row for row in load_json(self.roadmap_json).get("work_items", []) if isinstance(row, dict)}
        except (OSError, json.JSONDecodeError):
            roadmap_rows = {}
        decisions = self.human_decision_entries()
        status_views = {}
        if verification["audit_status"] == "PASS" and mode == "NORMAL_MODE":
            try:
                status_views = {entry["work_item_id"]: entry for entry in self.status_payload().get("work_items", [])}
            except (ProjectControlError, OSError, ValueError, KeyError, TypeError):
                status_views = {}
        work_items = []
        for item in items:
            row = roadmap_rows.get(item["work_item_id"], {})
            entry = {
                "work_item_id": item["work_item_id"], "display_reference": item.get("display_reference"),
                "title": item.get("title"), "objective": item.get("objective"), "status": item.get("status"),
                "integration_state": row.get("integration_state"), "human_gate": row.get("human_gate") or (item.get("human_decision_refs") or [None])[0],
                "dependencies": item.get("dependencies", []), "branch": item.get("branch"),
                "missing_gates": status_views.get(item["work_item_id"], {}).get("missing_gates", []),
                "authorities": status_views.get(item["work_item_id"], {}).get("authorities"),
                "close_head": item.get("close_head"),
            }
            if item.get("status") == "BLOCKED" and item.get("block_records"):
                block = item["block_records"][-1]
                entry["block"] = {"reason_code": block.get("reason_code"), "resume_condition": block.get("resume_condition"), "human_decision_id": block.get("human_decision_id")}
            work_items.append(entry)
        work_items.sort(key=lambda entry: entry["work_item_id"])
        by_status = lambda *statuses: [entry for entry in work_items if entry["status"] in statuses]  # noqa: E731
        core = self.core_status()
        skeleton = core.get("skeleton_version")
        drift = core.get("core_drift") or {}
        tongue = self.speech()
        language = self.language()
        now: list[dict[str, Any]] = []
        if mode == "BOOTSTRAP_MODE":
            now.append({"text": speak(tongue, "prj.not_initialized"), "tone": "warn", "source": "FIRST_START.md"})
        now.append({"text": speak(tongue, "checks.sentence_pass" if verification["audit_status"] == "PASS" else "checks.sentence_fail"),
                    "tone": "good" if verification["audit_status"] == "PASS" else "warn",
                    "source": speak(tongue, "source.audit"), "technical": f"HEAD {verification['head']}"})
        now.append({"text": speak(tongue, "prj.skeleton", skeleton=skeleton) + (
                        speak(tongue, "prj.skeleton_aligned") if not drift
                        else speak(tongue, "prj.skeleton_drift", count=len(drift))),
                    "tone": "good" if not drift else "warn", "source": speak(tongue, "source.core_manifest")})
        now.append({"text": self._backups_sentence,
                    "tone": "good" if self._backups_ok else ("neutral" if self._backups_none else "warn"),
                    "source": speak(tongue, "source.project_remotes")})
        for entry in by_status("IN_PROGRESS"):
            missing = ", ".join(entry["missing_gates"]) or speak(tongue, "status.none_declared")
            read = entry.get("authorities") or ""
            authorities = speak(tongue, f"authorities.line_{read.lower()}") if f"authorities.line_{read.lower()}" in SPEECH else ""
            now.append({"text": speak(tongue, "prj.in_progress", title=entry["title"], reference=entry["display_reference"], missing=missing)
                        + (f" {authorities[:1].upper()}{authorities[1:]}." if authorities else ""),
                        "tone": "neutral", "source": speak(tongue, "source.record", id=entry["work_item_id"]),
                        "technical": speak(tongue, "source.branch", branch=entry["branch"])})
        for entry in by_status("BLOCKED"):
            now.append({"text": speak(tongue, "prj.blocked", title=entry["title"], reference=entry["display_reference"],
                                      condition=entry.get("block", {}).get("resume_condition") or speak(tongue, "prj.unknown_condition")),
                        "tone": "warn", "source": speak(tongue, "source.record", id=entry["work_item_id"])})
        if not by_status("IN_PROGRESS", "BLOCKED") and mode == "NORMAL_MODE":
            now.append({"text": speak(tongue, "prj.at_rest") + speak(tongue, "prj.at_rest_authorized" if by_status("AUTHORIZED") else "prj.at_rest_plain"),
                        "tone": "neutral", "source": "roadmap"})
        style_word = {"PLAIN": "prj.style_plain", "TECHNICAL": "prj.style_technical"}.get(style, "prj.style_unset")
        now.append({"text": speak(tongue, "prj.style", style=speak(tongue, style_word)),
                    "tone": "neutral" if style in REPORTING_STYLES else "warn", "source": "project-state"})
        waiting: list[dict[str, Any]] = []
        if style not in REPORTING_STYLES:
            waiting.append({"title": speak(tongue, "wait.style"), "detail": speak(tongue, "wait.style_detail"), "source": speak(tongue, "source.interview")})
        if language not in LANGUAGES:
            waiting.append({"title": speak(tongue, "wait.language"), "detail": speak(tongue, "wait.language_detail"), "source": speak(tongue, "source.interview")})
        if mode == "BOOTSTRAP_MODE":
            waiting.append({"title": speak(tongue, "wait.init"), "detail": speak(tongue, "wait.init_detail"), "source": "FIRST_START.md"})
        if verification["audit_status"] != "PASS":
            waiting.append({"title": speak(tongue, "wait.audit"), "detail": speak(tongue, "wait.audit_detail"), "source": speak(tongue, "source.audit")})
        for entry in by_status("BLOCKED"):
            waiting.append({"title": speak(tongue, "wait.resume", title=entry["title"]),
                            "detail": speak(tongue, "wait.resume_detail",
                                            condition=entry.get("block", {}).get("resume_condition") or speak(tongue, "wait.unknown")),
                            "source": speak(tongue, "source.record", id=entry["work_item_id"])})
        if drift:
            waiting.append({"title": speak(tongue, "wait.drift"), "detail": ", ".join(sorted(drift)) + ".", "source": speak(tongue, "source.core_manifest_short")})
        for idea in ideas:
            if idea["state"] == "TO_CLARIFY":
                waiting.append({"title": speak(tongue, "wait.idea_clarify", quote=idea["quote"]), "detail": idea.get("note") or "", "source": idea["source"]})
            elif idea["state"] == "TO_SET":
                waiting.append({"title": speak(tongue, "wait.idea_settle", quote=idea["quote"]), "detail": idea.get("note") or "", "source": idea["source"]})
            elif idea["state"] == "EVOKED":
                waiting.append({"title": speak(tongue, "wait.idea_evoked", quote=idea["quote"]),
                                "detail": speak(tongue, "wait.idea_evoked_detail"), "source": idea["source"]})
        next_steps: list[dict[str, Any]] = []
        for entry in by_status("IN_PROGRESS"):
            next_steps.append({"title": speak(tongue, "next.finish", title=entry["title"]),
                               "detail": speak(tongue, "next.finish_detail",
                                               missing=", ".join(entry["missing_gates"]) or speak(tongue, "status.none_declared")),
                               "source": speak(tongue, "source.record", id=entry["work_item_id"])})
        for entry in by_status("AUTHORIZED"):
            deps = ", ".join(entry["dependencies"]) if entry["dependencies"] else speak(tongue, "next.no_dependency")
            next_steps.append({"title": speak(tongue, "next.start", title=entry["title"], reference=entry["display_reference"]),
                               "detail": speak(tongue, "next.start_detail", deps=deps, decision=entry["human_gate"]), "source": "roadmap"})
        for idea in ideas:
            if idea["state"] in {"SCOPED", "PLANNED", "IN_PROGRESS"}:
                next_steps.append({"title": speak(tongue, "idea.title", quote=idea["quote"]),
                                   "detail": (idea.get("note") or "") + (f" → {idea['target']}" if idea.get("target") else ""), "source": idea["source"]})
        later: list[dict[str, Any]] = [
            {"title": speak(tongue, "later.proposed", title=entry["title"], reference=entry["display_reference"]),
             "detail": entry.get("objective") or "", "source": "roadmap"} for entry in by_status("PROPOSED")]
        later.extend({"title": speak(tongue, "idea.title", quote=idea["quote"]), "detail": idea.get("note") or "", "source": idea["source"]}
                     for idea in ideas if idea["state"] == "LATER")
        past: list[dict[str, Any]] = []
        for entry in by_status("DONE", "REJECTED", "SUPERSEDED"):
            label = module.work_item_label(entry["status"], tongue)
            past.append({"date": self.commit_date(entry.get("close_head") or ""), "title": f"{entry['title']} ({entry['display_reference']}) — {label.lower()}",
                         "version": entry["work_item_id"],
                         "details": [entry.get("objective") or "", speak(tongue, "past.decision", decision=entry["human_gate"])],
                         "sources": speak(tongue, "source.record", id=entry["work_item_id"])})
        if decisions:
            past.append({"date": max((entry["date"] for entry in decisions if re.fullmatch(r"\d{4}-\d{2}-\d{2}", entry["date"])), default=""),
                         "title": speak(tongue, "past.decisions_title", count=len(decisions)), "version": None,
                         "details": [f"{entry['id']} — {entry['date'] or speak(tongue, 'past.unknown_date')} — {entry['decision']}" for entry in decisions],
                         "sources": "HUMAN_DECISIONS.md"})
        past.sort(key=lambda entry: (entry["date"] == "", entry["date"]))
        tags = self.version_tags()
        head_tag = verification.get("version_tag")
        view.update({
            "title": f"ROADMAP {name.upper()}", "eyebrow": speak(tongue, "prj.eyebrow"),
            "lede": speak(tongue, "prj.lede"),
            "versions": [{"version": tag["version"], "date": tag["date"], "label": "", "current": tag["tag"] == head_tag} for tag in tags] if tags else [],
            "next_version": None, "chantiers": [], "ideas": ideas, "work_items": work_items,
            "now": now, "waiting_for_owner": waiting, "next_steps": next_steps, "later": later, "past": past,
        })
        open_count = len(by_status("AUTHORIZED", "IN_PROGRESS", "BLOCKED"))
        view["stats"] = [
            {"label": speak(tongue, "stat.done"), "value": str(len(by_status("DONE"))), "sub": speak(tongue, "stat.done_sub")},
            {"label": speak(tongue, "stat.open_items"), "value": str(open_count),
             "sub": speak(tongue, "stat.open_items_sub", active=len(by_status("IN_PROGRESS")),
                          blocked=len(by_status("BLOCKED")), authorized=len(by_status("AUTHORIZED")))},
            {"label": speak(tongue, "stat.decisions"), "value": str(len(decisions)), "sub": speak(tongue, "stat.decisions_project_sub")},
            {"label": speak(tongue, "stat.ideas"),
             "value": str(sum(idea["state"] not in {"REALIZED", "DISCARDED"} for idea in ideas)),
             "sub": speak(tongue, "stat.ideas_sub", total=len(ideas))},
        ]
        version_text = speak(tongue, "prj.version_text", skeleton=skeleton) + (
            speak(tongue, "prj.version_project", tag=head_tag) if head_tag else "")
        verification["banner"] = self._banner(view, version_text, backups)

    def write_roadmap_view(
        self, view: dict[str, Any], html_path: str | None, markdown_path: str | None, governed: bool = False,
    ) -> tuple[list[str], list[str]]:
        """Write the page (never tracked) and the Markdown view.

        The Markdown view at its default path is an administrative record like the roadmap:
        in NORMAL_MODE it is rewritten only when its sources changed, from the canonical
        checkout on a clean worktree, and committed by Project Control itself. Elsewhere
        (Bootstrap Mode, the template, an explicit --markdown path) it is only written.
        Returns (written paths, notes).
        """
        module = self.roadmap_view_module()
        written: list[str] = []
        notes: list[str] = []

        def relative_of(target: str) -> str:
            relative = safe_relative_path(target)
            if relative is None:
                raise ProjectControlError(f"unsafe output path: {target}")
            return relative

        # Everything that can refuse is decided BEFORE the first byte is written: a command that
        # ends on "read only, nothing written" must not have rewritten the page on its way there.
        html_relative = relative_of(html_path) if html_path else None
        markdown_relative = relative_of(markdown_path) if markdown_path else None
        governed_commit = bool(markdown_relative) and governed and self.operating_mode() == "NORMAL_MODE"
        canonical_branch: str | None = None
        if governed_commit and not view.get("style_forced") and self.roadmap_view_state() != "CURRENT":
            self.validate_clean_administrative_baseline()
            canonical_branch, _ = self.require_canonical_checkout("roadmap-view --write")
            self.require_clean_worktree("roadmap-view --write")

        if html_relative:
            path = self.root / html_relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(module.render_html(view), encoding="utf-8")
            written.append(html_relative)
        if markdown_relative is None:
            return written, notes
        relative = markdown_relative
        content = module.render_markdown(view)
        if not governed_commit:
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            written.append(relative)
            return written, notes
        if view.get("style_forced"):
            notes.append(f"{relative} not written: the committed view follows the project's reporting style, not --style")
            return written, notes
        if self.roadmap_view_state() == "CURRENT":
            notes.append(f"{relative} unchanged: sources digest already current")
            return written, notes
        assert canonical_branch is not None
        transaction = FileTransaction(self.root)
        committed: tuple[str, str] | None = None
        try:
            transaction.write_text(relative, content)
            committed = self.commit_records(transaction, "chore(project-control): roadmap view")
            transaction.commit()
        except BaseException as exc:
            if committed is not None:
                rollback_errors = self.uncommit_records(transaction, canonical_branch, *committed)
                if rollback_errors:
                    raise ProjectControlError(f"roadmap view failed: {exc}; ROLLBACK FAILED: {'; '.join(rollback_errors)}") from exc
            else:
                transaction.rollback()
            raise
        written.append(relative)
        notes.append(f"{relative} committed on {canonical_branch} ({committed[1][:12]})")
        return written, notes

    def registry_errors(self) -> list[str]:
        try:
            text = self.worktree_registry.read_text(encoding="utf-8")
            records = {
                item.get("work_item_id"): item
                for item in self.records("project_control/work-items")
            }
        except (OSError, json.JSONDecodeError, ProjectControlError) as exc:
            return [str(exc)]
        entries: dict[str, dict[str, str]] = {}
        errors: list[str] = []
        for match in REGISTRY_ENTRY_PATTERN.finditer(text):
            work_item_id = match.group(1)
            if work_item_id in entries:
                errors.append(f"duplicate registry entry: {work_item_id}")
                continue
            fields: dict[str, str] = {}
            for line in match.group(2).splitlines():
                if ": " in line:
                    key, value = line.split(": ", 1)
                    fields[key] = value
            entries[work_item_id] = fields
        expected_status = {
            "AUTHORIZED": "DECLARED",
            "IN_PROGRESS": "ACTIVE",
            "IMPLEMENTED": "ACTIVE",
            "INTEGRATED": "ACTIVE",
            "DEPLOYED": "ACTIVE",
            "RUNTIME_PROVEN": "ACTIVE",
            "BLOCKED": "BLOCKED",
            "DONE": "CLOSED",
            "REJECTED": "CLOSED",
            "SUPERSEDED": "CLOSED",
        }
        for work_item_id, item in records.items():
            status = expected_status.get(item.get("status"))
            if status is None:
                continue
            entry = entries.get(str(work_item_id))
            if entry is None:
                errors.append(
                    f"missing registry entry: {work_item_id}: expected the block "
                    f"`<!-- PROJECT_CONTROL:{work_item_id} START -->` … "
                    f"`<!-- PROJECT_CONTROL:{work_item_id} END -->` in "
                    "docs/governance/WORKTREE_REGISTRY.md (see its Modèle section)"
                )
                continue
            expected = {
                "WORK_ITEM_ID": str(work_item_id),
                "DISPLAY_REFERENCE": str(item.get("display_reference")),
                "BASE_HEAD": str(item.get("base_head")),
                "START_HEAD": str(item.get("start_head")),
                "AUTHORIZED_SCOPE": ", ".join(item.get("authorized_paths", [])),
                "BRANCH": str(item.get("branch")),
                "STATUS": status,
                "CLOSE_CONDITION": str(item.get("close_condition")),
            }
            for field, value in expected.items():
                if entry.get(field) != value:
                    errors.append(f"{work_item_id}: registry {field} differs")
        extra = set(entries) - set(records)
        if extra:
            errors.append(f"registry entries without Work Item: {sorted(extra)}")
        active = [work_item_id for work_item_id, fields in entries.items() if fields.get("STATUS") == "ACTIVE"]
        if len(active) > 1:
            errors.append(f"multiple active registry entries: {active}")
        return errors

    def project_control_errors(self) -> list[str]:
        errors: list[str] = []
        try:
            project = self.project_state()
            work_items = self.records("project_control/work-items")
            conversations = self.records("project_control/conversations")
            agent_runs = self.records("project_control/agent-runs")
        except (OSError, json.JSONDecodeError, ProjectControlError) as exc:
            return [str(exc)]
        errors.extend(validate_project_state(project, self.first_start_status()))
        if errors:
            return errors
        key = project.get("project_key")
        canonical = self.canonical_branch() if self.operating_mode() == "NORMAL_MODE" else None
        try:
            self.legacy_records()
            legacy_usable = True
        except (ProjectControlError, OSError, ValueError) as exc:
            # Reported once here; LEGACY_RECORDS_PRESENT carries the same failure.
            errors.append(f"DONE evidence not verified: {exc}")
            legacy_usable = False
        for item in work_items:
            item_errors = validate_work_item(item, key, canonical)
            errors.extend(item_errors)
            if canonical is not None and item.get("branch") == canonical:
                errors.append(f"Work Item {item.get('work_item_id')}: branch must differ from canonical branch {canonical}")
            if not item_errors and legacy_usable:
                errors.extend(self.done_evidence_errors(item))
        for item in conversations:
            errors.extend(validate_conversation_reference(item))
        for item in agent_runs:
            errors.extend(validate_agent_run(item))
        if errors:
            return errors
        errors.extend(self.agent_run_authority_errors(agent_runs))
        try:
            decisions = self.human_decisions.read_text(encoding="utf-8")
        except OSError as exc:
            return errors + [str(exc)]
        try:
            frozen_decisions = self.frozen_decision_refs()
        except ProjectControlError as exc:
            return errors + [str(exc)]
        legacy_done_ids: set[str] = set()
        for item in work_items:
            try:
                if self.legacy_done(item):
                    legacy_done_ids.add(str(item.get("work_item_id")))
            except (ProjectControlError, OSError, ValueError):
                # An unreadable baseline grants no exemption; LEGACY_RECORDS_PRESENT reports it.
                pass
        errors.extend(validate_record_links(work_items, conversations, agent_runs, decisions, frozen_decisions, legacy_done_ids))
        summaries = {item.get("work_item_id"): item for item in load_json(self.roadmap_json).get("work_items", [])}
        records = {item.get("work_item_id"): item for item in work_items}
        if set(summaries) != set(records):
            errors.append(f"roadmap/record Work Item mismatch: roadmap={sorted(summaries)} records={sorted(records)}")
        for work_id in set(summaries) & set(records):
            for key_name in ("display_reference", "title", "status"):
                if summaries[work_id].get(key_name) != records[work_id].get(key_name):
                    errors.append(f"{work_id}: {key_name} differs between roadmap and record")
            human_refs = records[work_id].get("human_decision_refs", [])
            expected_gate = human_refs[0] if human_refs else None
            if summaries[work_id].get("human_gate") != expected_gate:
                errors.append(f"{work_id}: human_gate differs between roadmap and record")
            if summaries[work_id].get("dependencies") != records[work_id].get("dependencies"):
                errors.append(f"{work_id}: dependencies differ between roadmap and record")
        return errors

    def generality_errors(self) -> list[str]:
        errors: list[str] = []
        for root_name in ACTIVE_CORE_ROOTS:
            root = self.root / root_name
            candidates = [root] if root.is_file() else sorted(path for path in root.rglob("*") if path.is_file())
            for path in candidates:
                if ".git" in path.parts or path.suffix not in {".md", ".json", ".py", ""}:
                    continue
                text = path.read_text(encoding="utf-8", errors="replace")
                for label, pattern in FORBIDDEN_CORE_PATTERNS.items():
                    if pattern.search(text):
                        errors.append(f"{label}: {path.relative_to(self.root)}")
        return errors

    def business_files(self) -> list[str]:
        files: list[str] = []
        for directory in ("applications", "modules", "shared"):
            for path in sorted((self.root / directory).rglob("*")):
                if path.is_file() and path.name != "README.md":
                    files.append(str(path.relative_to(self.root)))
        return files

    def integration_merge_errors(self) -> list[str] | None:
        """None when no merge is in progress; otherwise why this merge is not a plain integration.

        An integration merge carries the work its branch already produced under its own gate.
        What it must never carry is a change smuggled in on the way: a path the merged branch
        never touched, appearing in the merge commit and passing under the name of integration.
        So every path the merge brings into the canonical tree must be a path the branch itself
        changed since the merge base."""
        if not self.merge_in_progress():
            return None
        merge_head = self.run_git(["rev-parse", "MERGE_HEAD"]).stdout.strip()
        base = self.run_git(["merge-base", "HEAD", merge_head])
        if base.returncode != 0 or not SHA40.fullmatch(base.stdout.strip()):
            return ["merge in progress but its merge base cannot be resolved"]
        base_sha = base.stdout.strip()
        # A rename on the branch is one change with two names: the file it took and the file it
        # left. Both belong to the branch, and a change the canonical branch made to the old name
        # since the base is a change to the renamed file — Git merges it into the new name, and
        # that result is a resolution, not an edit (fifth independent control, F-03).
        renamed_from: dict[str, str] = {}
        from_branch: set[str] = set()
        entries = self.git_paths(["diff", "--name-status", "-M", base_sha, merge_head])
        index = 0
        while index < len(entries):
            status = entries[index]
            if status[:1] in {"R", "C"} and index + 2 < len(entries):
                old_name, new_name = entries[index + 1], entries[index + 2]
                from_branch.update({old_name, new_name})
                renamed_from[new_name] = old_name
                index += 3
            elif index + 1 < len(entries):
                from_branch.add(entries[index + 1])
                index += 2
            else:
                break
        # The index, not the working tree: a passenger staged and then deleted from the disk is
        # gone from `diff HEAD` — which compares HEAD to the disk — while the merge commit still
        # carries it. What the commit writes is the index, so the index is what is read.
        incoming = set(self.git_paths(["diff", "--cached", "--name-only", "HEAD"]))
        smuggled = sorted(path for path in incoming - from_branch if path)
        if smuggled:
            return [
                "an integration merge carries only what its branch changed; "
                f"these paths come from nowhere else: {smuggled}"
            ]
        # And what it writes for a path must be what the branch produced for it. The merge
        # result can be edited before the commit, and a path the branch legitimately touched
        # used to carry any content at all under the name of integration — the adoption
        # baseline removed on the way, a frozen history reopened behind it (fourth independent
        # control, F12-01). Where only the branch changed the path since the base, the index
        # must hold the branch's blob; where both sides changed it, the result is a resolution,
        # and the audit judges it like any other state.
        from_canonical = set(self.git_paths(["diff", "--name-only", base_sha, "HEAD"]))
        deleted = set(self.git_paths(["diff", "--cached", "--name-only", "--diff-filter=D", "HEAD"]))
        edited = []
        unreadable = []
        for path in sorted(incoming & from_branch):
            if not path or path in from_canonical or renamed_from.get(path) in from_canonical:
                continue
            staged_blob = self.run_git(["rev-parse", "--verify", "--quiet", f":{path}"]).stdout.strip()
            branch_blob = self.run_git(["rev-parse", "--verify", "--quiet", f"{merge_head}:{path}"]).stdout.strip()
            if not staged_blob and not branch_blob and path not in deleted:
                # Neither side can be read for a path the index says it changed: that is not
                # equality, that is a lookup that failed. It is refused, not waved through.
                unreadable.append(path)
            elif staged_blob != branch_blob:
                edited.append(path)
        if unreadable:
            return [
                "an integration merge is judged on what it writes, and what it writes for these "
                f"paths could not be read: {unreadable}"
            ]
        if edited:
            return [
                "an integration merge carries what its branch produced, content included; "
                f"the merge result differs from the branch for: {edited}"
            ]
        return []

    def business_change_authorization_errors(self) -> list[str]:
        # A merge in progress is an integration, not development: it is judged on what it
        # integrates, not on the branch it lands on.
        merge_errors = self.integration_merge_errors()
        if merge_errors is not None:
            return merge_errors
        changed_business_paths = []
        for raw in self.changed_paths():
            path = safe_relative_path(raw)
            if path is None:
                continue
            candidate = PurePosixPath(path)
            if candidate.parts and candidate.parts[0] in BUSINESS_ROOTS and candidate.name != "README.md":
                changed_business_paths.append(path)
        if not changed_business_paths:
            return []
        if self.operating_mode() != "NORMAL_MODE":
            return [f"business changes require NORMAL_MODE: {sorted(changed_business_paths)}"]
        try:
            active_items = [
                item
                for item in self.records("project_control/work-items")
                if item.get("status") == "IN_PROGRESS"
            ]
        except (OSError, json.JSONDecodeError) as exc:
            return [f"cannot resolve active Work Item: {exc}"]
        if len(active_items) != 1:
            return [
                "current business changes require exactly one IN_PROGRESS Work Item; "
                f"found {[item.get('work_item_id') for item in active_items]}"
            ]
        active_item = active_items[0]
        current_branch = self.repository_context()["branch"]
        declared_branch = active_item.get("branch")
        errors: list[str] = []
        if current_branch != declared_branch:
            errors.append(
                f"current business changes require declared branch {declared_branch}; "
                f"current branch is {current_branch}"
            )
        errors.extend(
            normal_path_errors(changed_business_paths, active_item.get("authorized_paths", []))
        )
        return errors

    def traceability_errors(self) -> list[str]:
        path = self.root / "scripts/check_git_traceability.py"
        spec = importlib.util.spec_from_file_location("governed_git_traceability", path)
        if spec is None or spec.loader is None:
            return ["cannot load check_git_traceability.py"]
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        try:
            spec.loader.exec_module(module)
            try:
                payload = module.audit_payload(self.root)
            except TypeError:
                payload = module.audit_payload()
        except Exception as exc:
            return [f"traceability checker error: {exc}"]
        return list(payload.get("errors", []))

    def operating_mode(self) -> str:
        status = self.first_start_status()
        return {"NOT_STARTED": "BOOTSTRAP_MODE", "COMPLETE": "NORMAL_MODE"}.get(status, "INVALID")

    def initialization_state_errors(self) -> list[str]:
        status = self.first_start_status()
        if status not in {"NOT_STARTED", "COMPLETE"}:
            return [f"invalid FIRST_START status: {status}"]
        try:
            state = self.project_state()
        except (OSError, json.JSONDecodeError, ProjectControlError) as exc:
            return [str(exc)]
        errors = validate_project_state(state, status)
        if status == "COMPLETE":
            errors.extend(self.closeout_readiness(require_complete=True))
        return errors

    def closeout_readiness(self, require_complete: bool = False) -> list[str]:
        errors: list[str] = []
        try:
            self.canonical_branch()
        except ProjectControlError as exc:
            errors.append(str(exc))
        try:
            state = self.project_state()
            decisions_text = self.human_decisions.read_text(encoding="utf-8")
            charter = (self.root / "docs/governance/PROJECT_CHARTER.md").read_text(encoding="utf-8")
            architecture = (self.root / "docs/architecture/PROJECT_ARCHITECTURE_MAP.md").read_text(encoding="utf-8")
            initial_architecture = (self.root / "docs/architecture/INITIAL_ARCHITECTURE.md").read_text(encoding="utf-8")
            adr = (self.root / "docs/adr/ADR-0001-initial-architecture-boundaries.md").read_text(encoding="utf-8")
            work_items = self.records("project_control/work-items")
            conversations = self.records("project_control/conversations")
        except (OSError, json.JSONDecodeError, ProjectControlError) as exc:
            return [str(exc)]
        initialization = state.get("initialization", {})
        decision_ref = initialization.get("completion_human_decision_ref")
        decisions = set(re.findall(r"(?m)^## (HD-[0-9]{3,})\s*$", decisions_text))
        if declared_status(charter) != "VALIDATED" or "TODO(PROJECT_OWNER)" in charter:
            errors.append("closeout requires a validated Project Charter: its Status line must read exactly Status: `VALIDATED`, with no owner TODO left")
        if declared_status(architecture) != "VALIDATED":
            errors.append("closeout requires a validated Project Architecture Map: its Status line must read exactly Status: `VALIDATED`")
        if "ANTI_OCTOPUS_REVIEW: APPROVED_BY_PROJECT_OWNER" not in architecture or re.search(r"\| UNKNOWN \|", architecture):
            errors.append("closeout requires an approved Anti-Octopus Review with no UNKNOWN row")
        if declared_status(initial_architecture) != "VALIDATED":
            errors.append("closeout requires validated initial architecture: its Status line must read exactly Status: `VALIDATED`")
        if declared_status(adr) not in {"ACCEPTED", "NOT_APPLICABLE — PROJECT_OWNER_VALIDATED"}:
            errors.append("closeout requires the initial ADR accepted or explicitly not applicable: its Status line must read exactly Status: `ACCEPTED` or Status: `NOT_APPLICABLE — PROJECT_OWNER_VALIDATED`")
        if not HUMAN_DECISION_ID.fullmatch(str(decision_ref or "")) or decision_ref not in decisions:
            errors.append("closeout requires a recorded completion Human Decision")
        if state.get("reporting_style") not in REPORTING_STYLES:
            errors.append("closeout requires the Project Owner's reporting_style (TECHNICAL or PLAIN) in project-state")
        if state.get("language") not in LANGUAGES:
            errors.append("closeout requires the Project Owner's language (FR or EN) in project-state")
        lifecycle_items = work_items if require_complete else [
            item for item in work_items if item.get("status") == "AUTHORIZED"
        ]
        if not lifecycle_items:
            errors.append(
                "completed initialization requires its historical first Work Item"
                if require_complete
                else "closeout requires a first authorized Work Item"
            )
        for item in lifecycle_items:
            if not item.get("human_decision_refs") or not item.get("conversation_refs"):
                errors.append(f"{item.get('work_item_id')}: authorization must link a Human Decision and Conversation")
        conversation_ids = {item.get("conversation_ref") for item in conversations}
        if lifecycle_items and not any(
            set(item.get("conversation_refs", [])) & conversation_ids for item in lifecycle_items
        ):
            errors.append("closeout requires a stored provider-agnostic Conversation reference")
        errors.extend(self.roadmap_errors())
        errors.extend(self.project_control_errors())
        if not require_complete and self.business_files():
            errors.append(f"business capability present during initialization: {self.business_files()}")
        if require_complete:
            if self.first_start_status() != "COMPLETE" or initialization.get("status") != "COMPLETE":
                errors.append("normal mode requires FIRST_START and project-state COMPLETE")
        elif self.first_start_status() != "NOT_STARTED" or initialization.get("status") != "NOT_STARTED":
            errors.append("bootstrap closeout preflight requires NOT_STARTED")
        return list(dict.fromkeys(errors))

    def bootstrap_findings(self, planned_paths: Iterable[str] = ()) -> list[Finding]:
        findings = self.common_findings(include_traceability=False)
        status = self.first_start_status()
        add(findings, "BOOTSTRAP_MODE", status == "NOT_STARTED", f"FIRST_START={status}; expected NOT_STARTED")
        current = self.changed_paths()
        errors = bootstrap_path_errors([*current, *planned_paths])
        add(findings, "BOOTSTRAP_CHANGE_SCOPE", not errors, "worktree clean or all current/planned paths are bootstrap-allowlisted" if not errors else "; ".join(errors))
        try:
            owner = self.project_state().get("project_owner")
        except (OSError, json.JSONDecodeError):
            owner = None
        add(findings, "PROJECT_OWNER_DECLARATION", isinstance(owner, str) and bool(owner), f"project_owner={owner}")
        deployments = self.record_files("project_control/deployments")
        add(findings, "NO_BOOTSTRAP_DEPLOYMENT", not deployments, "no deployment record in Bootstrap Mode" if not deployments else f"deployment records: {deployments}")
        return findings

    def audit_findings(self) -> list[Finding]:
        return self.common_findings(include_traceability=True)

    def staged_paths(self) -> list[str]:
        listed = self.run_git(["diff", "--cached", "--name-only", "-z", "--no-renames"], text=False)
        if listed.returncode != 0:
            return ["<git-diff-failed>"]
        return sorted({value.decode("utf-8", "surrogateescape") for value in listed.stdout.split(b"\0") if value})

    def indexed_symlinks(self) -> list[str]:
        """Symlinks recorded in the index (mode 120000), whatever the worktree shows.

        Reading only the worktree let a link be staged and then hidden behind an ordinary file:
        the commit carried the link the control had announced it forbids.
        """
        listed = self.run_git(["ls-files", "-s", "-z"], text=False)
        if listed.returncode != 0:
            return []
        paths: list[str] = []
        for record in listed.stdout.split(b"\0"):
            if not record:
                continue
            entry = record.decode("utf-8", errors="surrogateescape")
            head, _, path = entry.partition("\t")
            if head.split(" ", 1)[0] == "120000" and path:
                paths.append(path)
        return sorted(paths)

    def gate_reference(self) -> Path:
        """The versioned gate: the file that travels with the template and is the reference."""
        return self.root / HOOKS_PATH / "pre-commit"

    def git_path(self, *arguments: str) -> Path | None:
        """A path Git resolves for this checkout, made absolute against the worktree."""
        located = self.run_git(["rev-parse", *arguments])
        if located.returncode != 0:
            return None
        path = Path(located.stdout.strip())
        return path if path.is_absolute() else self.root / path

    def gate_installed_path(self) -> Path | None:
        """Where the gate is installed outside the worktree: the repository's COMMON hooks
        directory.

        Not `--git-dir`: in a linked worktree that answers the worktree's own directory, where
        Git never looks for hooks. Installing there wrote a gate nobody would run and reported
        success — a protection that lies about its own presence is worse than none."""
        common = self.git_path("--git-common-dir")
        return None if common is None else common / "hooks" / "pre-commit"

    def gate_executed_path(self) -> Path | None:
        """The file Git will really run before a commit, whatever the configuration says.

        `--git-path hooks/pre-commit` answers the executed file in every case: the common hooks
        directory from a linked worktree, and the configured directory when `core.hooksPath` is
        set. Asking Git itself is the only way to be sure the answer matches what happens."""
        return self.git_path("--git-path", "hooks/pre-commit")

    def commit_gate_state(self) -> str:
        """Where the gate runs from, in one word.

        `INSTALLED` — a copy outside the worktree, identical to the reference: no commit can
        carry it away, because it is not part of the tree a commit writes.
        `IN_TREE` — the historical mode (`core.hooksPath scripts/hooks`): it works, but the gate
        lives inside what it guards and a single commit can remove it.
        `MISMATCH` — an installed copy that differs from the reference, or is not executable.
        `NOT_INSTALLED` — Git runs no gate at all.
        """
        reference = self.gate_reference()
        installed = self.gate_installed_path()
        executed = self.gate_executed_path()
        configured = self.run_git(["config", "--get", "core.hooksPath"])
        hooks_path = configured.stdout.strip() if configured.returncode == 0 else ""
        if hooks_path in ("", ".git/hooks") and installed is not None and installed.is_file():
            if executed is None or executed.resolve() != installed.resolve():
                # The copy exists, but it is not the file Git will run. Announcing it installed
                # is the lie this check exists to refuse.
                return "NOT_INSTALLED"
            if not os.access(installed, os.X_OK):
                return "MISMATCH"
            try:
                same = reference.is_file() and installed.read_bytes() == reference.read_bytes()
            except OSError:
                return "MISMATCH"
            return "INSTALLED" if same else "MISMATCH"
        if hooks_path == HOOKS_PATH and reference.is_file() and os.access(reference, os.X_OK):
            return "IN_TREE"
        return "NOT_INSTALLED"

    def hooks_installed(self) -> bool:
        """True when Git really runs a gate, wherever that gate is installed from."""
        return self.commit_gate_state() in {"INSTALLED", "IN_TREE"}

    def install_commit_gate(self) -> list[Finding]:
        """Copy the versioned gate outside the worktree so that no commit can remove it.

        The versioned file stays the reference — it travels with the template and is updated by
        `template-upgrade`; the copy is what Git executes. Installing again after an upgrade is
        the way to keep them identical.
        """
        findings: list[Finding] = []
        reference = self.gate_reference()
        installed = self.gate_installed_path()
        if not reference.is_file():
            add(findings, "GATE_REFERENCE", False, f"missing gate reference: {HOOKS_PATH}/pre-commit")
            return findings
        if installed is None:
            add(findings, "GATE_REFERENCE", False, "cannot locate the Git directory")
            return findings
        installed.parent.mkdir(parents=True, exist_ok=True)
        installed.write_bytes(reference.read_bytes())
        installed.chmod(0o755)
        configured = self.run_git(["config", "--get", "core.hooksPath"])
        if configured.returncode == 0 and configured.stdout.strip() == HOOKS_PATH:
            self.run_git(["config", "--unset", "core.hooksPath"])
            add(findings, "HOOKS_PATH", True, "core.hooksPath cleared: Git now runs the copy outside the worktree")
        add(findings, "COMMIT_GATE", self.commit_gate_state() == "INSTALLED",
            f"gate installed at {installed}; reference {HOOKS_PATH}/pre-commit unchanged")
        return findings

    # --- Proof of reading (P3): the authorities routed for a Work Item, hashed; an agent ---
    # --- presents the digest at start/resume, the run records it, close revalidates it. ---

    def authority_manifest(self, scopes: Iterable[str]) -> dict[str, Any]:
        """The routed authorities for `base` plus the given scopes, with their current hashes."""
        routing = load_json(self.routing_json)
        paths = list(routing.get("base", []))
        routed = routing.get("scopes", {})
        wanted = sorted(set(scopes))
        for scope in wanted:
            documents = routed.get(scope, [])
            if isinstance(documents, list):
                paths.extend(str(value) for value in documents)
        entries: list[dict[str, str]] = []
        for path in sorted(set(paths)):
            relative = safe_relative_path(path)
            if relative in MANIFEST_EXCLUDED_PATHS:
                continue
            local = self.root / (relative or "")
            if relative is None or not local.is_file() or local.is_symlink():
                raise ProjectControlError(f"routed authority is missing: {path}")
            entries.append({"path": relative, "sha256": file_sha256(local)})
        return {
            "manifest_digest": manifest_digest(entries),
            "generated_at": now_iso(),
            "head": self.repository_context()["head"],
            "scopes": wanted,
            "entries": entries,
        }

    def work_item_manifest(self, item: dict[str, Any]) -> dict[str, Any]:
        return self.authority_manifest(scopes_for_paths(item.get("authorized_paths", [])))

    def latest_agent_run(self, item: dict[str, Any]) -> dict[str, Any] | None:
        refs = item.get("agent_run_refs", [])
        if not refs:
            return None
        path = self.root / f"project_control/agent-runs/{refs[-1]}.json"
        return load_json(path) if path.is_file() else None

    def authorities_read_errors(self, item: dict[str, Any]) -> dict[str, list[str]]:
        """PRESENT / COMPLETE / CURRENT for the latest Agent Run of a started Work Item."""
        errors: dict[str, list[str]] = {"PRESENT": [], "COMPLETE": [], "CURRENT": []}
        run = self.latest_agent_run(item)
        if run is None:
            errors["PRESENT"].append(f"{item.get('work_item_id')}: no Agent Run")
            return errors
        read = run.get("authorities_read")
        if not isinstance(read, dict) or not isinstance(read.get("entries"), list) or not read["entries"]:
            errors["PRESENT"].append(f"{run.get('agent_run_ref')}: authorities_read is missing; run context-manifest, read, then acknowledge-authorities")
            return errors
        recorded = {entry.get("path"): entry.get("sha256") for entry in read["entries"] if isinstance(entry, dict)}
        expected = self.work_item_manifest(item)
        missing = [entry["path"] for entry in expected["entries"] if entry["path"] not in recorded]
        if missing:
            errors["COMPLETE"].append(f"{run.get('agent_run_ref')}: authorities not read: {missing}")
        # An authority the Work Item is authorized to write is authored under that authorization:
        # its own writes do not make the proof stale. Every other authority must be unchanged.
        authored = item.get("authorized_paths", [])
        changed = [entry["path"] for entry in expected["entries"]
                   if entry["path"] in recorded and recorded[entry["path"]] != entry["sha256"]
                   and normal_path_errors([entry["path"]], authored)]
        if changed:
            errors["CURRENT"].append(f"{run.get('agent_run_ref')}: authorities changed since they were read: {changed}; re-read and acknowledge-authorities")
        return errors

    def require_authorities_digest(self, item: dict[str, Any], digest: str | None, command: str) -> dict[str, Any]:
        """The digest an agent presents must be the current manifest of the Work Item."""
        manifest = self.work_item_manifest(item)
        if not digest:
            raise ProjectControlError(
                f"{command} requires --authorities-digest: run `context-manifest {item['work_item_id']}`, "
                "read every listed authority, then pass its MANIFEST_DIGEST"
            )
        if digest.strip().lower() != manifest["manifest_digest"]:
            raise ProjectControlError(
                f"{command}: authorities digest does not match the current authorities of {item['work_item_id']}; "
                "run context-manifest again, read what changed, then retry"
            )
        return manifest

    def agent_run_blobs_at(self, head: str, label: str) -> dict[str, str]:
        """Agent Runs present at a declared baseline, each with the blob it held there.

        The identifier alone would not do: an exemption granted by name travels with the name,
        so rewriting the content of an exempt run would carry its exemption to work done today."""
        listing = self.run_git(["ls-tree", "-r", head, "--", "project_control/agent-runs"])
        if listing.returncode != 0:
            raise ProjectControlError(f"cannot read {label} {head}")
        blobs: dict[str, str] = {}
        for line in listing.stdout.splitlines():
            meta, _, path = line.partition("\t")
            parts = meta.split()
            if len(parts) != 3 or parts[1] != "blob" or not path.endswith(".json"):
                continue
            blobs[PurePosixPath(path).stem] = parts[2]
        return blobs

    def agent_run_refs_at(self, head: str, label: str) -> set[str]:
        """Agent Run identifiers present in the tree at a declared baseline commit."""
        return set(self.agent_run_blobs_at(head, label))

    def unchanged_agent_runs_at(self, head: str, label: str) -> set[str]:
        """Agent Runs of a baseline whose file still holds, byte for byte, what it held there."""
        unchanged: set[str] = set()
        for identifier, blob in self.agent_run_blobs_at(head, label).items():
            path = self.root / f"project_control/agent-runs/{identifier}.json"
            if not path.is_file():
                continue
            current = self.run_git(["hash-object", "--", str(path)])
            if current.returncode == 0 and current.stdout.strip() == blob:
                unchanged.add(identifier)
        return unchanged

    def agent_run_has_authorities_read(self, identifier: str) -> bool:
        path = self.root / f"project_control/agent-runs/{identifier}.json"
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return False
        return isinstance(record, dict) and bool(record.get("authorities_read"))

    def legacy_agent_run_refs(self) -> set[str]:
        """Agent Runs recorded at the adoption baseline, and untouched since, are exempt."""
        baseline = self.legacy_baseline()
        if baseline is None:
            return set()
        return self.unchanged_agent_runs_at(baseline[0], "legacy baseline")

    def authorities_exempt_agent_run_refs(self) -> set[str]:
        """Agent Runs exempt from authorities_read: recorded at the adoption baseline, or at the
        proof-of-reading baseline declared when the project adopted the proof of reading with
        Agent Runs already on record. The exemption follows the frozen state, not the name: an
        exempt run rewritten today is no longer historical and owes the proof like any other."""
        exempt = self.legacy_agent_run_refs()
        baseline = self.authorities_baseline()
        if baseline is not None:
            exempt |= self.unchanged_agent_runs_at(baseline[0], "authorities baseline")
        return exempt

    def agent_run_authority_errors(self, runs: Sequence[dict[str, Any]]) -> list[str]:
        try:
            exempt = self.authorities_exempt_agent_run_refs()
        except (ProjectControlError, OSError, ValueError) as exc:
            return [str(exc)]
        errors: list[str] = []
        for run in runs:
            ref = str(run.get("agent_run_ref"))
            read = run.get("authorities_read")
            if ref in exempt and read is None:
                continue
            if not isinstance(read, dict):
                errors.append(
                    f"Agent Run {ref}: authorities_read is required after the adoption baseline; "
                    "an Agent Run recorded before the proof of reading is exempt only through authorities_baseline"
                )
                continue
            entries = read.get("entries")
            if not isinstance(entries, list) or not entries:
                errors.append(f"Agent Run {ref}: authorities_read.entries must be non-empty")
            elif read.get("manifest_digest") != manifest_digest(entries):
                errors.append(f"Agent Run {ref}: authorities_read.manifest_digest does not match its entries")
        return errors

    def acknowledge_authorities(self, work_item_id: str, digest: str | None) -> str:
        """Record a fresh reading of the authorities on the latest Agent Run (canonical, committed)."""
        if self.operating_mode() != "NORMAL_MODE":
            raise ProjectControlError("acknowledge-authorities is available only in NORMAL_MODE")
        self.validate_clean_administrative_baseline()
        item = self.work_item_by_id(work_item_id)
        if item is None:
            raise ProjectControlError(f"unknown Work Item: {work_item_id}")
        if item.get("status") != "IN_PROGRESS":
            raise ProjectControlError(f"{work_item_id} must be IN_PROGRESS, got {item.get('status')}")
        run = self.latest_agent_run(item)
        if run is None or run.get("result") != "IN_PROGRESS":
            raise ProjectControlError(f"{work_item_id} has no Agent Run in progress")
        canonical_branch, _ = self.require_canonical_checkout("acknowledge-authorities")
        self.require_clean_worktree("acknowledge-authorities")
        manifest = self.require_authorities_digest(item, digest, "acknowledge-authorities")
        run = dict(run)
        run["authorities_read"] = manifest
        run_ref = str(run["agent_run_ref"])
        transaction = FileTransaction(self.root)
        committed: tuple[str, str] | None = None
        try:
            transaction.write_json(f"project_control/agent-runs/{run_ref}.json", run)
            self.verify_post_mutation()
            committed = self.commit_records(transaction, f"chore(project-control): acknowledge authorities {work_item_id}")
            transaction.commit()
        except BaseException as exc:
            if committed is not None:
                rollback_errors = self.uncommit_records(transaction, canonical_branch, *committed)
                if rollback_errors:
                    raise ProjectControlError(f"acknowledge-authorities failed: {exc}; ROLLBACK FAILED: {'; '.join(rollback_errors)}") from exc
            else:
                transaction.rollback()
            raise
        return run_ref

    # --- Core manifest and template-upgrade (P2): the versioned core travels with its ---
    # --- manifest; a derived project sees its drift and upgrades intact files only.  ---

    def agents_core_errors(self) -> list[str]:
        try:
            text = (self.root / "AGENTS.md").read_text(encoding="utf-8")
        except OSError as exc:
            return [f"cannot read AGENTS.md: {exc}"]
        matches = re.findall(r"(?m)^[ \t]*`AGENTS_CORE:\s*([^`\r\n]+)`[ \t]*$", text)
        if len(matches) != 1:
            return [f"AGENTS.md must declare `AGENTS_CORE: {AGENTS_CORE_PATH}` exactly once; found {len(matches)}"]
        declared = matches[0].strip()
        if declared != AGENTS_CORE_PATH:
            return [f"AGENTS.md declares AGENTS_CORE {declared}; expected {AGENTS_CORE_PATH}"]
        if not (self.root / AGENTS_CORE_PATH).is_file():
            return [f"missing core authority: {AGENTS_CORE_PATH}"]
        return []

    def core_manifest_errors(self) -> list[str]:
        """CORE_MANIFEST: manifest present and well-formed, every listed core file present,
        AGENTS.md including the versioned core. A locally modified core file is not an audit
        error: status lists it and template-upgrade refuses to overwrite it silently."""
        try:
            manifest = load_core_manifest(self.root)
        except (OSError, json.JSONDecodeError, ProjectControlError) as exc:
            return [str(exc)]
        errors = [
            f"core file missing: {path}"
            for path, state in core_drift(self.root, manifest).items() if state == "MISSING"
        ]
        if AGENTS_CORE_PATH not in manifest["core"]:
            errors.append(f"core manifest does not list {AGENTS_CORE_PATH}")
        errors.extend(self.agents_core_errors())
        return errors

    def core_status(self) -> dict[str, Any]:
        """skeleton_version and core drift for status; never raises."""
        try:
            manifest = load_core_manifest(self.root)
        except (OSError, json.JSONDecodeError, ProjectControlError) as exc:
            return {"skeleton_version": "UNKNOWN", "core_drift": {CORE_MANIFEST_PATH: f"INVALID: {exc}"}}
        return {"skeleton_version": manifest["skeleton_version"], "core_drift": core_drift(self.root, manifest)}

    def core_manifest_findings(self) -> list[Finding]:
        """Read-only: does the committed manifest describe this tree's core exactly?"""
        findings: list[Finding] = []
        try:
            manifest = load_core_manifest(self.root)
        except (OSError, json.JSONDecodeError, ProjectControlError) as exc:
            add(findings, "CORE_MANIFEST", False, str(exc))
            return findings
        add(findings, "CORE_MANIFEST", True, f"skeleton_version {manifest['skeleton_version']}, {len(manifest['core'])} core file(s)")
        drift = core_drift(self.root, manifest)
        unlisted = sorted(set(core_files(self.root)) - set(manifest["core"]))
        add(findings, "CORE_ALIGNED", not drift and not unlisted,
            "tree matches the manifest" if not drift and not unlisted
            else f"drift: {drift}; core files not listed: {unlisted}")
        return findings

    def write_core_manifest(self, version: str) -> dict[str, Any]:
        if self.project_state().get("repository_role") != "PROJECT_TEMPLATE":
            raise ProjectControlError(
                "core-manifest --write is reserved to the template; a derived project receives its manifest through template-upgrade"
            )
        manifest = build_core_manifest(self.root, version)
        transaction = FileTransaction(self.root)
        try:
            transaction.write_json(CORE_MANIFEST_PATH, manifest)
            transaction.commit()
        except BaseException:
            transaction.rollback()
            raise
        return manifest

    def seed_required_files(self, source: Path, source_version: str, missing: list[str]) -> list[Finding]:
        """Write the files a newer version requires and the project does not have.

        Only files the source itself carries, only files the audit requires, only files the core
        does not own — and never over an existing one: this adds what is absent, it never
        replaces what the project wrote. They are administrative records, hence the canonical
        branch, where Project Control writes every other record."""
        findings: list[Finding] = []
        canonical = self.canonical_branch()
        branch = self.repository_context()["branch"]
        if branch != canonical:
            add(findings, "SEED_REQUIRED", False,
                f"administrative records are written on {canonical} only; this checkout is on {branch}")
            return findings
        if not missing:
            add(findings, "SEED_REQUIRED", True, f"nothing to seed: {source_version} requires no file the project lacks")
            return findings
        transaction = FileTransaction(self.root)
        try:
            for path in missing:
                transaction.write_bytes(path, (source / path).read_bytes(), (source / path).stat().st_mode)
            transaction.commit()
        except BaseException:
            transaction.rollback()
            raise
        add(findings, "SEED_REQUIRED", True,
            f"{len(missing)} file(s) written from {source_version}, blank as the template holds them: {missing}. "
            f"Commit them on {canonical} as an administrative change; the core is applied separately")
        return findings

    REHEARSAL_EXEMPT_CHECKS = ("COMMIT_GATE",)  # the apply reinstalls the gate itself

    def rehearse_upgrade(self, source: Path, source_version: str, to_write: Sequence[str]) -> tuple[bool, str]:
        """The new controller's audit on a throwaway checkout carrying the new core — before
        anything is written to the project.

        The command that upgrades a project runs under the project's current controller, which
        knows nothing of the rules the new version brings: a file it now requires, a decision
        field it now demands. Applied blind, such an upgrade completes and leaves the project
        red behind it — the wall met at 3.8.0, again at 3.18.0 with the baselines. So the
        upgrade is rehearsed first: HEAD is checked out in a linked worktree, the planned core
        is written and committed there, and the *new* `audit` is run on it. What it refuses is
        reported here, and `--apply` refuses while it does. The commit gate is exempt: the apply
        reinstalls it. The worktree is removed, whatever happens.
        """
        head = self.run_git(["rev-parse", "--verify", "HEAD"]).stdout.strip()
        if not SHA40.fullmatch(head):
            return False, "cannot rehearse without a HEAD to rehearse on"
        self.purge_stale_throwaway_checkouts()
        try:
            root, claim = self.open_throwaway("project-control-upgrade-", "rehearsal")
        except OSError as exc:
            return False, f"cannot rehearse: {exc}"
        checkout = str(root)
        environment = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        try:
            added = self.run_git(["worktree", "add", "--detach", checkout, head])
            if added.returncode != 0:
                return False, f"cannot rehearse: {added.stderr.strip() or added.stdout.strip()}"
            written: list[str] = []
            for path in to_write:
                content = upgraded_content(self.root, source, path)
                at_head = self.run_git(["rev-parse", "--verify", "--quiet", f"{head}:{path}"]).stdout.strip()
                if at_head and at_head == blob_digest(content):
                    continue
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
                os.chmod(target, (source / path).stat().st_mode)
                written.append(path)
            (root / CORE_MANIFEST_PATH).write_bytes((source / CORE_MANIFEST_PATH).read_bytes())
            written.append(CORE_MANIFEST_PATH)

            def git(*arguments: str) -> subprocess.CompletedProcess[str]:
                return subprocess.run(
                    ["git", "-c", "core.hooksPath=/dev/null", "-c", "user.name=Project Control",
                     "-c", "user.email=project-control@example.invalid", *arguments],
                    cwd=checkout, capture_output=True, text=True, env=environment, check=False,
                )

            staged = git("add", "--", *written)
            if staged.returncode != 0:
                return False, f"cannot rehearse: {staged.stderr.strip()}"
            committed = git("commit", "-q", "--no-verify", "--allow-empty", "-m", f"project-control: rehearsal of {source_version}")
            if committed.returncode != 0:
                return False, f"cannot rehearse: {committed.stderr.strip()}"
            audit = subprocess.run(
                [sys.executable, "-B", "scripts/project_control.py", "audit"],
                cwd=checkout, capture_output=True, text=True, env=environment, check=False, timeout=600,
            )
            reported = [line for line in audit.stdout.splitlines() if line.startswith("FAIL: ")]
            exempt = tuple(f"FAIL: {check} " for check in self.REHEARSAL_EXEMPT_CHECKS)
            failures = [line for line in reported if not line.startswith(exempt)]
            # An audit that fails only on an exempt check exits non-zero all the same: that exit
            # status is the exempt failure, not a second one. It used to be read as a generic
            # error, and a source whose only change was the gate itself was refused (fourth
            # independent control, F13-01).
            if audit.returncode != 0 and not reported:
                tail = (audit.stderr.strip().splitlines() or audit.stdout.strip().splitlines() or ["no output"])[-1]
                failures = [f"the new controller's audit exited {audit.returncode}: {tail}"]
            if failures:
                return False, (
                    f"{source_version} applied on a throwaway checkout of {head[:12]} would leave the project "
                    f"refused by its own audit — resolve this first, then upgrade: " + "; ".join(failures)
                )
            exempted = f"; exempt: {[line.split(' — ')[0][6:] for line in reported]} (the apply reinstalls the gate)" if reported else ""
            return True, (f"the new controller's audit passes on a throwaway checkout of {head[:12]} carrying "
                          f"{source_version} ({len(written) - 1} core file(s) differ from HEAD){exempted}")
        except (OSError, subprocess.SubprocessError) as exc:
            return False, f"cannot rehearse: {exc}"
        finally:
            self.close_throwaway(root, claim)
            self.run_git(["worktree", "prune"])

    def template_upgrade(
        self, source: Path, apply: bool, overwrite: Iterable[str] = (), seed_required: bool = False,
    ) -> list[Finding]:
        """Report (default) or apply the core of another template tree onto this project.

        Intact core files are updated, absent ones added; a locally modified core file is
        refused unless named by --overwrite; files removed upstream are reported, never deleted;
        records are never touched. The manifest of the source becomes the project's manifest.

        A newer version may also require files the project does not have and the core does not
        carry — the project's own ideas list, its view settings: mandatory, but the project's, so
        the core write leaves them alone. Missing, they fail the audit, and the commands meant to
        create them refuse for want of them. They are administrative records, so they belong on
        the canonical branch, not on the Work Item branch that carries the core: `--seed-required`
        writes them there, before the upgrade, and `--apply` refuses while they are missing rather
        than leaving the project in a state where nothing works.
        """
        findings: list[Finding] = []
        source = source.resolve()
        if not source.is_dir() or source == self.root:
            raise ProjectControlError("--source must be a directory holding another tree of the template")
        try:
            source_manifest = load_core_manifest(source)
        except (OSError, json.JSONDecodeError, ProjectControlError) as exc:
            add(findings, "SOURCE_MANIFEST", False, f"{source}: {exc}")
            return findings
        source_version = source_manifest["skeleton_version"]
        source_drift = core_drift(source, source_manifest)
        add(findings, "SOURCE_MANIFEST", not source_drift,
            f"{source} at {source_version}, {len(source_manifest['core'])} core file(s)"
            if not source_drift else f"source core is not intact: {source_drift}")
        try:
            local_manifest = load_core_manifest(self.root)
        except (OSError, json.JSONDecodeError, ProjectControlError) as exc:
            add(findings, "LOCAL_MANIFEST", False, str(exc))
            return findings
        local_version = local_manifest["skeleton_version"]
        add(findings, "LOCAL_MANIFEST", True, f"project at {local_version}, {len(local_manifest['core'])} core file(s)")
        if version_tuple(source_version) < version_tuple(local_version):
            add(findings, "UPGRADE_DIRECTION", False,
                f"source {source_version} is older than the project's {local_version}; a downgrade is not an upgrade")
            return findings
        required_missing = sorted(
            path for path in REQUIRED_FILES
            if path not in source_manifest["core"]
            and not (self.root / path).is_file()
            and (source / path).is_file()
        )
        if seed_required:
            return findings + self.seed_required_files(source, source_version, required_missing)
        add(findings, "REQUIRED_FILES", not required_missing,
            "the project has every file the new version requires"
            if not required_missing else
            f"{source_version} requires {len(required_missing)} file(s) the project does not have and the core "
            f"does not carry: {required_missing}. They are administrative records: write them on the canonical "
            f"branch first with `template-upgrade --source <source> --seed-required`, commit them there, then "
            f"come back and apply the core")
        local_drift = core_drift(self.root, local_manifest)
        plan: dict[str, str] = {}
        for path, digest in source_manifest["core"].items():
            local_file = self.root / path
            if local_drift.get(path) == "MODIFIED_LOCALLY":
                plan[path] = "MODIFIED_LOCALLY"
            elif not local_file.is_file():
                plan[path] = "ADDED"
            elif core_digest(self.root, path) == digest:
                plan[path] = "IDENTICAL"
            elif path not in local_manifest["core"]:
                # The new core claims a path the project already occupies with a file of its
                # own — the old manifest never knew it, so no drift is reported for it. Writing
                # over it would destroy the project's file without a word.
                plan[path] = "PROJECT_FILE"
            else:
                plan[path] = "UPDATED"
        for path in local_manifest["core"]:
            if path not in source_manifest["core"]:
                plan[path] = "REMOVED_UPSTREAM"
        by_state = {
            state: sorted(path for path, value in plan.items() if value == state)
            for state in ("IDENTICAL", "UPDATED", "ADDED", "REMOVED_UPSTREAM", "MODIFIED_LOCALLY", "PROJECT_FILE")
        }
        requested = {safe_relative_path(value) or value for value in overwrite}
        protected = by_state["MODIFIED_LOCALLY"] + by_state["PROJECT_FILE"]
        refused = [path for path in protected if path not in requested]
        unmatched = sorted(requested - set(protected))
        add(findings, "UPGRADE_PLAN", True,
            f"{local_version} -> {source_version}: identical {len(by_state['IDENTICAL'])}, "
            f"updated {by_state['UPDATED']}, added {by_state['ADDED']}, "
            f"removed upstream {by_state['REMOVED_UPSTREAM']}, modified locally {by_state['MODIFIED_LOCALLY']}, "
            f"project files on core paths {by_state['PROJECT_FILE']}")
        intact_detail = "every core file to update is intact locally"
        modified = [path for path in by_state["MODIFIED_LOCALLY"] if path not in requested]
        owned = [path for path in by_state["PROJECT_FILE"] if path not in requested]
        if modified:
            intact_detail = f"modified locally, refused without --overwrite: {modified}"
        if owned:
            clause = f"the project owns these paths, refused without --overwrite: {owned}"
            intact_detail = clause if not modified else f"{intact_detail}; {clause}"
        if unmatched:
            intact_detail += f"; --overwrite names no protected file: {unmatched}"
        add(findings, "LOCAL_CORE_INTACT", not refused and not unmatched, intact_detail)
        to_write = sorted(
            path for path, state in plan.items()
            if state in {"UPDATED", "ADDED"} or (state in {"MODIFIED_LOCALLY", "PROJECT_FILE"} and path in requested)
        )
        if (
            not any(item.status == "FAIL" for item in findings)
            and self.operating_mode() == "NORMAL_MODE"
            and self.project_state().get("repository_role") != "PROJECT_TEMPLATE"
        ):
            # The rehearsal represents the project as it will be committed after the apply:
            # HEAD, plus every core path the apply may write — judged against HEAD's blobs, not
            # against the disk. A core already written on the disk but not yet committed used to
            # leave the rehearsal with nothing to write, and the audit ran on the old controller
            # held in HEAD while announcing the new one (fourth independent control, F13-02).
            rehearsal_paths = [
                path for path in source_manifest["core"]
                if not (plan.get(path) in {"MODIFIED_LOCALLY", "PROJECT_FILE"} and path not in requested)
            ]
            rehearsed, rehearsal = self.rehearse_upgrade(source, source_version, rehearsal_paths)
            add(findings, "UPGRADE_REHEARSAL", rehearsed, rehearsal)
        if not apply:
            add(findings, "DRY_RUN", True, "nothing written; add --apply to upgrade")
            return findings
        if any(item.status == "FAIL" for item in findings):
            add(findings, "APPLY", False, "refused: resolve the failures above; nothing written")
            return findings
        if self.operating_mode() != "NORMAL_MODE":
            add(findings, "APPLY", False, "template-upgrade --apply requires NORMAL_MODE; a NOT_STARTED copy is replaced by a fresh copy of the template")
            return findings
        if self.project_state().get("repository_role") == "PROJECT_TEMPLATE":
            add(findings, "APPLY", False, "the template is upgraded by its own maintenance, not by template-upgrade")
            return findings
        transaction = FileTransaction(self.root)
        try:
            for path in to_write:
                transaction.write_bytes(path, upgraded_content(self.root, source, path), (source / path).stat().st_mode)
            transaction.write_bytes(CORE_MANIFEST_PATH, (source / CORE_MANIFEST_PATH).read_bytes())
            remaining = core_drift(self.root, source_manifest)
            if remaining:
                raise ProjectControlError(f"post-upgrade verification failed: {remaining}")
            transaction.commit()
        except BaseException:
            transaction.rollback()
            raise
        add(findings, "APPLY", True,
            f"{len(to_write)} core file(s) written, manifest now {source_version}; "
            f"removed upstream and left in place for a human decision: {by_state['REMOVED_UPSTREAM']}")
        # The executable gate lives outside the worktree, so the upgrade cannot have touched it:
        # left alone it would keep running the previous version. Reinstall it here rather than
        # leave the project one forgotten command away from an unguarded commit.
        state = self.commit_gate_state()
        if state in {"INSTALLED", "MISMATCH"}:
            self.install_commit_gate()
            add(findings, "COMMIT_GATE_REINSTALLED", self.commit_gate_state() == "INSTALLED",
                "the installed gate now matches the upgraded reference"
                if self.commit_gate_state() == "INSTALLED" else "reinstalling the gate failed — run install-gate")
        else:
            add(findings, "COMMIT_GATE_REINSTALLED", True,
                f"gate {state}: nothing to reinstall — run install-gate to have Git run the upgraded gate")
        return findings

    def is_canonical_commit_path(self, path: str) -> bool:
        """Paths a commit on the canonical branch may carry without a human authorization."""
        return self.is_administrative_path(path) or path.startswith(("reports/", "provenance/"))

    def commit_gate_findings(self) -> list[Finding]:
        """Read-only gate run by scripts/hooks/pre-commit before every commit.

        Fail-closed: the mode audit runs on the tree the commit would create — not on the
        working tree, which can differ from it — and the canonical branch
        only receives administrative records, reports and provenance — business, core and
        authority paths need a dedicated branch. Integration merges are not development and
        pass. PROJECT_CONTROL_HOOK_OVERRIDE=<human mandate> bypasses both rules explicitly;
        the mandate is echoed so that it appears in the terminal transcript.
        """
        findings: list[Finding] = []
        override = os.environ.get("PROJECT_CONTROL_HOOK_OVERRIDE", "").strip()
        staged = self.staged_paths()
        mode = self.operating_mode()
        add(findings, "STAGED_PATHS", "<git-diff-failed>" not in staged,
            f"{len(staged)} staged path(s)" if staged else "nothing staged")
        if override:
            add(findings, "HOOK_OVERRIDE", True, f"explicit human mandate supplied: {override}")
            return findings
        context = self.repository_context()
        if mode == "NORMAL_MODE":
            try:
                canonical = self.canonical_branch()
            except ProjectControlError as exc:
                canonical = None
                add(findings, "CANONICAL_BRANCH_DECLARED", False, str(exc))
            if canonical is not None and context["branch"] == canonical and not self.merge_in_progress():
                offending = [path for path in staged if not self.is_canonical_commit_path(path)]
                add(findings, "CANONICAL_BRANCH_PROTECTED", not offending,
                    "only administrative, report or provenance paths are staged on the canonical branch"
                    if not offending else
                    f"development on canonical branch {canonical} requires a dedicated Work Item branch "
                    f"or PROJECT_CONTROL_HOOK_OVERRIDE: {offending}")
            elif canonical is not None and not self.merge_in_progress():
                records = [path for path in staged if self.is_administrative_path(path)]
                add(findings, "WORK_BRANCH_RECORDS_READ_ONLY", not records,
                    "no administrative record is staged on the Work Item branch"
                    if not records else
                    f"administrative records are committed by Project Control on {canonical} only: {records}")
                check, ok, detail = self.work_branch_scope_gate(staged)
                add(findings, check, ok, detail)
            # Wherever the project state is in the commit — a Work Item branch, the canonical
            # branch, an integration merge — a baseline leaves or moves only on a decision.
            # The rule used to run on the Work Item branch alone, and the merge that integrated
            # the branch could edit the state on the way (fourth independent control, F12-01).
            check, ok, detail = self.baseline_change_gate(staged)
            add(findings, check, ok, detail)
            mode_findings, audited = self.staged_state_findings(mode, staged)
        elif mode == "BOOTSTRAP_MODE":
            mode_findings, audited = self.staged_state_findings(mode, staged)
        else:
            mode_findings, audited = [], "nothing"
            add(findings, "OPERATING_MODE", False, f"FIRST_START status invalid: {mode}")
        failures = [f"{item.check}: {item.detail}" for item in mode_findings if item.status == "FAIL"]
        add(findings, "MODE_AUDIT", not failures,
            f"{'audit' if mode == 'NORMAL_MODE' else 'bootstrap-audit'} PASS on {audited}"
            if not failures else "; ".join(failures))
        return findings

    def throwaway_owner(self) -> str | None:
        """What identifies this repository to its own throwaway checkouts: its common Git
        directory, resolved — the same from the main worktree and from any linked one."""
        common = git_common_dir(self.root)
        if common is None:
            return None
        try:
            return str(common.resolve())
        except OSError:
            return None

    def open_throwaway(self, prefix: str, checkout_name: str) -> tuple[Path, IO[str]]:
        """A holder folder of the controller's own for one throwaway checkout, marked and locked.

        The holder is created here, empty; the marker names this repository and the checkout
        the holder is for; the handle returned holds the marker locked for as long as the
        caller keeps it — the life of the command — so that a sweep from another process can
        tell a command still running from one that died. `close_throwaway` takes it all down."""
        holder = Path(tempfile.mkdtemp(prefix=prefix))
        marker = holder / THROWAWAY_MARKER_NAME
        marker.write_text(json.dumps({
            "repository": self.throwaway_owner(),
            "checkout": checkout_name,
            "pid": os.getpid(),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }, indent=2) + "\n", encoding="utf-8")
        claim = open(marker, "r+", encoding="utf-8")
        try:
            fcntl.flock(claim.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            claim.close()
            raise
        return holder / checkout_name, claim

    def close_throwaway(self, checkout: Path, claim: IO[str] | None) -> None:
        """Take a throwaway down: the checkout out of the worktree list and off the disk, the
        marker gone, the holder removed once nothing is left in it. Never recursively on the
        holder: a file that is not the checkout is not the controller's to remove, whoever put
        it there and whatever the folder is called."""
        self.remove_own_checkout(checkout)
        holder = checkout.parent
        if claim is not None:
            try:
                fcntl.flock(claim.fileno(), fcntl.LOCK_UN)
            except OSError:
                pass
            claim.close()
        for remove in ((holder / THROWAWAY_MARKER_NAME).unlink, holder.rmdir):
            try:
                remove()
            except OSError:
                pass

    def remove_own_checkout(self, checkout: Path) -> None:
        """Git removes a linked worktree it registered; a folder Git no longer knows is removed
        only if it is provably a linked checkout of this repository — its `.git` a file pointing
        into this repository's `worktrees/` — and it is the checkout its holder's marker names."""
        self.run_git(["worktree", "remove", "--force", str(checkout)])
        if checkout.exists() and self.is_own_linked_checkout(checkout):
            shutil.rmtree(checkout, ignore_errors=True)

    def is_own_linked_checkout(self, checkout: Path) -> bool:
        owner = self.throwaway_owner()
        pointer = checkout / ".git"
        if owner is None or not pointer.is_file():
            return False
        common = git_common_dir(checkout)
        try:
            return common is not None and str(common.resolve()) == owner
        except OSError:
            return False

    def purge_stale_throwaway_checkouts(self) -> list[str]:
        """Remove the throwaway checkouts this controller made and did not live to remove.

        Only what is provably its own: a linked worktree whose holder carries the controller's
        marker, naming this repository and that checkout — written by the command that made it
        — and whose marker is no longer locked, which happens only once that command is dead: a
        suspended or slow command still holds its lock, however old its checkout. What goes is
        the checkout, the marker, and the holder once it is empty. A folder whose name looks
        like the controller's, a checkout older than any limit, a note next to a checkout: none
        is touched. The sweep that used a name prefix and an age removed a review worktree and
        the two notes beside it (fifth independent control, F-01). Returns the checkouts removed."""
        owner = self.throwaway_owner()
        listed = self.run_git(["worktree", "list", "--porcelain"])
        if owner is None or listed.returncode != 0:
            return []
        removed: list[str] = []
        for line in listed.stdout.splitlines():
            if not line.startswith("worktree "):
                continue
            checkout = Path(line[len("worktree "):].strip())
            marker = checkout.parent / THROWAWAY_MARKER_NAME
            try:
                written = json.loads(marker.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if not isinstance(written, dict) or written.get("repository") != owner or written.get("checkout") != checkout.name:
                continue
            try:
                claim = open(marker, "r+", encoding="utf-8")
            except OSError:
                continue
            try:
                fcntl.flock(claim.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                claim.close()  # the command that made it is still running
                continue
            self.close_throwaway(checkout, claim)
            removed.append(str(checkout))
        if removed:
            self.run_git(["worktree", "prune"])
        return removed

    def history_heads(self) -> list[str]:
        """The commits the next commit will descend from: HEAD, and any merge in progress.

        During a merge the branch tip does not yet hold what the merge brings in. Judging an
        administrative commit against HEAD alone therefore refuses, at the very moment of the
        merge, a record whose closure arrives with it: with the gate installed, a blocked Work
        Item could no longer be resumed once a sibling had been closed on the canonical branch.
        The suite did not see it because it builds its repositories without the gate."""
        heads: list[str] = []
        head = self.run_git(["rev-parse", "--verify", "--quiet", "HEAD"])
        if head.returncode == 0 and SHA40.fullmatch(head.stdout.strip()):
            heads.append(head.stdout.strip())
        located = self.run_git(["rev-parse", "--git-path", "MERGE_HEAD"])
        if located.returncode == 0 and located.stdout.strip():
            try:
                # MERGE_HEAD holds one line per incoming parent; read them all rather than
                # resolve the ref, which would name only the first.
                merging = (self.root / located.stdout.strip()).read_text(encoding="utf-8").split()
            except OSError:
                merging = []
            heads.extend(parent for parent in merging if SHA40.fullmatch(parent) and parent not in heads)
        return heads

    def in_current_history(self, commit: str) -> bool:
        """Is this commit already part of what the next commit will descend from?"""
        return any(
            self.run_git(["merge-base", "--is-ancestor", commit, head]).returncode == 0
            for head in self.history_heads()
        )

    @contextlib.contextmanager
    def staged_worktree(self) -> Any:
        """A throwaway checkout of exactly what the commit would create, or None.

        The gate used to audit the working tree while announcing "the staged state". They are
        not the same thing: an index can hold a falsified record while the file on disk is
        clean, and the commit carries the index, not the disk. So the index is materialised as
        a real tree and audited there. Yields None when Git cannot do it, and the caller then
        says plainly what it could check."""
        self.purge_stale_throwaway_checkouts()
        tree = self.run_git(["write-tree"])
        digest = tree.stdout.strip()
        if tree.returncode != 0 or not SHA40.fullmatch(digest):
            yield None
            return
        # The commit Git is about to make descends from HEAD and from any merge in progress:
        # a photograph carrying the branch tip alone is not what the commit would create.
        parents = [argument for parent in self.history_heads() for argument in ("-p", parent)]
        commit = self.run_git(["commit-tree", digest, *parents, "-m", "project-control: staged state"])
        if commit.returncode != 0 or not SHA40.fullmatch(commit.stdout.strip()):
            yield None
            return
        try:
            checkout, claim = self.open_throwaway("project-control-staged-", "staged")
        except OSError:
            yield None
            return
        # Everything from here on needs an index of its own: inside a commit hook Git exports
        # GIT_INDEX_FILE and holds its lock, and a command that inherits it fails.
        borrowed = os.environ.pop("GIT_INDEX_FILE", None)
        try:
            added = self.run_git(["worktree", "add", "--detach", "--quiet", str(checkout), commit.stdout.strip()])
            if added.returncode != 0:
                yield None
            else:
                yield checkout
        finally:
            self.close_throwaway(checkout, claim)
            if borrowed is not None:
                os.environ["GIT_INDEX_FILE"] = borrowed

    def staged_state_findings(self, mode: str, staged: Sequence[str]) -> tuple[list[Finding], str]:
        """The mode audit run on the working tree AND on the tree the commit would create.

        Both are needed, and neither replaces the other. Checks about pending changes — business
        change authorization, Git traceability, a merge in progress — only mean something in the
        live repository, where those changes exist. Checks about content — records, schemas,
        roadmap and record coherence, the core manifest — must judge what the commit carries,
        which the working tree can contradict. Failures from either side fail the gate."""

        def audit(control: ProjectControl) -> list[Finding]:
            return control.audit_findings() if mode == "NORMAL_MODE" else control.bootstrap_findings(staged)

        live = audit(self)
        with self.staged_worktree() as checkout:
            if checkout is None:
                # Fail closed. Falling back on the working tree and announcing PASS made the
                # guarantee cancel itself the moment it was inconvenienced: what the commit
                # carries is exactly what could no longer be read. The mandated override stays
                # the way through for an environment where a temporary checkout is impossible.
                refusal = list(live)
                add(refusal, "STAGED_STATE_AUDITED", False,
                    "the staged state could not be materialised, so what this commit would write "
                    "could not be read; refused rather than judged on the working tree, which can "
                    "differ from it. PROJECT_CONTROL_HOOK_OVERRIDE=<mandat> if this environment "
                    "cannot make a temporary checkout")
                return refusal, "the working tree only (the staged state could not be materialised)"
            passing = {item.check for item in live if item.status != "FAIL"}
            extra = [
                Finding(item.check, item.status, f"in the staged state: {item.detail}")
                for item in audit(ProjectControl(checkout))
                if item.status == "FAIL" and item.check in passing
            ]
        return live + extra, "the working tree and the staged state"

    def work_branch_scope_gate(self, staged: Iterable[str]) -> tuple[str, bool, str]:
        """The commit gate applies the active Work Item's authorized paths to every staged path.

        The preflight already refuses a path outside the authorization; the gate has to refuse
        the same commit, otherwise a check skipped or a file added after it is enough to carry
        unauthorized work. Administrative records are handled by their own finding above; every
        other path — business, core, contracts, data, docs, scripts, tests — is measured against
        the authorization of the single active Work Item.
        """
        candidates = [path for path in staged if not self.is_administrative_path(path)]
        if not candidates:
            return "WORK_BRANCH_AUTHORIZED_PATHS", True, "no working path staged on the Work Item branch"
        try:
            active = [item for item in self.records("project_control/work-items")
                      if item.get("status") == "IN_PROGRESS"]
        except (OSError, json.JSONDecodeError) as exc:
            return "WORK_BRANCH_AUTHORIZED_PATHS", False, f"cannot resolve active Work Item: {exc}"
        if len(active) != 1:
            return ("WORK_BRANCH_AUTHORIZED_PATHS", False,
                    "a commit on a Work Item branch requires exactly one IN_PROGRESS Work Item; "
                    f"found {[item.get('work_item_id') for item in active]}")
        item = active[0]
        errors = normal_path_errors(candidates, item.get("authorized_paths", []))
        return ("WORK_BRANCH_AUTHORIZED_PATHS", not errors,
                f"every staged path belongs to {item.get('work_item_id')}" if not errors
                else "; ".join(errors))

    def committed_project_state(self, revision: str) -> dict[str, Any] | None:
        """The project state as Git holds it at `revision` — "HEAD", or "" for the index; None
        when absent there or unreadable (the mode audit says so in its own words)."""
        shown = self.run_git(["show", f"{revision}:project_control/project-state.v1.json"])
        if shown.returncode != 0:
            return None
        try:
            loaded = json.loads(shown.stdout)
        except json.JSONDecodeError:
            return None
        return loaded if isinstance(loaded, dict) else None

    def baseline_change_gate(self, staged: Iterable[str]) -> tuple[str, bool, str]:
        """A baseline leaves or moves only on a decision that says so (P17, steps 2 and 3).

        The project state is a file a Work Item may legitimately be authorised to write — the
        language and the reporting style live there. Setting a baseline to null was an ordinary
        write in an authorised file, and from that commit on nothing protected the closures behind
        the line. So the gate compares what the commit would carry with what HEAD holds: a
        baseline removed needs a decision of the active Work Item that names the removal and the
        commit it un-freezes; a baseline moved must descend from the one it replaces — the line
        of the past advances, it never recedes. A baseline declared or moved is anchored to its
        decision by the audit of the staged state, which runs after this check. The comparison
        runs wherever the project state is staged — a Work Item branch, the canonical branch, an
        integration merge whose result was edited before the commit.
        """
        check = "BASELINE_CHANGE_MANDATED"
        if "project_control/project-state.v1.json" not in set(staged):
            return check, True, "no baseline touched by this commit"
        before = self.committed_project_state("HEAD") or {}
        after = self.committed_project_state("") or {}

        def declared_head(state: dict[str, Any], kind: str) -> str | None:
            declared = state.get(kind)
            head = declared.get("head") if isinstance(declared, dict) else None
            return head if isinstance(head, str) and SHA40.fullmatch(head) else None

        errors: list[str] = []
        changes: list[str] = []
        for kind, (named_field, removed_field) in BASELINE_DECISION_FIELDS.items():
            old, new = declared_head(before, kind), declared_head(after, kind)
            if old == new:
                continue
            label = kind.replace("_", " ")
            if new is None:
                decision = self.active_work_item_decision_naming(removed_field, old)
                if decision is None:
                    errors.append(
                        f"{label} {old} is removed by this commit without a decision of the active Work Item "
                        f"carrying `{removed_field}: {old}`; removing a baseline is a human decision, recorded "
                        f"on the canonical branch before the work"
                    )
                else:
                    changes.append(f"{label} {old} removed on {decision}")
            elif old is not None:
                descends = self.run_git(["merge-base", "--is-ancestor", old, new]).returncode == 0
                if not descends:
                    errors.append(f"{label} would move from {old} to {new}, which does not descend from it: "
                                  f"a baseline never recedes")
                else:
                    changes.append(f"{label} moves from {old} to {new}; its decision must carry `{named_field}: {new}`")
            else:
                changes.append(f"{label} declared at {new}; its decision must carry `{named_field}: {new}`")
        if errors:
            return check, False, "; ".join(errors)
        return check, True, "; ".join(changes) if changes else "baselines unchanged"

    def active_work_item_decision_naming(self, field: str, value: str | None) -> str | None:
        """The decision of the single IN_PROGRESS Work Item that carries `field: value`, read as
        committed at HEAD — a decision only staged, or only on disk, mandates nothing."""
        if value is None:
            return None
        try:
            active = [item for item in self.records("project_control/work-items")
                      if item.get("status") == "IN_PROGRESS"]
        except (OSError, json.JSONDecodeError):
            return None
        if len(active) != 1:
            return None
        shown = self.run_git(["show", "HEAD:docs/governance/HUMAN_DECISIONS.md"])
        if shown.returncode != 0:
            return None
        for reference in active[0].get("human_decision_refs", []):
            if isinstance(reference, str) and human_decision_field(shown.stdout, reference, field) == value:
                return reference
        return None

    def work_item_by_id(self, work_item_id: str) -> dict[str, Any] | None:
        return next((item for item in self.records("project_control/work-items") if item.get("work_item_id") == work_item_id), None)

    def is_administrative_path(self, path: str) -> bool:
        return path in ADMINISTRATIVE_EXACT_PATHS or any(
            path.startswith(prefix)
            for prefix in (
                "project_control/work-items/",
                "project_control/conversations/",
                "project_control/agent-runs/",
            )
        )

    def generated_paths(self) -> list[str]:
        try:
            payload = load_json(self.classifications_path)
        except (OSError, json.JSONDecodeError):
            return []
        values = payload.get("PROJECT_CONTROL_GENERATED", [])
        return sorted(set(str(value) for value in values if safe_relative_path(str(value))))

    def register_generated_paths(self, transaction: FileTransaction, paths: Iterable[str]) -> None:
        payload = load_json(self.classifications_path)
        existing = payload.get("PROJECT_CONTROL_GENERATED", [])
        if not isinstance(existing, list):
            raise ProjectControlError("PROJECT_CONTROL_GENERATED classification must be a list")
        normalized = []
        for value in [*existing, *paths]:
            path = safe_relative_path(str(value))
            if path is None:
                raise ProjectControlError(f"unsafe generated path: {value}")
            normalized.append(path)
        payload["PROJECT_CONTROL_GENERATED"] = sorted(set(normalized))
        transaction.write_json("docs/governance/git-path-classifications.v1.json", payload)

    def update_roadmap(
        self,
        transaction: FileTransaction,
        item: dict[str, Any],
        integration_state: str,
    ) -> None:
        roadmap = load_json(self.roadmap_json)
        summaries = roadmap.get("work_items")
        if not isinstance(summaries, list):
            raise ProjectControlError("roadmap work_items must be a list")
        summary = {
            "work_item_id": item["work_item_id"],
            "display_reference": item["display_reference"],
            "title": item["title"],
            "status": item["status"],
            "integration_state": integration_state,
            "human_gate": item["human_decision_refs"][0],
            "dependencies": item["dependencies"],
        }
        indexes = [index for index, value in enumerate(summaries) if value.get("work_item_id") == item["work_item_id"]]
        if len(indexes) > 1:
            raise ProjectControlError(f"duplicate roadmap entry for {item['work_item_id']}")
        if indexes:
            summaries[indexes[0]] = summary
        else:
            summaries.append(summary)
        summaries.sort(key=lambda value: value["work_item_id"])
        roadmap["updated_at"] = now_iso()
        transaction.write_json("docs/governance/roadmap-state.v1.json", roadmap)
        transaction.write_text(
            "docs/governance/ROADMAP.md",
            render_roadmap_markdown(self.roadmap_md.read_text(encoding="utf-8"), summaries),
        )

    def update_registry(self, transaction: FileTransaction, item: dict[str, Any], status: str) -> None:
        transaction.write_text(
            "docs/governance/WORKTREE_REGISTRY.md",
            render_registry_entry(
                self.worktree_registry.read_text(encoding="utf-8"),
                item,
                status,
            ),
        )

    def validate_clean_administrative_baseline(self) -> None:
        findings = self.audit_findings()
        failures = [f"{item.check}: {item.detail}" for item in findings if item.status == "FAIL"]
        if failures:
            raise ProjectControlError("audit refused lifecycle mutation: " + "; ".join(failures))

    def require_clean_worktree(self, command: str) -> None:
        changed = self.changed_paths()
        if changed:
            raise ProjectControlError(f"{command} requires a clean worktree: {changed}")

    def require_canonical_checkout(self, command: str) -> tuple[str, str]:
        """Lifecycle transitions run from the canonical branch at its tip: records live only there."""
        context = self.repository_context()
        canonical_branch, canonical_head = self.canonical_tip()
        if context["branch"] != canonical_branch or context["head"] != canonical_head:
            raise ProjectControlError(
                f"canonical branch divergence: {command} must run from the checked-out canonical "
                f"branch {canonical_branch} at its current tip; branch={context['branch']}; "
                f"HEAD={context['head']}; canonical_tip={canonical_head}"
            )
        return canonical_branch, canonical_head

    def commit_records(self, transaction: FileTransaction, message: str) -> tuple[str, str]:
        """Commit the administrative paths written by a transaction, with explicit paths only.

        Records live on the canonical branch and Project Control is their author: the commit
        goes through the commit hook like any other. Returns (previous_head, new_head).
        """
        paths = sorted(str(path.relative_to(self.root)) for path in transaction.originals)
        if not paths:
            raise ProjectControlError("nothing to commit for this transition")
        foreign = [path for path in paths if not self.is_administrative_path(path)]
        if foreign:
            raise ProjectControlError(f"transition may only commit administrative paths: {foreign}")
        previous_head = self.repository_context()["head"]
        # Administrative records are Project Control's own: a project's .gitignore does not
        # get to hide them. Without -f, a broad rule such as `*.json` makes `git add` fail
        # AFTER staging the tracked ones, leaving an index the transaction never restored.
        added = self.run_git(["add", "-f", "--", *paths])
        if added.returncode != 0:
            self.run_git(["restore", "--staged", "--", *paths])
            raise ProjectControlError(f"cannot stage records: {added.stderr.strip()}")
        committed = self.run_git(["commit", "-q", "-m", message])
        if committed.returncode != 0:
            self.run_git(["restore", "--staged", "--", *paths])
            raise ProjectControlError(
                f"cannot commit records: {(committed.stdout + committed.stderr).strip()}"
            )
        new_head = self.repository_context()["head"]
        if new_head == previous_head or not SHA40.fullmatch(new_head):
            raise ProjectControlError("records commit did not advance HEAD")
        return previous_head, new_head

    def uncommit_records(self, transaction: FileTransaction, branch: str, previous_head: str, new_head: str) -> list[str]:
        """Undo a records commit made by this transition (the commit becomes unreachable)."""
        errors: list[str] = []
        paths = sorted(str(path.relative_to(self.root)) for path in transaction.originals)
        restored = self.run_git(["update-ref", f"refs/heads/{branch}", previous_head, new_head])
        if restored.returncode != 0:
            errors.append(f"cannot restore {branch} to {previous_head}: {restored.stderr.strip()}")
            return errors
        if paths:
            unstaged = self.run_git(["restore", "--staged", "--", *paths])
            if unstaged.returncode != 0:
                errors.append(f"cannot unstage records: {unstaged.stderr.strip()}")
        try:
            transaction.rollback()
        except Exception as exc:  # pragma: no cover - defensive
            errors.append(f"administrative files: {exc}")
        return errors

    def verify_post_mutation(self) -> None:
        errors = [
            *self.roadmap_errors(),
            *self.project_control_errors(),
            *self.traceability_errors(),
        ]
        if errors:
            raise ProjectControlError("post-mutation verification failed: " + "; ".join(errors))

    def require_lifecycle_decision(
        self,
        item: dict[str, Any],
        reference: str,
        action: str,
        *,
        reason_code: str | None = None,
        resume_condition: str | None = None,
    ) -> str:
        action = action.upper()
        decision_ref = reference.upper()
        if not HUMAN_DECISION_ID.fullmatch(decision_ref):
            raise ProjectControlError("human decision must match HD-NNN")
        if decision_ref in item.get("human_decision_refs", []):
            raise ProjectControlError(
                f"{action} requires a new Human Decision for {item.get('work_item_id')}"
            )
        decisions_text = self.human_decisions.read_text(encoding="utf-8")
        decision_errors = human_decision_errors(decisions_text, decision_ref)
        if decision_errors:
            raise ProjectControlError(
                f"{action} requires an existing valid Human Decision: " + "; ".join(decision_errors)
            )
        if not human_decision_relates_to_work_item(
            decisions_text,
            decision_ref,
            str(item.get("work_item_id")),
        ):
            raise ProjectControlError(
                f"{action} Human Decision {decision_ref} must relate to "
                f"{item.get('work_item_id')}"
            )
        if human_decision_field(
            decisions_text,
            decision_ref,
            "Chosen option",
        ) != "AUTHORIZE":
            raise ProjectControlError(
                f"{action.lower()} Human Decision {decision_ref} must declare "
                "Chosen option: AUTHORIZE"
            )
        declared_action = human_decision_field(
            decisions_text,
            decision_ref,
            "Project Control action",
        )
        if declared_action != action:
            raise ProjectControlError(
                f"{action.lower()} Human Decision {decision_ref} must declare "
                f"Project Control action: {action}"
            )
        if action == "BLOCK":
            if human_decision_field(
                decisions_text,
                decision_ref,
                "Block reason code",
            ) != reason_code:
                raise ProjectControlError(
                    f"block Human Decision {decision_ref} must confirm reason_code={reason_code}"
                )
            if human_decision_field(
                decisions_text,
                decision_ref,
                "Resume condition recorded",
            ) != resume_condition:
                raise ProjectControlError(
                    f"block Human Decision {decision_ref} must record the resume condition"
                )
        elif action == "RESUME":
            if human_decision_field(
                decisions_text,
                decision_ref,
                "Resume condition confirmed",
            ) != resume_condition:
                raise ProjectControlError(
                    f"resume Human Decision {decision_ref} must confirm the exact resume condition"
                )
        return decision_ref

    def canonical_tip(self) -> tuple[str, str]:
        canonical_branch = self.canonical_branch()
        result = self.run_git(
            ["rev-parse", "--verify", f"refs/heads/{canonical_branch}"]
        )
        tip = result.stdout.strip() if result.returncode == 0 else "UNKNOWN"
        if not SHA40.fullmatch(tip):
            raise ProjectControlError(
                f"cannot resolve canonical branch tip: {canonical_branch}"
            )
        return canonical_branch, tip

    def blocked_integration_state(self, item: dict[str, Any]) -> str:
        try:
            canonical_branch, _ = self.canonical_tip()
        except ProjectControlError:
            return "UNMERGED"
        branch = str(item.get("branch", ""))
        branch_exists = self.run_git(
            ["show-ref", "--verify", "--quiet", f"refs/heads/{branch}"]
        ).returncode == 0
        if branch_exists and self.run_git(
            [
                "merge-base",
                "--is-ancestor",
                f"refs/heads/{branch}",
                f"refs/heads/{canonical_branch}",
            ]
        ).returncode == 0:
            return "INTEGRATED"
        return "UNMERGED"

    def merge_in_progress(self) -> bool:
        return self.run_git(["rev-parse", "-q", "--verify", "MERGE_HEAD"]).returncode == 0

    def canonical_administrative_paths(self, canonical_branch: str) -> list[str]:
        listed = self.run_git(
            ["ls-tree", "-r", "--name-only", "-z", canonical_branch, "--", "docs/governance", "project_control"],
            text=False,
        )
        if listed.returncode != 0:
            raise ProjectControlError(f"cannot list canonical records: {listed.stderr.decode('utf-8', 'replace').strip()}")
        paths = [value.decode("utf-8") for value in listed.stdout.split(b"\0") if value]
        return sorted(path for path in paths if self.is_administrative_path(path))

    def merge_canonical_into_branch(
        self,
        branch: str,
        canonical_branch: str,
        work_item_id: str,
        decision_ref: str,
    ) -> str:
        """Align a diverged Work Item branch with the canonical branch by a merge commit.

        Business changes are merged by Git; administrative records are always taken from the
        canonical branch, which is the authority for them at resume time. A conflict on any
        non-administrative path is a business conflict: the merge is aborted and resume refused.
        History is never rewritten: no rebase, no cherry-pick, no reset.
        """
        if self.merge_in_progress():
            raise ProjectControlError("resume refuses to align a branch with a merge already in progress")
        merged = self.run_git(["merge", "--no-ff", "--no-commit", canonical_branch])
        if not self.merge_in_progress():
            raise ProjectControlError(
                f"cannot start alignment merge of {canonical_branch} into {branch}: "
                f"{(merged.stdout + merged.stderr).strip()}"
            )
        try:
            administrative = self.canonical_administrative_paths(canonical_branch)
            if administrative:
                taken = self.run_git(["checkout", canonical_branch, "--", *administrative])
                if taken.returncode != 0:
                    raise ProjectControlError(
                        f"cannot take canonical records during alignment: {taken.stderr.strip()}"
                    )
            unmerged = self.run_git(["diff", "--name-only", "-z", "--diff-filter=U"], text=False)
            if unmerged.returncode != 0:
                raise ProjectControlError("cannot inspect alignment conflicts")
            conflicts = sorted(value.decode("utf-8") for value in unmerged.stdout.split(b"\0") if value)
            if conflicts:
                raise ProjectControlError(
                    "resume refuses to resolve business conflicts between the Work Item branch and "
                    f"{canonical_branch}: {conflicts}; merge {canonical_branch} into {branch} under the "
                    "Work Item's authority, then resume"
                )
            committed = self.run_git([
                "commit", "--no-edit", "-m",
                f"chore(project-control): align {branch} with {canonical_branch} "
                f"for {work_item_id} resume ({decision_ref})",
            ])
            if committed.returncode != 0:
                raise ProjectControlError(
                    f"cannot commit alignment merge: {(committed.stdout + committed.stderr).strip()}"
                )
        except ProjectControlError:
            if self.merge_in_progress():
                self.run_git(["merge", "--abort"])
            raise
        if self.merge_in_progress() or self.changed_paths():
            raise ProjectControlError("alignment merge left the worktree dirty")
        return self.repository_context()["head"]

    def create_work_item(self, args: argparse.Namespace) -> str:
        self.validate_clean_administrative_baseline()
        if self.operating_mode() == "NORMAL_MODE":
            self.require_canonical_checkout("create-work-item")
            self.require_clean_worktree("create-work-item")
        work_item_id = args.work_item_id.upper()
        if not WORK_ITEM_ID.fullmatch(work_item_id):
            raise ProjectControlError("work_item_id must match WI-NNN")
        if self.work_item_by_id(work_item_id) is not None:
            raise ProjectControlError(f"{work_item_id} already exists")

        title = clean_cli_text(args.title, "title")
        objective = clean_cli_text(args.objective, "objective")
        owner = clean_cli_text(args.owner, "owner")
        decision_ref = args.human_decision.upper()
        if not HUMAN_DECISION_ID.fullmatch(decision_ref):
            raise ProjectControlError("human decision must match HD-NNN")
        path_errors = [path for path in args.path if safe_relative_path(path) is None]
        if not args.path or path_errors:
            raise ProjectControlError(f"authorized paths must be safe and non-empty: {path_errors}")
        # The Work Item's evidence directory is always part of its authorized scope: closure
        # reports and artifacts live there and must not need a separate authorization.
        authorized_paths = sorted({*args.path, evidence_directory(work_item_id)})
        dependencies = [value.upper() for value in args.depends_on]
        if any(not WORK_ITEM_ID.fullmatch(value) for value in dependencies):
            raise ProjectControlError("dependencies must match WI-NNN")
        records = {record.get("work_item_id"): record for record in self.records("project_control/work-items")}
        missing_dependencies = [value for value in dependencies if value not in records]
        if missing_dependencies:
            raise ProjectControlError(f"unknown dependencies: {missing_dependencies}")

        context = self.repository_context()
        base_head = args.base_head or context["head"]
        if not SHA40.fullmatch(str(base_head)) or self.run_git(["cat-file", "-e", f"{base_head}^{{commit}}"]).returncode != 0:
            raise ProjectControlError("base_head must identify an existing commit")
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:40] or "work"
        branch = args.branch or f"work/{work_item_id.lower()}-{slug}"
        if (
            not BRANCH_NAME.fullmatch(branch)
            or self.run_git(["check-ref-format", "--branch", branch]).returncode != 0
        ):
            raise ProjectControlError("branch must be a safe dedicated non-canonical branch")
        try:
            canonical = self.canonical_branch()
        except ProjectControlError:
            if self.operating_mode() == "NORMAL_MODE":
                raise
            canonical = None
        if branch in ({canonical} if canonical else {"main", "master"}):
            raise ProjectControlError("Work Item branch must differ from canonical branch")
        if any(record.get("branch") == branch for record in records.values()):
            raise ProjectControlError(f"branch is already declared by another Work Item: {branch}")

        decisions_text = self.human_decisions.read_text(encoding="utf-8")
        decision_exists = bool(re.search(rf"(?m)^## {re.escape(decision_ref)}\s*$", decisions_text))
        if not decision_exists and not args.decision:
            raise ProjectControlError(
                f"{decision_ref} is not recorded; --decision is required to record the human authorization"
            )
        if decision_exists and args.decision:
            raise ProjectControlError(f"{decision_ref} already exists; do not redefine a Human Decision")
        if decision_exists and human_decision_errors(decisions_text, decision_ref):
            raise ProjectControlError(f"{decision_ref} exists but is not a valid Human Decision record: " + "; ".join(human_decision_errors(decisions_text, decision_ref)))

        conversation_ref = args.conversation_ref or f"CONV-{work_item_id}"
        if not RECORD_REFERENCE.fullmatch(conversation_ref):
            raise ProjectControlError("conversation_ref must be a safe provider-agnostic record identifier")
        conversation_path = f"project_control/conversations/{conversation_ref}.json"
        conversation_file = self.root / conversation_path
        if conversation_file.exists():
            conversation = load_json(conversation_file)
            if conversation.get("conversation_ref") != conversation_ref:
                raise ProjectControlError(f"Conversation record mismatch: {conversation_path}")
            related = conversation.get("related_work_items")
            if not isinstance(related, list):
                raise ProjectControlError(f"Conversation record is invalid: {conversation_path}")
            conversation["related_work_items"] = sorted(set([*related, work_item_id]))
            conversation_is_new = False
        else:
            conversation = {
                "$schema": "../schemas/conversation-reference.v1.schema.json",
                "schema_version": "1.0.0",
                "conversation_ref": conversation_ref,
                "provider": clean_cli_text(args.conversation_provider, "conversation_provider"),
                "workspace": args.conversation_workspace,
                "title": clean_cli_text(args.conversation_title or title, "conversation_title"),
                "date": today_iso(),
                "purpose": objective,
                "related_work_items": [work_item_id],
                "external_reference": args.conversation_external_reference,
                "summary_reference": f"docs/governance/HUMAN_DECISIONS.md#{decision_ref}",
            }
            conversation_is_new = True

        project_key = self.project_state().get("project_key")
        applicability = {
            "code": args.code,
            "tests": args.tests,
            "integration": args.integration,
            "deployment": args.deployment,
            "runtime_proof": args.runtime_proof,
        }
        if "UNKNOWN" in applicability.values():
            raise ProjectControlError("create-work-item authorization forbids UNKNOWN applicability")
        item = {
            "$schema": "../schemas/work-item.v1.schema.json",
            "schema_version": "1.0.0",
            "work_item_id": work_item_id,
            "display_reference": display_reference_for(work_item_id, project_key),
            "title": title,
            "objective": objective,
            "owner": owner,
            "status": "AUTHORIZED",
            "human_decision_refs": [decision_ref],
            "conversation_refs": [conversation_ref],
            "agent_run_refs": [],
            "dependencies": dependencies,
            "base_head": base_head,
            "start_head": "UNKNOWN",
            "runtime_target": args.runtime_target,
            "branch": branch,
            "commits": [],
            "block_records": [],
            "authorized_paths": authorized_paths,
            "conflict_gate": args.conflict_gate,
            "direct_impact": [clean_cli_text(value, "direct_impact") for value in args.direct_impact],
            "indirect_impact": [clean_cli_text(value, "indirect_impact") for value in args.indirect_impact],
            "authority_impact": [clean_cli_text(value, "authority_impact") for value in args.authority_impact],
            "concurrent_work_impact": [
                clean_cli_text(value, "concurrent_work_impact") for value in args.concurrent_work_impact
            ],
            "applicability": applicability,
            "development_status": initial_gate_status(applicability["code"]),
            "test_status": initial_gate_status(applicability["tests"]),
            "integration_status": initial_gate_status(applicability["integration"]),
            "deployment_status": initial_gate_status(applicability["deployment"]),
            "runtime_proof_status": initial_gate_status(applicability["runtime_proof"]),
            "evidence": {gate: [] for gate in EVIDENCE_GATES},
            "close_condition": clean_cli_text(args.close_condition, "close_condition"),
        }
        item_errors = validate_work_item(item, project_key)
        if item_errors:
            raise ProjectControlError("invalid Work Item: " + "; ".join(item_errors))

        transaction = FileTransaction(self.root)
        item_path = f"project_control/work-items/{work_item_id}.json"
        try:
            if not decision_exists:
                decision = clean_cli_text(args.decision, "decision")
                authorized_by = clean_cli_text(args.authorized_by or owner, "authorized_by")
                decision_block = (
                    f"\n## {decision_ref}\n\n"
                    f"Date: {today_iso()}\n"
                    f"Decision: {decision}\n"
                    f"Context: Project Control create-work-item request.\n"
                    f"Options considered: AUTHORIZE | REJECT\n"
                    f"Chosen option: AUTHORIZE\n"
                    f"Reason: Explicit human authorization supplied to Project Control.\n"
                    f"Scope: {work_item_id} — {title}\n"
                    f"Reversible: YES\n"
                    f"Conversation reference: {conversation_ref}\n"
                    f"Related ADR: NOT_APPLICABLE\n"
                    f"Related Work Item: {work_item_id}\n"
                    f"Authorized by: {authorized_by}\n"
                )
                transaction.write_text(
                    "docs/governance/HUMAN_DECISIONS.md",
                    decisions_text.rstrip() + "\n" + decision_block,
                )
            transaction.write_json(conversation_path, conversation)
            transaction.write_json(item_path, item)
            self.update_roadmap(transaction, item, "UNMERGED")
            self.update_registry(transaction, item, "DECLARED")
            generated = [item_path]
            if conversation_is_new:
                generated.append(conversation_path)
            self.register_generated_paths(transaction, generated)
            self.verify_post_mutation()
            if self.operating_mode() == "NORMAL_MODE":
                # Records live on the canonical branch; the transition commits them itself.
                self.commit_records(
                    transaction, f"chore(project-control): create {work_item_id} ({decision_ref})",
                )
            transaction.commit()
        except BaseException:
            transaction.rollback()
            raise
        return work_item_id

    def next_agent_run_ref(self, work_item_id: str) -> str:
        prefix = f"RUN-{work_item_id}-"
        numbers = []
        for record in self.records("project_control/agent-runs"):
            ref = str(record.get("agent_run_ref", ""))
            match = re.fullmatch(re.escape(prefix) + r"([0-9]{3})", ref)
            if match:
                numbers.append(int(match.group(1)))
        return f"{prefix}{max(numbers, default=0) + 1:03d}"

    def start_work_item(self, work_item_id: str, planned_paths: Iterable[str], provider: str,
                        authorities_digest: str | None = None) -> str:
        if self.operating_mode() != "NORMAL_MODE":
            raise ProjectControlError("start is available only after bootstrap COMPLETE")
        self.validate_clean_administrative_baseline()
        item = self.work_item_by_id(work_item_id)
        if item is None:
            raise ProjectControlError(f"unknown Work Item: {work_item_id}")
        if item.get("status") != "AUTHORIZED":
            raise ProjectControlError(f"{work_item_id} must be AUTHORIZED, got {item.get('status')}")
        canonical_branch, start_head = self.require_canonical_checkout("start")
        self.require_clean_worktree("start")
        base_head = item.get("base_head")
        if (
            not SHA40.fullmatch(str(base_head or ""))
            or self.run_git(["cat-file", "-e", f"{base_head}^{{commit}}"]).returncode != 0
        ):
            raise ProjectControlError("base_head must identify an existing authorized commit")
        if self.run_git(["merge-base", "--is-ancestor", str(base_head), start_head]).returncode != 0:
            raise ProjectControlError(
                f"invalid authorization ancestry: base_head {base_head} is not an ancestor "
                f"of start_head {start_head}"
            )
        if item.get("start_head") != "UNKNOWN":
            raise ProjectControlError(
                f"{work_item_id} already has start_head={item.get('start_head')}; refusing silent recapture"
            )
        branch = item["branch"]
        if branch == canonical_branch:
            raise ProjectControlError(
                f"declared Work Item branch must differ from canonical branch {canonical_branch}"
            )
        branch_exists = self.run_git(["show-ref", "--verify", "--quiet", f"refs/heads/{branch}"]).returncode == 0
        if branch_exists:
            branch_tip = self.run_git(["rev-parse", "--verify", f"refs/heads/{branch}"])
            if branch_tip.returncode != 0 or branch_tip.stdout.strip() != start_head:
                raise ProjectControlError(
                    f"declared Work Item branch diverges from start_head {start_head}: {branch}"
                )

        # Proof of reading: the agent presents the digest of the current routed authorities.
        authorities = self.require_authorities_digest(item, authorities_digest, "start")
        # Records live on the canonical branch: write and commit them here, then open the branch
        # from the records commit. start_head is the canonical HEAD the transition was run at.
        run_ref = self.next_agent_run_ref(work_item_id)
        run_path = f"project_control/agent-runs/{run_ref}.json"
        item = dict(item)
        item["status"] = "IN_PROGRESS"
        item["start_head"] = start_head
        item["agent_run_refs"] = [*item.get("agent_run_refs", []), run_ref]
        run = {
            "$schema": "../schemas/agent-run.v1.schema.json",
            "schema_version": "1.0.0",
            "agent_run_ref": run_ref,
            "provider": clean_cli_text(provider, "agent_provider"),
            "work_item_id": work_item_id,
            "requested_scope": item["authorized_paths"],
            "base_head": item["base_head"],
            "start_head": start_head,
            "branch": branch,
            "started_at": now_iso(),
            "completed_at": None,
            "result": "IN_PROGRESS",
            "commits": [],
            "report_reference": None,
            "authorities_read": authorities,
        }
        transaction = FileTransaction(self.root)
        committed: tuple[str, str] | None = None
        created_branch = False
        advanced_existing_branch = False

        def restore_git_state() -> list[str]:
            rollback_errors: list[str] = []
            current = self.repository_context()["branch"]
            if current != canonical_branch:
                restored = self.run_git(["switch", canonical_branch])
                if restored.returncode != 0:
                    rollback_errors.append(
                        f"cannot restore canonical branch {canonical_branch}: {restored.stderr.strip()}"
                    )
                    return rollback_errors
            if created_branch:
                deleted = self.run_git(["branch", "-D", branch])
                if deleted.returncode != 0:
                    rollback_errors.append(
                        f"cannot remove transaction-created branch {branch}: {deleted.stderr.strip()}"
                    )
            elif advanced_existing_branch and committed is not None:
                restored_ref = self.run_git(["update-ref", f"refs/heads/{branch}", committed[0], committed[1]])
                if restored_ref.returncode != 0:
                    rollback_errors.append(f"cannot restore branch tip {branch}: {restored_ref.stderr.strip()}")
            if committed is not None:
                rollback_errors.extend(self.uncommit_records(transaction, canonical_branch, *committed))
            else:
                try:
                    transaction.rollback()
                except BaseException as rollback_error:
                    rollback_errors.append(f"administrative files: {rollback_error}")
            return rollback_errors

        try:
            transaction.write_json(f"project_control/work-items/{work_item_id}.json", item)
            transaction.write_json(run_path, run)
            self.update_roadmap(transaction, item, "ACTIVE_WORK")
            self.update_registry(transaction, item, "ACTIVE")
            self.register_generated_paths(transaction, [run_path])
            self.verify_post_mutation()
            findings = self.preflight_findings(
                work_item_id, planned_paths, start_head_override=start_head, expected_branch=canonical_branch,
            )
            failures = [f"{finding.check}: {finding.detail}" for finding in findings if finding.status == "FAIL"]
            if failures:
                raise ProjectControlError("start preflight failed: " + "; ".join(failures))
            committed = self.commit_records(transaction, f"chore(project-control): start {work_item_id}")
            if branch_exists:
                advanced = self.run_git(["update-ref", f"refs/heads/{branch}", committed[1], committed[0]])
                if advanced.returncode != 0:
                    raise ProjectControlError(f"cannot fast-forward declared branch {branch}: {advanced.stderr.strip()}")
                advanced_existing_branch = True
                switched = self.run_git(["switch", branch])
            else:
                switched = self.run_git(["switch", "-c", branch])
                created_branch = switched.returncode == 0
            if switched.returncode != 0:
                raise ProjectControlError(f"cannot checkout declared branch {branch}: {switched.stderr.strip()}")
            post_findings = self.preflight_findings(work_item_id, planned_paths)
            post_failures = [
                f"{finding.check}: {finding.detail}"
                for finding in post_findings
                if finding.status == "FAIL"
            ]
            if post_failures:
                raise ProjectControlError("post-start preflight failed: " + "; ".join(post_failures))
            transaction.commit()
        except BaseException as exc:
            rollback_errors = restore_git_state()
            if rollback_errors:
                raise ProjectControlError(
                    f"start failed: {exc}; ROLLBACK FAILED: {'; '.join(rollback_errors)}"
                ) from exc
            raise
        return run_ref

    def block_work_item(self, work_item_id: str, args: argparse.Namespace) -> None:
        if self.operating_mode() != "NORMAL_MODE":
            raise ProjectControlError("block is available only in NORMAL_MODE")
        self.validate_clean_administrative_baseline()
        canonical_branch, _ = self.require_canonical_checkout("block")
        self.require_clean_worktree("block")
        item = self.work_item_by_id(work_item_id)
        if item is None:
            raise ProjectControlError(f"unknown Work Item: {work_item_id}")
        previous_status = item.get("status")
        if previous_status not in {"AUTHORIZED", "IN_PROGRESS"}:
            raise ProjectControlError(
                f"{work_item_id} is not blockable from status {previous_status}"
            )
        reason_code = clean_cli_text(args.reason_code, "reason_code")
        if not REASON_CODE.fullmatch(reason_code):
            raise ProjectControlError(
                "reason_code must be machine-readable uppercase snake case"
            )
        resume_condition = clean_cli_text(
            args.resume_condition,
            "resume_condition",
        )
        decision_ref = self.require_lifecycle_decision(
            item,
            args.human_decision,
            "BLOCK",
            reason_code=reason_code,
            resume_condition=resume_condition,
        )
        blocked_run_ref: str | None = None
        blocked_run_path: str | None = None
        blocked_run: dict[str, Any] | None = None
        if previous_status == "IN_PROGRESS":
            run_refs = item.get("agent_run_refs", [])
            if not run_refs:
                raise ProjectControlError(
                    f"{work_item_id} IN_PROGRESS requires an Agent Run to block"
                )
            blocked_run_ref = str(run_refs[-1])
            blocked_run_path = (
                f"project_control/agent-runs/{blocked_run_ref}.json"
            )
            path = self.root / blocked_run_path
            if not path.is_file():
                raise ProjectControlError(f"missing Agent Run: {blocked_run_ref}")
            blocked_run = load_json(path)
            if blocked_run.get("result") not in {"IN_PROGRESS", "PARTIAL"}:
                raise ProjectControlError(
                    f"latest Agent Run {blocked_run_ref} is not blockable from "
                    f"result {blocked_run.get('result')}"
                )
        candidate = json.loads(json.dumps(item))
        block_records = candidate.setdefault("block_records", [])
        if not isinstance(block_records, list):
            raise ProjectControlError("block_records must be a list")
        if any(
            isinstance(record, dict) and record.get("resolved_at") is None
            for record in block_records
        ):
            raise ProjectControlError("an unresolved external dependency already exists")
        blocked_at = now_iso()
        block_records.append(
            {
                "type": "EXTERNAL_DEPENDENCY",
                "reason_code": reason_code,
                "blocked_at": blocked_at,
                "human_decision_id": decision_ref,
                "agent_run_ref": blocked_run_ref,
                "resume_condition": resume_condition,
                "resolved_at": None,
                "resolution_human_decision_id": None,
            }
        )
        candidate["human_decision_refs"] = [
            *candidate.get("human_decision_refs", []),
            decision_ref,
        ]
        candidate["status"] = "BLOCKED"
        item_errors = validate_work_item(
            candidate,
            self.project_state().get("project_key"),
            self.canonical_branch(),
        )
        if item_errors:
            raise ProjectControlError("block refused: " + "; ".join(item_errors))

        transaction = FileTransaction(self.root)
        try:
            if blocked_run is not None and blocked_run_path is not None:
                blocked_run["result"] = "BLOCKED"
                blocked_run["completed_at"] = (
                    blocked_run.get("completed_at") or blocked_at
                )
                blocked_run["report_reference"] = (
                    blocked_run.get("report_reference")
                    or f"project_control/work-items/{work_item_id}.json"
                )
                transaction.write_json(blocked_run_path, blocked_run)
            transaction.write_json(
                f"project_control/work-items/{work_item_id}.json",
                candidate,
            )
            self.update_roadmap(
                transaction,
                candidate,
                self.blocked_integration_state(candidate),
            )
            self.update_registry(transaction, candidate, "BLOCKED")
            self.verify_post_mutation()
            failures = [
                f"{finding.check}: {finding.detail}"
                for finding in self.audit_findings()
                if finding.status == "FAIL"
            ]
            if failures:
                raise ProjectControlError("post-block audit failed: " + "; ".join(failures))
            self.commit_records(
                transaction, f"chore(project-control): block {work_item_id} ({decision_ref})",
            )
            transaction.commit()
        except BaseException:
            transaction.rollback()
            raise

    def resume_work_item(
        self,
        work_item_id: str,
        planned_paths: Iterable[str],
        provider: str,
        human_decision: str,
        authorities_digest: str | None = None,
    ) -> str:
        if self.operating_mode() != "NORMAL_MODE":
            raise ProjectControlError("resume is available only in NORMAL_MODE")
        self.validate_clean_administrative_baseline()
        changed_paths = self.changed_paths()
        if changed_paths:
            raise ProjectControlError(
                f"resume requires a clean worktree before branch alignment: {changed_paths}"
            )
        item = self.work_item_by_id(work_item_id)
        if item is None:
            raise ProjectControlError(f"unknown Work Item: {work_item_id}")
        if item.get("status") != "BLOCKED":
            raise ProjectControlError(
                f"{work_item_id} must be BLOCKED, got {item.get('status')}"
            )
        block_records = item.get("block_records", [])
        unresolved_indexes = [
            index
            for index, record in enumerate(block_records)
            if isinstance(record, dict) and record.get("resolved_at") is None
        ]
        if unresolved_indexes != [len(block_records) - 1]:
            raise ProjectControlError(
                "resume requires exactly one latest unresolved external dependency"
            )
        resume_condition = str(block_records[unresolved_indexes[0]]["resume_condition"])
        decision_ref = self.require_lifecycle_decision(
            item,
            human_decision,
            "RESUME",
            resume_condition=resume_condition,
        )
        path_errors = normal_path_errors(planned_paths, item.get("authorized_paths", []))
        if path_errors:
            raise ProjectControlError("resume paths refused: " + "; ".join(path_errors))
        records = {
            record.get("work_item_id"): record
            for record in self.records("project_control/work-items")
        }
        other_active = [
            identifier
            for identifier, record in records.items()
            if identifier != work_item_id and record.get("status") == "IN_PROGRESS"
        ]
        if other_active:
            raise ProjectControlError(
                f"resume requires no other active Work Item: {other_active}"
            )

        provider = clean_cli_text(provider, "agent_provider")
        context = self.repository_context()
        original_branch = context["branch"]
        canonical_branch, resume_head = self.canonical_tip()
        if original_branch != canonical_branch or context["head"] != resume_head:
            raise ProjectControlError(
                "canonical branch divergence: resume must run from the checked-out "
                f"canonical branch {canonical_branch} at its current tip; "
                f"branch={original_branch}; HEAD={context['head']}; "
                f"canonical_tip={resume_head}"
            )
        base_head = item.get("base_head")
        if (
            not SHA40.fullmatch(str(base_head or ""))
            or self.run_git(["cat-file", "-e", f"{base_head}^{{commit}}"]).returncode != 0
            or self.run_git(
                ["merge-base", "--is-ancestor", str(base_head), resume_head]
            ).returncode != 0
        ):
            raise ProjectControlError(
                f"invalid resume ancestry: base_head {base_head} is not an ancestor "
                f"of canonical head {resume_head}"
            )
        branch = str(item.get("branch", ""))
        if branch == canonical_branch:
            raise ProjectControlError(
                f"declared Work Item branch must differ from canonical branch {canonical_branch}"
            )
        branch_exists = self.run_git(
            ["show-ref", "--verify", "--quiet", f"refs/heads/{branch}"]
        ).returncode == 0
        historical_commits = set(item.get("commits", []))
        for historical_run_ref in item.get("agent_run_refs", []):
            historical_run_path = (
                self.root
                / "project_control/agent-runs"
                / f"{historical_run_ref}.json"
            )
            if not historical_run_path.is_file():
                raise ProjectControlError(
                    f"missing historical Agent Run: {historical_run_ref}"
                )
            historical_run = load_json(historical_run_path)
            historical_commits.update(historical_run.get("commits", []))
        never_started = bool(
            not item.get("agent_run_refs")
            and item.get("start_head") == "UNKNOWN"
            and not historical_commits
        )
        old_branch_tip: str | None = None
        if branch_exists:
            result = self.run_git(["rev-parse", "--verify", f"refs/heads/{branch}"])
            old_branch_tip = result.stdout.strip() if result.returncode == 0 else None
            if old_branch_tip is None or not SHA40.fullmatch(old_branch_tip):
                raise ProjectControlError(f"cannot resolve declared Work Item branch: {branch}")
            if never_started and old_branch_tip != resume_head:
                raise ProjectControlError(
                    "resume refuses a pre-existing branch away from the canonical head "
                    "for a Work Item blocked before its first Agent Run"
                )
            for commit in sorted(historical_commits):
                if (
                    not SHA40.fullmatch(str(commit))
                    or self.run_git(["cat-file", "-e", f"{commit}^{{commit}}"]).returncode != 0
                    or self.run_git(
                        ["merge-base", "--is-ancestor", str(commit), old_branch_tip]
                    ).returncode != 0
                ):
                    raise ProjectControlError(
                        "historical Work Item or Agent Run commit is not preserved "
                        f"by branch {branch}: {commit}"
                    )
        elif not never_started:
            raise ProjectControlError(
                "resume refuses to recreate a missing branch for a previously started Work Item"
            )

        candidate = json.loads(json.dumps(item))
        resolved_at = now_iso()
        candidate["block_records"][-1]["resolved_at"] = resolved_at
        candidate["block_records"][-1]["resolution_human_decision_id"] = decision_ref
        candidate["human_decision_refs"] = [
            *candidate.get("human_decision_refs", []),
            decision_ref,
        ]
        candidate["status"] = "IN_PROGRESS"
        if candidate.get("start_head") == "UNKNOWN":
            candidate["start_head"] = resume_head
        run_ref = self.next_agent_run_ref(work_item_id)
        candidate["agent_run_refs"] = [
            *candidate.get("agent_run_refs", []),
            run_ref,
        ]
        item_errors = validate_work_item(
            candidate,
            self.project_state().get("project_key"),
            canonical_branch,
        )
        if item_errors:
            raise ProjectControlError("resume refused: " + "; ".join(item_errors))

        authorities = self.require_authorities_digest(candidate, authorities_digest, "resume")
        run_path = f"project_control/agent-runs/{run_ref}.json"
        run = {
            "$schema": "../schemas/agent-run.v1.schema.json",
            "schema_version": "1.0.0",
            "agent_run_ref": run_ref,
            "provider": provider,
            "work_item_id": work_item_id,
            "requested_scope": candidate["authorized_paths"],
            "base_head": candidate["base_head"],
            "start_head": resume_head,
            "branch": branch,
            "started_at": resolved_at,
            "completed_at": None,
            "result": "IN_PROGRESS",
            "commits": [],
            "report_reference": None,
            "authorities_read": authorities,
        }
        transaction = FileTransaction(self.root)
        committed: tuple[str, str] | None = None
        created_branch = False
        advanced_branch_tip: str | None = None
        self.last_alignment = {"mode": "NONE", "commit": None}

        def restore_git_state() -> list[str]:
            rollback_errors: list[str] = []
            if self.merge_in_progress():
                aborted = self.run_git(["merge", "--abort"])
                if aborted.returncode != 0:
                    rollback_errors.append(f"cannot abort alignment merge: {aborted.stderr.strip()}")
                    return rollback_errors
            current_branch = self.repository_context()["branch"]
            if current_branch != original_branch:
                restored = self.run_git(["switch", original_branch])
                if restored.returncode != 0:
                    rollback_errors.append(
                        f"cannot restore original branch {original_branch}: {restored.stderr.strip()}"
                    )
                    return rollback_errors
            if created_branch:
                deleted = self.run_git(["branch", "-D", branch])
                if deleted.returncode != 0:
                    rollback_errors.append(
                        f"cannot remove transaction-created branch {branch}: {deleted.stderr.strip()}"
                    )
            elif old_branch_tip is not None and advanced_branch_tip is not None:
                restored_ref = self.run_git(
                    ["update-ref", f"refs/heads/{branch}", old_branch_tip, advanced_branch_tip]
                )
                if restored_ref.returncode != 0:
                    rollback_errors.append(
                        f"cannot restore branch tip {branch}: {restored_ref.stderr.strip()}"
                    )
            if committed is not None:
                rollback_errors.extend(self.uncommit_records(transaction, canonical_branch, *committed))
            else:
                try:
                    transaction.rollback()
                except BaseException as rollback_error:
                    rollback_errors.append(f"administrative files: {rollback_error}")
            return rollback_errors

        try:
            # 1. Records are written and committed on the canonical branch.
            transaction.write_json(f"project_control/work-items/{work_item_id}.json", candidate)
            transaction.write_json(run_path, run)
            self.update_roadmap(transaction, candidate, "ACTIVE_WORK")
            self.update_registry(transaction, candidate, "ACTIVE")
            self.register_generated_paths(transaction, [run_path])
            self.verify_post_mutation()
            findings = self.preflight_findings(
                work_item_id, planned_paths, start_head_override=resume_head, expected_branch=canonical_branch,
            )
            failures = [f"{finding.check}: {finding.detail}" for finding in findings if finding.status == "FAIL"]
            if failures:
                raise ProjectControlError("resume preflight failed: " + "; ".join(failures))
            committed = self.commit_records(
                transaction, f"chore(project-control): resume {work_item_id} ({decision_ref})",
            )
            # 2. The Work Item branch is aligned with the canonical tip, never rewritten.
            if branch_exists:
                switched = self.run_git(["switch", branch])
            else:
                switched = self.run_git(["switch", "-c", branch, committed[1]])
                created_branch = switched.returncode == 0
            if switched.returncode != 0:
                raise ProjectControlError(
                    f"cannot checkout declared Work Item branch {branch}: {switched.stderr.strip()}"
                )
            if branch_exists:
                branch_behind = self.run_git(["merge-base", "--is-ancestor", "HEAD", canonical_branch]).returncode == 0
                if branch_behind:
                    merged = self.run_git(["merge", "--ff-only", canonical_branch])
                    if merged.returncode != 0:
                        raise ProjectControlError(
                            f"cannot fast-forward declared Work Item branch: {merged.stderr.strip()}"
                        )
                    self.last_alignment = {"mode": "FAST_FORWARD", "commit": self.repository_context()["head"]}
                else:
                    self.merge_canonical_into_branch(branch, canonical_branch, work_item_id, decision_ref)
                    self.last_alignment = {"mode": "MERGE", "commit": self.repository_context()["head"]}
                advanced_branch_tip = self.repository_context()["head"]
            # 3. Preflight on the aligned branch is the final gate.
            post_findings = self.preflight_findings(
                work_item_id, planned_paths, start_head_override=resume_head,
            )
            post_failures = [
                f"{finding.check}: {finding.detail}" for finding in post_findings if finding.status == "FAIL"
            ]
            if post_failures:
                raise ProjectControlError("post-resume preflight failed: " + "; ".join(post_failures))
            transaction.commit()
        except BaseException as exc:
            rollback_errors = restore_git_state()
            if rollback_errors:
                raise ProjectControlError(
                    f"resume failed: {exc}; ROLLBACK FAILED: {'; '.join(rollback_errors)}"
                ) from exc
            raise
        return run_ref

    def evidence_file(self, value: str, work_item_id: str, baseline: str) -> tuple[str, bytes]:
        path = safe_relative_path(value)
        prefix = f"reports/evidence/{work_item_id}/"
        if path is None or path != value or not path.startswith(prefix):
            raise ProjectControlError(f"evidence path must be inside {prefix}: {value}")
        local = self.root / path
        if not local.resolve().is_relative_to(self.root) or not local.is_file() or local.is_symlink():
            raise ProjectControlError(f"missing or unsafe evidence file: {path}")
        content = local.read_bytes()
        tracked = self.run_git(["show", f"{baseline}:{path}"], text=False)
        if tracked.returncode != 0 or tracked.stdout != content:
            raise ProjectControlError(f"evidence must be committed and unchanged at {baseline}: {path}")
        if not content:
            raise ProjectControlError(f"empty evidence file: {path}")
        history = self.run_git([
            "log", "--full-history", "--simplify-merges", "--format=%H", "-2", baseline, "--", path,
        ])
        if history.returncode != 0 or len(history.stdout.splitlines()) != 1:
            raise ProjectControlError(f"evidence is immutable after its first commit; use a new path: {path}")
        return path, content

    def validate_evidence(self, item: dict[str, Any], gate: str, reference: str, baseline: str,
                          require_pass: bool = True) -> dict[str, Any]:
        """Check recorded claims and their artifacts, not independently observe a runtime."""
        if not SHA40.fullmatch(str(baseline)) or self.run_git(["cat-file", "-e", f"{baseline}^{{commit}}"]).returncode != 0:
            raise ProjectControlError("evidence baseline must be an existing commit")
        path, content = self.evidence_file(reference, item["work_item_id"], baseline)
        try:
            evidence = json.loads(content)
        except (ValueError, UnicodeError) as exc:
            raise ProjectControlError(f"invalid evidence JSON: {path}") from exc
        errors = core_schema_errors(evidence, "evidence")
        if errors:
            raise ProjectControlError("invalid evidence: " + "; ".join(errors))
        expected = {"work_item_id": item["work_item_id"], "gate": gate,
                    "runtime_target": item["runtime_target"],
                    "level": gate_levels(item["runtime_target"])[gate]}
        for key, value in expected.items():
            if evidence[key] != value:
                raise ProjectControlError(f"evidence {path}: {key} must be {value}")
        if require_pass and evidence["result"] != "PASS":
            raise ProjectControlError(f"evidence {path}: result must be PASS, got {evidence['result']}")
        try:
            recorded = datetime.fromisoformat(evidence["recorded_at"].replace("Z", "+00:00"))
            if recorded.tzinfo is None or recorded > datetime.now(timezone.utc):
                raise ValueError("missing timezone or future date")
        except ValueError as exc:
            raise ProjectControlError(
                f"evidence {path}: recorded_at must be a past ISO timestamp carrying a timezone, "
                "for example 2026-01-31T14:05:00+01:00"
            ) from exc
        subject = evidence["subject_commit"]
        start = self.latest_run_start_head(item) if require_pass else item.get("start_head")
        if not SHA40.fullmatch(str(start)):
            raise ProjectControlError("evidence requires a started Work Item")
        if self.run_git(["merge-base", "--is-ancestor", start, subject]).returncode != 0 or self.run_git(["merge-base", "--is-ancestor", subject, baseline]).returncode != 0:
            raise ProjectControlError(f"evidence {path}: subject_commit must be between start_head and the closure baseline")
        read: list[tuple[str, str | None]] = []
        for artifact in evidence["artifacts"]:
            _, data = self.evidence_file(artifact["path"], item["work_item_id"], baseline)
            if artifact["path"] == path or hashlib.sha256(data).hexdigest() != artifact["sha256"]:
                raise ProjectControlError(f"evidence {path}: artifact hash mismatch: {artifact['path']}")
            if is_text_artifact(data):
                read.append((artifact["path"], failure_marker_in(data)))
        if evidence["result"] == "PASS" and read and all(marker for _, marker in read):
            failing = ", ".join(f"{name} ({marker!r})" for name, marker in read)
            raise ProjectControlError(
                f"evidence {path}: result is PASS but every text artifact it cites reports a failure: {failing}. "
                "Cite the output of the run that passed; a run that failed keeps its place beside it, or is "
                "recorded as its own evidence with result FAIL, which the history keeps"
            )
        changed = self.run_git(["diff", "--name-only", "-z", subject, baseline], text=False)
        if changed.returncode != 0:
            raise ProjectControlError(f"cannot compare evidence subject_commit: {subject}")
        paths = [v.decode("utf-8") for v in changed.stdout.split(b"\0") if v]
        stale = [v for v in paths if not self.is_administrative_path(v) and not v.startswith(f"reports/evidence/{item['work_item_id']}/")]
        if stale and require_pass:
            raise ProjectControlError(f"stale evidence {path}: changed since subject_commit: {stale}")
        return evidence

    def latest_run_start_head(self, item: dict[str, Any]) -> str:
        """A successful proof must cover the current execution, including after resume."""
        refs = item.get("agent_run_refs", [])
        if not refs:
            return str(item.get("start_head", "UNKNOWN"))
        ref = refs[-1]
        if not AGENT_RUN_REFERENCE.fullmatch(str(ref)):
            raise ProjectControlError("invalid latest Agent Run reference")
        run = load_json(self.root / f"project_control/agent-runs/{ref}.json")
        if run.get("work_item_id") != item["work_item_id"]:
            raise ProjectControlError("latest Agent Run must belong to the Work Item")
        return str(run.get("start_head", "UNKNOWN"))

    # --- Adoption baseline ("legacy_baseline"): history is frozen at a declared commit, ---
    # --- the current contract applies to everything after it; nothing is reconstructed. ---

    @staticmethod
    def require_baseline_named(decisions_text: str, kind: str, head: str, decision: str) -> None:
        """The decision a baseline cites must name that very commit.

        The controller used to check that a baseline points at a commit that exists and that a
        structured decision accompanies it — never that *that* decision speaks of *that* commit.
        So a decision recorded for line A could be cited to declare line B: the history behind
        the old line rewritten, then refrozen, all through the governed path (third independent
        control, P17). A declaration is refused unless its decision carries the commit, in the
        field named for its kind; a baseline moves only on a decision that says where."""
        field = BASELINE_DECISION_FIELDS[kind][0]
        chosen = human_decision_field_values(decisions_text, decision, "Chosen option") or []
        if len(chosen) > 1:
            # Written twice — REJECT twice, in the case the fifth independent control executed —
            # the field read as a single value was None, which is not REJECT, and the refusal
            # passed for a choice. A decision chooses once; two lines choose nothing.
            raise ProjectControlError(
                f"{kind.replace('_', ' ')} {head} cites {decision}, whose `Chosen option` is written "
                f"{len(chosen)} times ({', '.join(chosen)}): a decision chooses once, and this one declares nothing"
            )
        if chosen and chosen[0].upper() == "REJECT":
            raise ProjectControlError(
                f"{kind.replace('_', ' ')} {head} cites {decision}, a rejected decision: a refusal declares nothing"
            )
        named = human_decision_field(decisions_text, decision, field)
        if named != head:
            label = kind.replace("_", " ")
            raise ProjectControlError(
                f"{label} {head} is not named by its Human Decision {decision}: a baseline is declared "
                f"by a decision that carries `{field}: {head}` exactly once"
                + (f" (it names {named})" if named else "")
            )

    def legacy_baseline(self) -> tuple[str, str] | None:
        """The declared adoption baseline (commit, Human Decision); never inferred from HEAD."""
        declared = self.project_state().get("legacy_baseline")
        if declared is None:
            return None
        if not isinstance(declared, dict):
            raise ProjectControlError("legacy_baseline must be null or an object")
        head = str(declared.get("head", ""))
        decision = str(declared.get("human_decision_ref", ""))
        if not SHA40.fullmatch(head):
            raise ProjectControlError("legacy baseline head must be a 40-character commit")
        if (
            self.run_git(["cat-file", "-e", f"{head}^{{commit}}"]).returncode != 0
            or self.run_git(["merge-base", "--is-ancestor", head, "HEAD"]).returncode != 0
        ):
            raise ProjectControlError(f"legacy baseline {head} is missing or not in current history")
        try:
            decisions_text = self.human_decisions.read_text(encoding="utf-8")
        except OSError as exc:
            raise ProjectControlError(f"cannot read Human Decisions: {exc}") from exc
        if not HUMAN_DECISION_ID.fullmatch(decision) or not human_decision_is_valid(decisions_text, decision, as_mandate=False):
            raise ProjectControlError(f"legacy baseline requires a recorded Human Decision: {decision}")
        self.require_baseline_named(decisions_text, "legacy_baseline", head, decision)
        return head, decision

    def frozen_decision_refs(self) -> set[str]:
        """Human Decisions recorded at the adoption baseline whose text has not changed since.

        A rule that arrives with a controller upgrade judges the work that follows it. The
        doctrine promises that the closures frozen at the adoption baseline are neither
        reconstructed nor requalified, so the vocabulary of a decision recorded before that
        commit is read as it was written: the audit still requires its `Decision`, its
        `Authorized by` and, where it leaves the granted folder, its two confirmations — only
        the `Chosen option: AUTHORIZE` wording introduced later is not demanded of it.

        The exemption follows the state, not the name: a decision whose block has been
        rewritten since the baseline is read under the current rule like any other. Blank lines
        around a block are not part of it — the last decision of a file runs to its end, and
        recording a later decision must not, by itself, revoke an exemption.

        Nothing here relaxes a transition performed today: `create-work-item`, `block`,
        `resume` and `close` read their mandate in full, so a recorded refusal can never
        authorize new work."""
        try:
            baseline = self.legacy_baseline()
        except ProjectControlError:
            # An invalid declaration is reported by LEGACY_RECORDS_PRESENT; here it simply
            # grants no exemption.
            return set()
        if baseline is None:
            return set()
        shown = self.run_git(["show", f"{baseline[0]}:{HUMAN_DECISIONS_PATH}"])
        if shown.returncode != 0:
            raise ProjectControlError(
                f"cannot read {HUMAN_DECISIONS_PATH} at the adoption baseline {baseline[0]}"
            )
        try:
            current_text = self.human_decisions.read_text(encoding="utf-8")
        except OSError as exc:
            raise ProjectControlError(f"cannot read Human Decisions: {exc}") from exc
        frozen: set[str] = set()
        for reference in re.findall(r"(?m)^## (HD-[0-9]{3,})\s*$", shown.stdout):
            recorded = decision_block(shown.stdout, reference)
            current = decision_block(current_text, reference)
            if recorded is not None and current is not None and recorded.strip() == current.strip():
                frozen.add(reference)
        return frozen

    def authorities_baseline(self) -> tuple[str, str] | None:
        """The declared proof-of-reading baseline (commit, Human Decision); never inferred from HEAD.

        A project that adopts the proof of reading (skeleton 3.6+) with Agent Runs already recorded
        after its adoption baseline declares the commit at which those runs are frozen: they stay
        valid without authorities_read, every later Agent Run carries the proof."""
        declared = self.project_state().get("authorities_baseline")
        if declared is None:
            return None
        if not isinstance(declared, dict):
            raise ProjectControlError("authorities_baseline must be null or an object")
        head = str(declared.get("head", ""))
        decision = str(declared.get("human_decision_ref", ""))
        if not SHA40.fullmatch(head):
            raise ProjectControlError("authorities baseline head must be a 40-character commit")
        if (
            self.run_git(["cat-file", "-e", f"{head}^{{commit}}"]).returncode != 0
            or self.run_git(["merge-base", "--is-ancestor", head, "HEAD"]).returncode != 0
        ):
            raise ProjectControlError(f"authorities baseline {head} is missing or not in current history")
        try:
            decisions_text = self.human_decisions.read_text(encoding="utf-8")
        except OSError as exc:
            raise ProjectControlError(f"cannot read Human Decisions: {exc}") from exc
        if not HUMAN_DECISION_ID.fullmatch(decision) or not human_decision_is_valid(decisions_text, decision, as_mandate=False):
            raise ProjectControlError(f"authorities baseline requires a recorded Human Decision: {decision}")
        self.require_baseline_named(decisions_text, "authorities_baseline", head, decision)
        return head, decision

    def language(self) -> str:
        """The language the controller speaks to the Project Owner in: FR, EN, or UNKNOWN.

        It governs the prose addressed to a human — `status` and the roadmap view. Check names,
        report lines and refusal messages stay in English: they are identifiers, not text, and
        the tests, the commit gate and any tool reading the output rely on them being stable."""
        try:
            value = self.project_state().get("language", "UNKNOWN")
        except (OSError, json.JSONDecodeError, ProjectControlError):
            return "UNKNOWN"
        return str(value) if value in LANGUAGES or value == "UNKNOWN" else f"INVALID({value})"

    def speech(self) -> str:
        """The language to write in right now: FR while the choice has not been made."""
        chosen = self.language()
        return chosen if chosen in LANGUAGES else "FR"

    def reporting_style(self) -> str:
        """How the Project Owner wants to be reported to: TECHNICAL, PLAIN, or UNKNOWN (not chosen yet)."""
        try:
            value = self.project_state().get("reporting_style", "UNKNOWN")
        except (OSError, json.JSONDecodeError, ProjectControlError):
            return "UNKNOWN"
        return str(value) if value in REPORTING_STYLES or value == "UNKNOWN" else f"INVALID({value})"

    def authorities_baseline_audit(self) -> tuple[str, list[str]]:
        """Summary and errors of the proof-of-reading baseline declaration; fail closed."""
        try:
            baseline = self.authorities_baseline()
            if baseline is None:
                return "no authorities baseline declared", []
            declared = self.agent_run_blobs_at(baseline[0], "authorities baseline")
            exempt = self.unchanged_agent_runs_at(baseline[0], "authorities baseline")
        except (ProjectControlError, OSError, ValueError) as exc:
            return str(exc), [str(exc)]
        # A run rewritten since the baseline is no longer the history that was frozen. Saying so
        # is only useful when it still lacks the proof: one that acknowledged its authorities
        # since simply no longer needs the exemption.
        rewritten = sorted(
            identifier for identifier in set(declared) - exempt
            if not self.agent_run_has_authorities_read(identifier)
        )
        summary = f"{len(exempt)} Agent Run(s) exempt from authorities_read at {baseline[0]}"
        if rewritten:
            summary += f"; no longer historical, proof of reading required: {rewritten}"
        return summary, []

    def legacy_records(self) -> dict[str, tuple[bytes, dict[str, Any]]]:
        """Work Item records exactly as committed at the adoption baseline, by identifier."""
        baseline = self.legacy_baseline()
        if baseline is None:
            return {}
        head = baseline[0]
        cached = getattr(self, "_legacy_records", None)
        if cached is not None and cached[0] == head:
            return cached[1]
        listing = self.run_git(["ls-tree", "-r", "--name-only", "-z", head, "--", "project_control/work-items"], text=False)
        if listing.returncode != 0:
            raise ProjectControlError(f"cannot read legacy baseline {head}")
        records: dict[str, tuple[bytes, dict[str, Any]]] = {}
        for path in (entry.decode("utf-8", "surrogateescape") for entry in listing.stdout.split(b"\0") if entry):
            if not path.endswith(".json"):
                continue
            blob = self.run_git(["show", f"{head}:{path}"], text=False)
            if blob.returncode != 0:
                raise ProjectControlError(f"cannot read legacy Work Item: {path}")
            try:
                record = json.loads(blob.stdout)
            except ValueError as exc:
                raise ProjectControlError(f"invalid legacy Work Item JSON: {path}") from exc
            identifier = record.get("work_item_id") if isinstance(record, dict) else None
            if not isinstance(identifier, str) or path != f"project_control/work-items/{identifier}.json":
                raise ProjectControlError(f"legacy Work Item path/identity mismatch: {path}")
            records[identifier] = (blob.stdout, record)
        self._legacy_records = (head, records)
        return records

    def legacy_record(self, item: dict[str, Any]) -> dict[str, Any] | None:
        entry = self.legacy_records().get(str(item.get("work_item_id")))
        return entry[1] if entry else None

    def legacy_evidence_prefixes(self, item: dict[str, Any]) -> dict[str, list[str]]:
        """Evidence recorded before the baseline stays an unchanged prefix of each gate history."""
        original = self.legacy_record(item)
        original_evidence = original.get("evidence", {}) if original else {}
        prefixes = {
            gate: list(original_evidence.get(gate, [])) if isinstance(original_evidence, dict) else []
            for gate in EVIDENCE_GATES
        }
        evidence = item.get("evidence")
        for gate, prefix in prefixes.items():
            current = evidence.get(gate) if isinstance(evidence, dict) else None
            if not isinstance(current, list) or current[:len(prefix)] != prefix:
                raise ProjectControlError(f"{item.get('work_item_id')}: legacy {gate} evidence history changed")
        return prefixes

    def legacy_audit(self) -> tuple[str, list[str], list[str]]:
        """Summary, LEGACY_RECORDS_PRESENT errors and LEGACY_EVIDENCE_FROZEN errors; fail closed."""
        try:
            baseline = self.legacy_baseline()
            records = self.legacy_records()
        except (ProjectControlError, OSError, ValueError) as exc:
            return str(exc), [str(exc)], [str(exc)]
        if baseline is None:
            return "no legacy baseline declared", [], []
        head = baseline[0]
        if not records:
            return f"no Work Item at legacy baseline {head}", [], []
        present: list[str] = []
        frozen: list[str] = []
        for identifier, (blob, original) in records.items():
            path = self.root / f"project_control/work-items/{identifier}.json"
            if not path.is_file():
                present.append(f"{identifier}: legacy Work Item is missing")
                continue
            try:
                current = path.read_bytes()
                if original.get("status") == "DONE":
                    if current != blob:
                        frozen.append(f"{identifier}: legacy DONE record changed; historical bytes must be preserved")
                else:
                    record = json.loads(current)
                    if not isinstance(record, dict):
                        raise ProjectControlError(f"{identifier}: legacy Work Item is not an object")
                    self.legacy_evidence_prefixes(record)
            except (ProjectControlError, OSError, ValueError) as exc:
                frozen.append(str(exc))
        return f"{len(records)} legacy Work Item(s) frozen at {head}", present, frozen

    def legacy_done(self, item: dict[str, Any]) -> bool:
        original = self.legacy_record(item)
        return bool(original) and original.get("status") == "DONE"

    def done_evidence_errors(self, item: dict[str, Any]) -> list[str]:
        if item.get("status") != "DONE":
            return []
        work_item_id = item["work_item_id"]
        try:
            if self.legacy_done(item):
                # Closed before the adoption baseline: bytes are frozen (LEGACY_EVIDENCE_FROZEN);
                # no close_head and no evidence level is reconstructed for it.
                return []
            prefixes = self.legacy_evidence_prefixes(item)
        except (ProjectControlError, OSError, ValueError) as exc:
            return [str(exc)]
        baseline = item.get("close_head")
        if not SHA40.fullmatch(str(baseline)) or not self.in_current_history(str(baseline)):
            return [f"{work_item_id}: close_head is missing or not in current history"]
        errors: list[str] = []
        for gate in EVIDENCE_GATES:
            if item["applicability"][gate] != "APPLICABLE":
                continue
            refs = item["evidence"][gate][len(prefixes[gate]):]
            if not refs:
                errors.append(f"{work_item_id}: {gate} requires new verifiable evidence after the legacy baseline")
            for index, ref in enumerate(refs):
                try:
                    # Earlier reports may record failures; the last accepted report closes the gate.
                    self.validate_evidence(item, gate, ref, baseline, require_pass=index == len(refs) - 1)
                except (ProjectControlError, OSError, ValueError) as exc:
                    errors.append(f"{work_item_id}: {exc}")
        return errors

    def status_payload(self) -> dict[str, Any]:
        findings = self.audit_findings()
        failures = [f"{v.check}: {v.detail}" for v in findings if v.status == "FAIL"]
        project = self.project_state()
        items = self.records("project_control/work-items")
        legacy_head: str | None = None
        authorities_head: str | None = None
        legacy_done_ids: set[str] = set()
        if not failures:
            baseline = self.legacy_baseline()
            legacy_head = baseline[0] if baseline else None
            authorities = self.authorities_baseline()
            authorities_head = authorities[0] if authorities else None
            legacy_done_ids = {
                identifier for identifier, (_, original) in self.legacy_records().items()
                if original.get("status") == "DONE"
            }
        views = []
        for item in items:
            levels = gate_levels(item.get("runtime_target", "NOT_APPLICABLE"))
            missing = [gate for gate in EVIDENCE_GATES
                       if item["applicability"][gate] == "UNKNOWN" or
                       (item["applicability"][gate] == "APPLICABLE" and
                        (item.get("test_status" if gate == "tests" else gate + "_status") != levels[gate] or not item["evidence"][gate]))]
            if item["applicability"]["code"] == "APPLICABLE" and item.get("development_status") != "DEVELOPED":
                missing.insert(0, "code")
            if failures:
                validation = "INVALID"
            elif item["status"] != "DONE":
                validation = "PENDING"
            elif item["work_item_id"] in legacy_done_ids:
                validation = "LEGACY_PRESERVED"
            else:
                validation = "STRUCTURED_VERIFIED"
            views.append({"work_item_id": item["work_item_id"], "title": item["title"],
                          "objective": item["objective"], "status": item["status"],
                          "branch": item["branch"], "runtime_target": item["runtime_target"],
                          "missing_gates": missing, "dependencies": item["dependencies"],
                          "close_condition": item["close_condition"],
                          "evidence_validation": validation})
            if item["status"] == "BLOCKED" and item.get("block_records"):
                block = item["block_records"][-1]
                views[-1]["block"] = {key: block[key] for key in (
                    "reason_code", "resume_condition", "human_decision_id",
                )}
            if item["status"] == "IN_PROGRESS" and not failures:
                try:
                    authority_errors = self.authorities_read_errors(item)
                    views[-1]["authorities"] = "CURRENT" if not any(authority_errors.values()) else (
                        "MISSING" if authority_errors["PRESENT"] else "STALE")
                except (ProjectControlError, OSError, ValueError):
                    views[-1]["authorities"] = "UNKNOWN"
        mode = self.operating_mode()
        tongue = self.speech()
        if failures:
            next_action = speak(tongue, "next.audit")
        elif mode == "BOOTSTRAP_MODE":
            next_action = speak(tongue, "next.bootstrap")
        elif any(v["status"] == "IN_PROGRESS" for v in views):
            next_action = speak(tongue, "next.in_progress")
        elif any(v["status"] == "AUTHORIZED" for v in views):
            next_action = speak(tongue, "next.authorized")
        elif any(v["status"] == "BLOCKED" for v in views):
            next_action = speak(tongue, "next.blocked")
        else:
            next_action = speak(tongue, "next.idle")
        try:
            roadmap_view = self.roadmap_view_state()
        except (ProjectControlError, OSError, ValueError):
            roadmap_view = "UNKNOWN"
        return {"read_only": True, "mode": mode, "project_name": project["project_name"],
                "roadmap_view_inherited": self.roadmap_view_is_inherited(),
                **self.repository_context(), "audit_status": "FAIL" if failures else "PASS",
                "hooks": self.commit_gate_state(),
                "legacy_baseline": legacy_head, "authorities_baseline": authorities_head,
                "reporting_style": project.get("reporting_style", "UNKNOWN"),
                "language": project.get("language", "UNKNOWN"), **self.core_status(),
                "roadmap_view": roadmap_view,
                "work_items": views, "errors": failures, "next_action": next_action}

    def close_work_item(self, work_item_id: str, args: argparse.Namespace) -> None:
        if self.operating_mode() != "NORMAL_MODE":
            raise ProjectControlError("close is available only in NORMAL_MODE")
        self.validate_clean_administrative_baseline()
        item = self.work_item_by_id(work_item_id)
        if item is None:
            raise ProjectControlError(f"unknown Work Item: {work_item_id}")
        if item.get("status") not in {"IN_PROGRESS", "IMPLEMENTED", "INTEGRATED", "DEPLOYED", "RUNTIME_PROVEN"}:
            raise ProjectControlError(f"{work_item_id} is not closable from status {item.get('status')}")
        # A closure is an act of today, like create-work-item, block and resume: it reads its
        # mandate in full. Nothing frozen exempts it — a recorded refusal never closes anything.
        decisions_text = self.human_decisions.read_text(encoding="utf-8")
        refs = item.get("human_decision_refs", [])
        mandate_errors = [error for ref in refs for error in human_decision_errors(decisions_text, str(ref))]
        if not refs or mandate_errors:
            raise ProjectControlError(
                "close refused (HUMAN_AUTHORIZATION): "
                + ("the Work Item cites no Human Decision" if not refs else "; ".join(mandate_errors))
            )
        business_changes = [path for path in self.changed_paths() if not self.is_administrative_path(path)]
        if business_changes:
            raise ProjectControlError(f"close requires committed/integrated business paths: {business_changes}")
        # Records live on the canonical branch: close runs there, on a clean worktree, and
        # commits the closure itself.
        self.require_canonical_checkout("close")
        self.require_clean_worktree("close")
        # Proof of reading at close: the authorities read by the latest run must still be current.
        authority_errors = self.authorities_read_errors(item)
        stale = [error for check in ("PRESENT", "COMPLETE", "CURRENT") for error in authority_errors[check]]
        if stale:
            raise ProjectControlError("close refused (AUTHORITY_MANIFEST_AT_CLOSE): " + "; ".join(stale))
        candidate = json.loads(json.dumps(item))
        commits = sorted(set([*candidate.get("commits", []), *args.commit]))
        # A commit cited as this Work Item's work must belong to it. Existence and ancestry of
        # HEAD are not enough: any old commit of the repository satisfies both, and the closure
        # would then record a proof that has nothing to do with the authorized work.
        start_head = str(candidate.get("start_head") or "")
        authorized = candidate.get("authorized_paths", [])
        for commit in commits:
            if not SHA40.fullmatch(commit) or self.run_git(["cat-file", "-e", f"{commit}^{{commit}}"]).returncode != 0:
                raise ProjectControlError(f"unknown commit: {commit}")
            if self.run_git(["merge-base", "--is-ancestor", commit, "HEAD"]).returncode != 0:
                raise ProjectControlError(f"commit is not integrated in current HEAD: {commit}")
            if SHA40.fullmatch(start_head) and commit != start_head:
                if self.run_git(["merge-base", "--is-ancestor", start_head, commit]).returncode != 0:
                    raise ProjectControlError(
                        f"commit predates the Work Item: {commit} is not a descendant of its "
                        f"start_head {start_head}"
                    )
            touched = [path for path in self.git_paths(["show", "--name-only", "--format=", "--no-renames", commit]) if path]
            if authorized and touched and len(normal_path_errors(touched, authorized)) == len(touched):
                raise ProjectControlError(
                    f"commit touches nothing this Work Item was authorized to change: {commit}"
                )
        candidate["commits"] = commits
        applicability = candidate["applicability"]
        if applicability["integration"] == "APPLICABLE":
            current_branch = self.repository_context()["branch"]
            declared_branch = candidate["branch"]
            branch_exists = self.run_git(
                ["show-ref", "--verify", "--quiet", f"refs/heads/{declared_branch}"]
            ).returncode == 0
            integrated = (
                branch_exists
                and current_branch != declared_branch
                and self.run_git(
                    ["merge-base", "--is-ancestor", declared_branch, "HEAD"]
                ).returncode == 0
            )
            if not integrated:
                raise ProjectControlError(
                    "applicable integration requires the declared branch to be merged into the current baseline"
                )
        evidence_arguments = {
            "tests": args.test_evidence,
            "integration": args.integration_evidence,
            "deployment": args.deployment_evidence,
            "runtime_proof": args.runtime_evidence,
        }
        runtime_target = candidate["runtime_target"]
        status_fields = {
            "tests": ("test_status", "TESTED"),
            "integration": ("integration_status", "INTEGRATED"),
            "deployment": ("deployment_status", gate_levels(runtime_target)["deployment"]),
            "runtime_proof": ("runtime_proof_status", gate_levels(runtime_target)["runtime_proof"]),
        }
        if applicability["code"] == "APPLICABLE":
            if not commits:
                raise ProjectControlError("applicable code requires at least one integrated --commit")
            candidate["development_status"] = "DEVELOPED"
        else:
            candidate["development_status"] = "NOT_APPLICABLE"
        for gate, evidence_values in evidence_arguments.items():
            if applicability[gate] == "APPLICABLE":
                if not evidence_values:
                    raise ProjectControlError(f"applicable {gate} requires evidence")
                for value in evidence_values:
                    self.validate_evidence(candidate, gate, value, self.repository_context()["head"])
                previous = candidate["evidence"][gate]
                reused = set(previous) & set(evidence_values)
                if reused:
                    raise ProjectControlError(f"new evidence must use a new path to preserve history: {sorted(reused)}")
                candidate["evidence"][gate] = [*previous, *evidence_values]
                candidate[status_fields[gate][0]] = status_fields[gate][1]
            else:
                candidate["evidence"][gate] = []
                candidate[status_fields[gate][0]] = "NOT_APPLICABLE"
        candidate["status"] = "DONE"
        candidate["close_head"] = self.repository_context()["head"]
        errors = validate_work_item(candidate, self.project_state().get("project_key"), self.canonical_branch())
        if errors:
            raise ProjectControlError("closeout refused: " + "; ".join(errors))

        transaction = FileTransaction(self.root)
        try:
            transaction.write_json(f"project_control/work-items/{work_item_id}.json", candidate)
            for run_ref in candidate.get("agent_run_refs", []):
                run_path = f"project_control/agent-runs/{run_ref}.json"
                path = self.root / run_path
                if not path.is_file():
                    raise ProjectControlError(f"missing Agent Run: {run_ref}")
                run = load_json(path)
                if run.get("result") == "IN_PROGRESS":
                    run["result"] = "SUCCEEDED"
                    run["completed_at"] = now_iso()
                    run["commits"] = commits
                    run["report_reference"] = f"project_control/work-items/{work_item_id}.json"
                    transaction.write_json(run_path, run)
            self.update_roadmap(transaction, candidate, "HISTORICAL")
            self.update_registry(transaction, candidate, "CLOSED")
            self.verify_post_mutation()
            failures = [
                f"{finding.check}: {finding.detail}"
                for finding in self.audit_findings()
                if finding.status == "FAIL"
            ]
            if failures:
                raise ProjectControlError("post-close audit failed: " + "; ".join(failures))
            self.commit_records(transaction, f"chore(project-control): close {work_item_id}")
            transaction.commit()
        except BaseException:
            transaction.rollback()
            raise

    def preflight_findings(self, work_item_id: str, planned_paths: Iterable[str] = (), start_head_override: str | None = None, expected_branch: str | None = None) -> list[Finding]:
        findings = self.audit_findings()
        status = self.first_start_status()
        add(findings, "NORMAL_MODE", status == "COMPLETE", f"FIRST_START={status}; expected COMPLETE")
        item = self.work_item_by_id(work_item_id)
        if item is None:
            add(findings, "WORK_ITEM_EXISTS", False, f"unknown Work Item: {work_item_id}")
            return findings
        add(findings, "WORK_ITEM_EXISTS", True, f"{work_item_id}: {item.get('title')}")
        add(findings, "WORK_ITEM_AUTHORIZED", item.get("status") in PREFLIGHT_STATUSES, f"status={item.get('status')}")
        add(findings, "CONFLICT_GATE", item.get("conflict_gate") in {"INDEPENDENT", "DEPENDENT"}, f"classification={item.get('conflict_gate')}")
        refs = item.get("human_decision_refs", [])
        decisions_text = self.human_decisions.read_text(encoding="utf-8")
        decision_errors = [error for ref in refs for error in human_decision_errors(decisions_text, ref)]
        add(
            findings,
            "HUMAN_AUTHORIZATION",
            bool(refs) and not decision_errors,
            f"human_decision_refs={refs}" if refs and not decision_errors else f"human_decision_refs={refs}; " + "; ".join(decision_errors),
        )
        conversation_ids = {record.get("conversation_ref") for record in self.records("project_control/conversations")}
        conversation_refs = item.get("conversation_refs", [])
        add(
            findings,
            "CONVERSATION_TRACEABILITY",
            bool(conversation_refs) and all(ref in conversation_ids for ref in conversation_refs),
            f"conversation_refs={conversation_refs}",
        )
        applicability = item.get("applicability", {})
        known = isinstance(applicability, dict) and applicability and "UNKNOWN" not in applicability.values()
        add(findings, "APPLICABILITY_DECLARED", bool(known), f"applicability={applicability}")
        impacts_known = all(item.get(field) and all(value != "UNKNOWN" for value in item.get(field, [])) for field in IMPACT_FIELDS)
        add(findings, "IMPACT_MAP", impacts_known, "all four impacts declared")
        records = {record.get("work_item_id"): record for record in self.records("project_control/work-items")}
        incomplete = [dep for dep in item.get("dependencies", []) if records.get(dep, {}).get("status") != "DONE"]
        add(findings, "DEPENDENCIES_DONE", not incomplete, "all dependencies DONE" if not incomplete else f"not DONE: {incomplete}")
        other_active = [
            identifier for identifier, record in records.items()
            if identifier != work_item_id and record.get("status") == "IN_PROGRESS"
        ]
        add(
            findings,
            "SINGLE_ACTIVE_WORK_ITEM",
            not other_active,
            "no other Work Item is active" if not other_active else f"active: {other_active}",
        )
        context = self.repository_context()
        branch = context["branch"]
        declared_branch = item.get("branch")
        canonical = self.canonical_branch()
        expected = expected_branch or declared_branch
        branch_ok = declared_branch not in {canonical, "UNKNOWN", None} and branch == expected
        add(findings, "WORK_ITEM_BRANCH", branch_ok, f"branch={branch}; declared={declared_branch}; expected={expected}")
        if branch != canonical:
            # Records live on the canonical branch only: a Work Item branch never carries
            # administrative changes, so integration merges cannot conflict on records.
            administrative_changes = [path for path in self.changed_paths() if self.is_administrative_path(path)]
            add(
                findings, "WORK_BRANCH_RECORDS_READ_ONLY", not administrative_changes,
                "no administrative change on the Work Item branch"
                if not administrative_changes else
                f"administrative records are written on {canonical} only; changed here: {administrative_changes}",
            )
        base = item.get("base_head")
        base_ok = bool(SHA40.fullmatch(str(base or ""))) and self.run_git(["cat-file", "-e", f"{base}^{{commit}}"]).returncode == 0
        add(findings, "BASE_HEAD", base_ok, f"base_head={base}")
        start = start_head_override or self.latest_run_start_head(item)
        if start != "UNKNOWN" or item.get("status") == "IN_PROGRESS":
            start_ok = bool(SHA40.fullmatch(str(start))) and self.run_git(["cat-file", "-e", f"{start}^{{commit}}"]).returncode == 0
            ancestry_ok = base_ok and start_ok and self.run_git(["merge-base", "--is-ancestor", base, start]).returncode == 0 and self.run_git(["merge-base", "--is-ancestor", start, "HEAD"]).returncode == 0
            add(findings, "START_HEAD", bool(ancestry_ok), f"base_head={base}; start_head={start}; HEAD={context['head']}")
        current = [path for path in self.changed_paths() if not self.is_administrative_path(path)]
        path_errors = normal_path_errors([*current, *planned_paths], item.get("authorized_paths", []))
        add(findings, "AUTHORIZED_PATHS", not path_errors, "all current/planned paths are authorized" if not path_errors else "; ".join(path_errors))
        if item.get("status") == "IN_PROGRESS" or item.get("agent_run_refs"):
            # Proof of reading: the latest Agent Run must carry a complete, current manifest.
            try:
                authority_errors = self.authorities_read_errors(item)
            except (ProjectControlError, OSError, ValueError) as exc:
                authority_errors = {"PRESENT": [str(exc)], "COMPLETE": [], "CURRENT": []}
            for check, label in (("PRESENT", "authorities recorded on the latest Agent Run"),
                                 ("COMPLETE", "every routed authority of the Work Item was read"),
                                 ("CURRENT", "every authority read is unchanged")):
                add(findings, f"AUTHORITY_MANIFEST_{check}", not authority_errors[check],
                    label if not authority_errors[check] else "; ".join(authority_errors[check]))
        return findings


def report(command: str, findings: Sequence[Finding], context: dict[str, str], identifier: str | None = None,
           read_only: bool = True) -> int:
    passed = all(item.status == "PASS" for item in findings)
    print(f"PROJECT_CONTROL: {'PASS' if passed else 'FAIL'}")
    print(f"READ_ONLY: {'true' if read_only else 'false'}")
    print(f"COMMAND: {command}")
    if identifier:
        print(f"WORK_ITEM_ID: {identifier}")
    print(f"BRANCH: {context['branch']}")
    print(f"HEAD: {context['head']}")
    for item in findings:
        print(f"{item.status}: {item.check} — {item.detail}")
    return 0 if passed else 1


def lifecycle_report(
    command: str,
    status: str,
    context: dict[str, str],
    identifier: str,
    detail: str,
    label: str = "WORK_ITEM_ID",
) -> int:
    passed = status == "PASS"
    print(f"PROJECT_CONTROL: {status}")
    print("READ_ONLY: false")
    print(f"COMMAND: {command}")
    print(f"{label}: {identifier}")
    print(f"BRANCH: {context['branch']}")
    print(f"HEAD: {context['head']}")
    print(f"{'PASS' if passed else 'FAIL'}: TRANSACTION — {detail}")
    return 0 if passed else 1


def command_main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    status = subparsers.add_parser("status", help="Summarize current state and next action without writing.")
    status.add_argument("--json", action="store_true")
    subparsers.add_parser("audit", help="Audit schemas, governance, records and Git traceability.")
    subparsers.add_parser(
        "pre-commit",
        help="Commit gate run by scripts/hooks/pre-commit: mode audit on the staged state and canonical branch protection.",
    )
    subparsers.add_parser("bootstrap-audit", help="Audit a NOT_STARTED project in Bootstrap Mode.")
    bootstrap = subparsers.add_parser("bootstrap-preflight", help="Authorize only bootstrap-allowlisted paths.")
    bootstrap.add_argument("--path", action="append", default=[], help="Planned repository-relative path; repeat as needed.")
    closeout = subparsers.add_parser("bootstrap-closeout", help="Verify all initialization deliverables before COMPLETE.")
    closeout.add_argument("--path", action="append", default=[], help="Planned closeout path; repeat as needed.")
    preflight = subparsers.add_parser("preflight", help="Fail-closed normal-mode preflight for one Work Item.")
    preflight.add_argument("work_item_id", help="Internal Work Item ID, for example WI-001.")
    preflight.add_argument("--path", action="append", default=[], help="Planned repository-relative path; repeat as needed.")
    create = subparsers.add_parser(
        "create-work-item",
        help="Transactionally record an authorized Work Item and its administrative consequences.",
    )
    create.add_argument("work_item_id", help="Internal Work Item ID, for example WI-001.")
    create.add_argument("--title", required=True)
    create.add_argument("--objective", required=True)
    create.add_argument("--owner", required=True)
    create.add_argument("--human-decision", required=True, help="Existing or newly recorded HD-NNN.")
    create.add_argument("--decision", help="Decision text; required only when the Human Decision is new.")
    create.add_argument("--authorized-by", help="Human authorizer; defaults to --owner for a new decision.")
    create.add_argument("--conversation-ref")
    create.add_argument("--conversation-provider", default="ProjectControlCLI")
    create.add_argument("--conversation-workspace")
    create.add_argument("--conversation-title")
    create.add_argument("--conversation-external-reference")
    create.add_argument("--branch")
    create.add_argument("--base-head")
    create.add_argument("--path", action="append", required=True, help="Authorized work path; repeat as needed.")
    create.add_argument("--depends-on", action="append", default=[])
    create.add_argument("--conflict-gate", choices=("INDEPENDENT", "DEPENDENT"), required=True)
    create.add_argument("--direct-impact", action="append", required=True)
    create.add_argument("--indirect-impact", action="append", required=True)
    create.add_argument("--authority-impact", action="append", required=True)
    create.add_argument("--concurrent-work-impact", action="append", required=True)
    for option, default in (
        ("code", "APPLICABLE"),
        ("tests", "APPLICABLE"),
        ("integration", "APPLICABLE"),
        ("deployment", "NOT_APPLICABLE"),
        ("runtime-proof", "NOT_APPLICABLE"),
    ):
        create.add_argument(
            f"--{option}",
            dest=option.replace("-", "_"),
            choices=sorted(APPLICABILITY),
            default=default,
        )
    create.add_argument("--runtime-target", choices=sorted(RUNTIME_TARGETS), default="NOT_APPLICABLE")
    create.add_argument("--close-condition", required=True)
    start = subparsers.add_parser(
        "start",
        help="Create/check out the declared branch, run preflight, then enter IN_PROGRESS.",
    )
    start.add_argument("work_item_id")
    start.add_argument("--path", action="append", default=[])
    start.add_argument("--agent-provider", default="ProjectControlCLI")
    start.add_argument("--authorities-digest", help="MANIFEST_DIGEST printed by `context-manifest WI-NNN` after reading the listed authorities.")
    block = subparsers.add_parser(
        "block",
        help="Record an authorized external dependency and enter non-active BLOCKED.",
    )
    block.add_argument("work_item_id")
    block.add_argument("--human-decision", required=True)
    block.add_argument("--reason-code", required=True)
    block.add_argument("--resume-condition", required=True)
    resume = subparsers.add_parser(
        "resume",
        help="Resolve the latest external dependency and start a new Agent Run.",
    )
    resume.add_argument("work_item_id")
    resume.add_argument("--human-decision", required=True)
    resume.add_argument("--path", action="append", default=[])
    resume.add_argument("--agent-provider", default="ProjectControlCLI")
    resume.add_argument("--authorities-digest", help="MANIFEST_DIGEST printed by `context-manifest WI-NNN` after reading the listed authorities.")
    acknowledge = subparsers.add_parser(
        "acknowledge-authorities",
        help="Record a fresh reading of the routed authorities on the Agent Run in progress (canonical branch, committed).",
    )
    acknowledge.add_argument("work_item_id")
    acknowledge.add_argument("--authorities-digest", required=True, help="MANIFEST_DIGEST printed by `context-manifest WI-NNN`.")
    manifest_command = subparsers.add_parser(
        "context-manifest",
        help="Read-only: list the routed authorities of a Work Item (or of explicit scopes) with their hashes and MANIFEST_DIGEST.",
    )
    manifest_command.add_argument("work_item_id", nargs="?", help="Work Item whose authorized paths select the scopes.")
    manifest_command.add_argument("--scope", action="append", default=[], help="Additional scope of mandatory-documents.v1.json; repeat as needed.")
    manifest_command.add_argument("--json", action="store_true")
    close = subparsers.add_parser("close", help="Verify all applicable evidence and close one Work Item.")
    close.add_argument("work_item_id")
    close.add_argument("--commit", action="append", default=[])
    close.add_argument("--test-evidence", action="append", default=[])
    close.add_argument("--integration-evidence", action="append", default=[])
    close.add_argument("--deployment-evidence", action="append", default=[])
    close.add_argument("--runtime-evidence", action="append", default=[])
    subparsers.add_parser(
        "install-gate",
        help="Install the commit gate outside the worktree, from its versioned reference.",
    )
    manifest = subparsers.add_parser(
        "core-manifest",
        help="Check the core manifest against the tree; --write regenerates it (template maintenance only).",
    )
    manifest.add_argument("--write", action="store_true", help="Regenerate provenance/core-manifest.v1.json from the tree.")
    manifest.add_argument("--version", dest="skeleton_version", help="Skeleton version to record with --write (MAJOR.MINOR.PATCH).")
    upgrade = subparsers.add_parser(
        "template-upgrade",
        help="Compare this project's core with another template tree; report by default, --apply to upgrade intact files.",
    )
    upgrade.add_argument("--source", required=True, help="Directory holding the template tree to upgrade from.")
    upgrade.add_argument("--apply", action="store_true", help="Write the upgrade; without it nothing is written.")
    upgrade.add_argument("--overwrite", action="append", default=[], help="Locally modified core path to replace anyway; repeat as needed.")
    upgrade.add_argument(
        "--seed-required", action="store_true",
        help="On the canonical branch only: write the files the new version requires and the project does not have, then stop.",
    )
    view_command = subparsers.add_parser(
        "roadmap-view",
        help="Read-only: compute the roadmap view from the repository's files; --json prints it, --write renders the page and the Markdown view.",
    )
    view_command.add_argument("--json", action="store_true", help="Print the view model as JSON.")
    view_command.add_argument("--write", action="store_true", help="Write the HTML page and the Markdown view at their default paths.")
    view_command.add_argument("--html", help="Write the HTML page to this repository-relative path.")
    view_command.add_argument("--markdown", help="Write the Markdown view to this repository-relative path.")
    view_command.add_argument("--style", choices=("TECHNICAL", "PLAIN"), help="Render in this style instead of the project's reporting style.")
    idea = subparsers.add_parser("idea", help="Record what the Project Owner said (two synchronized forms, committed on the canonical branch in NORMAL_MODE).")
    idea_commands = idea.add_subparsers(dest="idea_command", required=True)
    idea_add = idea_commands.add_parser("add", help="Add an idea in the Project Owner's own words.")
    idea_add.add_argument("--quote", required=True, help="The Project Owner's words.")
    idea_add.add_argument("--source", required=True, help="Where it was said: discussion, date.")
    idea_add.add_argument("--state", choices=IDEA_STATES, default="EVOKED")
    idea_add.add_argument("--stated-at", dest="stated_at", help="YYYY-MM-DD; defaults to today.")
    idea_add.add_argument("--target", help="WI-NNN, version or HD-NNN carrying the idea, when known.")
    idea_add.add_argument("--note", help="What the idea became, in one line.")
    idea_set = idea_commands.add_parser("set", help="Change the state, target or note of an idea.")
    idea_set.add_argument("idea_id", help="ID-NNN")
    idea_set.add_argument("--state", choices=IDEA_STATES)
    idea_set.add_argument("--target", help="WI-NNN, version or HD-NNN; empty string clears it.")
    idea_set.add_argument("--note", help="One line; empty string clears it.")
    args = parser.parse_args(argv)
    control = ProjectControl(ROOT)
    if command_mutates(args):
        # Before the first read, not at the first write: these commands read the registers, compute
        # the next state and write it back. Two of them running at once both read the old registers
        # and the second silently dropped what the first had just recorded. Taking the lock here
        # makes the whole read-modify-write one operation, whoever runs it.
        hold_administrative_lock(control.root)
    context = control.repository_context()
    if args.command == "roadmap-view":
        try:
            view = control.roadmap_view_model(args.style)
            html_path = args.html or (control.view_paths()["html"] if args.write else None)
            markdown_path = args.markdown or (control.view_paths()["markdown"] if args.write else None)
            written, notes = control.write_roadmap_view(view, html_path, markdown_path, governed=args.write and not args.markdown)
        except (ProjectControlError, OSError, json.JSONDecodeError, ValueError, KeyError, TypeError) as exc:
            findings: list[Finding] = []
            add(findings, "ROADMAP_VIEW", False, str(exc))
            return report("roadmap-view", findings, control.repository_context())
        if args.json:
            print(json.dumps(view, ensure_ascii=False, indent=2))
            return 0
        findings = []
        verification = view["verification"]
        add(findings, "ROADMAP_VIEW", True,
            f"style {view['style']}; audit {verification['audit_status']}; sources_digest {verification['sources_digest']}"
            + (f"; written: {', '.join(written)}" if written else "; nothing written (use --write, --html or --markdown)")
            + (f"; {'; '.join(notes)}" if notes else ""))
        return report("roadmap-view", findings, control.repository_context(), read_only=not written)
    if args.command == "idea":
        try:
            idea_id = control.record_idea(args)
        except (ProjectControlError, OSError, json.JSONDecodeError) as exc:
            return lifecycle_report("idea", "FAIL", control.repository_context(), getattr(args, "idea_id", "ID-NEW").upper(), str(exc), label="IDEA_ID")
        committed = "committed on the canonical branch" if control.operating_mode() == "NORMAL_MODE" else "written (Bootstrap Mode: commit it with the initialization)"
        return lifecycle_report("idea", "PASS", control.repository_context(), idea_id, f"idea recorded in ideas-state.v1.json and IDEAS.md, {committed}", label="IDEA_ID")
    if args.command == "context-manifest":
        scopes = list(args.scope)
        label = "NO_WORK_ITEM"
        if args.work_item_id:
            item = control.work_item_by_id(args.work_item_id.upper())
            if item is None:
                raise ProjectControlError(f"unknown Work Item: {args.work_item_id}")
            scopes.extend(scopes_for_paths(item.get("authorized_paths", [])))
            label = args.work_item_id.upper()
        manifest = control.authority_manifest(scopes)
        if args.json:
            print(json.dumps(manifest, ensure_ascii=False, indent=2))
        else:
            print(f"CONTEXT_MANIFEST: {label} | scopes: {', '.join(manifest['scopes']) or 'base only'}")
            print(f"HEAD: {manifest['head']}")
            for entry in manifest["entries"]:
                print(f"AUTHORITY: {entry['path']} sha256={entry['sha256']}")
            print(f"MANIFEST_DIGEST: {manifest['manifest_digest']}")
        return 0
    if args.command == "install-gate":
        return report("install-gate", control.install_commit_gate(), context, read_only=False)
    if args.command == "core-manifest":
        if args.write:
            if not args.skeleton_version:
                raise ProjectControlError("core-manifest --write requires --version MAJOR.MINOR.PATCH")
            control.write_core_manifest(args.skeleton_version)
            return report("core-manifest", control.core_manifest_findings(), context, read_only=False)
        return report("core-manifest", control.core_manifest_findings(), context)
    if args.command == "template-upgrade":
        try:
            findings = control.template_upgrade(Path(args.source), args.apply, args.overwrite, args.seed_required)
        except (ProjectControlError, OSError) as exc:
            findings = []
            add(findings, "TEMPLATE_UPGRADE", False, str(exc))
        return report("template-upgrade", findings, control.repository_context(),
                      read_only=not (args.apply or args.seed_required))
    if args.command == "status":
        try:
            payload = control.status_payload()
        except (ProjectControlError, OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
            payload = {"read_only": True, **context, "audit_status": "FAIL", "errors": [str(exc)],
                       "next_action": speak(control.speech(), "status.broken")}
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            tongue = control.speech()

            def line(key: str, **values: Any) -> None:
                print(speak(tongue, key, **values))

            line("status.project", name=payload.get("project_name", "UNKNOWN"), mode=payload.get("mode", "INVALID"))
            style = payload.get("reporting_style", "UNKNOWN")
            line("status.reporting", label=reporting_style_label(style, tongue))
            line("status.language", label=LANGUAGE_LABELS.get(payload.get("language", "UNKNOWN"), payload.get("language")))
            line("status.branch", branch=context["branch"], head=context["head"])
            line("status.checks", status=payload["audit_status"])
            hooks = payload.get("hooks", "UNKNOWN")
            line("status.gate", state=speak(tongue, f"gate.{hooks}") if f"gate.{hooks}" in SPEECH else hooks)
            drift = payload.get("core_drift", {})
            core = (speak(tongue, "core.aligned") if not drift
                    else speak(tongue, "core.drift", paths=", ".join(f"{path} ({state})" for path, state in drift.items())))
            line("status.skeleton", version=payload.get("skeleton_version", "UNKNOWN"), core=core)
            view_state = payload.get("roadmap_view", "UNKNOWN")
            # A stale view generated at a commit this repository does not have came from the
            # tree the copy was taken from: it is not this project's view yet, and sending a
            # newcomer to regenerate it before he has initialized anything helps no one.
            if view_state == "STALE" and payload.get("roadmap_view_inherited"):
                view_state = "INHERITED"
            line("status.view", state=speak(tongue, f"view.{view_state}") if f"view.{view_state}" in SPEECH else view_state)
            items = payload.get("work_items", [])
            done = sum(item["status"] == "DONE" for item in items)
            frozen = sum(item.get("evidence_validation") == "LEGACY_PRESERVED" for item in items)
            legacy = speak(tongue, "status.legacy", frozen=frozen) if frozen else ""
            line("status.done", done=done, legacy=legacy,
                 blocked=sum(item["status"] == "BLOCKED" for item in items))
            for item in items:
                if item["status"] in {"DONE", "REJECTED", "SUPERSEDED"}:
                    continue
                line("status.item", id=item["work_item_id"], title=item["title"], status=item["status"])
                line("status.objective", objective=item["objective"])
                line("status.item_branch", branch=item["branch"], target=item["runtime_target"])
                line("status.missing", gates=", ".join(item["missing_gates"]) or speak(tongue, "status.none_declared"))
                if item.get("authorities"):
                    read = item["authorities"]
                    line("status.authorities",
                         state=speak(tongue, f"authorities.{read}") if f"authorities.{read}" in SPEECH else read)
                if item.get("block"):
                    line("status.block", code=item["block"]["reason_code"])
                    line("status.resume", condition=item["block"]["resume_condition"])
            for error in payload["errors"]:
                line("status.error", error=error)
            line("status.next", action=payload["next_action"])
        return 0 if payload['audit_status'] == "PASS" else 1
    if args.command == "audit":
        return report("audit", control.audit_findings(), context)
    if args.command == "pre-commit":
        return report("pre-commit", control.commit_gate_findings(), context)
    if args.command in {"bootstrap-audit", "bootstrap-preflight"}:
        return report(args.command, control.bootstrap_findings(getattr(args, "path", [])), context)
    if args.command == "bootstrap-closeout":
        findings = control.bootstrap_findings(args.path)
        readiness = control.closeout_readiness(require_complete=False)
        add(findings, "BOOTSTRAP_CLOSEOUT", not readiness, "initialization deliverables complete; transition may be recorded" if not readiness else "; ".join(readiness))
        return report("bootstrap-closeout", findings, context)
    if args.command in {"create-work-item", "start", "block", "resume", "close", "acknowledge-authorities"}:
        work_item_id = args.work_item_id.upper()
        try:
            if args.command == "create-work-item":
                control.create_work_item(args)
                detail = "Work Item, decision/conversation links, roadmap, registry and Git classification committed atomically"
            elif args.command == "start":
                run_ref = control.start_work_item(work_item_id, args.path, args.agent_provider, args.authorities_digest)
                detail = f"declared branch checked out, preflight passed and Agent Run {run_ref} started"
            elif args.command == "acknowledge-authorities":
                run_ref = control.acknowledge_authorities(work_item_id, args.authorities_digest)
                detail = f"authorities re-read and recorded on Agent Run {run_ref}"
            elif args.command == "block":
                control.block_work_item(work_item_id, args)
                detail = "external dependency recorded; Work Item and latest Agent Run BLOCKED"
            elif args.command == "resume":
                run_ref = control.resume_work_item(
                    work_item_id,
                    args.path,
                    args.agent_provider,
                    args.human_decision,
                    args.authorities_digest,
                )
                alignment = control.last_alignment
                aligned = {
                    "NONE": "branch already at canonical tip",
                    "FAST_FORWARD": f"branch fast-forwarded to {alignment['commit']}",
                    "MERGE": f"branch aligned by merge commit {alignment['commit']} (records taken from canonical)",
                }[str(alignment["mode"])]
                detail = f"resume condition confirmed; {aligned}; Agent Run {run_ref} started"
            else:
                control.close_work_item(work_item_id, args)
                detail = "applicable evidence records and Git references validated; Work Item DONE"
            return lifecycle_report(args.command, "PASS", control.repository_context(), work_item_id, detail)
        except (ProjectControlError, OSError, json.JSONDecodeError) as exc:
            return lifecycle_report(
                args.command,
                "FAIL",
                control.repository_context(),
                work_item_id,
                str(exc),
            )
    work_item_id = args.work_item_id.upper()
    return report("preflight", control.preflight_findings(work_item_id, args.path), context, work_item_id)


def main(argv: Sequence[str] | None = None) -> int:
    try:
        return command_main(argv)
    except (ProjectControlError, OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        print("PROJECT_CONTROL: FAIL")
        print(f"FAIL: INVALID_RECORDS — {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
