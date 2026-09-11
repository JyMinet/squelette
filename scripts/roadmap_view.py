#!/usr/bin/env python3
"""Generated roadmap view (P12, P6): renderers for the `roadmap-view` command.

The view shows where the project stands, what comes next, what awaits the Project Owner
and what became of the Project Owner's ideas. It is computed by project_control.py from
the repository's own files and rendered here as HTML (a self-contained page) and Markdown
(a committed human view). The view displays; it never decides anything.

Rendering rules (docs/agent-governance/ROADMAP_VIEW.md):
- the form is stable from one generation to the next: same sections, same order;
- PLAIN style: the view adds no technical identifier of its own (commit, digest, path,
  command) outside the folded "Pour les techniciens" block, which lists them in full;
  text quoted from the project's own files is shown as the Project Owner wrote it — the
  view displays, it does not rewrite him. TECHNICAL style: identifiers inline;
- every line names its source; what has no source is marked unknown;
- zoom: the past is collapsed, now and next steps are detailed, later is titles only.
"""

from __future__ import annotations

import html
import re
from typing import Any, Sequence

VIEW_SCHEMA_VERSION = "1.0.0"
VIEW_MARKER = re.compile(r"^<!-- ROADMAP_VIEW sources_digest=([a-f0-9]{64}) generated_at=(\S+) head=(\S+) -->$")

IDEA_STATES = (
    "EVOKED", "TO_CLARIFY", "TO_SET", "SCOPED", "PLANNED", "IN_PROGRESS",
    "REALIZED", "APPLIED", "INTEGRATED", "LATER", "DISCARDED",
)
IDEA_LABELS = {
    "EVOKED": "évoquée", "TO_CLARIFY": "à clarifier", "TO_SET": "à régler", "SCOPED": "cadrée",
    "PLANNED": "planifiée", "IN_PROGRESS": "en cours", "REALIZED": "réalisée", "APPLIED": "appliquée",
    "INTEGRATED": "intégrée", "LATER": "plus tard", "DISCARDED": "écartée",
}
IDEA_CHIPS = {
    "EVOKED": "scoped", "TO_CLARIFY": "ask", "TO_SET": "scoped", "SCOPED": "scoped", "PLANNED": "active",
    "IN_PROGRESS": "active", "REALIZED": "done", "APPLIED": "done", "INTEGRATED": "done",
    "LATER": "later", "DISCARDED": "later",
}
CHANTIER_LABELS = {
    "DONE": "Fait", "PARTIAL": "Partiel", "IN_PROGRESS": "En cours", "SCOPED": "Cadré",
    "TO_SCOPE": "À cadrer", "LATER": "Plus tard",
}
CHANTIER_CHIPS = {
    "DONE": "done", "PARTIAL": "partial", "IN_PROGRESS": "active", "SCOPED": "scoped",
    "TO_SCOPE": "later", "LATER": "later",
}
WORK_ITEM_LABELS = {
    "PROPOSED": "Proposé", "AUTHORIZED": "Autorisé", "IN_PROGRESS": "En cours", "IMPLEMENTED": "Développé",
    "INTEGRATED": "Intégré", "DEPLOYED": "Déployé", "RUNTIME_PROVEN": "Prouvé en marche", "DONE": "Terminé",
    "BLOCKED": "Bloqué", "REJECTED": "Rejeté", "SUPERSEDED": "Remplacé",
}
IDEA_LABELS_EN = {
    "EVOKED": "raised", "TO_CLARIFY": "to clarify", "TO_SET": "to settle", "SCOPED": "scoped",
    "PLANNED": "planned", "IN_PROGRESS": "in progress", "REALIZED": "delivered", "APPLIED": "applied",
    "INTEGRATED": "integrated", "LATER": "later", "DISCARDED": "discarded",
}
CHANTIER_LABELS_EN = {
    "DONE": "Done", "PARTIAL": "Partial", "IN_PROGRESS": "In progress", "SCOPED": "Scoped",
    "TO_SCOPE": "To scope", "LATER": "Later",
}
WORK_ITEM_LABELS_EN = {
    "PROPOSED": "Proposed", "AUTHORIZED": "Authorized", "IN_PROGRESS": "In progress", "IMPLEMENTED": "Implemented",
    "INTEGRATED": "Integrated", "DEPLOYED": "Deployed", "RUNTIME_PROVEN": "Proven in runtime", "DONE": "Done",
    "BLOCKED": "Blocked", "REJECTED": "Rejected", "SUPERSEDED": "Superseded",
}


def idea_label_in(state: str, language: str) -> str:
    table = IDEA_LABELS_EN if language == "EN" else IDEA_LABELS
    return table.get(state, state.lower())


def chantier_label(state: str, language: str) -> str:
    table = CHANTIER_LABELS_EN if language == "EN" else CHANTIER_LABELS
    return table.get(state, state)


def work_item_label(status: str, language: str) -> str:
    table = WORK_ITEM_LABELS_EN if language == "EN" else WORK_ITEM_LABELS
    return table.get(status, status)


WORK_ITEM_CHIPS = {
    "PROPOSED": "later", "AUTHORIZED": "scoped", "IN_PROGRESS": "active", "IMPLEMENTED": "active",
    "INTEGRATED": "active", "DEPLOYED": "active", "RUNTIME_PROVEN": "active", "DONE": "done",
    "BLOCKED": "partial", "REJECTED": "later", "SUPERSEDED": "later",
}
TONE_DOTS = {"good": "", "warn": " warn", "neutral": " neutral"}
MONTHS_FR = ("janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc.")


MONTHS_EN = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")


def written_date(value: str, language: str = "FR") -> str:
    """2026-09-07 -> 7 sept. 2026, or Sep 7, 2026; anything else is returned unchanged."""
    match = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})(?:[T ](\d{2}):(\d{2})(?::\d{2}(?:\.\d+)?)?(Z|[+-]\d{2}:?\d{2})?)?", value or "")
    if match is None:
        return value or ("unknown" if language == "EN" else "inconnu")
    year, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))
    if not 1 <= month <= 12:
        return value
    text = (f"{MONTHS_EN[month - 1]} {day}, {year}" if language == "EN"
            else f"{day} {MONTHS_FR[month - 1]} {year}")
    if match.group(4):
        text += f", {match.group(4)}:{match.group(5)}"
        # A timestamp carries its zone: say so, rather than let a UTC hour read as local time.
        if match.group(6) == "Z":
            text += " UTC"
        elif match.group(6):
            text += f" (UTC{match.group(6)})"
    return text


def french_date(value: str) -> str:
    """Kept as the French spelling of written_date, used where the language is not carried."""
    return written_date(value, "FR")


def short_date(value: str, language: str = "FR") -> str:
    text = written_date(value, language)
    return re.sub(r" \d{4}(,.*)?$", "", text)


