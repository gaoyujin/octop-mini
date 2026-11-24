"""Process entry: load config and run uvicorn (composition root preview)."""

from __future__ import annotations

import uvicorn

from mini.infra.config import load_config


def main() -> None:
    cfg = load_config()
    print(f"Loaded bind_host={cfg.bind_host} port={cfg.port}")
    uvicorn.run(
        "mini.api.main:app",
        host=cfg.bind_host,
        port=cfg.port,
        reload=False,
    )


if __name__ == "__main__":
    main()