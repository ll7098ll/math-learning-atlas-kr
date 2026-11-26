"""Export only the currently referenced portal assets, without changing Sites."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

from plan_portal_retention import reference_paths
from build_distribution_lab import build as build_distribution_lab
from build_inquiry_workbook import build as build_inquiry_workbook

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


def write_curriculum_index(dist: Path, catalog: dict) -> None:
    structure = json.loads((ROOT / "data/curriculum_structure.json").read_text(encoding="utf-8"))
    reviews = json.loads((ROOT / "data/curriculum_mapping_reviews.json").read_text(encoding="utf-8"))["reviews"]
    if structure["source_sha256"] != catalog["meta"]["sourceSha256"]:
        raise ValueError("Curriculum structure and catalog use different source PDFs.")
    blocks = {block["id"]: block for block in structure["blocks"]}
    codes = {standard["code"] for standard in catalog["standards"]}
    items = []
    for item in structure["items"]:
        block = blocks[item["block_id"]]
        review = reviews.get(item["source_fingerprint"])
        linked = review["standard_codes"] if review and review["source_text"] == item["text"] else []
        if not codes.issuperset(item["scope_codes"] + linked):
            raise ValueError(f"Unrecognized curriculum standard in {item['id']}")
        items.append({
            "id": item["id"], "text": item["text"], "subject": block["subject"],
            "domain": block["domain"], "category": block["category"], "page": item["pdf_page"],
            "scopeCodes": item["scope_codes"], "linkedCodes": linked,
        })
    (dist / "content/curriculum-structure.json").write_text(
        json.dumps({"version": catalog["version"], "items": items}, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8", newline="\n")


def install_compat_theme(dist: Path) -> None:
    source = ROOT / "site/frontend/compat"
    legacy_modules = sorted((source / "modules").glob("*.mjs"))
    for module in legacy_modules:
        shutil.copy2(module, dist / "modules" / module.name)
    shutil.copy2(source / "app.js", dist / "app.js")
    app_version = digest(dist / "app.js")[:16]
    build_distribution_lab(dist)
    build_inquiry_workbook(dist)
    style = "\n\n".join((source / name).read_text(encoding="utf-8").rstrip()
                         for name in ("atlas-tokens.css", "atlas-page.css", "portal-ui.css", "atlas-workspace.css",
                                      "atlas-shell.css", "atlas-tools.css", "atlas-print.css"))
    (dist / "portal-ui.css").write_text(style + "\n", encoding="utf-8", newline="\n")
    shutil.copy2(source / "portal-ui.js", dist / "portal-ui.js")
    css_version = digest(dist / "portal-ui.css")[:12]
    js_version = digest(dist / "portal-ui.js")[:12]
    reference = (
        f'<link data-atlas-theme rel="stylesheet" href="./portal-ui.css?v={css_version}">\n'
        f'<script data-atlas-theme defer src="./portal-ui.js?v={js_version}"></script>\n'
    )
    for name in ("legacy.html", "distribution-lab.html", "inquiry-workbook.html"):
        path = dist / name
        html = path.read_text(encoding="utf-8")
        if name == "legacy.html":
            html = re.sub(r'(?<=src="app\.js)\?v=[^"]+', f"?v={app_version}", html)
            def version_modules(match):
                mapping = json.loads(match[2])
                for module in legacy_modules:
                    relative = f"./modules/{module.name}"
                    mapping["imports"][relative] = relative + "?v=" + digest(module)[:16]
                return match[1] + json.dumps(mapping, ensure_ascii=False, separators=(",", ":")) + match[3]

            html = re.sub(r'(<script type="importmap">)(.*?)(</script>)',
                          version_modules, html, flags=re.DOTALL)
        html = re.sub(r'<link data-atlas-theme[^>]*>\n?|<script data-atlas-theme[^>]*></script>\n?', "", html)
        if "</head>" not in html:
            raise ValueError(f"No document head to theme in {name}")
        path.write_text(html.replace("</head>", reference + "</head>", 1).rstrip() + "\n",
                        encoding="utf-8", newline="\n")


def write_relation_resources(source: Path, dist: Path, catalog: dict, old_root: str) -> None:
    version = catalog["version"]
    # The data version still describes the same curriculum. Give the new
    # immutable file layout its own path so cached files cannot mix schemas.
    layout_id = hashlib.sha256(f"shared-relation-sources-v1:{version}".encode()).hexdigest()[:16]
    new_root = f"content/versions/{layout_id}/"
    connections = json.loads((dist / "content/connections.json").read_text(encoding="utf-8"))
    if connections["version"] != version:
        raise ValueError("Source list and catalog use different content versions.")

    def write_json(path, value):
        path.write_text(json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n",
                        encoding="utf-8", newline="\n")

    source_index = connections["sources"]
    source_ids = {item["id"] for item in source_index}
    if len(source_ids) != len(source_index):
        raise ValueError("Duplicate source identifiers in the source index.")
    write_json(dist / "content/sources.json", {"version": version, "sources": source_index})

    target = safe_path(dist, new_root)
    (target / "relations").mkdir(parents=True, exist_ok=True)
    shutil.copy2(safe_path(source, old_root + "hierarchy.json"), target / "hierarchy.json")
    for standard in catalog["standards"]:
        code = standard["code"]
        relative = f"relations/{code}.json"
        record = json.loads(safe_path(source, old_root + relative).read_text(encoding="utf-8"))
        inline = record.pop("sources", source_index)
        cited = {standard["sourceId"]}
        cited.update(sid for relation in record["relations"] for sid in relation.get("source_ids", ()))
        if record["version"] != version or inline != source_index or not cited <= source_ids:
            raise ValueError(f"Version or source index mismatch for {code}")
        write_json(safe_path(target, relative), record)
    write_json(dist / "content/catalog.json", {**catalog, "resourceRoot": new_root})


def install_explorer(dist: Path, frontend: Path, catalog: dict) -> None:
    legacy = dist / "legacy.html"
    if not legacy.is_file():
        shutil.copy2(dist / "index.html", legacy)
    shutil.copy2(frontend / "index.html", dist / "index.html")
    shutil.copytree(frontend / "explorer-assets", dist / "explorer-assets", dirs_exist_ok=True)
    install_compat_theme(dist)
    write_curriculum_index(dist, catalog)


def export(source: Path, output: Path, frontend: Path | None = None) -> dict:
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
    explorer = frontend is not None or (dist / "legacy.html").is_file()
    old_root = catalog["resourceRoot"]
    if explorer:
        paths = {relative for relative in paths if not relative.startswith(old_root)}
    # Fixed entry points, modules, examples and standard detail files are current assets.
    paths.update(p.relative_to(dist).as_posix() for p in dist.iterdir() if p.is_file())
    paths.update(p.relative_to(dist).as_posix() for p in (dist / "content").glob("*.json"))
    folders = ["modules", "examples", "content/standards"]
    if frontend is None:
        folders.append("explorer-assets")
    for folder in folders:
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
    if frontend is not None:
        install_explorer(output / "dist", frontend.resolve(), catalog)
    elif (output / "dist/legacy.html").is_file():
        install_compat_theme(output / "dist")
        write_curriculum_index(output / "dist", catalog)
    if explorer:
        write_relation_resources(dist, output / "dist", catalog, old_root)
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
    worktree = subprocess.run(["git", "-C", str(source), "status", "--porcelain"],
                              capture_output=True, text=True, check=False)
    clean = commit.returncode == worktree.returncode == 0 and not worktree.stdout
    manifest = {
        "schema_version": 1,
        "data_version": catalog["version"],
        "task_dataset_version": task["datasetVersion"],
        "concept_dataset_version": concept["datasetVersion"],
        "source_commit": commit.stdout.strip() if clean else None,
        "source_base_commit": commit.stdout.strip() if commit.returncode == 0 else None,
        "source_worktree_clean": clean,
        "scope": "current_references_only; no saved-version archives or hosting metadata",
        "test_path_adaptations": adapted,
        "files": [{"path": p.relative_to(output).as_posix(), "bytes": p.stat().st_size,
                   "sha256": digest(p), "optional_in_git": p.suffix.lower() == ".pdf"}
                  for p in sorted(output.rglob("*")) if p.is_file()],
    }
    (output / "snapshot.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return verify(output)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "tmp/pathways-release")
    parser.add_argument("--output", type=Path, default=ROOT / "site")
    parser.add_argument("--frontend", type=Path, help="Overlay a built GitHub explorer onto the exported legacy portal")
    parser.add_argument("--verify", action="store_true", help="Verify the exported snapshot without the original workspace")
    args = parser.parse_args()
    result = verify(args.output) if args.verify else export(args.source, args.output, args.frontend)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
