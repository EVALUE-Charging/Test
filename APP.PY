<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>⚡ 充電嗨翻天 — 積分挑戰賽</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700;900&family=Orbitron:wght@700;900&display=swap" rel="stylesheet">
<style>
  :root {
    --neon: #00f5ff;
    --gold: #ffd700;
    --pink: #ff2d78;
    --purple: #7b2fff;
    --green: #00ff9d;
    --bg: #060614;
    --card: rgba(255,255,255,0.04);
    --border: rgba(0,245,255,0.2);
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    background: var(--bg);
    color: #fff;
    font-family: 'Noto Sans TC', sans-serif;
    min-height: 100vh;
    overflow-x: hidden;
  }

  /* Animated background */
  .bg-grid {
    position: fixed; inset: 0; z-index: 0;
    background-image:
      linear-gradient(rgba(0,245,255,0.04) 1px, transparent 1px),
      linear-gradient(90deg, rgba(0,245,255,0.04) 1px, transparent 1px);
    background-size: 60px 60px;
    animation: gridMove 20s linear infinite;
  }
  @keyframes gridMove { to { background-position: 0 60px; } }

  .orbs {
    position: fixed; inset: 0; z-index: 0; pointer-events: none;
  }
  .orb {
    position: absolute; border-radius: 50%; filter: blur(80px); opacity: 0.25;
    animation: orbFloat 8s ease-in-out infinite;
  }
  .orb1 { width: 400px; height: 400px; background: var(--purple); top: -100px; left: -100px; }
  .orb2 { width: 300px; height: 300px; background: var(--pink); top: 30%; right: -80px; animation-delay: -3s; }
  .orb3 { width: 350px; height: 350px; background: var(--neon); bottom: -100px; left: 30%; animation-delay: -6s; opacity: 0.15; }
  @keyframes orbFloat {
    0%, 100% { transform: translateY(0) scale(1); }
    50% { transform: translateY(-30px) scale(1.05); }
  }

  /* Layout */
  .wrapper { position: relative; z-index: 1; max-width: 1100px; margin: 0 auto; padding: 0 24px 60px; }

  /* Header */
  header {
    text-align: center;
    padding: 60px 0 40px;
  }
  .event-badge {
    display: inline-block;
    background: linear-gradient(135deg, var(--purple), var(--pink));
    padding: 6px 20px; border-radius: 999px;
    font-size: 13px; font-weight: 700; letter-spacing: 2px;
    text-transform: uppercase; margin-bottom: 20px;
    animation: pulse 2s ease-in-out infinite;
  }
  @keyframes pulse { 0%,100%{box-shadow:0 0 0 0 rgba(255,45,120,0.4)} 50%{box-shadow:0 0 0 12px rgba(255,45,120,0)} }

  h1 {
    font-family: 'Orbitron', monospace;
    font-size: clamp(36px, 7vw, 72px);
    font-weight: 900;
    background: linear-gradient(135deg, var(--neon), var(--purple), var(--pink));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    line-height: 1.1; margin-bottom: 12px;
    text-shadow: none;
    filter: drop-shadow(0 0 30px rgba(0,245,255,0.3));
  }
  .subtitle {
    font-size: 17px; color: rgba(255,255,255,0.6);
    letter-spacing: 1px;
  }

  /* Countdown */
  .countdown-wrap {
    display: flex; justify-content: center; gap: 16px;
    margin: 32px 0;
  }
  .countdown-box {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 16px 24px;
    text-align: center;
    backdrop-filter: blur(10px);
    min-width: 80px;
  }
  .countdown-num {
    font-family: 'Orbitron', monospace;
    font-size: 36px; font-weight: 900;
    color: var(--neon);
    display: block;
    text-shadow: 0 0 20px var(--neon);
  }
  .countdown-label { font-size: 12px; color: rgba(255,255,255,0.4); margin-top: 4px; }

  /* Main grid */
  .main-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    margin: 40px 0;
  }
  @media (max-width: 700px) { .main-grid { grid-template-columns: 1fr; } }

  /* Cards */
  .card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 28px;
    backdrop-filter: blur(12px);
    transition: transform 0.3s, border-color 0.3s;
  }
  .card:hover { transform: translateY(-4px); border-color: var(--neon); }

  .card-title {
    font-size: 13px; font-weight: 700; letter-spacing: 2px;
    text-transform: uppercase; color: var(--neon);
    margin-bottom: 20px; display: flex; align-items: center; gap: 8px;
  }
  .card-title .icon { font-size: 18px; }

  /* User panel */
  .user-info {
    display: flex; align-items: center; gap: 16px; margin-bottom: 20px;
  }
  .avatar {
    width: 56px; height: 56px; border-radius: 50%;
    background: linear-gradient(135deg, var(--purple), var(--pink));
    display: flex; align-items: center; justify-content: center;
    font-size: 24px; flex-shrink: 0;
    box-shadow: 0 0 20px rgba(123,47,255,0.5);
  }
  .user-name { font-size: 18px; font-weight: 700; }
  .user-rank { font-size: 13px; color: var(--gold); margin-top: 2px; }

  .points-display {
    background: linear-gradient(135deg, rgba(0,245,255,0.1), rgba(123,47,255,0.1));
    border: 1px solid rgba(0,245,255,0.3);
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    margin-bottom: 16px;
  }
  .points-num {
    font-family: 'Orbitron', monospace;
    font-size: 48px; font-weight: 900;
    background: linear-gradient(135deg, var(--neon), var(--green));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 0 10px rgba(0,245,255,0.5));
  }
  .points-label { font-size: 13px; color: rgba(255,255,255,0.5); margin-top: 4px; }

  /* Progress bar */
  .progress-wrap { margin-bottom: 8px; }
  .progress-label {
    display: flex; justify-content: space-between;
    font-size: 12px; color: rgba(255,255,255,0.5);
    margin-bottom: 8px;
  }
  .progress-bar {
    height: 8px; border-radius: 999px;
    background: rgba(255,255,255,0.1);
    overflow: hidden;
  }
  .progress-fill {
    height: 100%; border-radius: 999px;
    background: linear-gradient(90deg, var(--neon), var(--purple));
    width: 0%;
    transition: width 1.5s cubic-bezier(0.23,1,0.32,1);
    position: relative;
    overflow: hidden;
  }
  .progress-fill::after {
    content: '';
    position: absolute; inset: 0;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    animation: shimmer 2s linear infinite;
  }
  @keyframes shimmer { from{transform:translateX(-100%)} to{transform:translateX(100%)} }

  /* Charge button */
  .charge-btn {
    width: 100%; padding: 16px;
    background: linear-gradient(135deg, var(--neon), var(--purple));
    border: none; border-radius: 14px;
    color: #000; font-weight: 900; font-size: 18px;
    cursor: pointer; letter-spacing: 1px;
    transition: all 0.3s;
    display: flex; align-items: center; justify-content: center; gap: 8px;
    margin-top: 16px;
    font-family: 'Noto Sans TC', sans-serif;
    position: relative; overflow: hidden;
  }
  .charge-btn::before {
    content: ''; position: absolute; inset: 0;
    background: rgba(255,255,255,0.2);
    transform: translateX(-100%);
    transition: transform 0.3s;
  }
  .charge-btn:hover::before { transform: translateX(100%); }
  .charge-btn:hover { transform: scale(1.03); box-shadow: 0 0 30px rgba(0,245,255,0.5); }
  .charge-btn:active { transform: scale(0.97); }

  /* Leaderboard */
  .leaderboard-card { grid-column: 1 / -1; }

  .lb-row {
    display: flex; align-items: center; gap: 16px;
    padding: 14px 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    transition: all 0.3s;
    cursor: default;
    border-radius: 8px;
    padding-left: 8px;
  }
  .lb-row:hover { background: rgba(255,255,255,0.03); }
  .lb-row:last-child { border-bottom: none; }

  .lb-rank {
    font-family: 'Orbitron', monospace;
    font-size: 20px; font-weight: 900;
    width: 36px; text-align: center; flex-shrink: 0;
  }
  .rank-1 { color: #FFD700; text-shadow: 0 0 15px #FFD700; }
  .rank-2 { color: #C0C0C0; text-shadow: 0 0 15px #C0C0C0; }
  .rank-3 { color: #CD7F32; text-shadow: 0 0 15px #CD7F32; }
  .rank-other { color: rgba(255,255,255,0.4); font-size: 16px; }

  .lb-avatar {
    width: 44px; height: 44px; border-radius: 50%; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; font-weight: 700;
  }
  .lb-info { flex: 1; }
  .lb-name { font-size: 16px; font-weight: 700; }
  .lb-charge { font-size: 12px; color: rgba(255,255,255,0.4); margin-top: 2px; }

  .lb-bar-wrap { width: 120px; flex-shrink: 0; }
  .lb-bar {
    height: 6px; background: rgba(255,255,255,0.08);
    border-radius: 999px; overflow: hidden;
  }
  .lb-bar-fill {
    height: 100%; border-radius: 999px;
    transition: width 1s ease;
  }

  .lb-pts {
    font-family: 'Orbitron', monospace;
    font-size: 18px; font-weight: 700;
    color: var(--gold); min-width: 80px; text-align: right;
    flex-shrink: 0;
  }

  /* Prizes */
  .prizes-grid {
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px;
  }
  @media (max-width: 700px) { .prizes-grid { grid-template-columns: 1fr 1fr; } }

  .prize-item {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 20px 16px;
    text-align: center;
    transition: all 0.3s;
    cursor: pointer;
  }
  .prize-item:hover {
    border-color: var(--gold);
    background: rgba(255,215,0,0.05);
    transform: translateY(-4px);
  }
  .prize-icon { font-size: 36px; margin-bottom: 10px; }
  .prize-name { font-size: 14px; font-weight: 700; margin-bottom: 4px; }
  .prize-pts {
    font-family: 'Orbitron', monospace;
    font-size: 12px; color: var(--gold);
  }

  /* Toast */
  .toast {
    position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%) translateY(100px);
    background: linear-gradient(135deg, var(--purple), var(--pink));
    padding: 14px 28px; border-radius: 999px;
    font-weight: 700; font-size: 15px;
    z-index: 100; transition: transform 0.4s cubic-bezier(0.23,1,0.32,1);
    pointer-events: none;
    white-space: nowrap;
  }
  .toast.show { transform: translateX(-50%) translateY(0); }

  /* Sparks */
  .spark {
    position: fixed; pointer-events: none; z-index: 200;
    font-size: 24px;
    animation: sparkFloat 1s ease-out forwards;
  }
  @keyframes sparkFloat {
    0% { opacity: 1; transform: translate(0,0) scale(1); }
    100% { opacity: 0; transform: translate(var(--dx), var(--dy)) scale(0); }
  }

  /* Section divider */
  .section-full {
    margin: 0 0 24px;
  }
</style>
</head>
<body>
<div class="bg-grid"></div>
<div class="orbs">
  <div class="orb orb1"></div>
  <div class="orb orb2"></div>
  <div class="orb orb3"></div>
</div>

<div class="wrapper">
  <header>
    <div class="event-badge">⚡ 限時活動進行中</div>
    <h1>充電嗨翻天</h1>
    <p class="subtitle">每次充電 · 累積積分 · 贏得大獎</p>

    <div class="countdown-wrap">
      <div class="countdown-box">
        <span class="countdown-num" id="cd-d">07</span>
        <div class="countdown-label">天</div>
      </div>
      <div class="countdown-box">
        <span class="countdown-num" id="cd-h">14</span>
        <div class="countdown-label">時</div>
      </div>
      <div class="countdown-box">
        <span class="countdown-num" id="cd-m">32</span>
        <div class="countdown-label">分</div>
      </div>
      <div class="countdown-box">
        <span class="countdown-num" id="cd-s">09</span>
        <div class="countdown-label">秒</div>
      </div>
    </div>
  </header>

  <div class="main-grid">
    <!-- User Panel -->
    <div class="card">
      <div class="card-title"><span class="icon">👤</span> 我的帳戶</div>
      <div class="user-info">
        <div class="avatar">🦸</div>
        <div>
          <div class="user-name">陳大充</div>
          <div class="user-rank">🥇 目前排行第 3 名</div>
        </div>
      </div>

      <div class="points-display">
        <div class="points-num" id="myPoints">2,480</div>
        <div class="points-label">我的積分</div>
      </div>

      <div class="progress-wrap">
        <div class="progress-label">
          <span>距離下個獎品</span>
          <span id="progressTxt">2,480 / 3,000</span>
        </div>
        <div class="progress-bar">
          <div class="progress-fill" id="progressFill"></div>
        </div>
      </div>

      <button class="charge-btn" onclick="doCharge(this)">
        ⚡ 立即充電 +100 積分
      </button>
    </div>

    <!-- Prizes -->
    <div class="card">
      <div class="card-title"><span class="icon">🎁</span> 獎品兌換區</div>
      <div class="prizes-grid">
        <div class="prize-item" onclick="redeemPrize('咖啡兌換券', 500)">
          <div class="prize-icon">☕</div>
          <div class="prize-name">咖啡券</div>
          <div class="prize-pts">500 pts</div>
        </div>
        <div class="prize-item" onclick="redeemPrize('九折優惠碼', 800)">
          <div class="prize-icon">🏷️</div>
          <div class="prize-name">九折優惠</div>
          <div class="prize-pts">800 pts</div>
        </div>
        <div class="prize-item" onclick="redeemPrize('藍牙耳機', 3000)">
          <div class="prize-icon">🎧</div>
          <div class="prize-name">藍牙耳機</div>
          <div class="prize-pts">3,000 pts</div>
        </div>
        <div class="prize-item" onclick="redeemPrize('iPad', 8000)">
          <div class="prize-icon">📱</div>
          <div class="prize-name">iPad</div>
          <div class="prize-pts">8,000 pts</div>
        </div>
        <div class="prize-item" onclick="redeemPrize('抽獎機會', 1500)">
          <div class="prize-icon">🎰</div>
          <div class="prize-name">抽獎機會</div>
          <div class="prize-pts">1,500 pts</div>
        </div>
        <div class="prize-item" onclick="redeemPrize('神秘禮物', 2000)">
          <div class="prize-icon">🎁</div>
          <div class="prize-name">神秘禮物</div>
          <div class="prize-pts">2,000 pts</div>
        </div>
      </div>
    </div>

    <!-- Leaderboard -->
    <div class="card leaderboard-card section-full">
      <div class="card-title"><span class="icon">🏆</span> 即時排行榜 <span style="margin-left:auto;font-size:11px;color:rgba(255,255,255,0.3);letter-spacing:1px">每分鐘更新</span></div>
      <div id="leaderboard"></div>
    </div>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
const players = [
  { name: '⚡ 王閃電', emoji: '⚡', charges: 142, pts: 14200, color: 'linear-gradient(135deg,#FFD700,#FF8C00)' },
  { name: '🔥 李大充', emoji: '🔥', charges: 98, pts: 9800, color: 'linear-gradient(135deg,#ff2d78,#7b2fff)' },
  { name: '👤 陳大充', emoji: '🦸', charges: 69, pts: 6900, color: 'linear-gradient(135deg,#00f5ff,#7b2fff)', isMe: true },
  { name: '💎 林冠宇', emoji: '💎', charges: 55, pts: 5500, color: 'linear-gradient(135deg,#a78bfa,#6d28d9)' },
  { name: '🌟 張美美', emoji: '🌟', charges: 48, pts: 4800, color: 'linear-gradient(135deg,#f472b6,#ec4899)' },
  { name: '🚀 黃超速', emoji: '🚀', charges: 42, pts: 4200, color: 'linear-gradient(135deg,#34d399,#059669)' },
  { name: '🎯 劉精準', emoji: '🎯', charges: 36, pts: 3600, color: 'linear-gradient(135deg,#fbbf24,#d97706)' },
  { name: '🦋 周飛飛', emoji: '🦋', charges: 29, pts: 2900, color: 'linear-gradient(135deg,#a5f3fc,#0891b2)' },
];

let myPts = 2480;
const maxPts = players[0].pts;

function renderLeaderboard() {
  const lb = document.getElementById('leaderboard');
  lb.innerHTML = '';
  const sorted = [...players].sort((a,b) => b.pts - a.pts);
  sorted.forEach((p, i) => {
    const rank = i + 1;
    const pct = Math.round(p.pts / maxPts * 100);
    const rankClass = rank <= 3 ? `rank-${rank}` : 'rank-other';
    const rankEmoji = rank === 1 ? '👑' : rank === 2 ? '🥈' : rank === 3 ? '🥉' : rank;
    const barColor = rank === 1 ? '#FFD700' : rank === 2 ? '#C0C0C0' : rank === 3 ? '#CD7F32' : '#7b2fff';
    const rowStyle = p.isMe ? 'background:rgba(0,245,255,0.05);border-left:3px solid var(--neon);border-radius:12px;' : '';
    lb.innerHTML += `
      <div class="lb-row" style="${rowStyle}">
        <div class="lb-rank ${rankClass}">${rankEmoji}</div>
        <div class="lb-avatar" style="background:${p.color}">${p.emoji}</div>
        <div class="lb-info">
          <div class="lb-name">${p.name}${p.isMe ? ' <span style="font-size:11px;color:var(--neon);background:rgba(0,245,255,0.1);padding:2px 8px;border-radius:999px;">我</span>' : ''}</div>
          <div class="lb-charge">已充電 ${p.charges} 次</div>
        </div>
        <div class="lb-bar-wrap">
          <div class="lb-bar">
            <div class="lb-bar-fill" style="width:${pct}%;background:${barColor}"></div>
          </div>
        </div>
        <div class="lb-pts">${p.pts.toLocaleString()}</div>
      </div>`;
  });
}

function updateMyDisplay() {
  document.getElementById('myPoints').textContent = myPts.toLocaleString();
  const next = 3000;
  const pct = Math.min(myPts / next * 100, 100);
  document.getElementById('progressFill').style.width = pct + '%';
  document.getElementById('progressTxt').textContent = `${myPts.toLocaleString()} / ${next.toLocaleString()}`;
}

function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2800);
}

