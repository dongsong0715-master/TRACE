"""Lock only this project's dependency tree, not the entire shared Conda environment."""

from importlib import metadata
from pathlib import Path

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

ROOT = Path(__file__).resolve().parents[1]


def main():
    pending = [
        (Requirement(item), {"dev"})
        for item in metadata.requires("trace-backend") or []
    ]
    locked: dict[str, str] = {}
    seen = set()
    while pending:
        requirement, active_extras = pending.pop()
        if requirement.marker and not any(
            requirement.marker.evaluate({"extra": extra})
            for extra in ["", *active_extras]
        ):
            continue
        name = canonicalize_name(requirement.name)
        key = (name, frozenset(requirement.extras))
        if key in seen:
            continue
        seen.add(key)
        dist = metadata.distribution(requirement.name)
        locked[name] = dist.version
        pending.extend(
            (Requirement(item), requirement.extras) for item in dist.requires or []
        )
    lines = [
        "# Generated from the verified py312 environment; project dependencies only.",
        "# Update pyproject.toml, install, test, then regenerate. Do not pip freeze all Conda packages.",
    ]
    lines.extend(f"{name}=={version}" for name, version in sorted(locked.items()))
    (ROOT / "backend" / "requirements.lock").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    print(f"Locked {len(locked)} packages.")


if __name__ == "__main__":
    main()
