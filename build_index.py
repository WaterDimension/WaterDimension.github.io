"""Generate site/data/notes.json and copy notebook files into site/notes/.

Renames Chinese filenames into safe slugs for hosting. Extracts a title from
the first <h1>/<h2>/<title> in HTML or first heading in Markdown, and infers
a tag/category from filename keywords.
"""

import json
import os
import re
import shutil
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "notebook"
DST = ROOT / "site" / "notes"
DATA = ROOT / "site" / "data"

DST.mkdir(parents=True, exist_ok=True)
DATA.mkdir(parents=True, exist_ok=True)

# Clean previous notes copies (keep dir)
for p in DST.iterdir():
    if p.is_file():
        p.unlink()


CATEGORY_RULES = [
    ("Redis", "Redis"),
    ("Redisson", "Redis"),
    ("Lua", "Redis"),
    ("MySQL", "数据库"),
    ("Spring", "Spring"),
    ("@Autowired", "Spring"),
    ("@Resource", "Spring"),
    ("Maven", "工程化"),
    ("YAML", "Spring"),
    ("Cookie", "Web基础"),
    ("Session", "Web基础"),
    ("TCP", "计算机网络"),
    ("IP", "计算机网络"),
    ("AOP", "Spring"),
    ("Git", "工程化"),
    ("算法", "算法"),
    ("黑马点评", "项目实战"),
    ("秒杀", "项目实战"),
    ("缓存", "Redis"),
    ("分布式锁", "Redis"),
    ("事务", "数据库"),
]


def detect_category(name: str) -> str:
    for kw, cat in CATEGORY_RULES:
        if kw.lower() in name.lower():
            return cat
    return "其他"


def slugify(name: str, idx: int) -> str:
    """Make a stable, URL-safe slug. Falls back to numeric id if name is all CJK."""
    base = unicodedata.normalize("NFKD", name)
    base = re.sub(r"[^A-Za-z0-9]+", "-", base).strip("-").lower()
    if not base or len(base) < 3:
        base = f"note-{idx:02d}"
    return f"{idx:02d}-{base}"[:60]


HTML_TITLE_RE = re.compile(r"<title>(.*?)</title>", re.IGNORECASE | re.DOTALL)
HTML_H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.IGNORECASE | re.DOTALL)
HTML_H2_RE = re.compile(r"<h2[^>]*>(.*?)</h2>", re.IGNORECASE | re.DOTALL)
TAG_RE = re.compile(r"<[^>]+>")


def extract_title(text: str, kind: str, fallback: str) -> str:
    if kind == "md":
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("#"):
                return line.lstrip("#").strip() or fallback
        return fallback
    # html
    for r in (HTML_H1_RE, HTML_H2_RE, HTML_TITLE_RE):
        m = r.search(text)
        if m:
            t = TAG_RE.sub("", m.group(1)).strip()
            t = re.sub(r"\s+", " ", t)
            if t:
                return t
    return fallback


def first_paragraph(text: str, kind: str) -> str:
    if kind == "md":
        # strip headings
        for line in text.splitlines():
            s = line.strip()
            if not s or s.startswith("#") or s.startswith("!") or s.startswith("```"):
                continue
            return s[:140]
        return ""
    # html: find first <p>
    m = re.search(r"<p[^>]*>(.*?)</p>", text, re.IGNORECASE | re.DOTALL)
    if not m:
        return ""
    s = TAG_RE.sub("", m.group(1)).strip()
    s = re.sub(r"\s+", " ", s)
    return s[:140]


def file_kind(path: Path) -> str:
    return "md" if path.suffix.lower() == ".md" else "html"


notes = []
files = sorted([p for p in SRC.iterdir() if p.suffix.lower() in (".html", ".md")])
FALLBACK_TITLE_BY_STEM = {
    "Spring 声明式事务 @Transactional 完整详解（面试+开发必备） (1)": "Spring 声明式事务 @Transactional 完整详解",
    "算法基础模板大全（覆盖绝大多数基础算法）": "算法基础模板大全（覆盖绝大多数基础算法）",
    "解决Redis排序后MySQL查询乱序问题：从原因到落地（通用版） (1)": "解决 Redis 排序后 MySQL 查询乱序问题（通用版）",
    "超级实用的 AOP 指南": "超级实用的 AOP 指南",
    "黑马点评-day02-缓存笔记": "黑马点评 day02：缓存笔记",
    "黑马点评-day03-秒杀笔记": "黑马点评 day03：秒杀笔记",
    "Redis+Lua实现秒杀优化": "Redis + Lua 实现秒杀优化",
}

for idx, src in enumerate(files, start=1):
    # utf-8-sig strips the BOM that some editors prepend (e.g. typora)
    text = src.read_text(encoding="utf-8-sig", errors="ignore")
    kind = file_kind(src)
    forced = FALLBACK_TITLE_BY_STEM.get(src.stem)
    title = forced or extract_title(text, kind, src.stem)
    summary = first_paragraph(text, kind)
    slug = slugify(src.stem, idx)
    out_name = f"{slug}.{kind}"
    shutil.copy2(src, DST / out_name)
    category = detect_category(src.stem + " " + title)
    notes.append(
        {
            "id": slug,
            "title": title,
            "category": category,
            "kind": kind,
            "file": out_name,
            "summary": summary,
            "size": src.stat().st_size,
        }
    )

(DATA / "notes.json").write_text(
    json.dumps(notes, ensure_ascii=False, indent=2), encoding="utf-8"
)

print(f"Copied {len(notes)} notes -> {DST}")
print(f"Index -> {DATA / 'notes.json'}")
