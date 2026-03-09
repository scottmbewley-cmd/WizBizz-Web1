import streamlit as st
import math, time, random

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="WIZBIZZ PRO — STREAMER HUB",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── PASSWORD GATE ─────────────────────────────────────────────────────────────
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if st.session_state.authenticated:
        return True

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');
    .stApp { background: #000000; }
    .login-wrap { display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:80vh; }
    .login-title { font-family:'Orbitron',monospace; font-size:2.8rem; font-weight:900; color:#00FFCC;
        text-shadow: 0 0 20px #00FFCC, 0 0 40px #00FFCC55; letter-spacing:0.15em; margin-bottom:0.2em; }
    .login-sub { font-family:'Share Tech Mono',monospace; color:#444; font-size:0.9rem; letter-spacing:0.3em; margin-bottom:2.5em; }
    </style>
    <div class="login-wrap">
        <div class="login-title">WIZBIZZ PRO</div>
        <div class="login-sub">STREAMER HUB · SECURE ACCESS</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        pwd = st.text_input("ACCESS CODE", type="password", placeholder="Enter your access code...")
        if st.button("CONNECT", use_container_width=True):
            if pwd == st.secrets.get("password", "wizbizz2024"):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ ACCESS DENIED")
    return False

if not check_password():
    st.stop()

# ── THEMES ───────────────────────────────────────────────────────────────────
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
    "CHROME":   {"on": "#C0C0C0", "off": "#444444"},
}

PLATFORMS = {
    "TikTok":    {"color": "#FF0050", "icon": "📱"},
    "YouTube":   {"color": "#FF0000", "icon": "▶️"},
    "Twitch":    {"color": "#9146FF", "icon": "🎮"},
    "Instagram": {"color": "#E1306C", "icon": "📸"},
    "Facebook":  {"color": "#1877F2", "icon": "👤"},
    "Kick":      {"color": "#53FC18", "icon": "🟢"},
    "Discord":   {"color": "#5865F2", "icon": "💬"},
    "X":         {"color": "#FFFFFF", "icon": "✖️"},
}

SOUNDBOARD = [
    {"label": "INTRO",     "emoji": "🎬", "color": "#00FFCC"},
    {"label": "HYPE",      "emoji": "🔥", "color": "#FF6B35"},
    {"label": "LOL",       "emoji": "😂", "color": "#FFD700"},
    {"label": "ALERT",     "emoji": "🚨", "color": "#FF1744"},
    {"label": "BRB",       "emoji": "⏸️", "color": "#87CEEB"},
    {"label": "GG",        "emoji": "🏆", "color": "#ADFF2F"},
    {"label": "DROP",      "emoji": "💧", "color": "#9146FF"},
    {"label": "RAID",      "emoji": "⚔️", "color": "#FF0050"},
    {"label": "HYPE 2",    "emoji": "⚡", "color": "#00FFCC"},
    {"label": "SUB",       "emoji": "⭐", "color": "#FFD700"},
    {"label": "DONATE",    "emoji": "💰", "color": "#ADFF2F"},
    {"label": "OUTRO",     "emoji": "🎭", "color": "#FF00FF"},
    {"label": "CLIP IT",   "emoji": "✂️", "color": "#FF6B35"},
    {"label": "POG",       "emoji": "😮", "color": "#00FFCC"},
    {"label": "LETS GO",   "emoji": "🚀", "color": "#FF1744"},
    {"label": "WELCOME",   "emoji": "👋", "color": "#87CEEB"},
    {"label": "FOLLOW",    "emoji": "❤️", "color": "#E1306C"},
    {"label": "SHARE",     "emoji": "📢", "color": "#1877F2"},
    {"label": "MUSIC ON",  "emoji": "🎵", "color": "#9146FF"},
    {"label": "MUSIC OFF", "emoji": "🔇", "color": "#444444"},
    {"label": "SCENE 1",   "emoji": "1️⃣", "color": "#00FFCC"},
    {"label": "SCENE 2",   "emoji": "2️⃣", "color": "#00FFCC"},
    {"label": "SCENE 3",   "emoji": "3️⃣", "color": "#00FFCC"},
    {"label": "SCENE 4",   "emoji": "4️⃣", "color": "#00FFCC"},
    {"label": "OVERLAY",   "emoji": "🖼️", "color": "#FFD700"},
    {"label": "CAM OFF",   "emoji": "📷", "color": "#FF1744"},
    {"label": "CAM ON",    "emoji": "📸", "color": "#ADFF2F"},
    {"label": "SHOUTOUT",  "emoji": "📣", "color": "#FF6B35"},
    {"label": "POLL",      "emoji": "📊", "color": "#87CEEB"},
    {"label": "TIMER",     "emoji": "⏱️", "color": "#FFD700"},
    {"label": "MUTE",      "emoji": "🔕", "color": "#FF1744"},
    {"label": "SFX 32",    "emoji": "🎛️", "color": "#555555"},
]

# ── SESSION STATE ────────────────────────────────────────────────────────────
if "theme" not in st.session_state:       st.session_state.theme = "CYBER"
if "streaming" not in st.session_state:   st.session_state.streaming = False
if "platforms" not in st.session_state:   st.session_state.platforms = {p: False for p in PLATFORMS}
if "last_fired" not in st.session_state:  st.session_state.last_fired = None
if "stream_time" not in st.session_state: st.session_state.stream_time = 0
if "widgets" not in st.session_state:     st.session_state.widgets = ["CHAT MONITOR", "ALERT QUEUE", "BIT TRACKER"]

accent = THEMES[st.session_state.theme]["on"]
accent_off = THEMES[st.session_state.theme]["off"]

# ── GLOBAL CSS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');

:root {{
    --accent: {accent};
    --accent-off: {accent_off};
    --bg: #000000;
    --panel: #0d0d0d;
    --border: #1a1a1a;
    --hint: #555555;
}}

.stApp {{ background: var(--bg) !important; }}
section[data-testid="stSidebar"] {{ background: var(--panel) !important; }}

h1,h2,h3,h4,h5,h6,p,label,div {{
    font-family: 'Share Tech Mono', monospace !important;
    color: #ccc;
}}

.main-title {{
    font-family: 'Orbitron', monospace !important;
    font-size: clamp(1.8rem, 4vw, 3.2rem);
    font-weight: 900;
    color: var(--accent);
    text-shadow: 0 0 20px var(--accent), 0 0 40px var(--accent)55;
    letter-spacing: 0.12em;
    text-align: center;
    margin: 0;
    padding: 0.3em 0 0.1em;
}}

.sub-title {{
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.75rem;
    color: var(--hint);
    letter-spacing: 0.35em;
    text-align: center;
    margin-bottom: 1.2em;
}}

.panel {{
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1rem;
    margin-bottom: 0.8rem;
}}

.panel-title {{
    font-family: 'Orbitron', monospace !important;
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: 0.25em;
    text-shadow: 0 0 8px var(--accent)88;
    margin-bottom: 0.8rem;
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.4rem;
}}

.stream-live {{
    background: linear-gradient(135deg, #1a0000, #2d0000);
    border: 1px solid #CC0000;
    border-radius: 4px;
    padding: 1.2rem;
    text-align: center;
    animation: pulse-red 2s infinite;
}}

.stream-idle {{
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1.2rem;
    text-align: center;
}}

@keyframes pulse-red {{
    0%,100% {{ box-shadow: 0 0 8px #CC000066; }}
    50%      {{ box-shadow: 0 0 20px #CC0000BB; }}
}}

.live-badge {{
    font-family: 'Orbitron', monospace !important;
    font-size: 1.6rem;
    font-weight: 900;
    color: #CC0000;
    text-shadow: 0 0 15px #CC0000;
    animation: pulse-red 1s infinite;
}}

.platform-btn-on {{
    display:inline-block; padding:6px 14px; border-radius:3px; margin:3px;
    font-family:'Share Tech Mono',monospace; font-size:0.8rem; font-weight:700;
    border: 1px solid; cursor:pointer;
}}

.sound-btn {{
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 3px;
    padding: 0.6rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.15s;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
}}

.widget-chip {{
    display: inline-block;
    background: var(--panel);
    border: 1px solid var(--accent)55;
    color: var(--accent);
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    padding: 4px 10px;
    border-radius: 2px;
    margin: 3px;
    letter-spacing: 0.15em;
}}

.stat-val {{
    font-family: 'Orbitron', monospace !important;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--accent);
    text-shadow: 0 0 10px var(--accent)88;
}}

.stat-lbl {{
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.65rem;
    color: var(--hint);
    letter-spacing: 0.2em;
}}

.theme-swatch {{
    display:inline-block; width:22px; height:22px; border-radius:2px;
    margin:2px; cursor:pointer; border: 2px solid transparent;
}}

.footer-bar {{
    background: var(--panel);
    border-top: 1px solid var(--border);
    padding: 0.6rem 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 1rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    color: var(--hint);
    letter-spacing: 0.1em;
}}

div[data-testid="stButton"] button {{
    font-family: 'Share Tech Mono', monospace !important;
    letter-spacing: 0.1em;
    font-size: 0.8rem;
    border-radius: 2px !important;
}}

div[data-testid="stSelectbox"] label,
div[data-testid="stMultiSelect"] label {{
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.75rem;
    color: var(--hint) !important;
    letter-spacing: 0.15em;
}}

.ecg-bar {{
    height: 40px;
    background: linear-gradient(90deg, transparent, var(--accent)33, var(--accent)99, var(--accent)33, transparent);
    border-radius: 2px;
    animation: ecg-sweep 2s linear infinite;
    margin: 6px 0;
}}

@keyframes ecg-sweep {{
    0%   {{ background-position: -200% center; }}
    100% {{ background-position: 200% center; }}
}}

.scanline {{
    position:fixed; top:0; left:0; right:0; bottom:0; pointer-events:none;
    background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.03) 2px, rgba(0,0,0,0.03) 4px);
    z-index:9999;
}}
</style>
<div class="scanline"></div>
""", unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">WIZBIZZ PRO</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">STREAMER HUB · v1.0</div>', unsafe_allow_html=True)

# ── LAYOUT: 3 COLUMNS ────────────────────────────────────────────────────────
left, centre, right = st.columns([1.1, 2, 1.1])

# ════════════════════════════════════════════════════════════
# LEFT SIDEBAR
# ════════════════════════════════════════════════════════════
with left:
    # LAUNCH PAD
    st.markdown(f'<div class="panel"><div class="panel-title">⬡ LAUNCH PAD</div>', unsafe_allow_html=True)
    launch_apps = ["OBS Studio", "Spotify", "Discord", "Browser", "Chat App", "Scene Switcher"]
    for app in launch_apps:
        if st.button(f"▶  {app}", key=f"launch_{app}", use_container_width=True):
            st.toast(f"Launching {app}...", icon="🚀")
    st.markdown('</div>', unsafe_allow_html=True)

    # WIDGET SLOTS
    st.markdown(f'<div class="panel"><div class="panel-title">⬡ ACTIVE WIDGETS</div>', unsafe_allow_html=True)
    for w in st.session_state.widgets:
        st.markdown(f'<span class="widget-chip">◈ {w}</span>', unsafe_allow_html=True)
    new_widget = st.selectbox("ADD WIDGET", ["", "CHAT MONITOR", "ALERT QUEUE", "BIT TRACKER",
                                              "FOLLOW FEED", "CLIP CATCHER", "POLL TRACKER"], key="new_w", label_visibility="collapsed")
    if new_widget and new_widget not in st.session_state.widgets:
        st.session_state.widgets.append(new_widget)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# CENTRE
# ════════════════════════════════════════════════════════════
with centre:
    # STREAM STATUS
    if st.session_state.streaming:
        st.markdown(f"""
        <div class="stream-live">
            <div class="live-badge">⬤ LIVE</div>
            <div style="font-family:'Share Tech Mono';font-size:0.75rem;color:#888;letter-spacing:0.2em;margin-top:4px;">STREAM IS RUNNING</div>
            <div class="ecg-bar"></div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("⏹  END STREAM", use_container_width=True, type="primary"):
            st.session_state.streaming = False
            st.toast("Stream ended", icon="⏹️")
            st.rerun()
    else:
        st.markdown(f"""
        <div class="stream-idle">
            <div style="font-family:'Orbitron',monospace;font-size:1.1rem;color:#333;letter-spacing:0.2em;">◯  OFFLINE</div>
            <div style="font-family:'Share Tech Mono';font-size:0.7rem;color:#2a2a2a;letter-spacing:0.2em;margin-top:4px;">READY TO BROADCAST</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("▶  GO LIVE", use_container_width=True, type="primary"):
            st.session_state.streaming = True
            st.toast("🔴 You're LIVE!", icon="🎙️")
            st.rerun()

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # STATS ROW
    s1, s2, s3, s4 = st.columns(4)
    stats = [
        ("2,847", "VIEWERS"),
        ("142", "FOLLOWERS"),
        ("38", "SUBS"),
        ("$124", "DONATIONS"),
    ]
    for col, (val, lbl) in zip([s1,s2,s3,s4], stats):
        with col:
            st.markdown(f"""
            <div class="panel" style="text-align:center;padding:0.6rem">
                <div class="stat-val">{val}</div>
                <div class="stat-lbl">{lbl}</div>
            </div>""", unsafe_allow_html=True)

    # BIZZ DECK (SOUNDBOARD)
    st.markdown(f'<div class="panel"><div class="panel-title">⬡ BIZZ DECK</div>', unsafe_allow_html=True)
    cols = st.columns(8)
    for i, sound in enumerate(SOUNDBOARD):
        with cols[i % 8]:
            if st.button(f"{sound['emoji']}\n{sound['label']}", key=f"sound_{i}", use_container_width=True):
                st.session_state.last_fired = sound['label']
                st.toast(f"🔊 {sound['label']} fired!", icon=sound['emoji'])
    if st.session_state.last_fired:
        st.markdown(f'<div style="font-family:Share Tech Mono;font-size:0.7rem;color:{accent};text-align:right;margin-top:4px;letter-spacing:0.15em">LAST FIRED: {st.session_state.last_fired}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # THEME SELECTOR
    st.markdown(f'<div class="panel"><div class="panel-title">⬡ INTERFACE THEME</div>', unsafe_allow_html=True)
    theme_cols = st.columns(len(THEMES))
    for col, (name, colors) in zip(theme_cols, THEMES.items()):
        with col:
            border = "3px solid white" if name == st.session_state.theme else "2px solid #222"
            st.markdown(f'<div style="background:{colors["on"]};width:28px;height:28px;border-radius:3px;border:{border};margin:auto;cursor:pointer"></div>', unsafe_allow_html=True)
            if st.button(name[:3], key=f"theme_{name}", use_container_width=True):
                st.session_state.theme = name
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# RIGHT SIDEBAR
# ════════════════════════════════════════════════════════════
with right:
    # MY WIZ / BRAND
    st.markdown(f'<div class="panel"><div class="panel-title">⬡ MY WIZ</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:#0a0a0a;border:1px solid #1a1a1a;width:120px;height:120px;
        margin:auto;display:flex;align-items:center;justify-content:center;
        font-family:Orbitron;font-size:2rem;color:{accent};
        text-shadow:0 0 15px {accent};">WB</div>
    <div style="text-align:center;font-family:Share Tech Mono;font-size:0.7rem;
        color:#444;margin-top:6px;letter-spacing:0.2em">YOUR BRAND</div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # INTEGRATIONS
    st.markdown(f'<div class="panel"><div class="panel-title">⬡ INTEGRATIONS</div>', unsafe_allow_html=True)
    for platform, info in PLATFORMS.items():
        is_on = st.session_state.platforms[platform]
        col_a, col_b = st.columns([3,1])
        with col_a:
            color = info["color"] if is_on else "#333"
            st.markdown(f'<div style="font-family:Share Tech Mono;font-size:0.8rem;color:{color};padding:4px 0;letter-spacing:0.1em">{info["icon"]} {platform}</div>', unsafe_allow_html=True)
        with col_b:
            label = "ON" if is_on else "OFF"
            if st.button(label, key=f"plat_{platform}"):
                st.session_state.platforms[platform] = not is_on
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # SETTINGS QUICK ACCESS
    st.markdown(f'<div class="panel"><div class="panel-title">⬡ SETTINGS</div>', unsafe_allow_html=True)
    st.toggle("WINDOW LOCK", key="win_lock")
    st.toggle("AUTO-LAUNCH", key="auto_launch")
    st.toggle("NOTIFICATIONS", key="notifs", value=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
active_platforms = [p for p, on in st.session_state.platforms.items() if on]
platform_str = "  ·  ".join(active_platforms) if active_platforms else "NO PLATFORMS ACTIVE"
status_str = "🔴 LIVE" if st.session_state.streaming else "◯ OFFLINE"

st.markdown(f"""
<div class="footer-bar">
    <span>WIZBIZZ PRO · v1.0</span>
    <span style="color:{accent}">{status_str}</span>
    <span>{platform_str}</span>
    <span>THEME: {st.session_state.theme}</span>
</div>
""", unsafe_allow_html=True)
