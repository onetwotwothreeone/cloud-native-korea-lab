# Codex Prompt: GWAN Kubernetes SecurityContext Baseline

You are working in the HYEAN/GWAN project.

Add and maintain Kubernetes SecurityContext as preventive runtime control.

Expected baseline:

GWAN API:

- runAsNonRoot: true
- runAsUser: 1000
- runAsGroup: 1000
- fsGroup: 1000
- seccompProfile: RuntimeDefault
- allowPrivilegeEscalation: false
- privileged: false
- readOnlyRootFilesystem: true
- capabilities.drop: ALL
- /tmp mounted as emptyDir

PostgreSQL:

- fsGroup: 999
- seccompProfile: RuntimeDefault
- allowPrivilegeEscalation: false
- privileged: false
- readOnlyRootFilesystem: false
- capabilities.drop: ALL

Explain this as least privilege and prevention-oriented runtime hardening.
