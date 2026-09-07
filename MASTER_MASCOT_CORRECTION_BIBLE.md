# 👑 BIBLE DE PRODUCTION ET DE CORRECTION 2-EN-1 : MASCOTTES UKO
> **Document de référence exhaustif pour l'opérateur IA / Studio 3D / Prestataire.**  
> Ce document regroupe **en une seule instruction par animation** : le **recadrage proportionnel strict (70% / 350 px)** ET la **correction de toutes les anomalies anatomiques, colorimétriques et de mouvement**, à partir des vidéos brutes originales.

---

# 📐 PARTIE 1 : LA RÈGLE D'OR UNIVERSELLE DES PROPORTIONS (Cadre 1080p & 512p)

Pour que toutes les animations d'une mascotte soient **visuellement superposables à 100% avec la version `00_idle`** :

```text
┌────────────────────────────────────────────────────────┐  ▲ Y = 0% (Haut du cadre)
│  MARGE SUPÉRIEURE / HEADROOM RÉSERVÉE (15% = 77 px)   │  │ Espace dédié aux effets aériens
│  (Ampoule 10_idea, Confettis 02, Étoiles, Zzz)         │  │ (L'accessoire ne rétrécit JAMAIS le corps)
├────────────────────────────────────────────────────────┤  ▼ Y = 15% (Sommet du crâne)
│                                                        │  ▲
│                                                        │  │
│        CORPS PRINCIPAL DE LA MASCOTTE                  │  │ HAUTEUR STRICTE DU CORPS = 70%
│        (Du sommet du crâne jusqu'au bas du corps)      │  │ (358 px sur 512 / 756 px sur 1080)
│                                                        │  │
│                                                        │  ▼
├────────────────────────────────────────────────────────┤  ▲ Y = 85% (Ligne de sol / Baseline)
│  MARGE INFÉRIEURE / ANCRAGE AU SOL (15% = 77 px)       │  │ Plan d'ancrage des pattes
└────────────────────────────────────────────────────────┘  ▼ Y = 100% (Bas du cadre)
```