function spawnSparks(btn) {
  const r = btn.getBoundingClientRect();
  const emojis = ['⚡','✨','🌟','💥','⭐'];
  for (let i = 0; i < 8; i++) {
    const s = document.createElement('div');
    s.className = 'spark';
    s.textContent = emojis[Math.floor(Math.random() * emojis.length)];
    const dx = (Math.random() - 0.5) * 200;
    const dy = -(Math.random() * 150 + 50);
    s.style.cssText = `left:${r.left + r.width/2}px;top:${r.top}px;--dx:${dx}px;--dy:${dy}px;animation-delay:${Math.random()*0.3}s`;
    document.body.appendChild(s);
    setTimeout(() => s.remove(), 1200);
  }
}

function doCharge(btn) {
  btn.disabled = true;
  btn.textContent = '⏳ 充電中...';
  spawnSparks(btn);
  setTimeout(() => {
    myPts += 100;
    const meIdx = players.findIndex(p => p.isMe);
    players[meIdx].pts += 100;
    players[meIdx].charges += 1;
    updateMyDisplay();
    renderLeaderboard();
    showToast('🎉 +100 積分！繼續加油！');
    btn.disabled = false;
    btn.innerHTML = '⚡ 立即充電 +100 積分';
  }, 1200);
}

function redeemPrize(name, cost) {
  if (myPts < cost) {
    showToast(`❌ 積分不足！還差 ${(cost - myPts).toLocaleString()} 積分`);
    return;
  }
  myPts -= cost;
  const meIdx = players.findIndex(p => p.isMe);
  players[meIdx].pts -= cost;
  updateMyDisplay();
  renderLeaderboard();
  showToast(`🎁 成功兌換「${name}」！`);
}

