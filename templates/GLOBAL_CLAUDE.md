# Global Instructions

## Session Startup

If CWD is the home directory (`~/`), run `/admin-startup`.
Otherwise, if a `/startup` command is available, run it. Project folders define their own `/startup`.

## Persistent Memory (claude-memory-mcp)

You have access to persistent semantic memory via MCP tools. Use it proactively.

### How Scopes Work

There are three scopes. **Search is scope-isolated** — each `memory_search` returns results from one scope only. You must query each scope separately.

| Scope | Resolves to | Visible to | Use for |
|-------|------------|------------|---------|
| `shared` | `cc-shared` (literal) | All machines, all projects | Lessons, patterns, fixes — durable knowledge for everyone |
| `project` | `cc-proj-{cwd_basename}` | Any machine with same folder name | Session state, WIP, project-specific decisions |
| `machine` | `cc-{hostname}` | This machine only | Machine-specific paths, services, env quirks |

**Resolution details:**
- `project` uses `os.path.basename(os.getcwd())` — the CWD folder name, NOT git root
- `machine` uses `socket.gethostname().split(".")[0].lower()`
- `shared` is the literal string `cc-shared` — same on every machine, which is how knowledge crosses boundaries

**Default to `shared`** for durable knowledge. The whole point of memory is collective wisdom. If a fix or lesson would help a different project, it MUST go to shared — not buried in project scope.

### Session Startup — search broadly, then narrow
1. `memory_search` with `scope=shared` — collective wisdom from ALL projects and machines
2. `memory_search` with `scope=project` — project-specific context (WIP, decisions, session state)
3. `memory_search` with `scope=machine` — local env quirks, paths, services specific to this box
4. Use what you find to orient. Shared wisdom may save you from repeating mistakes.

### During Work — store at milestones
- `memory_store` when you make a decision, solve a hard problem, or hit a progress checkpoint
- Ask: **"who benefits from this?"**
  - Session state, WIP, project-specific decisions → `scope=project`
  - Machine paths, services, local env quirks → `scope=machine`
  - Lessons, patterns, fixes that ANY project could use → `scope=shared`

### Session End — summarize and promote
1. Store a brief session summary at `scope=project` (next session continuity)
2. If any fix, pattern, or lesson is generalizable, store it ALSO at `scope=shared` with a `lesson/` or `fix/` key prefix
3. Don't duplicate — skip if already stored at shared during the session

### Key naming
Use prefixed keys: `session/YYYY-MM-DD-brief-desc`, `lesson/topic`, `decision/what`, `fix/what-was-fixed`

### What to store
- Decisions and their rationale
- Errors that took multiple attempts to fix (especially at `shared`)
- Architectural patterns and project conventions
- Session progress (crash recovery — the primary use case)

### What NOT to store
- Secrets, tokens, API keys
- Large code blocks (reference file paths instead)
- Transient state that will be stale next session

## Python Convention

ALWAYS use `pyenv` + `pyenv-virtualenv`. NEVER use `python -m venv`.
Virtualenv naming: `{project}-{major}.{minor}` (e.g. `cc-memory-3.12`).
Each project gets a `.python-version` file pointing to its pyenv virtualenv.
