# 🦉 Guide des Prompts de Régénération Vidéo 3D : Owluko
> **Prompt Bible & Technical Specs** pour outils de génération vidéo IA (*Kling 1.5/2.0, Runway Gen-3 Alpha, Luma Dream Machine, Hailuo Minimax, Midjourney v6.1 + Video*).

---

## ⚙️ Configuration Globale & Paramètres Techniques Communs

À appliquer sur **toutes les générations** :
* **Image de Référence (Image-to-Video / Character Reference)** : Uploader `mascots/owluko/owluko_idle.jpeg` comme référence stricte (Poids de référence / Fidelity = `0.85 - 0.95`).
* **Format & Résolution** : `1920x1080` (ou `1024x1024` 1:1), 24 fps, durée **4.0 secondes**.
* **Fond** : Solid pure uniform chroma green `#00FF00` (sans ombres portées, sans dégradé).
* **Caméra** : Frontal view, 85mm portrait lens, orthographic perspective, centered character.
* **Negative Prompt Global (À copier-coller systématiquement)** :
  ```text
  human hands, human fingers, human thumbs, human arms, bare skin, knuckles, morphing beak, tiny beak, giant beak, asymmetric ear tufts, horns, owl ears, visible human feet, deformed limbs, green spill, background shadows, camera shake, motion blur, flickering, low quality, 2D flat, noisy textures
  ```

---

## 🎬 Prompts Détaillés Pose par Pose (13 Animations)

---

### `00_idle` (Étalon de Référence)
* **Objectif** : Boucle de repos respiratoire subtile et vivante.
* **Prompt** :
  ```text
  [Character Reference: Owluko] Cute 3D stylized chubby round owl mascot standing still on a clean solid pure chroma green background (#00FF00). Smooth matte vinyl clay texture, warm brown and soft beige feathers, creamy white chest, medium golden-orange hooked beak, big glossy obsidian eyes with double white circular reflections. The owl stays perched in a cute round resting pose, subtle gentle breathing motion, occasional gentle eye blink, seamless perfect 4.0-second loop. Studio 3-point neutral 5500K lighting, crisp sharp silhouette, 8K resolution, 24fps.
  ```

---

### `01_waving` (Accueil / Salut)
* **Objectif** : Saluer avec son **aile en plumes** (et non une main humaine).
* **Prompt** :
  ```text
  [Character Reference: Owluko] Cute 3D chubby round owl mascot on solid chroma green (#00FF00). The owl lifts its right feathered wing (smooth rounded bird wing, strictly no fingers) and gently waves it in a friendly welcoming greeting. Warm facial expression, big sparkling black eyes, creamy white chest, golden beak. The owl waves two times smoothly and returns its wing to resting position, creating a seamless 4.0-second loop. Consistent anatomy, identical scale to idle reference, 5500K studio lighting, 24fps.
  ```

---

### `02_celebrating` (Succès / Célébration)
* **Objectif** : Célébration joyeuse sans rupture de boucle.
* **Prompt** :
  ```text
  [Character Reference: Owluko] Cute 3D chubby round owl mascot jumping slightly in joy on solid chroma green (#00FF00). The owl flaps both feathered wings upward in celebration with a happy squinting smile. Tiny colorful festive confettis (pink, cyan, gold) float down softly around the mascot and fade out seamlessly before the cycle ends. Strict mass conservation, identical round body proportions, pure feathered wings, seamless 4.0-second loop, 5500K studio lighting, 24fps.
  ```

---

### `03_ai_thinking` (Réflexion / Pensée)
* **Objectif** : Regard pensif vers le haut, extrémité de l'aile sous le bec.
* **Prompt** :
  ```text
  [Character Reference: Owluko] Cute 3D chubby round owl mascot in thoughtful thinking pose on solid chroma green (#00FF00). The owl tilts its round head slightly, brings the rounded tip of its right feathered wing gently under its golden beak, and gazes upward thoughtfully. Subtle glowing sparkle around the head, gentle curious tilt, smoothly returning to center, seamless 4.0-second loop. Identical cream belly, perfectly round head without ear tufts, 5500K studio lighting, 24fps.
  ```

---

### `04_error_404` (Erreur / Problème) 🔴 *CORRECTION CRITIQUE*
* **Ce qui est corrigé** : Plus de sous-exposition sombre, bec à taille normale, ventre crème lumineux.
* **Prompt** :
  ```text
  [Character Reference: Owluko] Cute 3D chubby round owl mascot in an apologetic confused 404 error pose on solid chroma green (#00FF00). The owl has a cute sad/puzzled expression, slightly drooping rounded feathered wings, and gently blinks with a small question mark floating and vanishing above its head. Maintain full bright studio 5500K lighting, identical creamy white chest and warm brown feathers (no dark shadowy mood). Standard medium golden beak (no oversized beak), seamless 4.0-second loop, 24fps.
  ```

---

