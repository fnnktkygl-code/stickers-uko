import re
from scripts.benchmark_owluko_fidelity import render_svg, evaluate_fidelity

with open("scratch/test_rwing_fix.svg") as f:
    svg = f.read()

# 1. Update Beak Gradient and Geometry
# In defs, replace beakGrad with calibrated porcelain amber
new_beak_grad = """    <!-- Beak Gradient (Porcelain Amber) -->
    <linearGradient id="beakGrad" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#D1BBA5" />
      <stop offset="35%" stop-color="#B29780" />
      <stop offset="75%" stop-color="#A08670" />
      <stop offset="100%" stop-color="#907560" />
    </linearGradient>"""
svg = re.sub(r'<!-- Beak Gradient -->\s*<linearGradient id="beakGrad".*?</linearGradient>', new_beak_grad, svg, flags=re.DOTALL)

# Remove the beak cast shadow that darkened Y=225
svg = re.sub(r'<!-- Beak Cast Shadow -->\s*<ellipse cx="256" cy="225" rx="15" ry="7" fill="#3D2B1E" opacity="0.32" />', '<!-- Beak Cast Shadow (Removed for porcelain continuity) -->', svg)

# Replace Beak path: starts at Y=172, tip at Y=207
new_beak_geom = """  <!-- 4. Beak (Porcelain Amber) -->
  <g id="beak">
    <path d="M 256 172 C 265 178, 267 194, 256 207 C 245 194, 247 178, 256 172 Z" fill="url(#beakGrad)" />
    <path d="M 256 175 C 258 184, 258 198, 256 204" stroke="#FFFFFF" stroke-width="0.8" stroke-linecap="round" opacity="0.22" fill="none" />
  </g>"""
svg = re.sub(r'<!-- 4\. Beak \(Porcelain Amber\) -->\s*<g id="beak">.*?</g>', new_beak_geom, svg, flags=re.DOTALL)

# 2. Update Feet: soften crevices and tune toe specular highlights
new_feet = """    <!-- Grounded Feet with 3 Anatomical Rounded Toes (Soft Porcelain Shading & Subtle Crevices) -->
    <g id="feet">
      <!-- Left Foot Ambient Shading -->
      <path d="M 156 455 C 156 445, 235 445, 235 455 L 235 491 L 156 491 Z" fill="#9E8876" opacity="0.25" />

      <!-- Left Foot 3 Rounded Toe Specular Highlights -->
      <ellipse cx="168" cy="474" rx="9" ry="8" fill="#E8DDD1" opacity="0.45" />
      <ellipse cx="194" cy="466" rx="11" ry="10" fill="#FFF2E6" opacity="0.55" />
      <ellipse cx="220" cy="474" rx="9" ry="8" fill="#DFD2C4" opacity="0.45" />

      <!-- Left Foot Subtle Crevices (Softened, Not Black) -->
      <path d="M 180 465 L 180 488" stroke="#8C6B4F" stroke-width="2.0" opacity="0.65" stroke-linecap="round" />
      <path d="M 206 465 L 206 488" stroke="#8C6B4F" stroke-width="2.0" opacity="0.65" stroke-linecap="round" />

      <!-- Left Foot Ground Contact Occlusion -->
      <path d="M 156 489 L 235 489" stroke="#3D2414" stroke-width="1.8" opacity="0.75" />

      <!-- Right Foot Ambient Shading -->
      <path d="M 276 455 C 276 445, 353 445, 353 455 L 353 491 L 276 491 Z" fill="#755E4C" opacity="0.30" />

      <!-- Right Foot 3 Rounded Toe Specular Highlights -->
      <ellipse cx="290" cy="474" rx="8" ry="7" fill="#C4B09C" opacity="0.35" />
      <ellipse cx="317" cy="466" rx="10" ry="9" fill="#D9C6B4" opacity="0.45" />
      <ellipse cx="341" cy="474" rx="8" ry="7" fill="#C8B5A2" opacity="0.35" />

      <!-- Right Foot Subtle Crevices (Softened, Not Black) -->
      <path d="M 304 465 L 304 488" stroke="#5C4230" stroke-width="2.0" opacity="0.65" stroke-linecap="round" />
      <path d="M 330 465 L 330 488" stroke="#5C4230" stroke-width="2.0" opacity="0.65" stroke-linecap="round" />

      <!-- Right Foot Ground Contact Occlusion -->
      <path d="M 276 489 L 354 489" stroke="#2D1A0E" stroke-width="1.8" opacity="0.80" />
    </g>"""
svg = re.sub(r'<!-- Grounded Feet with 3 Anatomical Rounded Toes.*?<!-- Right Foot Ground Contact Occlusion -->\s*<path d="M 276 490 L 354 490"[^>]+/>\s*</g>', new_feet, svg, flags=re.DOTALL)

# 3. Update Eyes: Pupil centered higher at Y=149/151 with smaller vertical radius ry=8.5/9.0
new_pupil_grad = """    <!-- Pupil Gradient -->
    <radialGradient id="pupilGrad" cx="50%" cy="45%" r="60%">
      <stop offset="0%" stop-color="#1C0E05" />
      <stop offset="70%" stop-color="#2D1A0E" />
      <stop offset="100%" stop-color="#462C1C" stop-opacity="0.9" />
    </radialGradient>"""
svg = re.sub(r'<!-- Pupil -->\s*<radialGradient id="pupilGrad".*?</radialGradient>', new_pupil_grad, svg, flags=re.DOTALL)

# Update eye groups
new_eyes = """  <!-- 3. Eye Sockets & Amber Eyes (Elliptical Anatomic Aperture) -->
  <!-- Left Eye -->
  <g id="left_eye">
    <!-- Brow Crevice / Socket Rim -->
    <ellipse cx="196" cy="158" rx="27" ry="19.5" fill="#3D2817" opacity="0.65" />
    <ellipse cx="196" cy="158" rx="25" ry="18" fill="#1C0C02" />
    <!-- Amber Iris -->
    <ellipse cx="196" cy="158" rx="24" ry="17" fill="url(#amberEyeL)" />
    <!-- Pupil (Centered higher, leaving amber lower crescent open) -->
    <ellipse cx="198" cy="149" rx="16" ry="9" fill="url(#pupilGrad)" />
  </g>

  <!-- Right Eye -->
  <g id="right_eye">
    <!-- Brow Crevice / Socket Rim -->
    <ellipse cx="308" cy="159" rx="28.5" ry="19.5" fill="#301A0D" opacity="0.75" />
    <ellipse cx="308" cy="159" rx="26.5" ry="18" fill="#180A02" />
    <!-- Amber Iris -->
    <ellipse cx="308" cy="159" rx="25.5" ry="17" fill="url(#amberEyeR)" />
    <!-- Pupil (Centered higher, leaving amber lower crescent open) -->
    <ellipse cx="306" cy="151" rx="16.5" ry="9.5" fill="url(#pupilGrad)" />
  </g>"""
svg = re.sub(r'<!-- 3\. Eye Sockets & Amber Eyes.*?<!-- Right Eye -->\s*<g id="right_eye">.*?</g>', new_eyes, svg, flags=re.DOTALL)

with open("scratch/test_calibrated_v2.svg", "w") as f:
    f.write(svg)

rendered = render_svg("scratch/test_calibrated_v2.svg", "scratch/test_calibrated_v2.png")
results = evaluate_fidelity(rendered, title="AUDIT: test_calibrated_v2.svg")
