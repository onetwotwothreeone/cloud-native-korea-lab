# 39_GWAN_Kubernetes_Config_And_Secret_Refinement

## Purpose

This step refines how GWAN Kubernetes configuration is separated between ConfigMap and Secret.

The goal is simple:

- Non-sensitive settings go to ConfigMap.
- Sensitive values go to Secret.
- Deployments consume those values through env or envFrom.
- Plain passwords should not be hardcoded in Deployment or ConfigMap.

## Why this matters

In a cloud native system, application behavior changes depending on the environment.

Examples:

- local
- dev
- staging
- production

ConfigMap is used for normal configuration such as database host, port, database name, and local file path.

Secret is used for sensitive values such as passwords.

## HYEAN/GWAN meaning

For HYEAN/GWAN, this step supports safer operation of the prevention-oriented intelligence system.

GWAN should be able to run in different environments without rewriting source code.

This allows HYEAN to keep the same intelligence logic while changing only the surrounding runtime configuration.

## Expected separation

### ConfigMap

- DATABASE_HOST
- DATABASE_PORT
- DATABASE_NAME
- DATABASE_DIALECT
- HYEAN_MEMORY_JSONL_PATH

### Secret

- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_DB

## Expected checks

- gwan-api consumes ConfigMap values.
- gwan-api consumes PostgreSQL password from Secret.
- postgres consumes Secret values.
- ConfigMap does not contain password.
- Deployment does not hardcode a raw password.
