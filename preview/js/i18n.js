/**
 * Uko UI — Moteur d'Internationalisation Centralisé (i18n)
 * Hardened & High-Performance Edition:
 * - 7 Langues Natives Intégrales (EN, FR, ES, DE, JA, PT, ZH)
 * - Allowlist Stricte d'Attributs (Sécurité Anti-XSS)
 * - Mémoïsation des Clés & Batching requestAnimationFrame (Haute Réactivité 60fps)
 * - Résilience Réseau, Messages Système & Termes de Licence
 */

const TRANSLATIONS = {
  "fr": {
    "meta": {
      "title": "Uko UI — Système de Mascottes Animées pour Interfaces Modernes",
      "desc": "Mascottes animées 3D, bulles de dialogue interactives et composants légers pour React, Next.js et Flutter."
    },
    "nav": {
      "studio": "Studio",
      "catalogue": "Catalogue",
      "integration": "Intégration",
      "pricing": "Tarifs",
      "freeSample": "Pack Gratuit",
      "lang": "Changer de langue",
      "themeDark": "Mode Sombre",
      "themeLight": "Mode Clair"
    },
    "hero": {
      "badge": "Mascottes 3D & Micro-Interactions",
      "titleStart": "Donnez une âme",
      "titleHighlight": "à vos interfaces",
      "titleEnd": "en 3 lignes de code.",
      "subtitle": "Système de mascottes animées 3D ultra-légères. 12 états universels pour booster la rétention, l'onboarding et l'engagement de vos utilisateurs.",
      "ctaStudio": "Tester dans le Studio",
      "ctaCatalogue": "Voir le Catalogue",
      "trust": "Prêt pour la production • 100% WebP & Code React / Flutter"
    },
    "studio": {
      "downloadPackBtn": "Télécharger {name}",
      "quickFreeBtn": "⚡ Essai Gratuit (0 €)",
      "quickProBtn": "📦 Obtenir le Pack (Dès 5 €)",
      "quickBarStatus": "{name} — 12 états animés 3D prêts à l'intégration",
      "badge": "Studio Interactif",
      "title": "Testez & Personnalisez en Temps Réel",
      "desc": "Basculez entre les mascottes, ajustez les messages et exportez le code instantanément.",
      "bubbleOn": "Bulle : Active",
      "bubbleOff": "Bulle : Masquée",
      "bubbleToggleLabel": "Bulle de dialogue",
      "bubbleToggleTitle": "Masquer / Afficher la bulle de message",
      "bubbleOptional": "Optionnel",
      "bubblePlaceholder": "Tapez votre message...",
      "bubbleClickToHide": "Cliquez pour masquer la bulle",
      "prevPose": "Pose précédente (←)",
      "nextPose": "Pose suivante (→)",
      "sizeLabel": "Taille",
      "renderLabel": "Rendu",
      "formatWebp": "WebP Animé",
      "formatPng": "PNG Statique",
      "copyCode": "Copier",
      "copied": "Copié !",
      "bgAuto": "Fond Automatique",
      "bgDark": "Fond Sombre",
      "bgBlack": "Noir Pur",
      "bgStone": "Fond Clair Washi",
      "bgChecker": "Grille de Transparence"
    },
    "poses": {
      "waving": "Accueil",
      "celebrating": "Succès",
      "ai_thinking": "Réflexion",
      "error_404": "Erreur 404",
      "thumbs_up": "Validation",
      "sleeping": "Repos",
      "pointing": "Guide",
      "searching": "Recherche",
      "loading": "Chargement",
      "idea": "Astuce",
      "security": "Sécurité",
      "goodbye": "Au revoir"
    },
    "messages": {
      "aituko": {
        "waving": "Bienvenue sur votre espace !",
        "celebrating": "Paiement validé avec succès !",
        "ai_thinking": "L'IA analyse vos données...",
        "error_404": "Page introuvable.",
        "thumbs_up": "Parfait, c'est enregistré !",
        "sleeping": "Mode veille activé...",
        "pointing": "Cliquez ici pour démarrer !",
        "searching": "Recherche en cours...",
        "loading": "Chargement de votre profil...",
        "idea": "Astuce : utilisez les raccourcis clavier !",
        "security": "Connexion 100% sécurisée.",
        "goodbye": "À très bientôt sur l'application !"
      },
      "owluko": {
        "waving": "Coucou ! Bienvenue à bord !",
        "celebrating": "Objectif atteint ! Bravo !",
        "ai_thinking": "Je réfléchis à la meilleure solution...",
        "error_404": "Oups ! Nid introuvable.",
        "thumbs_up": "C'est validé par la chouette !",
        "sleeping": "Zzz... Petite sieste de jour...",
        "pointing": "Regarde par ici !",
        "searching": "Je scrute l'horizon...",
        "loading": "Synchronisation du savoir...",
        "idea": "J'ai une idée lumineuse !",
        "security": "Données protégées sous mon aile.",
        "goodbye": "Bon vol et à bientôt !"
      },
      "luneko": {
        "waving": "Miaou ! Ravi de vous rencontrer !",
        "celebrating": "Youpi ! C est une victoire éclatante !",
        "ai_thinking": "Le chaton réfléchit à toute vitesse...",
        "error_404": "Oups ! La pelote s est emmêlée (404).",
        "thumbs_up": "Coup de patte validé à 100% !",
        "sleeping": "Ronron... Sieste réparatrice...",
        "pointing": "Par ici, regarde la nouveauté !",
        "searching": "Je furette partout pour trouver ça...",
        "loading": "Chargement tout doux en cours...",
        "idea": "Eurêka ! J ai une super astuce !",
        "security": "Espace ultra sécurisé sous ma garde !",
        "goodbye": "À très vite, prends soin de toi !"
      },
      "hatoko": {
        "waving": "Roucoule ! Prêt à livrer vos messages !",
        "celebrating": "Courrier livré ! Célébrons ce succès !",
        "ai_thinking": "Je calcule la route la plus rapide...",
        "error_404": "Oups ! Courrier égaré en vol (404).",
        "thumbs_up": "Message bien reçu et validé !",
        "sleeping": "Zzz... Repos au nid avant le vol...",
        "pointing": "C'est par là, suivez la trajectoire !",
        "searching": "Je survole la zone pour vous...",
        "loading": "En plein vol vers votre destination...",
        "idea": "Une idée express vient d'atterrir !",
        "security": "Vos plis sont sous scellé sécurisé.",
        "goodbye": "Bonne route et bon vent !"
      },
      "usako": {
        "waving": "Hop là ! Prêt pour un sprint éclair !",
        "celebrating": "Victoire éclatante ! Record battu !",
        "ai_thinking": "Mes moustaches analysent les données...",
        "error_404": "Oups ! Fausse piste dans le terrier (404).",
        "thumbs_up": "Validation éclair à 100% !",
        "sleeping": "Zzz... Micro-sieste de sprinteur...",
        "pointing": "Fonce par ici, c'est la bonne voie !",
        "searching": "Je furette à la vitesse de l'éclair...",
        "loading": "Accélération maximale en cours...",
        "idea": "Bond de génie ! J'ai la solution !",
        "security": "Zone protégée par mes réflexes d'acier.",
        "goodbye": "À toute vitesse, à très bientôt !"
      },
      "inuko": {
        "waving": "汪汪！忠诚护卫 Inuko 前来报到！",
        "celebrating": "任务圆满完成，太棒了！",
        "ai_thinking": "敏锐嗅觉正在分析最优解...",
        "error_404": "气味消失了... 这里什么都没有 (404)。",
        "thumbs_up": "100% 忠诚认证与批准！",
        "sleeping": "Zzz... 保持警惕的守护小憩...",
        "pointing": "往这边走，跟随忠实的向导！",
        "searching": "正在精准搜寻您所需的数据...",
        "loading": "守护巡视加载中...",
        "idea": "灵敏直觉！找到完美方案了！",
        "security": "防线已加锁，提供全方位安全防护。",
        "goodbye": "时刻忠诚守候，期待下次再见！"
      },
      "inuko": {
        "waving": "Au au! Guardião Inuko pronto pro dever!",
        "celebrating": "Missão cumprida com maestria!",
        "ai_thinking": "Farejando as melhores opções...",
        "error_404": "Rastro perdido... Nada por aqui (404).",
        "thumbs_up": "Aprovado com 100% de confiança!",
        "sleeping": "Zzz... Soneca de guarda vigilante...",
        "pointing": "Por aqui, siga o seu guia leal!",
        "searching": "Rastreando os dados que você precisa...",
        "loading": "Patrulha ativa em andamento...",
        "idea": "Faro apurado! Encontrei a resposta!",
        "security": "Perímetro totalmente blindado e seguro.",
        "goodbye": "Sempre fiel ao seu lado, até breve!"
      },
      "inuko": {
        "waving": "ワン！忠実な番犬イヌコ、任務開始！",
        "celebrating": "見事クリア！大成功です！",
        "ai_thinking": "鋭い嗅覚で最適解を分析中...",
        "error_404": "クーン... 痕跡が見つかりません (404)。",
        "thumbs_up": "忠誠を込めて完全承認！",
        "sleeping": "Zzz... 警戒しながらお昼寝中...",
        "pointing": "こちらです、僕についてきてください！",
        "searching": "必要なデータを鋭く捜索中...",
        "loading": "パトロール巡回中...",
        "idea": "ピンときた！解決策を発見！",
        "security": "強固なセキュリティで完全防衛。",
        "goodbye": "いつもお傍にいます。またね！"
      },
      "inuko": {
        "waving": "Wuff! Wächter Inuko meldet sich zum Dienst!",
        "celebrating": "Mission mit Bravour erfüllt!",
        "ai_thinking": "Mein Spürsinn analysiert die Daten...",
        "error_404": "Spur verloren... Hier ist nichts (404).",
        "thumbs_up": "Zu 100% freigegeben und bestätigt!",
        "sleeping": "Zzz... Kurze Wachpause eingelegt...",
        "pointing": "Hier entlang, folge meinem Schutz!",
        "searching": "Spüre die gesuchten Daten auf...",
        "loading": "Aktiver Rundgang läuft...",
        "idea": "Scharfer Instinkt! Lösung gefunden!",
        "security": "Bereich lückenlos abgesichert.",
        "goodbye": "Stets treu an deiner Seite, bis bald!"
      },
      "inuko": {
        "waving": "¡Guau! ¡Inuko el guardián al servicio!",
        "celebrating": "¡Misión cumplida con éxito rotundo!",
        "ai_thinking": "Rastreando la mejor solución...",
        "error_404": "Pista perdida... Nada por aquí (404).",
        "thumbs_up": "¡Aprobado con total lealtad!",
        "sleeping": "Zzz... Siesta de guardia con un ojo atento...",
        "pointing": "¡Por aquí, sigue a tu guía fiel!",
        "searching": "Rastreando los datos al detalle...",
        "loading": "Patrulla activa en curso...",
        "idea": "¡Instinto agudo! ¡Tengo la respuesta!",
        "security": "Perímetro totalmente protegido.",
        "goodbye": "¡Siempre leal, hasta pronto!"
      },
      "inuko": {
        "waving": "Woof! Guardian Inuko reporting for duty!",
        "celebrating": "Mission accomplished with honor!",
        "ai_thinking": "Tracking down the optimal route...",
        "error_404": "Scent lost... Nothing found here (404).",
        "thumbs_up": "100% verified and approved!",
        "sleeping": "Zzz... Guard power-nap in progress...",
        "pointing": "Right this way, follow my lead!",
        "searching": "Sniffing out the exact data you need...",
        "loading": "Active patrol in progress...",
        "idea": "Sharp instinct! I found the answer!",
        "security": "Perimeter locked and fully secured.",
        "goodbye": "Stay safe and see you soon!"
      },
      "inuko": {
        "waving": "Wouf ! Gardien Inuko au rapport !",
        "celebrating": "Mission accomplie avec brio !",
        "ai_thinking": "Mon flair détecte les meilleures options...",
        "error_404": "Piste perdue... Rien à cet endroit (404).",
        "thumbs_up": "Approuvé par le flair d'Inuko !",
        "sleeping": "Zzz... Un œil toujours ouvert en garde...",
        "pointing": "C'est par là, suivez le guide loyal !",
        "searching": "Je traque l'information à la trace...",
        "loading": "Patrouille active en cours de chargement...",
        "idea": "Flair affûté ! J'ai trouvé la solution !",
        "security": "Périmètre sous protection rapprochée.",
        "goodbye": "Toujours fidèle au poste, à bientôt !"
      }
    },
    "catalogue": {
      "badge": "Univers des Personnages",
      "title": "Catalogue des Mascottes Uko",
      "desc": "Chaque mascotte dispose de sa propre personnalité et de 12 états d'animation harmonisés.",
      "available": "Disponible",
      "soon": "Bientôt",
      "aitukoDesc": "Assistant IA • Accueil & Onboarding",
      "owlukoDesc": "Guide de Sagesse • Aide & Connaissance",
      "lunekoName": "Luneko",
      "lunekoDesc": "Compagnon Ludique • Engagement & Fun",
      "inukoName": "Inuko",
      "inukoDesc": "Gardien Athlétique • Fidélité & Sécurité",
      "hatokoName": "Hatoko",
      "hatokoDesc": "Messager Express • Notifications & Push",
      "usakoName": "Usako",
      "usakoDesc": "Sprinteur Agile • Raccourcis & Vitesse",
      "voteTitle": "Vote Mascotte",
      "voteSubtitle": "Votez en 1 clic pour le prochain animal :",
      "voteCountSuffix": "votes",
      "votedBadge": "Voté ✓",
      "voteCancelMsg": "Vote pour {name} annulé.",
      "voteSuccessMsg": "Vote pour {name} enregistré ! ✨",
      "suggestionPrompt": "Autre idée ? Ex: Loutre...",
      "suggestBtn": "Suggérer",
      "suggestSuccessMsg": "Suggestion « {val} » ajoutée aux propositions ! ✨"
    },
    "candidates": {
      "kumako": "🐻 Kumako (Ours)",
      "kitsuko": "🦊 Kitsuko (Renard)",
      "panduko": "🐼 Panduko (Panda)",
      "duckuko": "🦆 Duckuko (Canard)"
    },
    "pricing": {
      "freeDownloadStarted": "{name} — Pack Découverte téléchargé avec succès ! 🎉",
      "badge": "Tarifs Clairs",
      "title": "Tarifs Clairs & Sans Abonnement",
      "desc": "Licence commerciale perpétuelle incluse pour projets personnels et commerciaux illimités.",
      "freeTierTitle": "Pack Découverte",
      "freeTierPrice": "0,00 €",
      "freeTierDesc": "Pour tester immédiatement l'intégration dans votre application.",
      "freeTierItem1": "1 état complet offert (AItuko Waving)",
      "freeTierItem2": "Formats WebP, GIF et PNG HD",
      "freeTierItem3": "Composants React & Flutter",
      "freeTierItem4": "Licence de test et usage personnel",
      "freeTierBtn": "Télécharger Gratuitement",
      "starterTierTitle": "Pack Essentiel",
      "starterTierPrice": "5,00 €",
      "starterTierDesc": "Les 6 états essentiels pour dynamiser n'importe quel flux utilisateur.",
      "starterTierItem1": "6 états majeurs par mascotte",
      "starterTierItem2": "WebP transparents 60fps & PNG",
      "starterTierItem3": "Code source React + Next.js + Flutter",
      "starterTierItem4": "Licence commerciale perpétuelle",
      "starterTierBtn": "Obtenir l'Essentiel (5 €)",
      "proTierBadge": "Populaire",
      "proTierTitle": "Pack Pro 12 États",
      "proTierPrice": "9,00 €",
      "proTierDesc": "La suite d'animation intégrale pour couvrir l'intégralité de vos écrans.",
      "proTierItem1": "12 états d'animation complets",
      "proTierItem2": "Formats WebP, GIF, PNG HD & Vector",
      "proTierItem3": "Composants React, Vue, Svelte & Flutter",
      "proTierItem4": "Mises à jour et ajouts d'états à vie",
      "proTierItem5": "Licence commerciale illimitée",
      "proTierBtn": "Débloquer le Pack Pro (9 €)"
    },
    "modal": {
      "chooseMascot": "Mascotte choisie :",
      "payBtn": "Procéder au Paiement Sécurisé",
      "title": "Téléchargement Uko UI",
      "subtitle": "Archive ZIP prête à l'emploi.",
      "emailPlaceholder": "Votre adresse email",
      "submitBtn": "Télécharger l'Archive",
      "preparing": "Préparation du fichier...",
      "ready": "Téléchargement prêt",
      "downloadZip": "Télécharger le Fichier ZIP"
    },
    "footer": {
      "text": "Uko UI — Système de mascottes animées pour interfaces modernes.",
      "license": "Licence commerciale perpétuelle incluse • Composants prêts pour la production."
    },
    "resilience": {
      "offlineStatus": "Mode hors ligne actif — Le Studio reste 100% fonctionnel",
      "onlineStatus": "Connexion rétablie ✨",
      "rateLimitVote": "Ralentissez un instant avant de revoter.",
      "rateLimitSuggest": "Veuillez patienter {sec}s avant une nouvelle suggestion.",
      "rateLimitModal": "Trop de requêtes rapides. Veuillez patienter.",
      "imageRetry": "Réessayer",
      "imageOffline": "Image indisponible hors ligne"
    },
    "licenseModal": {
      "title": "Licence Commerciale Perpétuelle Uko UI",
      "subtitle": "Droits clairs, transparents et sans frais récurrents pour créateurs et développeurs.",
      "tabAllowed": "Ce qui est autorisé",
      "tabRestricted": "Ce qui est interdit",
      "tabGuarantee": "Garantie & Support",
      "allowedItem1": "Projets personnels et commerciaux illimités (SaaS, Apps mobiles, E-commerce, Sites vitrines).",
      "allowedItem2": "Intégration dans des projets clients (agences, freelances, startups).",
      "allowedItem3": "Modification, redimensionnement et adaptation des composants au code de votre application.",
      "allowedItem4": "Aucune attribution ni lien obligatoire vers Uko UI dans vos interfaces finales.",
      "allowedItem5": "Utilisation perpétuelle à vie sans abonnement ni redevance récurrente.",
      "restrictedItem1": "Revente, sous-licence ou redistribution directe des fichiers sources 3D (WebP, GIF, PNG bruts).",
      "restrictedItem2": "Inclusion des mascottes brutes dans des templates ou kits UI publics revendus comme concurrents.",
      "restrictedItem3": "Revendication de droits d'auteur exclusifs ou de marque déposée sur les designs originaux.",
      "guaranteeTitle": "Garantie Sérénité",
      "guaranteeText": "Tous les composants sont livrés prêts pour la production. Support technique et mises à jour des états inclus.",
      "closeBtn": "Fermer et retourner au Studio"
    }
  },
  "en": {
    "meta": {
      "title": "Uko UI — Animated Mascot System for Modern Interfaces",
      "desc": "Lightweight 3D animated mascots, interactive speech bubbles, and drop-in components for React, Next.js, and Flutter."
    },
    "nav": {
      "studio": "Studio",
      "catalogue": "Catalogue",
      "integration": "Integration",
      "pricing": "Pricing",
      "freeSample": "Free Sample",
      "lang": "Change language",
      "themeDark": "Dark Mode",
      "themeLight": "Light Mode"
    },
    "hero": {
      "badge": "3D Mascots & Micro-Interactions",
      "titleStart": "Bring personality",
      "titleHighlight": "to your interfaces",
      "titleEnd": "in 3 lines of code.",
      "subtitle": "Ultra-lightweight 3D animated mascot system. 12 universal states designed to supercharge user retention, onboarding, and engagement.",
      "ctaStudio": "Try in Studio",
      "ctaCatalogue": "Explore Catalogue",
      "trust": "Production-Ready • 100% WebP & React / Flutter Code"
    },
    "studio": {
      "downloadPackBtn": "Download {name}",
      "quickFreeBtn": "⚡ Free Sample (0 €)",
      "quickProBtn": "📦 Get the Pack (From 5 €)",
      "quickBarStatus": "{name} — 12 animated 3D states ready for integration",
      "badge": "Interactive Studio",
      "title": "Test & Customize in Real Time",
      "desc": "Switch characters, edit dialogue text, and export production code instantly.",
      "bubbleOn": "Bubble: Visible",
      "bubbleOff": "Bubble: Hidden",
      "bubbleToggleLabel": "Speech bubble",
      "bubbleToggleTitle": "Show / Hide speech bubble",
      "bubbleOptional": "Optional",
      "bubblePlaceholder": "Type your message...",
      "bubbleClickToHide": "Click to hide bubble",
      "prevPose": "Previous pose (←)",
      "nextPose": "Next pose (→)",
      "sizeLabel": "Size",
      "renderLabel": "Format",
      "formatWebp": "Animated WebP",
      "formatPng": "Static PNG",
      "copyCode": "Copy",
      "copied": "Copied!",
      "bgAuto": "Automatic Background",
      "bgDark": "Dark Canvas",
      "bgBlack": "Pure Black",
      "bgStone": "Light Washi Canvas",
      "bgChecker": "Transparency Grid"
    },
    "poses": {
      "waving": "Waving",
      "celebrating": "Celebrating",
      "ai_thinking": "Thinking",
      "error_404": "Error 404",
      "thumbs_up": "Thumbs Up",
      "sleeping": "Sleeping",
      "pointing": "Pointing",
      "searching": "Searching",
      "loading": "Loading",
      "idea": "Idea",
      "security": "Security",
      "goodbye": "Goodbye"
    },
    "messages": {
      "aituko": {
        "waving": "Welcome to your workspace!",
        "celebrating": "Payment confirmed successfully!",
        "ai_thinking": "AI is analyzing your data...",
        "error_404": "Page not found.",
        "thumbs_up": "All set, changes saved!",
        "sleeping": "Idle standby mode active...",
        "pointing": "Click right here to start!",
        "searching": "Searching the database...",
        "loading": "Syncing your account...",
        "idea": "Pro tip: Keyboard shortcuts save time!",
        "security": "100% secure connection.",
        "goodbye": "Catch you later!"
      },
      "owluko": {
        "waving": "Hello! Welcome aboard!",
        "celebrating": "Milestone reached! Great job!",
        "ai_thinking": "Contemplating the optimal path...",
        "error_404": "Whoops! Nest not found.",
        "thumbs_up": "Owl-certified & approved!",
        "sleeping": "Zzz... Daytime nap...",
        "pointing": "Take a look over here!",
        "searching": "Scanning the skies...",
        "loading": "Syncing wisdom...",
        "idea": "Bright idea incoming!",
        "security": "Safely guarded under my wing.",
        "goodbye": "Have a safe flight!"
      },
      "luneko": {
        "waving": "Meow! So happy to see you!",
        "celebrating": "Yay! Mission accomplished!",
        "ai_thinking": "Kitten is calculating with curiosity...",
        "error_404": "Oops! Yarn ball lost (404 error).",
        "thumbs_up": "Paw-fect! Validated and approved!",
        "sleeping": "Purr... Cozy power nap time...",
        "pointing": "Right over here! Check this out!",
        "searching": "Sniffing out the best results...",
        "loading": "Smooth synchronization underway...",
        "idea": "Spark of inspiration found!",
        "security": "Secure lock activated and guarded!",
        "goodbye": "See you soon! Have a pawsome day!"
      },
      "hatoko": {
        "waving": "Coo! Ready to deliver your messages!",
        "celebrating": "Mail delivered! Let's celebrate!",
        "ai_thinking": "Calculating the fastest flight route...",
        "error_404": "Oops! Lost letter in flight (404).",
        "thumbs_up": "Dispatch confirmed and stamped!",
        "sleeping": "Zzz... Resting peacefully in the nest...",
        "pointing": "Right over there, follow my flight!",
        "searching": "Scouting the skies for your data...",
        "loading": "In mid-flight to destination...",
        "idea": "An express spark just landed!",
        "security": "Your parcel is locked and sealed.",
        "goodbye": "Safe travels and smooth flights!"
      },
      "usako": {
        "waving": "Hop hop! Ready for a lightning sprint!",
        "celebrating": "Victory! New speed record unlocked!",
        "ai_thinking": "Whiskers twitching with fast insights...",
        "error_404": "Oops! Wrong turn in the burrow (404).",
        "thumbs_up": "Lightning-fast approval granted!",
        "sleeping": "Zzz... Quick sprinter power nap...",
        "pointing": "Sprint right this way!",
        "searching": "Scouting ahead at top speed...",
        "loading": "Maximum acceleration in progress...",
        "idea": "Quantum leap! I've got the solution!",
        "security": "Guarded with lightning-fast reflexes.",
        "goodbye": "Speed off safely, see you soon!"
      }
    },
    "catalogue": {
      "badge": "Character Universe",
      "title": "Uko Mascot Roster",
      "desc": "Each mascot comes with a unique personality and 12 harmonized animation states.",
      "available": "Available",
      "soon": "In Workshop",
      "aitukoDesc": "AI Assistant • Welcome & Onboarding",
      "owlukoDesc": "Wise Guide • Knowledge & Help",
      "lunekoName": "Luneko",
      "lunekoDesc": "Playful Kitten • Engagement & Fun",
      "inukoName": "Inuko",
      "inukoDesc": "Athletic Guardian • Loyalty & Protection",
      "hatokoName": "Hatoko",
      "hatokoDesc": "Express Courier • Push & Messaging",
      "usakoName": "Usako",
      "usakoDesc": "Agile Sprinter • Speed & Shortcuts",
      "voteTitle": "Community Vote",
      "voteSubtitle": "Cast your 1-click vote for the next mascot:",
      "voteCountSuffix": "votes",
      "votedBadge": "Voted ✓",
      "voteCancelMsg": "Vote for {name} cancelled.",
      "voteSuccessMsg": "Vote for {name} registered! ✨",
      "suggestionPrompt": "Other idea? E.g. Otter...",
      "suggestBtn": "Suggest",
      "suggestSuccessMsg": "Suggestion \"{val}\" submitted! ✨"
    },
    "candidates": {
      "kumako": "🐻 Kumako (Bear)",
      "kitsuko": "🦊 Kitsuko (Fox)",
      "panduko": "🐼 Panduko (Panda)",
      "duckuko": "🦆 Duckuko (Duck)"
    },
    "pricing": {
      "freeDownloadStarted": "{name} — Free Sample Pack downloaded successfully! 🎉",
      "badge": "Transparent Pricing",
      "title": "Simple Pricing, No Subscriptions",
      "desc": "Perpetual commercial license included for unlimited personal and commercial projects.",
      "freeTierTitle": "Discovery Pack",
      "freeTierPrice": "0.00 €",
      "freeTierDesc": "Test integration in your application immediately.",
      "freeTierItem1": "1 complete free state (AItuko Waving)",
      "freeTierItem2": "WebP, GIF, and HD PNG formats",
      "freeTierItem3": "React & Flutter drop-in components",
      "freeTierItem4": "Evaluation & personal usage license",
      "freeTierBtn": "Download Free Sample",
      "starterTierTitle": "Starter Pack",
      "starterTierPrice": "5.00 €",
      "starterTierDesc": "The 6 core states to elevate any onboarding or feedback flow.",
      "starterTierItem1": "6 key states per mascot",
      "starterTierItem2": "Transparent 60fps WebP & PNG",
      "starterTierItem3": "React + Next.js + Flutter source code",
      "starterTierItem4": "Perpetual commercial license",
      "starterTierBtn": "Get Starter Pack (5 €)",
      "proTierBadge": "Most Popular",
      "proTierTitle": "Pro Pack (12 States)",
      "proTierPrice": "9.00 €",
      "proTierDesc": "Full animation suite covering every user flow across your app.",
      "proTierItem1": "12 complete animation states",
      "proTierItem2": "WebP, GIF, HD PNG & Vector formats",
      "proTierItem3": "React, Vue, Svelte & Flutter components",
      "proTierItem4": "Lifetime updates and new states",
      "proTierItem5": "Unlimited commercial license",
      "proTierBtn": "Unlock Pro Suite (9 €)"
    },
    "modal": {
      "chooseMascot": "Selected Mascot:",
      "payBtn": "Proceed to Secure Payment",
      "title": "Uko UI Download",
      "subtitle": "Ready-to-use ZIP archive.",
      "emailPlaceholder": "Your email address",
      "submitBtn": "Download Archive",
      "preparing": "Preparing archive...",
      "ready": "Download ready",
      "downloadZip": "Download ZIP File"
    },
    "footer": {
      "text": "Uko UI — Animated mascot design system for modern interfaces.",
      "license": "Perpetual commercial license included • Production-ready components."
    },
    "resilience": {
      "offlineStatus": "Offline mode active — Studio remains 100% functional",
      "onlineStatus": "Connection restored ✨",
      "rateLimitVote": "Please wait a moment before voting again.",
      "rateLimitSuggest": "Please wait {sec}s before submitting another suggestion.",
      "rateLimitModal": "Too many rapid requests. Please wait a moment.",
      "imageRetry": "Retry loading",
      "imageOffline": "Image unavailable offline"
    },
    "licenseModal": {
      "title": "Uko UI Perpetual Commercial License",
      "subtitle": "Clear, transparent, and zero-recurring-fee terms for creators and developers.",
      "tabAllowed": "What is permitted",
      "tabRestricted": "What is prohibited",
      "tabGuarantee": "Warranty & Support",
      "allowedItem1": "Unlimited personal and commercial projects (SaaS, Mobile apps, E-commerce, Marketing sites).",
      "allowedItem2": "Integration into client work (Agencies, Freelancers, Startups).",
      "allowedItem3": "Modification, scaling, and adaptation of components to fit your app architecture.",
      "allowedItem4": "No mandatory attribution or backlink required in your end applications.",
      "allowedItem5": "Perpetual lifetime license with zero subscriptions or recurring royalties.",
      "restrictedItem1": "Direct resale, sub-licensing, or redistribution of raw 3D source files (WebP, GIF, PNG).",
      "restrictedItem2": "Inclusion of raw mascots in public UI kits or templates resold as competing sticker packs.",
      "restrictedItem3": "Claiming exclusive copyright or trademark ownership over the original character designs.",
      "guaranteeTitle": "Production Ready Guarantee",
      "guaranteeText": "All components are shipped production-ready. Technical support and future state updates included.",
      "closeBtn": "Close and return to Studio"
    }
  },
  "es": {
    "meta": {
      "title": "Uko UI — Sistema de Mascotas Animadas para Interfaces Modernas",
      "desc": "Mascotas animadas en 3D ultraligeras, globos de diálogo interactivos y componentes para React, Next.js y Flutter."
    },
    "nav": {
      "studio": "Estudio",
      "catalogue": "Catálogo",
      "integration": "Integración",
      "pricing": "Precios",
      "freeSample": "Muestra Gratis",
      "lang": "Cambiar idioma",
      "themeDark": "Modo Oscuro",
      "themeLight": "Modo Claro"
    },
    "hero": {
      "badge": "Mascotas 3D & Microinteracciones",
      "titleStart": "Dale personalidad",
      "titleHighlight": "a tus interfaces",
      "titleEnd": "en 3 líneas de código.",
      "subtitle": "Sistema de mascotas 3D ultraligeras. 12 estados universales para potenciar la retención, el onboarding y la interacción de tus usuarios.",
      "ctaStudio": "Probar en el Estudio",
      "ctaCatalogue": "Ver el Catálogo",
      "trust": "Listo para producción • 100% WebP y Código React / Flutter"
    },
    "studio": {
      "downloadPackBtn": "Descargar {name}",
      "quickFreeBtn": "⚡ Muestra Gratis (0 €)",
      "quickProBtn": "📦 Obtener el Pack (Desde 5 €)",
      "quickBarStatus": "{name} — 12 estados animados 3D listos para integrar",
      "badge": "Estudio Interactivo",
      "title": "Prueba y Personaliza en Tiempo Real",
      "desc": "Cambia de mascota, edita el diálogo y exporta el código de producción al instante.",
      "bubbleOn": "Globo: Activo",
      "bubbleOff": "Globo: Oculto",
      "bubbleToggleLabel": "Globo de diálogo",
      "bubbleToggleTitle": "Ocultar / Mostrar globo de diálogo",
      "bubbleOptional": "Opcional",
      "bubblePlaceholder": "Escribe tu mensaje...",
      "bubbleClickToHide": "Haz clic para ocultar el globo",
      "prevPose": "Pose anterior (←)",
      "nextPose": "Pose siguiente (→)",
      "sizeLabel": "Tamaño",
      "renderLabel": "Formato",
      "formatWebp": "WebP Animado",
      "formatPng": "PNG Estático",
      "copyCode": "Copiar",
      "copied": "¡Copiado!",
      "bgAuto": "Fondo Automático",
      "bgDark": "Fondo Oscuro",
      "bgBlack": "Negro Puro",
      "bgStone": "Fondo Claro Washi",
      "bgChecker": "Cuadrícula Transparente"
    },
    "poses": {
      "waving": "Bienvenida",
      "celebrating": "Éxito",
      "ai_thinking": "Pensando",
      "error_404": "Error 404",
      "thumbs_up": "Aprobado",
      "sleeping": "Reposo",
      "pointing": "Guía",
      "searching": "Búsqueda",
      "loading": "Carga",
      "idea": "Consejo",
      "security": "Seguridad",
      "goodbye": "Despedida"
    },
    "messages": {
      "aituko": {
        "waving": "¡Bienvenido a tu espacio!",
        "celebrating": "¡Pago confirmado con éxito!",
        "ai_thinking": "La IA está analizando tus datos...",
        "error_404": "Página no encontrada.",
        "thumbs_up": "¡Perfecto, cambios guardados!",
        "sleeping": "Modo reposo activado...",
        "pointing": "¡Haz clic aquí para empezar!",
        "searching": "Buscando en la base de datos...",
        "loading": "Sincronizando tus datos...",
        "idea": "Consejo: ¡Usa los atajos de teclado!",
        "security": "Conexión 100% segura.",
        "goodbye": "¡Hasta muy pronto!"
      },
      "owluko": {
        "waving": "¡Hola! ¡Bienvenido a bordo!",
        "celebrating": "¡Meta alcanzada! ¡Enhorabuena!",
        "ai_thinking": "Meditando la solución óptima...",
        "error_404": "¡Vaya! Nido no encontrado.",
        "thumbs_up": "¡Aprobado por el búho!",
        "sleeping": "Zzz... Siesta diurna...",
        "pointing": "¡Mira por aquí!",
        "searching": "Oteando el horizonte...",
        "loading": "Sincronizando sabiduría...",
        "idea": "¡Idea brillante en camino!",
        "security": "Protegido bajo mi ala.",
        "goodbye": "¡Buen vuelo y hasta pronto!"
      },
      "luneko": {
        "waving": "¡Miau! ¡Qué alegría verte por aquí!",
        "celebrating": "¡Genial! ¡Objetivo completado con éxito!",
        "ai_thinking": "El gatito analiza cada detalle...",
        "error_404": "¡Ups! Página perdida como ovillo de lana.",
        "thumbs_up": "¡Aprobado con garra!",
        "sleeping": "Ronroneo... Modo descanso activado...",
        "pointing": "¡Por aquí! Mira esta opción.",
        "searching": "Rastreando la información...",
        "loading": "Sincronizando de forma segura...",
        "idea": "¡Tengo una idea brillante!",
        "security": "Conexión totalmente blindada.",
        "goodbye": "¡Hasta pronto! Cuídate mucho."
      },
      "hatoko": {
        "waving": "¡Cú-cú! ¡Listo para entregar tus mensajes!",
        "celebrating": "¡Carta entregada! ¡Celebremos el éxito!",
        "ai_thinking": "Calculando la ruta de vuelo más rápida...",
        "error_404": "¡Ups! Carta extraviada en vuelo (404).",
        "thumbs_up": "¡Mensaje recibido y sellado con éxito!",
        "sleeping": "Zzz... Descansando en el nido...",
        "pointing": "¡Por aquí, sigue mi vuelo!",
        "searching": "Explorando los cielos para ti...",
        "loading": "En pleno vuelo hacia tu destino...",
        "idea": "¡Una idea exprés acaba de aterrizar!",
        "security": "Tus paquetes están bajo sello seguro.",
        "goodbye": "¡Buen viaje y hasta pronto!"
      },
      "usako": {
        "waving": "¡Hop hop! ¡Listo para un sprint veloz!",
        "celebrating": "¡Victoria rotunda! ¡Récord superado!",
        "ai_thinking": "Mis bigotes analizan los datos al instante...",
        "error_404": "¡Ups! Camino equivocado en la madriguera (404).",
        "thumbs_up": "¡Aprobación ultra rápida al 100%!",
        "sleeping": "Zzz... Siesta relámpago de corredor...",
        "pointing": "¡Corre por aquí, es el camino correcto!",
        "searching": "Rastreando a la velocidad de la luz...",
        "loading": "Aceleración máxima en marcha...",
        "idea": "¡Salto de genio! ¡Tengo la solución!",
        "security": "Protegido con reflejos de acero.",
        "goodbye": "¡A toda velocidad, hasta pronto!"
      }
    },
    "catalogue": {
      "badge": "Universo de Personajes",
      "title": "Catálogo de Mascotas Uko",
      "desc": "Cada personaje posee una personalidad única y 12 estados de animación armonizados.",
      "available": "Disponible",
      "soon": "En Taller",
      "aitukoDesc": "Asistente IA • Bienvenida & Onboarding",
      "owlukoDesc": "Guía Sabio • Ayuda & Conocimiento",
      "lunekoName": "Luneko",
      "lunekoDesc": "Gatito Juguetón • Interacción & Diversión",
      "inukoName": "Inuko",
      "inukoDesc": "Guardián Atlético • Lealtad & Seguridad",
      "hatokoName": "Hatoko",
      "hatokoDesc": "Mensajero Exprés • Notificaciones & Push",
      "usakoName": "Usako",
      "usakoDesc": "Corredor Ágil • Atajos & Velocidad",
      "voteTitle": "Votación de la Comunidad",
      "voteSubtitle": "Vota con 1 clic por el próximo animal:",
      "voteCountSuffix": "votos",
      "votedBadge": "Votado ✓",
      "voteCancelMsg": "Voto por {name} cancelado.",
      "voteSuccessMsg": "¡Voto por {name} registrado! ✨",
      "suggestionPrompt": "¿Otra idea? Ej: Nutria...",
      "suggestBtn": "Sugerir",
      "suggestSuccessMsg": "¡Sugerencia « {val} » enviada con éxito! ✨"
    },
    "candidates": {
      "kumako": "🐻 Kumako (Oso)",
      "kitsuko": "🦊 Kitsuko (Zorro)",
      "panduko": "🐼 Panduko (Panda)",
      "duckuko": "🦆 Duckuko (Pato)"
    },
    "pricing": {
      "freeDownloadStarted": "¡{name} — Paquete de prueba descargado con éxito! 🎉",
      "badge": "Precios Claros",
      "title": "Precios Claros y Sin Suscripción",
      "desc": "Licencia comercial perpetua incluida para proyectos personales y comerciales ilimitados.",
      "freeTierTitle": "Pack Descubrimiento",
      "freeTierPrice": "0,00 €",
      "freeTierDesc": "Para probar la integración en tu aplicación de inmediato.",
      "freeTierItem1": "1 estado completo gratis (AItuko Waving)",
      "freeTierItem2": "Formatos WebP, GIF y PNG HD",
      "freeTierItem3": "Componentes listos para React y Flutter",
      "freeTierItem4": "Licencia de prueba y uso personal",
      "freeTierBtn": "Descargar Gratis",
      "starterTierTitle": "Pack Esencial",
      "starterTierPrice": "5,00 €",
      "starterTierDesc": "Los 6 estados clave para elevar cualquier flujo de usuario.",
      "starterTierItem1": "6 estados principales por mascota",
      "starterTierItem2": "WebP transparente 60fps y PNG",
      "starterTierItem3": "Código fuente React + Next.js + Flutter",
      "starterTierItem4": "Licencia comercial perpetua",
      "starterTierBtn": "Obtener Esencial (5 €)",
      "proTierBadge": "Más Popular",
      "proTierTitle": "Pack Pro (12 Estados)",
      "proTierPrice": "9,00 €",
      "proTierDesc": "Suite de animación integral para cubrir todas las pantallas de tu app.",
      "proTierItem1": "12 estados de animación completos",
      "proTierItem2": "Formatos WebP, GIF, PNG HD y Vector",
      "proTierItem3": "Componentes React, Vue, Svelte y Flutter",
      "proTierItem4": "Actualizaciones y nuevos estados de por vida",
      "proTierItem5": "Licencia comercial ilimitada",
      "proTierBtn": "Desbloquear Pack Pro (9 €)"
    },
    "modal": {
      "chooseMascot": "Mascota seleccionada:",
      "payBtn": "Proceder al Pago Seguro",
      "title": "Descarga de Uko UI",
      "subtitle": "Archivo ZIP listo para usar.",
      "emailPlaceholder": "Tu correo electrónico",
      "submitBtn": "Descargar Archivo",
      "preparing": "Preparando descarga...",
      "ready": "Descarga lista",
      "downloadZip": "Descargar Archivo ZIP"
    },
    "footer": {
      "text": "Uko UI — Sistema de mascotas animadas para interfaces modernas.",
      "license": "Licencia comercial perpetua incluida • Componentes listos para producción."
    },
    "resilience": {
      "offlineStatus": "Modo sin conexión activo — El Studio sigue 100% funcional",
      "onlineStatus": "Conexión restablecida ✨",
      "rateLimitVote": "Espera un momento antes de volver a votar.",
      "rateLimitSuggest": "Espera {sec}s antes de enviar otra sugerencia.",
      "rateLimitModal": "Demasiadas solicitudes. Por favor, espera un momento.",
      "imageRetry": "Reintentar",
      "imageOffline": "Imagen no disponible sin conexión"
    },
    "licenseModal": {
      "title": "Licencia Comercial Perpetua Uko UI",
      "subtitle": "Términos claros, transparentes y sin tarifas recurrentes para creadores y desarrolladores.",
      "tabAllowed": "Lo que está permitido",
      "tabRestricted": "Lo que está prohibido",
      "tabGuarantee": "Garantía y Soporte",
      "allowedItem1": "Proyectos personales y comerciales ilimitados (SaaS, Apps móviles, E-commerce, Sitios web).",
      "allowedItem2": "Integración en proyectos para clientes (Agencias, Freelancers, Startups).",
      "allowedItem3": "Modificación, cambio de tamaño y adaptación de componentes al código de su aplicación.",
      "allowedItem4": "Sin atribución obligatoria ni enlace en sus aplicaciones finales.",
      "allowedItem5": "Uso perpetuo de por vida sin suscripciones ni regalías recurrentes.",
      "restrictedItem1": "Reventa, sublicencia o redistribución directa de archivos fuente 3D (WebP, GIF, PNG brutos).",
      "restrictedItem2": "Inclusión de las mascotas en plantillas o kits UI públicos revendidos como competidores.",
      "restrictedItem3": "Reclamar derechos de autor exclusivos o marcas registradas sobre los diseños originales.",
      "guaranteeTitle": "Garantía de Producción",
      "guaranteeText": "Todos los componentes se entregan listos para producción. Soporte técnico y actualizaciones incluidas.",
      "closeBtn": "Cerrar y volver al Studio"
    }
  },
  "de": {
    "meta": {
      "title": "Uko UI — Animiertes Maskottchen-System für moderne Interfaces",
      "desc": "Ultra-leichte animierte 3D-Maskottchen, interaktive Sprechblasen und Drop-In-Komponenten für React, Next.js und Flutter."
    },
    "nav": {
      "studio": "Studio",
      "catalogue": "Katalog",
      "integration": "Integration",
      "pricing": "Preise",
      "freeSample": "Gratis-Sample",
      "lang": "Sprache ändern",
      "themeDark": "Dunkelmodus",
      "themeLight": "Hellmodus"
    },
    "hero": {
      "badge": "3D-Maskottchen & Mikro-Interaktionen",
      "titleStart": "Verleihen Sie Ihren Interfaces",
      "titleHighlight": "eine Seele",
      "titleEnd": "mit nur 3 Zeilen Code.",
      "subtitle": "Ultra-leichtes animiertes 3D-Maskottchen-System. 12 universelle Zustände zur Steigerung von Nutzerbindung, Onboarding und Interaktion.",
      "ctaStudio": "Im Studio testen",
      "ctaCatalogue": "Katalog ansehen",
      "trust": "Produktionsbereit • 100% WebP & React / Flutter Code"
    },
    "studio": {
      "downloadPackBtn": "{name} laden",
      "quickFreeBtn": "⚡ Gratis-Probe (0 €)",
      "quickProBtn": "📦 Paket holen (Ab 5 €)",
      "quickBarStatus": "{name} — 12 animierte 3D-Zustände integrationsbereit",
      "badge": "Interaktives Studio",
      "title": "In Echtzeit testen & anpassen",
      "desc": "Wechseln Sie Maskottchen, bearbeiten Sie Nachrichten und exportieren Sie den Code sofort.",
      "bubbleOn": "Sprechblase: An",
      "bubbleOff": "Sprechblase: Aus",
      "bubbleToggleLabel": "Sprechblase",
      "bubbleToggleTitle": "Sprechblase ein-/ausblenden",
      "bubbleOptional": "Optional",
      "bubblePlaceholder": "Ihre Nachricht eingeben...",
      "bubbleClickToHide": "Klicken zum Ausblenden",
      "prevPose": "Vorherige Pose (←)",
      "nextPose": "Nächste Pose (→)",
      "sizeLabel": "Größe",
      "renderLabel": "Format",
      "formatWebp": "Animiertes WebP",
      "formatPng": "Statisches PNG",
      "copyCode": "Kopieren",
      "copied": "Kopiert!",
      "bgAuto": "Automatischer Hintergrund",
      "bgDark": "Dunkler Hintergrund",
      "bgBlack": "Reines Schwarz",
      "bgStone": "Heller Washi-Hintergrund",
      "bgChecker": "Transparenz-Gitter"
    },
    "poses": {
      "waving": "Begrüßung",
      "celebrating": "Erfolg",
      "ai_thinking": "Nachdenken",
      "error_404": "Fehler 404",
      "thumbs_up": "Bestätigung",
      "sleeping": "Ruhemodus",
      "pointing": "Anleitung",
      "searching": "Suche",
      "loading": "Laden",
      "idea": "Tipp",
      "security": "Sicherheit",
      "goodbye": "Abschied"
    },
    "messages": {
      "aituko": {
        "waving": "Willkommen in Ihrem Bereich!",
        "celebrating": "Zahlung erfolgreich bestätigt!",
        "ai_thinking": "KI analysiert Ihre Daten...",
        "error_404": "Seite nicht gefunden.",
        "thumbs_up": "Alles gespeichert!",
        "sleeping": "Ruhezustand aktiv...",
        "pointing": "Hier klicken zum Starten!",
        "searching": "Datenbank wird durchsucht...",
        "loading": "Konto wird synchronisiert...",
        "idea": "Tipp: Tastenkürzel sparen Zeit!",
        "security": "100% sichere Verbindung.",
        "goodbye": "Bis zum nächsten Mal!"
      },
      "owluko": {
        "waving": "Hallo! Willkommen an Bord!",
        "celebrating": "Ziel erreicht! Großartig!",
        "ai_thinking": "Ich grüble über der besten Lösung...",
        "error_404": "Hoppla! Nest nicht gefunden.",
        "thumbs_up": "Von der Eule genehmigt!",
        "sleeping": "Zzz... Kleines Tagesschläfchen...",
        "pointing": "Schau mal hier rüber!",
        "searching": "Ich scanne den Horizont...",
        "loading": "Wissen wird synchronisiert...",
        "idea": "Ich habe eine glänzende Idee!",
        "security": "Sicher unter meinen Flügeln.",
        "goodbye": "Guten Flug und bis bald!"
      },
      "luneko": {
        "waving": "Miau! Schön, dass du da bist!",
        "celebrating": "Juhu! Erfolg auf ganzer Linie!",
        "ai_thinking": "Das Kätzchen denkt aufmerksam nach...",
        "error_404": "Hoppla! Seite im Wollknäuel verloren.",
        "thumbs_up": "Mit Pfote bestätigt und genehmigt!",
        "sleeping": "Schnurr... Zeit für ein Nickerchen...",
        "pointing": "Hier entlang! Schau mal hier.",
        "searching": "Suche läuft auf Hochtouren...",
        "loading": "Sanftes Laden im Gange...",
        "idea": "Ein genialer Einfall!",
        "security": "Vollständig geschützter Bereich.",
        "goodbye": "Bis bald und einen tollen Tag!"
      },
      "hatoko": {
        "waving": "Gurrr! Bereit, deine Nachrichten zu liefern!",
        "celebrating": "Post zugestellt! Das feiern wir!",
        "ai_thinking": "Berechne die schnellste Flugroute...",
        "error_404": "Hoppla! Brief im Flug verloren (404).",
        "thumbs_up": "Nachricht empfangen und abgestempelt!",
        "sleeping": "Zzz... Ein kurzes Schläfchen im Nest...",
        "pointing": "Hier entlang, folge meinem Flug!",
        "searching": "Überfliege das Gebiet für dich...",
        "loading": "Im Direktflug zum Ziel...",
        "idea": "Ein Geistesblitz ist gelandet!",
        "security": "Deine Daten sind sicher versiegelt.",
        "goodbye": "Guten Flug und bis bald!"
      },
      "usako": {
        "waving": "Hoppla! Bereit für einen schnellen Sprint!",
        "celebrating": "Sieg! Neuer Geschwindigkeitsrekord!",
        "ai_thinking": "Meine Schnurrhaare analysieren die Daten...",
        "error_404": "Hoppla! Falsche Abzweigung im Bau (404).",
        "thumbs_up": "Blitzschnell zu 100% freigegeben!",
        "sleeping": "Zzz... Ein kurzer Powernap...",
        "pointing": "Hier entlang sprinten, genau richtig!",
        "searching": "Suche mit Höchstgeschwindigkeit...",
        "loading": "Maximale Beschleunigung läuft...",
        "idea": "Geistesblitz! Ich hab die Lösung!",
        "security": "Geschützt mit blitzschnellen Reflexen.",
        "goodbye": "Schnell wie der Wind, bis bald!"
      }
    },
    "catalogue": {
      "badge": "Charakter-Universum",
      "title": "Uko Maskottchen-Katalog",
      "desc": "Jedes Maskottchen besitzt eine eigene Persönlichkeit und 12 abgestimmte Animationszustände.",
      "available": "Verfügbar",
      "soon": "In Vorbereitung",
      "aitukoDesc": "KI-Assistent • Willkommen & Onboarding",
      "owlukoDesc": "Weiser Begleiter • Wissen & Hilfe",
      "lunekoName": "Luneko",
      "lunekoDesc": "Verspieltes Kätzchen • Engagement & Spaß",
      "inukoName": "Inuko",
      "inukoDesc": "Athletischer Wächter • Loyalität & Schutz",
      "hatokoName": "Hatoko",
      "hatokoDesc": "Express-Bote • Benachrichtigungen & Push",
      "usakoName": "Usako",
      "usakoDesc": "Agiler Sprinter • Tempo & Tastenkürzel",
      "voteTitle": "Community-Voting",
      "voteSubtitle": "Mit 1 Klick für das nächste Tier stimmen:",
      "voteCountSuffix": "Stimmen",
      "votedBadge": "Gewählt ✓",
      "voteCancelMsg": "Stimme für {name} widerrufen.",
      "voteSuccessMsg": "Stimme für {name} gespeichert! ✨",
      "suggestionPrompt": "Andere Idee? Z.B. Otter...",
      "suggestBtn": "Vorschlagen",
      "suggestSuccessMsg": "Vorschlag « {val} » erfolgreich eingereicht! ✨"
    },
    "candidates": {
      "kumako": "🐻 Kumako (Bär)",
      "kitsuko": "🦊 Kitsuko (Fuchs)",
      "panduko": "🐼 Panduko (Panda)",
      "duckuko": "🦆 Duckuko (Ente)"
    },
    "pricing": {
      "freeDownloadStarted": "{name} — Kostenloses Sample-Paket erfolgreich heruntergeladen! 🎉",
      "badge": "Transparente Preise",
      "title": "Transparente Preise, kein Abo",
      "desc": "Lebenslange kommerzielle Lizenz für unbegrenzte persönliche und kommerzielle Projekte.",
      "freeTierTitle": "Entdecker-Paket",
      "freeTierPrice": "0,00 €",
      "freeTierDesc": "Testen Sie die Integration sofort in Ihrer App.",
      "freeTierItem1": "1 vollständiger Gratis-Zustand (AItuko Waving)",
      "freeTierItem2": "WebP, GIF und HD-PNG Formate",
      "freeTierItem3": "React- & Flutter-Komponenten",
      "freeTierItem4": "Lizenz für Test & persönliche Nutzung",
      "freeTierBtn": "Kostenlos herunterladen",
      "starterTierTitle": "Starter-Paket",
      "starterTierPrice": "5,00 €",
      "starterTierDesc": "Die 6 wichtigsten Zustände für jeden Nutzer-Flow.",
      "starterTierItem1": "6 Schlüsselzustände pro Maskottchen",
      "starterTierItem2": "Transparente 60fps WebP & PNG",
      "starterTierItem3": "Quellcode für React + Next.js + Flutter",
      "starterTierItem4": "Dauerhafte kommerzielle Lizenz",
      "starterTierBtn": "Starter-Paket sichern (5 €)",
      "proTierBadge": "Beliebt",
      "proTierTitle": "Pro-Paket (12 Zustände)",
      "proTierPrice": "9,00 €",
      "proTierDesc": "Komplette Animationssuite für alle Screens Ihrer Anwendung.",
      "proTierItem1": "12 vollständige Animationszustände",
      "proTierItem2": "WebP, GIF, HD-PNG & Vektorformate",
      "proTierItem3": "Komponenten für React, Vue, Svelte & Flutter",
      "proTierItem4": "Lebenslange Updates & neue Zustände",
      "proTierItem5": "Unbegrenzte kommerzielle Lizenz",
      "proTierBtn": "Pro-Paket freischalten (9 €)"
    },
    "modal": {
      "chooseMascot": "Ausgewähltes Maskottchen:",
      "payBtn": "Zur sicheren Zahlung",
      "title": "Uko UI Download",
      "subtitle": "Einsatzbereites ZIP-Archiv.",
      "emailPlaceholder": "Ihre E-Mail-Adresse",
      "submitBtn": "Archiv herunterladen",
      "preparing": "Archiv wird vorbereitet...",
      "ready": "Download bereit",
      "downloadZip": "ZIP-Datei herunterladen"
    },
    "footer": {
      "text": "Uko UI — Animiertes Maskottchen-System für moderne Interfaces.",
      "license": "Lebenslange kommerzielle Lizenz inklusive • Produktionsbereite Komponenten."
    },
    "resilience": {
      "offlineStatus": "Offline-Modus aktiv — Studio bleibt zu 100 % funktionsfähig",
      "onlineStatus": "Verbindung wiederhergestellt ✨",
      "rateLimitVote": "Bitte warten Sie einen Moment vor der nächsten Stimme.",
      "rateLimitSuggest": "Bitte warten Sie {sec}s vor dem nächsten Vorschlag.",
      "rateLimitModal": "Zu viele Anfragen. Bitte kurz warten.",
      "imageRetry": "Erneut versuchen",
      "imageOffline": "Bild offline nicht verfügbar"
    },
    "licenseModal": {
      "title": "Unbefristete kommerzielle Uko UI Lizenz",
      "subtitle": "Klare, transparente Bedingungen ohne wiederkehrende Gebühren für Entwickler.",
      "tabAllowed": "Was erlaubt ist",
      "tabRestricted": "Was untersagt ist",
      "tabGuarantee": "Garantie & Support",
      "allowedItem1": "Unbegrenzte persönliche und kommerzielle Projekte (SaaS, mobile Apps, E-Commerce).",
      "allowedItem2": "Integration in Kundenprojekte (Agenturen, Freelancer, Start-ups).",
      "allowedItem3": "Anpassung, Skalierung und Modifikation der Komponenten an Ihren Code.",
      "allowedItem4": "Keine Namensnennung oder Verlinkung in Ihren Endanwendungen erforderlich.",
      "allowedItem5": "Lebenslange Lizenz ohne wiederkehrende Lizenzgebühren oder Abonnements.",
      "restrictedItem1": "Direkter Wiederverkauf, Unterlizenzierung oder Weitergabe der 3D-Quelldateien (WebP, GIF, PNG).",
      "restrictedItem2": "Einbindung in öffentlich weiterverkaufte UI-Kits oder Design-Templates.",
      "restrictedItem3": "Beanspruchung exklusiver Urheber- oder Markenrechte an den Originalfiguren.",
      "guaranteeTitle": "Produktionsreife-Garantie",
      "guaranteeText": "Alle Komponenten werden sofort einsatzbereit geliefert. Technischer Support und Status-Updates inklusive.",
      "closeBtn": "Schließen und zurück zum Studio"
    }
  },
  "ja": {
    "meta": {
      "title": "Uko UI — モダンUIのための3Dアニメーションマスコットシステム",
      "desc": "超軽量3Dアニメーションマスコット、対話型吹き出し、React・Next.js・Flutter対応の即戦力コンポーネント。"
    },
    "nav": {
      "studio": "スタジオ",
      "catalogue": "カタログ",
      "integration": "導入ガイド",
      "pricing": "料金プラン",
      "freeSample": "無料サンプル",
      "lang": "言語を切り替える",
      "themeDark": "ダークモード",
      "themeLight": "ライトモード"
    },
    "hero": {
      "badge": "3Dマスコット ＆ マイクロインタラクション",
      "titleStart": "インターフェースに",
      "titleHighlight": "命を吹き込む",
      "titleEnd": "わずか3行のコードで。",
      "subtitle": "超軽量な3Dアニメーションマスコットシステム。ユーザーの継続率、オンボーディング、エンゲージメントを高める12種類のユニバーサルステート。",
      "ctaStudio": "スタジオで試す",
      "ctaCatalogue": "カタログを見る",
      "trust": "本番環境対応 • 100% WebP ＆ React / Flutter コード"
    },
    "studio": {
      "downloadPackBtn": "{name}をダウンロード",
      "quickFreeBtn": "⚡ 無料サンプル (0 €)",
      "quickProBtn": "📦 パックを入手 (5 €〜)",
      "quickBarStatus": "{name} — 12種類の3Dアニメーションが統合可能",
      "badge": "インタラクティブ・スタジオ",
      "title": "リアルタイムで体験＆カスタマイズ",
      "desc": "マスコットの切り替え、吹き出しメッセージの編集、コード出力を即座に行えます。",
      "bubbleOn": "吹き出し: ON",
      "bubbleOff": "吹き出し: 非表示",
      "bubbleToggleLabel": "吹き出しメッセージ",
      "bubbleToggleTitle": "吹き出しの表示 / 非表示",
      "bubbleOptional": "任意",
      "bubblePlaceholder": "メッセージを入力...",
      "bubbleClickToHide": "クリックして吹き出しを非表示",
      "prevPose": "前のポーズ (←)",
      "nextPose": "次のポーズ (→)",
      "sizeLabel": "サイズ",
      "renderLabel": "フォーマット",
      "formatWebp": "アニメーション WebP",
      "formatPng": "静止画 PNG",
      "copyCode": "コピー",
      "copied": "コピー完了！",
      "bgAuto": "自動背景",
      "bgDark": "ダーク背景",
      "bgBlack": "漆黒ブラック",
      "bgStone": "和紙ライト背景",
      "bgChecker": "透過グリッド"
    },
    "poses": {
      "waving": "ウェルカム",
      "celebrating": "お祝い",
      "ai_thinking": "考え中",
      "error_404": "エラー404",
      "thumbs_up": "承認",
      "sleeping": "スリープ",
      "pointing": "ガイド",
      "searching": "検索中",
      "loading": "読込中",
      "idea": "ヒント",
      "security": "安心安全",
      "goodbye": "またね"
    },
    "messages": {
      "aituko": {
        "waving": "あなたのスペースへようこそ！",
        "celebrating": "決済が正常に完了しました！",
        "ai_thinking": "AIがデータを分析しています...",
        "error_404": "ページが見つかりません。",
        "thumbs_up": "完璧です、保存しました！",
        "sleeping": "スリープモード待機中...",
        "pointing": "ここをクリックして開始！",
        "searching": "データベースを検索中...",
        "loading": "アカウントを同期中...",
        "idea": "ヒント：ショートカットキーで効率アップ！",
        "security": "100%安全な暗号化接続です。",
        "goodbye": "またお会いしましょう！"
      },
      "owluko": {
        "waving": "やあ！ようこそ！",
        "celebrating": "目標達成！素晴らしい！",
        "ai_thinking": "最善の解決策を思案中...",
        "error_404": "おっと！巣が見つかりません。",
        "thumbs_up": "フクロウのお墨付き！",
        "sleeping": "Zzz... お昼寝中...",
        "pointing": "ここを見てみて！",
        "searching": "大空を見渡し中...",
        "loading": "知恵を同期中...",
        "idea": "ひらめきました！",
        "security": "翼の下でしっかり保護。",
        "goodbye": "良い旅を！またね！"
      },
      "luneko": {
        "waving": "にゃーん！いらっしゃいませ！",
        "celebrating": "やったね！大成功だよ！",
        "ai_thinking": "子猫が考え中ニャ...",
        "error_404": "おっと！毛糸玉が迷子です（404）。",
        "thumbs_up": "肉球スタンプで承認完了！",
        "sleeping": "ゴロゴロ... お昼寝中ニャ...",
        "pointing": "こっちを見てニャ！",
        "searching": "一生懸命探しているよ...",
        "loading": "スムーズに読み込み中...",
        "idea": "ピコーン！ひらめいたニャ！",
        "security": "安心・安全に保護されています。",
        "goodbye": "またね！良い一日をニャ！"
      },
      "hatoko": {
        "waving": "クルックー！お届け物の準備完了です！",
        "celebrating": "配達完了！お祝いしましょう！",
        "ai_thinking": "最速のフライトルートを計算中...",
        "error_404": "おっと！手紙が迷子になりました (404)。",
        "thumbs_up": "メッセージ受領、スタンプ完了！",
        "sleeping": "Zzz... 巣でひと休み中...",
        "pointing": "こちらです、私の羽についてきて！",
        "searching": "上空からくまなく探索中...",
        "loading": "目的地へ向かって飛行中...",
        "idea": "ひらめきのお便りが届きました！",
        "security": "大切なお荷物は厳重に封印保護！",
        "goodbye": "良い空の旅を、また会いましょう！"
      },
      "usako": {
        "waving": "ピョン！快速ダッシュの準備完了！",
        "celebrating": "大勝利！新記録達成です！",
        "ai_thinking": "おヒゲを動かして高速分析中...",
        "error_404": "おっと！穴ぐらで迷子になりました (404)。",
        "thumbs_up": "超特急でバッチリ承認完了！",
        "sleeping": "Zzz... スプリンターの快速お昼寝...",
        "pointing": "こちらへダッシュ、大正解のルートです！",
        "searching": "光速スピードで探索中...",
        "loading": "フルスピード加速中...",
        "idea": "ピョンとひらめいた！答えがわかりました！",
        "security": "電光石火の反射神経で完全ガード！",
        "goodbye": "ダッシュで行ってらっしゃい、またね！"
      }
    },
    "catalogue": {
      "badge": "キャラクターの世界",
      "title": "Uko マスコットカタログ",
      "desc": "各マスコットは独自の個性と統一感のある12種類のアニメーションステートを備えています。",
      "available": "配信中",
      "soon": "準備中",
      "aitukoDesc": "AIアシスタント • 歓迎 ＆ オンボーディング",
      "owlukoDesc": "賢いガイド • ナレッジ ＆ ヘルプ",
      "lunekoName": "Luneko",
      "lunekoDesc": "やんちゃな子猫 • 交流 ＆ 楽しさ",
      "inukoName": "Inuko",
      "inukoDesc": "俊敏な番犬 • 忠誠とセキュリティ",
      "hatokoName": "Hatoko",
      "hatokoDesc": "伝書鳩 • 通知 ＆ プッシュ配信",
      "usakoName": "Usako",
      "usakoDesc": "俊足うさぎ • ショートカット ＆ スピード",
      "voteTitle": "マスコット投票",
      "voteSubtitle": "次に欲しい動物を1クリックで投票：",
      "voteCountSuffix": "票",
      "votedBadge": "投票済み ✓",
      "voteCancelMsg": "{name} への投票を取り消しました。",
      "voteSuccessMsg": "{name} に投票しました！✨",
      "suggestionPrompt": "他の動物？ 例: カワウソ...",
      "suggestBtn": "提案する",
      "suggestSuccessMsg": "提案「{val}」を受け付けました！✨"
    },
    "candidates": {
      "kumako": "🐻 クマコ (熊)",
      "kitsuko": "🦊 キツコ (狐)",
      "panduko": "🐼 パンダコ (パンダ)",
      "duckuko": "🦆 ダクコ (アヒル)"
    },
    "pricing": {
      "freeDownloadStarted": "{name} — 無料サンプルパックのダウンロードが完了しました！🎉",
      "badge": "明瞭な料金体系",
      "title": "サブスクなし・買い切りプラン",
      "desc": "個人・商用プロジェクト無制限で利用可能な永久商用ライセンス付き。",
      "freeTierTitle": "ディスカバリー版",
      "freeTierPrice": "0.00 €",
      "freeTierDesc": "アプリへの導入を今すぐテストできます。",
      "freeTierItem1": "無料ステート1種類 (AItuko Waving)",
      "freeTierItem2": "WebP、GIF、HD PNG形式",
      "freeTierItem3": "React ＆ Flutterコンポーネント",
      "freeTierItem4": "評価・個人利用ライセンス",
      "freeTierBtn": "無料でダウンロード",
      "starterTierTitle": "スターター版",
      "starterTierPrice": "5.00 €",
      "starterTierDesc": "ユーザー体験を彩る主要な6ステート。",
      "starterTierItem1": "マスコットあたり主要6ステート",
      "starterTierItem2": "透過60fps WebP ＆ PNG",
      "starterTierItem3": "React + Next.js + Flutterソースコード",
      "starterTierItem4": "永久商用利用ライセンス",
      "starterTierBtn": "スターター版を入手 (5 €)",
      "proTierBadge": "一番人気",
      "proTierTitle": "プロ版（12ステート）",
      "proTierPrice": "9.00 €",
      "proTierDesc": "アプリの全画面を網羅する完全アニメーションスイート。",
      "proTierItem1": "12種類の完全アニメーションステート",
      "proTierItem2": "WebP、GIF、HD PNG ＆ ベクター形式",
      "proTierItem3": "React、Vue、Svelte、Flutter対応",
      "proTierItem4": "生涯アップデート ＆ 新ステート追加",
      "proTierItem5": "無制限の商用ライセンス",
      "proTierBtn": "プロ版をアンロック (9 €)"
    },
    "modal": {
      "chooseMascot": "選択中のマスコット：",
      "payBtn": "安全な決済に進む",
      "title": "Uko UI ダウンロード",
      "subtitle": "すぐに使えるZIPアーカイブ。",
      "emailPlaceholder": "メールアドレスを入力",
      "submitBtn": "アーカイブをダウンロード",
      "preparing": "準備中...",
      "ready": "ダウンロード可能",
      "downloadZip": "ZIPファイルをダウンロード"
    },
    "footer": {
      "text": "Uko UI — モダンインターフェースのためのアニメーションマスコットシステム。",
      "license": "永久商用ライセンス付属 • 本番導入対応コンポーネント。"
    },
    "resilience": {
      "offlineStatus": "オフラインモード — スタジオは100%動作します",
      "onlineStatus": "接続が復旧しました ✨",
      "rateLimitVote": "連続投票はお控えください。少しお待ちください。",
      "rateLimitSuggest": "次の提案まであと {sec} 秒お待ちください。",
      "rateLimitModal": "リクエストが多すぎます。しばらくお待ちください。",
      "imageRetry": "再試行",
      "imageOffline": "オフラインのため画像が利用できません"
    },
    "licenseModal": {
      "title": "Uko UI 永久商用ライセンス",
      "subtitle": "開発者とクリエイターのための明確で透明性のある買い切りライセンス規約。",
      "tabAllowed": "許可されている利用範囲",
      "tabRestricted": "禁止事項",
      "tabGuarantee": "保証とサポート",
      "allowedItem1": "商用・個人を問わず無制限のプロジェクト（SaaS、モバイルアプリ、Webサイト）。",
      "allowedItem2": "受託開発やクライアントワークへの組み込み（制作会社、フリーランス、スタートアップ）。",
      "allowedItem3": "アプリのUIに合わせたサイズ変更、色調補正、コードのカスタマイズ。",
      "allowedItem4": "最終成果物へのクレジット表記やUko UIへのリンク義務なし。",
      "allowedItem5": "サブスクリプションや追加ロイヤリティなしの永久利用権。",
      "restrictedItem1": "3D画像素材（WebP, GIF, PNG）そのものの再配布、転売、サブライセンス。",
      "restrictedItem2": "UIキットやテンプレートとして素材を抽出し競合製品として販売する行為。",
      "restrictedItem3": "オリジナルキャラクターデザインに対する独占的商標権・著作権の主張。",
      "guaranteeTitle": "本番導入保証",
      "guaranteeText": "すべてのコンポーネントは本番環境ですぐに動作します。技術サポートとアップデートが含まれます。",
      "closeBtn": "閉じてスタジオに戻る"
    }
  },
  "pt": {
    "meta": {
      "title": "Uko UI — Sistema de Mascotes Animados para Interfaces Modernas",
      "desc": "Mascotes animados 3D ultra-leves, balões de fala interativos e componentes prontos para React, Next.js e Flutter."
    },
    "nav": {
      "studio": "Studio",
      "catalogue": "Catálogo",
      "integration": "Integração",
      "pricing": "Preços",
      "freeSample": "Amostra Grátis",
      "lang": "Alterar idioma",
      "themeDark": "Modo Escuro",
      "themeLight": "Modo Claro"
    },
    "hero": {
      "badge": "Mascotes 3D & Micro-interações",
      "titleStart": "Dê personalidade",
      "titleHighlight": "às suas interfaces",
      "titleEnd": "em 3 linhas de código.",
      "subtitle": "Sistema de mascotes 3D animados ultra-leves. 12 estados universais para impulsionar a retenção, onboarding e engajamento dos seus usuários.",
      "ctaStudio": "Testar no Studio",
      "ctaCatalogue": "Ver o Catálogo",
      "trust": "Pronto para produção • 100% WebP e Código React / Flutter"
    },
    "studio": {
      "downloadPackBtn": "Baixar {name}",
      "quickFreeBtn": "⚡ Amostra Grátis (0 €)",
      "quickProBtn": "📦 Obter o Pack (A partir de 5 €)",
      "quickBarStatus": "{name} — 12 estados animados 3D prontos para integrar",
      "badge": "Studio Interativo",
      "title": "Teste e Personalize em Tempo Real",
      "desc": "Alterne entre mascotes, edite as falas e exporte o código de produção instantaneamente.",
      "bubbleOn": "Balão: Ativo",
      "bubbleOff": "Balão: Oculto",
      "bubbleToggleLabel": "Balão de diálogo",
      "bubbleToggleTitle": "Ocultar / Exibir balão de fala",
      "bubbleOptional": "Opcional",
      "bubblePlaceholder": "Digite sua mensagem...",
      "bubbleClickToHide": "Clique para ocultar o balão",
      "prevPose": "Pose anterior (←)",
      "nextPose": "Próxima pose (→)",
      "sizeLabel": "Tamanho",
      "renderLabel": "Formato",
      "formatWebp": "WebP Animado",
      "formatPng": "PNG Estático",
      "copyCode": "Copiar",
      "copied": "Copiado!",
      "bgAuto": "Fundo Automático",
      "bgDark": "Fundo Escuro",
      "bgBlack": "Preto Puro",
      "bgStone": "Fundo Claro Washi",
      "bgChecker": "Grade de Transparência"
    },
    "poses": {
      "waving": "Boas-vindas",
      "celebrating": "Sucesso",
      "ai_thinking": "Pensando",
      "error_404": "Erro 404",
      "thumbs_up": "Aprovado",
      "sleeping": "Repouso",
      "pointing": "Guia",
      "searching": "Busca",
      "loading": "Carregando",
      "idea": "Dica",
      "security": "Segurança",
      "goodbye": "Despedida"
    },
    "messages": {
      "aituko": {
        "waving": "Bem-vindo ao seu espaço!",
        "celebrating": "Pagamento aprovado com sucesso!",
        "ai_thinking": "A IA está analisando seus dados...",
        "error_404": "Página não encontrada.",
        "thumbs_up": "Tudo pronto, alterações salvas!",
        "sleeping": "Modo de espera ativado...",
        "pointing": "Clique aqui para começar!",
        "searching": "Buscando no banco de dados...",
        "loading": "Sincronizando seus dados...",
        "idea": "Dica pro: atalhos de teclado poupam tempo!",
        "security": "Conexão 100% segura.",
        "goodbye": "Até logo mais!"
      },
      "owluko": {
        "waving": "Olá! Bem-vindo a bordo!",
        "celebrating": "Meta batida! Parabéns!",
        "ai_thinking": "Calculando a melhor rota...",
        "error_404": "Ops! Ninho não encontrado.",
        "thumbs_up": "Aprovado pela coruja!",
        "sleeping": "Zzz... Cochilo diurno...",
        "pointing": "Dê uma olhada aqui!",
        "searching": "Observando o horizonte...",
        "loading": "Sincronizando sabedoria...",
        "idea": "Tive uma ideia brilhante!",
        "security": "Protegido sob minhas asas.",
        "goodbye": "Bom voo e até breve!"
      },
      "luneko": {
        "waving": "Miau! Que bom ter você aqui!",
        "celebrating": "Oba! Missão cumprida com sucesso!",
        "ai_thinking": "O gatinho está pensando rapidinho...",
        "error_404": "Ops! Novelo perdido (Erro 404).",
        "thumbs_up": "Validado com carimbo de patinha!",
        "sleeping": "Ronrom... Hora da soneca...",
        "pointing": "Olha aqui! Dá uma conferida.",
        "searching": "Procurando pelos melhores dados...",
        "loading": "Carregamento suave em andamento...",
        "idea": "Tive uma ideia excelente!",
        "security": "Ambiente 100% blindado e seguro.",
        "goodbye": "Até breve! Tenha um ótimo dia!"
      },
      "hatoko": {
        "waving": "Arrulhar! Pronto para entregar seus recados!",
        "celebrating": "Correio entregue! Vamos comemorar!",
        "ai_thinking": "Calculando a rota aérea mais rápida...",
        "error_404": "Ops! Carta perdida em voo (404).",
        "thumbs_up": "Mensagem recebida e carimbada!",
        "sleeping": "Zzz... Descansando no ninho...",
        "pointing": "Por aqui, siga meu voo!",
        "searching": "Sobrevoando a área para encontrar...",
        "loading": "Em pleno voo até o destino...",
        "idea": "Uma ideia expressa acabou de pousar!",
        "security": "Suas encomendas estão sob lacre seguro.",
        "goodbye": "Boa viagem e até logo!"
      },
      "usako": {
        "waving": "Pula pula! Pronto para um tiro de velocidade!",
        "celebrating": "Vitória incrível! Recorde quebrado!",
        "ai_thinking": "Meus bigodes estão analisando os dados...",
        "error_404": "Ops! Caminho errado na toca (404).",
        "thumbs_up": "Aprovação relâmpago 100%!",
        "sleeping": "Zzz... Sesta rápida de atleta...",
        "pointing": "Corra por aqui, é a direção certa!",
        "searching": "Farejando na velocidade da luz...",
        "loading": "Aceleração máxima em andamento...",
        "idea": "Pulo de gênio! Encontrei a resposta!",
        "security": "Protegido com reflexos rápidos de aço.",
        "goodbye": "A toda velocidade, até breve!"
      }
    },
    "catalogue": {
      "badge": "Universo dos Personagens",
      "title": "Catálogo de Mascotes Uko",
      "desc": "Cada mascote possui uma personalidade única e 12 estados de animação harmonizados.",
      "available": "Disponível",
      "soon": "Em Breve",
      "aitukoDesc": "Assistente IA • Boas-vindas & Onboarding",
      "owlukoDesc": "Guia Sábio • Conhecimento & Ajuda",
      "lunekoName": "Luneko",
      "lunekoDesc": "Gatinho Brincalhão • Engajamento & Diversão",
      "inukoName": "Inuko",
      "inukoDesc": "Guardião Atlético • Lealdade & Segurança",
      "hatokoName": "Hatoko",
      "hatokoDesc": "Mensageiro Expresso • Notificações & Push",
      "usakoName": "Usako",
      "usakoDesc": "Veloz & Ágil • Atalhos & Produtividade",
      "voteTitle": "Votação da Comunidade",
      "voteSubtitle": "Vote com 1 clique no próximo animal:",
      "voteCountSuffix": "votos",
      "votedBadge": "Votado ✓",
      "voteCancelMsg": "Voto em {name} cancelado.",
      "voteSuccessMsg": "Voto em {name} registrado! ✨",
      "suggestionPrompt": "Outra ideia? Ex: Lontra...",
      "suggestBtn": "Sugerir",
      "suggestSuccessMsg": "Sugestão « {val} » enviada com sucesso! ✨"
    },
    "candidates": {
      "kumako": "🐻 Kumako (Urso)",
      "kitsuko": "🦊 Kitsuko (Raposa)",
      "panduko": "🐼 Panduko (Panda)",
      "duckuko": "🦆 Duckuko (Pato)"
    },
    "pricing": {
      "freeDownloadStarted": "{name} — Pacote de demonstração baixado com sucesso! 🎉",
      "badge": "Preços Claros",
      "title": "Preços Simples, Sem Assinatura",
      "desc": "Licença comercial perpétua incluída para projetos pessoais e comerciais ilimitados.",
      "freeTierTitle": "Pacote Descoberta",
      "freeTierPrice": "0,00 €",
      "freeTierDesc": "Teste a integração no seu app imediatamente.",
      "freeTierItem1": "1 estado completo gratis (AItuko Waving)",
      "freeTierItem2": "Formatos WebP, GIF e PNG HD",
      "freeTierItem3": "Componentes prontos para React & Flutter",
      "freeTierItem4": "Licença para testes e uso pessoal",
      "freeTierBtn": "Baixar Gratuitamente",
      "starterTierTitle": "Pacote Essencial",
      "starterTierPrice": "5,00 €",
      "starterTierDesc": "Os 6 estados essenciais para animar qualquer fluxo de usuário.",
      "starterTierItem1": "6 estados principais por mascote",
      "starterTierItem2": "WebP transparente 60fps & PNG",
      "starterTierItem3": "Código-fonte React + Next.js + Flutter",
      "starterTierItem4": "Licence comercial perpétua",
      "starterTierBtn": "Obter Essencial (5 €)",
      "proTierBadge": "Mais Popular",
      "proTierTitle": "Pacote Pro (12 Estados)",
      "proTierPrice": "9,00 €",
      "proTierDesc": "Suite de animação completa para todas as telas do seu aplicativo.",
      "proTierItem1": "12 estados de animação completos",
      "proTierItem2": "Formatos WebP, GIF, PNG HD & Vetorial",
      "proTierItem3": "Componentes React, Vue, Svelte & Flutter",
      "proTierItem4": "Atualizações vitalícias e novos estados",
      "proTierItem5": "Licença comercial ilimitada",
      "proTierBtn": "Desbloquear Pacote Pro (9 €)"
    },
    "modal": {
      "chooseMascot": "Mascote selecionado:",
      "payBtn": "Prosseguir para Pagamento Seguro",
      "title": "Download Uko UI",
      "subtitle": "Arquivo ZIP pronto para uso.",
      "emailPlaceholder": "Seu endereço de e-mail",
      "submitBtn": "Baixar Arquivo",
      "preparing": "Preparando download...",
      "ready": "Download pronto",
      "downloadZip": "Baixar Arquivo ZIP"
    },
    "footer": {
      "text": "Uko UI — Sistema de mascotes animados para interfaces modernas.",
      "license": "Licença comercial perpétua incluída • Componentes prontos para produção."
    },
    "resilience": {
      "offlineStatus": "Modo offline ativo — O Studio continua 100% funcional",
      "onlineStatus": "Conexão restabelecida ✨",
      "rateLimitVote": "Aguarde um momento antes de votar novamente.",
      "rateLimitSuggest": "Aguarde {sec}s antes de enviar outra sugestão.",
      "rateLimitModal": "Muitas requisições rápidas. Por favor, aguarde.",
      "imageRetry": "Tentar novamente",
      "imageOffline": "Imagem indisponível offline"
    },
    "licenseModal": {
      "title": "Licença Comercial Perpétua Uko UI",
      "subtitle": "Termos claros, transparentes e sem taxas recorrentes para criadores e desenvolvedores.",
      "tabAllowed": "O que é permitido",
      "tabRestricted": "O que é proibido",
      "tabGuarantee": "Garantia e Suporte",
      "allowedItem1": "Projetos pessoais e comerciais ilimitados (SaaS, Aplicativos móveis, E-commerce, Sites).",
      "allowedItem2": "Integração em projetos de clientes (Agências, Freelancers, Startups).",
      "allowedItem3": "Modificação, redimensionamento e adaptação dos componentes ao código da aplicação.",
      "allowedItem4": "Nenhuma atribuição ou link obrigatório em suas aplicações finais.",
      "allowedItem5": "Uso perpétuo vitalício sem assinaturas ou royalties recorrentes.",
      "restrictedItem1": "Revenda direta, sublicenciamento ou redistribuição dos arquivos fonte 3D brutos.",
      "restrictedItem2": "Inclusão das mascotes em kits de UI ou templates públicos revendidos como concorrentes.",
      "restrictedItem3": "Reivindicação de direitos autorais exclusivos ou marcas registradas dos designs originais.",
      "guaranteeTitle": "Garantia de Produção",
      "guaranteeText": "Todos os componentes são entregues prontos para produção. Suporte técnico e atualizações inclusos.",
      "closeBtn": "Fechar e voltar ao Studio"
    }
  },
  "zh": {
    "meta": {
      "title": "Uko UI — 现代界面的3D动效吉祥物设计系统",
      "desc": "超轻量3D动画吉祥物、交互式气泡对话框，支持 React、Next.js 和 Flutter 即插即用组件。"
    },
    "nav": {
      "studio": "工作室",
      "catalogue": "吉祥物图鉴",
      "integration": "集成指南",
      "pricing": "价格方案",
      "freeSample": "免费体验",
      "lang": "切换语言",
      "themeDark": "深色模式",
      "themeLight": "浅色模式"
    },
    "hero": {
      "badge": "3D吉祥物 ＆ 微交互系统",
      "titleStart": "赋予您的界面",
      "titleHighlight": "生动灵魂",
      "titleEnd": "仅需3行代码。",
      "subtitle": "超轻量级3D动画吉祥物系统。包含12种通用动效状态，全面提升用户留存率、新手引导与交互趣味性。",
      "ctaStudio": "在工作室体验",
      "ctaCatalogue": "浏览全部图鉴",
      "trust": "生产环境即用 • 100% WebP 与 React / Flutter 代码"
    },
    "studio": {
      "downloadPackBtn": "下载 {name}",
      "quickFreeBtn": "⚡ 免费试用 (0 €)",
      "quickProBtn": "📦 获取完整礼包 (5 €起)",
      "quickBarStatus": "{name} — 12个3D动画状态即插即用",
      "badge": "交互式工作室",
      "title": "实时体验与个性化定制",
      "desc": "自由切换吉祥物角色、编辑气泡文本，并一键导出生产级前端代码。",
      "bubbleOn": "气泡：开启",
      "bubbleOff": "气泡：隐藏",
      "bubbleToggleLabel": "对话气泡",
      "bubbleToggleTitle": "显示 / 隐藏对话气泡",
      "bubbleOptional": "可选",
      "bubblePlaceholder": "输入您的文案...",
      "bubbleClickToHide": "点击隐藏气泡",
      "prevPose": "上一个动作 (←)",
      "nextPose": "下一个动作 (→)",
      "sizeLabel": "尺寸",
      "renderLabel": "格式",
      "formatWebp": "动效 WebP",
      "formatPng": "静态 PNG",
      "copyCode": "复制代码",
      "copied": "已复制！",
      "bgAuto": "自适应背景",
      "bgDark": "深色背景",
      "bgBlack": "纯黑背景",
      "bgStone": "和纸浅色背景",
      "bgChecker": "透明网格"
    },
    "poses": {
      "waving": "欢迎",
      "celebrating": "庆祝",
      "ai_thinking": "思考中",
      "error_404": "404错误",
      "thumbs_up": "点赞确认",
      "sleeping": "休眠",
      "pointing": "指引",
      "searching": "搜索",
      "loading": "加载中",
      "idea": "提示",
      "security": "安全保护",
      "goodbye": "告别"
    },
    "messages": {
      "aituko": {
        "waving": "欢迎进入您的专属空间！",
        "celebrating": "订单支付成功！太棒了！",
        "ai_thinking": "AI 正在分析您的数据...",
        "error_404": "未找到该页面。",
        "thumbs_up": "一切就绪，已保存！",
        "sleeping": "已进入休眠省电模式...",
        "pointing": "点击这里立即开始！",
        "searching": "正在全库检索中...",
        "loading": "正在同步您的数据...",
        "idea": "效率贴士：善用快捷键事半功倍！",
        "security": "100% 安全加密连接。",
        "goodbye": "期待下次与您相遇！"
      },
      "owluko": {
        "waving": "嗨！欢迎登船！",
        "celebrating": "达成里程碑！祝贺！",
        "ai_thinking": "正在思考最佳方案...",
        "error_404": "哎呀！没有找到鸟巢。",
        "thumbs_up": "猫头鹰认证通过！",
        "sleeping": "Zzz... 白天打盹中...",
        "pointing": "看这边哦！",
        "searching": "正在极目远眺，搜寻目标...",
        "loading": "正在同步智慧宝库...",
        "idea": "我有了一个绝妙的点子！",
        "security": "在我的羽翼下安全无忧。",
        "goodbye": "祝飞行愉快，再见！"
      },
      "luneko": {
        "waving": "喵～！很高兴遇见你！",
        "celebrating": "太棒啦！目标圆满达成！",
        "ai_thinking": "小猫咪正在飞速思考中...",
        "error_404": "哎呀！毛线团迷路了（404）。",
        "thumbs_up": "猫爪盖章，完美通过！",
        "sleeping": "呼噜呼噜... 正在小憩中...",
        "pointing": "往这边看！点这里开始。",
        "searching": "正在全网搜寻中...",
        "loading": "正在平稳加载中...",
        "idea": "灵光一现！有了好主意！",
        "security": "连接全面受保护，安全无忧。",
        "goodbye": "下次再见！祝你拥有美好一天！"
      },
      "hatoko": {
        "waving": "咕咕！随时为您递送信件与通知！",
        "celebrating": "信件成功送达！太棒了！",
        "ai_thinking": "正在规划最快飞行航线...",
        "error_404": "哎呀！信件在飞行中迷路了 (404)。",
        "thumbs_up": "信息已盖章确认送达！",
        "sleeping": "Zzz... 在鸽巢里小憩片刻...",
        "pointing": "往这边走，跟随我的飞行方向！",
        "searching": "正在高空全面扫描搜索...",
        "loading": "正全速飞往目的地...",
        "idea": "灵感快件刚刚着陆！",
        "security": "数据邮件均已严格加密封存。",
        "goodbye": "祝您旅途平安，下次见！"
      },
      "usako": {
        "waving": "跳跳！闪电冲刺已准备就绪！",
        "celebrating": "大获全胜！刷新最快记录！",
        "ai_thinking": "胡须颤动中，高速计算数据...",
        "error_404": "哎呀！在兔洞里走错方向了 (404)。",
        "thumbs_up": "极速闪电通过审核！",
        "sleeping": "Zzz... 飞毛腿小憩充电中...",
        "pointing": "往这边冲刺，路线完全正确！",
        "searching": "正在以光速飞奔搜索...",
        "loading": "全马力加速载入中...",
        "idea": "灵机一跳！我有解决秘籍！",
        "security": "凭借敏捷身手坚固防护！",
        "goodbye": "极速前行，期待与您再次相见！"
      }
    },
    "catalogue": {
      "badge": "角色宇宙",
      "title": "Uko 吉祥物图鉴",
      "desc": "每个角色都拥有独特的性格设定与统一的12种动画状态。",
      "available": "现已推出",
      "soon": "工坊打磨中",
      "aitukoDesc": "AI助手 • 欢迎与新手引导",
      "owlukoDesc": "智慧向导 • 知识库与帮助",
      "lunekoName": "Luneko",
      "lunekoDesc": "活泼小猫 • 用户互动与趣味",
      "inukoName": "Inuko",
      "inukoDesc": "矫健护卫犬 • 忠诚与安全保障",
      "hatokoName": "Hatoko",
      "hatokoDesc": "飞鸽使者 • 消息通知与推送",
      "usakoName": "Usako",
      "usakoDesc": "敏捷飞兔 • 快捷操作与提速",
      "voteTitle": "社区投票",
      "voteSubtitle": "一键投票选出下一款吉祥物：",
      "voteCountSuffix": "票",
      "votedBadge": "已投票 ✓",
      "voteCancelMsg": "已取消对 {name} 的投票。",
      "voteSuccessMsg": "已成功为 {name} 投票！✨",
      "suggestionPrompt": "其他动物想法？如：水獭...",
      "suggestBtn": "提交建议",
      "suggestSuccessMsg": "您的建议「{val}」已收录！✨"
    },
    "candidates": {
      "kumako": "🐻 Kumako (小熊)",
      "kitsuko": "🦊 Kitsuko (小狐狸)",
      "panduko": "🐼 Panduko (大熊猫)",
      "duckuko": "🦆 Duckuko (小鸭子)"
    },
    "pricing": {
      "freeDownloadStarted": "{name} — 免费体验包下载成功！🎉",
      "badge": "透明定价",
      "title": "明码标价，无订阅捆绑",
      "desc": "包含永久商用授权，可无限次用于个人与商业项目。",
      "freeTierTitle": "新手探索包",
      "freeTierPrice": "0.00 €",
      "freeTierDesc": "立即在您的应用中测试集成效果。",
      "freeTierItem1": "1个免费完整状态 (AItuko Waving)",
      "freeTierItem2": "WebP、GIF 与高清 PNG 格式",
      "freeTierItem3": "React 与 Flutter 源码组件",
      "freeTierItem4": "测试与个人项目使用授权",
      "freeTierBtn": "免费下载",
      "starterTierTitle": "核心精选包",
      "starterTierPrice": "5.00 €",
      "starterTierDesc": "覆盖核心业务流程所需的6大常用状态。",
      "starterTierItem1": "每款吉祥物包含6大核心状态",
      "starterTierItem2": "透明背景 60fps WebP 与 PNG",
      "starterTierItem3": "React + Next.js + Flutter 源码",
      "starterTierItem4": "永久商业授权",
      "starterTierBtn": "获取基础版 (5 €)",
      "proTierBadge": "最受欢迎",
      "proTierTitle": "专业全能版 (12款全状态)",
      "proTierPrice": "9.00 €",
      "proTierDesc": "覆盖应用全流程的完整动效套件。",
      "proTierItem1": "12个完整动画状态",
      "proTierItem2": "WebP、GIF、高清PNG及矢量格式",
      "proTierItem3": "支持 React、Vue、Svelte、Flutter",
      "proTierItem4": "终身免费更新及新状态增补",
      "proTierItem5": "无限制商业授权",
      "proTierBtn": "解锁专业版 (9 €)"
    },
    "modal": {
      "chooseMascot": "已选吉祥物：",
      "payBtn": "前往安全支付",
      "title": "Uko UI 资源下载",
      "subtitle": "即插即用的 ZIP 归档包。",
      "emailPlaceholder": "输入您的邮箱地址",
      "submitBtn": "下载归档包",
      "preparing": "正在准备文件...",
      "ready": "下载就绪",
      "downloadZip": "下载 ZIP 文件"
    },
    "footer": {
      "text": "Uko UI — 现代界面的3D动效吉祥物设计系统。",
      "license": "包含永久商用授权 • 生产环境即插即用。"
    },
    "resilience": {
      "offlineStatus": "离线模式生效中 — 工作室功能 100% 可用",
      "onlineStatus": "网络连接已恢复 ✨",
      "rateLimitVote": "操作过于频繁，请稍候再投票。",
      "rateLimitSuggest": "请等待 {sec} 秒后再提交新建议。",
      "rateLimitModal": "请求过于频繁，请稍后再试。",
      "imageRetry": "重试加载",
      "imageOffline": "离线状态下图片不可用"
    },
    "licenseModal": {
      "title": "Uko UI 永久商业授权许可",
      "subtitle": "面向开发者与创作者的清晰、透明且无后续订阅费用的商用条款。",
      "tabAllowed": "允许的使用范围",
      "tabRestricted": "严禁的滥用行为",
      "tabGuarantee": "品质保障与技术支持",
      "allowedItem1": "无限制用于个人与商业项目（SaaS平台、移动端App、电商网站、客户端项目）。",
      "allowedItem2": "直接集成至外包与客户定制项目中（设计工作室、独立开发者、初创企业）。",
      "allowedItem3": "自由修改、缩放尺寸并针对您的应用架构深度定制代码。",
      "allowedItem4": "最终上线产品中无需强制保留署名或指向 Uko UI 的外链。",
      "allowedItem5": "一次性永久买断，零后续订阅费用，无附加版税。",
      "restrictedItem1": "直接倒卖、转授权或公开分发原始 3D 图像文件（WebP、GIF、PNG 源文件）。",
      "restrictedItem2": "将原始吉祥物打包进公开售卖的 UI Kit 或模板竞品中。",
      "restrictedItem3": "对原始吉祥物角色设计主张排他性独家著作权或注册为独立商标。",
      "guaranteeTitle": "生产级品质保证",
      "guaranteeText": "所有组件均已适配生产环境。包含后续技术支持与新状态更新。",
      "closeBtn": "关闭并返回工作室"
    }
  }
};

