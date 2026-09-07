# 📘 Guide des Standards de Génération & Charte de Cohérence des Mascottes Uko
> **Standard Operating Procedure (SOP) & Design Bible** pour la production multi-poses et multi-animations (IA Générative, Studios 3D, Animateurs).

---

## 🎯 Objectif
Garantir une **cohérence absolue (Zéro Inconsistance)** entre toutes les animations et images d'une même mascotte, quel que soit l'outil de génération (Midjourney, Stable Diffusion / Flux + LoRA, Blender, Cinema 4D) ou le prestataire 3D.

---

## 1. 📐 Invariance Anatomique & Proportions (Model Sheet & Scale)

### 1.1 Règle du Ratio d'Échelle Canonique (*Head-to-Body Ratio*)
* **Ratio de tête** : La taille de la tête par rapport au corps doit être rigoureusement identique sur 100% des déclinaisons (ex: Style Chibi 1:1.5 ou 1:2).
* **Volume Corporel Invariant (*Mass Conservation*)** :
  * Même en cas de déformation dynamique (*Squash & Stretch* lors d'un saut ou d'une célébration), le volume total de la mascotte ne doit ni grossir ni rétrécir de manière permanente.
  * **Cas des postures couchées / 4 pattes** (ex: `sleeping`, `searching`) : La largeur du corps ou la taille du crâne doit rester à l'échelle 1:1 de la version debout (`idle`).

### 1.2 Isolation des Accessoires Aériens (*Overhead Props & VFX*)
* Les effets visuels flottants (ampoule pour `idea`, confettis pour `celebrating`, étincelles, loupe pour `searching`, bouclier pour `security`) **ne doivent en aucun cas réduire la taille du personnage**.
* Le personnage doit conserver sa taille cible (ex: 350 px dans une boîte 512×512), et les accessoires doivent occuper la marge supérieure (*Headroom* réservée de 60 à 90 px).

### 1.3 Baseline & Ancrage au Sol vs Lévitation
* **Mascottes terrestres** (Owluko, Luneko, Inuko, Hatoko, Usako) : Les pattes/pieds doivent être ancrés sur une ligne d'horizon / plan de sol fixe (*Ground Plane* constant).
* **Mascottes flottantes** (AItuko le robot) : L'altitude de flottaison par rapport à la base doit être mesurée et stabilisée autour du centre de masse ($\pm 10\text{px}$ d'oscillation max).

---

## 2. 🎨 Charte Chromatique & Matériaux (Color & Texture Consistency)

### 2.1 Valeurs HEX / RGB Fixes par Composant
Chaque mascotte doit posséder sa table de couleurs non négociable :
* **AItuko** : Blanc Céramique (`#F8FAFC`), Bleu Électrique Yeux (`#00F0FF`), Métal Articulations (`#334155`), Orange Accent (`#FF6B00`).
* **Owluko** : Brun Plumes (`#8B5A2B`), Ventre Crème (`#FDF6E2`), Bec/Pattes Or (`#F59E0B`), Yeux Obsidienne (`#1E293B`).
* **Luneko** : Pelage Roux Doré (`#E67E22`), Blanc Poitrail/Pattes (`#FFFFFF`), Coussinets Rose Pâle (`#FFB6C1`), Yeux Émeraude (`#10B981`).
* **Tolérance colorimétrique** : $\Delta E < 2.0$ (aucune dérive vers du jaune verdâtre ou du violet entre deux poses).

### 2.2 Finition des Matériaux (*Shader & Material Finish*)
* **Texture** : Mat doux / Plastique vinylique de collection (*Smooth Matte Vinyl / Soft Claymorphism*).
* **Subsurface Scattering (SSS)** : Diffusion de lumière sous-cutanée subtile et uniforme pour donner un aspect vivant sans paraître cireux.
* **Reflets (*Specular Roughness*)** : Rugosité fixée entre `0.35` et `0.45` pour éviter les reflets miroir aveuglants qui brûlent les détails.

---

## 3. 💡 Setup Éclairage Studio & Caméra 3D (Lighting & Camera)

### 3.1 Setup Caméra Standardisé
* **Type d'objectif** : Focale longue équivalente **85mm à 100mm** (ou projection orthographique / quasi-isométrique) pour éliminer toute distorsion de perspective (pas de grand angle "effet fisheye" qui déforme le museau).
* **Angle de vue** : Caméra frontale légèrement plongeante à **+5° à +8°** d'élévation, pointée directement sur le centre de masse du buste.