def esc(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def md_cell(value: Any) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", "¦").replace("\n", " ").strip() or "—"


TEXT: dict[str, dict[str, str]] = {
    "empty.todo": {"FR": "Rien ne t’attend pour l’instant.", "EN": "Nothing awaits you right now."},
    "empty.far": {"FR": "Rien de plus lointain n’est écrit.", "EN": "Nothing further out is written down."},
    "empty.now": {"FR": "Rien à signaler.", "EN": "Nothing to report."},
    "empty.next": {"FR": "Aucune étape suivante n’est écrite.", "EN": "No next step is written down."},
    "empty.past": {"FR": "Rien n’est encore derrière nous.", "EN": "Nothing is behind us yet."},
    "empty.ideas": {"FR": "Aucune idée enregistrée pour l’instant. Une idée dite au fil d’une discussion se note avec « idea add ».",
                    "EN": "No idea recorded yet. An idea said in passing is recorded with “idea add”."},
    "empty.chantiers": {"FR": "Aucun chantier enregistré.", "EN": "No workstream recorded."},
    "empty.work_items": {"FR": "Aucun chantier enregistré.", "EN": "No Work Item recorded."},
    "version.next": {"FR": "suivante", "EN": "next"},
    "version.upcoming": {"FR": "à venir", "EN": "upcoming"},
    "version.to_scope": {"FR": "à cadrer", "EN": "to scope"},
    "h.versions": {"FR": "Les versions, dans l’ordre", "EN": "The versions, in order"},
    "h.versions_zoom": {"FR": "une étape par version · la suivante est en pointillé",
                        "EN": "one step per version · the next one is dotted"},
    "h.ideas": {"FR": "Tes idées, et ce qu’elles sont devenues", "EN": "Your ideas, and what became of them"},
    "h.ideas_zoom": {"FR": "une idée évoquée devient une ligne ici, jamais un oubli",
                     "EN": "an idea raised becomes a line here, never an omission"},
    "h.ideas_states": {"FR": "Les états : évoquée, à clarifier, à régler, cadrée, planifiée, en cours, réalisée, appliquée, intégrée, plus tard, écartée.",
                       "EN": "The states: raised, to clarify, to settle, scoped, planned, in progress, delivered, applied, integrated, later, discarded."},
    "h.now": {"FR": "Maintenant", "EN": "Right now"},
    "h.detail": {"FR": "en détail", "EN": "in detail"},
    "h.waiting": {"FR": "Ce qui t’attend", "EN": "What awaits you"},
    "h.waiting_zoom": {"FR": "tes actions, dans l’ordre", "EN": "your actions, in order"},
    "h.next": {"FR": "Prochaines étapes", "EN": "Next steps"},
    "h.past": {"FR": "Ce qui est derrière nous", "EN": "What is behind us"},
    "h.technicians": {"FR": "Pour les techniciens", "EN": "For technicians"},
    "h.verification": {"FR": "Vérification", "EN": "Verification"},
    "col.when": {"FR": "Quand", "EN": "When"},
    "col.idea": {"FR": "Ton idée", "EN": "Your idea"},
    "col.became": {"FR": "Ce qu’elle est devenue", "EN": "What became of it"},
    "col.state": {"FR": "État", "EN": "State"},
    "col.source": {"FR": "Source", "EN": "Source"},
    "col.number": {"FR": "N°", "EN": "No."},
    "col.chantier": {"FR": "Chantier", "EN": "Workstream"},
    "col.where": {"FR": "Où en est-on", "EN": "Where it stands"},
    "col.sheet": {"FR": "Fiche", "EN": "Scope sheet"},
    "col.decision": {"FR": "Décision", "EN": "Decision"},
    "cell.missing": {"FR": "Vérifications manquantes : {missing}.", "EN": "Missing checks: {missing}."},
    "cell.blocked": {"FR": "Bloqué : {condition}.", "EN": "Blocked: {condition}."},
    "cell.scope_sheet": {"FR": "fiche de cadrage dans le dossier", "EN": "scope sheet in the folder"},
    "btn.expand": {"FR": "Tout déployer", "EN": "Expand all"},
    "btn.collapse": {"FR": "Tout replier", "EN": "Collapse all"},
    "tech.summary": {"FR": "Pour les techniciens — détails de la vérification (replié)",
                     "EN": "For technicians — verification details (folded)"},
    "tech.generated": {"FR": "généré le {when} · style {style} · rôle {role}",
                       "EN": "generated {when} · style {style} · role {role}"},
    "tech.aligned": {"FR": "aligné", "EN": "aligned"},
    "tech.drifted": {"FR": "modifié localement", "EN": "modified locally"},
    "tech.tests": {"FR": "tests déclarés : {count}", "EN": "tests declared: {count}"},
    "stats.label": {"FR": "Chiffres clés", "EN": "Key figures"},
    "stamp.label": {"FR": "Vérification", "EN": "Verification"},
    "rules.title": {"FR": "Règles de ce tableau", "EN": "Rules of this dashboard"},
    "rules.body": {"FR": "Il montre, il ne décide rien : aucune ligne ici n’est une décision. Chaque ligne dit d’où elle vient (le dossier, une fiche, un message du Project Owner). Ce qui n’a pas de source est marqué inconnu ou non vérifié — jamais inventé. Le passé est replié, le présent et la suite sont détaillés, la fin est en titres. Les idées y figurent toujours, avec leur état.",
                   "EN": "It shows, it decides nothing: no line here is a decision. Every line says where it comes from (the folder, a scope sheet, a message from the Project Owner). What has no source is marked unknown or unverified — never invented. The past is folded, the present and what follows are detailed, the far end is titles only. Ideas always appear, with their state."},
    "settings.title": {"FR": "Réglages de la vue", "EN": "View settings"},
    "settings.refresh": {"FR": "Mise à jour automatique", "EN": "Automatic refresh"},
    "settings.style": {"FR": "Style", "EN": "Style"},
    "settings.past": {"FR": "Passé", "EN": "Past"},
    "settings.expanded": {"FR": "déployé", "EN": "expanded"},
    "settings.folded": {"FR": "replié", "EN": "folded"},
    "settings.far": {"FR": "Fin", "EN": "Far end"},
    "settings.detailed": {"FR": "détaillée", "EN": "detailed"},
    "settings.titles_only": {"FR": "titres seulement", "EN": "titles only"},
    "settings.form": {"FR": "Forme", "EN": "Form"},
    "settings.form_value": {"FR": "stable, générée par le contrôleur", "EN": "stable, generated by the controller"},
    "settings.language": {"FR": "Langue", "EN": "Language"},
    "howto.title": {"FR": "Comment s’en servir", "EN": "How to use it"},
    "howto.body": {"FR": "Cette page est générée depuis les fichiers du projet (roadmap, décisions, idées, réglages) par la commande roadmap-view. Dans la discussion « ROADMAP », n’importe quel message la régénère ; une phrase qui commence par « RÉGLAGE : » change un réglage ci-contre. Tout le reste — une décision, une écriture dans le dossier, un changement de version — est renvoyé vers une autre discussion.",
                   "EN": "This page is generated from the project's files (roadmap, decisions, ideas, settings) by the roadmap-view command. In the “ROADMAP” conversation, any message regenerates it; a sentence starting with “RÉGLAGE:” changes one of the settings opposite. Everything else — a decision, a write in the folder, a version change — is sent to another conversation."},
    "md.lede": {"FR": "Vue générée par `roadmap-view` depuis les fichiers du projet ; elle montre, elle ne décide rien. Ne pas éditer à la main : relancer la commande.",
                "EN": "View generated by `roadmap-view` from the project's files; it shows, it decides nothing. Do not edit by hand: run the command again."},
    "md.no_idea": {"FR": "aucune idée enregistrée", "EN": "no idea recorded"},
    "md.no_chantier": {"FR": "aucun chantier enregistré", "EN": "no workstream recorded"},
    "h.chantiers_template": {"FR": "Les chantiers du squelette", "EN": "The skeleton's workstreams"},
    "h.chantiers_template_zoom": {"FR": "un chantier = une fiche dans le dossier", "EN": "one workstream = one sheet in the folder"},
    "h.chantiers": {"FR": "Les chantiers", "EN": "The Work Items"},
    "h.chantiers_zoom": {"FR": "un chantier = un Work Item de la roadmap", "EN": "one line = one Work Item of the roadmap"},
    "h.far": {"FR": "Plus loin", "EN": "Further out"},
    "md.nothing": {"FR": "Rien.", "EN": "Nothing."},
    "md.sources": {"FR": "Sources", "EN": "Sources"},
    "md.scope_sheets": {"FR": "fiches de cadrage", "EN": "scope sheets"},
    "md.source_label": {"FR": "source", "EN": "source"},
    "src.label": {"FR": "Source", "EN": "Source"},
    "src.unknown": {"FR": "inconnue.", "EN": "unknown."},
    "prj.style_plain": {"FR": "simple", "EN": "plain"},
    "prj.style_technical": {"FR": "technique", "EN": "technical"},
}


def colon(view: dict[str, Any]) -> str:
    """French puts a space before the colon; English does not."""
    return ": " if str(view.get("language", "FR")).upper() == "EN" else " : "


def _t(view: dict[str, Any], key: str, **values: Any) -> str:
    """The one sentence `key` names, in the language the view carries."""
    entry = TEXT.get(key)
    if entry is None:
        return key
    return entry.get(str(view.get("language", "FR")).upper(), entry["FR"]).format(**values)


def idea_label(state: str) -> str:
    return IDEA_LABELS.get(state, state.lower())


def chip(kind: str, label: str) -> str:
    return f'<span class="chip chip-{esc(kind)}">{esc(label)}</span>'


# --- HTML -------------------------------------------------------------------------------

CSS = """
  :root {
    --bg: #F4F6F9; --surface: #FFFFFF; --surface-2: #EAEFF5; --ink: #17202B; --ink-2: #46536A;
    --muted: #74829A; --line: #D5DCE7; --line-strong: #B8C3D3; --accent: #1F5FBF; --accent-ink: #164A93;
    --accent-soft: #E1EAF9; --good: #1E7F4F; --good-soft: #DFF2E6; --warn: #9A5F0A; --warn-soft: #FBEEDA;
    --crit: #B42318; --crit-soft: #FBE3E0;
    --shadow: 0 1px 2px rgba(23, 32, 43, 0.06), 0 8px 24px rgba(23, 32, 43, 0.06);
    --sans: "IBM Plex Sans", "Helvetica Neue", Arial, sans-serif;
    --mono: "IBM Plex Mono", "SFMono-Regular", Menlo, Consolas, monospace;
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --bg: #0E131A; --surface: #151C26; --surface-2: #1D2633; --ink: #E7ECF2; --ink-2: #B3BECC;
      --muted: #8593A6; --line: #2A3543; --line-strong: #3B485A; --accent: #7FAAFF; --accent-ink: #A9C6FF;
      --accent-soft: #1A2A47; --good: #5FC791; --good-soft: #143222; --warn: #E4AC52; --warn-soft: #3A2A10;
      --crit: #F0908A; --crit-soft: #40171A;
      --shadow: 0 1px 2px rgba(0, 0, 0, 0.4), 0 8px 24px rgba(0, 0, 0, 0.35);
    }
  }
  :root[data-theme="dark"] {
    --bg: #0E131A; --surface: #151C26; --surface-2: #1D2633; --ink: #E7ECF2; --ink-2: #B3BECC;
    --muted: #8593A6; --line: #2A3543; --line-strong: #3B485A; --accent: #7FAAFF; --accent-ink: #A9C6FF;
    --accent-soft: #1A2A47; --good: #5FC791; --good-soft: #143222; --warn: #E4AC52; --warn-soft: #3A2A10;
    --crit: #F0908A; --crit-soft: #40171A;
    --shadow: 0 1px 2px rgba(0, 0, 0, 0.4), 0 8px 24px rgba(0, 0, 0, 0.35);
  }
  * { box-sizing: border-box; }
  body { margin: 0; background: var(--bg); color: var(--ink); font-family: var(--sans); font-size: 15.5px; line-height: 1.55; -webkit-font-smoothing: antialiased; }
  a { color: var(--accent-ink); }
  code { font-family: var(--mono); font-size: 0.86em; color: var(--ink-2); background: var(--surface-2); padding: 0.05em 0.35em; border-radius: 3px; white-space: nowrap; }
  h1, h2, h3 { text-wrap: balance; margin: 0; }
  p { margin: 0; }
  ul { margin: 0; padding-left: 1.1em; }
  li + li { margin-top: 0.45em; }
  b { font-weight: 600; }
  .page { max-width: 1180px; margin: 0 auto; padding: 28px 24px 56px; display: flex; flex-direction: column; gap: 30px; }
  .masthead { display: grid; grid-template-columns: 1fr auto; gap: 20px 32px; align-items: end; padding-bottom: 20px; border-bottom: 2px solid var(--ink); }
  .eyebrow { font-size: 11.5px; letter-spacing: 0.09em; text-transform: uppercase; color: var(--muted); font-weight: 600; }
  .masthead h1 { font-size: 34px; font-weight: 600; letter-spacing: -0.01em; line-height: 1.1; margin-top: 6px; }
  .masthead .lede { margin-top: 8px; color: var(--ink-2); max-width: 60ch; }
  .stamp { font-size: 13.5px; line-height: 1.55; color: var(--ink-2); background: var(--surface); border: 1px solid var(--line); border-left: 4px solid var(--good); padding: 12px 16px; min-width: 320px; max-width: 440px; display: grid; grid-template-columns: auto 1fr; gap: 3px 14px; }
  .stamp.unverified { border-left-color: var(--warn); }
  .stamp .k { color: var(--muted); }
  .stamp .v { color: var(--ink); }
  .stamp .ok { color: var(--good); font-weight: 600; }
  .stamp .ko { color: var(--warn); font-weight: 600; }
  .stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
  .stat { background: var(--surface); border: 1px solid var(--line); padding: 14px 16px 12px; display: flex; flex-direction: column; gap: 2px; }
  .stat .label { font-size: 12px; color: var(--muted); letter-spacing: 0.04em; text-transform: uppercase; font-weight: 600; }
  .stat .value { font-size: 26px; font-weight: 600; letter-spacing: -0.01em; font-variant-numeric: tabular-nums; line-height: 1.2; }
  .stat .sub { font-size: 13px; color: var(--ink-2); }
  section { display: flex; flex-direction: column; gap: 12px; }
  .section-head { display: flex; align-items: baseline; justify-content: space-between; gap: 16px; flex-wrap: wrap; }
  .section-head h2 { font-size: 21px; font-weight: 600; }
  .section-head .zoom { font-size: 12.5px; color: var(--muted); font-weight: 500; }
  .panel { background: var(--surface); border: 1px solid var(--line); padding: 18px 20px; }
  .src { display: block; font-size: 12.5px; color: var(--muted); margin-top: 3px; }
  .timeline { overflow-x: auto; }
  .timeline svg { display: block; width: 100%; min-width: 780px; height: auto; }
  .timeline .rail { stroke: var(--line-strong); stroke-width: 2; }
  .timeline .rail-future { stroke: var(--line-strong); stroke-width: 2; stroke-dasharray: 5 5; }
  .timeline .node-done { fill: var(--accent); stroke: var(--accent); }
  .timeline .node-current { fill: var(--accent); stroke: var(--accent); }
  .timeline .node-ring { fill: none; stroke: var(--accent); stroke-width: 2; }
  .timeline .node-future { fill: var(--surface); stroke: var(--muted); stroke-width: 2; stroke-dasharray: 3 3; }
  .timeline .tag { font-family: var(--sans); font-size: 13px; font-weight: 600; fill: var(--ink); text-anchor: middle; }
  .timeline .tag-future { fill: var(--muted); }
  .timeline .date { font-family: var(--sans); font-size: 11px; fill: var(--muted); text-anchor: middle; }
  .timeline .what { font-family: var(--sans); font-size: 11.5px; fill: var(--ink-2); text-anchor: middle; }
  .timeline .badge { font-family: var(--sans); font-size: 10.5px; font-weight: 600; fill: var(--accent-ink); text-anchor: middle; letter-spacing: 0.06em; }
  .cols { display: grid; grid-template-columns: 1.1fr 1fr; gap: 16px; align-items: start; }
  .stack { display: flex; flex-direction: column; gap: 16px; }
  .todo { border-left: 4px solid var(--warn); box-shadow: var(--shadow); }
  .todo ol { margin: 0; padding-left: 1.3em; }
  .todo li + li { margin-top: 0.75em; }
  .facts { list-style: none; padding: 0; }
  .facts li { display: grid; grid-template-columns: 22px 1fr; gap: 8px; align-items: start; }
  .facts li + li { margin-top: 0.6em; }
  .facts .chip { margin-left: 6px; vertical-align: middle; }
  .dot { width: 12px; height: 12px; border-radius: 50%; margin-top: 7px; justify-self: center; border: 2px solid var(--good); background: var(--good-soft); }
  .dot.warn { border-color: var(--warn); background: var(--warn-soft); }
  .dot.neutral { border-color: var(--line-strong); background: var(--surface-2); }
  .sketch { list-style: none; padding: 0; display: grid; grid-template-columns: 1fr 1fr; gap: 6px 16px; }
  .sketch li { color: var(--ink-2); font-size: 14.5px; padding: 6px 0; border-bottom: 1px dashed var(--line); margin: 0; }
  .empty { color: var(--muted); font-size: 14.5px; }
  .chip { display: inline-flex; align-items: center; gap: 5px; font-size: 12px; font-weight: 600; letter-spacing: 0.02em; padding: 2px 8px; border-radius: 999px; white-space: nowrap; border: 1px solid transparent; }
  .chip::before { content: ""; width: 7px; height: 7px; border-radius: 50%; background: currentColor; }
  .chip-done { color: var(--good); background: var(--good-soft); }
  .chip-active { color: var(--accent-ink); background: var(--accent-soft); }
  .chip-partial { color: var(--warn); background: var(--warn-soft); }
  .chip-scoped { color: var(--ink-2); background: var(--surface-2); }
  .chip-later { color: var(--muted); background: transparent; border-color: var(--line); }
  .chip-later::before { background: transparent; border: 1.5px solid currentColor; width: 5px; height: 5px; }
  .chip-unverified { color: var(--warn); background: transparent; border-color: var(--warn); }
  .chip-ask { color: var(--crit); background: var(--crit-soft); }
  .tablewrap { overflow-x: auto; background: var(--surface); border: 1px solid var(--line); }
  table { border-collapse: collapse; width: 100%; min-width: 760px; font-size: 14.5px; }
  th, td { text-align: left; padding: 10px 14px; vertical-align: top; border-bottom: 1px solid var(--line); }
  th { font-size: 11.5px; letter-spacing: 0.07em; text-transform: uppercase; color: var(--muted); font-weight: 600; background: var(--surface-2); }
  tr:last-child td { border-bottom: none; }
  td.num { font-family: var(--mono); font-size: 12.5px; color: var(--ink-2); white-space: nowrap; }
  td.when { color: var(--muted); font-size: 13px; white-space: nowrap; }
  td .name { font-weight: 600; }
  td .quote { font-style: italic; color: var(--ink); }
  td.srcc { color: var(--muted); font-size: 13px; white-space: nowrap; }
  details { border: 1px solid var(--line); background: var(--surface); }
  details + details { margin-top: -1px; }
  summary { cursor: pointer; list-style: none; display: grid; grid-template-columns: 18px 72px 1fr auto; gap: 12px; align-items: baseline; padding: 10px 14px; user-select: none; }
  summary::-webkit-details-marker { display: none; }
  summary::before { content: "\\25B8"; color: var(--muted); font-size: 13px; }
  details[open] > summary::before { content: "\\25BE"; }
  summary:focus-visible { outline: 2px solid var(--accent); outline-offset: -2px; }
  summary .when { font-size: 13px; color: var(--muted); }
  summary .title { font-weight: 500; }
  summary .ver { font-size: 12.5px; color: var(--accent-ink); font-weight: 600; white-space: nowrap; }
  details .body { padding: 4px 14px 14px 44px; color: var(--ink-2); font-size: 14.5px; }
  details .body ul { padding-left: 1.1em; }
  details .body li + li { margin-top: 0.35em; }
  details.tech { margin-top: 4px; }
  details.tech summary { grid-template-columns: 18px 1fr; }
  details.tech .body { font-family: var(--mono); font-size: 12.5px; line-height: 1.7; padding-left: 44px; word-break: break-all; }
  .tree-controls { display: flex; gap: 8px; }
  .btn { font: inherit; font-size: 12.5px; font-weight: 500; color: var(--ink-2); background: var(--surface); border: 1px solid var(--line-strong); padding: 4px 10px; border-radius: 4px; cursor: pointer; }
  .btn:hover { border-color: var(--accent); color: var(--accent-ink); }
  .btn:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
  .rules { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; padding-top: 20px; border-top: 1px solid var(--line-strong); }
  .rules h3 { font-size: 12px; letter-spacing: 0.07em; text-transform: uppercase; color: var(--muted); margin-bottom: 6px; }
  .rules p, .rules li { font-size: 13.5px; color: var(--ink-2); }
  .rules ul { list-style: none; padding: 0; }
  .rules li { display: flex; justify-content: space-between; gap: 12px; border-bottom: 1px dashed var(--line); padding: 4px 0; margin: 0; }
  .rules li span:last-child { color: var(--ink); text-align: right; font-weight: 500; }
  @media (max-width: 900px) {
    .masthead { grid-template-columns: 1fr; align-items: start; }
    .stats { grid-template-columns: repeat(2, 1fr); }
    .cols { grid-template-columns: 1fr; }
    .rules { grid-template-columns: 1fr; }
    .sketch { grid-template-columns: 1fr; }
    summary { grid-template-columns: 18px 1fr; }
    summary .ver { grid-column: 2; }
    .stamp { max-width: none; }
  }
"""

SCRIPT = """
  (function () {
    var tree = document.getElementById("tree");
    if (!tree) return;
    var items = tree.querySelectorAll("details[data-id]");
    document.querySelectorAll("[data-tree]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var open = btn.getAttribute("data-tree") === "open";
        items.forEach(function (d) { if (!d.classList.contains("tech")) d.open = open; });
      });
    });
  })();
"""


def _plain(view: dict[str, Any]) -> bool:
    return view.get("style") != "TECHNICAL"


def scope_cell(scope: str | None, plain: bool, language: str = "FR") -> str:
    """The "Fiche" cell: a file path is a technical identifier the view adds itself."""
    if not scope:
        return "—"
    if not plain:
        return str(scope)
    entry = TEXT["cell.scope_sheet"]
    return entry.get(str(language).upper(), entry["FR"])


def _source(text: str | None, view: dict[str, Any] | None = None) -> str:
    view = view or {}
    label = _t(view, "src.label")
    mark = colon(view)
    body = esc(text) if text else _t(view, "src.unknown")
    return f'<span class="src">{label}{mark}{body}</span>'


def _facts(entries: Sequence[dict[str, Any]], view: dict[str, Any], empty: str) -> str:
    if not entries:
        return f'<p class="empty">{esc(empty)}</p>'
    items = []
    for entry in entries:
        tone = TONE_DOTS.get(entry.get("tone", "neutral"), " neutral")
        text = esc(entry.get("text") or entry.get("title"))
        if entry.get("title") and entry.get("detail"):
            text = f"<b>{esc(entry['title'])}</b> {esc(entry['detail'])}"
        elif entry.get("title") and not entry.get("text"):
            text = f"<b>{esc(entry['title'])}</b>"
        technical = entry.get("technical")
        if technical and not _plain(view):
            text += f" <code>{esc(technical)}</code>"
        items.append(f'<li><span class="dot{tone}"></span><div>{text}{_source(entry.get("source"), view)}</div></li>')
    return '<ul class="facts">' + "".join(items) + "</ul>"


def _todo(entries: Sequence[dict[str, Any]], view: dict[str, Any]) -> str:
    if not entries:
        return f'<p class="empty">{esc(_t(view, "empty.todo"))}</p>'
    items = []
    for entry in entries:
        text = f"<b>{esc(entry.get('title'))}</b>"
        if entry.get("detail"):
            text += f" {esc(entry['detail'])}"
        technical = entry.get("technical")
        if technical and not _plain(view):
            text += f" <code>{esc(technical)}</code>"
        items.append(f"<li>{text}{_source(entry.get('source'), view)}</li>")
    return "<ol>" + "".join(items) + "</ol>"


def _sketch(entries: Sequence[dict[str, Any]], view: dict[str, Any]) -> str:
    if not entries:
        return f'<p class="empty">{esc(_t(view, "empty.far"))}</p>'
    detail = view.get("zoom", {}).get("far") == "DETAIL"
    items = []
    for entry in entries:
        text = esc(entry.get("title"))
        if detail and entry.get("detail"):
            text += f" — {esc(entry['detail'])}"
        items.append(f"<li>{text}</li>")
    sources = list(dict.fromkeys(
        part.strip() for entry in entries if entry.get("source") for part in str(entry["source"]).split(" ; ") if part.strip()
    ))
    trailer = _source(" ; ".join(sources), view) if sources else ""
    return '<ul class="sketch">' + "".join(items) + "</ul>" + trailer


def _timeline(view: dict[str, Any]) -> str:
    versions = view.get("versions") or []
    if not versions:
        return ""
    count = len(versions) + 1
    step = 900 / max(count - 1, 1)
    xs = [46 + round(index * step) for index in range(count)]
    current_index = next((index for index, version in enumerate(versions) if version.get("current")), len(versions) - 1)
    parts = [
        f'<line class="rail" x1="{xs[0]}" y1="70" x2="{xs[len(versions) - 1]}" y2="70"></line>',
        f'<line class="rail-future" x1="{xs[len(versions) - 1]}" y1="70" x2="{xs[-1]}" y2="70"></line>',
    ]
    # Label lines: the denser the timeline, the shorter each line, so neighbours never collide.
    per_line = 1 if step < 95 else 2
    max_lines = 3

    def label_lines(label: str) -> list[str]:
        words = str(label).split()
        lines = [" ".join(words[i:i + per_line]) for i in range(0, len(words), per_line)]
        return lines[:max_lines]

    for index, version in enumerate(versions):
        x = xs[index]
        if index == current_index:
            parts.append(f'<circle class="node-ring" cx="{x}" cy="70" r="13"></circle>')
            parts.append(f'<circle class="node-current" cx="{x}" cy="70" r="7"></circle>')
            parts.append(f'<text class="badge" x="{x}" y="22">ACTUELLE</text>')
        else:
            parts.append(f'<circle class="node-done" cx="{x}" cy="70" r="7"></circle>')
        parts.append(f'<text class="tag" x="{x}" y="44">{esc(version.get("version"))}</text>')
        parts.append(f'<text class="date" x="{x}" y="96">{esc(short_date(str(version.get("date", "")), str(view.get("language", "FR"))))}</text>')
        for line_index, line in enumerate(label_lines(version.get("label", ""))):
            parts.append(f'<text class="what" x="{x}" y="{114 + 15 * line_index}">{esc(line)}</text>')
    x = xs[-1]
    upcoming = view.get("next_version") or {}
    parts.append(f'<circle class="node-future" cx="{x}" cy="70" r="7"></circle>')
    parts.append(f'<text class="tag tag-future" x="{x}" y="44">{esc(upcoming.get("version") or _t(view, "version.next"))}</text>')
    parts.append(f'<text class="date" x="{x}" y="96">{esc(upcoming.get("date") or _t(view, "version.upcoming"))}</text>')
    for line_index, line in enumerate(label_lines(upcoming.get("label") or _t(view, "version.to_scope"))):
        parts.append(f'<text class="what" x="{x}" y="{114 + 15 * line_index}">{esc(line)}</text>')
    return (
        f'<section><div class="section-head"><h2>{esc(_t(view, "h.versions"))}</h2>'
        f'<span class="zoom">{esc(_t(view, "h.versions_zoom"))}</span></div>'
        f'<div class="panel timeline"><svg viewBox="0 0 1000 160" role="img" aria-label="{esc(_t(view, "h.versions"))}">'
        + "".join(parts) + "</svg></div></section>"
    )


def _ideas_table(view: dict[str, Any]) -> str:
    ideas = view.get("ideas") or []
    if not ideas:
        body = f'<p class="empty">{esc(_t(view, "empty.ideas"))}</p>'
    else:
        rows = []
        for idea in ideas:
            target = idea.get("target")
            became = esc(idea.get("note") or "")
            if target:
                became = (became + " " if became else "") + f"<span class=\"srcc\">→ {esc(target)}</span>"
            rows.append(
                f'<tr><td class="when">{esc(short_date(str(idea.get("stated_at", "")), str(view.get("language", "FR"))))}</td>'
                f'<td><span class="quote">« {esc(idea.get("quote"))} »</span></td>'
                f"<td>{became or '—'}</td>"
                f"<td>{chip(IDEA_CHIPS.get(idea.get('state', ''), 'scoped'), idea_label_in(str(idea.get('state', '')), str(view.get('language', 'FR'))))}</td>"
                f'<td class="srcc">{esc(idea.get("source"))}</td></tr>'
            )
        body = (
            f'<div class="tablewrap"><table><thead><tr><th>{esc(_t(view, "col.when"))}</th><th>{esc(_t(view, "col.idea"))}</th>'
            f'<th>{esc(_t(view, "col.became"))}</th><th>{esc(_t(view, "col.state"))}</th><th>{esc(_t(view, "col.source"))}</th>'
            '</tr></thead><tbody>' + "".join(rows) + "</tbody></table></div>"
        )
    return (
        f'<section><div class="section-head"><h2>{esc(_t(view, "h.ideas"))}</h2>'
        f'<span class="zoom">{esc(_t(view, "h.ideas_zoom"))}</span></div>' + body +
        f'<span class="src">{esc(_t(view, "h.ideas_states"))}</span></section>'
    )


def _chantiers_table(view: dict[str, Any]) -> str:
    chantiers = view.get("chantiers") or []
    if not chantiers:
        return ""
    rows = []
    for item in chantiers:
        scope = scope_cell(item.get("scope"), _plain(view), str(view.get("language", "FR")))
        rows.append(
            f'<tr><td class="num">{esc(item.get("id"))}</td><td><span class="name">{esc(item.get("title"))}</span></td>'
            f"<td>{chip(CHANTIER_CHIPS.get(item.get('state', ''), 'scoped'), chantier_label(str(item.get('state', '')), str(view.get('language', 'FR'))))}</td>"
            f"<td>{esc(item.get('summary'))}</td><td class=\"srcc\">{esc(scope)}</td></tr>"
        )
    return (
        f'<section><div class="section-head"><h2>{esc(_t(view, "h.chantiers_template"))}</h2>'
        f'<span class="zoom">{esc(_t(view, "h.chantiers_template_zoom"))}</span></div>'
        f'<div class="tablewrap"><table><thead><tr><th>{esc(_t(view, "col.number"))}</th><th>{esc(_t(view, "col.chantier"))}</th>'
        f'<th>{esc(_t(view, "col.state"))}</th><th>{esc(_t(view, "col.where"))}</th><th>{esc(_t(view, "col.sheet"))}</th>'
        '</tr></thead><tbody>'
        + "".join(rows) + "</tbody></table></div></section>"
    )


def _work_items_table(view: dict[str, Any]) -> str:
    items = view.get("work_items") or []
    if view.get("role") == "PROJECT_TEMPLATE":
        return ""
    if not items:
        body = f'<p class="empty">{esc(_t(view, "empty.work_items"))}</p>'
    else:
        rows = []
        plain = _plain(view)
        for item in items:
            status = str(item.get("status", ""))
            detail = esc(item.get("objective") or "")
            missing = item.get("missing_gates") or []
            if missing and status not in {"DONE", "REJECTED", "SUPERSEDED"}:
                detail += f" <span class=\"srcc\">{esc(_t(view, 'cell.missing', missing=', '.join(missing)))}</span>"
            if item.get("block"):
                detail += f" <span class=\"srcc\">{esc(_t(view, 'cell.blocked', condition=item['block'].get('resume_condition')))}</span>"
            reference = item.get("display_reference") or item.get("work_item_id")
            technical = "" if plain else f' <code>{esc(item.get("branch"))}</code>'
            rows.append(
                f'<tr><td class="num">{esc(item.get("work_item_id"))}</td>'
                f'<td><span class="name">{esc(item.get("title"))}</span> <span class="srcc">{esc(reference)}</span>{technical}</td>'
                f"<td>{chip(WORK_ITEM_CHIPS.get(status, 'scoped'), work_item_label(status, str(view.get('language', 'FR'))))}</td>"
                f"<td>{detail}</td><td class=\"srcc\">{esc(item.get('human_gate') or '—')}</td></tr>"
            )
        body = (
            f'<div class="tablewrap"><table><thead><tr><th>{esc(_t(view, "col.number"))}</th><th>{esc(_t(view, "col.chantier"))}</th>'
            f'<th>{esc(_t(view, "col.state"))}</th><th>{esc(_t(view, "col.where"))}</th><th>{esc(_t(view, "col.decision"))}</th>'
            '</tr></thead><tbody>'
            + "".join(rows) + "</tbody></table></div>"
        )
    return (
        f'<section><div class="section-head"><h2>{esc(_t(view, "h.chantiers"))}</h2>'
        f'<span class="zoom">{esc(_t(view, "h.chantiers_zoom"))}</span></div>' + body + "</section>"
    )


def _past(view: dict[str, Any]) -> str:
    entries = view.get("past") or []
    expanded = view.get("zoom", {}).get("past") == "EXPANDED"
    parts = []
    for index, entry in enumerate(entries):
        details = "".join(f"<li>{esc(line)}</li>" for line in entry.get("details") or [])
        version = esc(entry.get("version") or "")
        parts.append(
            f'<details data-id="p{index}"{" open" if expanded else ""}><summary><span class="when">{esc(short_date(str(entry.get("date", "")), str(view.get("language", "FR"))))}</span>'
            f'<span class="title">{esc(entry.get("title"))}</span><span class="ver">{version}</span></summary>'
            f'<div class="body"><ul>{details}</ul>{_source(entry.get("sources"), view)}</div></details>'
        )
    if not parts:
        parts.append(f'<p class="empty">{esc(_t(view, "empty.past"))}</p>')
    verification = view.get("verification", {})
    tech_lines = [
        esc(_t(view, "tech.generated", when=view.get("generated_at"), style=view.get("style"), role=view.get("role"))),
        f"branch {esc(verification.get('branch'))} · HEAD {esc(verification.get('head'))} · tag {esc(verification.get('version_tag') or 'none')}",
        f"audit {esc(verification.get('audit_status'))} · skeleton {esc(verification.get('skeleton_version'))} · core "
        f"{esc(_t(view, 'tech.aligned' if verification.get('core_aligned') else 'tech.drifted'))} · hook {esc(verification.get('hooks'))}",
    ]
    remotes = verification.get("remotes") or {}
    if remotes:
        tech_lines.append("remotes: " + " · ".join(f"{esc(name)} {esc(head)}" for name, head in sorted(remotes.items())))
    if verification.get("tests_count") is not None:
        tech_lines.append(esc(_t(view, "tech.tests", count=verification.get("tests_count"))))
    tech_lines.append(f"sources_digest {esc(verification.get('sources_digest'))}")
    for entry in verification.get("sources") or []:
        tech_lines.append(f"{esc(entry.get('path'))} sha256={esc(entry.get('sha256'))}")
    for entry in view.get("technical_notes") or []:
        tech_lines.append(esc(entry))
    parts.append(
        f'<details class="tech" data-id="tech"><summary><span class="title">{esc(_t(view, "tech.summary"))}</span></summary>'
        '<div class="body">' + "<br>".join(tech_lines) + "</div></details>"
    )
    return (
        f'<section><div class="section-head"><h2>{esc(_t(view, "h.past"))}</h2><div class="tree-controls">'
        f'<button class="btn" type="button" data-tree="open">{esc(_t(view, "btn.expand"))}</button>'
        f'<button class="btn" type="button" data-tree="close">{esc(_t(view, "btn.collapse"))}</button></div></div>'
        '<div class="tree" id="tree">' + "".join(parts) + "</div></section>"
    )


def _stats(view: dict[str, Any]) -> str:
    tiles = view.get("stats") or []
    if not tiles:
        return ""
    cells = "".join(
        f'<div class="stat"><span class="label">{esc(tile.get("label"))}</span><span class="value">{esc(tile.get("value"))}</span>'
        f'<span class="sub">{esc(tile.get("sub"))}</span></div>'
        for tile in tiles[:4]
    )
    return f'<div class="stats" aria-label="{esc(_t(view, "stats.label"))}">{cells}</div>'


def _stamp(view: dict[str, Any]) -> str:
    verification = view.get("verification", {})
    rows = []
    for key, value, klass in verification.get("banner") or []:
        rows.append(f'<span class="k">{esc(key)}</span><span class="{esc(klass or "v")}">{esc(value)}</span>')
    unverified = " unverified" if verification.get("audit_status") != "PASS" else ""
    return f'<div class="stamp{unverified}" aria-label="{esc(_t(view, "stamp.label"))}">{"".join(rows)}</div>'


def render_html(view: dict[str, Any]) -> str:
    """A self-contained page: inline CSS and script, no external resource but the fonts."""
    settings = view.get("settings") or {}
    plain = _plain(view)
    left = (
        f'<section><div class="section-head"><h2>{esc(_t(view, "h.now"))}</h2><span class="zoom">{esc(_t(view, "h.detail"))}</span></div>'
        f'<div class="panel">{_facts(view.get("now") or [], view, _t(view, "empty.now"))}</div></section>'
        f'<section><div class="section-head"><h2>{esc(_t(view, "h.waiting"))}</h2><span class="zoom">{esc(_t(view, "h.waiting_zoom"))}</span></div>'
        f'<div class="panel todo">{_todo(view.get("waiting_for_owner") or [], view)}</div></section>'
    )
    right = (
        f'<section><div class="section-head"><h2>{esc(_t(view, "h.next"))}</h2><span class="zoom">{esc(_t(view, "h.detail"))}</span></div>'
        f'<div class="panel">{_facts(view.get("next_steps") or [], view, _t(view, "empty.next"))}</div></section>'
        f'<section><div class="section-head"><h2>{esc(_t(view, "h.far"))}</h2><span class="zoom">{esc(_t(view, "settings.titles_only"))}</span></div>'
        f'<div class="panel">{_sketch(view.get("later") or [], view)}</div></section>'
    )
    rules = (
        f'<footer class="rules"><div><h3>{esc(_t(view, "rules.title"))}</h3><p>{esc(_t(view, "rules.body"))}</p></div>'
        f'<div><h3>{esc(_t(view, "settings.title"))}</h3><ul>'
        f'<li><span>{esc(_t(view, "settings.refresh"))}</span><span>{esc(settings.get("regeneration_label", "—"))}</span></li>'
        f'<li><span>{esc(_t(view, "settings.style"))}</span><span>{esc(_t(view, "prj.style_plain" if plain else "prj.style_technical"))}</span></li>'
        f'<li><span>{esc(_t(view, "settings.past"))}</span>'
        f'<span>{esc(_t(view, "settings.expanded" if view.get("zoom", {}).get("past") == "EXPANDED" else "settings.folded"))}</span></li>'
        f'<li><span>{esc(_t(view, "settings.far"))}</span>'
        f'<span>{esc(_t(view, "settings.detailed" if view.get("zoom", {}).get("far") == "DETAIL" else "settings.titles_only"))}</span></li>'
        f'<li><span>{esc(_t(view, "settings.form"))}</span><span>{esc(_t(view, "settings.form_value"))}</span></li>'
        f'<li><span>{esc(_t(view, "settings.language"))}</span><span>{esc(settings.get("language_label", "—"))}</span></li>'
        "</ul></div>"
        f'<div><h3>{esc(_t(view, "howto.title"))}</h3><p>{esc(_t(view, "howto.body"))}</p></div></footer>'
    )
    body = (
        f'<title>{esc(view.get("title"))}</title>'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">'
        f"<style>{CSS}</style>"
        '<div class="page"><header class="masthead"><div>'
        f'<div class="eyebrow">{esc(view.get("eyebrow"))}</div><h1>{esc(view.get("title"))}</h1>'
        f'<p class="lede">{esc(view.get("lede"))}</p></div>{_stamp(view)}</header>'
        + _stats(view) + _timeline(view)
        + f'<div class="cols"><div class="stack">{left}</div><div class="stack">{right}</div></div>'
        + _ideas_table(view) + _chantiers_table(view) + _work_items_table(view) + _past(view) + rules
        + f"</div><script>{SCRIPT}</script>"
    )
    return (
        "<!doctype html>\n<html lang=\"fr\">\n<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n"
        + body.replace("<title>", "\n<title>", 1).replace("</title>", "</title>\n</head>\n<body>", 1)
        + "\n</body>\n</html>\n"
    )


# --- Markdown ---------------------------------------------------------------------------

def _md_entries(entries: Sequence[dict[str, Any]], view: dict[str, Any], numbered: bool = False) -> str:
    if not entries:
        return "_Rien._\n"
    lines = []
    for index, entry in enumerate(entries, start=1):
        text = entry.get("text") or entry.get("title") or ""
        if entry.get("title") and entry.get("detail"):
            text = f"**{entry['title']}** {entry['detail']}"
        technical = entry.get("technical")
        if technical and not _plain(view):
            text += f" `{technical}`"
        source = entry.get("source")
        if source:
            text += f" _({_t(view, 'md.source_label')}{colon(view)}{source})_"
        prefix = f"{index}. " if numbered else "- "
        lines.append(prefix + md_cell(text).replace("¦", "|"))
    return "\n".join(lines) + "\n"


def render_markdown(view: dict[str, Any]) -> str:
    verification = view.get("verification", {})
    lines = [
        f"<!-- ROADMAP_VIEW sources_digest={verification.get('sources_digest')} generated_at={view.get('generated_at')} head={verification.get('head')} -->",
        f"# {view.get('title')}",
        "",
        _t(view, "md.lede"),
        "",
        f"## {_t(view, 'h.verification')}",
        "",
    ]
    for key, value, _ in verification.get("banner") or []:
        lines.append(f"- {key}{colon(view)}{value}")
    lines += ["", f"## {_t(view, 'h.now')}", "", _md_entries(view.get("now") or [], view),
              f"## {_t(view, 'h.waiting')}", "", _md_entries(view.get("waiting_for_owner") or [], view, numbered=True),
              f"## {_t(view, 'h.next')}", "", _md_entries(view.get("next_steps") or [], view),
              f"## {_t(view, 'h.far')}", ""]
    later = view.get("later") or []
    lines.append("\n".join(f"- {md_cell(entry.get('title'))}" for entry in later) + "\n" if later else f"_{_t(view, 'md.nothing')}_\n")
    lines += [f"## {_t(view, 'h.ideas')}", "",
              f"| {_t(view, 'col.when')} | {_t(view, 'col.idea')} | {_t(view, 'col.became')} | {_t(view, 'col.state')} | {_t(view, 'col.source')} |",
              "|---|---|---|---|---|"]
    for idea in view.get("ideas") or []:
        became = idea.get("note") or ""
        if idea.get("target"):
            became = (became + " " if became else "") + f"→ {idea['target']}"
        lines.append(f"| {md_cell(idea.get('stated_at'))} | « {md_cell(idea.get('quote'))} » | {md_cell(became)} | {idea_label_in(str(idea.get('state', '')), str(view.get('language', 'FR')))} | {md_cell(idea.get('source'))} |")
    if not view.get("ideas"):
        lines.append(f"| — | {_t(view, 'md.no_idea')} | — | — | — |")
    lines.append("")
    if view.get("chantiers"):
        lines += [f"## {_t(view, 'h.chantiers_template')}", "",
                  f"| {_t(view, 'col.number')} | {_t(view, 'col.chantier')} | {_t(view, 'col.state')} | {_t(view, 'col.where')} | {_t(view, 'col.sheet')} |",
                  "|---|---|---|---|---|"]
        for item in view["chantiers"]:
            lines.append(f"| {item.get('id')} | {md_cell(item.get('title'))} | {chantier_label(str(item.get('state', '')), str(view.get('language', 'FR')))} | {md_cell(item.get('summary'))} | {md_cell(scope_cell(item.get('scope'), _plain(view), str(view.get('language', 'FR'))))} |")
        lines.append("")
    if view.get("role") != "PROJECT_TEMPLATE":
        lines += [f"## {_t(view, 'h.chantiers')}", "",
                  f"| {_t(view, 'col.number')} | {_t(view, 'col.chantier')} | {_t(view, 'col.state')} | {_t(view, 'col.where')} | {_t(view, 'col.decision')} |",
                  "|---|---|---|---|---|"]
        items = view.get("work_items") or []
        for item in items:
            status = str(item.get("status", ""))
            lines.append(f"| {item.get('work_item_id')} | {md_cell(item.get('title'))} | {work_item_label(status, str(view.get('language', 'FR')))} | {md_cell(item.get('objective'))} | {md_cell(item.get('human_gate'))} |")
        if not items:
            lines.append(f"| — | {_t(view, 'md.no_chantier')} | — | — | — |")
        lines.append("")
    lines += [f"## {_t(view, 'h.past')}", ""]
    past = view.get("past") or []
    for entry in past:
        lines.append(f"- **{short_date(str(entry.get('date', '')), str(view.get('language', 'FR')))} — {md_cell(entry.get('title'))}**" + (f" ({entry['version']})" if entry.get("version") else ""))
        for detail in entry.get("details") or []:
            lines.append(f"  - {md_cell(detail)}")
        if entry.get("sources"):
            lines.append(f"  - _{_t(view, 'md.sources')} : {md_cell(entry['sources'])}_")
    if not past:
        lines.append(f"_{_t(view, 'empty.past')}_")
    lines += ["", f"## {_t(view, 'h.technicians')}", "",
              "- " + _t(view, "tech.generated", when=view.get("generated_at"), style=view.get("style"), role=view.get("role")),
              f"- branch `{verification.get('branch')}` · HEAD `{verification.get('head')}` · tag `{verification.get('version_tag') or 'none'}`",
              f"- audit {verification.get('audit_status')} · skeleton {verification.get('skeleton_version')} · core "
              f"{_t(view, 'tech.aligned' if verification.get('core_aligned') else 'tech.drifted')} · hook {verification.get('hooks')}"]
    remotes = verification.get("remotes") or {}
    if remotes:
        lines.append("- remotes: " + " · ".join(f"`{name}` `{head}`" for name, head in sorted(remotes.items())))
    scopes = [(item.get("id"), item.get("scope")) for item in view.get("chantiers") or [] if item.get("scope")]
    if scopes and _plain(view):
        # PLAIN moved the paths out of the table; they belong here, not nowhere.
        lines.append(f"- {_t(view, 'md.scope_sheets')}: " + " · ".join(f"{identifier} `{path}`" for identifier, path in scopes))
    lines.append(f"- sources_digest `{verification.get('sources_digest')}`")
    for entry in verification.get("sources") or []:
        lines.append(f"- `{entry.get('path')}` sha256=`{entry.get('sha256')}`")
    for note in view.get("technical_notes") or []:
        lines.append(f"- {note}")
    return "\n".join(lines) + "\n"


def parse_view_marker(text: str) -> dict[str, str] | None:
    """The generation marker of a committed Markdown view, or None when absent/invalid."""
    first = text.splitlines()[0] if text else ""
    match = VIEW_MARKER.match(first.strip())
    if match is None:
        return None
    return {"sources_digest": match.group(1), "generated_at": match.group(2), "head": match.group(3)}
