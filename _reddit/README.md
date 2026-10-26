# Scheduled Reddit posts

Each `.md` file here is one Reddit post. The `Scheduled publish` workflow checks every
15 minutes and posts anything whose `when:` time has passed, then adds `posted:` and
`reddit_url:` to the file so it is never posted twice.

Name files `YYYY-MM-DD-short-title.md` and use this template:

```
---
title: "Your Reddit post title"
when: 2026-11-02 08:00          # UK time, 24-hour clock
subreddit: Crypto_Taxes_UK      # optional (this is the default)
link: https://swabi.co.uk/...   # optional: makes it a link post
flair: Announcement             # optional: must already exist on the subreddit
---
Post text in Reddit markdown, e.g. [link text](https://example.com).
```

Note: this repository is public, so anything queued here can be seen on GitHub before it posts.
Nothing posts until the Reddit secrets are added (REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET,
REDDIT_USERNAME, REDDIT_PASSWORD) under Settings > Secrets and variables > Actions.