1. **Hauteur Corporelle Constante ($70\%$ du cadre)** : Le corps de la mascotte (du haut du crâne jusqu'au bas des pattes) doit occuper exactement **70% de la hauteur totale**.
2. **Règle du Headroom (Accessoires Aériens)** : Les éléments flottants (`10_idea` ampoule, `02_celebrating` confettis, `06_sleeping` Zzz, `11_security` bouclier) habitent la marge supérieure de 15%. **Interdiction formelle de réduire la taille du personnage pour faire rentrer un accessoire**.
3. **Conservation de Masse (Postures couchées / 4 pattes)** : Pour les postures basses (ex: Luneko qui dort ou cherche au sol), la tête et le volume corporel restent à l'échelle **1:1** de la version debout (`00_idle`). Ne jamais étirer le corps pour remplir la hauteur.
4. **Fond Vert Pur Obligatoire** : `#00FF00` uni sans ombre portée, sans sol visible. (Si la mascotte a des yeux/détails verts, utiliser le bleu `#0000FF`).
5. **🔒 RÈGLE D'OR ABSOLUE : IMMUTABILITÉ GÉOMÉTRIQUE ET ANATOMIQUE DU MODÈLE MASTER SVG** :
   - Dès qu'une mascotte a son **Master Turnaround officiel validé avec ses vraies dimensions SVG**, ce modèle vectoriel et ses proportions constituent la **SOURCE UNIQUE ET INVIOLABLE DE VÉRITÉ GÉOMÉTRIQUE ET ANATOMIQUE**.
   - **Interdiction formelle d'altérer l'anatomie au fil des animations** : on ne change JAMAIS la taille de la tête, le diamètre des yeux, la courbure du bec, la forme des ailerons ou l'ancrage des pattes au cours du temps.
   - Si la mascotte a une taille anatomique $T$, elle garde $T$ dans TOUTES ses animations et états futurs.
   - Seules les transformations d'animation cinématique (rotations $\theta$, légères translations de respiration $\Delta y \le 4\text{ px}$, compressions/extensions élastiques minimes $0.985\dots 1.015$, clignements de paupières) sont autorisées.
   - Cette règle s'applique à Owluko, AItuko, et à **TOUTES** les mascottes futures sans exception.

---

# 🦉 PARTIE 2 : OWLUKO (La Chouette) — BIBLE DÉTAILLÉE POSE PAR POSE

### 🎯 Fiche Identité & Étalon Canonique (`00_idle`) :
* **Espèce & Morphologie** : Chouette sphérique joufflue, tête parfaitement ronde sans cornes ni aigrettes.
* **Membres Supérieurs** : **Ailes de plumes d'oiseau pures** (strictement AUCUNE main, AUCUN doigt, AUCUN pouce humain).
* **Membres Inférieurs** : Corps posé en boule duveteuse, petites serres dorées rentrées ou délicatement posées.
* **Visage & Bec** : Grands yeux noirs profonds avec double reflet blanc circulaire. Bec doré moyen en cône courbé (`#F59E0B`).
* **Palette Stricte** : Plumes brun doux (`#8B5A2B`), Poitrail crème chaud (`#E4E3D8`), Bec/Serres doré (`#F59E0B`), Yeux obsidienne (`#1E293B`).

---

### Tableau de Correction 2-en-1 : Owluko (13 États)

#### `00_idle` (Repos Actif — Étalon de Référence)
* **Recadrage & Proportions** : Corps centré, hauteur = 70% (358 px), centré horizontalement.
* **Instructions & Prompt** :
  ```text
  [Character Reference: Owluko Idle] 3D stylized chubby round owl mascot standing still on pure solid chroma green (#00FF00). Smooth matte vinyl clay texture, warm brown and soft beige feathers, creamy white chest (#E4E3D8), medium golden-orange hooked beak (#F59E0B), large glossy black eyes with double white specular reflections. Body height exactly 70% of frame height. Gentle breathing motion, occasional gentle eye blink. 3-point neutral 5500K lighting, seamless 4.0s 24fps loop, strictly NO background shadows, NO green spill.
  ```

---

#### `01_waving` (Accueil / Salut)
* **Proportions** : Hauteur corps = 70%, aile levée dans la largeur.
* **Correction d'incohérence** : Aile droite en plumes qui salue (ZÉRO main humaine).
* **Instructions & Prompt** :
  ```text
  [Character Reference: Owluko] Cute 3D round owl mascot on solid chroma green (#00FF00). The owl lifts its right feathered wing (smooth rounded bird wing, strictly NO human fingers, NO thumb) and waves friendly twice before returning to resting pose. Body scale strictly 70% of canvas height, identical creamy chest and golden beak. Seamless 4.0s 24fps loop, 5500K studio lighting.
  ```

---

#### `02_celebrating` (Succès / Célébration)
* **Proportions** : Hauteur corps = 70%, confettis flottant dans les 15% de marge haute.
* **Correction d'incohérence** : Pas de rétrécissement du corps, disparition douce des confettis en fin de boucle.
* **Instructions & Prompt** :
  ```text
  [Character Reference: Owluko] Cute 3D round owl mascot hopping joyfully on solid chroma green (#00FF00). The owl flaps both feathered wings upward in celebration. Colorful small confettis float gently in the top 15% margin and fade out smoothly during the last 0.5s. Body height locked at 70% of frame height (mass conservation). Seamless 4.0s 24fps loop, 24fps.
  ```

---

#### `03_ai_thinking` (Réflexion / Pensée)
* **Proportions** : Hauteur corps = 70%, tête inclinée subtilement.
* **Correction d'incohérence** : Extrémité arrondie de l'aile sous le bec doré, tête lisse sans aigrettes.
* **Instructions & Prompt** :
  ```text
  [Character Reference: Owluko] Cute 3D round owl mascot in thoughtful thinking pose on solid chroma green (#00FF00). Head tilts slightly, rounded feather tip of right wing rests gently under the golden beak, looking upward thoughtfully. Body height strictly 70%, perfectly round head without ear tufts. Seamless 4.0s 24fps loop, 5500K lighting.
  ```

---

#### `04_error_404` (Erreur / Problème) 🔴 *CORRECTION MAJEURE*
* **Proportions** : Hauteur corps = 70%, point d'interrogation dans la marge haute.
* **Corrections d'incohérences** :
  1. **Éclairage** : Conserver l'éclairage 5500K éclatant (supprimer le filtre sombre/terne).
  2. **Ventre** : Restaurer le duvet crème éclatant `#E4E3D8`.
  3. **Bec** : Taille normale moyenne (supprimer le bec géant tombant).
* **Instructions & Prompt** :
  ```text
  [Character Reference: Owluko] Cute 3D round owl mascot in an apologetic confused 404 error pose on solid chroma green (#00FF00). Body height strictly 70% of canvas. Sad puzzled expression, slightly drooping rounded feathered wings, small glowing question mark floating in top 15% margin. Maintain full bright 5500K studio lighting, vibrant creamy-white chest (#E4E3D8) and warm brown feathers. Standard medium golden beak (NO oversized beak), seamless 4.0s 24fps loop.
  ```

---

#### `05_thumbs_up` (Validation / Pouce Haut) 🔴 *CORRECTION MAJEURE*
* **Proportions** : Hauteur corps = 70%.
* **Correction d'incohérence** : **SUPPRESSION TOTALE DU POUCE ET DE LA MAIN HUMAINE**. L'aile de plumes se courbe vers le haut en forme d'approbation stylisée.
* **Instructions & Prompt** :
  ```text
  [Character Reference: Owluko] Cute 3D round owl mascot giving an approval gesture on solid chroma green (#00FF00). Body height strictly 70% of canvas. The owl curves its right feathered wing upward into a cute rounded stylized approval silhouette (pure bird wing with soft feather tip curved up, strictly NO human skin, NO fingers, NO thumb knuckles). Confident happy wink, golden beak, creamy chest, seamless 4.0s 24fps loop, 24fps.
  ```

---

#### `06_sleeping` (Repos / Sommeil)
* **Proportions** : Hauteur corps = 70%, bulles Zzz dans la marge haute.
* **Correction d'incohérence** : Yeux fermés en arcs souriants, corps en boule duveteuse identique à `idle`.
* **Instructions & Prompt** :
  ```text
  [Character Reference: Owluko] Cute 3D round owl mascot sleeping peacefully on solid chroma green (#00FF00). Body height strictly 70%. Eyes closed in curved happy crescent arcs, head slightly nodding in sleep, small translucent Zzz bubbles floating in upper margin. Identical plumage colors, smooth breathing cycle, seamless 4.0s 24fps loop.
  ```

---

#### `07_pointing` (Guide / Direction) 🔴 *CORRECTION MAJEURE*
* **Proportions** : Hauteur corps = 70%.
* **Corrections d'incohérences** :
  1. **ZÉRO index humain** : L'aile droite s'étend en pointe de plumes douce.
  2. **Pattes** : Supprimer la patte grise isolée, corps posé en boule sur son plumage.
  3. **Éclairage** : Atténuer la surexposition sur le poitrail crème.
* **Instructions & Prompt** :
  ```text
  [Character Reference: Owluko] Cute 3D round owl mascot pointing to the right on solid chroma green (#00FF00). Body height strictly 70%. The owl extends its right feathered wing smoothly to the side (pure bird wing feather contour, strictly NO human arm, NO index finger). Body resting in plush rounded pose without protruding solitary grey legs. Balanced lighting on cream chest, seamless 4.0s 24fps loop.
  ```

---

#### `08_searching` (Recherche / Loupe) 🔴 *CORRECTION MAJEURE*
* **Proportions** : Hauteur corps = 70% (en 1080p net, éliminer le fichier 486p flou).
* **Correction d'incohérence** : La loupe est tenue entre les plumes des ailes (ZÉRO doigts humains).
* **Instructions & Prompt** :
  ```text
  [Character Reference: Owluko] Cute 3D round owl mascot holding a classic magnifying glass on solid chroma green (#00FF00). Body height strictly 70%, crisp 1080p resolution. The owl holds the wooden handle between its two feathered wings (feathers wrapping gently around handle, strictly NO human fingers) and peeks curiously through the glass. Seamless 4.0s 24fps loop, 5500K lighting.
  ```

---

#### `09_loading` (Chargement / Sablier) 🔴 *CORRECTION MAJEURE*
* **Proportions** : Hauteur corps = 70%, sablier flottant à côté.
* **Corrections d'incohérences** :
  1. **Crâne** : Supprimer l'aigrette/corne asymétrique sur la tempe droite. Tête 100% ronde.
  2. **Bec** : Bec doré moyen net et distinct.
* **Instructions & Prompt** :
  ```text
  [Character Reference: Owluko] Cute 3D round owl mascot watching a glowing glass hourglass on solid chroma green (#00FF00). Body height strictly 70%. Perfectly smooth spherical round head (strictly NO ear tufts, NO horns, NO asymmetric feathers). The owl tilts its head following the trickling sand, well-defined golden beak, seamless 4.0s 24fps loop, 24fps.
  ```

---

#### `10_idea` (Astuce / Idée) 🔴 *CORRECTION DE PROPORTIONS CRITIQUE*
* **Proportions** : **CORPS MAINTENU À 70% (358 px)**. L'ampoule flotte dans les 15% de marge haute au-dessus du crâne.
* **Correction d'incohérence** : Ne pas réduire le corps d'Owluko à 208 px pour loger l'ampoule.
* **Instructions & Prompt** :
  ```text
  [Character Reference: Owluko] Cute 3D round owl mascot with a bright idea on solid chroma green (#00FF00). The owl's body strictly maintains its full 70% canvas height (350px/512px). A glowing yellow lightbulb pops up floating in the 15% top margin 40px above the head. The owl looks up happily at the bulb. Lightbulb glows, pulses, and fades softly, seamless 4.0s 24fps loop.
  ```

---

#### `11_security` (Sécurité / Bouclier) 🔴 *CORRECTION MAJEURE*
* **Proportions** : Hauteur corps = 70%.
* **Corrections d'incohérences** :
  1. **Bouclier** : Fini métallique argenté et bleu saphir (supprimer la matière dorée sursaturée).
  2. **Colorimétrie** : Zéro reflet jaune projeté sur le ventre crème d'Owluko.
* **Instructions & Prompt** :
  ```text
  [Character Reference: Owluko] Cute 3D round owl mascot holding a sleek metallic security shield on solid chroma green (#00FF00). Body height strictly 70%. The shield has a silver-metallic and sapphire-blue finish with a glowing white checkmark (clean metallic reflection, strictly NO yellow light cast onto the owl's chest). Confident reassuring expression, identical cream belly, seamless 4.0s 24fps loop.
  ```

---

#### `12_goodbye` (Au Revoir / Départ) 🔴 *CORRECTION MAJEURE*
* **Proportions** : Hauteur corps = 70%.
* **Corrections d'incohérences** :
  1. **Bec** : Vrai bec doré moyen de taille normale (restaurer le bec de l'étalon `00_idle`, supprimer le micro-bec).
  2. **Pattes** : Supprimer les longues pattes orange qui marchent. Corps posé en boule peluche.
* **Instructions & Prompt** :
  ```text
  [Character Reference: Owluko] Cute 3D round owl mascot waving farewell on solid chroma green (#00FF00). Body height strictly 70%. The owl holds a small vintage brown suitcase tucked near its side while waving its right feathered wing with a gentle smile. Full-sized golden hooked beak (exact scale of 00_idle, strictly NO tiny shrinking beak), body sitting in standard round plush pose without anomalous protruding orange legs, seamless 4.0s 24fps loop.
  ```

---

# 🤖 PARTIE 3 : AITUKO (Le Robot) — BIBLE DÉTAILLÉE

### 🎯 Fiche Identité & Étalon Canonique (`00_idle`) :
* **Morphologie** : Robot flottant high-tech mignon, tête ovale avec écran facial noir et yeux LED cyan (`#00F0FF`).
* **Matériaux** : Coque blanc céramique (`#F8FAFC`), métal brossé gris ardoise (`#334155`), bouton d'accent orange (`#FF6B00`).
* **Lévitation** : Flotte à 15% au-dessus du bas de cadre avec une oscillation douce ($\pm 8\text{px}$).

### Consignes de Correction 2-en-1 par Animation :
* **`00_idle` à `09_loading`, `11_security`, `12_goodbye`** :
  * Hauteur du corps du robot verrouillée à **70% de la hauteur du cadre**.
  * Écran facial toujours noir brillant avec reflets cyan néon nets.
* **`04_error_404`** : Yeux LED affichant `404` ou des croix `X X` en rouge ou orange vif, petite fumée cartoon en haut, coque restant blanc céramique propre.
* **`10_idea` (Correction Proportions)** : Le corps d'AItuko doit faire **70% de la hauteur**. L'ampoule holographique flotte au-dessus de son antenne dans la marge supérieure de 15%.
* **`06_sleeping`** : Écran en veille avec yeux fermés en arcs bleus doux `-_-`, lévitation basse ralentie.

---

# 🐱 PARTIE 4 : LUNEKO (Le Chat Roux) — BIBLE DÉTAILLÉE

### 🎯 Fiche Identité & Étalon Canonique (`00_idle`) :
* **Morphologie** : Chaton roux tigré mignon, oreilles pointues, grand poitrail blanc, yeux émeraude (`#10B981`), coussinets rose pâle (`#FFB6C1`).
* **Règle Fond Vert / Fond Bleu** : En raison des yeux émeraudes, **utiliser un fond bleu pur `#0000FF`** si le vert crée un conflit de découpe (*Chroma Key Conflict*).

### Consignes de Correction 2-en-1 par Animation :
* **`00_idle` à `05_thumbs_up`, `07_pointing`, `09_loading` à `12_goodbye`** :
  * Hauteur corporelle debout verrouillée à **70% du cadre**.
  * `05_thumbs_up` & `07_pointing` : Patte de chat douce avec coussinets roses (pas de main humaine).
* **`06_sleeping` & `08_searching` (Règle Spéciale Quadrupède / Masse)** :
  * Sur `06_sleeping` (en boule) et `08_searching` (à 4 pattes au sol) : **La tête et le volume du chat restent à l'échelle 1:1 de `00_idle`** (largeur corporelle de 74% du cadre, hauteur de 50%). Ne jamais étirer verticalement le chat.
* **`10_idea` (Correction Proportions)** : Corps à 70%, ampoule flottant au-dessus des oreilles.

---

# 📋 PARTIE 5 : HATOKO, USAKO & INUKO (Le Reste du Set)

| Mascotte | Espèce | Règle Anatomique Clé | Règle de Proportion |
| :--- | :--- | :--- | :--- |
| **Hatoko** | Pigeon / Colombe | Ailes de plumes douces grises/blanches, bec orange délicat, zéro main humaine sur `thumbs_up` et `pointing`. | Corps à 70% de hauteur, tête ronde sans déformation. |
| **Usako** | Lapin Blanc | Longues oreilles dressées contenues dans la marge haute (ne pas couper les oreilles), nez rose pastel, queue pompon. | Corps à 65-70%, oreilles dans les 15% supérieurs. |
| **Inuko** | Chien Shiba | Pelage fauve et blanc, queue enroulée sur le dos, oreilles triangulaires dressées, truffe noire. | Corps assis ou debout à 70% de hauteur. |

---

# 🚀 SYNTHÈSE DES DIRECTIVES À TRANSMETTRE À L'OPÉRATEUR / GÉNÉRATEUR

1. **Règle de Cadrage Universelle** : "Chaque vidéo doit être livrée en 1080p sur fond vert pur `#00FF00`. Le corps principal du personnage doit impérativement mesurer 70% de la hauteur de l'image (756 px / 1080 px) avec le sommet de la tête aligné à Y = 15%."
2. **Règle des Accessoires Flottants** : "Les ampoules, étoiles, confettis et boucliers doivent occuper les 15% supérieurs sans jamais rapetisser le corps de la mascotte."
3. **Règle d'Anatomie Animale Stricte** : "Interdiction formelle de générer des doigts, mains, pouces ou bras humains sur les oiseaux (Owluko, Hatoko) ou animaux (Luneko, Usako, Inuko). Pour saluer, pointer ou valider, utiliser uniquement les ailes de plumes ou les pattes animales stylisées."
4. **Fidélité au Fichier `00_idle`** : "Toutes les couleurs, teintes de bec, reflets d'yeux et finitions de texture doivent être calquées à 100% sur l'image de référence `00_idle`."
