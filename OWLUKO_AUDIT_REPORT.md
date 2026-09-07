# 🦉 Rapport d'Audit de Cohérence : Owluko
> **Audit scientifique complet des 13 états d'Owluko basé sur l'étalon canonique `00_idle`.**

---

## 🎯 Étalon Canonique de Référence : `00_idle`
* **Fichier source** : `owluko_idle.jpeg` / `owluko_idle.mp4`
* **Luminosité moyenne ($L^*$)** : **`80.1`** (Exposition studio neutre 5500K)
* **Indice de Chaleur ($R/B$)** : **`1.10`**
* **Palette Dominante** : 
  * Ventre Crème : `#E4E3D8` (70.9% de surface)
  * Plumes Tête/Dos : `#72592D` / `#8B5A2B`
  * Bec & Serres : `#F59E0B` (2.1% de surface)
  * Yeux : Noir profond `#1E293B` avec reflets blancs doubles
* **Vidéo de référence** : 4.00s, 24.0 fps, 96 frames, Boucle sans raccord visible ($RMS = 3.8$).

---

## 📊 Tableau Synthétique de Conformité

| État | Pose / Action | Écart Couleur ($\Delta E$) | Écart Lumière ($\Delta L^*$) | Continuité Boucle ($RMS$) | Diagnostic Global |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **00_idle** | Repos Actif *(Étalon)* | `0.0` | `+0.0` | `3.8` | 🟢 **100% Conforme (Référence)** |
| **01_waving** | Accueil / Salut | `3.1` | `-1.8` | `2.4` | 🟢 **Excellente conformité** |
| **02_celebrating** | Succès / Confettis | `4.2` | `-1.2` | `14.1` | 🟡 **Bon** *(Confettis VFX)* |
| **03_ai_thinking** | Réflexion | `1.7` | `-1.0` | `5.9` | 🟢 **Parfait** |
| **04_error_404** | Erreur / Triste | **`11.1`** | **`-7.5`** | `7.4` | 🔴 **Anomalie d'exposition & teinte** |
| **05_thumbs_up** | Validation | `5.3` | `-1.0` | `2.8` | 🟢 **Bonne conformité** |
| **06_sleeping** | Sommeil | `1.9` | `-0.7` | `6.7` | 🟢 **Parfait** |
| **07_pointing** | Guide / Direction | **`6.0`** | `-0.2` | `1.9` | 🟡 **Ventre surexposé/blanchi** |
| **08_searching** | Loupe / Recherche | `5.4` | `+2.5` | `2.5` | 🟡 **Reflets loupe sur le ventre** |
| **09_loading** | Sablier / Attente | `4.9` | `+0.2` | `15.2` | 🟡 **Micro-saut de boucle sablier** |
| **10_idea** | Astuce / Ampoule | `4.1` | `-1.8` | `12.2` | 🟢 **Bon** *(Échelle 350px corrigée)* |
| **11_security** | Bouclier / Sécurité | **`11.5`** | `+0.5` | `14.1` | 🔴 **Pollution jaune du bouclier** |
| **12_goodbye** | Au Revoir | `1.9` | `-0.7` | `4.2` | 🟢 **Parfait** |

---

## 🔍 Analyse Détaillée des 3 Anomalies Identifiées

### 🔴 1. Pose `04_error_404` : Sous-exposition et dérive du ventre crème
* **Le problème** : 
  * La luminosité générale chute de **-7.5 points** ($L^* = 72.6$ vs $80.1$ sur idle).
  * Le ventre crème perd sa pureté et devient grisâtre/brun délavé (`RGB: 197, 165, 144` au lieu de `196, 196, 180`).
  * La surface crème visible s'effondre à **42.5%** (contre 70.9% sur idle).
* **Cause IA** : L'IA a "dramatisé" la scène en assombrissant l'éclairage studio au lieu de garder le setup 5500K neutre.
* **Correction à exiger** : Remonter l'exposition globale de +7.5 points et rétablir le blanc-crème d'origine sur le ventre.

---

### 🔴 2. Pose `11_security` : Pollution chromatique du bouclier
* **Le problème** :
  * Écart de couleur le plus élevé de tout le set (**$\Delta E = 11.5$**).
  * L'indice de chaleur monte à **$1.28$** (+0.18 par rapport à idle), créant une dominante très jaune/ambrée.
  * Le bouclier doré masque la moitié du ventre (crème réduit à 48.5%) et projette une lumière jaune sur les plumes du bas.
* **Cause IA** : Réflexion de lumière de l'accessoire non maîtrisée.
* **Correction à exiger** : Définir un matériau de bouclier plus neutre (argent/métal ou bleu nuit Uko) ou neutraliser les rebonds jaunes sur le plumage.

---

### 🟡 3. Poses `07_pointing` & `08_searching` : Blanchiment / Surexposition locale
* **Le problème** :
  * Le ventre crème d'Owluko est "brûlé" par une lumière trop forte (la zone claire passe à **87.0%** en `pointing` et **90.7%** en `searching` contre 70.9% sur idle).
  * Sur `searching`, le reflet de verre de la loupe décolore le poitrail.
* **Correction à exiger** : Atténuer la lumière d'appoint (Fill Light) à droite pour préserver la nuance texturée crème/beige du poitrail.

---

## 🎬 Anomalies de Looping Vidéo (Cinétique)
* **`09_loading`** ($RMS = 15.2$) & **`02_celebrating`** ($RMS = 14.1$) :
  * Présentent un léger sursaut lors du passage de la frame 96 à la frame 01 (rotation du sablier / disparition des confettis).
  * **Correction** : Raccorder la dernière frame pour que la rotation ou la retombée des particules se termine exactement en cycle continu.
