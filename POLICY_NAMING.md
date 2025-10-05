# Inclusive Naming and Content Compliance (Maps/UGC)

This repository follows an inclusive naming policy suitable for submission to game platforms and official content pools.

- No slurs, stereotyping, harassment, or sexualized terms in any identifiers, filenames, comments, or asset metadata. This includes internal/debug assets that are not visible in-game.
- Avoid culture-war/political, religious, or violent-extremist references unless explicitly required by the narrative and approved by the publisher.
- Prefer descriptive, neutral names, e.g. `cat_counter`, `train_gate_open`, `fog_density_step`.
- Use English-only identifiers for cross-team readability.
- Enforce pre-commit audits with `tools/audit_identifiers.py` in CI. Fail builds on findings.

Suggested CI step:
```
python3 tools/audit_identifiers.py --root . --include ".vmf,.vmap,.nut,.lua,.cfg,.txt,.json,.xml,.kv,.kv3"
```

Remediation protocol when violations are found:
- Rename identifiers to neutral terms; do not “mask” spelling.
- Rebuild/export assets and re-test.
- Document the change in a short changelog entry (what/why/where), e.g. `RENAME: math_counter targetname from <redacted> to cat_counter`.
- Add a repo-wide commit message tag `compliance:` for audit trail.

This policy exists to protect collaborators, players, and publishing partners and is non-negotiable for official submissions.

