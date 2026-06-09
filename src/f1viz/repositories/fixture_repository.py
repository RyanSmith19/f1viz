import json
from pathlib import Path
from typing import Any

from f1viz.openf1.endpoints import OpenF1Endpoint


class FixtureRepository:
    """Read and write raw OpenF1 fixtures for deterministic tests and demos."""

    def __init__(self, root: Path) -> None:
        self.root = root

    def path_for(self, endpoint: OpenF1Endpoint, name: str) -> Path:
        return self.root / endpoint.value / f"{name}.json"

    def load(self, endpoint: OpenF1Endpoint, name: str) -> list[dict[str, Any]]:
        path = self.path_for(endpoint, name)
        with path.open("r", encoding="utf-8") as fixture_file:
            payload = json.load(fixture_file)

        if not isinstance(payload, list):
            raise TypeError(f"Fixture {path} must contain a JSON list")

        return payload

    def save(self, endpoint: OpenF1Endpoint, name: str, payload: list[dict[str, Any]]) -> Path:
        path = self.path_for(endpoint, name)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as fixture_file:
            json.dump(payload, fixture_file, indent=2, sort_keys=True)
            fixture_file.write("\n")
        return path

