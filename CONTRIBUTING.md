# Contributing to Rah-e-Ravaan

## Branch Naming

Use the following format:

- `main` — stable code
- `feature/<short-description>` — new features
- `fix/<short-description>` — bug fixes
- `chore/<short-description>` — setup and maintenance

Example:

`feature/user-authentication`

## Commits

Use clear, concise commit messages.

Format:

`<type>: <description>`

Examples:

- `feat: add trip creation API`
- `fix: correct login validation`
- `chore: update dependencies`
- `docs: update setup instructions`

## Pull Requests

- Create a branch from `main`.
- Keep PRs focused on one change.
- Explain what was changed.
- Mention related Jira ticket(s).
- Ensure tests and checks pass before requesting review.
- At least one team member should review the PR before merging.

## Code Quality

Before opening a PR:

- Keep code formatted.
- Remove unused code.
- Do not commit secrets or API keys.
- Run the relevant tests and linting checks.