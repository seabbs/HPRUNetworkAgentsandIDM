#!/usr/bin/env -S uv run --with matplotlib --with pillow --script
"""A short video of the deck for social media.

Usage:
    ./scripts/social-video.py

The finished slides flip through on the left. On the right, the build
plays back: a clock, commits climbing, and my steers popping up as they
were sent. Long breaks are skipped. Ends on the how-it-was-built slide.
Needs ffmpeg, _shots/ from "task slides" and notes/build-timeline.csv.
Writes figures/agents-deck.mp4, which the prompts page embeds, and
_social/agents-deck.gif.
"""

import csv
import shutil
import subprocess
import textwrap
from datetime import datetime, timedelta
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

TEAL, SLATE, BRICK, INK, GREY = ("#1f6f8b", "#4a5899", "#b5432f", "#2b2b2b",
                                 "#6b7280")
W, H, FPS = 1920, 1080, 25
PLAY, END = 24.0, 4.0
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
OBLIQUE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf"
out = Path("_social")
frames = out / "frames"


def font(path, size):
    return ImageFont.truetype(path, size)


# A selection of my steers, typos corrected, at the time each was sent.
STEERS = [
    ("12:50", "We need to make a slide deck for a talk I need to give."),
    ("12:56", "You can commit to main as we work."),
    ("13:11", "We are finding it very hard to collaborate in an "
              "agent-driven environment."),
    ("15:38", "Challenges, not dangers."),
    ("15:41", "Have one that highlights what a tool-using LLM actually is."),
    ("15:44", "What agents do needs a picture of a rubber duck."),
    ("15:48", "Of course it is all currently very heavily subsidised."),
    ("15:53", "We don't have anything about how to use the time they "
              "give us?"),
    ("16:42", "The abstract is not how a human would write."),
    ("16:45", "Correct my typos in any copied-in prompts."),
    ("16:55", "This is good, but the figure is boring."),
    ("17:11", "Bit dry. Can we have emojis or little pictures?"),
    ("17:17", "Hmm, the emojis look kind of budget."),
    ("17:17", "Cut."),
    ("17:18", "I like them in how to collaborate. Okay, let's keep the "
              "emojis."),
    ("17:42", "We need the fire hose image."),
    ("19:08", "Can we make the title slide a bit more fun?"),
    ("19:14", "Agents often have a very spiky ability profile."),
    ("19:21", "Does the Merge and refit box still make sense?"),
    ("19:31", "Could we have a nice little slide after the thank you?"),
]

events = {"commit": [], "message": []}
with open("notes/build-timeline.csv") as f:
    for row in csv.DictReader(f):
        events[row["event"]].append(datetime.fromisoformat(row["time_utc"]))
commits, messages = sorted(events["commit"]), sorted(events["message"])
day = messages[0].date()
steers = [(datetime.combine(day, datetime.strptime(t, "%H:%M").time())
           + timedelta(seconds=30), s) for t, s in STEERS]
start, stop = messages[0] - timedelta(minutes=2), commits[-1]

# Skip long breaks: playback runs on active time, gaps capped at 2 min.
marks = sorted(messages + commits)
knots, acc = [(start, 0.0)], 0.0
for a, b in zip([start] + marks, marks):
    acc += min((b - a).total_seconds(), 120)
    knots.append((b, acc))


def session_time(sec):
    """Session clock time at a playback second."""
    target = sec / PLAY * acc
    for (t0, a0), (t1, a1) in zip(knots, knots[1:]):
        if a1 >= target:
            frac = 0 if a1 == a0 else (target - a0) / (a1 - a0)
            return t0 + (t1 - t0) * frac
    return stop


# The build graph, drawn once; frames reveal it up to the clock.
GW, GH = 600, 330
plt.rcParams.update({"font.size": 12, "font.family": "DejaVu Sans"})
fig = plt.figure(figsize=(GW / 100, GH / 100), dpi=100)
ax = fig.add_axes([0.1, 0.17, 0.87, 0.78])
ax.step(commits, range(1, len(commits) + 1), where="post", color=TEAL, lw=2.5)
ax.vlines(messages, -13, -4, color=BRICK, lw=1, alpha=0.7)
ax.set_xlim(start, stop + timedelta(minutes=4))
ax.set_ylim(-16, len(commits) + 6)
ax.set_yticks([0, 25, 50, 75])
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax.grid(axis="y", color="#e5e7eb")
for side in ("top", "right", "left"):
    ax.spines[side].set_visible(False)
ax.spines["bottom"].set_color(GREY)
ax.tick_params(colors=GREY, length=0)
fig.canvas.draw()
graph = Image.frombuffer("RGBA", fig.canvas.get_width_height(),
                         fig.canvas.buffer_rgba()).convert("RGB")
x0_plot, y_top = ax.transData.transform((mdates.date2num(start),
                                         len(commits) + 6))
_, y_bot = ax.transData.transform((mdates.date2num(start), -16))


