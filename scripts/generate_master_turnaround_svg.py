#!/usr/bin/env python3
"""
Generate Master Turnaround SVG (4-view pure vector file).
Scalable, clean SVG code with 0 hands, uniform white porcelain, and cyan glow.
"""

import os
import sys
import numpy as np

sys.path.insert(0, "/Users/richard/Developer/Stickers Uko")
from scripts.render_turnaround_master_board import extract_view_geometry

BRAIN_DIR = "/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68"
WORKSPACE_DIR = "/Users/richard/Developer/Stickers Uko"

def pts_to_svg_path(pts):
    if len(pts) < 3:
        return ""
    d = [f"M {pts[0][0]:.1f},{pts[0][1]:.1f}"]
    for p in pts[1:]:
        d.append(f"L {p[0]:.1f},{p[1]:.1f}")
    d.append("Z")
    return " ".join(d)

def generate_turnaround_svg():
    views = ["front", "three_quarter", "profile", "back"]
    geoms = {v: extract_view_geometry(v) for v in views}
    
    W = 1920
    H = 820
    col_w = W // 4
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="background-color: #0B0F17; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <!-- Cyan Glow Filter -->
    <filter id="cyanGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="6" result="blur1" />
      <feGaussianBlur stdDeviation="14" result="blur2" />
      <feMerge>
        <feMergeNode in="blur2" />
        <feMergeNode in="blur1" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <!-- Visor Horizon Specular Gradient -->
    <linearGradient id="specularArc" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.5" />
      <stop offset="50%" stop-color="#94A3B8" stop-opacity="0.2" />
      <stop offset="100%" stop-color="#000000" stop-opacity="0" />
    </linearGradient>

    <!-- Ground Shadow Radial -->
    <radialGradient id="groundShadowGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.6" />
      <stop offset="60%" stop-color="#000000" stop-opacity="0.2" />
      <stop offset="100%" stop-color="#000000" stop-opacity="0" />
    </radialGradient>

    <!-- Thruster Radial Glow -->
    </defs>

  <!-- Header Banner -->
  <rect x="0" y="0" width="{W}" height="90" fill="#0F172A" />
  <line x1="0" y1="90" x2="{W}" y2="90" stroke="#1F2937" stroke-width="2" />
  <text x="40" y="40" fill="#00F0FF" font-size="20" font-weight="700" letter-spacing="1">AITUKO — PLANCHE DE TURNAROUND DU MODELE MASTER VECTORIEL (360° MASTER)</text>
  <text x="40" y="68" fill="#94A3B8" font-size="13">Modèle Géométrique Officiel Reconstruit — 4 Vues Orthographiques Calibrées — Porcelaine Blanche Pure &amp; Zéro Main</text>

  <!-- Architectural Guides -->
  <g stroke="#00F0FF" stroke-width="1" stroke-dasharray="6,8" opacity="0.35">
    <line x1="40" y1="180" x2="{W-40}" y2="180" />
    <line x1="40" y1="265" x2="{W-40}" y2="265" stroke="#00F0FF" />
    <line x1="40" y1="360" x2="{W-40}" y2="360" stroke="#94A3B8" />
    <line x1="40" y1="550" x2="{W-40}" y2="550" stroke="#94A3B8" />
    <line x1="40" y1="645" x2="{W-40}" y2="645" stroke="#34D399" />
  </g>
  <g fill="#94A3B8" font-size="11" font-family="monospace">
    <text x="{W-180}" y="176" fill="#34D399">SOMMET CASQUE</text>
    <text x="{W-180}" y="261" fill="#00F0FF">HORIZON YEUX</text>
    <text x="{W-180}" y="356">EMBOITEMENT COU</text>
    <text x="{W-180}" y="546">BASE TORSE</text>
    <text x="{W-180}" y="641" fill="#34D399">SUSTENTATION SOL</text>
  </g>
"""

    cols_meta = [
        ("front", "0° — VUE DE FACE", "Visor 2 yeux cyan, 2 pods latéraux, 2 pieds V"),
        ("three_quarter", "45° — TROIS-QUARTS", "Visor galbé oblique, perspective yeux & pods"),
        ("profile", "90° — PROFIL", "Arc facial convexe, 1 œil profil, pod centré"),
        ("back", "180° — VUE DE DOS", "Porcelaine pure complète (zéro écran/yeux)")
    ]

    target_h = 460.0
    for i, (vname, title, desc) in enumerate(cols_meta):
        cx = i * col_w
        data = geoms[vname]
        orig_h = data["h"]
        orig_w = data["w"]
        s = target_h / orig_h
        off_x = cx + (col_w - orig_w * s) / 2.0
        off_y = 180 - 15

        def tr(pts):
            return [(round(p[0] * s + off_x, 1), round(p[1] * s + off_y, 1)) for p in pts]

        svg += f"""
  <!-- Card {title} -->
  <rect x="{cx + 15}" y="110" width="{col_w - 30}" height="{H - 135}" rx="12" fill="#111827" fill-opacity="0.8" stroke="#1F2937" />
  
  <!-- Column Banner -->
  <rect x="{cx + 25}" y="120" width="{col_w - 50}" height="38" rx="8" fill="#0F172A" stroke="{'#00F0FF' if i==0 else '#34D399'}" stroke-opacity="0.4" />
  <text x="{cx + 40}" y="144" fill="{'#00F0FF' if i==0 else '#34D399'}" font-size="13" font-weight="700">{title}</text>

  <g id="fig_{vname}">
    <!-- Ground Shadow -->
    <ellipse cx="{cx + col_w//2}" cy="650" rx="{orig_w * 0.36 * s}" ry="12" fill="url(#groundShadowGrad)" />
