"""Agent workspace directory bootstrap (teaching placeholder for BackendWorkspace)."""

from __future__ import annotations

from mini.infra.paths import PathLayout

_SOUL_PLACEHOLDER = "# SOUL.md — course 05 placeholder; production uses BackendWorkspace.\n"


def init_agent_workspace(layout: PathLayout, agent_id: str) -> Path:
    """Create ``{MINI_HOME}/agents/<agent_id>/`` and a stub ``SOUL.md``."""
    root = layout.agent_workspace(agent_id)
    root.mkdir(parents=True, exist_ok=True)
    soul = root / "SOUL.md"
    if not soul.exists():
        soul.write_text(_SOUL_PLACEHOLDER, encoding="utf-8")
    return root