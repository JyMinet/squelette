# Contributing

Squelette is small on purpose. Contributions are welcome when they keep it that way.

## Before you write

- Open an issue first, in English or in French: the problem you hit, the failure scenario, the smallest change that fixes it. `OMIT > ACTIVATE WITHOUT NEED` — a capability is never added because it exists.
- The core — the files listed in `provenance/core-manifest.v1.json`: the controller, its schemas, its tests, the commit hook and the agent doctrine — changes only in this repository, never inside a derived project. A generic improvement is brought back here, then reaches projects through `template-upgrade`.
- If you are an AI agent: read `AGENTS.md` first (`CLAUDE.md` if you are Claude). Its rules apply to you here too.

## A change

1. Fork, branch from `main`, one change per branch.
2. Standard-library Python only: no new dependency, no service, no network.
3. `python3 -B -m unittest discover -s tests` must pass, including the hello-squelette replay. If you changed what the controller prints, regenerate the transcript and the README block: `python3 -B examples/hello-squelette/demo.py --write`.
4. A change to a core file regenerates the manifest: `python3 -B scripts/project_control.py core-manifest --write --version MAJOR.MINOR.PATCH` (the maintainer sets the version).
5. Git: explicit paths only — never `git add .`, `git add -A`, `git reset --hard`, `git clean` or a force push. The commit gate (`python3 -B scripts/project_control.py install-gate`, installed outside the worktree) audits every commit; a maintenance of the core commits with `PROJECT_CONTROL_HOOK_OVERRIDE="<mandate>"`, and the mandate is part of the record.
6. Commit messages and tags are in French in this repository (its maintainer's rule). The first screen of the README is bilingual; the detailed documentation is in French; controller messages are in French for now.
7. Open a pull request that names the failure scenario the change fixes, or the need it serves. No demonstrated scenario, no change: an observation is welcome as an issue.

## Decisions

The Project Owner — the maintainer — decides on scope, versions and promotions. Every version of the template is a tag (`v3.x.y`) promoted by a recorded decision in `provenance/CHANGELOG.md`, with its maintenance report under `provenance/maintenance/`. A pull request is a proposal; the decision is recorded there.

## En français

Ouvrir d'abord une issue (le problème, le scénario d'échec, le plus petit changement utile) ; le core ne se modifie qu'ici, jamais dans un projet dérivé ; Python standard, sans dépendance ; tests, audits et démo verts ; chemins Git explicites, jamais d'ajout global ; commits et tags en français ; sans scénario d'échec démontré, pas de changement ; le Project Owner tranche.
