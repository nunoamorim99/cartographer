#!/usr/bin/env python3
"""
build_pdf.py — render a stakeholder Markdown document to a B&W PDF.

Pipeline: Markdown -> styled HTML -> WeasyPrint -> PDF.

DEPENDENCIES & SELF-BOOTSTRAP
  This script needs the Python packages `markdown` and `weasyprint`. Many machines
  block a global `pip install` (PEP 668, "externally-managed-environment"). To avoid
  forcing a manual setup, if the packages are missing this script transparently creates
  a private virtual environment INSIDE THE SKILL (scripts/.venv, falling back to
  ~/.cache/cartographer/venv if the skill dir is read-only), installs the packages there,
  and re-runs itself. The venv lives with the skill, never in the user's project.

  WeasyPrint also needs system libraries (Pango, Cairo, GDK-PixBuf) that a venv cannot
  install. If those are absent, this script prints exactly what to install and exits with
  a non-zero status — the calling workflow should still deliver the .md and skip the .pdf.

Conventions enforced so output matches the documentation standard:
  - The first H1 keeps its italic subtitle line styled as a subtitle.
  - A leading "What's new" block is wrapped in a bordered banner.
  - An optional --wordmark sets the lower-left footer label.
  - Diacritics are verified for accented languages (from the .<lang>.md suffix).

Usage:
    python3 build_pdf.py INPUT.md [OUTPUT.pdf] [--wordmark LABEL]
"""

import argparse
import os
import re
import subprocess
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CSS = os.path.join(HERE, "style.css")
PKG_DEPS = ["markdown", "weasyprint"]

# ---------------------------------------------------------------------------
# Dependency self-bootstrap (runs before the heavy imports)
# ---------------------------------------------------------------------------

def _have_deps():
    try:
        import markdown  # noqa: F401
        import weasyprint  # noqa: F401
        return True
    except Exception:
        return False


def _venv_python(venv_dir):
    sub = "Scripts" if os.name == "nt" else "bin"
    exe = "python.exe" if os.name == "nt" else "python"
    return os.path.join(venv_dir, sub, exe)


def _candidate_venv_dirs():
    # Prefer a venv inside the skill (self-contained, not in the user's project);
    # fall back to a user cache dir if the skill directory is read-only.
    yield os.path.join(HERE, ".venv")
    cache = os.environ.get("XDG_CACHE_HOME") or os.path.join(
        os.path.expanduser("~"), ".cache")
    yield os.path.join(cache, "cartographer", "venv")


def _fail_deps():
    sys.stderr.write(
        "[cartographer] Could not prepare the PDF toolchain (markdown + weasyprint).\n"
        "  The Markdown (.md) document is unaffected — only the .pdf was skipped.\n"
        "  WeasyPrint needs system libraries a virtual env cannot install:\n"
        "    Debian/Ubuntu: sudo apt-get install -y libpango-1.0-0 libpangocairo-1.0-0 "
        "libgdk-pixbuf-2.0-0 libffi-dev\n"
        "    macOS (brew):  brew install pango cairo gdk-pixbuf libffi\n"
        "  Then re-run, or produce PDFs later — the .md files are complete on their own.\n"
    )
    sys.exit(3)


def ensure_deps_or_reexec():
    """Make markdown + weasyprint importable, creating a private venv if needed."""
    if _have_deps():
        return
    if os.environ.get("CARTOGRAPHER_PDF_BOOTSTRAPPED") == "1":
        _fail_deps()  # already re-execed once and they are still missing
    for venv_dir in _candidate_venv_dirs():
        py = _venv_python(venv_dir)
        try:
            if not os.path.exists(py):
                subprocess.run([sys.executable, "-m", "venv", venv_dir],
                               check=True, capture_output=True)
            subprocess.run([py, "-m", "pip", "install", "-q",
                            "--disable-pip-version-check", *PKG_DEPS],
                           check=True, capture_output=True)
        except Exception:
            continue  # this location failed (read-only, etc.) — try the next
        env = dict(os.environ, CARTOGRAPHER_PDF_BOOTSTRAPPED="1")
        try:
            os.execve(py, [py, os.path.abspath(__file__), *sys.argv[1:]], env)
        except Exception:
            continue
    _fail_deps()


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

LATIN_DIACRITICS = set("áàâãäéèêëíìîïóòôõöúùûüçñ"
                       "ÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇÑ")