### `05_thumbs_up` (Validation / Pouce Haut) 🔴 *CORRECTION CRITIQUE*
* **Ce qui est corrigé** : **ZÉRO main humaine / ZÉRO pouce humain**. L'aile se plie vers le haut pour mimer le geste de manière stylisée.
* **Prompt** :
  ```text
  [Character Reference: Owluko] Cute 3D chubby round owl mascot giving an approval gesture on solid chroma green (#00FF00). The owl curves its right feathered wing upward into a cute rounded wing-thumbs-up stylized silhouette (pure bird wing with soft feather tip curved up, strictly NO human skin, NO fingers, NO human thumb). Confident happy wink, golden beak, creamy chest, seamless 4.0-second loop. Consistent 350px scale, 5500K studio lighting, 24fps.
  ```

---

### `06_sleeping` (Repos / Sommeil)
* **Objectif** : Yeux fermés en arcs souriants, bulles Zzz.
* **Prompt** :
  ```text
  [Character Reference: Owluko] Cute 3D chubby round owl mascot sleeping peacefully on solid chroma green (#00FF00). The owl has its eyes gently closed in curved happy crescent arcs, head slightly nodding in deep sleep, with small translucent Zzz bubbles floating up and popping gently. Identical round body, plumage colors identical to idle reference, smooth breathing cycle, seamless 4.0-second loop, 5500K studio lighting, 24fps.
  ```

---

### `07_pointing` (Guide / Direction) 🔴 *CORRECTION CRITIQUE*
* **Ce qui est corrigé** : **ZÉRO index humain**, pas de patte grise solitaire, pas de surexposition.
* **Prompt** :
  ```text
  [Character Reference: Owluko] Cute 3D chubby round owl mascot pointing to the right on solid chroma green (#00FF00). The owl extends its right feathered wing fully to the side, with the tapered rounded tip of the wing directing attention (strictly bird wing feather contour, NO human arm, NO index finger). Gentle friendly glance toward the viewer, balanced studio lighting on the cream chest without overexposure, seamless 4.0-second loop, 24fps.
  ```

---

### `08_searching` (Recherche / Loupe) 🔴 *CORRECTION CRITIQUE*
* **Ce qui est corrigé** : Version 1080p nette, aile tenant la loupe sans doigts de peau humaine.
* **Prompt** :
  ```text
  [Character Reference: Owluko] Cute 3D chubby round owl mascot holding a classic magnifying glass on solid chroma green (#00FF00). The owl holds the wooden handle between its two feathered wings (feathers wrapping gently around handle, NO human fingers) and looks through the glass, slightly magnifying its big shiny black eye in a curious detective expression. Identical plumage textures, high-definition 1080p, seamless 4.0-second loop, 24fps.
  ```

---

### `09_loading` (Attente / Sablier) 🔴 *CORRECTION CRITIQUE*
* **Ce qui est corrigé** : **Tête 100% ronde sans corne/aigrette asymétrique**, sablier fluide.
* **Prompt** :
  ```text
  [Character Reference: Owluko] Cute 3D chubby round owl mascot watching a glowing glass hourglass on solid chroma green (#00FF00). A small hourglass hovers near the owl, sand trickling smoothly. The owl has a perfectly smooth spherical round head (strictly NO ear tufts, NO horns, NO asymmetric feathers on head). The owl tilts its head following the sand, golden beak well-defined, seamless 4.0-second loop, 5500K studio lighting, 24fps.
  ```

---

### `10_idea` (Idée / Ampoule)
* **Objectif** : Ampoule flottant dans la marge haute (Headroom) sans écraser le corps.
* **Prompt** :
  ```text
  [Character Reference: Owluko] Cute 3D chubby round owl mascot with a bright idea on solid chroma green (#00FF00). A bright glowing yellow lightbulb pops up hovering 40px above the owl's head. The owl's eyes light up with joy, looking up excitedly at the bulb. The body maintains its full 350px scale (bulb sits in upper headroom). Lightbulb glows, pulses gently, and fades softly, seamless 4.0-second loop, 5500K studio lighting, 24fps.
  ```

---

### `11_security` (Sécurité / Bouclier) 🔴 *CORRECTION CRITIQUE*
* **Ce qui est corrigé** : Pas de pollution jaune sur le ventre, matériau de bouclier métallique argenté / bleu Uko propre.
* **Prompt** :
  ```text
  [Character Reference: Owluko] Cute 3D chubby round owl mascot holding a sleek metallic security shield on solid chroma green (#00FF00). The shield has a silver-metallic and deep sapphire-blue finish with a glowing white checkmark (clean metallic reflection, strictly NO yellow light cast on the owl's chest). The owl holds the shield proudly in front, confident reassuring smile, identical cream belly and brown plumage, seamless 4.0-second loop, 24fps.
  ```

---

### `12_goodbye` (Au Revoir / Départ) 🔴 *CORRECTION CRITIQUE*
* **Ce qui est corrigé** : Vrai bec doré moyen de taille normale, pattes rétractées ou masquées comme sur `idle`.
* **Prompt** :
  ```text
  [Character Reference: Owluko] Cute 3D chubby round owl mascot waving goodbye on solid chroma green (#00FF00). The owl holds a small cute vintage brown suitcase tucked near its wing, while waving its other feathered wing gently with a warm friendly farewell smile. Full-sized golden hooked beak (identical to 00_idle, strictly NO tiny shrinking beak), body sitting in standard round plush pose without anomalous protruding orange legs, seamless 4.0-second loop, 5500K studio lighting, 24fps.
  ```
