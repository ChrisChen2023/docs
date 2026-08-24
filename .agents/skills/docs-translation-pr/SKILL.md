---
name: docs-translation-pr
description: Audit English and Chinese MDX documentation for matching coverage, translate missing or outdated Chinese pages from the English source, preserve all MDX structure and technical tokens, and open a review-only pull request with the requested GitHub reviewer. Use this skill whenever the user asks to synchronize, translate, compare, localize, or submit a PR for bilingual documentation.
compatibility: Requires Python 3 for the bundled scanner, Git, and GitHub CLI (`gh`) for pull requests. Requires a configured Git remote and authenticated GitHub CLI session for PR creation.
---

# Bilingual documentation translation

Synchronize the `zh/` documentation tree from the English source tree without changing the site's MDX structure. Treat this as a reviewable documentation change: never merge the pull request automatically.

## Safety and approval rules

- Work on a new branch. Never commit directly to the default branch.
- Ask for the reviewer's GitHub username or resolve it from the user's explicit identity before creating the PR. Do not guess from an email address.
- Create the PR as open and review-only. Do not use `--auto`, `--merge`, `--squash`, `--rebase`, or any merge API.
- Set the requested reviewer explicitly with `gh pr create --reviewer <owner>`. If the reviewer cannot be resolved, stop before creating the PR and ask for the exact GitHub handle.
- Do not alter English source files, `docs.json`, API definitions, links, code, commands, identifiers, or image paths unless the user explicitly requests it.
- Do not translate secrets, environment variables, URLs, file paths, CLI commands, API paths, JSON keys, code, or component names.

## Workflow

### 1. Inspect the repository

Read `AGENTS.md`, `docs.json`, and the relevant English and Chinese pages. Confirm the repository root and default branch with Git. Check the working tree and preserve unrelated user changes.

Run the bundled inventory first:

```bash
python .agents/skills/docs-translation-pr/scripts/scan_translation_pairs.py .
```

The report lists missing Chinese pages, orphan Chinese pages, and per-file structural counts. Treat missing or orphan pages as findings to report, not as permission to delete or create content without checking navigation.

### 2. Compare paired pages

Pair each English path with the same path below `zh/`. For every pair, compare:

- frontmatter keys and page metadata
- headings and section order
- Mintlify/MDX component names, nesting, attributes, and closing tags
- fenced code block languages and code contents
- links, image paths, API paths, CLI commands, flags, identifiers, and placeholders
- lists, tables, admonitions, tabs, accordions, and inline formatting

Classify each difference as `missing translation`, `outdated translation`, `English-only content`, `Chinese-only content`, or `intentional localization`. Record the file and a concise explanation before editing.

### 3. Translate conservatively

Use the English page as the source of truth. Update only the paired file under `zh/` unless the user explicitly asks for a new localized page. Preserve the complete MDX skeleton byte-for-byte where possible:

- Keep frontmatter delimiters and keys. Translate human-readable `title`, `description`, and `sidebarTitle` values when appropriate, but preserve metadata types and paths.
- Keep every opening and closing component tag, attribute name, prop expression, import, export, and JSX expression unchanged.
- Keep code fences, language identifiers, commands, code, URLs, anchors, image paths, API schemas, and placeholders unchanged.
- Translate prose, headings, table labels, callout text, and explanatory comments into natural Simplified Chinese.
- Preserve heading hierarchy, list nesting, table column count, and link destinations. Translate link labels only when the destination remains the same.
- Do not translate product names, model names, command names, HTTP methods, API parameters, environment variables, or technical identifiers.

For a page with structural uncertainty, stop and inspect the source and target rather than repairing MDX by intuition.

### 4. Validate before committing

Run the scanner again and inspect the diff:

```bash
python .agents/skills/docs-translation-pr/scripts/scan_translation_pairs.py .
git diff --check
git diff --stat
git diff -- zh/
```

For each changed page, verify that structural counts and protected tokens match the English source. If Mintlify CLI is available, run:

```bash
mint validate
mint broken-links
```

If the CLI is unavailable, say so explicitly and retain the other validation results. Do not hide validation failures.

### 5. Commit and open the review PR

After validation, create a focused commit on the new branch. Before opening the PR, show the user the planned title, summary, changed files, validation results, and exact reviewer handle when the workflow requires interactive approval.

Create the PR without merging:

```bash
gh pr create \
  --title "docs: synchronize Chinese translations" \
  --body-file /tmp/docs-translation-pr-body.md \
  --reviewer <github-reviewer>
```

The PR body should state the English source scope, translated pages, known intentional differences, checks run, and that the PR is awaiting review. Confirm afterward that the PR is open and the reviewer is assigned. Never enable auto-merge.

## Expected final report

Report:

1. Pairing findings and pages changed.
2. Structural and documentation validation results.
3. Branch and commit names.
4. PR URL, assigned reviewer, and explicit confirmation that it was not merged.
5. Any unresolved pages, missing tools, or decisions requiring user input.
