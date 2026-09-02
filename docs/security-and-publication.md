# Security and publication boundary

Use a public framework and a private challenge bank.

## Safe to publish

- Analyzer and dashboard source code.
- Format adapters and synthetic fixtures.
- Generic runner scripts.
- Evidence definitions and evaluation-axis routing.
- A toy task that is clearly marked as public and non-benchmark.
- Sanitized results from a retired task.

## Keep private for an active evaluation

- Agent-facing task instructions.
- Challenge codebases and seeded defects.
- Hidden verifiers and expected patches.
- Customer or production data.
- Raw trajectories that contain private source code or prompts.
- Authentication files, environment secrets, and service tokens.
- Human ratings and unpublished submission text.

## Publication checklist

Before you publish a report or retired case:

1. Search for tokens, credentials, email addresses, user names, and local paths.
2. Remove private source code and command output.
3. Remove active prompts, fixtures, and verifier assertions.
4. Confirm that the case is retired.
5. State which fields were removed or transformed.
6. Keep the original private artifact in an approved evidence location.

Public framework code does not make an active evaluation invalid by itself. Public task-specific answers can make the result a recognition test instead of a coding test.
