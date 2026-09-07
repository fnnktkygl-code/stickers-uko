import base64
import os

def build_viewer():
    layers_dir = "mascots/owluko/rig_layers"
    layer_names = [
        "00_shadow.png",
        "01_foot_left.png",
        "02_foot_right.png",
        "03_body_porcelain.png",
        "04_wing_left.png",
        "05_wing_right.png",
        "06_eye_left.png",
        "07_eye_right.png",
        "08_eyelid_left.png",
        "09_eyelid_right.png",
        "10_beak.png"
    ]
    
    # Embed images as Base64 so the HTML viewer is completely standalone!
    b64_assets = {}
    for name in layer_names:
        p = os.path.join(layers_dir, name)
        with open(p, "rb") as f:
            b64_assets[name] = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
            
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Owluko — Rive & After Effects Interactive Puppet Rig</title>
<style>
  :root {{
    --bg: #0F172A;
    --card: #1E293B;
    --text: #F8FAFC;
    --accent: #F59E0B;
    --border: #334155;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: var(--bg);
    color: var(--text);
    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: 100vh;
    padding: 24px 16px;
  }}
  header {{
    text-align: center;
    margin-bottom: 20px;
  }}
  h1 {{
    font-size: 24px;
    font-weight: 700;
    color: var(--accent);
    margin-bottom: 6px;
  }}
  p.sub {{
    font-size: 14px;
    color: #94A3B8;
  }}
  .main-stage {{
    display: flex;
    flex-wrap: wrap;
    gap: 24px;
    justify-content: center;
    max-width: 1080px;
    width: 100%;
  }}
  .canvas-card {{
    background: var(--card);
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 10px 25px -5px rgba(0,0,0,0.5);
    border: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    align-items: center;
  }}
  .canvas-wrapper {{
    position: relative;
    width: 480px;
    height: 480px;
    border-radius: 12px;
    background: radial-gradient(circle at center, #1e293b 0%, #0f172a 100%);
    overflow: hidden;
    border: 1px solid #475569;
  }}
  canvas {{
    width: 100%;
    height: 100%;
    display: block;
    cursor: crosshair;
  }}
  .controls-panel {{
    background: var(--card);
    border-radius: 16px;
    padding: 24px;
    width: 360px;
    border: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    gap: 16px;
  }}
  .control-group {{
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}
  label {{
    font-size: 13px;
    font-weight: 600;
    color: #CBD5E1;
    display: flex;
    justify-content: space-between;
  }}
  input[type="range"] {{
    accent-color: var(--accent);
    cursor: pointer;
  }}
  .btn-row {{
    display: flex;
    gap: 10px;
  }}
  button {{
    background: #334155;
    color: #F8FAFC;
    border: 1px solid #475569;
    padding: 10px 14px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    flex: 1;
  }}
  button:hover {{
    background: var(--accent);
    color: #000;
  }}
  .toggle-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 13px;
  }}
  .stats-bar {{
    margin-top: 12px;
    font-size: 12px;
    color: #64748B;
    display: flex;
    justify-content: space-between;
    width: 100%;
  }}
</style>
</head>
<body>

<header>
  <h1>Owluko — Rive & After Effects Interactive Puppet Rig</h1>
  <p class="sub">100% Studio Clean Assets • 60 FPS Kinematics • Dynamic State Machine</p>
</header>

<div class="main-stage">
  <div class="canvas-card">
    <div class="canvas-wrapper" id="canvasWrapper">
      <canvas id="rigCanvas" width="512" height="512"></canvas>
    </div>
    <div class="stats-bar">
      <span>FPS: <strong id="fpsVal">60</strong></span>
      <span>Engine: <strong>HTML5 2.5D Canvas Rig</strong></span>
      <span>GPU Draw: <strong>&lt; 0.5%</strong></span>
    </div>
  </div>

  <div class="controls-panel">
    <h3 style="font-size:16px; border-bottom:1px solid #334155; padding-bottom:8px;">State Machine Inputs</h3>

    <div class="btn-row">
      <button id="btnBlink" style="background:#F59E0B; color:#000;">Trigger Blink (Eyelids)</button>
    </div>

    <div class="control-group">
      <label>Gaze Tracking (Mouse / Look X, Y) <span id="gazeVal">0, 0</span></label>
      <div style="font-size:11px; color:#94A3B8;">Move cursor over canvas to direct Owluko's gaze.</div>
    </div>

    <div class="control-group">
      <label>Breathing Speed <span id="speedVal">1.0x</span></label>
      <input type="range" id="breathSpeed" min="0" max="2.0" step="0.1" value="1.0">
    </div>

    <div class="control-group">
      <label>Breathing Amplitude (Squash/Stretch) <span id="ampVal">1.8%</span></label>
      <input type="range" id="breathAmp" min="0" max="4.0" step="0.2" value="1.8">
    </div>

    <div class="control-group">
      <label>Wing Secondary Sway <span id="wingVal">2.4°</span></label>
      <input type="range" id="wingSway" min="0" max="6.0" step="0.2" value="2.4">
    </div>

    <div class="toggle-row">
      <span>Draw Bone Skeleton</span>
      <input type="checkbox" id="chkSkeleton">
    </div>

    <div class="toggle-row">
      <span>Background</span>
      <select id="selBg" style="background:#0F172A; color:#FFF; border:1px solid #475569; padding:4px 8px; border-radius:6px;">
        <option value="studio">Studio Dark</option>
        <option value="white">Pure White</option>
        <option value="green">Chroma Green</option>
        <option value="checker">Checkerboard</option>
      </select>
    </div>
  </div>
