# Publishing routine for Claude (Swabi website)

This is the Jekyll site for swabi.co.uk (GitHub Pages, auto-deploys on push to `main`). Blog posts live in `_posts/`. See `BLOGGING.md` for the post template and front matter. Keep this file free of passwords, keys and private details: the repo is public.

## When Sham says a post is approved ("publish it", "post it to the blog")
Do all of this without asking further questions:

1. Write the blog article as `_posts/YYYY-MM-DD-short-title.md` (today's date, lower-case hyphens). Copy the structure and tone of the existing posts: front matter (`title`, `description`, `tags`), a short opening paragraph, `<!--more-->`, then `##` sections, plain British English, a soft call to action linking to `/#contact`.
2. Facts must match the approved social post (dates, figures, sources). Add a short "Sources" list of links at the end.
3. Media:
   - Video: save the MP4 as `assets/blog/<short-title>.mp4` (keep under about 25 MB; if larger, tell Sham) and embed near the top of the article body after `<!--more-->` with:
     `<video controls playsinline preload="metadata" style="width:100%;max-width:420px;border-radius:12px"><source src="/assets/blog/<short-title>.mp4" type="video/mp4"></video>`
   - Carousel: export slides as JPGs under about 500 KB into `assets/blog/` and use `image:` / `image_alt:` front matter for the cover, with the rest as images in the body.
4. Do not change the site's design, navigation or existing posts unless asked.
5. Commit to `main` with a clear message and push. The site updates within a couple of minutes. Then reply with the live URL: `https://swabi.co.uk/blog/<short-title>/`.

## Scheduling a post for later
Give the post a future `date:` with a time and UK offset, e.g. `date: 2026-11-02 08:00:00 +0000` (GMT) or `+0100` (BST), and push it. It stays hidden until then. The `Scheduled publish` workflow checks every 15 minutes and rebuilds the site once the time has passed, so allow up to about 30 minutes. If a social post links to it, schedule the social post at least 30 minutes later. To publish straight away, use a date/time in the past.

## Rules
- Never publish anything Sham has not approved in chat.
- The content is general guidance, not personal tax advice. Do not give individual advice or promise outcomes.
- If the video file cannot be fetched, publish the article without it and tell Sham what is missing.
