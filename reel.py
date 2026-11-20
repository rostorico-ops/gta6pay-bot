import os, asyncio, subprocess, textwrap, random
from PIL import Image, ImageDraw, ImageFont
import edge_tts
from config import VOICE

W, H = 1080, 1920
FONTS = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
         "/System/Library/Fonts/Supplemental/Arial Bold.ttf"]
PALETTES = [((255, 0, 128), (40, 0, 90)), ((255, 120, 0), (90, 0, 60)), ((0, 200, 255), (60, 0, 120))]

def font(size):
    for f in FONTS:
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()

def card(title, source, path):
    top, bot = random.choice(PALETTES)
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        r = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(top[i] * (1 - r) + bot[i] * r) for i in range(3)))
    d.rectangle([60, 260, 520, 360], fill=(0, 0, 0))
    d.text((90, 275), "GTA 6 NEWS", font=font(64), fill=(255, 255, 255))
    y = 520
    for line in textwrap.wrap(title.upper(), 18)[:8]:
        d.text((64, y + 4), line, font=font(88), fill=(0, 0, 0))
        d.text((60, y), line, font=font(88), fill=(255, 255, 255))
        y += 110
    d.text((60, H - 330), "Source: " + source[:40], font=font(42), fill=(255, 255, 255))
    d.text((60, H - 260), "Follow @gta6pay for daily GTA 6 updates", font=font(42), fill=(255, 230, 0))
    img.save(path)

def build(item, out="out"):
    os.makedirs(out, exist_ok=True)
    png, mp3, mp4 = f"{out}/card.png", f"{out}/voice.mp3", f"{out}/reel.mp4"
    card(item["title"], item["source"], png)
    script = f"GTA 6 news. {item['title']}. {item['summary'][:250]} Follow for daily GTA 6 updates."
    asyncio.run(edge_tts.Communicate(script, VOICE).save(mp3))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", png, "-i", mp3,
        "-vf", "scale=1200:-1,zoompan=z='min(zoom+0.0006,1.15)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,format=yuv420p",
        "-c:v", "libx264", "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", mp4], check=True)
    return mp4
