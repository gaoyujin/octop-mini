from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from mini.cli import run as run_cmd


def test_run_uvicorn_delegates_to_launch() -> None:
    with patch("mini.launch.run_foreground_blocking") as blocking:
        run_cmd._run_uvicorn(host="127.0.0.1", port=8765, reload=False, workers=1, log_level=None)
    blocking.assert_called_once_with(
        host="127.0.0.1",
        port=8765,
        reload=False,
        workers=1,
        log_level=None,
    )


def test_cli_run_patches_uvicorn(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MINI_HOME", str(tmp_path))
    with patch.object(run_cmd, "_run_uvicorn") as uvicorn_mock:
        from click.testing import CliRunner

        from mini.cli.main import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["run", "--port", "8810"])
        assert result.exit_code == 0, result.output
        uvicorn_mock.assert_called_once()
        kwargs = uvicorn_mock.call_args.kwargs
        assert kwargs["port"] == 8810