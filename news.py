import json, re, html, feedparser
from config import FEEDS, KEYWORDS

def clean(t):
    t = re.sub(r"<[^>]+>", " ", html.unescape(t or ""))
    return re.sub(r"\s+", " ", t).strip()

def fetch():
    posted = set(json.load(open("posted.json")))
    items = []
    for url in FEEDS:
        try:
            d = feedparser.parse(url, agent="Mozilla/5.0 gta6pay-bot")
        except Exception:
            continue
        for e in d.entries[:30]:
            title = clean(e.get("title"))
            title = re.sub(r"\s+-\s+[^-]+$", "", title) if "news.google" in url else title
            text = (title + " " + clean(e.get("summary"))).lower()
            if not any(k in text for k in KEYWORDS) or e.get("link") in posted:
                continue
            src = clean(e.get("source", {}).get("title")) if e.get("source") else d.feed.get("title", "")
            summ = clean(e.get("summary"))
            if summ.lower().startswith(title.lower()[:30]): summ = ""
            items.append({"title": title, "summary": summ[:400],
                          "link": e.get("link"), "source": src or "web",
                          "ts": tuple(e.get("published_parsed") or (0,))})
    items.sort(key=lambda x: x["ts"], reverse=True)
    return items

def mark(link):
    p = json.load(open("posted.json"))
    p.append(link)
    json.dump(p[-500:], open("posted.json", "w"), indent=0)
