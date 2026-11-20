import os, sys, shutil, subprocess, time
from news import fetch, mark
from reel import build
from publish import publish_reel
from config import HASHTAGS

def caption(it):
    s = it["summary"]
    s = (s[:220].rsplit(" ", 1)[0] + "...") if len(s) > 220 else s
    return (f"🚨 {it['title']}\n\n{s}\n\n📰 Source: {it['source']}\n"
            f"🔔 Follow @gta6pay for daily GTA 6 news!\n💬 What do you think? Comment below 👇\n\n{HASHTAGS}")

items = fetch()
if not items:
    print("No new GTA 6 news."); sys.exit(0)
it = items[0]
print("Selected:", it["title"])
mp4 = build(it)
cap = caption(it)
print(cap)
if not os.environ.get("IG_TOKEN"):
    print("DRY RUN (no IG_TOKEN) ->", mp4); sys.exit(0)

# host video publicly on the 'media' branch of this (public) repo
repo = os.environ["GITHUB_REPOSITORY"]
name = f"reel_{int(time.time())}.mp4"
sh = lambda *c: subprocess.run(c, check=True)
shutil.copy(mp4, f"/tmp/{name}")
sh("git", "fetch", "origin", "media")
sh("git", "worktree", "add", "/tmp/media", "origin/media")
shutil.copy(f"/tmp/{name}", f"/tmp/media/{name}")
sh("git", "-C", "/tmp/media", "add", name)
sh("git", "-C", "/tmp/media", "commit", "-qm", f"add {name}")
sh("git", "-C", "/tmp/media", "push", "origin", "HEAD:media")
url = f"https://raw.githubusercontent.com/{repo}/media/{name}"
time.sleep(20)
print("Published:", publish_reel(url, cap))
mark(it["link"])
