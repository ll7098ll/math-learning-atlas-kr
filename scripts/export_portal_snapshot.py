"""Export only the currently referenced portal assets, without changing Sites."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

from plan_portal_retention import reference_paths

ROOT = Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_path(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f"Path outside snapshot: {relative}")
    return path


def verify(output: Path) -> dict:
    manifest = json.loads((output / "snapshot.json").read_text(encoding="utf-8"))
    optional_missing = []
    for item in manifest["files"]:
        path = safe_path(output, item["path"])
        if not path.is_file() and item["optional_in_git"]:
            optional_missing.append(item["path"])
            continue
        if not path.is_file() or digest(path) != item["sha256"]:
            raise ValueError(f"Missing or modified snapshot file: {item['path']}")
    return {"status": "pass", "version": manifest["data_version"],
            "files": len(manifest["files"]), "optional_missing": optional_missing}


def export(source: Path, output: Path) -> dict:
    source, output = source.resolve(), output.resolve()
    if output.exists():
        raise ValueError("Output already exists; choose a new directory. Existing files are never replaced.")
    if output.is_relative_to(source) or source.is_relative_to(output):
        raise ValueError("Source and output directories must be separate.")
    dist = source / "dist"
    read = lambda name: json.loads((dist / "content" / name).read_text(encoding="utf-8"))
    catalog, task, concept = (read(name) for name in
                              ("catalog.json", "task-pathways-index.json", "concept-pathways-index.json"))
    paths = set(reference_paths(catalog, task, concept))
    # Fixed entry points, modules, examples and standard detail files are current assets.
    paths.update(p.relative_to(dist).as_posix() for p in dist.iterdir() if p.is_file())
    paths.update(p.relative_to(dist).as_posix() for p in (dist / "content").glob("*.json"))
    for folder in ("modules", "examples", "content/standards"):
        paths.update(p.relative_to(dist).as_posix() for p in (dist / folder).rglob("*") if p.is_file())
    for relative in paths:
        path = safe_path(dist, relative)
        if not path.is_file():
            raise ValueError(f"Missing current asset: {relative}")
        if "/items/" in relative and digest(path) != path.stem:
            raise ValueError(f"Content hash mismatch: {relative}")
    tests = sorted((source / "tests").glob("*.mjs"))
    if not tests:
        raise ValueError("Portal tests are required.")
    output.mkdir(parents=True)
    for relative in sorted(paths):
        target = output / "dist" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(dist / relative, target)
    # The exported site lives beside the research folders instead of above research/.
    adapted = []
    for test in tests:
        original = test.read_text(encoding="utf-8")
        content = original.replace("'../research/", "'../../").replace("'research/", "'../")
        target = output / "tests" / test.name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")
        if content != original:
            adapted.append(test.name)
    commit = subprocess.run(["git", "-C", str(source), "rev-parse", "HEAD"],
                            capture_output=True, text=True, check=False)
    manifest = {
        "schema_version": 1,
        "data_version": catalog["version"],
        "task_dataset_version": task["datasetVersion"],
        "concept_dataset_version": concept["datasetVersion"],
        "source_commit": commit.stdout.strip() if commit.returncode == 0 else None,
        "scope": "current_references_only; no saved-version archives or hosting metadata",
        "test_path_adaptations": adapted,
        "files": [{"path": p.relative_to(output).as_posix(), "bytes": p.stat().st_size,
                   "sha256": digest(p), "optional_in_git": p.suffix.lower() == ".pdf"}
                  for p in sorted(output.rglob("*")) if p.is_file()],
    }
    (output / "snapshot.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return verify(output)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "tmp/pathways-release")
    parser.add_argument("--output", type=Path, default=ROOT / "site")
    parser.add_argument("--verify", action="store_true", help="Verify the exported snapshot without the original workspace")
    args = parser.parse_args()
    result = verify(args.output) if args.verify else export(args.source, args.output)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
