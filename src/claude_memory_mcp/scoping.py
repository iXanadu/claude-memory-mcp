import os
import socket


def resolve_user_id(scope: str | None = None, default_scope: str = "machine") -> str:
    """Resolve a scope name to a ha-semantic-memory user_id string.

    Scopes:
        machine  -> cc-{hostname}     (machine-specific context)
        shared   -> cc-shared         (fleet-wide knowledge)
        project  -> cc-proj-{dirname} (project-specific patterns)
    """
    scope = scope or default_scope

    if scope == "machine":
        hostname = socket.gethostname().split(".")[0].lower()
        return f"cc-{hostname}"
    elif scope == "shared":
        return "cc-shared"
    elif scope == "project":
        dirname = os.path.basename(os.getcwd())
        return f"cc-proj-{dirname}"
    else:
        return f"cc-{scope}"
