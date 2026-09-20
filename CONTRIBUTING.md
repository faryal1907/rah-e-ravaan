# Contributing to Rah-e-Ravaan

## Branch Naming

Every branch maps to exactly one Jira story. Use the following format:

```
<type>/RER-<ticket>-<short-description>
```

| Type | When to use |
|------|-------------|
| `feat` | New feature or user-facing behaviour |
| `fix` | Bug fix |
| `chore` | Tooling, config, dependencies, CI |
| `docs` | Documentation only |

Examples:

```
feat/RER-26-customer-signup
fix/RER-30-jwt-refresh-rotation
chore/RER-20-branch-protection
docs/RER-100-architecture-doc
```

**Rules:**
- One branch per story — all commits for that story go on the same branch.
- Branch off `main` only. Never branch off another feature branch.
- Direct pushes to `main` are blocked. Every change must go through a pull request — even small ones.
- Keep branches short-lived: open a PR within 2–3 days of starting work and merge before the sprint ends.

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

### Opening a PR

1. Push your branch and go to `https://github.com/faryal1907/rah-e-ravaan/compare/main...<your-branch>`.
2. The description box will be **automatically pre-filled** with the PR template — fill in every section before submitting.
3. Set the base branch to `main`.
4. Request a review from at least one teammate. CODEOWNERS will auto-assign the right reviewer based on which files you changed.
5. Wait for CI checks to pass and at least 1 approval before merging.

### PR Template Sections

Every PR must complete all five sections:

| Section | What to write |
|---------|--------------|
| **What** | One or two sentences describing the change. What does this PR do? |
| **Why** | The motivation. Reference the Jira ticket — e.g. `Closes #RER-26`. |
| **Testing Done** | Commands you ran, API calls you made, devices you tested on. Tick the checkboxes that apply. |
| **Screenshots** | Before/after screenshots or a short recording for any UI change (web or Flutter). Leave blank for backend-only PRs. |
| **Checklist** | Tick every item that applies. Do not submit with unchecked items you have not thought about. |

### Rules

- One PR per story — scope it to the Jira ticket it implements.
- Keep PRs focused: avoid bundling unrelated fixes or refactors.
- Do not commit secrets, API keys, or credentials. Add new variables to `.env.example` instead.
- Do not merge your own PR without a review unless explicitly agreed for a hotfix.

## Code Quality

Before opening a PR:

- Keep code formatted.
- Remove unused code.
- Do not commit secrets or API keys.
- Run the relevant tests and linting checks.