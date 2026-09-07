# 🦉 Rapport Statistique d'Incohérence : Owluko
> **Audit exhaustif et matrice d'anomalies des 13 animations d'Owluko basé sur l'étalon canonique `00_idle`.**

---

## 📊 1. Statistiques Globales du Set d'Animations

* **Animations Totalement Conformes (0 défaut)** : **2 / 13** (`15.4%`) $\rightarrow$ `00_idle`, `03_ai_thinking`
* **Animations avec Défauts Mineurs (1 à 2 défauts)** : **4 / 13** (`30.8%`) $\rightarrow$ `01_waving`, `06_sleeping`, `10_idea`, `12_goodbye`
* **Animations avec Défauts Majeurs (3 défauts ou plus)** : **7 / 13** (`53.8%`) $\rightarrow$ `02_celebrating`, `04_error_404`, `05_thumbs_up`, `07_pointing`, `08_searching`, `09_loading`, `11_security`
* **Nombre Total d'Incohérences Détectées sur le Set** : **32 anomalies**

---

## 📋 2. Tableau Récapitulatif par Animation (Nombre d'Incohérences & Détails)

| # | Animation | Nb Défauts | 1. Pattes / Serres | 2. Ailes vs Mains | 3. Bec & Visage | 4. Tête / Aigrettes | 5. Couleur / Lumière | 6. Statique vs Vidéo | 7. Looping Vidéo | Sévérité |
| :-: | :--- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| **00** | **00_idle** | **0** | ✅ Conforme | ✅ Conforme | ✅ Conforme | ✅ Conforme | ✅ Conforme | ✅ Conforme | ✅ Conforme | 🟢 **ÉTALON** |
| **01** | **01_waving** | **2** | ✅ Conforme | ✅ Conforme | ✅ Conforme | ✅ Conforme | 🟡 $\Delta E = 3.1$ | 🔴 Pose différente | ✅ Conforme | 🟡 **Faible** |
| **02** | **02_celebrating** | **3** | ✅ Conforme | ✅ Conforme | ✅ Conforme | ✅ Conforme | 🟡 $\Delta E = 4.2$ | 🔴 Pose différente | 🟡 Sursaut ($RMS 14.1$) | 🟠 **Moyenne** |
| **03** | **03_ai_thinking** | **0** | ✅ Conforme | ✅ Conforme | ✅ Conforme | ✅ Conforme | ✅ $\Delta E = 1.7$ | ✅ Conforme | ✅ Conforme | 🟢 **Parfait** |
| **04** | **04_error_404** | **4** | 🟡 Pattes masquées | ✅ Conforme | 🔴 Bec géant ($7022\text{px}$) | ✅ Conforme | 🔴 $\Delta E 11.1$ / $\Delta L^* -7.5$ | 🔴 Cadrage différent | ✅ Conforme | 🔴 **Critique** |
| **05** | **05_thumbs_up** | **3** | ✅ Conforme | 🔴 **Pouce humain** | ✅ Conforme | ✅ Conforme | 🟡 $\Delta E = 5.3$ | 🔴 Pose différente | ✅ Conforme | 🔴 **Critique** |
| **06** | **06_sleeping** | **1** | ✅ Conforme | ✅ Conforme | 🟡 Bec petit | ✅ Conforme | ✅ $\Delta E = 1.9$ | ✅ Conforme | ✅ Conforme | 🟢 **Très Bon** |
| **07** | **07_pointing** | **4** | 🔴 1 seule patte grise | 🔴 **Index humain** | 🟡 Bec surdimensionné | ✅ Conforme | 🟡 Ventre surexposé | 🔴 Pose très divergente | ✅ Conforme | 🔴 **Critique** |
| **08** | **08_searching** | **4** | 🟡 Pattes masquées | 🔴 **Main préhensile** | ✅ Conforme | ✅ Conforme | 🟡 Reflets loupe | 🔴 **Basse Définition 486p** | ✅ Conforme | 🔴 **Critique** |
| **09** | **09_loading** | **4** | 🟡 Pattes masquées | 🟡 Aile déformée | 🔴 Bec écrasé | 🔴 **Aigrette parasite** | 🟡 Dominante dorée | 🔴 **Basse Définition 486p** | 🟡 Sursaut ($RMS 15.2$) | 🔴 **Critique** |
| **10** | **10_idea** | **2** | ✅ Conforme | ✅ Conforme | 🟡 Bec comprimé | ✅ Conforme | 🟡 Halo ampoule | 🔴 Pose différente | 🟡 Sursaut clignotement | 🟡 **Faible** |
| **11** | **11_security** | **4** | 🔴 Serres vertes/or | 🟡 Aile masquée | ✅ Conforme | ✅ Conforme | 🔴 **Pollution jaune $\Delta E 11.5$** | 🔴 Pose différente | 🟡 Sursaut ($RMS 14.1$) | 🔴 **Critique** |
| **12** | **12_goodbye** | **3** | 🔴 **Pattes brun-orange** | ✅ Conforme | 🔴 **Bec minuscule ($447\text{px}$)** | ✅ Conforme | ✅ $\Delta E = 1.9$ | 🔴 Pose différente | ✅ Conforme | 🟠 **Moyenne** |

