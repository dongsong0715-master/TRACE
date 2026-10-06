"""Verify the relocated starter dataset without changing its frozen content."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    demo_dir = ROOT / "data" / "demo" / "v1"
    rules_dir = ROOT / "data" / "rules" / "v1"
    manifest = json.loads(
        (demo_dir / "generation_manifest.json").read_text(encoding="utf-8")
    )
    for name, expected in manifest["files"].items():
        folder = (
            rules_dir if name in {"rules.json", "diagnosis_template.json"} else demo_dir
        )
        source = (folder / name).read_bytes()
        assert hashlib.sha256(source).hexdigest() == expected, f"Hash changed: {name}"
        assert source == (ROOT / "docs" / "一期样例数据" / name).read_bytes(), (
            f"Baseline drift: {name}"
        )
    print("data/demo/v1 与 data/rules/v1 的6个内容文件通过哈希和基线一致性校验。")


if __name__ == "__main__":
    main()
