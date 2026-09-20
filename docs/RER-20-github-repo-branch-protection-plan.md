# RER-20: GitHub Repo & Branch Protection Setup Development Plan

## Overview

**Objective**: Prevent accidental direct pushes to `main` and standardize how changes get reviewed across the Rah-e-Ravaan project.

**Scope**: Configure GitHub branch protection rules on `main`, add PR and issue templates, and define code ownership for all major areas of the codebase (`/backend`, `/web`, `/mobile`).

## Current State Analysis

### Existing Repository Structure
- **Backend**: FastAPI application in `/backend`
- **Mobile**: Flutter application in `/mobile`
- **Web**: (planned) web frontend in `/web`
- **No `.github/` directory**: No existing PR templates, issue templates, or CODEOWNERS file
- **No branch protection**: Direct pushes to `main` are currently unrestricted

### Problems to Solve
- Any contributor can push directly to `main`, bypassing review
- No standard format for pull requests or issue reports
- No clear ownership mapping for different parts of the codebase
- Status checks (CI) are not required before merging

## Development Steps

### Phase 1: GitHub Branch Protection Rules

**Objective**: Lock down `main` so all changes must go through a reviewed PR.

**Tasks**:
1. Navigate to **GitHub → Repository → Settings → Branches → Add branch ruleset** (or classic branch protection under `main`).

2. Apply the following settings for the `main` branch:

   **Pull Request Reviews**:
   - Require a pull request before merging: ✅
   - Required number of approvals: **≥ 1**
   - Dismiss stale reviews when new commits are pushed: ✅
   - Require review from Code Owners: ✅

   **Status Checks**:
   - Require status checks to pass before merging: ✅
   - Require branches to be up to date before merging: ✅
   - Add relevant CI checks once GitHub Actions workflows exist (e.g., `backend-tests`, `lint`)

   **Push Restrictions**:
   - Allow force pushes: ❌ (disabled)
   - Allow deletions: ❌ (disabled)
   - Restrict who can push directly: limit to repository admins only (bypass for emergency hotfixes)

3. Verify the rule is active by attempting a direct push to `main` from a non-admin account — it should be rejected.

**Acceptance Criteria**:
- A direct `git push origin main` from a standard contributor is rejected with a clear error
- A PR to `main` shows a required review check before the merge button is active
- Force pushes to `main` are blocked

---

### Phase 2: Pull Request Template

**Objective**: Ensure every PR includes a consistent description covering what changed, why, how it was tested, and any visual evidence for UI changes.

**Tasks**:
1. Create the directory `.github/` in the repository root (if not already present).

2. Create `.github/PULL_REQUEST_TEMPLATE.md` with the following sections:

   - **What** — a brief description of the changes in this PR
   - **Why** — the motivation or ticket reference (e.g., `Closes #RER-XX`)
   - **Testing Done** — steps taken to verify the changes work; commands run, devices tested on
   - **Screenshots** — for any UI changes (Flutter, web); leave blank if not applicable
   - **Checklist** — common items like "linter passes", "no hardcoded secrets", "docs updated if needed"

3. Commit the file on a branch and open a test PR to confirm the template auto-populates in the PR description box.

**Acceptance Criteria**:
- Opening a new PR against `main` automatically shows the template in the description field
- All five sections are present and labeled clearly
- The checklist is actionable and not overly long

---

### Phase 3: Issue Templates

**Objective**: Give contributors a clear, structured format for filing bug reports and feature requests.

**Tasks**:
1. Create the directory `.github/ISSUE_TEMPLATE/` in the repository root.

2. Create `.github/ISSUE_TEMPLATE/bug_report.md` with:
   - **Front matter**: `name`, `about`, `title` prefix (e.g., `[BUG]`), `labels: bug`, `assignees: ""`
   - **Sections**:
     - Describe the bug
     - Steps to reproduce
     - Expected behavior
     - Actual behavior
     - Environment (OS, Flutter version, backend version, browser if web)
     - Screenshots / logs (optional)
     - Additional context

3. Create `.github/ISSUE_TEMPLATE/feature_request.md` with:
   - **Front matter**: `name`, `about`, `title` prefix (e.g., `[FEATURE]`), `labels: enhancement`, `assignees: ""`
   - **Sections**:
     - Problem statement — what user need or pain point does this address?
     - Proposed solution
     - Alternatives considered
     - Acceptance criteria — how will we know this is done?
     - Additional context / mockups

**Acceptance Criteria**:
- GitHub's "New Issue" page shows two template options: **Bug Report** and **Feature Request**
- Each template pre-fills the correct label and title prefix
- The sections guide the reporter to provide all information needed to act on the issue

