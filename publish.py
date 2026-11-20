import os, time, requests
G = "https://graph.facebook.com/v21.0"

def publish_reel(video_url, caption):
    tok, uid = os.environ["IG_TOKEN"], os.environ["IG_USER_ID"]
    r = requests.post(f"{G}/{uid}/media", data={"media_type": "REELS", "video_url": video_url,
                      "caption": caption, "share_to_feed": "true", "access_token": tok}).json()
    if "id" not in r:
        raise RuntimeError(r)
    cid = r["id"]
    for _ in range(40):
        s = requests.get(f"{G}/{cid}", params={"fields": "status_code,status", "access_token": tok}).json()
        if s.get("status_code") == "FINISHED":
            break
        if s.get("status_code") == "ERROR":
            raise RuntimeError(s)
        time.sleep(15)
    r = requests.post(f"{G}/{uid}/media_publish", data={"creation_id": cid, "access_token": tok}).json()
    if "id" not in r:
        raise RuntimeError(r)
    return r["id"]
