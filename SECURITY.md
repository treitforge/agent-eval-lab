# Security policy

## Report a vulnerability

Use GitHub private vulnerability reporting when it is available for this repository. Do not open a public issue that contains an unredacted credential, private trajectory, unpublished task, or hidden verifier.

## Sensitive evaluation data

Raw trajectories can contain source code, prompts, paths, command output, environment values, and model responses. Treat them as sensitive until you review and redact them.

The default `.gitignore` excludes `.runs/`, `artifacts/`, `reports/`, and common local export names. This protection is not complete. Review staged files before every push.

The example runner accepts a path to an external Codex authentication file. It passes the path to Harbor. It never copies the file into this repository or prints its content.
