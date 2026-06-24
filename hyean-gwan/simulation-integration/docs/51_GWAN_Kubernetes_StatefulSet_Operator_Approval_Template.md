# 51_GWAN_Kubernetes_StatefulSet_Operator_Approval_Template

## Purpose

This document provides the manual operator approval template before any real PostgreSQL Deployment to StatefulSet cutover.

## Current Status

CURRENT_DECISION: NO_GO

Real migration must remain blocked until the operator explicitly approves it.

## Operator Approval Template

### 1. Operator Information

- Operator Name:
- Approval Date:
- Approval Time:
- Environment:
- Namespace: hyean-gwan

### 2. Required Pre-Checks

The operator must confirm all items below.

- [ ] pytest passed
- [ ] GitHub Actions passed
- [ ] PostgreSQL Deployment is available
- [ ] PostgreSQL Pod is running
- [ ] postgres-data PVC is Bound
- [ ] PostgreSQL Service exists
- [ ] PostgreSQL Secret exists
- [ ] GWAN API ConfigMap exists
- [ ] PostgreSQL backup/restore baseline passed
- [ ] StatefulSet draft manifest renders successfully
- [ ] StatefulSet migration dry-run passed
- [ ] StatefulSet rollback dry-run passed
- [ ] Cutover checklist passed

### 3. Risk Review

The operator must review these risks before approval.

- Data loss risk
- Backup restore failure risk
- Service downtime risk
- DNS or Service selector mismatch risk
- PVC binding issue risk
- Rollback failure risk

### 4. Approval Decision

Choose only one.

- [ ] APPROVED
- [ ] NOT APPROVED

## Required Approval Variable

Real migration can proceed only when the operator explicitly sets:

APPROVED_BY_OPERATOR=true

Until then:

APPROVED_BY_OPERATOR=false

FINAL_DECISION=NO_GO

## Final Rule

No real StatefulSet migration should be executed from this template.

This document only prepares the manual approval record.

## Next Recommended Step

52_GWAN_Kubernetes_StatefulSet_Manual_Approval_Record
