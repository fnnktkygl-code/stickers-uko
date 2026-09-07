# 🛠️ Guide des Prompts de Correction Chirurgicale : Owluko
> **Inpainting & Instruct-Edit Prompts** pour corriger les anomalies directement sur les images/vidéos existantes (*Runway Inpaint/Gen-3, Midjourney Vary Region, Photoshop Generative Fill, ControlNet Inpaint, Kling Motion Brush / Edit*).

---

## 🎯 Principe de Fonctionnement
Pour chaque animation problématique, vous appliquez un **masque de sélection (Inpainting)** sur la zone à corriger, puis vous collez le prompt de modification ciblé.

---

### `05_thumbs_up` (Validation) 🔴 *CORRECTION DE L'AILE / MAIN HUMAINE*
* **Zone à masquer (Inpainting Mask)** : L'aile droite (la main et le pouce).
* **Prompt de Correction (Instruct / Edit Prompt)** :
  ```text
  Replace the human hand, thumb, and fingers with a smooth rounded owl feathered wing curved upward in a stylized wing-tip thumbs-up silhouette. Exact matching warm brown and beige feather texture, soft plush toy material. Strictly NO human skin, NO fingers, NO thumb knuckles.
  ```
* **Contrainte de préservation** : Laisser le corps, le visage, le clin d'œil et le fond vert 100% intacts.

---

### `07_pointing` (Guide) 🔴 *CORRECTION DU BRAS / INDEX & DE LA PATTE*
* **Zone à masquer 1** : L'aile droite (le bras et l'index tendu).
  * **Prompt de Correction** :
    ```text
    Replace the human arm and pointing index finger with a tapered bird wing covered in soft brown feathers extending smoothly to the right. Pure owl wing silhouette.
    ```
* **Zone à masquer 2** : Le bas du corps (la patte grise solitaire).
  * **Prompt de Correction** :
    ```text
    Remove the protruding solitary grey foot, tuck legs beneath the soft creamy feathers of the lower belly in a clean plush resting pose.
    ```

---

### `12_goodbye` (Au Revoir) 🔴 *CORRECTION DU BEC MINUSCULE & DES PATTES ORANGE*
* **Zone à masquer 1** : Le bec au centre du visage.
  * **Prompt de Correction** :
    ```text
    Enlarge and restore the golden-orange hooked beak to standard medium proportion (exact size and shape as 00_idle reference), smooth polished golden-yellow cone centered between the eyes.
    ```
* **Zone à masquer 2** : Le bas du corps (les longues pattes orange qui marchent).
  * **Prompt de Correction** :
    ```text
    Remove the long orange walking feet, replace with the owl sitting in a cute rounded compact body shape with feet tucked into the lower plumage.
    ```

---

### `04_error_404` (Erreur) 🔴 *CORRECTION DE L'EXPOSITION SOMBRE & DU BEC GÉANT*
* **Zone à masquer 1** : Le bec tombant disproportionné.
  * **Prompt de Correction** :
    ```text
    Resize the oversized drooping beak down to standard medium golden hooked beak, maintaining a cute sad expression without facial distortion.
    ```
* **Prompt Global (Color / Lighting Edit)** :
  ```text
  Brighten overall scene exposure by +20%, adjust color grading to neutral 5500K studio light, restore vibrant creamy-white chest feathers and rich warm brown plumage (remove dark gloomy wash).
  ```

---

### `09_loading` (Chargement) 🔴 *CORRECTION DE L'AIGRETTE PARASITE SUR LE CRÂNE*
* **Zone à masquer** : La tempe droite et le dessus droit du crâne (la corne de plume).
* **Prompt de Correction** :
  ```text
  Remove the asymmetric pointy feather tuft / horn on the right temple, smooth the head contour into a perfectly continuous round spherical dome.
  ```

---

### `11_security` (Sécurité) 🔴 *CORRECTION DE LA POLLUTION JAUNE DU BOUCLIER*
* **Zone à masquer** : Le bouclier et la moitié inférieure du poitrail.
* **Prompt de Correction** :
  ```text
  Change shield material to sleek brushed silver metal and deep sapphire blue, eliminate all yellow/orange light reflection cast onto the owl's creamy white chest feathers.
  ```

---

### `08_searching` (Recherche) 🔴 *CORRECTION DES DOIGTS SUR LA LOUPE*
* **Zone à masquer** : Les extrémités des ailes tenant le manche de la loupe.
* **Prompt de Correction** :
  ```text
  Replace human fingers gripping the wooden handle with soft rounded feathered wing tips gently wrapping around the handle. High definition, crisp textures.
  ```

---

### `02_celebrating` (Célébration) 🟡 *CORRECTION DU RACCORD DE BOUCLE*
* **Prompt Cinétique / Loop Edit** :
  ```text
  Fade out confetti particles smoothly in the last 12 frames (0.5s) to allow a seamless invisible loop back to the initial jumping frame.
  ```

---

### `10_idea` (Idée) 🟡 *CORRECTION DE L'ESPACE HAUTEUR (HEADROOM)*
* **Prompt de Recadrage / Échelle** :
  ```text
  Keep the owl body at exactly 70% of canvas height (350px/512px), place the glowing yellow lightbulb 40px floating strictly in the upper margin above the head without shrinking the character.
  ```
