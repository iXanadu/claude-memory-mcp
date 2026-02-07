import socket
from unittest.mock import patch

from claude_memory_mcp.scoping import resolve_user_id


def test_machine_scope():
    hostname = socket.gethostname().split(".")[0].lower()
    assert resolve_user_id("machine") == f"cc-{hostname}"


def test_machine_scope_is_default():
    result = resolve_user_id(None, default_scope="machine")
    hostname = socket.gethostname().split(".")[0].lower()
    assert result == f"cc-{hostname}"


def test_shared_scope():
    assert resolve_user_id("shared") == "cc-shared"


def test_project_scope():
    with patch("claude_memory_mcp.scoping.os.getcwd", return_value="/Users/test/projects/my-app"):
        assert resolve_user_id("project") == "cc-proj-my-app"


def test_custom_scope_passthrough():
    assert resolve_user_id("custom-thing") == "cc-custom-thing"


def test_none_scope_uses_default():
    assert resolve_user_id(None, default_scope="shared") == "cc-shared"
