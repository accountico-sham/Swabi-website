"""Prints 'yes' if any blog post's publish time has passed since the last site build, else 'no'.

Usage: python due_posts.py <last-build-ISO-time>
Jekyll hides future-dated posts until the site is rebuilt, so the scheduler workflow
uses this to decide when a rebuild is needed.
"""
import pathlib, re, sys
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

UK = ZoneInfo("Europe/London")
last_build = datetime.fromisoformat(sys.argv[1].replace("Z", "+00:00"))
now = datetime.now(timezone.utc)

def post_time(path):
    text = path.read_text(encoding="utf-8")
    fm = text.split("---", 2)[1] if text.startswith("---") else ""
    m = re.search(r"^date:\s*(.+)$", fm, re.M)
    if m:
        raw = m.group(1).strip().strip('"\'')
        for fmt in ("%Y-%m-%d %H:%M:%S %z", "%Y-%m-%d %H:%M %z", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
            try:
                dt = datetime.strptime(raw, fmt)
                return dt if dt.tzinfo else dt.replace(tzinfo=UK)
            except ValueError:
                pass
    d = re.match(r"(\d{4}-\d{2}-\d{2})", path.name)
    return datetime.strptime(d.group(1), "%Y-%m-%d").replace(tzinfo=UK) if d else None

due = []
for p in sorted(pathlib.Path("_posts").glob("*.md")):
    t = post_time(p)
    if t and last_build < t <= now:
        due.append(f"{p.name} (due {t.isoformat()})")

for d in due:
    print("Due:", d, file=sys.stderr)
print("yes" if due else "no")