"""
        # Feet
        for f in data["feet"]:
            pts = tr(f)
            if len(pts) >= 3:
                fx = sum(p[0] for p in pts) / len(pts)
                fy = max(p[1] for p in pts)
                svg += f"""    <path d="{pts_to_svg_path(pts)}" fill="#FFFFFF" stroke="#D1D5DB" stroke-width="1.2" />\n"""

        # Torso
        for t in data["torso"]:
            pts = tr(t)
            if len(pts) >= 3:
                svg += f"""    <path d="{pts_to_svg_path(pts)}" fill="#FFFFFF" stroke="#D1D5DB" stroke-width="1.2" />\n"""

        # Profile/3Q pods
        if vname == "profile":
            pbox = [96 * s + off_x, 252 * s + off_y, 58 * s, 136 * s]
            pcx = pbox[0] + pbox[2] / 2
            pcy = pbox[1] + pbox[3]
            svg += f"""    <rect x="{pbox[0]:.1f}" y="{pbox[1]:.1f}" width="{pbox[2]:.1f}" height="{pbox[3]:.1f}" rx="{28*s:.1f}" fill="#FFFFFF" stroke="#D1D5DB" stroke-width="1.2" />\n"""
        elif vname == "three_quarter":
            for px_raw, py_raw, pw_raw, ph_raw in [(212, 252, 46, 133), (12, 252, 46, 133)]:
                pbox = [px_raw * s + off_x, py_raw * s + off_y, pw_raw * s, ph_raw * s]
                pcx = pbox[0] + pbox[2] / 2
                pcy = pbox[1] + pbox[3]
                svg += f"""    <rect x="{pbox[0]:.1f}" y="{pbox[1]:.1f}" width="{pbox[2]:.1f}" height="{pbox[3]:.1f}" rx="{22*s:.1f}" fill="#FFFFFF" stroke="#D1D5DB" stroke-width="1.2" />\n"""

        # Neck
        for n in data["neck"]:
            pts = tr(n)
            if len(pts) >= 3:
                svg += f"""    <path d="{pts_to_svg_path(pts)}" fill="#1E293B" />\n"""

        # Head Dome
        if len(data["head"]) >= 3:
            pts = tr(data["head"])
            svg += f"""    <path d="{pts_to_svg_path(pts)}" fill="#FFFFFF" stroke="#D1D5DB" stroke-width="1.2" />\n"""

        # Visor
        for v in data["visor"]:
            pts = tr(v)
            if len(pts) >= 3:
                svg += f"""    <path d="{pts_to_svg_path(pts)}" fill="#0C0E14" stroke="#1C212E" stroke-width="1.5" />\n"""

        # Cyan Eyes
        for e in data["eyes"]:
            pts = tr(e)
            if len(pts) >= 3:
                svg += f"""    <path d="{pts_to_svg_path(pts)}" fill="#00F0FF" filter="url(#cyanGlow)" />\n"""

        # Front/Back pods
        for p in data["pods"]:
            pts = tr(p)
            if len(pts) >= 3:
                px = sum(pt[0] for pt in pts) / len(pts)
                py = max(pt[1] for pt in pts)
                svg += f"""    <path d="{pts_to_svg_path(pts)}" fill="#FFFFFF" stroke="#D1D5DB" stroke-width="1.2" />\n"""

        svg += f"""  </g>
  <!-- Description -->
  <rect x="{cx + 25}" y="{H - 65}" width="{col_w - 50}" height="32" rx="6" fill="#0F172A" stroke="#1F2937" />
  <text x="{cx + 38}" y="{H - 44}" fill="#94A3B8" font-size="11">{desc}</text>
"""

    svg += "</svg>"

    out_svg_ws = os.path.join(WORKSPACE_DIR, "mascots/aituko/aituko_master_turnaround.svg")
    with open(out_svg_ws, "w") as f:
        f.write(svg)
    out_svg_brain = os.path.join(BRAIN_DIR, "aituko_master_turnaround.svg")
    with open(out_svg_brain, "w") as f:
        f.write(svg)
    print(f"✅ Saved Master Turnaround SVG: {out_svg_ws}")

if __name__ == "__main__":
    generate_turnaround_svg()