// Countdown
const endDate = new Date();
endDate.setDate(endDate.getDate() + 7);
endDate.setHours(endDate.getHours() + 14);

function updateCountdown() {
  const now = new Date();
  const diff = endDate - now;
  if (diff <= 0) return;
  const d = Math.floor(diff / 86400000);
  const h = Math.floor((diff % 86400000) / 3600000);
  const m = Math.floor((diff % 3600000) / 60000);
  const s = Math.floor((diff % 60000) / 1000);
  document.getElementById('cd-d').textContent = String(d).padStart(2,'0');
  document.getElementById('cd-h').textContent = String(h).padStart(2,'0');
  document.getElementById('cd-m').textContent = String(m).padStart(2,'0');
  document.getElementById('cd-s').textContent = String(s).padStart(2,'0');
}

// Simulate live leaderboard changes
function liveUpdate() {
  const nonMe = players.filter(p => !p.isMe);
  const pick = nonMe[Math.floor(Math.random() * nonMe.length)];
  const gain = Math.floor(Math.random() * 3 + 1) * 100;
  pick.pts += gain;
  pick.charges += 1;
  renderLeaderboard();
}

renderLeaderboard();
updateMyDisplay();
updateCountdown();
setInterval(updateCountdown, 1000);
setInterval(liveUpdate, 5000);

// Animate progress bar on load
setTimeout(() => updateMyDisplay(), 100);
</script>
</body>
</html>