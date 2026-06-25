# 71_GWAN_Kubernetes_StatefulSet_Portfolio_Demo_Readme

## Purpose

This document is a portfolio-friendly README for the HYEAN/GWAN PostgreSQL StatefulSet migration safety demo.

PORTFOLIO_DEMO_README_STATUS=CREATED

## HYEAN Service Goal

HYEAN_SERVICE_GOAL=PREVENTIVE_SURVIVAL_INTELLIGENCE

HYEAN is a preventive survival intelligence service.

It observes risk, protects operational memory, and helps humans make safer decisions before damage happens.

## Demo Title

DEMO_TITLE=HYEAN_GWAN_POSTGRESQL_STATEFULSET_SAFETY_DEMO

## Current Demo Status

DEMO_STATUS=READY_FOR_PORTFOLIO_REVIEW  
POSTGRES_CURRENT_MODE=DEPLOYMENT_WITH_PVC  
STATEFULSET_STATUS=NOT_CREATED  
CURRENT_DECISION=NO_GO  
APPROVED_BY_OPERATOR=false  
FINAL_DECISION=NO_GO  
OPERATOR_FINAL_APPROVAL_STATUS=NOT_APPROVED  
FINAL_APPROVAL_GATE_STATUS=BLOCKED  
PREFLIGHT_STATUS=PASSED_BUT_BLOCKED  
PORTFOLIO_DEMO_SCRIPT_STATUS=CREATED  
MIGRATION_EXECUTION_ALLOWED=false  
REAL_MIGRATION_EXECUTED=false  
SECRET_VALUES_EXPORTED=false  

## What This Demo Proves

This demo proves that HYEAN/GWAN can prepare a risky database infrastructure change without executing it too early.

The system checks safety before action.

## Beginner Explanation

Think of PostgreSQL as the memory box of the service.

Moving the memory box is dangerous.

So GWAN checks backup, health, storage, approval, and secret safety first.

The important point is not moving fast.

The important point is moving safely.

## Architecture Summary

Current mode:

- PostgreSQL runs as Deployment
- PostgreSQL uses PVC for storage
- GWAN API runs as Deployment
- PostgreSQL StatefulSet is not created yet
- Final approval gate is blocked
- Real migration is not allowed

## Safety Checks

- Kubernetes namespace exists
- PostgreSQL Deployment is available
- PostgreSQL Pod is running
- PostgreSQL PVC is Bound
- PostgreSQL Service exists
- PostgreSQL Secret exists
- Secret values are not exported
- Backup file exists and is fresh
- Read-only DB integrity check passed
- Operator final approval is not granted
- Final approval gate remains blocked

## Portfolio Message

This project shows cloud-native operational maturity.

It does not simply run commands.

It creates evidence, checks risk, blocks unsafe execution, and explains the decision clearly.

## Interview Talking Point

I designed a Kubernetes-based PostgreSQL migration safety workflow for HYEAN/GWAN.

Instead of immediately migrating from Deployment to StatefulSet, I built safety checks for backup freshness, database integrity, Secret handling, operator approval, and final preflight status.

The result is a portfolio-ready demo that proves safe decision-making before infrastructure change.

## Community Learning Point

Cloud Native is not only about deploying applications.

It is also about knowing when not to deploy, when not to migrate, and how to protect data before making changes.

## Next Recommended Step

72_GWAN_Kubernetes_StatefulSet_Portfolio_Demo_Runbook