const SAFE_I18N_ATTRS = Object.freeze(new Set([
  'placeholder',
  'title',
  'aria-label',
  'aria-description',
  'alt',
  'content'
]));

class I18nManager {
  constructor() {
    this.supportedLangs = Object.freeze(['en', 'fr', 'es', 'de', 'ja', 'pt', 'zh']);
    this.defaultLang = 'fr';
    this.currentLang = this.detectLanguage();
    this._memo = new Map();
    this._i18nNodes = null;
    this._attrNodes = null;
  }

  detectLanguage() {
    let saved = null;
    try {
      saved = localStorage.getItem('uko_lang');
    } catch (e) {
      console.warn('[i18n Security] Accès localStorage restreint (mode privé/sandbox)', e);
    }

    if (saved && this.supportedLangs.includes(saved)) {
      return saved;
    }

    const browserLang = (navigator.language || navigator.userLanguage || '').toLowerCase();
    for (const lang of this.supportedLangs) {
      if (browserLang.startsWith(lang)) {
        return lang;
      }
    }

    return this.defaultLang;
  }

  setLanguage(lang) {
    if (!this.supportedLangs.includes(lang)) return;
    this.currentLang = lang;
    this._memo.clear();
    try {
      localStorage.setItem('uko_lang', lang);
    } catch (e) {}
    document.documentElement.lang = lang;
    this.updateDOM();
  }