DIACRITIC_LANGS = {"pt", "es", "fr", "it", "de", "ca", "ro", "pl", "tr", "nl"}
WHATS_NEW_TITLES = (
    "what's new", "whats new", "novidades", "o que há de novo",
    "novedades", "nouveautés", "novità", "neuigkeiten", "was ist neu",
)


def lang_from_filename(path):
    m = re.search(r"\.([a-z]{2})\.md$", os.path.basename(path), re.IGNORECASE)
    return m.group(1).lower() if m else None


def diacritics_present(text):
    return sorted({ch for ch in text if ch in LATIN_DIACRITICS})


def wrap_subtitle(html):
    pattern = re.compile(r"(<h1[^>]*>.*?</h1>)\s*<p><em>(.*?)</em></p>", re.DOTALL)
    return pattern.sub(r'\1\n<p class="subtitle"><em>\2</em></p>', html, count=1)


def wrap_whats_new(html):
    heading_re = re.compile(
        r'(<h[23][^>]*>\s*(?:[^<]*?)\s*</h[23]>)\s*(<ul>.*?</ul>)',
        re.DOTALL | re.IGNORECASE,
    )

    def repl(m):
        heading_text = re.sub(r"<[^>]+>", "", m.group(1)).strip().lower()
        if any(t in heading_text for t in WHATS_NEW_TITLES):
            return f'<div class="whats-new">{m.group(1)}{m.group(2)}</div>'
        return m.group(0)

    return heading_re.sub(repl, html, count=1)


def md_to_html(md_text, lang="en"):
    import markdown
    body = markdown.markdown(md_text, extensions=["tables", "sane_lists", "attr_list"])
    body = wrap_subtitle(body)
    body = wrap_whats_new(body)
    return (f"<!DOCTYPE html><html lang='{lang}'><head><meta charset='utf-8'></head>"
            f"<body>{body}</body></html>")


def wordmark_css_string(label):
    safe = label.replace('"', '\\"')
    return ('@page { @bottom-left { '
            f'content: "{safe}"; '
            'font-family: "Fira Sans", "DejaVu Sans", sans-serif; '
            'font-size: 8pt; letter-spacing: 2px; color: #000; } }')


def check_diacritics(md_text, input_path):
    lang = lang_from_filename(input_path)
    present = diacritics_present(md_text)
    if present:
        sys.stderr.write(
            f"[diacritics] accented characters present ({''.join(present)}). "
            f"Verify they render in the PDF.\n")
        return
    if lang in DIACRITIC_LANGS:
        sys.stderr.write(
            f"[diacritics] WARNING: {os.path.basename(input_path)} is tagged language "
            f"'{lang}', which uses accents, but none were found. Check diacritics.\n")


def build(input_path, output_path=None, css_path=DEFAULT_CSS, wordmark=None):
    from weasyprint import HTML, CSS
    from weasyprint.text.fonts import FontConfiguration
    # A FontConfiguration is REQUIRED for @font-face fonts to load and embed; without it
    # WeasyPrint silently ignores @font-face and falls back to system fonts.
    font_config = FontConfiguration()
    with open(input_path, "r", encoding="utf-8") as f:
        md_text = unicodedata.normalize("NFC", f.read())
    if output_path is None:
        output_path = os.path.splitext(input_path)[0] + ".pdf"
    lang = lang_from_filename(input_path) or "en"
    # CSS(filename=...) sets its base_url to the stylesheet's own location, so the
    # @font-face url("fonts/...") references resolve next to style.css (scripts/fonts/).
    stylesheets = [CSS(filename=css_path, font_config=font_config)]
    if wordmark:
        stylesheets.append(CSS(string=wordmark_css_string(wordmark),
                               font_config=font_config))
    HTML(string=md_to_html(md_text, lang), base_url=HERE).write_pdf(
        output_path, stylesheets=stylesheets, font_config=font_config)
    check_diacritics(md_text, input_path)
    return output_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output", nargs="?", default=None)
    ap.add_argument("--wordmark", default=None,
                    help="Footer label shown lower-left (e.g. the project name).")
    args = ap.parse_args()
    ensure_deps_or_reexec()   # may create a venv and re-exec into it
    print(build(args.input, args.output, wordmark=args.wordmark))


if __name__ == "__main__":
    main()
