import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="WIZBIZZ PRO — STREAMER HUB",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide ALL Streamlit chrome so only our app shows
st.markdown("""
<style>
#MainMenu, header, footer, .stDeployButton { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
.stApp { background: #000 !important; overflow: hidden; }
section[data-testid="stAppViewContainer"] { padding: 0 !important; }
div[data-testid="stAppViewBlockContainer"] { padding: 0 !important; max-width:100% !important; }
</style>
""", unsafe_allow_html=True)

APP_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Rajdhani:wght@600;700&display=swap" rel="stylesheet">
<style>
  :root {
    --accent: #00FFCC;
    --accent-dim: rgba(0,255,204,0.12);
    --black: #000;
    --panel: #111;
    --border: #222;
    --detail: #444;
    --hint: #666;
    --edit: #FF4444;
  }
  * { box-sizing:border-box; margin:0; padding:0; }
  html,body { background:#000; color:#fff; font-family:'Rajdhani','Segoe UI',sans-serif; overflow:hidden; height:100vh; width:100vw; }

  /* SCANLINES */
  body::after {
    content:''; position:fixed; inset:0; pointer-events:none; z-index:9999;
    background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.025) 2px, rgba(0,0,0,0.025) 4px);
  }

  /* LAYOUT */
  #app { display:flex; flex-direction:column; height:100vh; }
  #row { display:flex; flex:1; overflow:hidden; }
  #left  { width:245px; min-width:245px; display:flex; flex-direction:column; border-right:1px solid var(--border); }
  #mid   { flex:1; display:flex; flex-direction:column; overflow:hidden; }
  #right { width:245px; min-width:245px; display:flex; flex-direction:column; border-left:1px solid var(--border); }
  #foot  { height:44px; border-top:1px solid var(--border); display:flex; align-items:center; justify-content:space-between; padding:0 16px; flex-shrink:0; position:relative; }

  /* GLOW TEXT */
  .glow {
    font-family:'Bebas Neue',Impact,sans-serif; letter-spacing:.08em; line-height:1;
    color:var(--accent);
    text-shadow: 0 0 4px var(--accent), 0 0 12px var(--accent), 0 0 28px color-mix(in srgb,var(--accent) 45%,transparent);
  }

  /* PANEL */
  .box { background:var(--panel); border:1px solid var(--border); }

  /* ── LEFT ── */
  #lhead { padding:8px 8px 0; flex-shrink:0; }
  #lhead .box { padding:0 0 6px; text-align:center; }
  #lhead .glow { font-size:20px; display:block; padding:8px 0 4px; }
  .addbtn { display:block; width:calc(100% - 16px); margin:0 8px 6px; background:var(--border); color:var(--accent);
    font:700 12px/1 'Rajdhani',sans-serif; letter-spacing:1px; border:none; cursor:pointer; padding:7px; transition:background .15s; }
  .addbtn:hover { background:var(--detail); }

  #scene-sw { display:flex; align-items:center; justify-content:center; gap:7px; background:var(--panel);
    border:1px solid var(--border); margin:5px 8px; padding:7px; cursor:pointer;
    font:700 12px/1 'Rajdhani',sans-serif; letter-spacing:1px; color:#ddd; transition:border-color .2s,color .2s; }
  #scene-sw:hover { border-color:var(--accent); color:var(--accent); }

  #wscroll { flex:1; overflow-y:auto; padding:3px 6px; }
  #wscroll::-webkit-scrollbar { width:3px; }
  #wscroll::-webkit-scrollbar-thumb { background:var(--border); }
  .wcount { color:var(--accent); font-size:10px; font-weight:700; letter-spacing:1px; padding:4px 4px 3px; }
  .wslot { background:#000; border:1px solid var(--panel); padding:5px 8px; margin-bottom:2px;
    font-size:10px; letter-spacing:.5px; color:var(--border); cursor:pointer; transition:border-color .15s; }
  .wslot.on { border-color:var(--border); color:var(--accent); display:flex; align-items:center; gap:6px; }
  .wdot { width:5px; height:5px; border-radius:50%; background:var(--accent); box-shadow:0 0 5px var(--accent); flex-shrink:0; }
  .wiz-sel { width:calc(100% - 10px); margin:3px 5px; background:var(--panel); border:1px solid var(--border);
    color:var(--hint); font:12px 'Rajdhani',sans-serif; padding:4px 6px; cursor:pointer; }

  /* LAUNCH */
  #lframe { background:var(--panel); border:1px solid var(--border); margin:5px 8px 8px;
    padding:8px; text-align:center; flex-shrink:0; }
  #radar { display:block; margin:0 auto; cursor:pointer; }
  #lhint { color:var(--hint); font-size:8px; letter-spacing:1px; margin-top:3px; font-weight:700; }
  #running { display:none; cursor:pointer; }
  #ecg-cv { display:block; margin:0 auto; }
  .livebadge { display:inline-flex; align-items:center; gap:5px; color:#CC0000;
    font-size:10px; font-weight:700; letter-spacing:2px; margin-top:3px; }
  .ldot { width:7px; height:7px; border-radius:50%; background:#CC0000; animation:pdot 1s infinite; }
  @keyframes pdot { 0%,100%{box-shadow:0 0 3px #CC0000} 50%{box-shadow:0 0 10px #CC0000} }

  /* ── MID ── */
  #mtitle { text-align:center; font-size:50px; padding:5px 0 0; flex-shrink:0; }
  #mlogo  { text-align:center; color:var(--panel); font:700 18px/1 'Bebas Neue',sans-serif;
    letter-spacing:4px; padding:1px 0 2px; flex-shrink:0; }

  /* BIZZ DECK */
  #deck { flex:1; margin:3px 8px 4px; border:1px solid var(--border); display:flex; flex-direction:column; overflow:hidden; min-height:0; }
  #dtitle { text-align:center; font-size:18px; padding:4px 0 2px; flex-shrink:0; }
  #dgrid { display:grid; grid-template-columns:repeat(8,1fr); gap:3px; padding:3px 6px; flex:1; min-height:0; }
  .dbtn {
    background:var(--panel); border:1px solid var(--border); border-radius:7px;
    display:flex; flex-direction:column; align-items:center; justify-content:center;
    cursor:pointer; padding:3px 1px; position:relative; overflow:hidden; user-select:none;
    transition:border-color .15s, box-shadow .15s, background .15s;
  }
  .dbtn:hover { border-color:var(--accent); box-shadow:0 0 7px var(--accent-dim); }
  .dbtn:active,.dbtn.fire { border-color:var(--accent); box-shadow:0 0 14px var(--accent); background:color-mix(in srgb,var(--accent) 14%,#000); }
  .dbtn.edit .dlbl { color:var(--edit) !important; }
  .dbtn.empty .dlbl { color:var(--border) !important; }
  .dico { font-size:16px; line-height:1; margin-bottom:2px; }
  .dlbl { color:var(--accent); font:700 7.5px/1.15 'Rajdhani',sans-serif; text-align:center; letter-spacing:.3px; }
  #lfired { color:var(--hint); font-size:8px; letter-spacing:1px; padding:1px 8px 3px; text-align:right; flex-shrink:0; }
  #lfired span { color:var(--accent); }

  /* DECK CONTROLS */
  #dctrl { display:flex; align-items:center; justify-content:center; gap:10px; padding:3px 8px 6px; flex-shrink:0; }
  .tlbl { color:var(--accent); font:700 10px/1 'Rajdhani',sans-serif; letter-spacing:1px; }
  .tpill { width:48px; height:22px; border-radius:11px; background:var(--panel); border:1px solid var(--accent);
    position:relative; cursor:pointer; transition:background .2s; box-shadow:0 0 5px var(--accent-dim); }
  .tpill.on { background:color-mix(in srgb,var(--edit) 18%,var(--panel)); border-color:var(--edit); }
  .tknob { position:absolute; top:2px; left:2px; width:16px; height:16px; border-radius:50%;
    background:var(--hint); transition:left .2s,background .2s; }
  .tpill.on .tknob { left:28px; background:var(--edit); }

  /* THEME */
  #tsec { background:#000; border:1px solid var(--border); margin:0 8px 4px; padding:5px 8px 6px; flex-shrink:0; }
  #tttl { font-size:12px; letter-spacing:1px; margin-bottom:5px; }
  #tgrid { display:flex; gap:5px; flex-wrap:wrap; }
  .tbtn { display:flex; flex-direction:column; align-items:center; gap:2px; cursor:pointer; padding:1px; }
  .tsw { width:27px; height:27px; border-radius:3px; border:2px solid transparent; transition:border-color .15s; }
  .tbtn.active .tsw { border-color:#fff; box-shadow:0 0 7px rgba(255,255,255,.45); }
  .tbtn:hover .tsw { border-color:rgba(255,255,255,.4); }
  .tnm { font-size:7px; font-weight:700; letter-spacing:.3px; opacity:.65; }

  /* SETTINGS */
  #ssec { background:var(--panel); border:1px solid var(--border); margin:0 8px 5px; padding:6px 10px; flex-shrink:0; }
  #sttl { font-size:12px; letter-spacing:1px; margin-bottom:6px; }
  .srow { display:flex; align-items:center; justify-content:space-between; margin-bottom:5px; }
  .slbl { font-size:9px; font-weight:700; letter-spacing:1px; color:#ccc; }
  .stog { width:36px; height:18px; border-radius:9px; background:#CC0000; position:relative;
    cursor:pointer; border:none; transition:background .2s; flex-shrink:0; }
  .stog::after { content:''; position:absolute; top:2px; right:2px; width:14px; height:14px;
    border-radius:50%; background:#fff; transition:right .2s; }
  .stog.off { background:var(--detail); }
  .stog.off::after { right:auto; left:2px; }

  /* ── RIGHT ── */
  #rhead { padding:8px 8px 0; flex-shrink:0; }
  #rhead .box { text-align:center; padding:6px 0 7px; }
  #rrscroll { flex:1; overflow-y:auto; padding:0 8px; }
  #rrscroll::-webkit-scrollbar { width:3px; }
  #rrscroll::-webkit-scrollbar-thumb { background:var(--border); }

  /* Brand */
  .rbox { background:var(--panel); border:1px solid var(--border); margin-bottom:5px; padding:8px; }
  #logobox { width:100px; height:100px; background:var(--panel); border:1px dashed var(--border);
    display:flex; align-items:center; justify-content:center; cursor:pointer; margin:0 auto 3px;
    color:var(--border); font-size:13px; font-weight:700; transition:border-color .15s; }
  #logobox:hover { border-color:var(--accent); color:var(--accent); }
  #sname { color:var(--accent); font:700 18px/1 'Bebas Neue',sans-serif; letter-spacing:1px;
    margin-top:4px; cursor:pointer; text-align:center; }
  .muted { color:var(--hint); font-size:7.5px; text-align:center; display:block; margin-top:2px; }

  /* Integrations */
  #igbox { background:var(--panel); border:1px solid var(--border); margin-bottom:5px; }
  .prow { display:flex; align-items:center; justify-content:space-between; padding:4px 8px;
    border-bottom:1px solid var(--border); }
  .prow:last-child { border-bottom:none; }
  .pleft { display:flex; align-items:center; gap:7px; }
  .pico { font-size:13px; width:18px; text-align:center; }
  .pname { font-size:10px; font-weight:700; letter-spacing:.3px; }
  .ptog { font-size:8px; font-weight:700; letter-spacing:1px; padding:3px 7px;
    border:none; cursor:pointer; font-family:'Rajdhani',sans-serif; border-radius:2px; min-width:32px; text-align:center; }
  .ptog.on  { background:var(--accent); color:#000; }
  .ptog.off { background:var(--border); color:var(--hint); }

  /* ── FOOTER ── */
  #foot { font:700 8.5px/1 'Rajdhani',sans-serif; letter-spacing:1px; color:var(--hint); }
  #flinks { display:flex; gap:20px; }
  .flink { color:var(--accent); text-decoration:none; font:700 9px/1 'Rajdhani',sans-serif;
    letter-spacing:.5px; cursor:pointer; transition:opacity .15s; display:flex; align-items:center; gap:4px; }
  .flink:hover { opacity:.65; }
  #fstatus { display:flex; align-items:center; gap:5px; font:700 9px/1 'Rajdhani',sans-serif; letter-spacing:2px; }
  #sdot { width:7px; height:7px; border-radius:50%; background:var(--detail); }
  #sdot.live { background:#00cc44; box-shadow:0 0 6px #00cc44; }

  /* RIPPLE */
  .rip { position:absolute; border-radius:50%;
    background:radial-gradient(circle,var(--accent) 0%,transparent 70%);
    opacity:.35; pointer-events:none; animation:rout .4s ease-out forwards; transform:translate(-50%,-50%); }
  @keyframes rout { to { width:120px; height:120px; opacity:0; } }

  /* TOAST */
  #toast { position:fixed; bottom:54px; left:50%; transform:translateX(-50%);
    background:var(--accent); color:#000; font:700 10px/1 'Rajdhani',sans-serif;
    padding:5px 14px; letter-spacing:1px; border-radius:2px;
    opacity:0; transition:opacity .18s; pointer-events:none; z-index:999; white-space:nowrap; }
  #toast.show { opacity:1; }
</style>
</head>
<body>
<div id="app">
  <div id="row">

    <!-- ══ LEFT ══ -->
    <div id="left">
      <div id="lhead">
        <div class="box">
          <span class="glow">Wiz Widgets</span>
          <button class="addbtn" onclick="toast('Widget store — coming soon!')">+ ADD WIDGET</button>
        </div>
      </div>
      <div id="scene-sw" onclick="toast('Scene Switcher activated')">▶ Scene Switcher</div>
      <div id="wscroll">
        <div class="wcount">◆ ACTIVE WIDGETS</div>
        <div class="wslot on"><div class="wdot"></div>CHAT MONITOR</div>
        <div class="wslot on"><div class="wdot"></div>ALERT QUEUE</div>
        <div class="wslot on"><div class="wdot"></div>BIT TRACKER</div>
        <div class="wslot">SLOT 4</div>
        <div class="wslot">SLOT 5</div>
        <div class="wslot">SLOT 6</div>
        <div class="wslot">SLOT 7</div>
        <div class="wslot">SLOT 8</div>
        <div class="wslot">SLOT 9</div>
        <div class="wslot">SLOT 10</div>
        <div class="wslot">SLOT 11</div>
        <div class="wslot">SLOT 12</div>
      </div>
      <select class="wiz-sel" onchange="toast('Widget: '+this.value)">
        <option value="">Select Widget…</option>
        <option>OBS Scene Monitor</option>
        <option>Donation Tracker</option>
        <option>Sub Counter</option>
        <option>Clip Queue</option>
      </select>
      <div id="lframe">
        <canvas id="radar" width="120" height="120" onclick="toggleLive()"></canvas>
        <div id="lhint">Press Launch to Start</div>
        <div id="running" onclick="toggleLive()">
          <canvas id="ecg-cv" width="220" height="55"></canvas>
          <div class="livebadge"><div class="ldot"></div>LIVE</div>
        </div>
      </div>
    </div>

    <!-- ══ MID ══ -->
    <div id="mid">
      <div class="glow" id="mtitle">STREAMER HUB</div>
      <div id="mlogo">WIZBIZZ PRO</div>
      <div id="deck">
        <div class="glow" id="dtitle">BIZZ DECK</div>
        <div id="dgrid"></div>
        <div id="lfired">LAST FIRED: <span id="lfname">—</span></div>
        <div id="dctrl">
          <span class="tlbl">EDIT DECK</span>
          <div class="tpill" id="etoggle" onclick="toggleEdit()"><div class="tknob"></div></div>
        </div>
      </div>
      <div id="tsec">
        <div class="glow" id="tttl" style="font-size:13px;letter-spacing:1px;">◆ INTERFACE THEME</div>
        <div id="tgrid">
          <div class="tbtn active" onclick="setTheme(this,'cyber','#00FFCC','CYB')"><div class="tsw" style="background:#00FFCC"></div><div class="tnm">CYB</div></div>
          <div class="tbtn" onclick="setTheme(this,'neon','#FF00FF','NEO')"><div class="tsw" style="background:#FF00FF"></div><div class="tnm">NEO</div></div>
          <div class="tbtn" onclick="setTheme(this,'gold','#FFD700','GOL')"><div class="tsw" style="background:#FFD700"></div><div class="tnm">GOL</div></div>
          <div class="tbtn" onclick="setTheme(this,'toxic','#ADFF2F','TOX')"><div class="tsw" style="background:#ADFF2F"></div><div class="tnm">TOX</div></div>
          <div class="tbtn" onclick="setTheme(this,'blood','#FF1744','BLO')"><div class="tsw" style="background:#FF1744"></div><div class="tnm">BLO</div></div>
          <div class="tbtn" onclick="setTheme(this,'arctic','#87CEEB','ARC')"><div class="tsw" style="background:#87CEEB"></div><div class="tnm">ARC</div></div>
          <div class="tbtn" onclick="setTheme(this,'cobalt','#0047AB','COB')"><div class="tsw" style="background:#0047AB"></div><div class="tnm">COB</div></div>
          <div class="tbtn" onclick="setTheme(this,'ember','#FF6B35','EMB')"><div class="tsw" style="background:#FF6B35"></div><div class="tnm">EMB</div></div>
          <div class="tbtn" onclick="setTheme(this,'rosegold','#FFB6C1','ROS')"><div class="tsw" style="background:#FFB6C1"></div><div class="tnm">ROS</div></div>
          <div class="tbtn" onclick="setTheme(this,'chrome','#C0C0C0','CHR')"><div class="tsw" style="background:#C0C0C0"></div><div class="tnm">CHR</div></div>
        </div>
      </div>
      <div id="ssec">
        <div class="glow" id="sttl" style="font-size:13px;letter-spacing:1px;">◆ SETTINGS</div>
        <div class="srow"><span class="slbl">WINDOW LOCK</span><button class="stog" onclick="this.classList.toggle('off');toast('Window Lock toggled')"></button></div>
        <div class="srow"><span class="slbl">AUTO-LAUNCH</span><button class="stog" onclick="this.classList.toggle('off');toast('Auto-Launch toggled')"></button></div>
        <div class="srow"><span class="slbl">NOTIFICATIONS</span><button class="stog" onclick="this.classList.toggle('off');toast('Notifications toggled')"></button></div>
      </div>
    </div>

    <!-- ══ RIGHT ══ -->
    <div id="right">
      <div id="rhead">
        <div class="box"><span class="glow" style="font-size:20px;display:block;padding:6px 0 7px;text-align:center;">My Wiz</span></div>
      </div>
      <div id="rrscroll">
        <div class="rbox" style="text-align:center;margin-top:5px;">
          <div id="logobox" onclick="toast('Logo upload — desktop app feature')">＋ LOGO</div>
          <span class="muted">Click logo to change</span>
          <div id="sname" onclick="editName()">Your Name <span style="color:var(--border);font-size:11px;">✎</span></div>
          <span class="muted">Click name to edit</span>
        </div>
        <div id="igbox">
          <div class="glow" style="font-size:13px;text-align:center;padding:7px 0 3px;letter-spacing:1px;display:block;">INTEGRATIONS</div>
          <button class="addbtn" style="margin:0 8px 6px;width:calc(100% - 16px);" onclick="toast('Toggle Edit to manage integrations')">✎ EDIT</button>
          <div id="platlist"></div>
        </div>
      </div>
    </div>

  </div><!-- /row -->

  <!-- FOOTER -->
  <div id="foot">
    <span style="font-size:8px;letter-spacing:1px;">WIZBIZZ PRO · v1.0</span>
    <div id="fstatus"><div id="sdot"></div><span id="stxt">OFFLINE</span></div>
    <div id="flinks">
      <a class="flink" href="https://www.tiktok.com/@wizbizzpro" target="_blank">◈ TikTok</a>
      <a class="flink" href="https://www.youtube.com/@wizbizzpro" target="_blank">▶ YouTube</a>
      <a class="flink" href="https://www.twitch.tv" target="_blank">◈ Twitch</a>
      <a class="flink" href="https://www.instagram.com" target="_blank">◎ Instagram</a>
      <a class="flink" onclick="toast('wizbizzpro@hotmail.com copied!')">✉ Support</a>
    </div>
    <span id="ftheme" style="font-size:8px;letter-spacing:1px;">THEME: CYBER</span>
  </div>
</div><!-- /app -->
<div id="toast"></div>

<script>
// ── BUTTONS ──
const BTNS = [
  {i:"⚡",l:"INTRO"},{i:"🔥",l:"HYPE"},{i:"😂",l:"LOL"},{i:"🚨",l:"ALERT"},
  {i:"⏸",l:"BRB"},{i:"🏆",l:"GG"},{i:"💧",l:"DROP"},{i:"⚔",l:"RAID"},
  {i:"⚡",l:"HYPE 2"},{i:"⭐",l:"SUB"},{i:"💰",l:"DONATE"},{i:"🎭",l:"OUTRO"},
  {i:"✂",l:"CLIP IT"},{i:"😮",l:"POG"},{i:"🚀",l:"LETS GO"},{i:"👋",l:"WELCOME"},
  {i:"❤",l:"FOLLOW"},{i:"📢",l:"SHARE"},{i:"🎵",l:"MUSIC ON"},{i:"🔇",l:"MUSIC OFF"},
  {i:"1️⃣",l:"SCENE 1"},{i:"2️⃣",l:"SCENE 2"},{i:"3️⃣",l:"SCENE 3"},{i:"4️⃣",l:"SCENE 4"},
  {i:"🖼",l:"OVERLAY"},{i:"📷",l:"CAM OFF"},{i:"📸",l:"CAM ON"},{i:"📣",l:"SHOUTOUT"},
  {i:"📊",l:"POLL"},{i:"⏱",l:"TIMER"},{i:"🔕",l:"MUTE"},{i:"🎛",l:"SFX 32"},
];

const PLATS = [
  {n:"YouTube",  c:"#FF0000",i:"▶"},
  {n:"Twitch",   c:"#9146FF",i:"◈"},
  {n:"Instagram",c:"#E1306C",i:"◎"},
  {n:"Facebook", c:"#1877F2",i:"◉"},
  {n:"Kick",     c:"#53FC18",i:"◆"},
  {n:"Discord",  c:"#5865F2",i:"◇"},
  {n:"TikTok",   c:"#FF0050",i:"◈"},
];
const platState = {YouTube:true,Twitch:true,Instagram:true,Facebook:true,Kick:false,Discord:false,TikTok:false};

// Build deck
const grid = document.getElementById('dgrid');
let editMode = false;

function buildDeck() {
  grid.innerHTML = '';
  BTNS.forEach((b,i) => {
    const d = document.createElement('div');
    d.className = 'dbtn';
    d.dataset.i = i;
    d.innerHTML = `<div class="dico">${b.i}</div><div class="dlbl">${b.l}</div>`;
    d.addEventListener('click', e => fireBtn(d, b, e));
    grid.appendChild(d);
  });
}
buildDeck();

function fireBtn(el, b, e) {
  if (editMode) { toast('Assign sound: '+b.l); return; }
  const rect = el.getBoundingClientRect();
  const rip = document.createElement('div');
  rip.className='rip';
  rip.style.cssText=`width:8px;height:8px;left:${e.clientX-rect.left}px;top:${e.clientY-rect.top}px`;
  el.appendChild(rip);
  setTimeout(()=>rip.remove(),420);
  el.classList.add('fire');
  setTimeout(()=>el.classList.remove('fire'),360);
  document.getElementById('lfname').textContent = b.l;
  toast('🔥 '+b.l+' FIRED');
}

function toggleEdit() {
  editMode = !editMode;
  document.getElementById('etoggle').classList.toggle('on', editMode);
  grid.querySelectorAll('.dbtn').forEach(d => d.classList.toggle('edit', editMode));
  toast(editMode ? '✎ Edit Mode — click to assign' : 'Edit Mode OFF');
}

// Build platforms
function buildPlats() {
  const pl = document.getElementById('platlist');
  pl.innerHTML = '';
  PLATS.forEach(p => {
    const on = platState[p.n];
    const row = document.createElement('div');
    row.className = 'prow';
    row.innerHTML = `
      <div class="pleft">
        <span class="pico" style="color:${on?p.c:'#444'}">${p.i}</span>
        <span class="pname" style="color:${on?'#ddd':'#555'}">${p.n}</span>
      </div>
      <button class="ptog ${on?'on':'off'}" onclick="togglePlat('${p.n}')">${on?'ON':'OFF'}</button>`;
    pl.appendChild(row);
  });
}
buildPlats();

function togglePlat(name) {
  platState[name] = !platState[name];
  buildPlats();
}

// Themes
function setTheme(el, name, hex, abbr) {
  document.querySelectorAll('.tbtn').forEach(b=>b.classList.remove('active'));
  el.classList.add('active');
  document.documentElement.style.setProperty('--accent', hex);
  // Update accent-dim
  const r=parseInt(hex.slice(1,3),16),g=parseInt(hex.slice(3,5),16),b=parseInt(hex.slice(5,7),16);
  document.documentElement.style.setProperty('--accent-dim',`rgba(${r},${g},${b},0.12)`);
  document.getElementById('ftheme').textContent = 'THEME: ' + name.toUpperCase();
  toast('Theme: '+name.toUpperCase());
}

// Live / Radar
let isLive=false, rPhase=0, ePhase=0;
const rCv=document.getElementById('radar'), rCtx=rCv.getContext('2d');
const eCv=document.getElementById('ecg-cv'), eCtx=eCv.getContext('2d');

function toggleLive() {
  isLive = !isLive;
  document.getElementById('lhint').style.display = isLive?'none':'block';
  document.getElementById('running').style.display = isLive?'block':'none';
  const dot=document.getElementById('sdot'), txt=document.getElementById('stxt');
  dot.className = isLive?'live':'';
  txt.textContent = isLive?'LIVE':'OFFLINE';
  toast(isLive?'🔴 GOING LIVE!':'⚫ Stream ended');
}

function getAccent() {
  return getComputedStyle(document.documentElement).getPropertyValue('--accent').trim();
}

function drawRadar() {
  const S=120, cx=cy=60, ctx=rCtx;
  ctx.clearRect(0,0,S,S);
  const hex=getAccent().replace('#','');
  const ar=parseInt(hex.slice(0,2),16), ag=parseInt(hex.slice(2,4),16), ab=parseInt(hex.slice(4,6),16);
  const rgba=(r,g,b,a)=>`rgba(${Math.round(r)},${Math.round(g)},${Math.round(b)},${a})`;
  const rr=50, or=57;
  const ang=(360-(rPhase*1.5)%360)%360;

  // outer ring
  ctx.beginPath(); ctx.arc(cx,cy,or,0,Math.PI*2);
  ctx.strokeStyle=rgba(ar,ag,ab,0.13); ctx.lineWidth=3; ctx.stroke();
  ctx.beginPath(); ctx.arc(cx,cy,or-2,0,Math.PI*2);
  ctx.strokeStyle=getAccent(); ctx.lineWidth=1.5; ctx.stroke();

  // disc
  ctx.beginPath(); ctx.arc(cx,cy,rr,0,Math.PI*2);
  ctx.fillStyle=rgba(ar,ag,ab,0.015); ctx.fill();

  // grid rings
  [.33,.66,1].forEach(f=>{
    ctx.beginPath(); ctx.arc(cx,cy,rr*f-1,0,Math.PI*2);
    ctx.strokeStyle=rgba(ar,ag,ab,0.055); ctx.lineWidth=1; ctx.stroke();
  });
  ctx.strokeStyle=rgba(ar,ag,ab,0.055); ctx.lineWidth=1;
  ctx.beginPath(); ctx.moveTo(cx-rr+3,cy); ctx.lineTo(cx+rr-3,cy); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(cx,cy-rr+3); ctx.lineTo(cx,cy+rr-3); ctx.stroke();

  // sweep
  const td=70, ts=45;
  for(let i=0;i<ts;i++){
    const sa=((ang+i*td/ts)*Math.PI)/180;
    const t=1-i/ts, b2=t*t*0.32;
    const xe=cx+Math.cos(sa)*(rr-2), ye=cy-Math.sin(sa)*(rr-2);
    ctx.beginPath(); ctx.moveTo(cx,cy); ctx.lineTo(xe,ye);
    ctx.strokeStyle=rgba(ar*b2+(255-ar)*b2*.4,ag*b2+(255-ag)*b2*.4,ab*b2+(255-ab)*b2*.4,b2+0.04);
    ctx.lineWidth=2.5; ctx.stroke();
  }
  // head
  for(let i=0;i<7;i++){
    const sa=((ang+i*.6)*Math.PI)/180;
    const t=1-i/7, xe=cx+Math.cos(sa)*(rr-2), ye=cy-Math.sin(sa)*(rr-2);
    ctx.beginPath(); ctx.moveTo(cx,cy); ctx.lineTo(xe,ye);
    ctx.strokeStyle=rgba(ar*t+(255-ar)*t*.4,ag*t+(255-ag)*t*.4,ab*t+(255-ab)*t*.4,t*.75);
    ctx.lineWidth=1.8; ctx.stroke();
  }
  // centre dot
  ctx.beginPath(); ctx.arc(cx,cy,2.5,0,Math.PI*2);
  ctx.fillStyle=getAccent(); ctx.fill();
  rPhase++;
}

function drawECG() {
  const W=220,H=55, ctx=eCtx;
  ctx.clearRect(0,0,W,H);
  const accent=getAccent();
  ctx.beginPath();
  for(let x=0;x<W;x++){
    const t=(x+ePhase)/18;
    const y=H/2-(Math.sin(t)*11+Math.sin(t*3.1)*3.5+(Math.abs(Math.sin(t*.65))<.05?-20:0)+(Math.abs(Math.sin(t*.65+.05))<.08?16:0));
    x===0?ctx.moveTo(x,y):ctx.lineTo(x,y);
  }
  ctx.strokeStyle=accent; ctx.lineWidth=1.8;
  ctx.shadowBlur=7; ctx.shadowColor=accent; ctx.stroke(); ctx.shadowBlur=0;
  ePhase+=2;
}

(function loop(){ drawRadar(); if(isLive) drawECG(); requestAnimationFrame(loop); })();

// Edit name
function editName() {
  const el=document.getElementById('sname');
  const cur=el.textContent.replace('✎','').trim();
  el.innerHTML=`<input id="ni" value="${cur}" style="background:var(--panel);border:1px solid var(--accent);color:var(--accent);font-family:'Bebas Neue',sans-serif;font-size:16px;text-align:center;padding:2px 5px;width:130px;"/><button onclick="saveName()" style="background:var(--accent);color:#000;border:none;cursor:pointer;padding:2px 7px;font-weight:700;font-size:10px;margin-left:3px;">✔</button>`;
  const ni=document.getElementById('ni');
  ni.focus(); ni.select();
  ni.onkeydown=e=>{if(e.key==='Enter')saveName();};
}
function saveName(){
  const ni=document.getElementById('ni');
  if(!ni)return;
  const n=ni.value.trim()||'Your Name';
  document.getElementById('sname').innerHTML=n+' <span style="color:var(--border);font-size:11px;">✎</span>';
  toast('Name: '+n);
}

// Toast
let tt;
function toast(msg){
  const t=document.getElementById('toast');
  t.textContent=msg; t.classList.add('show');
  clearTimeout(tt); tt=setTimeout(()=>t.classList.remove('show'),2200);
}
</script>
</body>
</html>"""

components.html(APP_HTML, height=820, scrolling=False)
