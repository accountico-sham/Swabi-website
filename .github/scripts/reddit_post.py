"""Posts any due Reddit posts queued in _reddit/ and marks them as posted.

Each file in _reddit/ looks like:

    ---
    title: "Where else to find us (this sub came first)"
    when: 2026-11-02 08:00          # UK time
    subreddit: Crypto_Taxes_UK      # optional, this is the default
    link: https://swabi.co.uk/...   # optional: makes it a link post instead of text
    flair: Announcement             # optional: flair text, must already exist on the sub
    ---
    Body text in Reddit markdown (ignored for link posts).

After posting, the script adds `posted:` and `reddit_url:` to the file so it is never posted twice.
Needs secrets: REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD.
"""
import os, pathlib, re, sys
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

UK = ZoneInfo("Europe/London")
QUEUE = pathlib.Path("_reddit")
need = ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USERNAME", "REDDIT_PASSWORD"]
if any(not os.environ.get(k) for k in need):
    print("Reddit credentials not set up yet. Skipping.")
    sys.exit(0)

def parse(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return None, None, text
    meta = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        if _:
            meta[k.strip()] = re.sub(r"\s+#.*$", "", v).strip().strip('"\'')
    return meta, m.group(2).strip(), text

def due_time(raw):
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(raw, fmt).replace(tzinfo=UK)
        except ValueError:
            pass
    raise ValueError(f"Can't read time: {raw!r} (use YYYY-MM-DD HH:MM, UK time)")

now = datetime.now(timezone.utc)
due = []
for p in sorted(QUEUE.glob("*.md")):
    meta, body, text = parse(p)
    if not meta or meta.get("posted") or not meta.get("when"):
        continue
    if due_time(meta["when"]) <= now:
        due.append((p, meta, body, text))

if not due:
    print("No Reddit posts due.")
    sys.exit(0)

import praw
reddit = praw.Reddit(
    client_id=os.environ["REDDIT_CLIENT_ID"],
    client_secret=os.environ["REDDIT_CLIENT_SECRET"],
    username=os.environ["REDDIT_USERNAME"],
    password=os.environ["REDDIT_PASSWORD"],
    user_agent="swabi-scheduler/1.0 (by u/" + os.environ["REDDIT_USERNAME"] + ")",
)

for p, meta, body, text in due:
    sub = reddit.subreddit(meta.get("subreddit", "Crypto_Taxes_UK"))
    kwargs = {"title": meta["title"]}
    if meta.get("flair"):
        for f in sub.flair.link_templates.user_selectable():
            if f["flair_text"] == meta["flair"]:
                kwargs["flair_id"] = f["flair_template_id"]
    if meta.get("link"):
        post = sub.submit(url=meta["link"], **kwargs)
    else:
        post = sub.submit(selftext=body, **kwargs)
    url = "https://www.reddit.com" + post.permalink
    stamp = now.astimezone(UK).strftime("%Y-%m-%d %H:%M")
    p.write_text(text.replace("\n---\n", f"\nposted: {stamp}\nreddit_url: {url}\n---\n", 1), encoding="utf-8")
    print(f"Posted {p.name}: {url}")
