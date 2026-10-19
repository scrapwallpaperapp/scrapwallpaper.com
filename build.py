#!/usr/bin/env python3
"""Builds Scrap's website (scrapwallpaper.com) from the parts in this folder.

Run:  python3 build.py
Writes: index.html, privacy/index.html (from the app's own privacy-policy.txt, so the words never drift apart),
support/index.html, 404.html. The pages are plain files; GitHub Pages serves them as they are.
"""
import pathlib, re, html

HERE = pathlib.Path(__file__).resolve().parent
APP_POLICY = HERE.parent / "Android App/app/src/main/assets/privacy-policy.txt"
SITE = "https://scrapwallpaper.com"
EMAIL = "scrapwallpaperapp@gmail.com"

# ---- shared pieces --------------------------------------------------------------------------------------------
HOLDER_CSS = """
.mp { position: absolute; left: 51.5%; top: 0; margin-top: 6%; width: min(28%, 150px); aspect-ratio: 220 / 205; z-index: 2; pointer-events: none; transform: translate(-50%, -50%) rotate(var(--tilt, 0deg)); }
.pp { position: absolute; left: 48.5%; top: 0; margin-top: -2%; width: min(24%, 130px); aspect-ratio: 236 / 360; z-index: 2; pointer-events: none; transform: translate(-50%, -50%) rotate(var(--tilt, 0deg)); }
.mp img, .pp img { position: absolute; inset: 0; width: 100%; height: 100%; }
.tp { position: absolute; left: calc(50% + var(--shift, 0%)); top: 0; margin-top: 1%; width: 38%; aspect-ratio: 38 / 11; z-index: 2; transform: translate(-50%, -50%) rotate(var(--tilt, 0deg)); }
.tp.navy { background: rgba(47, 74, 109, .59); }
.tp.cream { background: rgba(248, 241, 222, .82); box-shadow: 0 0 0 .5px rgba(43, 38, 32, .12) inset; }
.tp.washi { width: 44%; aspect-ratio: 44 / 12; background-color: rgba(251, 244, 236, .9); background-image: repeating-linear-gradient(90deg, rgba(196, 71, 58, .5) 0 6px, transparent 6px 12px), repeating-linear-gradient(0deg, rgba(196, 71, 58, .5) 0 6px, transparent 6px 12px); clip-path: polygon(0 0, 100% 0, 98.5% 20%, 100% 40%, 98.5% 60%, 100% 80%, 98.5% 100%, 0 100%, 1.5% 80%, 0 60%, 1.5% 40%, 0 20%); }
.hero-shots { display: grid; grid-template-columns: 1fr 1fr; gap: 26px; align-items: start; }
.page { max-width: 760px; margin: 0 auto; }
.page h2 { font-size: 30px; margin: 26px 0 6px; }
.page ul { padding-left: 22px; } .page li { margin: 6px 0; }
.qa h2 { font-size: 30px; margin: 28px 0 4px; }
"""

def head(title, description, path, root):
    """<head> with the site's description cards and icons. `root` is the relative path to the site root ("" or "../")."""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<meta name="theme-color" content="#BF9563">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}/assets/img/feature.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{root}assets/img/icon-512.png">
<link rel="apple-touch-icon" href="{root}assets/img/icon-512.png">
<link rel="stylesheet" href="{root}assets/site.css">
<style>{HOLDER_CSS}</style>
</head>
"""

def topbar(root, dark=False):
    return f"""<div class="wrap top"><a class="wordmark" href="{root or './'}"><img src="{root}assets/img/icon-512.png" alt="">Scrap</a><nav><a href="{root or './'}#foldables">Foldables</a><a href="{root or './'}#key-photo">Key Photo</a><a href="{root}privacy/">Privacy</a><a href="{root}support/">Support</a></nav></div>"""

def footer(root):
    return f"""<footer class="footer">
  <div class="wrap">
    <div class="hand">Scrap</div>
    <a href="{root}privacy/">Privacy policy</a><a href="{root}support/">Support</a><a href="mailto:{EMAIL}">{EMAIL}</a>
    <p style="margin-top:14px">Made by Brayan Castaneda. Google Play is a trademark of Google LLC.</p>
  </div>
</footer>"""

def mappin(colour, tilt): return f'<span class="mp" style="--tilt:{tilt}deg"><img src="assets/img/pins/{colour}.shadow.png" alt=""><img src="assets/img/pins/{colour}.png" alt=""></span>'
def pushpin(colour, tilt): return f'<span class="pp" style="--tilt:{tilt}deg"><img src="assets/img/pushpins/{colour}.shadow.png" alt=""><img src="assets/img/pushpins/{colour}.png" alt=""></span>'
def tape(kind, tilt, shift=0): return f'<span class="tp {kind}" style="--tilt:{tilt}deg;--shift:{shift}%"></span>'
CORNERS = '<span class="c c1"></span><span class="c c2"></span><span class="c c3"></span><span class="c c4"></span>'

# ---- home ------------------------------------------------------------------------------------------------------
def home():
    body = f"""<body class="home">