  _initNodeCache() {
    if (this._i18nNodes) return;
    this._i18nNodes = Array.from(document.querySelectorAll('[data-i18n]')).map(el => ({
      el,
      key: el.getAttribute('data-i18n'),
      isInput: (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA')
    }));

    this._attrNodes = Array.from(document.querySelectorAll('[data-i18n-attr]')).map(el => {
      const spec = el.getAttribute('data-i18n-attr') || '';
      const bindings = [];
      spec.split(';').forEach(p => {
        const [rawAttr, rawKey] = p.split(':');
        if (rawAttr && rawKey) {
          const attr = rawAttr.trim().toLowerCase();
          const key = rawKey.trim();
          if (SAFE_I18N_ATTRS.has(attr)) {
            bindings.push({ attr, key });
          }
        }
      });
      return { el, bindings };
    });
  }

  has(keyPath) {
    if (!keyPath || typeof keyPath !== 'string') return false;
    const lookup = (langObj, path) => {
      if (!langObj || typeof langObj !== 'object') return undefined;
      const keys = path.split('.');
      let val = langObj;
      for (let i = 0; i < keys.length; i++) {
        const k = keys[i];
        if (k === '__proto__' || k === 'constructor' || k === 'prototype') return undefined;
        if (val && typeof val === 'object' && Object.prototype.hasOwnProperty.call(val, k)) {
          val = val[k];
        } else {
          return undefined;
        }
      }
      return val;
    };
    return lookup(TRANSLATIONS[this.currentLang], keyPath) !== undefined ||
           lookup(TRANSLATIONS[this.defaultLang], keyPath) !== undefined;
  }

  get(keyPath, params = {}, fallback = undefined) {
    const hasParams = Object.keys(params).length > 0;
    const memoKey = `${this.currentLang}:${keyPath}`;
    
    if (!hasParams && fallback === undefined && this._memo.has(memoKey)) {
      return this._memo.get(memoKey);
    }

    const lookup = (langObj, path) => {
      if (!langObj || typeof langObj !== 'object' || typeof path !== 'string') return undefined;
      const keys = path.split('.');
      let val = langObj;
      for (let i = 0; i < keys.length; i++) {
        const k = keys[i];
        if (k === '__proto__' || k === 'constructor' || k === 'prototype') {
          return undefined;
        }
        if (val && typeof val === 'object' && Object.prototype.hasOwnProperty.call(val, k)) {
          val = val[k];
        } else {
          return undefined;
        }
      }
      return val;
    };

    let val = lookup(TRANSLATIONS[this.currentLang], keyPath);
    if (val === undefined) {
      val = lookup(TRANSLATIONS[this.defaultLang], keyPath);
    }
    if (val === undefined) {
      return fallback !== undefined ? fallback : keyPath;
    }

    if (typeof val === 'string') {
      if (!hasParams) {
        this._memo.set(memoKey, val);
        return val;
      }
      return val.replace(/\{(\w+)\}/g, (_, match) => {
        if (Object.prototype.hasOwnProperty.call(params, match)) {
          return String(params[match]);
        }
        return `{${match}}`;
      });
    }
    return val;
  }

  updateDOM() {
    document.documentElement.lang = this.currentLang;
    this._initNodeCache();

    requestAnimationFrame(() => {
      // 1. data-i18n (Protection absolue anti-écrasement par clé brute)
      const nodes = this._i18nNodes;
      if (nodes) {
        for (let i = 0; i < nodes.length; i++) {
          const item = nodes[i];
          if (!item.key) continue;
          
          if (this.has(item.key)) {
            const text = this.get(item.key);
            if (text !== undefined && text !== item.key) {
              if (item.isInput) {
                item.el.value = text;
              } else {
                item.el.textContent = text;
              }
            }
          }
        }
      }

      // 2. data-i18n-attr (Protection attributs)
      const attrNodes = this._attrNodes;
      if (attrNodes) {
        for (let i = 0; i < attrNodes.length; i++) {
          const item = attrNodes[i];
          const bindings = item.bindings;
          for (let j = 0; j < bindings.length; j++) {
            const b = bindings[j];
            if (!b.key) continue;
            
            if (this.has(b.key)) {
              const val = this.get(b.key);
              if (val && val !== b.key) {
                item.el.setAttribute(b.attr, val);
              }
            }
          }
        }
      }

      // 3. Flags and checkmarks
      const langMeta = {
        en: { flag: '🇬🇧', code: 'EN' },
        fr: { flag: '🇫🇷', code: 'FR' },
        es: { flag: '🇪🇸', code: 'ES' },
        de: { flag: '🇩🇪', code: 'DE' },
        ja: { flag: '🇯🇵', code: 'JA' },
        pt: { flag: '🇧🇷', code: 'PT' },
        zh: { flag: '🇨🇳', code: 'ZH' }
      };
      
      const activeFlag = document.getElementById('activeLangFlag');
      const activeCode = document.getElementById('activeLangCode');
      if (activeFlag && activeCode && langMeta[this.currentLang]) {
        activeFlag.textContent = langMeta[this.currentLang].flag;
        activeCode.textContent = langMeta[this.currentLang].code;
      }

      for (let i = 0; i < this.supportedLangs.length; i++) {
        const l = this.supportedLangs[i];
        const check = document.getElementById(`check-${l}`);
        if (check) {
          if (l === this.currentLang) check.classList.remove('hidden');
          else check.classList.add('hidden');
        }
      }

      if (typeof onLanguageChanged === 'function') {
        onLanguageChanged(this.currentLang);
      }
    });
  }
}

window.i18n = new I18nManager();
