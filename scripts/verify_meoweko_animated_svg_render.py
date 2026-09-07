#!/usr/bin/env python3
import os
import subprocess
import cv2
import numpy as np
from PIL import Image

from scripts.test_animated_svg_and_lottie import (
    body_pts, tail_pts, flank_l_pts, flank_r_pts, white_coat_pts,
    points_to_svg_cubic_spline
)

spline_body = points_to_svg_cubic_spline(body_pts)
spline_tail = points_to_svg_cubic_spline(tail_pts)
spline_flank_l = points_to_svg_cubic_spline(flank_l_pts)
spline_flank_r = points_to_svg_cubic_spline(flank_r_pts)
spline_white = points_to_svg_cubic_spline(white_coat_pts)

# Inner ears (smooth almond triangular recesses)
spline_ear_l = "M 176 72 C 182 85, 204 118, 215 138 C 210 142, 182 142, 172 136 C 166 122, 170 85, 176 72 Z"
spline_ear_r = "M 336 72 C 342 85, 346 122, 340 136 C 330 142, 302 142, 297 138 C 308 118, 330 85, 336 72 Z"

def build_svg(bg_mode="dark"):
    bg_rect = '<rect width="512" height="512" fill="#0B0F17" />' if bg_mode == "dark" else '<rect width="512" height="512" fill="#00FF00" />' if bg_mode == "green" else ''
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <!-- Multi-stop authentic porcelain ceramic shaders -->
    <linearGradient id="gingerCoatMaster" x1="25%" y1="15%" x2="75%" y2="85%">
      <stop offset="0%" stop-color="#F7AD63" />
      <stop offset="30%" stop-color="#EA8835" />
      <stop offset="65%" stop-color="#D26E20" />
      <stop offset="100%" stop-color="#B25010" />
    </linearGradient>

    <linearGradient id="tailGradient" x1="15%" y1="20%" x2="85%" y2="80%">
      <stop offset="0%" stop-color="#EA8835" />
      <stop offset="55%" stop-color="#CD681C" />
      <stop offset="100%" stop-color="#A54708" />
    </linearGradient>

    <radialGradient id="creamPorcelainBody" cx="50%" cy="34%" r="66%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="42%" stop-color="#FAF7F2" />
      <stop offset="78%" stop-color="#ECE5D7" />
      <stop offset="100%" stop-color="#D5C9B6" />
    </radialGradient>

    <radialGradient id="pinkEarCavityL" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#FDCABC" />
      <stop offset="45%" stop-color="#F8A796" />
      <stop offset="80%" stop-color="#E88270" />
      <stop offset="100%" stop-color="#CE5C48" />
    </radialGradient>

    <radialGradient id="pinkEarCavityR" cx="65%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#FDCABC" />
      <stop offset="45%" stop-color="#F8A796" />
      <stop offset="80%" stop-color="#E88270" />
      <stop offset="100%" stop-color="#CE5C48" />
    </radialGradient>

    <radialGradient id="amberIrisL" cx="65%" cy="65%" r="55%">
      <stop offset="0%" stop-color="#FFF066" />
      <stop offset="35%" stop-color="#E5B52B" />
      <stop offset="70%" stop-color="#9C7314" />
      <stop offset="100%" stop-color="#3A2303" />
    </radialGradient>

    <radialGradient id="amberIrisR" cx="35%" cy="65%" r="55%">
      <stop offset="0%" stop-color="#FFF066" />
      <stop offset="35%" stop-color="#E5B52B" />
      <stop offset="70%" stop-color="#9C7314" />
      <stop offset="100%" stop-color="#3A2303" />
    </radialGradient>

    <radialGradient id="chestSpecularHighlight" cx="50%" cy="30%" r="50%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.8" />
      <stop offset="50%" stop-color="#FFFFFF" stop-opacity="0.25" />
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.0" />
    </radialGradient>

    <style>
      @keyframes breathe_pos {{
        0%, 50%, 100% {{ transform: translateY(0px); }}
        25% {{ transform: translateY(2.5px); }}
        75% {{ transform: translateY(-2.5px); }}
      }}
      @keyframes breathe_scale {{
        0%, 50%, 100% {{ transform: scale(1.0, 1.0); }}
        25% {{ transform: scale(1.008, 0.992); }}
        75% {{ transform: scale(0.992, 1.008); }}
      }}
      @keyframes tail_sway {{
        0%, 100% {{ transform: rotate(-3.5deg); }}
        50% {{ transform: rotate(3.5deg); }}
      }}
      @keyframes ear_twitch {{
        0%, 38%, 52%, 100% {{ transform: rotate(0deg); }}
        42% {{ transform: rotate(-2.5deg); }}
        47% {{ transform: rotate(2.0deg); }}
      }}
      @keyframes eye_blink {{
        0%, 15%, 26%, 60%, 75%, 100% {{ transform: scaleY(1); }}
        18%, 23%, 68%, 73% {{ transform: scaleY(0.08); }}
      }}

      .anim-torso {{
        transform-box: view-box;
        transform-origin: 256px 360px;
        animation: breathe_pos 4s ease-in-out infinite, breathe_scale 4s ease-in-out infinite;
      }}
      .anim-head {{
        transform-box: view-box;
        transform-origin: 256px 200px;
        animation: ear_twitch 4s ease-in-out infinite;
      }}
      .anim-tail {{
        transform-box: view-box;
        transform-origin: 185px 445px;
        animation: tail_sway 4s ease-in-out infinite;
      }}
      .anim-eyes {{
        transform-box: view-box;
        transform-origin: 256px 172px;
        animation: eye_blink 4s cubic-bezier(0.45, 0.05, 0.55, 0.95) infinite;
      }}
    </style>
  </defs>

  {bg_rect}

  <!-- 1. Tail (Backmost layer, left swish with harmonic sway) -->
  <g class="anim-tail">
    <path d="{spline_tail}" fill="url(#tailGradient)" stroke="#92400A" stroke-width="0.9" />
  </g>

  <!-- 2. Master Silhouette Base (Ginger Ceramic Shell) -->
  <g class="anim-torso">
    <path d="{spline_body}" fill="url(#gingerCoatMaster)" stroke="#92400A" stroke-width="0.9" />

    <!-- 3. Left & Right Flank Depths (Shading separation) -->
    <path d="{spline_flank_l}" fill="url(#gingerCoatMaster)" opacity="0.95" />
    <path d="{spline_flank_r}" fill="url(#gingerCoatMaster)" opacity="0.95" />

    <!-- 4. Inner Ear Cavities (Soft Peach Porcelain) -->
    <g class="anim-head">
      <path d="{spline_ear_l}" fill="url(#pinkEarCavityL)" stroke="#BF5340" stroke-width="0.8" />
      <!-- Left Ear Tufts -->
      <path d="M 184 122 C 180 120, 175 124, 170 126" stroke="#FAF7F2" stroke-width="2.6" stroke-linecap="round" fill="none" />
      <path d="M 188 130 C 182 129, 177 132, 172 134" stroke="#FAF7F2" stroke-width="2.2" stroke-linecap="round" fill="none" />

      <path d="{spline_ear_r}" fill="url(#pinkEarCavityR)" stroke="#BF5340" stroke-width="0.8" />
      <!-- Right Ear Tufts -->
      <path d="M 328 122 C 332 120, 337 124, 342 126" stroke="#FAF7F2" stroke-width="2.6" stroke-linecap="round" fill="none" />
      <path d="M 324 130 C 330 129, 335 132, 340 134" stroke="#FAF7F2" stroke-width="2.2" stroke-linecap="round" fill="none" />

      <!-- 5. Forehead Tabby Stripes (Ginger / Amber) -->
      <path d="M 256 75 C 256 95, 256 115, 256 130" stroke="#B85210" stroke-width="7.5" stroke-linecap="round" fill="none" opacity="0.85" />
      <path d="M 235 84 C 238 102, 241 115, 244 126" stroke="#B85210" stroke-width="6.5" stroke-linecap="round" fill="none" opacity="0.8" />
      <path d="M 277 84 C 274 102, 271 115, 268 126" stroke="#B85210" stroke-width="6.5" stroke-linecap="round" fill="none" opacity="0.8" />
    </g>

    <!-- 6. White Fur Coat (Blaze, Chubby Cheeks, Muzzle, Chest, Front Legs, Paws) -->
    <path d="{spline_white}" fill="url(#creamPorcelainBody)" stroke="#C8BEAD" stroke-width="0.9" />

    <!-- Chest Curvature Specular Highlight -->
    <ellipse cx="256" cy="320" rx="38" ry="48" fill="url(#chestSpecularHighlight)" />

    <!-- Vertical Leg Divide & Paw Clefts -->
    <path d="M 256 360 C 256 395, 256 440, 256 478" stroke="#B8AC98" stroke-width="1.6" stroke-linecap="round" fill="none" opacity="0.85" />
    
    <!-- Left Paw Toes (3 rounded toes) -->
    <path d="M 209 466 C 209 476, 208 483, 207 490" stroke="#B8AC98" stroke-width="1.5" stroke-linecap="round" fill="none" />
    <path d="M 232 466 C 233 476, 234 483, 235 490" stroke="#B8AC98" stroke-width="1.5" stroke-linecap="round" fill="none" />

    <!-- Right Paw Toes (3 rounded toes) -->
    <path d="M 277 466 C 278 476, 279 483, 280 490" stroke="#B8AC98" stroke-width="1.5" stroke-linecap="round" fill="none" />
    <path d="M 300 466 C 301 476, 302 483, 303 490" stroke="#B8AC98" stroke-width="1.5" stroke-linecap="round" fill="none" />

    <!-- 7. Glassy Amber Orb Eyes (With organic blink animation) -->
    <g class="anim-eyes">
      <!-- Left Eye -->
      <g id="leftEyeGroup" transform="translate(216, 172) rotate(-3)">
        <ellipse cx="0" cy="0" rx="23" ry="25" fill="#1C1004" />
        <ellipse cx="0" cy="0" rx="21.5" ry="23.5" fill="url(#amberIrisL)" />
        <ellipse cx="1" cy="0" rx="15" ry="17" fill="#0D0702" />
        <circle cx="2" cy="-7" r="7.5" fill="#FFFFFF" />
        <circle cx="-6" cy="10" r="3.2" fill="#FFFFFF" opacity="0.65" />
      </g>

      <!-- Right Eye -->
      <g id="rightEyeGroup" transform="translate(296, 172) rotate(3)">
        <ellipse cx="0" cy="0" rx="23" ry="25" fill="#1C1004" />
        <ellipse cx="0" cy="0" rx="21.5" ry="23.5" fill="url(#amberIrisR)" />
        <ellipse cx="-1" cy="0" rx="15" ry="17" fill="#0D0702" />
        <circle cx="2" cy="-7" r="7.5" fill="#FFFFFF" />
        <circle cx="-6" cy="10" r="3.2" fill="#FFFFFF" opacity="0.65" />
      </g>
    </g>

    <!-- 8. Peach Nose & Feline Smile ω -->
    <path d="M 250 195 C 253 193, 259 193, 262 195 C 264 197, 258 203, 256 203 C 254 203, 248 197, 250 195 Z" fill="#F89D8A" stroke="#DF715C" stroke-width="0.9" />
    <path d="M 256 203 L 256 208" stroke="#8E7E6F" stroke-width="1.3" stroke-linecap="round" fill="none" />
    <path d="M 246 211 C 250 214, 253 213, 256 208 C 259 213, 262 214, 266 211" stroke="#8E7E6F" stroke-width="1.3" stroke-linecap="round" fill="none" />

    <!-- 9. Delicate Feline Whiskers -->
    <!-- Left Whiskers -->
    <path d="M 238 205 C 215 204, 192 210, 176 216" stroke="#FFFFFF" stroke-width="1.3" stroke-linecap="round" fill="none" opacity="0.92" />
    <path d="M 236 210 C 213 213, 190 222, 180 230" stroke="#FFFFFF" stroke-width="1.3" stroke-linecap="round" fill="none" opacity="0.92" />
    <path d="M 237 216 C 216 224, 198 236, 188 245" stroke="#FFFFFF" stroke-width="1.1" stroke-linecap="round" fill="none" opacity="0.85" />

    <!-- Right Whiskers -->
    <path d="M 274 205 C 297 204, 320 210, 336 216" stroke="#FFFFFF" stroke-width="1.3" stroke-linecap="round" fill="none" opacity="0.92" />
    <path d="M 276 210 C 299 213, 322 222, 332 230" stroke="#FFFFFF" stroke-width="1.3" stroke-linecap="round" fill="none" opacity="0.92" />
    <path d="M 275 216 C 296 224, 314 236, 324 245" stroke="#FFFFFF" stroke-width="1.1" stroke-linecap="round" fill="none" opacity="0.85" />
  </g>
</svg>"""
    return svg

svg_dark = build_svg("dark")
svg_trans = build_svg("transparent")
with open("scratch/meoweko_animated_test.svg", "w") as f:
    f.write(svg_dark)
print(f"✅ Saved scratch/meoweko_animated_test.svg ({len(svg_dark)/1024:.1f} KB)")