---

## 🔍 3. Analyse Détaillée par Catégorie de Défaut

### 1. 🦶 Les Incohérences de Pattes / Serres (6 animations affectées)
* **`00_idle`** : Pattes douces et rentrées sous le duvet.
* **`12_goodbye`** : Deux grandes pattes émergent avec une couleur **brun-orangé chaud (`#9C802D`)**.
* **`11_security`** : Pattes teintées de **jaune verdâtre (`#9BB45A`)** à cause du bouclier.
* **`07_pointing`** : **Une seule patte visible**, teintée en gris-brun sombre (`#6D5E45`).
* **`04_error_404`, `08_searching`, `09_loading`** : Pattes totalement absentes/tronquées au sol.

### 2. 🖐️ Les Mutations Ailes ⇄ Mains Humaines (3 animations affectées)
* **`05_thumbs_up`** : Mutation en main humaine avec **pouce levé distinct**.
* **`07_pointing`** : Mutation en bras humain avec **index pointé**.
* **`08_searching`** : Doigts humains tenant le manche en bois de la loupe.

### 3. 👃 Les Déformations & Disparitions du Bec (4 animations affectées)
* **`00_idle` (Étalon)** : Bec doré équilibré de **`4 210 px`**.
* **`12_goodbye`** : Bec réduit à une micro-tache de **`447 px`** (**-89.4%** de surface !).
* **`04_error_404`** : Bec pointu exagéré de **`7 022 px`** (**+66.8%** de surface).
* **`09_loading`** : Bec plat écrasé contre le sablier.

### 4. 🦱 Silhouette de Crâne & Aigrettes Parasites (1 animation affectée)
* **`09_loading`** : Apparition d'une **aigrette/corne de plume asymétrique** sur la droite du crâne (type grand-duc), rompant la tête ronde de la chouette.

### 5. 🎨 Colorimétrie & Éclairage (7 animations affectées)
* **`04_error_404`** : Sous-exposition sévère ($\Delta L^* = -7.5$, $\Delta E = 11.1$).
* **`11_security`** : Pollution lumineuse jaune du bouclier ($\Delta E = 11.5$, Warmth $+0.18$).
* **`07_pointing` & `08_searching`** : Blanchiment du poitrail par surexposition locale.

### 6. 📁 Fichiers Sources Dégradés & Conflits Statique vs Vidéo (10 animations affectées)
* **`08_searching` & `09_loading`** : Fichiers statiques livrés en **486p (864×486)** avec fond vert sombre et bruité (`RGB: 38, 196, 6`) au lieu de 768p pur (`RGB: 5, 252, 4`).
* **8 autres poses** : Décalage de pose flagrant entre le fichier image JPEG et le premier photogramme de la vidéo MP4.

### 7. ⏱ Looping & Continuité Cinétique (4 animations affectées)
* **`02_celebrating`, `09_loading`, `10_idea`, `11_security`** : Rupture de raccordement en fin de cycle ($RMS > 12.0$), créant un micro-saut visuel à la boucle.