### 3.2 Setup Lumière 3-Points (*Three-Point Studio Lighting*)
1. **Key Light (Lumière Principale)** : 45° haut-gauche, température de couleur neutre **5500K**, ombres douces et diffuses.
2. **Fill Light (Lumière de Remplissage)** : 45° bas-droite, intensité à **35%**, température **5000K**, débouche les ombres sans créer de second reflet parasite.
3. **Rim Light / Back Light (Lumière de Détourage)** : Directement derrière et au-dessus, intensité à **50%** pour séparer nettement la silhouette du fond sans créer de halo blanc exagéré.

---

## 4. 🟩 Fond Vert & Exigences de Détourage (Chroma Keying)

### 4.1 Spécifications du Fond Vert
* **Couleur de fond** : Vert pur uniforme `#00FF00` (RGB: 0, 255, 0) à 100% de saturation, parfaitement éclairé sans dégradé ni ombre projetée de la mascotte sur le mur de fond.
* **Règle d'or de contraste** : Si la mascotte comporte des éléments verts (ex: yeux émeraudes de Luneko), **le fond vert est strictement interdit** $\rightarrow$ Utiliser un fond bleu pur `#0000FF` (Blue Screen).

### 4.2 Distance Sujet-Fond & Anti-Spill
* Maintenir une distance virtuelle suffisante entre la mascotte et le fond vert pour éviter que la lumière verte ne rebondisse sur les bords blancs/crème du personnage (*Green Spill*).
* Si un despill numérique est appliqué, s'assurer qu'il ne grise pas les tons jaunes ou or (ex: bec d'Owluko).

---

## 5. ⏱ Animation, Cadence & Looping (Motion Standard)

* **Cadence d'images (Framerate)** : **24 fps fixe** (zéro interpolation variable).
* **Durée de boucle** : Exactement **4,00 secondes (96 frames)** pour un cycle complet.
* **Boucle Parfaite (*Seamless Loop*)** :
  * La frame 96 doit se fondre de manière imperceptible dans la frame 01.
  * Pour les animations d'action ponctuelle (ex: `05_thumbs_up`, `07_pointing`), le personnage doit amorcer son geste depuis la pose de repos, exécuter l'action, puis revenir délicatement à sa pose de repos.

---

## 6. 📋 Grille de Validation Pré-Livraison (Checklist 10 Points)

Avant d'intégrer toute nouvelle mascotte ou animation au catalogue Uko, vérifier point par point :

| # | Point de Contrôle | Critère d'Acceptation | Statut |
| :-: | :--- | :--- | :-: |
| **1** | **Hauteur corporelle** | Corps seul calibré à 350 px dans le cadre 512×512 | [ ] |
| **2** | **Headroom & Props** | Accessoires au-dessus de la tête sans rétrécir le corps | [ ] |
| **3** | **Couleurs exactes** | Codes HEX respectés ($\Delta E < 2.0$) | [ ] |
| **4** | **Yeux & Visage** | Pupilles, reflets et micro-expressions identiques | [ ] |
| **5** | **Texture & Matière** | Fini Claymorphism / Vinyle mat sans brillance excessive | [ ] |
| **6** | **Éclairage** | Key Light 5500K 45° gauche, ombres douces | [ ] |
| **7** | **Fond uniforme** | Vert `#00FF00` pur sans ombres portées au mur | [ ] |
| **8** | **Aucun artefact IA** | Pas de doigts fusionnés, membres surnuméraires ou bave | [ ] |
| **9** | **Durée & Cadence** | 96 frames à 24.0 fps (durée exacte 4,00s) | [ ] |
| **10** | **Seamless Loop** | Raccordement parfait entre dernière et première frame | [ ] |

---

## 7. 🤖 Template de Briefing pour Prestataire ou IA Générative

```markdown
**PROMPT / BRIEF STRUCTURE :**
[Character Sheet Reference: {MASCOT_ID}]
- Pose/Action : {STATE_NAME} - {ACTION_DESCRIPTION}
- Style : 3D Premium Japandi Claymorphism, Soft Vinyl Toy, Studio Render, Pixar-like quality.
- View : Front view, slight 6° elevation, 85mm lens, no fisheye distortion.
- Scale : Full body centered, body height precisely 70% of canvas, leaving 15% top margin for overhead VFX.
- Palette : Strict HEX [{HEX_BODY}, {HEX_DETAILS}, {HEX_EYES}].
- Lighting : 3-Point Studio Lighting (Key 5500K 45° left, Soft Fill 35% right, Rim back light).
- Background : Solid pure chromakey green (#00FF00), perfectly lit, zero shadows on background, no green spill on subject.
- Quality : 8K textures, clean geometry, zero blur, sharp silhouette contours, seamless 4.0s 24fps loop.
```
