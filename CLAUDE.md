# CLAUDE.md

This file provides guidance to AI assistants (Claude and others) working in this repository.

---

## Repository Overview

**Repository**: alexregrets/alexregrets
**Status**: This repository is currently empty — no source files, build configs, or tests have been committed yet.

> When code is added, update this file to reflect the actual project structure, stack, conventions, and workflows.

---

## Current State

The repository was initialized with a single branch and a remote configured at the local proxy. No commits exist yet.

```
/home/user/alexregrets/
└── .git/        # Git metadata only
```

---

## General Conventions for AI Assistants

These conventions apply until project-specific ones are established:

### Reading Code Before Changing It

- Always read a file before editing it.
- Never propose changes based on assumptions about file contents.
- When exploring an unfamiliar area, trace call sites and usages before modifying signatures or interfaces.

### Making Changes

- Keep changes minimal and focused on the stated task.
- Do not refactor, add comments, or clean up code outside the scope of the request.
- Prefer editing existing files over creating new ones.
- Delete code that is no longer used; do not leave dead code behind.
- Do not add error handling for situations that cannot occur.

### Security

- Never introduce command injection, SQL injection, XSS, or other OWASP Top 10 vulnerabilities.
- Do not commit secrets, credentials, API keys, or `.env` files.
- Validate input only at system boundaries (user input, external APIs); trust internal framework guarantees.

### Git Workflow

- Always develop on the designated feature branch; never push directly to `main` or `master` without explicit permission.
- Write clear, descriptive commit messages that explain *why* the change was made, not just *what* changed.
- Stage specific files rather than using `git add -A` or `git add .` to avoid accidentally including sensitive files.
- Do not amend commits that have already been pushed unless explicitly instructed.
- Push with: `git push -u origin <branch-name>`

### Commit Message Format

```
<short imperative summary (50 chars max)>

<optional body explaining motivation and context>
```

Example:
```
Add user authentication middleware

JWT validation was missing from API routes. This adds a reusable
middleware that checks the Authorization header on protected endpoints.
```

---

## Development Workflow (Template)

Once the project is established, document the following here:

### Setup

```bash
# Install dependencies
# e.g., npm install / pip install -r requirements.txt / cargo build

# Copy and configure environment variables
cp .env.example .env
```

### Running the Application

```bash
# Start the development server
# e.g., npm run dev / python main.py / cargo run
```

### Running Tests

```bash
# Run the full test suite
# e.g., npm test / pytest / cargo test
```

### Linting and Formatting

```bash
# Check code style
# e.g., npm run lint / ruff check . / cargo clippy
```

### Building for Production

```bash
# Create a production build
# e.g., npm run build / docker build .
```

---

## Project Structure (Template)

Update this section once the codebase is established. A typical structure might look like:

```
├── src/           # Application source code
├── tests/         # Test files
├── docs/          # Documentation
├── scripts/       # Utility/automation scripts
├── .github/       # CI/CD workflows (GitHub Actions)
├── .env.example   # Environment variable template
└── CLAUDE.md      # This file
```

---

## Environment Variables (Template)

Document required environment variables here as they are added. Example:

| Variable       | Description                | Required |
| -------------- | -------------------------- | -------- |
| `DATABASE_URL` | Connection string for the DB | Yes    |
| `API_KEY`      | Third-party API key         | Yes     |
| `DEBUG`        | Enable debug logging        | No      |

---

## Key Decisions and Context (Template)

Use this section to record architectural decisions that would otherwise only exist in someone's head:

- **Why X over Y**: Explain tradeoffs made when choosing libraries, frameworks, or patterns.
- **Known limitations**: Document intentional shortcuts or areas that need future attention.
- **External dependencies**: Note any third-party services or APIs the application relies on.

---

## Updating This File

This file should be kept current. Update it whenever:

- A new major dependency or framework is added.
- The directory structure changes significantly.
- A new development workflow or tooling step is introduced.
- An architectural decision is made that future contributors should know about.

The goal is that any AI assistant or new developer can read this file and immediately understand how to work in the repository.
