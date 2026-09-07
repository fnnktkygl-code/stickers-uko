# Walkthrough — Animation Master AItuko State 04 : Error 404 (Fidélité 100% Canonique)

> [!IMPORTANT]
> **Conformité Rigoureuse aux Directives Utilisateur & Vérité Terrain :**
> - **PIEDS OPTION IDÉALE & RENDU EN AVANT DU TORSE** :
>   * Approbation explicite de l'Option Idéale :
>     - Pied gauche : rotation $+12.0^\circ$ (sens horaire, facette interne orientée vers le corps), $\Delta x_L = -8.0\text{ px}$
>     - Pied droit : rotation $-12.0^\circ$ (sens anti-horaire, facette interne orientée vers le corps), $\Delta x_R = +8.0\text{ px}$
>     - Contact sol parfait : $\Delta y = +22.0\text{ px}$ (posés à plat sur le plancher $y = 488\text{ px}$), $scale_x = 1.12, scale_y = 0.88$
>   * Rendu des pieds **EN AVANT DU TORSE AFFAISSÉ** pour une assise naturelle et crédible contre le bas du ventre.
>   * Interpolation cinématique fluide de $f=26$ à $f=35$ (touchdown) et de $f=75$ à $f=84$ (reboot).
> - **TRONC DU CORPS FERMEMENT POSÉ AU SOL** :
>   * Conformité avec la référence studio 3D : le tronc touche directement le plan de sol studio.
>   * En posture assise affaissée ($f=35\dots 74$) :
>     - Descente du tronc : $\Delta y_{root} = 72.0\text{ px}$ (la base arrondie du tronc atteint $y \sim 485\dots 487\text{ px}$)
>     - Écrasement élastique du torse : $scale_x = 1.06, scale_y = 0.93$
>     - Inclinaison empathique de la tête : $\Delta y_{head} = 78.0\text{ px}$, $\text{rot}_{head} = 3.6^\circ$, menton bas masquant discrètement le collier
>     - Ailerons latéraux au sol : $\Delta y_{pods} = 70.0\text{ px}$, $\text{rot}_L = +14.0^\circ, \text{rot}_R = -14.0^\circ$, $\Delta x_L = -4.0\text{ px}, \Delta x_R = +4.0\text{ px}$
>     - Ombre de contact studio : ellipse dense d'occlusion sous la base du torse ($x \in [200, 312], y \in [482, 494]$) et sous les pieds.
> - **TÉLÉMÉTRIE VISIÈRE 100% ROUGE — STRICTEMENT ZÉRO PIXEL CYAN PENDANT L'ERREUR** :
>   * *"Tout doit être en rouge, pas en couleur cyan. C'est une erreur."*
>   * **Phase 2 (Alerte / Panne, $f = 21\dots 28$)** : Points d'exclamation rouge néon éclatant **`!   !`** avec fûts verticaux, points et lueur diffuse.
>   * **Phase 4 (Affaissement Assis, $f = 29\dots 74$)** : Option 01 — Télémétrie 7-Segments Classique Industriel **`E r r`** :
>     - Géométrie authentique d'afficheurs 7 segments avec biseaux / onglets à 45° sur chaque segment.
>     - Segments fantômes éteints visibles en arrière-plan sombre (`#2D0E10`, opacité ~0.35) pour un réalisme électronique LCD/LED authentique.
>     - Segments actifs en rouge cyber LED éclatant (`#FF3B30`) avec cœur interne corail clair (`#FFD0D0`) et bloom subtil.
>     - Caractère 1 : `E` (segments A, F, G, E, D allumés).
>     - Caractère 2 : `r` (segments E, G allumés : montant vertical bas-gauche + barre médiane).
>     - Caractère 3 : `r` (segments E, G allumés : montant vertical bas-gauche + barre médiane).
>     - Centré sur la visière affaissée à $y \approx 105\dots 137\text{ px}$.
>   * **Zéro cyan absolu** : Infill automatique de tout résidu de halo dans la zone visière avec la teinte obsidienne sombre `(14, 18, 26)`. Strictement 0 pixel cyan sur tout le canevas et sur les posters statiques.
>   * **Phase 5 (Reboot, $f = 75\dots 84$)** : Extinction de la télémétrie rouge, ré-allumage joyeux des yeux cyan (`^ ^`) à $f = 81$, décollage ascensionnel.
>   * **Phase 6 (Stabilisation, $f = 85\dots 119$)** : Amortissement harmonique avec clignement de conscience à $f = 103\dots 107$.
> - **SUPPRESSION TOTALE DE LA CARTE 404 FLOTTANTE** :
>   * Zéro badge ou carte externe flottante. Toute la télémétrie s'affiche directement **dans l'écran de la visière**.
> - **Fichier Lottie Vectoriel Pur < 50 Ko** : **39.12 Ko** (11 calques Bodymovin, Option 01 7-segments E r r, markers `error_intro` $f=0\dots 34$, `error_slump_loop` $f=35\dots 74$, `error_reboot` $f=75\dots 119$).
> - **Validation Tests Unitaires 100% Verte** : **59/59 tests réussis** sur toute la suite AItuko.
> 
> ---
> 
> ## 1. Décomposition Cinématique des 120 Frames (Boucle 4.0s / 30 FPS)
> 
> | Phase | Frames | Durée | Cinématique, Posture & Télémétrie Visière |
> | :--- | :--- | :--- | :--- |
> | **1. Sustentation Nominale** | $f = 0\dots 20$ | $0.0\text{s} - 0.67\text{s}$ | Vol stationnaire équilibré, yeux cyan souriants (`^ ^`), ombre de sol diffuse à $y = 488\text{ px}$ (16px d'air sous les pieds). |
> | **2. Alerte & Panne `!   !`** | $f = 21\dots 28$ | $0.70\text{s} - 0.93\text{s}$ | Coupure brutale des propulseurs, yeux cyan **totalement éteints**, points d'exclamation d'alerte **`!   !`** rouge cyber LED. |
> | **3. Impact & Transition Assise** | $f = 29\dots 34$ | $0.97\text{s} - 1.13\text{s}$ | Touchdown au sol, transition fluide vers Option Idéale et affaissement complet, transition vers l'affichage **`E r r`**. |
> | **4. Tronc Fermement au Sol & `E r r`** | $f = 35\dots 74$ | $1.17\text{s} - 2.47\text{s}$ | **Tronc au sol** ($\Delta y_{root} = +72\text{ px}$, base à $y \sim 485..487\text{ px}$), pieds Option Idéale posés en avant ($\Delta y = +22\text{ px}, \Delta x = \mp 8\text{ px}, \pm 12^\circ$), ailerons au sol ($\Delta y = 70\text{ px}, \pm 14^\circ$). Option 01 7-segments **`E r r`** rouge cyber biseauté avec segments fantômes `#2D0E10`. Zéro cyan. |
> | **5. Reboot Système & Décollage** | $f = 75\dots 84$ | $2.50\text{s} - 2.80\text{s}$ | Extinction de la télémétrie rouge, ré-allumage éclatant des yeux cyan (`^ ^`) à $f = 81$, poussée verticale ascensionnelle. |
> | **6. Amorti Harmonique & Clignement** | $f = 85\dots 119$ | $2.83\text{s} - 4.00\text{s}$ | Stabilisation C1 damped settle, clignement de conscience ($f = 103\dots 107$), bouclage seamless parfait à $f = 120 / 0$. |

---

## 2. Planche Officielle Master Error 404 ($1920 \times 1080$ px)

![Planche Officielle Master AItuko Error 404](/Users/richard/Developer/Stickers%20Uko/assets/04_error_404/aituko_error_404_master_board.png)

---

## 3. Carrousel des 4 Poses Clés du Rendu de Production ($512 \times 512$ px)

````carousel
![01 — Sustentation Nominale (t = 0.0s)](/Users/richard/Developer/Stickers%20Uko/assets/04_error_404/keyframe_01_nominal_levitation.png)
<!-- slide -->
![02 — Alerte Immédiate '! !' (t = 0.83s)](/Users/richard/Developer/Stickers%20Uko/assets/04_error_404/keyframe_02_shock_stutter.png)
<!-- slide -->
![03 — Posture Assise & Télémétrie 'ERR' (t = 1.83s)](/Users/richard/Developer/Stickers%20Uko/assets/04_error_404/keyframe_03_grounded_slump_err.png)
<!-- slide -->
![04 — Reboot Système & Redécollage (t = 2.73s)](/Users/richard/Developer/Stickers%20Uko/assets/04_error_404/keyframe_04_reboot_ascent.png)
````

---

## 4. Planche Trichrome d'Inspection Multi-Fonds ($1536 \times 512$ px)

Vérification de la lisibilité de la posture assise canonique et de la télémétrie visière rouge sur Studio White, Studio Dark et Chroma Green :

![Planche Trichrome d'Inspection Multi-Fonds](/Users/richard/Developer/Stickers%20Uko/assets/04_error_404/aituko_error_404_studio_trichroma_board.png)

---

## 5. Comparaison Côte-à-Côte Rendu vs Référence Studio

![Comparaison Côte-à-Côte](/Users/richard/Developer/Stickers%20Uko/assets/04_error_404/seated_f55_comparison.png)

---

## 6. Aperçus Animés de Production (Boucle 4.0s / 30 FPS)

````carousel
![Rendu GIF Fond Studio Dark](/Users/richard/Developer/Stickers%20Uko/assets/04_error_404/animated_dark.gif)
<!-- slide -->
![Rendu GIF Fond Vert Chroma](/Users/richard/Developer/Stickers%20Uko/assets/04_error_404/animated_green.gif)
<!-- slide -->
![Rendu GIF Transparent](/Users/richard/Developer/Stickers%20Uko/assets/04_error_404/animated.gif)
````

---

## 7. Résultats des Tests Unitaires Automatisés

```bash
$ python3 -m unittest discover tests/
...........................................................
----------------------------------------------------------------------
Ran 59 tests in 4.784s

OK
```

- **`test_aituko_error_404_visual_integrity.py` : 9/9 tests réussis**
  1. `test_01_lottie_file_sizes_and_markers` : **39.12 Ko** (< 50.0 Ko), markers `error_intro` ($0..35$), `error_slump_loop` ($35..40$), `error_reboot` ($75..45$), superposition stricte pieds devant torse, zéro calque de carte flottante.
  2. `test_02_slump_kinematics_and_ground_contact` : Tronc fermement au sol $\Delta y_{root} = 72.0\text{px} \ge 65.0\text{px}$, base au sol $y \in [485, 488]$, pieds Option Idéale $\Delta x = \mp 8\text{px}$, rotation $+12.0^\circ / -12.0^\circ$, écrasement $scale_x = 1.12, scale_y = 0.88$, $\Delta y = 22.0\text{px}$.
  3. `test_03_diegetic_visor_telemetry_timing` : Alerte `! !` ($f=25$), télémétrie 7-segments `E r r` ($f=55$), reboot cyan ($f=82$), clignement ($f=105$).
  4. `test_04_zero_human_hands_and_fingers` : Zéro doigt, zéro main humaine sur les ailerons.
  5. `test_05_porcelain_colors_and_zero_cyan_during_error` : **0 pixel cyan** sur tout le canevas pendant les phases d'erreur ($f=25, 30, 55, 70$) et sur les fichiers statiques.
  6. `test_06_deliverables_completeness` : Vérification exhaustive des livrables dans `assets/04_error_404/`, `mascots/aituko/`, `aituko/assets/04_error_404/`, `downloads/`.
  7. `test_07_zero_external_foot_assets_and_zero_floating_card` : Absence stricte d'assets de pieds externes ou de carte flottante dans le code.
  8. `test_08_svg_transforms_and_zero_pod_or_head_drift` : Validation des origines CSS et de l'ordre DOM des pieds après le torse dans le SVG animé.
  9. `test_09_option_01_7seg_telemetry_and_geometry` : Validation complète de l'Option 01 7-segments `E r r` (12 segments fantômes `#2D0E10`, 9 segments actifs `#FF3B30`, 9 surbrillances cœur `#FFD0D0` dans Lottie et SVG, géométrie polygonale fermée à 4/6 sommets, coordonnées visière nominale $y \in [105, 138]$ et pose assise $f=55$).

---

## 8. Livrables et Fichiers de Production Générés

| Fichier / Format | Emplacement Principal | Rôle & Spécifications |
| :--- | :--- | :--- |
| **Lottie JSON Vectoriel** | [`assets/04_error_404/lottie.json`](file:///Users/richard/Developer/Stickers%20Uko/assets/04_error_404/lottie.json) | **39.12 Ko** (< 50 Ko), 11 calques vectoriels, markers Bodymovin, radial shadow falloff |
| **SVG Animé CSS** | [`assets/04_error_404/animated.svg`](file:///Users/richard/Developer/Stickers%20Uko/assets/04_error_404/animated.svg) | CSS keyframes 512x512 autonome, posture assise + `! !` + `ERR` |
| **WebP Animé Transparent** | [`assets/04_error_404/animated.webp`](file:///Users/richard/Developer/Stickers%20Uko/assets/04_error_404/animated.webp) | 120 frames RGBA 8-bit, 30 fps, boucle fluide 4.0s |
| **PNG Animé (APNG)** | [`assets/04_error_404/animated.png`](file:///Users/richard/Developer/Stickers%20Uko/assets/04_error_404/animated.png) | 120 frames RGBA, boucle continue 4.0s |
| **GIF Animé Transparent** | [`assets/04_error_404/animated.gif`](file:///Users/richard/Developer/Stickers%20Uko/assets/04_error_404/animated.gif) | GIF transparent haute netteté |
| **GIF Dark Studio** | [`assets/04_error_404/animated_dark.gif`](file:///Users/richard/Developer/Stickers%20Uko/assets/04_error_404/animated_dark.gif) | Fond studio sombre `#0B0F17` |
| **GIF Chroma Green** | [`assets/04_error_404/animated_green.gif`](file:///Users/richard/Developer/Stickers%20Uko/assets/04_error_404/animated_green.gif) | Fond vert incrustation `#00FF00` |
| **Vidéo MP4 Looped** | [`assets/04_error_404/looped_video.mp4`](file:///Users/richard/Developer/Stickers%20Uko/assets/04_error_404/looped_video.mp4) | H.264 CRF 18, 30 fps, boucle continue 4.0s |
| **Poster Statique PNG** | [`assets/04_error_404/static.png`](file:///Users/richard/Developer/Stickers%20Uko/assets/04_error_404/static.png) | Image clé d'erreur 512x512 (hero pose $f=55$), zéro cyan |
| **Poster Statique WebP** | [`assets/04_error_404/static.webp`](file:///Users/richard/Developer/Stickers%20Uko/assets/04_error_404/static.webp) | Image clé d'erreur WebP 512x512 (hero pose $f=55$) |
| **Planche Master Board** | [`assets/04_error_404/aituko_error_404_master_board.png`](file:///Users/richard/Developer/Stickers%20Uko/assets/04_error_404/aituko_error_404_master_board.png) | 1920x1080 px avec les 4 étapes clés et spécifications techniques |
| **Planche Trichrome** | [`assets/04_error_404/aituko_error_404_studio_trichroma_board.png`](file:///Users/richard/Developer/Stickers%20Uko/assets/04_error_404/aituko_error_404_studio_trichroma_board.png) | 1536x512 px comparaison White, Dark, Chroma Green |
| **Bundle Zip Complet** | [`downloads/aituko_error_404_bundle.zip`](file:///Users/richard/Developer/Stickers%20Uko/downloads/aituko_error_404_bundle.zip) | Archive téléchargeable tout-en-un synchronisée |