---

### Phase 4: CODEOWNERS File

**Objective**: Automatically assign reviewers based on which part of the codebase a PR touches, and enforce owner review via branch protection.

**Tasks**:
1. Create `CODEOWNERS` in the repository root (GitHub also recognises `.github/CODEOWNERS` and `docs/CODEOWNERS`; root is preferred for visibility).

2. Define ownership mappings:

   | Path | Owner(s) |
   |------|----------|
   | `/backend/` | Backend team GitHub handles |
   | `/mobile/` | Mobile team GitHub handles |
   | `/web/` | Web team GitHub handles |
   | `/.github/` | All team leads (anyone who touches CI/CD config) |
   | `docker-compose.yml` | DevOps / backend lead |
   | `docs/` | All team leads |

3. Use GitHub username syntax (e.g., `@username` or `@org/team-slug` for org teams).

4. Add a catch-all (`*`) at the top mapped to all leads so no file is ever unowned.

5. Commit on a branch, open a PR touching `/backend/`, and verify the backend owner is automatically added as a reviewer.

**Acceptance Criteria**:
- PRs touching `/backend/` automatically request a review from the backend owner(s)
- PRs touching `/mobile/` automatically request a review from the mobile owner(s)
- PRs touching `/web/` automatically request a review from the web owner(s)
- The `CODEOWNERS` syntax passes GitHub's validation (no errors shown in repo settings)

---

### Phase 5: Verification & Documentation

**Objective**: Confirm all protections and templates work end-to-end and document the workflow for contributors.

**Tasks**:
1. **End-to-end test** (use a test branch and a second GitHub account or a teammate):
   - Attempt a direct push to `main` → confirm rejection
   - Open a PR → confirm template appears, CODEOWNERS reviewer is auto-assigned, and merge is blocked until approved
   - Approve the PR → confirm merge succeeds

2. **Update `CONTRIBUTING.md`** in the repo root:
   - Add a section on the branch model (feature branches off `main`, naming convention e.g. `feat/RER-XX-short-description`)
   - Document how to open a PR and what each template section means
   - Note that direct pushes to `main` are blocked

3. **Update `docs/DEVELOPMENT_WORKFLOW.md`** to reference the new branch protection rules and issue/PR templates.

**Acceptance Criteria**:
- `CONTRIBUTING.md` accurately describes the PR and branch workflow
- Any new contributor can read the docs and understand how to open an issue and a PR
- No gaps between what the docs say and what GitHub enforces

---

## Key Files and Modules

### New Files to Create
```
/.github/PULL_REQUEST_TEMPLATE.md          # PR description template
/.github/ISSUE_TEMPLATE/bug_report.md      # Bug report issue template
/.github/ISSUE_TEMPLATE/feature_request.md # Feature request issue template
/CODEOWNERS                                # Code ownership mappings
docs/RER-20-github-repo-branch-protection-plan.md  # This document
```

### Files to Modify
```
/CONTRIBUTING.md                           # Add branch model and PR workflow section
/docs/DEVELOPMENT_WORKFLOW.md              # Reference new branch protection setup
```

### GitHub Settings to Configure (UI / API)
```
Repository → Settings → Branches → main   # Branch protection rule
```

---

## Acceptance Criteria

### Functional Requirements
1. ✅ A direct push to `main` from a non-admin is rejected by GitHub
2. ✅ A new PR automatically displays the PR template in the description field
3. ✅ A new issue shows two template choices: Bug Report and Feature Request
4. ✅ PRs touching `/backend/` auto-request review from the backend code owner
5. ✅ PRs touching `/mobile/` auto-request review from the mobile code owner
6. ✅ Merge button on `main` PRs is blocked until ≥ 1 approval is granted
7. ✅ Force pushes to `main` are blocked

### Technical Requirements
1. ✅ `CODEOWNERS` file uses valid GitHub syntax with no validation errors
2. ✅ Branch protection rule includes "Require review from Code Owners"
3. ✅ Issue templates include correct front-matter (`name`, `about`, `labels`)
4. ✅ PR template includes: what, why, testing done, screenshots, checklist

### Documentation Requirements
1. ✅ `CONTRIBUTING.md` documents the branch naming convention and PR process
2. ✅ `DEVELOPMENT_WORKFLOW.md` references branch protection rules
3. ✅ All `.github/` files are committed on a branch and merged via a PR (dogfooding the process)

---

## Testing and Verification

### Manual Testing Steps

1. **Test direct push rejection**:
   ```bash
   git checkout main
   git commit --allow-empty -m "test: direct push to main"
   git push origin main
   # Expected: rejected — protected branch
   ```

