import os, subprocess
import cv2, numpy as np
from PIL import Image, ImageDraw

def generate_flawless_meoweko_svg(bg_mode="dark"):
    bg_fill = "#0B0F17" if bg_mode == "dark" else "#00FF00" if bg_mode == "green" else "transparent"
    bg_rect = f'<rect width="512" height="512" fill="{bg_fill}" />' if bg_fill != "transparent" else ""

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <!-- Ceramic porcelain ginger coat gradients -->
    <linearGradient id="gingerBody" x1="30%" y1="10%" x2="70%" y2="90%">
      <stop offset="0%" stop-color="#F8B16A" />
      <stop offset="28%" stop-color="#EC8E3E" />
      <stop offset="68%" stop-color="#D37120" />
      <stop offset="100%" stop-color="#AA4808" />
    </linearGradient>

    <!-- Seamless tubular tail gradient -->
    <linearGradient id="gingerTail" x1="10%" y1="30%" x2="90%" y2="70%">
      <stop offset="0%" stop-color="#F5A358" />
      <stop offset="40%" stop-color="#DB7926" />
      <stop offset="80%" stop-color="#B2500E" />
      <stop offset="100%" stop-color="#803004" />
    </linearGradient>

    <!-- White porcelain ceramic gradients -->
    <radialGradient id="whiteCoatGrad" cx="50%" cy="32%" r="68%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="45%" stop-color="#FAF7F2" />
      <stop offset="78%" stop-color="#EDE6D9" />
      <stop offset="100%" stop-color="#DACFBE" />
    </radialGradient>

    <!-- Chubby cheeks porcelain glow -->
    <radialGradient id="cheekLGrad" cx="35%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.9" />
      <stop offset="50%" stop-color="#FAF7F2" stop-opacity="0.6" />
      <stop offset="100%" stop-color="#FAF7F2" stop-opacity="0.0" />
    </radialGradient>

    <radialGradient id="cheekRGrad" cx="65%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.9" />
      <stop offset="50%" stop-color="#FAF7F2" stop-opacity="0.6" />
      <stop offset="100%" stop-color="#FAF7F2" stop-opacity="0.0" />
    </radialGradient>

    <!-- Inner ear pink cavities with ambient depth -->
    <radialGradient id="earCavityL" cx="40%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#FDCABC" />
      <stop offset="45%" stop-color="#F7A594" />
      <stop offset="80%" stop-color="#E57D6B" />
      <stop offset="100%" stop-color="#C5503C" />
    </radialGradient>

    <radialGradient id="earCavityR" cx="60%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#FDCABC" />
      <stop offset="45%" stop-color="#F7A594" />
      <stop offset="80%" stop-color="#E57D6B" />
      <stop offset="100%" stop-color="#C5503C" />
    </radialGradient>

    <!-- Glassy amber orb iris -->
    <radialGradient id="amberIrisL" cx="62%" cy="65%" r="58%">
      <stop offset="0%" stop-color="#FFF36D" />
      <stop offset="35%" stop-color="#E9B726" />
      <stop offset="70%" stop-color="#9E6910" />
      <stop offset="100%" stop-color="#381F02" />
    </radialGradient>

    <radialGradient id="amberIrisR" cx="38%" cy="65%" r="58%">
      <stop offset="0%" stop-color="#FFF36D" />
      <stop offset="35%" stop-color="#E9B726" />
      <stop offset="70%" stop-color="#9E6910" />
      <stop offset="100%" stop-color="#381F02" />
    </radialGradient>

    <!-- Nose coral/peach -->
    <linearGradient id="noseGrad" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#F9A49A" />
      <stop offset="100%" stop-color="#E8786B" />
    </linearGradient>

    <!-- Torso highlight -->
    <radialGradient id="chestHighlight" cx="50%" cy="30%" r="50%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.85" />
      <stop offset="50%" stop-color="#FFFFFF" stop-opacity="0.25" />
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.0" />
    </radialGradient>

    <!-- Flank gradients -->
    <radialGradient id="flankL" cx="35%" cy="50%" r="65%">
      <stop offset="0%" stop-color="#F9AE66" />
      <stop offset="55%" stop-color="#DF7E2C" />
      <stop offset="100%" stop-color="#A84B0A" />
    </radialGradient>

    <radialGradient id="flankR" cx="65%" cy="50%" r="65%">
      <stop offset="0%" stop-color="#F9AE66" />
      <stop offset="55%" stop-color="#DF7E2C" />
      <stop offset="100%" stop-color="#A84B0A" />
    </radialGradient>

    <!-- Paw toe 3D gradient -->
    <linearGradient id="toeGrad" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="70%" stop-color="#FAF7F2" />
      <stop offset="100%" stop-color="#E4DACB" />
    </linearGradient>

    <!-- Animation keyframes -->
    <style>
      @keyframes breathe_pos {{
        0%, 50%, 100% {{ transform: translateY(0px); }}
        25% {{ transform: translateY(2.0px); }}
        75% {{ transform: translateY(-2.0px); }}
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
        42% {{ transform: rotate(-2.2deg); }}
        47% {{ transform: rotate(1.8deg); }}
      }}
      @keyframes eye_blink {{
        0%, 15%, 26%, 60%, 75%, 100% {{ transform: scaleY(1); }}
        18%, 23%, 68%, 73% {{ transform: scaleY(0.08); }}
      }}

      .anim-torso {{
        transform-box: view-box;
        transform-origin: 271.5px 360px;
        animation: breathe_pos 4s ease-in-out infinite, breathe_scale 4s ease-in-out infinite;
      }}
      .anim-head {{
        transform-box: view-box;
        transform-origin: 271.5px 180px;
        animation: ear_twitch 4s ease-in-out infinite;
      }}
      .anim-tail {{
        transform-box: view-box;
        transform-origin: 185px 445px;
        animation: tail_sway 4s ease-in-out infinite;
      }}
      .anim-eyes {{
        transform-box: view-box;
        transform-origin: 271.5px 171.5px;
        animation: eye_blink 4s cubic-bezier(0.45, 0.05, 0.55, 0.95) infinite;
      }}
    </style>
  </defs>

  {bg_rect}

  <!-- 1. Tail: Single seamless tubular curved path with rounded tip -->
  <g class="anim-tail">
    <path d="M 185 438 C 158 440, 134 446, 122 458 C 115 466, 115 476, 126 480 C 138 484, 158 476, 175 464 C 188 454, 194 446, 198 440 C 188 425, 172 414, 155 414 C 138 414, 124 425, 120 440 C 117 452, 124 458, 128 456 C 136 440, 150 430, 166 430 C 174 430, 180 434, 185 438 Z" fill="url(#gingerTail)" stroke="#803004" stroke-width="0.8" />
  </g>

  <!-- 2. Master Body Shell (Ginger porcelain silhouette) -->
  <g class="anim-torso">
    <!-- Outer silhouette matching 3D reference landmarks -->
    <!-- Left ear: apex at (167, 41) -->
    <!-- Crown: (210, 75) to (271.5, 71) to (330, 75) -->
    <!-- Right ear: apex at (376, 41) -->
    <!-- Outer temples & cheeks: (390, 85) -> (385, 185) -> (370, 235) -->
    <!-- Neck: (337, 260) -->
    <!-- Right flank: (351, 340) -> (373, 400) -> (360, 465) -> (336, 490) -->
    <!-- Base paws: Y=490 -->
    <!-- Left flank: (207, 490) -> (174, 450) -> (169, 400) -> (192, 340) -->
    <!-- Neck: (207, 260) -->
    <!-- Left cheek & temple: (173, 235) -> (159, 185) -> (152, 85) -> (167, 41) -->
    <path d="M 167 41 C 158 58, 153 75, 152 85 C 150 110, 154 140, 159 185 C 162 212, 166 226, 173 235 C 184 250, 196 256, 207 260 C 196 285, 192 315, 192 340 C 185 365, 172 385, 169 400 C 164 425, 166 445, 174 460 C 184 478, 196 488, 207 490 L 336 490 C 347 488, 359 478, 365 465 C 375 445, 377 425, 373 400 C 370 385, 358 365, 351 340 C 351 315, 347 285, 337 260 C 348 256, 360 250, 370 235 C 377 226, 381 212, 385 185 C 389 140, 393 110, 390 85 C 389 75, 384 58, 376 41 C 362 55, 340 68, 330 75 C 310 72, 290 71, 271.5 71 C 253 71, 233 72, 210 75 C 200 68, 181 55, 167 41 Z" fill="url(#gingerBody)" stroke="#883404" stroke-width="0.8" />

    <!-- 3. Left & Right Flank Depth Shading -->
    <!-- Left Flank -->
    <path d="M 192 340 C 185 365, 172 385, 169 400 C 164 425, 166 445, 174 460 C 184 478, 196 488, 207 490 L 236 490 C 238 460, 238 430, 234 395 C 230 365, 222 345, 212 330 Z" fill="url(#flankL)" opacity="0.92" />
    <!-- Right Flank -->
    <path d="M 351 340 C 358 365, 370 385, 373 400 C 377 425, 375 445, 365 465 C 359 478, 347 488, 336 490 L 307 490 C 305 460, 305 430, 309 395 C 313 365, 321 345, 331 330 Z" fill="url(#flankR)" opacity="0.92" />

    <!-- 4. Inner Ear Cavities with Sculpted Tufts -->
    <g class="anim-head">
      <!-- Left Inner Ear Cavity -->
      <path d="M 169 49 C 160 70, 160 95, 166 120 C 174 128, 186 122, 196 100 C 204 82, 198 65, 192 58 Z" fill="url(#earCavityL)" stroke="#B64534" stroke-width="0.8" />
      <!-- Left Ear Tufts (3 soft sculpted porcelain tufts) -->
      <path d="M 170 98 C 176 100, 183 96, 189 92 C 184 98, 178 104, 169 106" fill="#FAF7F2" stroke="#FAF7F2" stroke-width="0.5" />
      <path d="M 168 108 C 174 110, 181 106, 187 102 C 182 108, 176 114, 167 116" fill="#FAF7F2" stroke="#FAF7F2" stroke-width="0.5" />
      <path d="M 166 118 C 172 120, 179 116, 185 112 C 180 118, 174 122, 165 124" fill="#FAF7F2" stroke="#FAF7F2" stroke-width="0.5" />

      <!-- Right Inner Ear Cavity -->
      <path d="M 374 49 C 383 70, 383 95, 377 120 C 369 128, 357 122, 347 100 C 339 82, 345 65, 351 58 Z" fill="url(#earCavityR)" stroke="#B64534" stroke-width="0.8" />
      <!-- Right Ear Tufts (3 soft sculpted porcelain tufts) -->
      <path d="M 373 98 C 367 100, 360 96, 354 92 C 359 98, 365 104, 374 106" fill="#FAF7F2" stroke="#FAF7F2" stroke-width="0.5" />
      <path d="M 375 108 C 369 110, 362 106, 356 102 C 361 108, 367 114, 376 116" fill="#FAF7F2" stroke="#FAF7F2" stroke-width="0.5" />
      <path d="M 377 118 C 371 120, 364 116, 358 112 C 363 118, 369 122, 378 124" fill="#FAF7F2" stroke="#FAF7F2" stroke-width="0.5" />

      <!-- 5. Forehead Tabby Stripes (Soft amber rounded drops) -->
      <!-- Center vertical drop -->
      <path d="M 271.5 73 C 275 73, 276 80, 276 95 C 276 110, 273.5 118, 271.5 118 C 269.5 118, 267 110, 267 95 C 267 80, 268 73, 271.5 73 Z" fill="#B24E0C" opacity="0.85" />
      <!-- Left tilted drop -->
      <path d="M 243 81 C 246 80, 250 84, 252 98 C 254 112, 253 120, 251 121 C 249 122, 245 118, 243 104 C 241 92, 241 82, 243 81 Z" fill="#B24E0C" opacity="0.80" />
      <!-- Right tilted drop -->
      <path d="M 300 81 C 302 82, 302 92, 300 104 C 298 118, 294 122, 292 121 C 290 120, 289 112, 291 98 C 293 84, 297 80, 300 81 Z" fill="#B24E0C" opacity="0.80" />
    </g>

    <!-- 6. White Fur Coat: Solid White Porcelain from Blaze to Paws -->
    <!-- Solid white base filling the entire front legs, paws, chest, and cheeks -->
    <path d="M 271.5 112 C 256 132, 240 148, 228 158 C 205 168, 178 184, 162 205 C 154 218, 156 235, 172 250 C 188 262, 204 266, 214 275 C 220 310, 224 365, 226 415 C 228 445, 218 458, 205 466 C 201 470, 201 490, 210 490 L 333 490 C 342 490, 342 470, 338 466 C 325 458, 315 445, 317 415 C 319 365, 323 310, 329 275 C 339 266, 355 262, 371 250 C 387 235, 389 218, 381 205 C 365 184, 338 168, 315 158 C 303 148, 287 132, 271.5 112 Z" fill="url(#whiteCoatGrad)" stroke="#C6BAA8" stroke-width="0.8" />

    <!-- 7. Grounded 3D Front & Rear Paws (Solid White Ceramic resting on Y=490) -->
    <!-- Left Front Paw: X in [232, 270], 3 distinct rounded toes -->
    <g id="leftPawToes">
      <!-- Outer toe -->
      <path d="M 232 490 C 232 468, 244 466, 245 470 L 245 490 Z" fill="url(#toeGrad)" stroke="#C6BAA8" stroke-width="0.6" />
      <!-- Middle toe -->
      <path d="M 244 490 C 244 464, 258 462, 258 470 L 258 490 Z" fill="url(#toeGrad)" stroke="#C6BAA8" stroke-width="0.6" />
      <!-- Inner toe -->
      <path d="M 257 490 C 257 465, 270 465, 270 472 L 270 490 Z" fill="url(#toeGrad)" stroke="#C6BAA8" stroke-width="0.6" />
      <!-- Toe shadow creases -->
      <path d="M 244.5 470 L 244.5 490" stroke="#B8AC98" stroke-width="1.3" stroke-linecap="round" />
      <path d="M 257.5 470 L 257.5 490" stroke="#B8AC98" stroke-width="1.3" stroke-linecap="round" />
    </g>

    <!-- Right Front Paw: X in [273, 311], 3 distinct rounded toes -->
    <g id="rightPawToes">
      <!-- Inner toe -->
      <path d="M 273 490 C 273 465, 286 465, 286 472 L 286 490 Z" fill="url(#toeGrad)" stroke="#C6BAA8" stroke-width="0.6" />
      <!-- Middle toe -->
      <path d="M 285 490 C 285 464, 299 462, 299 470 L 299 490 Z" fill="url(#toeGrad)" stroke="#C6BAA8" stroke-width="0.6" />
      <!-- Outer toe -->
      <path d="M 298 490 C 298 468, 310 466, 310 470 L 310 490 Z" fill="url(#toeGrad)" stroke="#C6BAA8" stroke-width="0.6" />
      <!-- Toe shadow creases -->
      <path d="M 285.5 470 L 285.5 490" stroke="#B8AC98" stroke-width="1.3" stroke-linecap="round" />
      <path d="M 298.5 470 L 298.5 490" stroke="#B8AC98" stroke-width="1.3" stroke-linecap="round" />
    </g>

    <!-- Rear Paws (Left & Right outer pads) -->
    <path d="M 207 490 C 205 476, 216 470, 226 472 C 230 473, 232 480, 233 490 Z" fill="url(#toeGrad)" stroke="#C6BAA8" stroke-width="0.6" />
    <path d="M 336 490 C 338 476, 327 470, 317 472 C 313 473, 311 480, 310 490 Z" fill="url(#toeGrad)" stroke="#C6BAA8" stroke-width="0.6" />

    <!-- Ambient shadow groove between front legs -->
    <path d="M 271.5 375 C 271.5 410, 271.5 450, 271.5 490" stroke="#B8AC98" stroke-width="1.8" stroke-linecap="round" fill="none" opacity="0.85" />

    <!-- Chest Specular Highlight -->
    <ellipse cx="271.5" cy="320" rx="38" ry="50" fill="url(#chestHighlight)" />

    <!-- 8. Glassy Amber Orb Eyes (With blink animation) -->
    <g class="anim-eyes">
      <!-- Left Eye: Center (225, 171.5), tilted -5deg -->
      <g transform="translate(225, 171.5) rotate(-5)">
        <!-- Dark Eyeliner Socket -->
        <ellipse cx="0" cy="0" rx="27" ry="29" fill="#1C1004" />
        <!-- Glowing Amber Iris -->
        <ellipse cx="0" cy="0" rx="25.5" ry="27.5" fill="url(#amberIrisL)" />
        <!-- Black Pupil -->
        <ellipse cx="0.5" cy="0" rx="18.5" ry="20" fill="#080401" />
        <!-- Crisp Primary Specular Glint (at 1:30 position) -->
        <circle cx="5" cy="-7" r="8.0" fill="#FFFFFF" />
        <!-- Secondary Ambient Specular Glint (at 7:30 position) -->
        <circle cx="-6" cy="11" r="3.6" fill="#FFFFFF" opacity="0.65" />
      </g>

      <!-- Right Eye: Center (318, 171.5), tilted +5deg -->
      <g transform="translate(318, 171.5) rotate(5)">
        <!-- Dark Eyeliner Socket -->
        <ellipse cx="0" cy="0" rx="27" ry="29" fill="#1C1004" />
        <!-- Glowing Amber Iris -->
        <ellipse cx="0" cy="0" rx="25.5" ry="27.5" fill="url(#amberIrisR)" />
        <!-- Black Pupil -->
        <ellipse cx="-0.5" cy="0" rx="18.5" ry="20" fill="#080401" />
        <!-- Crisp Primary Specular Glint (at 1:30 position) -->
        <circle cx="5" cy="-7" r="8.0" fill="#FFFFFF" />
        <!-- Secondary Ambient Specular Glint (at 7:30 position) -->
        <circle cx="-6" cy="11" r="3.6" fill="#FFFFFF" opacity="0.65" />
      </g>
    </g>

    <!-- 9. Whisker Pads (Muzzle Mounds) & Soft Nose -->
    <!-- Whisker pad left mound -->
    <ellipse cx="258" cy="214" rx="15" ry="12" fill="#FAF7F2" opacity="0.9" />
    <!-- Whisker pad right mound -->
    <ellipse cx="285" cy="214" rx="15" ry="12" fill="#FAF7F2" opacity="0.9" />

    <!-- Button Nose: Rounded kidney/mushroom shape -->
    <path d="M 262 196 C 266 194, 277 194, 281 196 C 285 200, 278 207, 271.5 207 C 265 207, 258 200, 262 196 Z" fill="url(#noseGrad)" stroke="#DF6E62" stroke-width="0.8" />
    <ellipse cx="271.5" cy="197" rx="3.5" ry="1.5" fill="#FFFFFF" opacity="0.6" />

    <!-- Philtrum & Mouth Line ω -->
    <path d="M 271.5 207 L 271.5 215" stroke="#7A6857" stroke-width="1.4" stroke-linecap="round" fill="none" />
    <path d="M 250 222 C 256 226, 265 224, 271.5 215 C 278 224, 287 226, 293 222" stroke="#7A6857" stroke-width="1.4" stroke-linecap="round" fill="none" />
    <!-- Chin Shadow -->
    <ellipse cx="271.5" cy="236" rx="11" ry="4.5" fill="#DCCEBE" opacity="0.5" />

    <!-- 10. Delicate Porcelain Feline Whiskers (3 left, 3 right) -->
    <!-- Left Whiskers -->
    <path d="M 248 214 C 222 213, 198 218, 180 220" stroke="#FAF7F2" stroke-width="1.3" stroke-linecap="round" fill="none" opacity="0.95" />
    <path d="M 246 220 C 220 222, 196 230, 178 236" stroke="#FAF7F2" stroke-width="1.3" stroke-linecap="round" fill="none" opacity="0.95" />
    <path d="M 247 226 C 224 233, 204 242, 190 250" stroke="#FAF7F2" stroke-width="1.1" stroke-linecap="round" fill="none" opacity="0.90" />
    
    <!-- Right Whiskers -->
    <path d="M 295 214 C 321 213, 345 218, 363 220" stroke="#FAF7F2" stroke-width="1.3" stroke-linecap="round" fill="none" opacity="0.95" />
    <path d="M 297 220 C 323 222, 347 230, 365 236" stroke="#FAF7F2" stroke-width="1.3" stroke-linecap="round" fill="none" opacity="0.95" />
    <path d="M 296 226 C 319 233, 339 242, 353 250" stroke="#FAF7F2" stroke-width="1.1" stroke-linecap="round" fill="none" opacity="0.90" />
  </g>
</svg>"""
    return svg

svg_content = generate_flawless_meoweko_svg("dark")
with open("scratch/meoweko_perfect_vector.svg", "w") as f:
    f.write(svg_content)

cmd = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "--headless",
    "--disable-gpu",
    "--screenshot=scratch/meoweko_perfect_vector.png",
    "--window-size=512,512",
    "--default-background-color=00000000",
    "file:///Users/richard/Developer/Stickers Uko/scratch/meoweko_perfect_vector.svg"
]
subprocess.run(cmd, check=True)

# Build side-by-side comparison
ref = Image.open("mascots/meoweko/meoweko_master_exact_512.png").convert("RGBA")
vec = Image.open("scratch/meoweko_perfect_vector.png").convert("RGBA")

comp = Image.new("RGBA", (1024, 512), (11, 15, 23, 255))
comp.paste(ref, (0, 0), ref)
comp.paste(vec, (512, 0), vec)

draw = ImageDraw.Draw(comp)
draw.line([(512, 0), (512, 512)], fill=(217, 155, 38), width=2)
comp.save("scratch/meoweko_perfect_comparison.png")
print("Saved scratch/meoweko_perfect_comparison.png!")
