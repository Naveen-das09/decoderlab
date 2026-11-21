## Summary
<!-- User-visible behavior and why it matters -->

## Issue / acceptance criteria
<!-- Link issue, concrete criteria and scope exclusions -->

## Verification
- [ ] Relevant tests run, with exact commands and evidence
- [ ] CI checks pass or blockers are explained
- [ ] Documentation / ADR updated
- [ ] No credentials, private datasets or costly services added
- [ ] No unexpected public compute endpoint or unbounded job

## Scientific review (when QEC/ML changes)
- [ ] Code, distance, logical basis and noise channels clearly specified
- [ ] Error/failure semantics and sample sizes correct
- [ ] Seeds, dependencies, circuit/model identity and provenance captured
- [ ] Statistical uncertainty appropriate; no fabricated measurements
- [ ] Real integration tested or explicit test gap documented

## Design review (when UI/chart changes)
- [ ] Responsive desktop and mobile layouts verified
- [ ] Keyboard/screen-reader equivalent available
- [ ] Loading, empty, error and missing-data states tested
- [ ] Data origin and units clearly visible
- [ ] Screenshots or short video supplied (no private data)

## Risk / rollback
<!-- Breaking API changes, data migration, dependencies and recovery -->

**Merge policy:** draft PR until owner review. No autonomous merge.