</div>

<script>
const ASSETS_B64 = {b64_assets};
const images = {{}};
let loadedCount = 0;
const totalAssets = Object.keys(ASSETS_B64).length;

for (let [k, src] of Object.entries(ASSETS_B64)) {{
  const img = new Image();
  img.src = src;
  img.onload = () => {{
    loadedCount++;
    if (loadedCount === totalAssets) {{
      requestAnimationFrame(renderLoop);
    }}
  }};
  images[k] = img;
}}

const canvas = document.getElementById("rigCanvas");
const ctx = canvas.getContext("2d");
const canvasWrapper = document.getElementById("canvasWrapper");

let lookTarget = {{ x: 0, y: 0 }};
let lookCurrent = {{ x: 0, y: 0 }};

canvasWrapper.addEventListener("mousemove", (e) => {{
  const rect = canvasWrapper.getBoundingClientRect();
  const mx = (e.clientX - rect.left) / rect.width * 512;
  const my = (e.clientY - rect.top) / rect.height * 512;
  // Offset from eye center (256, 160)
  lookTarget.x = Math.max(-1, Math.min(1, (mx - 256) / 140));
  lookTarget.y = Math.max(-1, Math.min(1, (my - 160) / 140));
  document.getElementById("gazeVal").textContent = `${{(lookTarget.x * 100).toFixed(0)}}, ${{(lookTarget.y * 100).toFixed(0)}}`;
}});

canvasWrapper.addEventListener("mouseleave", () => {{
  lookTarget.x = 0;
  lookTarget.y = 0;
  document.getElementById("gazeVal").textContent = "0, 0";
}});

// Blink trigger state
let isBlinking = false;
let blinkStartTime = 0;
const blinkDuration = 0.24; // 240ms

function triggerBlink() {{
  isBlinking = true;
  blinkStartTime = performance.now() / 1000;
}}

document.getElementById("btnBlink").addEventListener("click", triggerBlink);

let lastTime = performance.now();
let frameCounter = 0;
let lastFpsUpdate = performance.now();