def gx(t):
    return ax.transData.transform((mdates.date2num(t), 0))[0]


plt.close(fig)

slides = sorted(Path("_shots").glob("slide-*.png"))
deck, stats_slide = slides[:-1], slides[-1]
SW, SH = 1180, 664
thumbs = [Image.open(p).convert("RGB").resize((SW, SH), Image.LANCZOS)
          for p in deck]
sam = Image.open("figures/sam.jpg").convert("RGB").resize((56, 56))
mask = Image.new("L", (56, 56), 0)
ImageDraw.Draw(mask).ellipse((0, 0, 55, 55), fill=255)
banner = Image.open("figures/agents-title.png").convert("RGBA")
banner = banner.resize((420, int(420 * banner.height / banner.width)),
                       Image.LANCZOS)


def bubble(d, img, x, y, text, alpha):
    lines = textwrap.wrap(text, 40)
    h = 22 + 30 * len(lines)
    tint = tuple(int(255 - (255 - c) * alpha) for c in (181, 67, 47))
    d.rounded_rectangle((x + 70, y, x + 590, y + h), 18, outline=tint,
                        width=3, fill="white")
    for k, line in enumerate(lines):
        d.text((x + 90, y + 12 + 30 * k), line, font=font(OBLIQUE, 22),
               fill=tint)
    if alpha > 0.5:
        img.paste(sam, (x, y + 4), mask)
    return h


def frame(sec):
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    d.text((60, 48), "AI agents in infectious disease modelling",
           font=font(BOLD, 46), fill=INK)
    d.text((60, 112), "Built by agents in one afternoon, steered by me",
           font=font(FONT, 28), fill=GREY)
    img.paste(banner, (W - 60 - banner.width, 30), banner)
    # The finished deck flips through, with a short crossfade.
    pos = sec / PLAY * len(thumbs)
    i = min(int(pos), len(thumbs) - 1)
    fade = min(max((pos - i - 0.85) / 0.15, 0), 1)
    slide = thumbs[i] if fade == 0 or i + 1 >= len(thumbs) else \
        Image.blend(thumbs[i], thumbs[i + 1], fade)
    d.rectangle((52, 202, 60 + SW + 8, 210 + SH + 8), fill="#e5e7eb")
    img.paste(slide, (56, 206))
    # The build plays back on the right.
    now = session_time(sec)
    rx = 1290
    d.text((rx, 196), now.strftime("%H:%M"), font=font(BOLD, 64), fill=INK)
    d.text((rx + 250, 230), "UTC, 2 November", font=font(FONT, 22),
           fill=GREY)
    n_c = sum(c <= now for c in commits)
    n_m = sum(m <= now for m in messages)
    d.text((rx, 280), f"{n_c} commits", font=font(BOLD, 28), fill=TEAL)
    d.text((rx + 230, 280), f"{n_m} messages from me", font=font(BOLD, 28),
           fill=BRICK)
    g = graph.copy()
    cut = gx(now)
    ImageDraw.Draw(g).rectangle((cut + 1, GH - y_top - 2, GW, GH - y_bot + 2),
                                fill="white")
    img.paste(g, (rx - 30, 320))
    # My steers pop up as they were sent, newest first.
    y = 680
    shown = [(t, s) for t, s in steers if t <= now][-3:][::-1]
    for k, (t, s) in enumerate(shown):
        if y > H - 60:
            break
        y += bubble(d, img, rx, y, s, 1.0 if k == 0 else 0.45) + 14
    return img


def end_frame(sec):
    img = Image.open(stats_slide).convert("RGB").resize((W, H), Image.LANCZOS)
    d = ImageDraw.Draw(img)
    d.rectangle((0, H - 90, W, H), fill=TEAL)
    d.text((60, H - 70), "samabbott.co.uk/HPRUNetworkAgentsandIDM",
           font=font(BOLD, 40), fill="white")
    d.text((W - 640, H - 64), "Slides, every prompt, and the code",
           font=font(FONT, 30), fill="white")
    return img


shutil.rmtree(frames, ignore_errors=True)
frames.mkdir(parents=True)
n_play, n_end = int(PLAY * FPS), int(END * FPS)
last = None
for k in range(n_play):
    last = frame(k / FPS)
    last.save(frames / f"f{k:04d}.png")
end = end_frame(0)
for k in range(n_end):
    blend = min(k / (FPS * 0.6), 1)
    Image.blend(last, end, blend).save(frames / f"f{n_play + k:04d}.png")

subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
                "-i", str(frames / "f%04d.png"), "-c:v", "libx264",
                "-pix_fmt", "yuv420p", "-crf", "20",
                str(Path("figures/agents-deck.mp4"))], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i",
                "figures/agents-deck.mp4", "-vf",
                "fps=12,scale=960:-1:flags=lanczos,split[a][b];"
                "[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=bayer",
                str(out / "agents-deck.gif")], check=True)
shutil.rmtree(frames)
print("wrote figures/agents-deck.mp4 and _social/agents-deck.gif")
