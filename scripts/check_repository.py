"""Read-only checks for the research repository's publishable working files.

Uses only the Python standard library. Does not read tmp/ or nested Sites Git
repositories, contact the network, stage files, or change source data. This is
a focused preflight check, not a complete secret scanner or a Gitignore parser.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DIRECTORIES = {".github", "analyses", "data", "docs", "indexes", "portal", "scripts", "site"}
TEXT_SUFFIXES = {".md", ".json", ".csv", ".tsv", ".py", ".js", ".mjs", ".cjs", ".html", ".css", ".yml", ".yaml", ".txt", ".toml", ".ps1", ".sh"}
MIB = 1024 * 1024
SECRET_PATTERNS = {
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github-token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b|\bgithub_pat_[A-Za-z0-9_]{50,}\b"),
    "openai-token": re.compile(r"\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{32,}\b"),
    "aws-access-key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
}
LINK = re.compile(r"!?\[[^\]\n]*\]\((<[^>\n]+>|[^)\n]+)\)")
FENCES = re.compile(r"^\s*(`{3,}|~{3,})")


def ignore_rules(root: Path):
    """Support the simple root .gitignore rules shipped with this project."""
    path = root / ".gitignore"
    if not path.is_file():
        return []
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")]


def is_ignored(relative: str, rules: list[str]) -> bool:
    parts = relative.strip("/").split("/")
    if ".git" in parts:
        return True
    ignored = False
    # Match the path and every parent, so an ignored directory also excludes
    # a Markdown link pointing to a file inside it even when absent locally.
    candidates = ["/".join(parts[:i]) for i in range(1, len(parts) + 1)]
    for rule in rules:
        negate = rule.startswith("!")
        pattern = rule[1:] if negate else rule
        anchored = pattern.startswith("/")
        pattern = pattern.strip("/")
        if pattern.startswith("**/"):
            pattern = pattern[3:]
        if anchored or "/" in pattern:
            matched = any(fnmatch.fnmatchcase(candidate, pattern) for candidate in candidates)
        else:
            matched = any(fnmatch.fnmatchcase(part, pattern) for part in parts)
        if matched:
            ignored = not negate
    return ignored


def candidates(root: Path, rules: list[str]):
    for path in sorted(root.iterdir()):
        if path.is_symlink() or is_ignored(path.name, rules):
            continue
        if path.is_file():
            yield path
        elif path.name in DIRECTORIES:
            for directory, children, filenames in os.walk(path, followlinks=False):
                base = Path(directory)
                children[:] = sorted(name for name in children
                    if not (base / name).is_symlink()
                    and not is_ignored((base / name).relative_to(root).as_posix(), rules))
                for name in sorted(filenames):
                    file = base / name
                    if not file.is_symlink() and not is_ignored(file.relative_to(root).as_posix(), rules):
                        yield file


def markdown_destinations(content: str):
    fence = None
    for line_number, line in enumerate(content.splitlines(), 1):
        match = FENCES.match(line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker[0]
            elif marker[0] == fence:
                fence = None
            continue
        if fence:
            continue
        for match in LINK.finditer(line):
            target = match.group(1).strip()
            if target.startswith("<"):
                target = target[1:-1]
            else:
                target = re.split(r'\s+["\']', target, maxsplit=1)[0]
            yield line_number, target


def check(root: Path):
    rules = ignore_rules(root)
    issues = []
    excluded_links = 0
    links_checked = 0
    count = 0
    total_bytes = 0
    max_file = (0, "")
    for file in candidates(root, rules):
        relative = file.relative_to(root).as_posix()
        size = file.stat().st_size
        count += 1
        total_bytes += size
        max_file = max(max_file, (size, relative))
        if size > 100 * MIB:
            issues.append({"level": "error", "file": relative, "kind": "file-over-100-MiB"})
        elif size > 50 * MIB:
            issues.append({"level": "warning", "file": relative, "kind": "file-over-50-MiB"})
        if file.suffix.lower() not in TEXT_SUFFIXES and not file.name.startswith("."):
            continue
        # Bound memory for abnormal input; a large unscanned text file must be
        # reviewed explicitly instead of receiving an apparent clean result.
        if size > 25 * MIB:
            issues.append({"level": "error", "file": relative, "kind": "text-over-scan-limit-25-MiB"})
            continue
        try:
            content = file.read_text(encoding="utf-8-sig")
        except UnicodeError:
            issues.append({"level": "error", "file": relative, "kind": "not-utf8"})
            continue
        for kind, pattern in SECRET_PATTERNS.items():
            if pattern.search(content):
                # Never print matching text or credential values.
                issues.append({"level": "error", "file": relative, "kind": kind})
        if file.suffix.lower() != ".md":
            continue
        for line, destination in markdown_destinations(content):
            parsed = urlsplit(destination)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target_path = unquote(parsed.path).replace("\\", "/")
            target = (root / target_path.lstrip("/") if target_path.startswith("/")
                      else file.parent / target_path).resolve()
            if not target.is_relative_to(root):
                issues.append({"level": "error", "file": relative, "line": line, "kind": "link-outside-repository"})
                continue
            target_relative = target.relative_to(root).as_posix()
            if is_ignored(target_relative, rules):
                excluded_links += 1
                continue
            links_checked += 1
            if not target.exists():
                issues.append({"level": "error", "file": relative, "line": line, "kind": "missing-local-link", "target": target_relative})
    return {
        "candidate_files": count,
        "candidate_bytes": total_bytes,
        "largest_file": {"file": max_file[1], "bytes": max_file[0]},
        "local_links_checked": links_checked,
        "excluded_local_links": excluded_links,
        "issues": issues,
        "scope": "working files in named source directories; root .gitignore simple rules; inline Markdown file links; known credential formats",
        "not_checked": ["external URLs", "Markdown anchors/reference-style links", "Git commit history/index contents", "source redistribution rights", "all possible secret formats"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="print a compact JSON report to stdout; do not write a file")
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    result = check(ROOT)
    errors = sum(issue["level"] == "error" for issue in result["issues"])
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Candidates: {result['candidate_files']} files, {result['candidate_bytes'] / MIB:.1f} MiB")
        print(f"Local links: {result['local_links_checked']} checked, {result['excluded_local_links']} excluded/local-only")
        print(f"Findings: {errors} errors, {len(result['issues']) - errors} warnings")
        for issue in result["issues"][:40]:
            location = issue["file"] + (f":{issue['line']}" if "line" in issue else "")
            print(f"{issue['level'].upper()} {location}: {issue['kind']}" + (f" -> {issue['target']}" if "target" in issue else ""))
        if len(result["issues"]) > 40:
            print("Only the first 40 findings shown. Use --json for the complete report.")
        print("This preflight does not inspect Git history, all secret formats, external URLs or redistribution rights.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

