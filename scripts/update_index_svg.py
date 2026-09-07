import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update CSS Animations in index.html
old_css_pattern = r'/\* ==========================================================================\s+AITUKO ORGANIC VECTOR RIG KINEMATICS.*?\.aituko-eyes-glow \{[^}]+\}'
new_css = '''/* ==========================================================================
       AITUKO ORGANIC VECTOR RIG KINEMATICS (Exact 4.0s Harmonic 3D Motion)
       ========================================================================== */
    @keyframes aitukoTorsoFloat {
      0%, 100% { transform: translate3d(0, 0px, 0); }
      25% { transform: translate3d(0, -18px, 0); }
      50% { transform: translate3d(0, 0px, 0); }
      75% { transform: translate3d(0, 16px, 0); }
    }
    @keyframes aitukoHeadBob {
      0%, 100% { transform: translate3d(0, 0px, 0) rotate(0deg); }
      28% { transform: translate3d(0, -18px, 0) rotate(-2.2deg); }
      50% { transform: translate3d(0, 0px, 0) rotate(0deg); }
      78% { transform: translate3d(0, 16px, 0) rotate(2.0deg); }
    }
    @keyframes aitukoLeftArmHover {
      0%, 100% { transform: translate(132px, 333px) rotate(-7deg); }
      27% { transform: translate(126px, 315px) rotate(-12deg); }
      50% { transform: translate(132px, 333px) rotate(-7deg); }
      75% { transform: translate(134px, 349px) rotate(-5deg); }
    }
    @keyframes aitukoRightArmHover {
      0%, 100% { transform: translate(380px, 333px) rotate(7deg); }
      27% { transform: translate(386px, 315px) rotate(12deg); }
      50% { transform: translate(380px, 333px) rotate(7deg); }
      75% { transform: translate(378px, 349px) rotate(5deg); }
    }
    @keyframes aitukoPodsHover {
      0%, 100% { transform: translate3d(0, 0px, 0); }
      28% { transform: translate3d(0, -18px, 0); }
      50% { transform: translate3d(0, 0px, 0); }
      78% { transform: translate3d(0, 16px, 0); }
    }
    @keyframes aitukoShadowBreathe {
      0%, 100% { transform: scale(1); opacity: 0.80; }
      25% { transform: scale(0.82); opacity: 0.55; }
      50% { transform: scale(1); opacity: 0.80; }
      75% { transform: scale(1.08); opacity: 0.98; }
    }
    @keyframes aitukoEyeBlink {
      0%, 65%, 72%, 100% { transform: scaleY(1); }
      67% { transform: scaleY(0.08); }
      70% { transform: scaleY(0.15); }
    }
    @keyframes aitukoGlowPulse {
      0%, 100% { opacity: 0.90; filter: drop-shadow(0 0 8px #00F0FF); }
      50% { opacity: 1.0; filter: drop-shadow(0 0 14px #00F0FF) drop-shadow(0 0 20px rgba(0, 240, 255, 0.5)); }
    }

    .aituko-torso-anim {
      animation: aitukoTorsoFloat 4s cubic-bezier(0.42, 0, 0.58, 1) infinite;
      transform-box: view-box;
      transform-origin: 256px 315px;
    }
    .aituko-head-anim {
      animation: aitukoHeadBob 4s cubic-bezier(0.42, 0, 0.58, 1) infinite;
      transform-box: view-box;
      transform-origin: 256px 183px;
    }
    .aituko-left-arm-anim {
      animation: aitukoLeftArmHover 4s cubic-bezier(0.42, 0, 0.58, 1) infinite;
      transform-box: view-box;
      transform-origin: 132px 283px;
    }
    .aituko-right-arm-anim {
      animation: aitukoRightArmHover 4s cubic-bezier(0.42, 0, 0.58, 1) infinite;
      transform-box: view-box;
      transform-origin: 380px 283px;
    }
    .aituko-pods-anim {
      animation: aitukoPodsHover 4s cubic-bezier(0.42, 0, 0.58, 1) infinite;
      transform-box: view-box;
      transform-origin: 256px 479px;
    }
    .aituko-shadow-anim {
      animation: aitukoShadowBreathe 4s cubic-bezier(0.42, 0, 0.58, 1) infinite;
      transform-box: view-box;
      transform-origin: 256px 495px;
    }
    .aituko-eyes-blink {
      animation: aitukoEyeBlink 4s ease-in-out infinite;
      transform-box: view-box;
      transform-origin: 256px 99px;
    }
    .aituko-eyes-glow {
      animation: aitukoGlowPulse 4s ease-in-out infinite;
    }'''

match = re.search(old_css_pattern, content, re.DOTALL)
if match:
    content = content[:match.start()] + new_css + content[match.end():]
    print("✅ CSS animations updated in index.html")
else:
    print("⚠️ CSS pattern not found")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
