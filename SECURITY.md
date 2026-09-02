# Security policy

## Report a vulnerability

Use GitHub private vulnerability reporting. Do not put a credential or private evaluation file in a public issue.

## Sensitive evaluation data

Raw trajectories can contain private data. This data can include source code, prompts, paths, command output, environment values, and model responses.

Treat each raw trajectory as sensitive. Review and redact the trajectory before you share it.

The default `.gitignore` excludes common run and report paths. This protection is not complete. Review all staged files before each push.

The example runner accepts a path to an external Codex authentication file. It gives only the path to Harbor. It does not copy or print the file.
