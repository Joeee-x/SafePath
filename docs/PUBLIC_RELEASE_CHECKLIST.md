# Public Release Checklist

Run this checklist before making the repository public or pushing new changes.

- [ ] Confirm that every committed data record is synthetic or has written publication approval.
- [ ] Remove real organization names, addresses, contacts, platform links, referral codes, screenshots, and raw research exports.
- [ ] Remove user-provided text, free-form notes, and any information that can be linked back to an individual.
- [ ] Remove credentials, environment files, deployment configuration, local paths, IDE settings, and generated database files.
- [ ] Confirm the repository has no inherited Git history from the private implementation.
- [ ] Run `python -m unittest discover -s tests -v`.
- [ ] Run `python scripts/validate_public_repo.py`.
- [ ] Inspect `git status --short` and `git log --oneline` before the first push.

The validator is a guardrail, not a substitute for human review. It checks a deliberately conservative set of patterns and rejects non-demo data files.