<div class="corkbg" style="padding:0 0 46px">
  {topbar("")}
  <div class="wrap grid2" style="align-items:center;padding-top:16px">
    <div class="polaroid tilt-l" style="padding:18px 22px 24px">{mappin('red', -1.5)}
      <h1 style="font-size:clamp(40px,5.6vw,60px)">Your photos, as a scrapbook on your home screen.</h1>
      <p style="font-size:19px;margin:14px 0 18px">Polaroids, tape and pins on paper. On a foldable, it opens like a book. Private by design: your photos stay on your phone.</p>
      <a class="btn" href="#coming-soon">Coming soon on Google Play</a>
    </div>
    <div class="hero-shots">
      <div class="polaroid tilt-r">{pushpin('blue', 1.2)}<img src="assets/img/shot-1.jpg" alt="Close it: the cover. Open it: the book." width="675" height="1200"><div class="cap">Close it, open it</div></div>
      <div class="polaroid tilt-l" style="margin-top:40px">{pushpin('yellow', -1.8)}<img src="assets/img/shot-2.jpg" alt="The home screen with the Key Photo" width="675" height="1200"><div class="cap">Your home screen</div></div>
    </div>
  </div>
</div>
<section class="section" id="foldables">
  <div class="wrap grid2">
    <div class="feature">
      <h2>Made for foldables</h2>
      <p>Closed, your phone shows the cover of your book. Open it, and the book opens: the rest of your photos are inside. Three ways to open: Book, Side by side, Centerpiece.</p>
      <p class="muted">Regular phones get the cover on the lock screen and a page from inside on the home screen.</p>
    </div>
    <div class="polaroid tilt-r">{tape("navy", -4, 3)}<img src="assets/img/feature.jpg" alt="A closed and an open foldable phone showing the same scrapbook" width="1024" height="500"><div class="cap">Closed, the cover. Open, the book.</div></div>
  </div>
</section>
<section class="section" id="key-photo">
  <div class="wrap grid2">
    <div class="polaroid corners tilt-l" style="max-width:380px">{CORNERS}<img src="assets/img/shot-4.jpg" alt="Scrap's camera" width="675" height="1200"><div class="cap">Snap, and it's in your book</div></div>
    <div class="feature">
      <h2>The Key Photo</h2>
      <p>Double-tap the Key Photo on your home screen to open Scrap's camera. Your new photo lands in the book with a <span class="stamp">TAKEN LIVE · OCT 15</span> stamp, and the full-size photo is saved to your phone's gallery too.</p>
      <p class="muted">A Key Photo widget does the same with one tap.</p>
    </div>
  </div>
</section>
<section class="section" id="studio">
  <div class="wrap">
    <h2 style="text-align:center">Make it yours in the studio</h2>
    <p class="muted" style="text-align:center;max-width:640px;margin:10px auto 36px">Arrange Polaroids on cork, kraft, lined or plain paper. Tape, pins, photo corners, captions and date stamps. Drag, tilt, resize and layer everything.</p>
    <div class="grid3">
      <div class="polaroid tilt-l">{tape("cream", 3, -4)}<img src="assets/img/shot-3.jpg" alt="The studio" width="675" height="1200"><div class="cap">The studio</div></div>
      <div class="polaroid tilt-s">{tape("washi", -5, 2)}<img src="assets/img/shot-7.jpg" alt="Packs: magnets, pins and more" width="675" height="1200"><div class="cap">Packs</div></div>
      <div class="polaroid tilt-r">{mappin("white", 1.4)}<img src="assets/img/shot-8.jpg" alt="The closet investigation look" width="675" height="1200"><div class="cap">Closet investigation</div></div>
    </div>
  </div>
</section>
<section class="section" id="coming-soon">
  <div class="wrap grid2">
    <div class="card">
      <h3>Free</h3>
      <p>One book with unlimited photos, the starter looks, frames and tape, the camera and Key Photo, captions, stamps, and the foldable design.</p>
      <h3>Scrap Plus</h3>
      <p>One-time purchase, not a subscription: more than one book, extra stamp looks, and two packs of your choice.</p>
      <h3>Packs</h3>
      <p class="muted" style="margin:0">Pin board · Fridge door · Journal · Closet investigation · Christmas magnets. Anything you buy works with every look.</p>
    </div>
    <div class="card">
      <h3>Private by design</h3>
      <p>Scrap keeps your photos on your phone. It has no server, no account, no ads and no tracking, and it removes the hidden location from every photo it saves. Your photos stay yours.</p>
      <p class="muted">Back your book up any time with "Save a copy". On a new phone, Find my photos puts each photo back in its place.</p>
      <p class="muted" style="margin:0">Scrap is coming to Google Play for Android. <a href="support/">Questions?</a></p>
    </div>
  </div>
