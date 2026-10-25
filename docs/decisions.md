# Project Decision Log

This document records significant project decisions, their rationale, alternatives considered and any outstanding questions.

## 25 October 2026 — Initial Project Direction

**Decision status:** Provisional — subject to API exploration.

**Proposed audience:** London local authority transport and environmental teams.

**Proposed focus:** Investigate nitrogen dioxide (NO₂) measurements at selected roadside and urban-background monitoring sites, focusing on rush-hour patterns and the completeness of monitoring data.

### Alternatives Considered

- Geographical comparisons of pollution levels across London.
- Air-quality patterns during school travel hours.
- Monitoring-site data completeness and reliability.
- Identification of unusual pollution events.

### Rationale

The proposed direction combines a clear question for a defined audience with opportunities to demonstrate historical data collection, data quality checks and useful visualisations.

A geographical monitoring-site map and an hourly heat map are being considered as possible outputs.

### Outstanding Questions

- Which monitoring sites currently provide suitable NO₂ measurements?
- Are both roadside and urban-background sites available?
- How complete and recent are their measurements?
- What fields and relationships does the API provide?
- How should the pipeline handle missing or delayed readings?
- What data model will best support incremental updates without duplicates?

The final scope and implementation approach will be determined after investigating the API and its data.