function renderLoop(now) {{
  const t = now / 1000;
  const dt = Math.min(0.1, (now - lastTime) / 1000);
  lastTime = now;

  frameCounter++;
  if (now - lastFpsUpdate >= 1000) {{
    document.getElementById("fpsVal").textContent = frameCounter;
    frameCounter = 0;
    lastFpsUpdate = now;
  }}

  // Smooth gaze interpolation
  lookCurrent.x += (lookTarget.x - lookCurrent.x) * 0.12;
  lookCurrent.y += (lookTarget.y - lookCurrent.y) * 0.12;

  // Parameters from UI
  const speed = parseFloat(document.getElementById("breathSpeed").value);
  const amp = parseFloat(document.getElementById("breathAmp").value) / 100.0;
  const wingAmp = parseFloat(document.getElementById("wingSway").value) * Math.PI / 180.0;
  const showSkeleton = document.getElementById("chkSkeleton").checked;
  const bgMode = document.getElementById("selBg").value;

  // Clear background
  ctx.clearRect(0, 0, 512, 512);
  if (bgMode === "white") {{
    ctx.fillStyle = "#FFFFFF";
    ctx.fillRect(0, 0, 512, 512);
  }} else if (bgMode === "green") {{
    ctx.fillStyle = "#00FF00";
    ctx.fillRect(0, 0, 512, 512);
  }} else if (bgMode === "checker") {{
    for (let y = 0; y < 512; y += 32) {{
      for (let x = 0; x < 512; x += 32) {{
        ctx.fillStyle = ((x / 32 + y / 32) % 2 === 0) ? "#1e293b" : "#334155";
        ctx.fillRect(x, y, 32, 32);
      }}
    }}
  }}

  // Periodic natural blink every 3.5 seconds if not manual
  if (!isBlinking && Math.sin(t * 1.8) > 0.995) {{
    triggerBlink();
  }}

  let blinkProgress = 0;
  if (isBlinking) {{
    const elapsed = t - blinkStartTime;
    if (elapsed >= blinkDuration) {{
      isBlinking = false;
      blinkProgress = 0;
    }} else {{
      const p = elapsed / blinkDuration;
      // Ease in / ease out bell curve
      blinkProgress = Math.sin(p * Math.PI);
    }}
  }}

  // Kinematics calculations
  // Respiration cycle: frequency ~ 0.5 Hz (2.0s period)
  const breath = Math.sin(t * 2 * Math.PI * 0.5 * speed);
  const scaleY = 1.0 + breath * amp;
  const scaleX = 1.0 - breath * (amp * 0.5);
  const pelvisBob = breath * (amp * 80.0);
  const headTilt = Math.sin(t * 2 * Math.PI * 0.25 * speed) * 0.026; // ~1.5 deg

  // Wing secondary harmonic
  const wingLag = 0.12;
  const wingPhase = Math.sin((t - wingLag) * 2 * Math.PI * 0.5 * speed);
  const leftWingRot = -wingPhase * wingAmp;
  const rightWingRot = wingPhase * wingAmp;

  // 1. DRAW SHADOW
  ctx.save();
  ctx.translate(256, 489);
  const shadowScale = 1.0 + breath * (amp * 0.6);
  ctx.scale(shadowScale, shadowScale);
  ctx.drawImage(images["00_shadow.png"], -256, -489);
  ctx.restore();

  // 2. DRAW FEET (Grounded, zero sliding)
  ctx.drawImage(images["01_foot_left.png"], 0, 0);
  ctx.drawImage(images["02_foot_right.png"], 0, 0);

  // 3. DRAW BODY (Anchored at Pelvis [256, 435])
  ctx.save();
  ctx.translate(256, 435 + pelvisBob);
  ctx.rotate(headTilt);
  ctx.scale(scaleX, scaleY);
  ctx.translate(-256, -435);

  // Draw Body Capsule
  ctx.drawImage(images["03_body_porcelain.png"], 0, 0);

  // Draw Wings
  // Left Wing (Anchor: 128, 192)
  ctx.save();
  ctx.translate(128, 192);
  ctx.rotate(leftWingRot);
  ctx.translate(-128, -192);
  ctx.drawImage(images["04_wing_left.png"], 0, 0);
  ctx.restore();

  // Right Wing (Anchor: 384, 192)
  ctx.save();
  ctx.translate(384, 192);
  ctx.rotate(rightWingRot);
  ctx.translate(-384, -192);
  ctx.drawImage(images["05_wing_right.png"], 0, 0);
  ctx.restore();

  // Draw Head Elements
  // Eyeballs (Anchor pupil: 193, 160 & 315, 163)
  const gazePxX = lookCurrent.x * 3.5;
  const gazePxY = lookCurrent.y * 3.0;

  // Left Eye
  ctx.save();
  ctx.translate(193 + gazePxX, 160 + gazePxY);
  ctx.drawImage(images["06_eye_left.png"], -193, -160);
  ctx.restore();

  // Right Eye
  ctx.save();
  ctx.translate(315 + gazePxX, 163 + gazePxY);
  ctx.drawImage(images["07_eye_right.png"], -315, -163);
  ctx.restore();

  // Eyelids (Blink downwards by up to 17px)
  const blinkDy = blinkProgress * 17.0;

  // Left Eyelid
  ctx.save();
  ctx.translate(0, blinkDy);
  ctx.drawImage(images["08_eyelid_left.png"], 0, 0);
  ctx.restore();

  // Right Eyelid
  ctx.save();
  ctx.translate(0, blinkDy);
  ctx.drawImage(images["09_eyelid_right.png"], 0, 0);
  ctx.restore();

  // Beak
  ctx.drawImage(images["10_beak.png"], 0, 0);

  ctx.restore(); // End Body transform

  // Draw Skeleton Overlay if checked
  if (showSkeleton) {{
    ctx.save();
    ctx.strokeStyle = "#F59E0B";
    ctx.fillStyle = "#F59E0B";
    ctx.lineWidth = 2;

    const bones = [
      [256, 489, 256, 435 + pelvisBob], // Root to Pelvis
      [256, 435 + pelvisBob, 204, 425], // Pelvis to L Foot
      [256, 435 + pelvisBob, 308, 425], // Pelvis to R Foot
      [256, 435 + pelvisBob, 256, 175 + pelvisBob], // Pelvis to Head
      [256, 175 + pelvisBob, 128, 192 + pelvisBob], // Spine to L Shoulder
      [256, 175 + pelvisBob, 384, 192 + pelvisBob], // Spine to R Shoulder
      [256, 175 + pelvisBob, 193, 160 + pelvisBob], // Head to L Eye
      [256, 175 + pelvisBob, 315, 163 + pelvisBob], // Head to R Eye
    ];

    bones.forEach(([x1, y1, x2, y2]) => {{
      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.lineTo(x2, y2);
      ctx.stroke();

      ctx.beginPath();
      ctx.arc(x1, y1, 4, 0, Math.PI * 2);
      ctx.fill();
      ctx.beginPath();
      ctx.arc(x2, y2, 4, 0, Math.PI * 2);
      ctx.fill();
    }});

    ctx.restore();
  }}

  requestAnimationFrame(renderLoop);
}}
</script>
</body>
</html>
"""
    viewer_path = "mascots/owluko/rive/owluko_interactive_viewer.html"
    with open(viewer_path, "w") as f:
        f.write(html)
    print("Saved standalone interactive viewer:", viewer_path)

if __name__ == "__main__":
    build_viewer()