</section>
{footer("")}
</body></html>
"""
    return head("Scrap: Scrapbook Wallpaper", "Your photos as a scrapbook wallpaper. On a foldable, it opens like a book. Private by design: no account, no ads, no tracking.", "/", "") + body

# ---- privacy policy: the app's own text -----------------------------------------------------------------------
def privacy():
    text = APP_POLICY.read_text()
    blocks = []
    for n, group in enumerate(re.split(r"\n\s*\n", text.strip())):
        lines = [l.strip() for l in group.splitlines() if l.strip()]
        for i, line in enumerate(lines):
            if n == 0 and i == 0: blocks.append(("title", line))
            elif line.startswith("Last updated"): blocks.append(("date", line))
            elif line.startswith("• "): blocks.append(("bullet", line[2:]))
            elif i == 0 and len(lines) > 1 and not line.endswith("."): blocks.append(("heading", line))
            else: blocks.append(("text", line))
    out, in_list = [], False
    def close():
        nonlocal in_list
        if in_list: out.append("</ul>"); in_list = False
    for kind, line in blocks:
        esc = html.escape(line).replace(EMAIL, f'<a href="mailto:{EMAIL}">{EMAIL}</a>')
        if kind == "bullet":
            if not in_list: out.append("<ul>"); in_list = True
            out.append(f"<li>{esc}</li>"); continue
        close()
        if kind == "title": out.append(f"<h1>{esc}</h1>")
        elif kind == "date": out.append(f'<p class="muted typed" style="font-size:14px">{esc}</p>')
        elif kind == "heading": out.append(f"<h2>{esc}</h2>")
        else: out.append(f"<p>{esc}</p>")
    close()
    body = f"""<body>
<div class="corkbg">{topbar("../")}</div>
<main class="wrap section"><article class="card page">{''.join(out)}</article></main>
{footer("../")}
</body></html>
"""
    return head("Privacy policy · Scrap", "Scrap's privacy policy: no account, no ads, no tracking. Your photos stay on your phone.", "/privacy/", "../") + body

# ---- support ---------------------------------------------------------------------------------------------------
def support():
    body = f"""<body>
<div class="corkbg">{topbar("../")}</div>
<main class="wrap section"><article class="card page qa">
<h1>Support</h1>
<p style="font-size:19px">Questions, ideas or something not working? Write to <a href="mailto:{EMAIL}?subject=Scrap%20feedback">{EMAIL}</a>. A person reads every message.</p>
<p class="muted">The quickest way from the app: Settings → Send feedback. It fills in your phone's model and Android version for you, which helps a lot with problems.</p>
<h2>Where are my photos kept?</h2>
<p>On your phone, in Scrap's own private storage. Scrap has no server and no account, so nothing is uploaded anywhere. Photos taken with Scrap's camera are also saved to your phone's gallery, in an album called Scrap.</p>
<h2>How do I move my book to a new phone?</h2>
<p>In Scrap's Settings, tap "Save a copy of your book" and keep the file somewhere safe, like Google Drive. On the new phone, open Scrap and choose "Open a book file". If your phone's own backup brought your book back without its pictures, tap "Find my photos" and pick them again: each one goes back in its place.</p>
<h2>Purchases and refunds</h2>
<p>Scrap Plus and the packs are bought through Google Play, which also handles refunds. Your purchases come back by themselves on a new phone with the same Google account; if they don't, use "Restore" in Scrap's Settings.</p>
<h2>Privacy</h2>
<p>The short version: no account, no ads, no tracking, and your photos stay on your phone. The full <a href="../privacy/">privacy policy</a> is here too.</p>
</article></main>
{footer("../")}
</body></html>
"""
    return head("Support · Scrap", "Help with Scrap, the scrapbook wallpaper app: contact, moving to a new phone, purchases.", "/support/", "../") + body

def not_found():
    body = f"""<body>
<div class="corkbg">{topbar("")}</div>
<main class="wrap section"><article class="card page" style="text-align:center">
<h1>That page isn't in the book.</h1>
<p class="muted">The address may have a typo, or the page moved.</p>
<p><a class="btn" href="./">Back to the start</a></p>
</article></main>
{footer("")}
</body></html>
"""
    return head("Not found · Scrap", "Page not found.", "/404.html", "") + body

if __name__ == "__main__":
    (HERE / "index.html").write_text(home())
    (HERE / "privacy").mkdir(exist_ok=True); (HERE / "privacy/index.html").write_text(privacy())
    (HERE / "support").mkdir(exist_ok=True); (HERE / "support/index.html").write_text(support())
    (HERE / "404.html").write_text(not_found())
    (HERE / "CNAME").write_text("scrapwallpaper.com")  # as GitHub writes it (no line break), so a rebuild leaves it unchanged
    (HERE / ".nojekyll").write_text("")
    (HERE / ".gitignore").write_text("mockups/\n.DS_Store\n")
    print("built: index.html, privacy/index.html, support/index.html, 404.html, CNAME")
