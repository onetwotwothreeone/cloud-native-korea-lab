# 60_GWAN_Kubernetes_StatefulSet_Migration_Risk_Register

## Purpose

Migration Risk Register

This document lists the major risks before a future PostgreSQL Deployment to StatefulSet migration.

This step does not execute real migration.

The goal is to identify risks before action, keep migration blocked, and protect GWAN memory.

## HYEAN/GWAN Safety Principle

HYEAN is a prevention-first survival intelligence service.

GWAN must protect memory, continuity, and operator trust.

A database is not just a container.

A database is memory.

Therefore, migration risk must be reviewed before migration execution.

## Current Decision State

CURRENT_DECISION=NO_GO

APPROVED_BY_OPERATOR=false

FINAL_DECISION=NO_GO

RISK_REGISTER_STATUS=REVIEW_ONLY

## Current Workload State

- PostgreSQL is still running as Deployment.
- PostgreSQL Pod is running.
- PostgreSQL PVC exists and is Bound.
- PostgreSQL Service exists.
- PostgreSQL Secret exists.
- GWAN API ConfigMap exists.
- No active PostgreSQL StatefulSet exists yet.
- Real migration has not been executed.

## Risk Register

| ID | Risk | Impact | Prevention | Recovery |
|---|---|---|---|---|
| R01 | Data loss during migration | Critical | Run backup/restore baseline before migration | Restore from verified backup |
| R02 | PostgreSQL downtime | High | Use pre-migration checks and operator approval | Roll back to Deployment |
| R03 | PVC mismatch | Critical | Confirm PVC name and mount path before migration | Stop migration and keep current Deployment |
| R04 | Secret mismatch | High | Verify gwan-postgres-secret before migration | Restore correct Secret values |
| R05 | ConfigMap mismatch | High | Verify DATABASE_HOST, DATABASE_PORT, DATABASE_NAME, DATABASE_USER | Restore gwan-api-config |
| R06 | Service routing error | High | Review postgres Service and future headless Service separately | Revert service routing |
| R07 | StatefulSet manifest error | High | Render draft and dry-run apply before real apply | Do not apply real StatefulSet |
| R08 | Readiness probe failure | Medium | Check pg_isready command before cutover | Keep old Deployment serving traffic |
| R09 | NetworkPolicy blocks traffic | High | Confirm GWAN API to PostgreSQL NetworkPolicy | Revert or update NetworkPolicy |
| R10 | Resource limit too small | Medium | Review CPU and memory requests/limits | Increase resource limits |
| R11 | Rollback plan missing | Critical | Keep rollback dry-run and rollback runbook ready | Execute approved rollback only |
| R12 | Operator approval confusion | Critical | Keep approval records explicit | Keep FINAL_DECISION=NO_GO until approved |
| R13 | CI passes but runtime fails | High | Run local Kubernetes checks after CI | Fix runtime issue before migration |
| R14 | Wrong image or tag | Medium | Verify GHCR image and deployment image | Roll back to known good image |
| R15 | Manual command mistake | Critical | Use reviewed command checklist | Stop and re-check before execution |

## Risk Decision

The migration risk level is still high.

The system must remain in NO_GO state.

The next safe action is more review, not execution.

## Not Allowed In This Step

- Do not create a live PostgreSQL StatefulSet.
- Do not delete the current PostgreSQL Deployment.
- Do not modify the existing PostgreSQL PVC.
- Do not switch database traffic.
- Do not execute real migration.
- Do not execute rollback.

## Review Result

Risk register exists.

Major migration risks are documented.

Prevention and recovery actions are documented.

Real migration remains blocked.

## Next Recommended Step

61_GWAN_Kubernetes_StatefulSet_Risk_Mitigation_Checklist
