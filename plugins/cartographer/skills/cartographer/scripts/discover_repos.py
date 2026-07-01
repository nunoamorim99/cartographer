#!/usr/bin/env python3
"""
discover_repos.py — read-only git discovery for the Cartographer documentation skill.

Two modes:

  Scan (default):
      python3 discover_repos.py [PROJECT_ROOT]
    Scans immediate subdirectories of the root, detects git repositories, and reports
    the facts the documentation workflow needs: branches, default branch, HEAD commit,
    unmerged feature work, and value-bearing files. It reports facts and a *conservative
    documentation-signal hint* — it deliberately does NOT make the thin/not-thin
    judgment, because that requires reading the content, which is the model's job.

  Commit log between two points (for drift + "What's new"):
      python3 discover_repos.py --log REPO_PATH SINCE_SHA [UNTIL_REF]
    Lists the commits on UNTIL_REF (default: the repo's default branch) that are not in
    SINCE_SHA, newest first. This is what grounds drift detail and the "What's new"
    bullets in the real commit range rather than guessing from the latest commit alone.

This script NEVER writes to any repository. It runs git only in read-only modes
(rev-parse, for-each-ref, log, rev-list, symbolic-ref). No commits, checkouts, fetches,
or branch changes. All interpretation (role classification, HOW->WHAT translation, prose,
and the final thin-doc call) is left to the model.
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

VALUE_BEARING = {
    "stakeholder": ["STAKEHOLDER.md", "STAKEHOLDER.MD", "stakeholder.md"],
    "readme": ["README.md", "README.MD", "README.rst", "README.txt", "README", "readme.md"],
    "changelog": ["CHANGELOG.md", "CHANGELOG", "CHANGELOG.MD", "HISTORY.md", "changelog.md"],
}
DOC_DIRS = ["docs", "doc", "documentation"]

# Conservative word thresholds for the documentation-signal HINT only.
# The model makes the real call after reading the content.
MINIMAL_README_WORDS = 25   # below this, with nothing else, signal is "minimal"
EMPTY_README_WORDS = 5      # at/below this the readme carries effectively no signal

# Signature phrases of generated/scaffold READMEs. A README that is mostly boilerplate
# carries no real product signal even when it is long — so the script flags it and the
# model should look past it to the real surfaces (docs/, product sheets, STAKEHOLDER.md).
BOILERPLATE_SIGNS = (
    "this project was bootstrapped with create react app",
    "create-react-app",
    "welcome to your expo app",
    "npx create-expo-app",
    "npx expo",
    "this is a next.js project bootstrapped with",
    "create-next-app",
    "this template provides a minimal setup to get",   # Vite templates
    "vite + react", "vite + vue",
    "getting started with create",
    "npm run dev` to start",
    "edit `app/page",
)


def run_git(repo_path, args, timeout=20):
    try:
        result = subprocess.run(
            ["git", "-C", repo_path] + args,
            capture_output=True, text=True, timeout=timeout,
        )
        if result.returncode != 0:
            return False, result.stderr.strip()
        return True, result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as exc:
        return False, str(exc)


def is_git_repo(path):
    if not os.path.exists(os.path.join(path, ".git")):
        return False
    ok, out = run_git(path, ["rev-parse", "--is-inside-work-tree"])
    return ok and out == "true"


def default_branch(repo_path, local_branches):
    ok, out = run_git(repo_path, ["symbolic-ref", "refs/remotes/origin/HEAD"])
    if ok and out:
        return out.rsplit("/", 1)[-1]
    for candidate in ("main", "master"):
        if candidate in local_branches:
            return candidate
    ok, out = run_git(repo_path, ["rev-parse", "--abbrev-ref", "HEAD"])
    return out if ok else None


def list_local_branches(repo_path):
    ok, out = run_git(
        repo_path, ["for-each-ref", "--format=%(refname:short)", "refs/heads"]
    )
    if not ok or not out:
        return []
    return [b for b in out.splitlines() if b]


def commits_between(repo_path, since_sha, until_ref):
    """Commits in until_ref but not in since_sha, newest first."""
    fmt = "%H%x1f%h%x1f%cI%x1f%an%x1f%s"
    ok, out = run_git(
        repo_path, ["log", f"--format={fmt}", f"{since_sha}..{until_ref}"]
    )
    if not ok or not out:
        return []
    commits = []
    for line in out.splitlines():
        parts = line.split("\x1f")
        if len(parts) >= 5:
            commits.append({
                "sha": parts[0], "short_sha": parts[1], "date": parts[2],
                "author": parts[3], "subject": parts[4],
            })
    return commits


def unmerged_count(repo_path, branch, base):
    if branch == base:
        return 0
    ok, out = run_git(repo_path, ["rev-list", "--count", f"{base}..{branch}"])
    return int(out) if ok and out.isdigit() else 0


def last_commit(repo_path, ref):
    fmt = "%H%x1f%h%x1f%cI%x1f%an%x1f%s"
    ok, out = run_git(repo_path, ["log", "-1", f"--format={fmt}", ref])
    if not ok or not out:
        return None
    parts = out.split("\x1f")
    if len(parts) < 5:
        return None
    return {"sha": parts[0], "short_sha": parts[1], "date": parts[2],
            "author": parts[3], "subject": parts[4]}


def find_value_files(path):
    found = {"stakeholder": None, "readme": None, "changelog": None, "doc_dirs": []}
    try:
        entries = set(os.listdir(path))
    except OSError:
        return found
    for kind, names in VALUE_BEARING.items():
        for name in names:
            if name in entries:
                found[kind] = name
                break
    for d in DOC_DIRS:
        if os.path.isdir(os.path.join(path, d)):
            found["doc_dirs"].append(d)
    return found


def readme_metrics(path, readme_name):
    """Return (bytes, words, is_boilerplate) for the README, or (0, 0, False)."""
    if not readme_name:
        return 0, 0, False
    full = os.path.join(path, readme_name)
    try:
        with open(full, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        lowered = text.lower()
        boiler = any(sign in lowered for sign in BOILERPLATE_SIGNS)
        return os.path.getsize(full), len(text.split()), boiler
    except OSError:
        return 0, 0, False


def doc_signal(value, readme_words, readme_boilerplate):
    """A CONSERVATIVE hint, not a verdict. The model decides thinness from content.
    - present : has a STAKEHOLDER.md, a docs/ dir, or a substantive non-boilerplate README
    - minimal : only a short README, or a README that is mostly generated scaffold text
    - none    : effectively no documentation surface at all

    A long boilerplate README (Expo/CRA/Next scaffold) does NOT count as 'present' on its
    own — it carries no product signal. The model should look to docs/ or a product sheet.
    """
    if value["stakeholder"] or value["doc_dirs"]:
        return "present"
    if readme_words >= MINIMAL_README_WORDS and not readme_boilerplate:
        return "present"
    if readme_words > EMPTY_README_WORDS:
        return "minimal"
    return "none"


def assess_repo(name, path):
    local = list_local_branches(path)
    base = default_branch(path, local)

    feature_branches = []
    for b in local:
        if b == base:
            continue
        ahead = unmerged_count(path, b, base) if base else 0
        if ahead > 0:
            feature_branches.append({
                "branch": b,
                "commits_ahead_of_default": ahead,
                "last_commit": last_commit(path, b),
            })
    feature_branches.sort(key=lambda x: x["commits_ahead_of_default"], reverse=True)

    value = find_value_files(path)
    r_bytes, r_words, r_boiler = readme_metrics(path, value["readme"])

    return {
        "name": name,
        "path": path,
        "is_git_repo": True,
        "default_branch": base,
        "local_branches": local,
        "branch_count": len(local),
        "head": last_commit(path, "HEAD"),
        "default_branch_head": last_commit(path, base) if base else None,
        "feature_branches_with_unmerged_work": feature_branches,
        "has_unmerged_feature_work": len(feature_branches) > 0,
        "value_bearing_files": {
            "stakeholder_md": value["stakeholder"],
            "readme": value["readme"],
            "readme_bytes": r_bytes,
            "readme_words": r_words,
            "readme_boilerplate": r_boiler,
            "changelog": value["changelog"],
            "doc_dirs": value["doc_dirs"],
        },
        # A HINT only — read the content before deciding a repo is too thin to document.
        "doc_signal": doc_signal(value, r_words, r_boiler),
    }


def scan(root):
    root = os.path.abspath(root)
    repos, non_repo_dirs = [], []
    try:
        entries = sorted(os.listdir(root))
    except OSError as exc:
        return {"error": f"cannot read project root: {exc}", "root": root}

    for entry in entries:
        if entry.startswith("."):
            continue
        full = os.path.join(root, entry)
        if not os.path.isdir(full):
            continue
        if entry in ("Stakeholder-Docs", "node_modules", "__pycache__"):
            continue
        if is_git_repo(full):
            repos.append(assess_repo(entry, full))
        else:
            non_repo_dirs.append(entry)

    return {
        "root": root,
        "scanned_at": datetime.now(timezone.utc).isoformat(),
        "repo_count": len(repos),
        "repos": repos,
        "non_repo_dirs": non_repo_dirs,
    }


def main():
    ap = argparse.ArgumentParser(description="Read-only git discovery for Cartographer.")
    ap.add_argument("root", nargs="?", default=os.getcwd(),
                    help="Project root to scan (default: cwd).")
    ap.add_argument("--log", nargs=2, metavar=("REPO", "SINCE"),
                    help="List commits in REPO reachable from UNTIL but not SINCE.")
    ap.add_argument("--until", default=None,
                    help="End ref for --log (default: the repo's default branch).")
    args = ap.parse_args()

    if args.log:
        repo, since = args.log
        repo = os.path.abspath(repo)
        until = args.until
        if until is None:
            until = default_branch(repo, list_local_branches(repo)) or "HEAD"
        result = {
            "repo": repo, "since": since, "until": until,
            "commits": commits_between(repo, since, until),
        }
    else:
        result = scan(args.root)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