2. **Test PR template**:
   ```bash
   git checkout -b test/RER-20-verify-template
   git commit --allow-empty -m "test: verify PR template"
   git push origin test/RER-20-verify-template
   # Open PR on GitHub → confirm template appears in description
   ```

3. **Test CODEOWNERS auto-assignment**:
   - Open a PR that modifies a file in `/backend/`
   - Confirm the backend owner appears in "Reviewers" automatically

4. **Test issue templates**:
   - Go to **Issues → New Issue** on GitHub
   - Confirm two template cards are shown
   - Click each and verify the sections and labels are pre-filled correctly

5. **Test merge block**:
   - Open a PR without any approvals
   - Confirm the "Merge pull request" button is greyed out / blocked
   - Add an approval → confirm button becomes active

### Common Pitfalls
- **CODEOWNERS with typos**: GitHub silently ignores invalid lines; check Settings → Code owners for warnings
- **Status checks not listed**: The check name in branch protection must exactly match the job name in the GitHub Actions workflow; add checks after CI is configured (RER-21+)
- **Admin bypass**: Admins can merge without review by default; consider enabling "Do not allow bypassing the above settings" for stricter enforcement

---

## Technical Considerations

### Security
- Enabling "Require review from Code Owners" closes the gap where a PR author approves their own code via a secondary account
- Disabling force pushes protects the commit history and prevents `--force` rewrites of reviewed code
- The `CODEOWNERS` file itself should be owned by all leads to prevent unauthorised changes

### Developer Experience
- Keep the PR template concise — long templates get ignored; aim for 5–8 checklist items maximum
- Issue templates should have enough structure to be useful but not so many required fields that reporters give up
- Branch naming convention (e.g., `feat/RER-XX-slug`, `fix/RER-XX-slug`) makes it easy to trace branches back to tickets

### Scalability
- Use GitHub org **teams** (e.g., `@rah-e-ravaan/backend-team`) in `CODEOWNERS` rather than individual usernames; this avoids updating the file every time a team member joins or leaves
- As CI matures (GitHub Actions), add individual workflow status checks to the branch protection required checks list

---

## Timeline Estimate

- **Phase 1 (Branch Protection)**: 0.5 hours (GitHub UI configuration)
- **Phase 2 (PR Template)**: 1 hour
- **Phase 3 (Issue Templates)**: 1–1.5 hours
- **Phase 4 (CODEOWNERS)**: 1 hour
- **Phase 5 (Verification & Docs)**: 1–2 hours

**Total Estimated Time**: 4.5–6 hours

---

## Dependencies and Prerequisites

### External Dependencies
- GitHub repository with admin access (to configure branch protection)
- At least one additional GitHub account or teammate available to test review requirements

### Internal Dependencies
- Contributor GitHub usernames (or org team slugs) must be known before writing `CODEOWNERS`
- CI workflow job names must be confirmed before adding status checks to branch protection (can be left as a stub and filled in when RER-21 / CI setup is complete)

---

## Risks and Mitigation

### Risk 1: No CI checks configured yet
**Impact**: The "require status checks" rule has nothing to enforce until GitHub Actions workflows exist.  
**Mitigation**: Configure the branch protection rule now but leave the status check list empty; add specific check names as CI workflows are added in subsequent stories.

### Risk 2: CODEOWNERS prevents unblocking urgent fixes
**Impact**: If the designated owner is unavailable, a PR can be stuck waiting for review.  
**Mitigation**: Map at least two owners per path; document an admin override process in `CONTRIBUTING.md` for genuine emergencies.

### Risk 3: Contributors ignore templates
**Impact**: PRs and issues arrive with poor descriptions despite the templates.  
**Mitigation**: The templates are defaults, not enforced; pair them with a brief note in onboarding docs explaining why each section matters.

---

## Success Metrics

1. Zero direct pushes land on `main` after protection is enabled
2. 100% of new PRs open with the template pre-filled
3. Reviewers are auto-assigned on every PR touching a protected path
4. New contributors can open a correctly formatted issue within 2 minutes of reading `CONTRIBUTING.md`

---

## Next Steps After Completion

1. Add GitHub Actions CI workflow (lint, tests) and register job names as required status checks on `main`
2. Configure GitHub Environments for staging/production deployment gates
3. Add Dependabot configuration for automated dependency PRs
4. Consider adding a `SECURITY.md` for responsible disclosure

---

## References

- [GitHub — About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub — Creating a pull request template](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository)
- [GitHub — Configuring issue templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository)
- [GitHub — About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)

---

**Document Version**: 1.0  
**Last Updated**: 2026-09-20  
**Author**: Development Team  
**Status**: Planning Phase
