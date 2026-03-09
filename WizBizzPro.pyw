# ══════════════════════════════════════════════════════════════════════════════
#  WIZBIZZ PRO — STREAMER HUB
#  Main application file — v1.0
# ══════════════════════════════════════════════════════════════════════════════

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import font as tkfont
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageFilter, ImageChops
import os, shutil, json, webbrowser, sys, importlib.util, math, random, ctypes
import logging

# ── PATHS ────────────────────────────────────────────────────────────────────

BASE_PATH    = os.path.dirname(os.path.abspath(sys.argv[0]))
WIDGETS_PATH = os.path.join(BASE_PATH, "widgets")
ICONS_PATH   = os.path.join(BASE_PATH, "icons")
SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(BASE_PATH, "user_settings.json")
LOG_FILE      = os.path.join(BASE_PATH, "wizbizz.log")
os.chdir(BASE_PATH)
if not os.path.exists(WIDGETS_PATH):
    os.makedirs(WIDGETS_PATH)
if not os.path.exists(ICONS_PATH):
    os.makedirs(ICONS_PATH)

# ── LOGGING ──────────────────────────────────────────────────────────────────

logging.basicConfig(
    filename=LOG_FILE, level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S")
log = logging.getLogger("WizHub")

# ── COLOUR PALETTE ───────────────────────────────────────────────────────────

C_BLACK   = "#000000"
C_PANEL   = "#111111"
C_BORDER  = "#222222"
C_DETAIL  = "#444444"
C_HINT    = "#888888"
C_EDIT    = "#FF4444"
C_RUNNING = "#CC0000"

# ── THEME DEFINITIONS ────────────────────────────────────────────────────────

THEMES = {
    "CYBER":    {"on": "#00FFCC", "off": "#FF0000"},
    "NEON":     {"on": "#FF00FF", "off": "#8A2BE2"},
    "GOLD":     {"on": "#FFD700", "off": "#000000"},
    "TOXIC":    {"on": "#ADFF2F", "off": "#006400"},
    "BLOOD":    {"on": "#FF1744", "off": "#7F0000"},
    "ARCTIC":   {"on": "#87CEEB", "off": "#1a3a4a"},
    "COBALT":   {"on": "#0047AB", "off": "#001433"},
    "EMBER":    {"on": "#FF6B35", "off": "#7A2800"},
    "ROSEGOLD": {"on": "#FFB6C1", "off": "#8B3A47"},
    "CHROME":   {"on": "#C0C0C0", "off": C_DETAIL},
}

# ── BRAND LIBRARY ────────────────────────────────────────────────────────────

BRAND_LIBRARY = {
    "tiktok": {
        "name": "TikTok",
        "color": "#FF0050",
        "url_base": "",
        "icon": "tiktok.png"
    },
    "youtube": {
        "name": "YouTube", 
        "color": "#FF0000",
        "url_base": "",
        "icon": "youtube.png"
    },
    "instagram": {
        "name": "Instagram",
        "color": "#E1306C", 
        "url_base": "",
        "icon": "instagram.png"
    },
    "twitch": {
        "name": "Twitch",
        "color": "#9146FF",
        "url_base": "",
        "icon": "twitch.png"
    },
    "facebook": {
        "name": "Facebook",
        "color": "#1877F2",
        "url_base": "",
        "icon": "facebook.png"
    },
    "kick": {
        "name": "Kick",
        "color": "#53FC18",
        "url_base": "",
        "icon": "kick.png"
    },
    "discord": {
        "name": "Discord",
        "color": "#5865F2",
        "url_base": "",
        "icon": "discord.png"
    },
    "mail": {
        "name": "Mail",
        "color": "#00B4D8",
        "url_base": "",
        "icon": "Mail.png"
    }
}

# Maximum number of integration slots
MAX_INTEGRATIONS = 12

# ── LAYOUT CONSTANTS ─────────────────────────────────────────────────────────

SIDEBAR_WIDTH     = 280
WIDGET_SLOT_COUNT = 12
LAUNCH_SLOT_COUNT = 10
SFX_COLS, SFX_ROWS = 8, 4
SFX_COUNT         = SFX_COLS * SFX_ROWS
MIN_WINDOW_W      = 1420
MIN_WINDOW_H      = 1010
DEFAULT_WINDOW    = "1600x950"
RADAR_RGB         = (0, 255, 204)
RADAR_HEX         = "#00FFCC"

FOOTER_LINKS = [
    ("tiktok",    "WizBizz Pro", "https://www.tiktok.com/@wizbizzpro"),
    ("youtube",   "WizBizz Pro", "https://www.youtube.com/@wizbizzpro"),
    ("discord",   "Community",   "https://discord.gg/wizbizz"),
    ("instagram", "WizBizz Pro", "DISABLED"),
    ("Mail",      "Support",     "copy_email"),
]

# ══════════════════════════════════════════════════════════════════════════════
#  STANDALONE HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def hex_to_rgb(h):
    h = h.lstrip("#")
    return (int(h[0:2],16), int(h[2:4],16), int(h[4:6],16))

def rgb_to_hex(r, g, b):
    return f"#{min(255,max(0,int(r))):02x}{min(255,max(0,int(g))):02x}{min(255,max(0,int(b))):02x}"

def dim_colour(hex_colour, factor):
    h = hex_colour.lstrip("#")
    return f"#{int(int(h[0:2],16)*factor):02x}{int(int(h[2:4],16)*factor):02x}{int(int(h[4:6],16)*factor):02x}"

def bright_colour(hex_colour, white_mix):
    h = hex_colour.lstrip("#")
    r = int(int(h[0:2],16)*(1-white_mix) + 255*white_mix)
    g = int(int(h[2:4],16)*(1-white_mix) + 255*white_mix)
    b = int(int(h[4:6],16)*(1-white_mix) + 255*white_mix)
    return f"#{min(255,r):02x}{min(255,g):02x}{min(255,b):02x}"

def draw_rounded(can, x1, y1, x2, y2, r, **kw):
    p = [x1+r,y1, x1+r,y1, x2-r,y1, x2-r,y1, x2,y1, x2,y1+r, x2,y1+r,
         x2,y2-r, x2,y2-r, x2,y2, x2-r,y2, x2-r,y2, x1+r,y2, x1+r,y2,
         x1,y2, x1,y2-r, x1,y2-r, x1,y1+r, x1,y1+r, x1,y1]
    return can.create_polygon(p, **kw, smooth=True)

def find_pil_font(size):
    candidates = [
        os.path.join(SCRIPT_DIR, "fonts", "BebasNeue-Regular.ttf"),
        os.path.join(SCRIPT_DIR, "fonts", "Rajdhani-Bold.ttf"),
    ]
    win_fonts = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
    for n in ("impact.ttf", "ariblk.ttf", "arial.ttf"):
        candidates.append(os.path.join(win_fonts, n))
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
               "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        candidates.append(p)
    for fp in candidates:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                pass
    return ImageFont.load_default()

def render_glow_text(text, font_size, accent_hex, bg_rgb):
    """Render a neon glow title. Returns (PIL Image, PhotoImage)."""
    acc_rgb = hex_to_rgb(accent_hex)
    scale = 6
    pil_size = font_size * scale
    pil_font = find_pil_font(pil_size)

    # Measure with letter spacing
    tmp = Image.new('RGBA', (1, 1))
    bb = ImageDraw.Draw(tmp).textbbox((0, 0), text, font=pil_font)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    spacing = int(pil_size * 0.08)
    char_widths = [ImageDraw.Draw(tmp).textbbox((0,0), ch, font=pil_font) for ch in text]
    char_widths = [cb[2]-cb[0] for cb in char_widths]
    total_w = sum(char_widths) + spacing * (len(text)-1)

    pad = int(pil_size * 0.7)
    W, H = total_w + pad*2, th + pad*2
    tx, ty = pad, pad - bb[1]

    # Build text mask with letter spacing
    mask = Image.new('L', (W, H), 0)
    draw = ImageDraw.Draw(mask)
    cx = tx
    for ch in text:
        cb = draw.textbbox((0, 0), ch, font=pil_font)
        draw.text((cx-cb[0], ty), ch, font=pil_font, fill=255)
        cx += cb[2]-cb[0] + spacing

    # Glow parameters
    lum = (acc_rgb[0]*0.299 + acc_rgb[1]*0.587 + acc_rgb[2]*0.114) / 255.0
    boost = max(1.0, 1.8 - lum)
    glow_rgb = tuple(min(255, int(c*boost)) for c in acc_rgb)
    base_pil = 288
    r_scale = pil_size / base_pil
    size_damp = min(1.0, (288 / max(1, pil_size)) ** 1.3)

    final = Image.new('RGBA', (W, H), (*bg_rgb, 255))

    # Tight glow
    tr = max(1, int(6*r_scale))
    t = mask.filter(ImageFilter.GaussianBlur(radius=tr))
    t = t.point(lambda p: min(int(80*size_damp), p))
    layer = Image.new('RGBA', (W, H), (*glow_rgb, 255)); layer.putalpha(t)
    final = Image.alpha_composite(final, layer)

    # Wide glow
    wr = max(2, int(25*r_scale))
    w = mask.filter(ImageFilter.GaussianBlur(radius=wr))
    w = w.point(lambda p: min(int(12*size_damp), p))
    layer = Image.new('RGBA', (W, H), (*glow_rgb, 255)); layer.putalpha(w)
    final = Image.alpha_composite(final, layer)

    # Inner halo
    hi_r, ho_r = max(1, int(3*r_scale)), max(2, int(12*r_scale))
    ib = mask.filter(ImageFilter.GaussianBlur(radius=hi_r))
    ob = mask.filter(ImageFilter.GaussianBlur(radius=ho_r))
    hr = ImageChops.subtract(ob, ib)
    hc = int(55*size_damp)
    ha = hr.point(lambda p: min(hc, int(p*1.4*size_damp)))
    bh = tuple(min(255, c+60) for c in glow_rgb)
    layer = Image.new('RGBA', (W, H), (*bh, 255)); layer.putalpha(ha)
    final = Image.alpha_composite(final, layer)

    # Outer halo
    ho2 = max(3, int(22*r_scale))
    ob2 = mask.filter(ImageFilter.GaussianBlur(radius=ho2))
    hr2 = ImageChops.subtract(ob2, ob)
    ha2 = hr2.point(lambda p: min(int(20*size_damp), p))
    layer = Image.new('RGBA', (W, H), (*glow_rgb, 255)); layer.putalpha(ha2)
    final = Image.alpha_composite(final, layer)

    # Gradient letters
    sharp = mask.point(lambda p: 255 if p > 100 else 0)
    bt = tuple(min(255, c+180) for c in acc_rgb)
    mb = tuple(min(255, c+90) for c in acc_rgb)
    grad = Image.new('RGBA', (1, H), (0,0,0,255))
    for y in range(H):
        if ty <= y <= ty+th:
            t2 = (y-ty) / max(1, th)
            if t2 < 0.3:
                f = t2/0.3
                r,g,b = int(bt[0]*(1-f)+mb[0]*f), int(bt[1]*(1-f)+mb[1]*f), int(bt[2]*(1-f)+mb[2]*f)
            else:
                f = (t2-0.3)/0.7
                r,g,b = int(mb[0]*(1-f)+acc_rgb[0]*f), int(mb[1]*(1-f)+acc_rgb[1]*f), int(mb[2]*(1-f)+acc_rgb[2]*f)
        else:
            r,g,b = acc_rgb
        grad.putpixel((0, y), (r, g, b, 255))
    grad = grad.resize((W, H), Image.Resampling.NEAREST)
    grad.putalpha(sharp)
    final = Image.alpha_composite(final, grad)

    out_w, out_h = max(1, W//scale), max(1, H//scale)
    final = final.resize((out_w, out_h), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(final)
    return final, photo

def generate_ecg(total_length):
    """Generate a randomised ECG heartbeat pattern."""
    pattern, x = [], 0
    while x < total_length:
        cl = random.randint(55, 80)
        rh, sd, ph, th = random.uniform(14,26), random.uniform(8,18), random.uniform(1,3), random.uniform(2,5)
        if random.random() < 0.3: sd = random.uniform(16, 24)
        noise = lambda: random.uniform(-0.4, 0.4)
        for i in range(cl):
            if x >= total_length: break
            t = i/cl
            if   t < 0.08: y = noise()
            elif t < 0.15: y = -ph*math.sin((t-0.08)/0.07*math.pi) + noise()*0.2
            elif t < 0.22: y = noise()
            elif t < 0.28:
                pt = (t-0.22)/0.06
                y = sd*0.3*(pt/0.25) if pt < 0.25 else sd*0.3 - rh*((pt-0.25)/0.75)
            elif t < 0.34: y = -rh + (rh+sd)*((t-0.28)/0.06)
            elif t < 0.42: y = sd*(1-((t-0.34)/0.08)**2) + noise()*0.2
            elif t < 0.50: y = noise()
            elif t < 0.62: y = -th*math.sin((t-0.50)/0.12*math.pi) + noise()*0.2
            else:          y = noise()
            pattern.append(y)
            x += 1
    return pattern

def draw_radar(canvas, size, phase):
    """Draw the radar sweep on a canvas. Fixed colours, not theme dependent."""
    c = canvas
    c.delete("all")
    cx = cy = size / 2
    ar, ag, ab = RADAR_RGB
    hx = rgb_to_hex
    pulse = 0.5 + 0.5*math.sin(phase*0.035)

    outer_r, radar_r = 60, 53
    angle_deg = (360 - (phase*1.5) % 360) % 360

    # Ambient bloom
    for br, ba in [(63,0.04),(60,0.06),(56,0.05)]:
        a = ba*(0.7+0.3*pulse)
        c.create_oval(cx-br,cy-br,cx+br,cy+br, outline=hx(ar*a,ag*a,ab*a), width=5)

    # Outer ring
    c.create_oval(cx-outer_r-2,cy-outer_r-2,cx+outer_r+2,cy+outer_r+2,
                  outline=hx(ar*0.15,ag*0.15,ab*0.15), width=4)
    c.create_oval(cx-outer_r,cy-outer_r,cx+outer_r,cy+outer_r, outline=RADAR_HEX, width=2)

    # Disc
    c.create_oval(cx-radar_r,cy-radar_r,cx+radar_r,cy+radar_r,
                  fill=hx(ar*0.015,ag*0.015,ab*0.015), outline=hx(ar*0.1,ag*0.1,ab*0.1), width=1)

    # Grid
    gc, gg = hx(ar*0.07,ag*0.07,ab*0.07), hx(ar*0.03,ag*0.03,ab*0.03)
    for frac in [0.33, 0.66, 1.0]:
        gr = radar_r*frac - 2
        c.create_oval(cx-gr,cy-gr,cx+gr,cy+gr, outline=gg, width=3)
        c.create_oval(cx-gr,cy-gr,cx+gr,cy+gr, outline=gc, width=1)
    for args in [(cx-radar_r+4,cy,cx+radar_r-4,cy),(cx,cy-radar_r+4,cx,cy+radar_r-4)]:
        c.create_line(*args, fill=gg, width=3)
        c.create_line(*args, fill=gc, width=1)

    # Sweep head glow
    angle_rad = math.radians(angle_deg)
    hgx = cx + math.cos(angle_rad)*radar_r*0.45
    hgy = cy - math.sin(angle_rad)*radar_r*0.45
    for gr, ga in [(22,0.04),(14,0.07),(8,0.1)]:
        c.create_oval(hgx-gr,hgy-gr,hgx+gr,hgy+gr, fill=hx(ar*ga,ag*ga,ab*ga), outline="")

    # Sweep beam — 3 layers
    td, ts = 70, 45
    for lw, calc in [(6, lambda t: t**3*0.2), (3, lambda t: t**2*0.35)]:
        for i in range(ts):
            sa = math.radians(angle_deg + i*td/ts)
            t = 1.0 - i/ts
            xe, ye = cx+math.cos(sa)*(radar_r-3), cy-math.sin(sa)*(radar_r-3)
            b = calc(t)
            c.create_line(cx,cy,xe,ye, fill=hx(ar*b,ag*b,ab*b), width=lw)
    for i in range(ts):
        sa = math.radians(angle_deg + i*td/ts)
        t = 1.0-i/ts
        xe, ye = cx+math.cos(sa)*(radar_r-3), cy-math.sin(sa)*(radar_r-3)
        b, wm = t*t, max(0,t-0.5)*2
        c.create_line(cx,cy,xe,ye,
            fill=hx(ar*b+(255-ar)*wm*b*0.5, ag*b+(255-ag)*wm*b*0.5, ab*b+(255-ab)*wm*b*0.5), width=1)

    # Head lines
    for i in range(8):
        sa = math.radians(angle_deg + i*0.6)
        t = 1.0 - i/8
        xe, ye = cx+math.cos(sa)*(radar_r-3), cy-math.sin(sa)*(radar_r-3)
        c.create_line(cx,cy,xe,ye,
            fill=hx(ar*t+(255-ar)*t*0.5, ag*t+(255-ag)*t*0.5, ab*t+(255-ab)*t*0.5), width=2)

    # Tip
    lr = math.radians(angle_deg)
    tipx, tipy = cx+math.cos(lr)*(radar_r-3), cy-math.sin(lr)*(radar_r-3)
    for tr, ta in [(5,0.12),(3,0.25)]:
        tc = hx(ar*ta+255*(1-ta)*0.3, ag*ta+255*(1-ta)*0.3, ab*ta+255*(1-ta)*0.3)
        c.create_oval(tipx-tr,tipy-tr,tipx+tr,tipy+tr, fill=tc, outline="")
    c.create_line(cx,cy,tipx,tipy, fill=hx(min(255,ar+60),min(255,ag+60),min(255,ab+60)), width=2)
    c.create_oval(tipx-2,tipy-2,tipx+2,tipy+2,
        fill=hx(min(255,ar+100),min(255,ag+100),min(255,ab+100)), outline=RADAR_HEX, width=1)

    # LAUNCH text
    tb = 0.6 + 0.4*pulse
    c.create_text(cx, cy, text="LAUNCH", fill=hx(ar*0.15,ag*0.15,ab*0.15), font=("Bahnschrift",18,"bold"))
    c.create_text(cx, cy, text="LAUNCH", fill=hx(ar*tb,ag*tb,ab*tb), font=("Bahnschrift",17,"bold"))

def draw_ecg(canvas, ecg_pattern, phase):
    """Draw the RUNNING ECG bar. Fixed colours, not theme dependent."""
    c = canvas
    c.delete("all")
    w, h = 240, 65
    ar, ag, ab = RADAR_RGB
    hx = rgb_to_hex
    mid_y = h // 2

    c.create_rectangle(2,2,w-2,h-2, fill=C_BLACK, outline=hx(ar*0.08,ag*0.08,ab*0.08), width=2)
    c.create_line(6,mid_y,w-6,mid_y, fill=hx(ar*0.04,ag*0.04,ab*0.04), width=1)

    ecg_len = len(ecg_pattern)
    offset = int(phase*1.5) % ecg_len
    points = [(6+px, mid_y + ecg_pattern[(px+offset)%ecg_len]) for px in range(w-12)]

    if len(points) > 1:
        flat = [v for p in points for v in p]
        c.create_line(*flat, fill=hx(ar*0.06,ag*0.06,ab*0.06), width=3, smooth=True)
        c.create_line(*flat, fill=hx(ar*0.25,ag*0.25,ab*0.25), width=1, smooth=True)

    if len(points) > 2:
        for i in range(1, len(points)-1):
            dy = abs(points[i][1]-points[i-1][1])
            if dy > 2:
                b = min(0.45, 0.25+dy/40)
                c.create_line(points[i-1][0],points[i-1][1], points[i][0],points[i][1],
                              fill=hx(ar*b,ag*b,ab*b), width=1)

    c.create_text(w//2, mid_y, text="R U N N I N G", fill=C_RUNNING, font=("Bahnschrift",24,"bold"))

def setup_scrollbar(scrollbar_canvas, content_canvas):
    """Wire up a custom scrollbar. Used by both sidebars."""
    sb, can = scrollbar_canvas, content_canvas
    def _update(*args):
        sb.delete("all")
        sw, sh = sb.winfo_width(), sb.winfo_height()
        if sh < 2 or sw < 2: return
        lo, hi = float(args[0]), float(args[1])
        y0, y1 = int(lo*sh), int(hi*sh)
        if y1-y0 < 30: y1 = y0+30
        m = 3; x0, x1 = m, sw-m
        sb.create_rectangle(x0,y0,x1,y1, fill=C_BORDER, outline=C_BORDER, width=1, tags="thumb")
        mid = (y0+y1)//2
        for off in [-6, 0, 6]:
            ly = mid+off
            if y0+6 < ly < y1-6:
                sb.create_line(x0+4,ly,x1-4,ly, fill=C_DETAIL, width=1, tags="thumb")
                sb.create_line(x0+4,ly+1,x1-4,ly+1, fill=C_PANEL, width=1, tags="thumb")
    def _press(e):
        sh = sb.winfo_height()
        if not sh: return
        on_thumb = any(sb.coords(it)[1] <= e.y <= sb.coords(it)[3]
                       for it in sb.find_withtag("thumb") if len(sb.coords(it)) >= 4)
        if on_thumb:
            sb._drag_offset = e.y - can.yview()[0]*sh
        else:
            can.yview_moveto(e.y/sh)
            lo, hi = can.yview()
            sb._drag_offset = (hi-lo)*sh/2
    def _drag(e):
        sh = sb.winfo_height()
        if sh: can.yview_moveto((e.y - getattr(sb,'_drag_offset',0))/sh)
    sb.bind("<Button-1>", _press)
    sb.bind("<B1-Motion>", _drag)
    can.configure(yscrollcommand=_update)

def resize_icon_for_integration(source_path, size=32):
    """Resize and center an icon to exact square dimensions."""
    try:
        img = Image.open(source_path).convert("RGBA")
        # Resize maintaining aspect ratio
        img.thumbnail((size, size), Image.Resampling.LANCZOS)
        # Center on transparent square canvas
        canvas = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        offset = ((size - img.width) // 2, (size - img.height) // 2)
        canvas.paste(img, offset, img if img.mode == 'RGBA' else None)
        return canvas
    except Exception as e:
        log.error(f"Icon resize failed: {e}")
        return None


# ══════════════════════════════════════════════════════════════════════════════
#  SETTINGS I/O — with backup protection
# ══════════════════════════════════════════════════════════════════════════════

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            log.error("Settings file corrupted, attempting backup restore")
            bak = SETTINGS_FILE + ".bak"
            if os.path.exists(bak):
                try:
                    with open(bak, "r") as f:
                        return json.load(f)
                except Exception:
                    log.error("Backup also corrupted, using defaults")
        except Exception as e:
            log.error(f"Failed to load settings: {e}")
    return {"startup_apps": [], "launch_slots": [{"path": None, "pos": None}] * LAUNCH_SLOT_COUNT}

def save_settings(data):
    try:
        # Backup current file before overwriting
        if os.path.exists(SETTINGS_FILE):
            shutil.copy2(SETTINGS_FILE, SETTINGS_FILE + ".bak")
        with open(SETTINGS_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        log.error(f"Failed to save settings: {e}")


# ══════════════════════════════════════════════════════════════════════════════
#  WIZ SCREEN SNIFFER
# ══════════════════════════════════════════════════════════════════════════════

class GhostBox(tk.Toplevel):
    _HWND_TOPMOST = -1
    _SWP_FLAGS = 0x0001 | 0x0002 | 0x0010 | 0x0040

    def __init__(self, parent, color="#00FFCC", callback=None):
        super().__init__(parent)
        self.callback, self.color, self.cursor_type = callback, color, "arrow"
        self.overrideredirect(True)
        self.configure(bg=color)
        self.geometry("400x300+200+200")
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.55)
        lbl = tk.Label(self,
            text="⌖ WIZ SCREEN SNIFFER\nDrag to move  •  Corner to resize\n"
                 "Double-Click to Confirm  •  ESC to cancel",
            fg="black", bg=color, font=("Bahnschrift", 12))
        lbl.pack(expand=True, fill="both")
        lbl.bind("<Button-1>", self._start_move)
        lbl.bind("<B1-Motion>", self._do_move)
        lbl.bind("<Double-Button-1>", self._finish)
        self.bind("<Motion>", self._check_edge)
        self.bind("<Escape>", lambda e: self.destroy())
        self.after(50, self._force_topmost)

    def _force_topmost(self):
        try:
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id()) or self.winfo_id()
            ctypes.windll.user32.SetWindowPos(hwnd, self._HWND_TOPMOST, 0, 0, 0, 0, self._SWP_FLAGS)
        except Exception: pass
        try: self.after(200, self._force_topmost)
        except Exception: pass

    def _start_move(self, e): self.m_x, self.m_y = e.x, e.y
    def _do_move(self, e):
        if self.cursor_type == "arrow":
            self.geometry(f"+{self.winfo_x()+(e.x-self.m_x)}+{self.winfo_y()+(e.y-self.m_y)}")
        else:
            self.geometry(f"{max(100,e.x_root-self.winfo_x())}x{max(100,e.y_root-self.winfo_y())}")
    def _check_edge(self, e):
        resize = e.x > self.winfo_width()-25 and e.y > self.winfo_height()-25
        self.config(cursor="size_nw_se" if resize else "arrow")
        self.cursor_type = "resize" if resize else "arrow"
    def _finish(self, e):
        x, y, w, h = self.winfo_x(), self.winfo_y(), self.winfo_width(), self.winfo_height()
        if self.callback:
            self.destroy(); self.callback(x, y, w, h)
        else:
            d = f"POS: {x}, {y} | SIZE: {w}x{h}"
            self.clipboard_clear(); self.clipboard_append(d)
            messagebox.showinfo("Wiz Sniffer", f"COORDINATES COPIED:\n{d}")
            self.destroy()


# ══════════════════════════════════════════════════════════════════════════════
#  TEMPLATE PICKER DIALOG  
# ══════════════════════════════════════════════════════════════════════════════

class TemplatePicker(tk.Toplevel):
    """Choose from brand library templates."""
    
    def __init__(self, parent, accent_color, on_select):
        super().__init__(parent)
        self.accent = accent_color
        self.on_select = on_select
        
        self.title("Choose Template")
        self.geometry("480x640")
        self.configure(bg=C_BLACK)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Title
        tk.Label(self, text="CHOOSE FROM LIBRARY", fg=accent_color, bg=C_BLACK,
                 font=("Bahnschrift", 16, "bold")).pack(pady=(15, 5))
        
        tk.Label(self, text="Select a platform or create custom",
                 fg=C_HINT, bg=C_BLACK, font=("Segoe UI", 9)).pack(pady=(0, 15))
        
        # Template grid (3x3 = 9 boxes: 8 templates + 1 custom)
        grid_frame = tk.Frame(self, bg=C_BLACK)
        grid_frame.pack(padx=20, pady=(0, 15))
        
        row, col = 0, 0
        for template_id, template in BRAND_LIBRARY.items():
            self._create_template_btn(grid_frame, template_id, template, row, col)
            col += 1
            if col >= 3:
                col = 0
                row += 1
        
        # Add CREATE CUSTOM button as 9th grid item
        self._create_custom_btn(grid_frame, row, col)
        
        # CANCEL button only
        btn_frame = tk.Frame(self, bg=C_BLACK)
        btn_frame.pack(pady=(10, 20))
        
        tk.Button(btn_frame, text="CANCEL", bg=C_PANEL, fg=C_HINT,
                  font=("Bahnschrift", 11), bd=0, cursor="hand2", padx=20, pady=8,
                  command=self.destroy).pack()
        
        # Center on parent window (not screen)
        self.update_idletasks()
        parent.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
        
        # Ensure it stays on screen
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        if x + self.winfo_width() > screen_w:
            x = screen_w - self.winfo_width() - 20
        if y + self.winfo_height() > screen_h:
            y = screen_h - self.winfo_height() - 40
        if x < 0: x = 20
        if y < 0: y = 20
        
        self.geometry(f"+{x}+{y}")
    
    def _create_template_btn(self, parent, template_id, template, row, col):
        """Create template button."""
        frame = tk.Frame(parent, bg=C_PANEL, highlightbackground=template["color"],
                         highlightthickness=2, cursor="hand2", width=130, height=110)
        frame.grid(row=row, column=col, padx=5, pady=5)
        frame.pack_propagate(False)
        
        # Try to load real icon, fallback to letter
        icon_loaded = False
        if template.get("icon"):
            try:
                # Look for icon in main folder (where your existing icons are)
                icon_path = template["icon"]
                if os.path.exists(icon_path):
                    img = Image.open(icon_path).resize((32, 32), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    if not hasattr(self, 'template_icons'):
                        self.template_icons = []
                    self.template_icons.append(photo)
                    icon_lbl = tk.Label(frame, image=photo, bg=C_PANEL)
                    icon_lbl.pack(pady=(15, 5))
                    icon_loaded = True
            except Exception as e:
                log.warning(f"Could not load icon {template.get('icon')}: {e}")
        
        if not icon_loaded:
            # Fallback to letter
            letter = template["name"][0]
            icon_lbl = tk.Label(frame, text=letter, fg=template["color"], bg=C_PANEL,
                                font=("Bahnschrift", 24, "bold"))
            icon_lbl.pack(pady=(15, 5))
        
        # Name
        name_lbl = tk.Label(frame, text=template["name"], fg=template["color"],
                            bg=C_PANEL, font=("Segoe UI", 10, "bold"))
        name_lbl.pack(pady=(0, 10))
        
        # Bind click
        for w in (frame, icon_lbl, name_lbl):
            w.bind("<Button-1>", lambda e, tid=template_id: self._select(tid))
    
    def _create_custom_btn(self, parent, row, col):
        """Create the CREATE CUSTOM button styled like template buttons."""
        frame = tk.Frame(parent, bg=C_PANEL, highlightbackground=self.accent,
                         highlightthickness=2, cursor="hand2", width=130, height=110)
        frame.grid(row=row, column=col, padx=5, pady=5)
        frame.pack_propagate(False)
        
        # Plus icon
        plus_lbl = tk.Label(frame, text="+", fg=self.accent, bg=C_PANEL,
                            font=("Bahnschrift", 32, "bold"))
        plus_lbl.pack(pady=(10, 0))
        
        # Text
        text_lbl = tk.Label(frame, text="CREATE\nCUSTOM", fg=self.accent,
                            bg=C_PANEL, font=("Segoe UI", 9, "bold"))
        text_lbl.pack(pady=(0, 10))
        
        # Bind click
        for w in (frame, plus_lbl, text_lbl):
            w.bind("<Button-1>", lambda e: self._select(None))
    
    def _select(self, template_id):
        """Template selected."""
        if self.on_select:
            self.on_select(template_id)
        self.destroy()


# ══════════════════════════════════════════════════════════════════════════════
#  INTEGRATION EDITOR DIALOG
# ══════════════════════════════════════════════════════════════════════════════

class IntegrationEditor(tk.Toplevel):
    """Popup dialog for editing integration slots."""
    
    def __init__(self, parent, accent_color, template_id=None, existing_data=None, on_save=None, on_delete=None):
        super().__init__(parent)
        self.accent = accent_color
        self.on_save = on_save
        self.on_delete = on_delete
        self.icon_path = None
        self.icon_photo = None
        
        # Load template or existing data
        if template_id and template_id in BRAND_LIBRARY:
            template = BRAND_LIBRARY[template_id]
            self.display_name_val = template["name"]
            self.url_val = template["url_base"]
            self.color_val = template["color"]
            self.icon_val = template.get("icon", "")
        elif existing_data:
            self.display_name_val = existing_data.get("display_name", "")
            self.url_val = existing_data.get("url", "")
            self.color_val = existing_data.get("color", accent_color)
            self.icon_val = existing_data.get("icon", "")
        else:
            self.display_name_val = ""
            self.url_val = ""
            self.color_val = accent_color
            self.icon_val = ""
        
        # Window setup
        self.title("Edit Integration")
        self.geometry("450x380")
        self.configure(bg=C_BLACK)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Title
        tk.Label(self, text="EDIT INTEGRATION", fg=accent_color, bg=C_BLACK,
                 font=("Bahnschrift", 16, "bold")).pack(pady=(15, 20))
        
        # Icon section
        icon_frame = tk.Frame(self, bg=C_BLACK)
        icon_frame.pack(pady=(0, 15))
        
        self.icon_preview = tk.Label(icon_frame, text="?", fg=accent_color, bg=C_PANEL,
                                      width=4, height=2, font=("Bahnschrift", 18, "bold"),
                                      relief="solid", bd=1)
        self.icon_preview.pack(side="left", padx=(0, 10))
        
        tk.Button(icon_frame, text="Browse Icon...", bg=C_BORDER, fg=accent_color,
                  font=("Segoe UI", 10), bd=0, cursor="hand2", padx=15, pady=5,
                  command=self._browse_icon).pack(side="left")
        
        # Display Name
        tk.Label(self, text="Display Name:", fg=C_HINT, bg=C_BLACK,
                 font=("Segoe UI", 9)).pack(anchor="w", padx=40, pady=(0, 3))
        self.name_entry = tk.Entry(self, bg=C_PANEL, fg=accent_color, insertbackground=accent_color,
                                    font=("Segoe UI", 11), bd=0, relief="flat")
        self.name_entry.pack(fill="x", padx=40, ipady=6)
        self.name_entry.insert(0, self.display_name_val)
        
        # URL/Path
        tk.Label(self, text="URL or App Path:", fg=C_HINT, bg=C_BLACK,
                 font=("Segoe UI", 9)).pack(anchor="w", padx=40, pady=(15, 3))
        self.url_entry = tk.Entry(self, bg=C_PANEL, fg="#e8e0d0", insertbackground=accent_color,
                                   font=("Segoe UI", 10), bd=0, relief="flat")
        self.url_entry.pack(fill="x", padx=40, ipady=6)
        self.url_entry.insert(0, self.url_val)
        
        # Buttons
        btn_frame = tk.Frame(self, bg=C_BLACK)
        btn_frame.pack(side="bottom", pady=20)
        
        if existing_data and on_delete:
            tk.Button(btn_frame, text="DELETE", bg=C_PANEL, fg=C_EDIT,
                      font=("Bahnschrift", 11, "bold"), bd=0, cursor="hand2",
                      padx=20, pady=8, command=self._delete).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="CANCEL", bg=C_PANEL, fg=C_HINT,
                  font=("Bahnschrift", 11), bd=0, cursor="hand2",
                  padx=20, pady=8, command=self.destroy).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="SAVE", bg=accent_color, fg=C_BLACK,
                  font=("Bahnschrift", 11, "bold"), bd=0, cursor="hand2",
                  padx=25, pady=8, command=self._save).pack(side="left", padx=5)
        
        # Load existing icon if present
        if self.icon_val:
            self._load_existing_icon()
        
        # Center on parent
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
    
    def _browse_icon(self):
        path = filedialog.askopenfilename(title="Select Icon",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")])
        if path:
            self.icon_path = path
            self._update_icon_preview(path)
    
    def _update_icon_preview(self, path):
        try:
            img = resize_icon_for_integration(path, 32)
            if img:
                self.icon_photo = ImageTk.PhotoImage(img)
                self.icon_preview.config(image=self.icon_photo, text="", bg=C_BLACK)
        except Exception as e:
            log.error(f"Icon preview failed: {e}")
    
    def _load_existing_icon(self):
        # Try ICONS_PATH first (for saved icons)
        icon_full_path = os.path.join(ICONS_PATH, self.icon_val)
        if os.path.exists(icon_full_path):
            self._update_icon_preview(icon_full_path)
        # Try current directory (for template icons like tiktok.png)
        elif os.path.exists(self.icon_val):
            self._update_icon_preview(self.icon_val)
        else:
            # Fallback to letter with color
            letter = self.display_name_val[0] if self.display_name_val else "?"
            self.icon_preview.config(text=letter, fg=self.color_val, bg=C_PANEL, image="")
    
    def _save(self):
        name = self.name_entry.get().strip()
        url = self.url_entry.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Display name is required", parent=self)
            return
        
        # URL is optional - show warning but allow save
        if not url:
            if not messagebox.askyesno("Confirm", 
                "No URL or path entered. You can add this later using the edit button.\n\nContinue?", 
                parent=self):
                return
            url = ""  # Set empty string if user confirms
        
        # Save icon
        icon_filename = self.icon_val
        
        # If user browsed for a new icon, save it
        if self.icon_path:
            try:
                ext = os.path.splitext(self.icon_path)[1]
                safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()
                safe_name = safe_name.replace(' ', '_').lower()
                icon_filename = f"{safe_name}{ext}"
                
                img = resize_icon_for_integration(self.icon_path, 32)
                if img:
                    img.save(os.path.join(ICONS_PATH, icon_filename))
                else:
                    messagebox.showerror("Error", "Failed to process icon", parent=self)
                    return
            except Exception as e:
                log.error(f"Icon save failed: {e}")
                messagebox.showerror("Error", f"Failed to save icon: {e}", parent=self)
                return
        
        # If using template icon (not browsed), copy it to ICONS_PATH
        elif self.icon_val and not os.path.exists(os.path.join(ICONS_PATH, self.icon_val)):
            try:
                # Template icon exists in current directory, copy to ICONS_PATH
                if os.path.exists(self.icon_val):
                    img = resize_icon_for_integration(self.icon_val, 32)
                    if img:
                        img.save(os.path.join(ICONS_PATH, self.icon_val))
                        icon_filename = self.icon_val
            except Exception as e:
                log.warning(f"Could not copy template icon: {e}")
                # Not critical - will fall back to letter icon
        
        data = {
            "display_name": name,
            "url": url,
            "icon": icon_filename,
            "color": self.color_val,
            "type": "application" if url.endswith(('.exe', '.lnk', '.bat', '.cmd')) else "website"
        }
        
        if self.on_save:
            self.on_save(data)
        self.destroy()
    
    def _delete(self):
        if messagebox.askyesno("Confirm Delete", "Delete this integration?", parent=self):
            if self.on_delete:
                self.on_delete()
            self.destroy()


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN APPLICATION
# ══════════════════════════════════════════════════════════════════════════════

class WizHubPro:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WIZBIZZ PRO - STREAMER HUB")
        self._load_custom_fonts()
        self.root.geometry(DEFAULT_WINDOW)
        self.root.configure(bg=C_BLACK)
        
        # Set dark title bar (Windows 11/10)
        try:
            import ctypes as ct
            hwnd = ct.windll.user32.GetParent(self.root.winfo_id())
            # DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            ct.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ct.byref(ct.c_int(1)), ct.sizeof(ct.c_int))
        except Exception:
            pass

        self.user_data           = load_settings()
        self.sounds_edit_mode    = False
        self.platforms_edit_mode = False
        self.live_state          = False
        self._settings_open      = False
        self.sidebar_icons       = {}
        self.footer_icons        = []

        if self.user_data.get("size_lock", True):
            self.root.minsize(MIN_WINDOW_W, MIN_WINDOW_H)

        self.active_theme = self.user_data.get("theme", "CYBER")
        self.accent = THEMES[self.active_theme]["on"]

        self._init_launch_slots()
        self._build_layout()

    def _init_launch_slots(self):
        raw = self.user_data.get("launch_slots", [])
        self.launch_slots = []
        for entry in raw:
            if isinstance(entry, str):
                self.launch_slots.append({"path": entry, "pos": None})
            elif isinstance(entry, dict):
                self.launch_slots.append({"path": entry.get("path"), "pos": entry.get("pos")})
            else:
                self.launch_slots.append({"path": None, "pos": None})
        while len(self.launch_slots) < LAUNCH_SLOT_COUNT:
            self.launch_slots.append({"path": None, "pos": None})
        self.launch_slots = self.launch_slots[:LAUNCH_SLOT_COUNT]

    # ┌─────────────────────────────────────────────────────────────────────────
    # │  LAYOUT
    # └─────────────────────────────────────────────────────────────────────────

    def _build_layout(self):
        self._build_footer()
        self._build_left_sidebar()
        self._build_right_sidebar()
        self._build_centre()
        self.refresh_logo()
        self.apply_locks()

    def _build_footer(self):
        self.footer = tk.Frame(self.root, bg=C_BLACK, height=80)
        self.footer.pack(side="bottom", fill="x")
        tk.Frame(self.footer, bg=C_BORDER, height=1).pack(side="top", fill="x")
        self._setup_footer_links()

    def _build_left_sidebar(self):
        self.left_sidebar = tk.Frame(self.root, bg=C_BLACK, width=SIDEBAR_WIDTH)
        self.left_sidebar.pack(side="left", fill="y")
        self.left_sidebar.pack_propagate(False)

        # Header
        self.header_frame = tk.Frame(self.left_sidebar, bg=C_PANEL,
            highlightbackground=C_BORDER, highlightthickness=1)
        self.header_frame.pack(fill="x", padx=10, pady=(10, 5))
        self.side_title = self._make_glow_title(self.header_frame, "Wiz Widgets", 32, C_PANEL, "_side_glow")
        self.side_title.pack(pady=(10, 5))
        self.add_w_btn = tk.Button(self.header_frame, text="+ ADD WIDGET", bg=C_BORDER, fg=self.accent,
            font=("Bahnschrift", 13), bd=0, cursor="hand2", command=self.add_widget_popup)
        self.add_w_btn.pack(pady=(0, 15), fill="x", padx=15)

        self._build_launch_frame()
        self._build_widget_slots()
        self._animate_launch_btn()

    def _build_launch_frame(self):
        self.start_frame = tk.Frame(self.left_sidebar, bg=C_PANEL,
            highlightbackground=C_BORDER, highlightthickness=1)
        self.start_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        self._launch_canvas_size = 130
        self._launch_radar_phase = 0
        self._launch_can = tk.Canvas(self.start_frame, width=130, height=130,
            bg=C_PANEL, highlightthickness=0, cursor="hand2")
        self._launch_can.pack(pady=(10, 2))
        self._launch_can.bind("<Button-1>", lambda e: self.start_everything())
        self._press_lbl = tk.Label(self.start_frame, text="Press Launch to Start",
            fg=C_HINT, bg=C_PANEL, font=("Bahnschrift", 8))
        self._press_lbl.pack(pady=(0, 8))
        self._ecg_pattern = generate_ecg(600)
        self._running_can = tk.Canvas(self.start_frame, width=240, height=65,
            bg=C_PANEL, highlightthickness=0, cursor="hand2")
        self._running_can.bind("<Button-1>", lambda e: self.start_everything())

    def _build_widget_slots(self):
        cont = tk.Frame(self.left_sidebar, bg=C_BLACK)
        cont.pack(fill="both", expand=True, padx=6)
        sb_f = tk.Frame(cont, bg=C_BLACK, width=44)
        sb_f.pack(side="left", fill="y"); sb_f.pack_propagate(False)
        self._widget_sb = tk.Canvas(sb_f, width=36, bg=C_BLACK, highlightthickness=0)
        self._widget_sb.pack(expand=True, fill="y", padx=4)
        self._widget_can = tk.Canvas(cont, bg=C_BLACK, highlightthickness=0, width=204)
        self._widget_can.pack(side="right", fill="both", expand=False)
        self.widget_container = tk.Frame(self._widget_can, bg=C_BLACK, width=204)
        self._wc_win = self._widget_can.create_window((0,0), window=self.widget_container, anchor="nw", width=204)
        self.widget_container.bind("<Configure>",
            lambda e: self._widget_can.configure(scrollregion=self._widget_can.bbox("all")))
        setup_scrollbar(self._widget_sb, self._widget_can)
        def _ws(e): self._widget_can.yview_scroll(int(-1*(e.delta/120)), "units")
        self._widget_can.bind("<MouseWheel>", _ws)
        self.widget_container.bind("<MouseWheel>", _ws)

        self.slots = []
        for i in range(WIDGET_SLOT_COUNT):
            slot = tk.Frame(self.widget_container, bg=C_BLACK, height=65, width=204,
                highlightbackground=C_PANEL, highlightthickness=1)
            slot.pack(fill="x", pady=1); slot.pack_propagate(False)
            lbl = tk.Label(slot, text=f"SLOT {i+1}", fg=C_BORDER, bg=C_BLACK, font=("Segoe UI", 8))
            lbl.pack(expand=True)
            lbl.bind("<MouseWheel>", _ws); slot.bind("<MouseWheel>", _ws)
            self.slots.append(slot)
        self.load_external_widgets()

    def _build_right_sidebar(self):
        self.right_sidebar = tk.Frame(self.root, bg=C_BLACK, width=SIDEBAR_WIDTH)
        self.right_sidebar.pack(side="right", fill="y")
        self.right_sidebar.pack_propagate(False)

        # My Wiz header
        rh = tk.Frame(self.right_sidebar, bg=C_PANEL, highlightbackground=C_BORDER, highlightthickness=1)
        rh.pack(fill="x", padx=10, pady=(10, 5))
        self.right_title = self._make_glow_title(rh, "My Wiz", 32, C_PANEL, "_right_glow")
        self.right_title.pack(pady=(10, 5))

        self._build_brand_box()
        self._build_integrations_box()
        self.setup_socials()
        self._setup_platforms_toggle()

    def _build_brand_box(self):
        bf = tk.Frame(self.right_sidebar, bg=C_PANEL, highlightbackground=C_BORDER, highlightthickness=1)
        bf.pack(fill="x", padx=10, pady=(5, 5))
        self.brand_frame = bf
        self.logo_btn = tk.Button(bf, bg=C_PANEL, width=140, height=140,
            command=self.up_logo, bd=0, relief="flat", cursor="hand2")
        self.logo_btn.pack(pady=(8, 2))
        tk.Label(bf, text="Click logo to change", fg=C_HINT, bg=C_PANEL, font=("Segoe UI", 7)).pack()
        self._name_frame = tk.Frame(bf, bg=C_PANEL)
        self._name_frame.pack(pady=(4, 1))
        name = self.user_data.get("streamer_name", "Your Name")
        self.user_label = tk.Label(self._name_frame, text=name, fg=self.accent, bg=C_PANEL,
            font=("Bahnschrift", 22, "bold"), cursor="hand2")
        self.user_label.pack(side="left")
        tk.Label(self._name_frame, text=" ✎", fg=C_BORDER, bg=C_PANEL,
            font=("Segoe UI", 10), cursor="hand2").pack(side="left")
        tk.Label(bf, text="Click name to edit", fg=C_HINT, bg=C_PANEL, font=("Segoe UI", 7)).pack(pady=(0, 8))
        self.user_label.bind("<Button-1>", lambda e: self._edit_name())
        self._name_frame.bind("<Button-1>", lambda e: self._edit_name())

    def _build_integrations_box(self):
        f = tk.Frame(self.right_sidebar, bg=C_PANEL, highlightbackground=C_BORDER, highlightthickness=1)
        f.pack(fill="x", padx=10, pady=(5, 5))
        self.integrations_title = self._make_glow_title(f, "INTEGRATIONS", 26, C_PANEL, "_int_glow")
        self.integrations_title.pack(anchor="center", pady=(10, 5))
        self._edit_socials_btn = tk.Button(f, text="✎ EDIT", bg=C_BORDER, fg=self.accent,
            font=("Bahnschrift", 13), bd=0, cursor="hand2", command=self.flip_platforms)
        self._edit_socials_btn.pack(pady=(0, 15), fill="x", padx=15)

    def _build_centre(self):
        self.center = tk.Frame(self.root, bg=C_BLACK)
        self.center.pack(side="left", fill="both", expand=True)
        self.main_title = self._make_glow_title(self.center, "STREAMER HUB", 72, C_BLACK, "_main_glow")
        self.main_title.pack(pady=(6, 2))

        try:
            lp = "new Logo.png" if os.path.exists("new Logo.png") else "new Logo.jpg"
            img = Image.open(lp).convert("RGBA")
            data = list(img.getdata()); w, h = img.size
            nb = lambda px: px[0]>20 or px[1]>20 or px[2]>20
            rows = [y for y in range(h) if any(nb(data[y*w+x]) for x in range(w))]
            cols = [x for x in range(w) if any(nb(data[y*w+x]) for y in range(h))]
            if rows and cols:
                p = 10; img = img.crop((max(0,cols[0]-p), max(0,rows[0]-p), min(w,cols[-1]+p), min(h,rows[-1]+p)))
            img = img.resize((380, 180), Image.Resampling.LANCZOS)
            self.hero = ImageTk.PhotoImage(img)
            tk.Label(self.center, image=self.hero, bg=C_BLACK).pack(pady=(0, 0))
        except Exception as e:
            log.warning(f"Hero logo not found: {e}")
            tk.Label(self.center, text="WIZBIZZ PRO", fg=C_PANEL, bg=C_BLACK, font=("Bahnschrift", 38)).pack()

        self._build_soundboard()

    def _build_soundboard(self):
        self.board_frame = tk.Frame(self.center, bg=C_BLACK,
            highlightbackground=C_BORDER, highlightthickness=1)
        self.board_frame.pack(pady=(2, 8), padx=15, expand=True)
        self.board_title = self._make_glow_title(self.board_frame, "BIZZ DECK", 32, C_BLACK, "_deck_glow")
        self.board_title.pack(pady=(6, 6))
        gf = tk.Frame(self.board_frame, bg=C_BLACK)
        gf.pack(padx=8)

        self.btns = {}
        for i in range(1, SFX_COUNT+1):
            bid = f"sfx_{i}"
            r, c = (i-1)//SFX_COLS, (i-1)%SFX_COLS
            can = tk.Canvas(gf, width=88, height=88, bg=C_BLACK, highlightthickness=0)
            can.grid(row=r, column=c, padx=4, pady=4)
            shape = draw_rounded(can, 4, 4, 84, 84, 12, fill=C_PANEL, outline=C_BORDER)
            name = self.user_data.get(f"{bid}_name", f"SOUND {i}")
            txt = can.create_text(44, 44, text=name, fill=self.accent,
                font=("Bahnschrift", 9), justify="center", width=78)
            can.tag_bind(shape, "<Button-1>", lambda e, b=bid: self.process_click(b))
            can.tag_bind(txt, "<Button-1>", lambda e, b=bid: self.process_click(b))
            self.btns[bid] = {"can": can, "shape": shape, "txt": txt}

        self._setup_sounds_toggle()

    # ┌─────────────────────────────────────────────────────────────────────────
    # │  GLOW TITLES
    # └─────────────────────────────────────────────────────────────────────────

    def _load_custom_fonts(self):
        for fn in ("BebasNeue-Regular.ttf", "Rajdhani-Bold.ttf"):
            fp = os.path.join(SCRIPT_DIR, "fonts", fn)
            if os.path.exists(fp):
                try: ctypes.windll.gdi32.AddFontResourceExW(fp, 0x10, 0)
                except Exception: pass
        avail = list(tkfont.families())
        self._header_font = "Bebas Neue" if "Bebas Neue" in avail else "Impact"
        self._sub_font = "Rajdhani" if "Rajdhani" in avail else "Bahnschrift"

    def _make_glow_title(self, parent, text, size, bg, store_as=None):
        _, photo = render_glow_text(text, size, self.accent, hex_to_rgb(bg))
        lbl = tk.Label(parent, image=photo, bg=bg, bd=0, highlightthickness=0)
        lbl.image = photo
        if not hasattr(self, '_glow_canvases'): self._glow_canvases = []
        self._glow_canvases.append({"label": lbl, "text": text, "font_size": size, "bg": bg})
        if store_as: setattr(self, store_as, lbl)
        return lbl

    # ┌─────────────────────────────────────────────────────────────────────────
    # │  AUDIO
    # └─────────────────────────────────────────────────────────────────────────

    def play_win_sound(self, path):
        try:
            p = f'"{os.path.normpath(path)}"'
            mci = ctypes.windll.winmm.mciSendStringW
            mci("close bizz_sound", None, 0, None)
            mci(f"open {p} type mpegvideo alias bizz_sound", None, 0, None)
            mci("play bizz_sound", None, 0, None)
        except Exception as e:
            log.warning(f"Audio playback failed: {e}")

    def get_sound_duration(self, path):
        try:
            p = f'"{os.path.normpath(path)}"'
            mci = ctypes.windll.winmm.mciSendStringW
            mci("close bizz_query", None, 0, None)
            mci(f"open {p} type mpegvideo alias bizz_query", None, 0, None)
            mci("set bizz_query time format milliseconds", None, 0, None)
            buf = ctypes.create_unicode_buffer(64)
            mci("status bizz_query length", buf, 64, None)
            mci("close bizz_query", None, 0, None)
            return int(buf.value)
        except Exception:
            return None

    def play_click(self):
        p = os.path.join(BASE_PATH, "click.wav")
        if os.path.exists(p): self.play_win_sound(p)

    # ┌─────────────────────────────────────────────────────────────────────────
    # │  LAUNCH / RUNNING
    # └─────────────────────────────────────────────────────────────────────────

    def start_everything(self):
        self.play_click()
        self.live_state = not self.live_state
        if self.live_state:
            self._launch_can.pack_forget()
            self._press_lbl.pack_forget()
            self._running_can.pack(pady=(10, 8))
            for slot in self.launch_slots:
                path, pos = slot.get("path"), slot.get("pos")
                if path and os.path.exists(path):
                    try:
                        os.startfile(path)
                        if pos:
                            for d in (2000, 4000, 6000, 8000):
                                self.root.after(d, lambda p=path, po=pos: self._snap_window(p, po))
                    except Exception as e:
                        log.warning(f"Failed to launch {path}: {e}")
        else:
            self._running_can.pack_forget()
            self._launch_can.pack(pady=(10, 2))
            self._press_lbl.pack(pady=(0, 8))

    def _animate_launch_btn(self):
        self._launch_radar_phase += 1
        if self.live_state:
            draw_ecg(self._running_can, self._ecg_pattern, self._launch_radar_phase)
        else:
            draw_radar(self._launch_can, self._launch_canvas_size, self._launch_radar_phase)
        self.root.after(33, self._animate_launch_btn)

    # ┌─────────────────────────────────────────────────────────────────────────
    # │  WINDOW MANAGEMENT (Win32)
    # └─────────────────────────────────────────────────────────────────────────

    def _find_hwnds(self, app_path):
        raw = os.path.basename(app_path).rsplit(".", 1)[0].lower()
        words = [w for w in raw.replace("_"," ").replace("-"," ").split() if len(w)>2]
        found = []
        EP = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
        def cb(hwnd, _):
            if ctypes.windll.user32.IsWindowVisible(hwnd):
                n = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
                if n > 0:
                    buf = ctypes.create_unicode_buffer(n+1)
                    ctypes.windll.user32.GetWindowTextW(hwnd, buf, n+1)
                    if any(w in buf.value.lower() for w in words): found.append(hwnd)
            return True
        ctypes.windll.user32.EnumWindows(EP(cb), 0)
        return found

    def _snap_window(self, app_path, pos_str):
        try:
            parts = [v.strip() for v in pos_str.split(",")]
            x, y, w, h = int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])
            for hwnd in self._find_hwnds(app_path): self._move_win32(hwnd, x, y, w, h)
        except Exception as e:
            log.warning(f"Window snap failed: {e}")

    def _move_win32(self, hwnd, x, y, w, h):
        try:
            u32 = ctypes.windll.user32
            style = u32.GetWindowLongW(hwnd, -16)
            if style & (0x01000000 | 0x20000000):
                u32.SetWindowLongW(hwnd, -16, style & ~0x01000000 & ~0x20000000)
            flags = 0x0004 | 0x0010 | 0x0020
            u32.SetWindowPos(hwnd, 0, x, y, w, h, flags)
            self.root.after(150, lambda: u32.SetWindowPos(hwnd, 0, x, y, w, h, flags))
        except Exception as e:
            log.warning(f"Win32 move failed: {e}")

    # ┌─────────────────────────────────────────────────────────────────────────
    # │  SOUNDBOARD
    # └─────────────────────────────────────────────────────────────────────────

    def process_click(self, bid):
        self.play_click()
        btn = self.btns[bid]
        if self.sounds_edit_mode:
            if bid in self.user_data:
                self.user_data.pop(bid, None)
                self.user_data.pop(f"{bid}_name", None)
                self.save(); self.apply_locks(); return
            p = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
            if p:
                self.user_data[bid] = p
                self.user_data[f"{bid}_name"] = os.path.basename(p).rsplit('.',1)[0].upper()[:18]
                self.save(); self.apply_locks()
            return
        btn["can"].itemconfig(btn["shape"], fill="white")
        path = self.user_data.get(bid)
        if path and os.path.exists(path):
            dur = self.get_sound_duration(path) or 350
            self.root.after(dur, lambda: btn["can"].itemconfig(btn["shape"], fill=C_PANEL))
            self.root.after(100, lambda: self.play_win_sound(path))
        else:
            self.root.after(350, lambda: btn["can"].itemconfig(btn["shape"], fill=C_PANEL))

    # ┌─────────────────────────────────────────────────────────────────────────
    # │  SETTINGS PANEL
    # └─────────────────────────────────────────────────────────────────────────

    def open_settings(self):
        self.play_click()
        if self._settings_open: self._close_settings(); return
        self._settings_open = True
        self.gear.config(fg=self.accent)
        self._settings_panel = tk.Frame(self.center, bg=C_BLACK,
            highlightbackground=self.accent, highlightthickness=1)
        self._settings_panel.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._settings_title_label = tk.Label(self._settings_panel, text="PRO HUB CONFIGURATION",
            fg=self.accent, bg=C_BLACK, font=("Bahnschrift", 20))
        self._settings_title_label.pack(pady=(15, 10))
        cols = tk.Frame(self._settings_panel, bg=C_BLACK)
        cols.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        for i in range(3): cols.columnconfigure(i, weight=1, uniform="col")
        cols.rowconfigure(0, weight=1)
        self._build_settings_col1(cols)
        self._build_settings_col2(cols)
        self._build_settings_col3(cols)

    def _build_settings_col1(self, cols):
        f = tk.LabelFrame(cols, text="  LAUNCH PAD  ", fg=self.accent, bg=C_BLACK,
            font=("Segoe UI", 9), padx=8, pady=8)
        f.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        tk.Label(f, text="BROWSE = pick app  •  SNIPE = set position  •  Right-click = paste",
            fg=C_DETAIL, bg=C_BLACK, font=("Segoe UI", 7)).pack(anchor="w", pady=(0, 6))
        self._launchpad_frame, self._slot_frames = f, []
        for idx in range(LAUNCH_SLOT_COUNT): self._build_slot_row(f, idx)

    def _build_settings_col2(self, cols):
        f = tk.LabelFrame(cols, text="  OPTIONS  ", fg=self.accent, bg=C_BLACK, font=("Segoe UI", 9))
        f.grid(row=0, column=1, sticky="nsew", padx=(0, 6))
        slk = tk.Frame(f, bg=C_BLACK)
        slk.pack(pady=(15, 5), padx=10, fill="x")
        tk.Label(slk, text="WINDOW SIZE LOCK", fg=self.accent, bg=C_BLACK,
            font=("Bahnschrift", 11, "bold")).pack(anchor="w")
        tk.Label(slk, text="Prevents window from shrinking below usable size",
            fg=C_DETAIL, bg=C_BLACK, font=("Segoe UI", 8)).pack(anchor="w", pady=(0, 6))
        self._size_lock_var = tk.BooleanVar(value=self.user_data.get("size_lock", True))
        def _tgl():
            v = self._size_lock_var.get(); self.user_data["size_lock"] = v
            self.root.minsize(MIN_WINDOW_W, MIN_WINDOW_H) if v else self.root.minsize(0, 0)
            self.save()
        tk.Checkbutton(slk, variable=self._size_lock_var, command=_tgl, bg=C_BLACK, fg=self.accent,
            selectcolor=C_PANEL, activebackground=C_BLACK, activeforeground=self.accent,
            font=("Bahnschrift", 10), text="Enable size lock", cursor="hand2").pack(anchor="w")

        sbf = tk.Frame(f, bg=C_BLACK); sbf.place(relx=0.5, rely=0.4, anchor="center")
        sc = tk.Canvas(sbf, width=180, height=54, bg=C_BLACK, highlightthickness=0); sc.pack()
        self._save_changes_canvas = sc  # Store reference for theme updates
        def _ds(h=False):
            sc.delete("all")
            gc = dim_colour(self.accent, 0.3 if h else 0.15)
            for i in range(4, 0, -1): draw_rounded(sc, i, i, 180-i, 54-i, 10, fill=gc, outline="")
            fl = self.accent if h else C_PANEL; fg = C_BLACK if h else self.accent
            draw_rounded(sc, 4, 4, 176, 50, 8, fill=fl, outline=self.accent)
            sc.create_text(90, 27, text="SAVE CHANGES", fill=fg, font=("Bahnschrift", 13, "bold"))
        _ds()
        sc.bind("<Enter>", lambda e: _ds(True)); sc.bind("<Leave>", lambda e: _ds(False))
        sc.bind("<Button-1>", lambda e: [self.play_click(), self._close_settings()])

        inf = tk.Frame(f, bg=C_BLACK); inf.pack(side="bottom", pady=(0, 15))
        tk.Label(inf, text="WIZBIZZ PRO", fg=C_BORDER, bg=C_BLACK, font=("Bahnschrift", 10)).pack()
        tk.Label(inf, text="v1.0  •  Streamer Hub", fg=C_DETAIL, bg=C_BLACK, font=("Segoe UI", 8)).pack()
        tk.Label(inf, text="wizbizzpro.com", fg=C_DETAIL, bg=C_BLACK, font=("Segoe UI", 8)).pack(pady=(2, 0))

    def _build_settings_col3(self, cols):
        f = tk.LabelFrame(cols, text="  INTERFACE THEME  ", fg=self.accent, bg=C_BLACK,
            font=("Segoe UI", 9), padx=8, pady=8)
        f.grid(row=0, column=2, sticky="nsew")
        pv = tk.Canvas(f, height=8, bg=C_BLACK, highlightthickness=0); pv.pack(fill="x", pady=(0, 8))
        def _sp(c):
            pv.delete("all"); w = pv.winfo_width() or 200
            for i in range(30):
                a = max(0, min(1, 1.0-abs((i/30)-0.5)*1.6))
                r,g,b = int(int(c[1:3],16)*a), int(int(c[3:5],16)*a), int(int(c[5:7],16)*a)
                pv.create_rectangle(int(i/30*w), 0, int((i+1)/30*w), 8, fill=f"#{r:02x}{g:02x}{b:02x}", outline="")
        
        self._theme_buttons = []  # Store theme buttons for updates
        for n in THEMES:
            c = THEMES[n]["on"]
            b = tk.Button(f, text=n, command=lambda n=n: self.update_theme(n), bg=C_PANEL, fg=c,
                font=("Bahnschrift", 12), activebackground=C_PANEL, activeforeground=c,
                bd=1, relief="solid", cursor="hand2")
            b.pack(fill="x", pady=3)
            b.bind("<Enter>", lambda e, c=c: _sp(c)); b.bind("<Leave>", lambda e: pv.delete("all"))
            self._theme_buttons.append((b, n))

    def _close_settings(self):
        self.save()
        if hasattr(self, "_settings_panel"):
            try: self._settings_panel.place_forget(); self._settings_panel.destroy()
            except Exception: pass
        self._settings_open = False
        self.gear.config(fg=C_BORDER)

    # ┌─────────────────────────────────────────────────────────────────────────
    # │  LAUNCH SLOT ROWS
    # └─────────────────────────────────────────────────────────────────────────

    def _build_slot_row(self, parent, idx):
        s = self.launch_slots[idx]
        path, pos = s.get("path"), s.get("pos")
        filled = path is not None
        border = self.accent if filled else C_BORDER
        bg = C_PANEL if filled else C_BLACK

        outer = tk.Frame(parent, bg=bg, highlightbackground=border, highlightthickness=1)
        outer.pack(fill="x", pady=3)
        top = tk.Frame(outer, bg=bg); top.pack(fill="x", pady=(7, 2), padx=4)
        tk.Label(top, text=f"{idx+1}", fg=C_DETAIL, bg=bg, font=("Segoe UI", 11), width=2).pack(side="left", padx=(6, 2))
        nl = tk.Label(top, text=os.path.basename(path) if filled else "EMPTY",
            fg=self.accent if filled else C_BORDER, bg=bg, font=("Segoe UI", 9, "bold"), anchor="w")
        nl.pack(side="left", fill="x", expand=True, padx=6)
        bf = tk.Frame(top, bg=bg); bf.pack(side="right", padx=4)
        if filled:
            tk.Button(bf, text="REMOVE", fg=C_EDIT, bg=C_PANEL, font=("Segoe UI", 8, "bold"),
                bd=0, padx=6, cursor="hand2", command=lambda i=idx: self._remove_slot(i)).pack(side="left", padx=(0, 4))
        tk.Button(bf, text="BROWSE", fg=self.accent, bg=C_PANEL, font=("Segoe UI", 8, "bold"),
            bd=0, padx=6, cursor="hand2", command=lambda i=idx: self._browse_slot(i)).pack(side="left")

        pr = tk.Frame(outer, bg=bg); pr.pack(fill="x", padx=8, pady=(2, 7))
        tk.Label(pr, text="⌖ "+(pos or "NO POSITION SET"), fg=self.accent if pos else C_BORDER,
            bg=bg, font=("Segoe UI", 8), anchor="w").pack(side="left", fill="x", expand=True)
        rb = tk.Frame(pr, bg=bg); rb.pack(side="right")
        if pos:
            tk.Button(rb, text="CLEAR", fg=C_EDIT, bg=C_PANEL, font=("Segoe UI", 8, "bold"),
                bd=0, padx=5, cursor="hand2", command=lambda i=idx: self._clear_pos(i)).pack(side="left", padx=(0, 4))
        tk.Button(rb, text="⌖  SNIPE", fg=self.accent, bg=C_BLACK, font=("Bahnschrift", 9),
            bd=1, relief="solid", padx=6, cursor="hand2",
            command=lambda i=idx: self._open_sniffer(i)).pack(side="left")

        for w in (outer, top, nl): w.bind("<Button-3>", lambda e, i=idx: self._paste_slot(i))
        try:
            outer.drop_target_register("DND_Files")
            outer.dnd_bind("<<Drop>>", lambda e, i=idx: self._set_slot_path(i, e.data.strip().strip('"').strip("{}")))
        except Exception: pass
        self._slot_frames.append(outer)

    def _open_sniffer(self, idx):
        def cb(x, y, w, h):
            self.launch_slots[idx]["pos"] = f"{x},{y},{w},{h}"; self.save(); self._refresh_launchpad()
        GhostBox(self.root, color=self.accent, callback=cb)

    def _refresh_launchpad(self):
        for w in self._launchpad_frame.winfo_children()[1:]: w.destroy()
        self._slot_frames = []
        for idx in range(LAUNCH_SLOT_COUNT): self._build_slot_row(self._launchpad_frame, idx)

    def _set_slot_path(self, idx, path):
        path = path.strip().strip('"')
        if path: self.launch_slots[idx]["path"] = path; self.save(); self._refresh_launchpad()

    def _remove_slot(self, idx):
        self.launch_slots[idx] = {"path": None, "pos": None}; self.save(); self._refresh_launchpad()

    def _clear_pos(self, idx):
        self.launch_slots[idx]["pos"] = None; self.save(); self._refresh_launchpad()

    def _browse_slot(self, idx):
        p = filedialog.askopenfilename(title=f"Select App for Slot {idx+1}",
            filetypes=[("Shortcuts & Executables", "*.lnk *.exe *.bat *.cmd *.py"), ("All Files", "*.*")])
        if p: self._set_slot_path(idx, p)

    def _paste_slot(self, idx):
        try:
            t = self.root.clipboard_get().strip()
            if t: self._set_slot_path(idx, t)
        except Exception: pass

    # ┌─────────────────────────────────────────────────────────────────────────
    # │  WIDGETS
    # └─────────────────────────────────────────────────────────────────────────

    def add_widget_popup(self):
        fp = filedialog.askopenfilename(title="Select WizBizz Widget",
            filetypes=[("Wiz Widget", "*.pyw"), ("Python Script", "*.py")])
        if fp:
            try:
                with open(fp, 'r') as f:
                    if f.readline().strip() == "# WIZ-PRO-V1-99X-2026":
                        shutil.copy(fp, os.path.join(WIDGETS_PATH, os.path.basename(fp)))
                        messagebox.showinfo("WizBizz Pro", "Restart Hub to Load Widget!")
                    else:
                        messagebox.showerror("Security Error", "Invalid Signature.")
            except Exception as e:
                log.error(f"Widget install failed: {e}")
                messagebox.showerror("Error", str(e))

    def load_external_widgets(self):
        if not os.path.exists(WIDGETS_PATH): return
        for idx, f in enumerate(f for f in os.listdir(WIDGETS_PATH) if f.endswith((".py", ".pyw"))):
            if idx >= WIDGET_SLOT_COUNT: break
            try:
                spec = importlib.util.spec_from_file_location(f.split('.')[0], os.path.join(WIDGETS_PATH, f))
                mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
                if hasattr(mod, "initialize"): mod.initialize(self.slots[idx], self.accent)
            except Exception as e:
                log.error(f"Widget '{f}' failed to load: {e}")

    # ┌─────────────────────────────────────────────────────────────────────────
    # │  THEME
    # └─────────────────────────────────────────────────────────────────────────

    def update_theme(self, name):
        self.active_theme = name
        self.accent = THEMES[name]["on"]
        
        # Update user label and add widget button
        self.user_label.config(fg=self.accent)
        self.add_w_btn.config(fg=self.accent)
        
        # Update "EDIT" button on integrations
        if hasattr(self, "_edit_socials_btn"):
            self._edit_socials_btn.config(fg=self.accent)
        
        # Update "EDIT DECK" label
        if hasattr(self, "_snd_toggle") and "lbl" in self._snd_toggle:
            self._snd_toggle["lbl"].config(fg=self.accent)
        
        # Update footer links
        if hasattr(self, "_footer_labels"):
            for label in self._footer_labels:
                try:
                    label.config(fg=self.accent)
                except:
                    pass
        
        # Update soundboard buttons
        for btn in self.btns.values(): 
            btn["can"].itemconfig(btn["txt"], fill=self.accent)
        
        # Update glow titles
        if hasattr(self, "_glow_canvases"):
            for g in self._glow_canvases:
                _, photo = render_glow_text(g["text"], g["font_size"], self.accent, hex_to_rgb(g["bg"]))
                g["label"].config(image=photo)
                g["label"].image = photo
        
        # Update settings panel if open - need to refresh launchpad and theme sections
        if self._settings_open and hasattr(self, "_settings_panel"):
            self._settings_panel.config(highlightbackground=self.accent)
            if hasattr(self, "_settings_title_label"):
                self._settings_title_label.config(fg=self.accent)
            
            # Refresh the entire launchpad to update BROWSE/SNIPE/REMOVE buttons
            if hasattr(self, "_launchpad_frame"):
                self._refresh_launchpad()
            
            # Update SAVE CHANGES button in settings
            if hasattr(self, "_save_changes_canvas"):
                sc = self._save_changes_canvas
                sc.delete("all")
                gc = dim_colour(self.accent, 0.15)
                for i in range(4, 0, -1): 
                    draw_rounded(sc, i, i, 180-i, 54-i, 10, fill=gc, outline="")
                draw_rounded(sc, 4, 4, 176, 50, 8, fill=C_PANEL, outline=self.accent)
                sc.create_text(90, 27, text="SAVE CHANGES", fill=self.accent, font=("Bahnschrift", 13, "bold"))
        
        self.apply_locks()
        self.save()

    # ┌─────────────────────────────────────────────────────────────────────────
    # │  SOCIALS / INTEGRATIONS
    # └─────────────────────────────────────────────────────────────────────────

    def setup_socials(self):
        # Get integrations from user data (empty list if none)
        self.integrations = self.user_data.get("integrations", [])
        
        # Clear existing social scroll area
        for w in self.right_sidebar.winfo_children():
            if getattr(w, "_is_social_scroll", False): w.destroy()
        
        # Create scroll container
        sc = tk.Frame(self.right_sidebar, bg=C_BLACK)
        sc._is_social_scroll = True
        sc.pack(fill="both", expand=True, padx=6)
        soc_can = tk.Canvas(sc, bg=C_BLACK, highlightthickness=0)
        soc_can.pack(side="left", fill="both", expand=True)
        # Pushed slightly away from the absolute edge for a cleaner look
        sb = tk.Canvas(sc, width=36, bg=C_BLACK, highlightthickness=0)
        sb.place(relx=0.98, rely=0, relheight=1, anchor="ne")
        self._socials_frame = tk.Frame(soc_can, bg=C_BLACK)
        setup_scrollbar(sb, soc_can)
        # Capture the ID
        frame_id = soc_can.create_window((0, 0), window=self._socials_frame, anchor="nw")
        # Update scrollregion
        self._socials_frame.bind("<Configure>", lambda e: soc_can.configure(scrollregion=soc_can.bbox("all")))
        # INCREASED: From 0.75 to 0.82 to make the boxes "a little more" wide
        soc_can.bind("<Configure>", lambda e: soc_can.itemconfig(frame_id, width=int(e.width * 0.82)))
        soc_can.bind("<MouseWheel>", lambda e: soc_can.yview_scroll(int(-1*(e.delta/120)), "units"))
        self._socials_frame.bind("<MouseWheel>", lambda e: soc_can.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        # Build integration rows
        for idx, integration in enumerate(self.integrations):
            self._build_integration_row(integration, idx)
        
        # Add empty slots up to MAX_INTEGRATIONS
        empty_count = MAX_INTEGRATIONS - len(self.integrations)
        for i in range(empty_count):
            self._build_empty_integration_slot(len(self.integrations) + i)

    def _build_integration_row(self, data, index):
        """Build a single integration row."""
        row = tk.Frame(self._socials_frame, bg=C_BLACK, highlightbackground=C_PANEL, highlightthickness=1)
        row.pack(fill="x", padx=4, pady=1)
        
        # Click handler
        def _click():
            self.play_click()
            if data["type"] == "application":
                path = data["url"]
                if os.path.exists(path):
                    os.startfile(path)
                else:
                    messagebox.showerror("WizBizz Pro", f"Cannot find: {path}")
            else:
                webbrowser.open(data["url"])
        
        # Icon
        icon_loaded = False
        if data.get("icon"):
            icon_path = os.path.join(ICONS_PATH, data["icon"])
            if os.path.exists(icon_path):
                try:
                    img = Image.open(icon_path).resize((26, 26), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    if not hasattr(self, 'integration_icons'): self.integration_icons = []
                    self.integration_icons.append(photo)
                    lbl = tk.Label(row, image=photo, bg=C_BLACK, cursor="hand2")
                    lbl.pack(side="left", padx=(8, 6), pady=3)
                    lbl.bind("<Button-1>", lambda e: _click())
                    icon_loaded = True
                except Exception as e:
                    log.error(f"Failed to load icon: {e}")
        
        if not icon_loaded:
            # Default letter icon - use brand color
            letter = data["display_name"][0].upper() if data["display_name"] else "?"
            brand_color = data.get("color", self.accent)
            lt = tk.Label(row, text=letter, fg=brand_color, bg=C_BLACK,
                          font=("Bahnschrift", 14, "bold"), width=2, cursor="hand2")
            lt.pack(side="left", padx=(8, 6), pady=3)
            lt.bind("<Button-1>", lambda e: _click())
        
        # Display name label - use brand color
        brand_color = data.get("color", self.accent)
        name_lbl = tk.Label(row, text=data["display_name"], fg=brand_color, bg=C_BLACK,
                            font=("Segoe UI", 10, "bold"), cursor="hand2", anchor="w")
        name_lbl.pack(side="left", fill="x", expand=True, padx=(0, 4), pady=3)
        name_lbl.bind("<Button-1>", lambda e: _click())
        
        # Edit button (only shown in edit mode)
        edit_btn = tk.Button(row, text="✎", bg=C_BLACK, fg=self.accent,
                             font=("Segoe UI", 10), bd=0, cursor="hand2",
                             command=lambda: self._edit_integration(index))
        if self.platforms_edit_mode:
            edit_btn.pack(side="right", padx=(0, 6))
        row._edit_btn = edit_btn
    
    def _build_empty_integration_slot(self, index):
        """Build an empty slot placeholder."""
        row = tk.Frame(self._socials_frame, bg=C_BLACK, highlightbackground=C_PANEL, highlightthickness=1)
        row.pack(fill="x", padx=4, pady=1)
        
        tk.Label(row, text="＋  empty slot", fg=C_BORDER, bg=C_BLACK,
                 font=("Segoe UI", 9)).pack(side="left", padx=12, pady=12)
        
        # Edit button (only shown in edit mode)
        edit_btn = tk.Button(row, text="✎", bg=C_BLACK, fg=self.accent,
                             font=("Segoe UI", 10), bd=0, cursor="hand2",
                             command=lambda: self._edit_integration(index))
        if self.platforms_edit_mode:
            edit_btn.pack(side="right", padx=(0, 6))
        row._edit_btn = edit_btn
    
    def _edit_integration(self, index):
        """Open integration editor dialog."""
        self.play_click()
        
        # Get existing data if editing, None if new
        existing = self.integrations[index] if index < len(self.integrations) else None
        
        def on_save(data):
            if index < len(self.integrations):
                self.integrations[index] = data
            else:
                self.integrations.append(data)
            self.user_data["integrations"] = self.integrations
            self.save()
            self.setup_socials()
            if self.platforms_edit_mode:
                self.apply_locks()  # Re-show edit buttons
        
        def on_delete():
            if index < len(self.integrations):
                # Delete icon file if it exists
                icon_file = self.integrations[index].get("icon")
                if icon_file:
                    icon_path = os.path.join(ICONS_PATH, icon_file)
                    try:
                        if os.path.exists(icon_path):
                            os.remove(icon_path)
                    except Exception as e:
                        log.error(f"Failed to delete icon: {e}")
                
                self.integrations.pop(index)
                self.user_data["integrations"] = self.integrations
                self.save()
                self.setup_socials()
                if self.platforms_edit_mode:
                    self.apply_locks()  # Re-show edit buttons
        
        # If existing, go straight to editor; if new, show template picker
        if existing:
            IntegrationEditor(self.root, self.accent, None, existing, on_save, on_delete)
        else:
            def on_template_select(template_id):
                IntegrationEditor(self.root, self.accent, template_id, None, on_save, None)
            TemplatePicker(self.root, self.accent, on_template_select)

    # ┌─────────────────────────────────────────────────────────────────────────
    # │  FOOTER
    # └─────────────────────────────────────────────────────────────────────────

    def _setup_footer_links(self):
        self.footer_icons = []
        self._footer_labels = []  # Store references for theme updates
        cont = tk.Frame(self.footer, bg=C_BLACK); cont.pack(expand=True)
        for icon, label, url in FOOTER_LINKS:
            f = tk.Frame(cont, bg=C_BLACK); f.pack(side="left", padx=25, pady=20)
            try:
                ip = f"{icon}.png" if os.path.exists(f"{icon}.png") else f"{icon}.jpg"
                img = Image.open(ip).resize((20, 20), Image.Resampling.LANCZOS)
                ph = ImageTk.PhotoImage(img); self.footer_icons.append(ph)
                tk.Label(f, image=ph, bg=C_BLACK, cursor="hand2").pack(side="left", padx=5)
            except Exception: pass
            l2 = tk.Label(f, text=label, fg=self.accent, bg=C_BLACK, font=("Segoe UI", 10, "bold"), cursor="hand2")
            l2.pack(side="left")
            l2.bind("<Button-1>", lambda e, u=url, w=l2: [self.play_click(), self._footer_click(u, w)])
            self._footer_labels.append(l2)  # Store reference
        self.gear = tk.Label(self.footer, text="⚙", fg=C_BORDER, bg=C_BLACK,
            font=("Segoe UI", 18), cursor="hand2")
        self.gear.place(relx=0.98, rely=0.5, anchor="e")
        self.gear.bind("<Button-1>", lambda e: self.open_settings())

    def _footer_click(self, url, widget):
        if url == "DISABLED": return
        if url == "copy_email":
            email = "wizbizzpro@hotmail.com"
            self.root.clipboard_clear(); self.root.clipboard_append(email)
            self._toast(f"Copied: {email}", widget)
        else: webbrowser.open(url)

    def _toast(self, text, widget):
        t = tk.Toplevel(self.root); t.overrideredirect(True); t.configure(bg=self.accent)
        t.geometry(f"+{widget.winfo_rootx()-40}+{widget.winfo_rooty()-40}")
        tk.Label(t, text=text, fg=C_BLACK, bg=self.accent, font=("Segoe UI", 9, "bold"), padx=8, pady=4).pack()
        self.root.after(2000, t.destroy)

    # ┌─────────────────────────────────────────────────────────────────────────
    # │  TOGGLES & EDIT MODES
    # └─────────────────────────────────────────────────────────────────────────

    def _make_toggle(self, parent, label, bg, command):
        cont = tk.Frame(parent, bg=bg); cont.pack(pady=6)
        lbl = tk.Label(cont, text=label, fg=self.accent, bg=bg, font=("Bahnschrift", 11, "bold")); lbl.pack()
        W, H, R = 64, 30, 15
        can = tk.Canvas(cont, width=W, height=H, bg=bg, highlightthickness=0); can.pack(pady=(3, 0))
        glow_layers = []
        for off, a in [(3, 0.12), (2, 0.18), (1, 0.25)]:
            glow = draw_rounded(can, off, off, W-off, H-off, R, fill=dim_colour(self.accent, a), outline="")
            glow_layers.append((glow, off, a))
        pill = draw_rounded(can, 3, 3, W-3, H-3, R, fill=C_PANEL, outline=self.accent)
        knob = can.create_oval(5, 5, H-3, H-3, fill=C_HINT, outline="")
        can.bind("<Button-1>", lambda e: command()); lbl.bind("<Button-1>", lambda e: command())
        return {"can": can, "pill": pill, "knob": knob, "lbl": lbl, "W": W, "H": H, "glow_layers": glow_layers}

    def _setup_sounds_toggle(self):
        f = tk.Frame(self.board_frame, bg=C_BLACK); f.pack(pady=(8, 15))
        self._snd_toggle = self._make_toggle(f, "EDIT DECK", C_BLACK, self.flip_sounds)
        self.can_snd, self.rct_snd, self.swi_snd = self._snd_toggle["can"], self._snd_toggle["pill"], self._snd_toggle["knob"]

    def _setup_platforms_toggle(self):
        f = tk.Frame(self.right_sidebar, bg=C_BLACK); f.pack(pady=6)
        self._plat_toggle = self._make_toggle(f, "", C_BLACK, self.flip_platforms)
        self.can_plat, self.rct_plat, self.swi_plat = self._plat_toggle["can"], self._plat_toggle["pill"], self._plat_toggle["knob"]
        self._plat_toggle["lbl"].pack_forget(); self.can_plat.pack_forget()

    def apply_locks(self):
        W, H = self._snd_toggle["W"], self._snd_toggle["H"]
        sc = C_EDIT if self.sounds_edit_mode else C_PANEL
        self.can_snd.itemconfig(self.rct_snd, fill=sc, outline=self.accent)
        # Update glow layers with current theme
        for glow, off, a in self._snd_toggle["glow_layers"]:
            self.can_snd.itemconfig(glow, fill=dim_colour(self.accent, a))
        # Update label text color
        self._snd_toggle["lbl"].config(fg=self.accent)
        if self.sounds_edit_mode:
            self.can_snd.coords(self.swi_snd, W-H+3, 5, W-5, H-3); self.can_snd.itemconfig(self.swi_snd, fill=C_EDIT)
        else:
            self.can_snd.coords(self.swi_snd, 5, 5, H-3, H-3); self.can_snd.itemconfig(self.swi_snd, fill=C_HINT)

        for bid, btn in self.btns.items():
            if self.sounds_edit_mode:
                if bid in self.user_data:
                    btn["can"].itemconfig(btn["txt"], fill=C_EDIT, text=self.user_data.get(f"{bid}_name"))
                else: btn["can"].itemconfig(btn["txt"], fill=C_BORDER, text="EMPTY")
            else:
                btn["can"].itemconfig(btn["txt"], fill=self.accent, text=self.user_data.get(f"{bid}_name", f"SOUND {bid.split('_')[1]}"))

        W2, H2 = self._plat_toggle["W"], self._plat_toggle["H"]
        pc = C_EDIT if self.platforms_edit_mode else C_PANEL
        self.can_plat.itemconfig(self.rct_plat, fill=pc, outline=self.accent)
        # Update glow layers with current theme
        for glow, off, a in self._plat_toggle["glow_layers"]:
            self.can_plat.itemconfig(glow, fill=dim_colour(self.accent, a))
        if self.platforms_edit_mode:
            self.can_plat.coords(self.swi_plat, W2-H2+3, 5, W2-5, H2-3); self.can_plat.itemconfig(self.swi_plat, fill=C_EDIT)
        else:
            self.can_plat.coords(self.swi_plat, 5, 5, H2-3, H2-3); self.can_plat.itemconfig(self.swi_plat, fill=C_HINT)

        # Show/hide integration edit buttons
        if hasattr(self, "_socials_frame"):
            for row in self._socials_frame.winfo_children():
                edit_btn = getattr(row, "_edit_btn", None)
                if edit_btn:
                    if self.platforms_edit_mode:
                        edit_btn.pack(side="right", padx=(0, 6))
                    else:
                        edit_btn.pack_forget()

    def flip_sounds(self):
        self.play_click(); self.sounds_edit_mode = not self.sounds_edit_mode; self.apply_locks()

    def flip_platforms(self):
        self.play_click(); self.platforms_edit_mode = not self.platforms_edit_mode; self.apply_locks(); self.save()

    # ┌─────────────────────────────────────────────────────────────────────────
    # │  LOGO & NAME
    # └─────────────────────────────────────────────────────────────────────────

    def up_logo(self):
        self.play_click()
        p = filedialog.askopenfilename(title="Choose Your Brand Logo", filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if p: shutil.copy(p, "user_logo.png"); self.refresh_logo()

    def _edit_name(self):
        self.play_click()
        current = self.user_label.cget("text")
        for w in self._name_frame.winfo_children(): w.pack_forget()
        entry = tk.Entry(self._name_frame, font=("Bahnschrift", 22, "bold"), fg=self.accent, bg=C_PANEL,
            insertbackground=self.accent, bd=0, highlightthickness=2, highlightbackground=self.accent, justify="center", width=12)
        entry.insert(0, current); entry.pack(side="left", padx=(0, 4)); entry.focus_set(); entry.select_range(0, "end")
        def _save(event=None):
            name = entry.get().strip() or "Your Name"
            for w in self._name_frame.winfo_children(): w.destroy()
            self.user_label = tk.Label(self._name_frame, text=name, fg=self.accent, bg=C_PANEL,
                font=("Bahnschrift", 22, "bold"), cursor="hand2")
            self.user_label.pack(side="left")
            tk.Label(self._name_frame, text=" ✎", fg=C_BORDER, bg=C_PANEL, font=("Segoe UI", 10), cursor="hand2").pack(side="left")
            self.user_label.bind("<Button-1>", lambda e: self._edit_name())
            self._name_frame.bind("<Button-1>", lambda e: self._edit_name())
            self.user_data["streamer_name"] = name; self.save()
        entry.bind("<Return>", _save); entry.bind("<FocusOut>", _save)
        tk.Button(self._name_frame, text="✔", command=_save, bg=self.accent, fg=C_BLACK,
            font=("Segoe UI", 10, "bold"), bd=0, cursor="hand2", padx=4).pack(side="left")

    def refresh_logo(self):
        try:
            i = Image.open("user_logo.png").resize((130, 130))
            self.uph = ImageTk.PhotoImage(i); self.logo_btn.config(image=self.uph, text="", bg="#111")
        except Exception:
            self.logo_btn.config(image="", text="＋ LOGO", fg=self.accent, bg=C_PANEL, font=("Bahnschrift", 13))

    # ┌─────────────────────────────────────────────────────────────────────────
    # │  SAVE / LOAD
    # └─────────────────────────────────────────────────────────────────────────

    def save(self):
        d = {
            "theme": self.active_theme,
            "startup_apps": self.user_data.get("startup_apps", []),
            "launch_slots": self.launch_slots,
            "streamer_name": self.user_data.get("streamer_name", "Your Name"),
            "size_lock": self.user_data.get("size_lock", True),
            "integrations": self.user_data.get("integrations", []),  # Save integrations!
        }
        # Save soundboard data
        for bid in self.btns:
            if bid in self.user_data: d[bid] = self.user_data[bid]
            if f"{bid}_name" in self.user_data: d[f"{bid}_name"] = self.user_data[f"{bid}_name"]
        save_settings(d)


# ══════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        WizHubPro().root.mainloop()
    except Exception as e:
        log.critical(f"Application crashed: {e}", exc_info=True)
        raise
