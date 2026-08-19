#!/usr/bin/env python3
"""Reject files that belong in the private research repository."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IGNORED_ROOTS = {".git", ".venv", "site", ".cache", "__pycache__"}
PRIVATE_PARTS = {
    "checkpoints",
    "codex_tasks",
    "data",
    "experiments",
    "hypotheses",
    "ideas",
    "logs",
    "outputs",
    "results",
}
PRIVATE_SUFFIXES = {".ckpt", ".log", ".npy", ".npz", ".pkl", ".pt", ".pth", ".safetensors"}
MAX_PUBLIC_FILE_BYTES = 2 * 1024 * 1024


def main() -> None:
    errors: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        if relative.parts[0] in IGNORED_ROOTS:
            continue
        lowered_parts = {part.lower() for part in relative.parts}
        if lowered_parts & PRIVATE_PARTS:
            errors.append(f"private directory in public repo: {relative}")
        if path.suffix.lower() in PRIVATE_SUFFIXES:
            errors.append(f"private/binary artifact in public repo: {relative}")
        if path.stat().st_size > MAX_PUBLIC_FILE_BYTES:
            errors.append(f"file exceeds 2 MiB public limit: {relative}")
    if errors:
        raise SystemExit("\n".join(errors))
    print("Public repository boundary check passed")


if __name__ == "__main__":
    main()
