# hello-squelette

One governed change, replayed for real in a temporary copy of the template — a couple of seconds, nothing beyond Python 3 and Git (macOS / Linux).

```bash
python3 -B examples/hello-squelette/demo.py            # replay and print the transcript
python3 -B examples/hello-squelette/demo.py --verbose  # keep every PASS line of the controller's reports
python3 -B examples/hello-squelette/demo.py --check    # what the test suite runs: fail if the committed transcript drifted
python3 -B examples/hello-squelette/demo.py --write    # maintainers: refresh TRANSCRIPT.md and the README block
```

What happens: (1) the tracked tree becomes a fresh repository, with the commit hook installed; (2) Bootstrap Mode refuses business code; (3) a scripted Project Owner answers the FIRST_START interview and the closeout passes; (4) a human decision authorizes WI-001 through `create-work-item`; (5) the agent proves it has read the authorities, then starts; (6) a drift outside the authorized scope is refused; (7) the change is tested and integrated; (8) evidence is recorded and `close` marks the Work Item `DONE`.

`TRANSCRIPT.md` is generated, never edited by hand; the test suite replays the demo and fails if the transcript or the README block no longer match what the controller prints. The checkout you run the demo from is not modified (only `--write` touches the two generated files). A derived project does not replay the demo: it describes the template.

En français : une seule commande rejoue un changement gouverné complet dans une copie temporaire ; `TRANSCRIPT.md` est généré, jamais écrit à la main, et la suite de tests le compare à la vraie sortie du contrôleur ; le dépôt d'où l'on lance la démo n'est pas modifié.
