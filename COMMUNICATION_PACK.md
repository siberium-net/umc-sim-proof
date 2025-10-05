# Transit — Incident and Remediation Pack

This pack contains draft texts to communicate with stakeholders about the map takedown and remediation plan.

## 1) Publisher-facing note (to Valve)

Subject: Transit — Immediate Remediation and Compliance Plan

Hello Valve Team,

We acknowledge and regret that an internal identifier in the Transit map contained an offensive term. The string was not intended for player exposure, but we accept that any presence is unacceptable. We have:
- audited the project tree,
- removed the term and any similar terms,
- instituted pre‑submission lint checks (see attached `POLICY_NAMING.md` and `tools/audit_identifiers.py`).

Request:
- We request a defined cure window to submit a clean build and to furnish audit logs.
- We agree to content policy alignment and propose adding the attached compliance checklist to our agreement.

Thank you for the opportunity to fix this responsibly.

## 2) Public statement (players)

We discovered an offensive internal identifier in a tool script for Transit. It should never have been there. We removed it, audited the project, and added safeguards so it cannot happen again. We’re sorry. If you encountered coverage of this issue, please know the map itself never intended to depict or condone hateful content. We’ve asked Valve to review a clean build.

## 3) Q&A talking points
- Why was the map removed? — A content policy violation in internal files (identifier). Not acceptable. Fixed.
- Will it be back? — We’ve requested review of a clean build and will follow all guidance.
- Who is responsible? — The team takes responsibility as a group. We’ve instituted preventive controls.
- What changed? — Renamed identifiers; added automated audits; updated submission checklist.

## 4) Timeline
- T0: Takedown notice.
- T0+1d: Full repo scan, renames, new build; furnish audit logs to Valve.
- T0+2–3d: Valve review; hotfixes as needed.
- T0+?d: Reinstatement or further changes.

