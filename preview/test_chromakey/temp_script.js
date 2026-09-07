
    'use strict';

    // Safe Storage Wrapper (Résistant aux sandboxes iframe et mode privé)
    const safeStorage = {
      get(key) {
        try { return localStorage.getItem(key); } catch (e) { return null; }
      },
      set(key, val) {
        try { localStorage.setItem(key, val); } catch (e) {}
      }
    };

    // Allowlists Stricts
    const ALLOWED_THEMES = Object.freeze(['dark', 'light']);
    const ALLOWED_FRAMEWORKS = Object.freeze(['react', 'vue', 'flutter', 'html']);
    const ALLOWED_TIERS = Object.freeze(['free', 'starter', 'pro']);

    const poseKeys = Object.freeze([
      "idle", "waving", "celebrating", "ai_thinking", "error_404", "thumbs_up",
      "sleeping", "pointing", "searching", "loading", "idea", "security", "goodbye"
    ]);

    const poseFolders = Object.freeze([
      "00_idle", "01_waving", "02_celebrating", "03_ai_thinking", "04_error_404", "05_thumbs_up",
      "06_sleeping", "07_pointing", "08_searching", "09_loading", "10_idea", "11_security", "12_goodbye"
    ]);

    const AITUKO_VIDEOS = Object.freeze([
      "mascots/aituko/aituko_idle.mp4",
      "mascots/aituko/aituko_waving.mp4",
      "mascots/aituko/aituko_celebration.mp4",
      "mascots/aituko/aituko_thinking.mp4",
      "mascots/aituko/aituko_error_404.mp4",
      "mascots/aituko/aituko_thumbs_up.mp4",
      "mascots/aituko/aituko_sleeping.mp4",
      "mascots/aituko/aituko_pointing.mp4",
      "mascots/aituko/aituko_searching.mp4",
      "mascots/aituko/aituko_loading.mp4",
      "mascots/aituko/aituko_idea.mp4",
      "mascots/aituko/aituko_security.mp4",
      "mascots/aituko/aituko_goodbye.mp4"
    ]);

    const MASCOTS = Object.freeze({
      aituko: {
        name: "AItuko",
        component: "AItuko",
        flutter: "AItukoMascot",
        folderPrefix: "assets/",
        zips: {
          free: "downloads/Uko-Free-Sample.zip",
          starter: "downloads/AItuko-Starter-6-States.zip",
          pro: "downloads/AItuko-Pro-12-States.zip"
        }
      },
      owluko: {
        name: "Owluko",
        component: "Owluko",
        flutter: "OwlukoMascot",
        folderPrefix: "mascots/owluko/assets/",
        zips: {
          free: "downloads/Owluko-Free-Sample.zip",
          starter: "downloads/Owluko-Starter-6-States.zip",
          pro: "downloads/Owluko-Pro-12-States.zip"
        }
      },
      luneko: {
        name: "Luneko",
        component: "Luneko",
        flutter: "LunekoMascot",
        folderPrefix: "mascots/luneko/assets/",
        zips: {
          free: "downloads/Luneko-Free-Sample.zip",
          starter: "downloads/Luneko-Starter-Pack.zip",
          pro: "downloads/Luneko-Pro-12-States.zip"
        }
      },
      hatoko: {
        name: "Hatoko",
        component: "Hatoko",
        flutter: "HatokoMascot",
        folderPrefix: "mascots/hatoko/assets/",
        zips: {
          free: "downloads/Hatoko-Free-Sample.zip",
          starter: "downloads/Hatoko-Starter-Pack.zip",
          pro: "downloads/Hatoko-Pro-12-States.zip"
        }
      },
      usako: {
        name: "Usako",
        component: "Usako",
        flutter: "UsakoMascot",
        folderPrefix: "mascots/usako/assets/",
        zips: {
          free: "downloads/Usako-Free-Sample.zip",
          starter: "downloads/Usako-Starter-Pack.zip",
          pro: "downloads/Usako-Pro-12-States.zip"
        }
      },
      inuko: {
        name: "Inuko",
        component: "Inuko",
        flutter: "InukoMascot",
        folderPrefix: "mascots/inuko/assets/",
        zips: {
          free: "downloads/Inuko-Free-Sample.zip",
          starter: "downloads/Inuko-Starter-Pack.zip",
          pro: "downloads/Inuko-Pro-12-States.zip"
        }
      }
    });

    let currentMascot = "aituko";
    let activeIdx = 0;
    let lastActiveIdx = 0;
    let isAnimated = true;
    let currentSize = 200;
    let scheduledSize = 200;
    let sizeRafId = null;
    let snippetDebounceTimer = null;
    let currentFw = 'react';
    let isBubbleVisible = true;
    let currentModalTier = 'pro';

    // Registre Statique des Éléments DOM (Élimine le DOM Thrashing)
    const DOM = {};
    function initDOMRegistry() {
      DOM.bubbleInput = document.getElementById('bubbleInput');
      DOM.bubbleDisplay = document.getElementById('bubbleTextDisplay');
      DOM.bubbleBox = document.getElementById('speechBubbleEl');
      DOM.bubbleToggle = document.getElementById('bubbleToggle');
      DOM.bubbleQuickTxt = document.getElementById('bubbleQuickTxt');
      DOM.eyeOpen = document.getElementById('eyeIconOpen');
      DOM.eyeClosed = document.getElementById('eyeIconClosed');
      DOM.counterTxt = document.getElementById('counterTxt');
      DOM.formatBtn = document.getElementById('formatBtn');
      DOM.stageBox = document.getElementById('stageBox');
      DOM.mascotVideo = document.getElementById('mascotVideo');
      DOM.mascotImg = document.getElementById('mascotImg');
      DOM.mascotStageWrapper = document.getElementById('mascotStageWrapper');
      DOM.fallbackOverlay = document.getElementById('mascotFallbackOverlay');
      DOM.sizeTxt = document.getElementById('sizeTxt');
      DOM.codeBlock = document.getElementById('codeBlock');
      DOM.copyTxt = document.getElementById('copyTxt');
      DOM.catalogueVoteCount = document.getElementById('catalogueVoteCount');
      DOM.buyModal = document.getElementById('buyModal');
      DOM.modalTierName = document.getElementById('modalTierName');
      DOM.modalPrice = document.getElementById('modalPrice');
      DOM.downloadLink = document.getElementById('downloadLink');
      DOM.paySubmitBtn = document.getElementById('paySubmitBtn');
      DOM.paySuccess = document.getElementById('paySuccess');
      DOM.langMenu = document.getElementById('langDropdownMenu');
      DOM.langChevron = document.getElementById('langChevron');
      DOM.langBtn = document.getElementById('langDropdownBtn');
      DOM.toastContainer = document.getElementById('japandiToastContainer');
      
      DOM.pills = poseKeys.map((_, i) => document.getElementById(`pill-${i}`));
      DOM.fwBtns = {
        react: document.getElementById('fw-react'),
        vue: document.getElementById('fw-vue'),
        flutter: document.getElementById('fw-flutter'),
        html: document.getElementById('fw-html')
      };
    }

    // Fonctions d'échappement et sanitization contextuelle
    function sanitizeForJsx(str) {
      return String(str).replace(/[&<>"']/g, (c) => {
        const entities = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
        return entities[c] || c;
      });
    }

    function sanitizeForDart(str) {
      return String(str)
        .replace(/\\/g, '\\\\')
        .replace(/'/g, "\\'")
        .replace(/\$/g, '\\$')
        .replace(/\r?\n/g, ' ');
    }

    function sanitizePlainText(str) {
      return String(str).replace(/[<>]/g, '').trim();
    }

    function clampSize(val) {
      const parsed = parseInt(val, 10);
      if (isNaN(parsed)) return 180;
      return Math.min(280, Math.max(120, parsed));
    }

    // ==========================================================================
    // 1. MOTEUR DE PRÉCHARGEMENT INTELLIGENT DES ACTIFS (MascotAssetPreloader)
    // ==========================================================================
    class MascotAssetPreloader {
      constructor() {
        this.cache = new Map();
        this.idleQueue = [];
        this.isIdleProcessing = false;
      }

      getAssetUrl(mascotKey, poseFolder, animated) {
        const prefix = getAssetPrefixFor(mascotKey);
        const filename = animated ? "animated.webp?v=chroma-green-20260830-v14" : "static.png?v=chroma-green-20260830-v14";
        return `${prefix}${poseFolder}/${filename}`;
      }

      preload(url) {
        if (this.cache.has(url)) return;
        const img = new Image();
        img.decoding = 'async';
        img.src = url;
        this.cache.set(url, img);
      }

      preloadRing(mascotKey, centerIdx, animated) {
        const count = poseFolders.length;
        // Voisins immédiats (Priorité 1)
        const nextIdx = (centerIdx + 1) % count;
        const prevIdx = (centerIdx - 1 + count) % count;
        this.preload(this.getAssetUrl(mascotKey, poseFolders[nextIdx], animated));
        this.preload(this.getAssetUrl(mascotKey, poseFolders[prevIdx], animated));

        // Voisins secondaires (Priorité 2)
        const next2Idx = (centerIdx + 2) % count;
        const prev2Idx = (centerIdx - 2 + count) % count;
        this.preload(this.getAssetUrl(mascotKey, poseFolders[next2Idx], animated));
        this.preload(this.getAssetUrl(mascotKey, poseFolders[prev2Idx], animated));

        // File d'attente en idle pour le reste des poses
        for (let i = 0; i < count; i++) {
          if (i !== centerIdx && i !== nextIdx && i !== prevIdx && i !== next2Idx && i !== prev2Idx) {
            this.queueIdle(this.getAssetUrl(mascotKey, poseFolders[i], animated));
          }
        }
      }

      queueIdle(url) {
        if (this.cache.has(url) || this.idleQueue.includes(url)) return;
        this.idleQueue.push(url);
        if (!this.isIdleProcessing) {
          this.isIdleProcessing = true;
          if ('requestIdleCallback' in window) {
            requestIdleCallback((d) => this.processIdle(d), { timeout: 2000 });
          } else {
            setTimeout(() => this.processIdle({ timeRemaining: () => 15 }), 100);
          }
        }
      }

      processIdle(deadline) {
        while (this.idleQueue.length > 0 && deadline.timeRemaining() > 2) {
          const url = this.idleQueue.shift();
          this.preload(url);
        }
        if (this.idleQueue.length > 0) {
          if ('requestIdleCallback' in window) {
            requestIdleCallback((d) => this.processIdle(d), { timeout: 2000 });
          } else {
            setTimeout(() => this.processIdle({ timeRemaining: () => 15 }), 100);
          }
        } else {
          this.isIdleProcessing = false;
        }
      }
    }

    const preloader = new MascotAssetPreloader();

    // ==========================================================================
    // 2. GESTIONNAIRE DE CHARGEMENT RÉSILIENT & RETRY EXPONENTIEL (MascotImageLoader)
    // ==========================================================================
    class MascotImageLoaderController {
      constructor() {
        this.maxRetries = 3;
        this.currentAttempt = 0;
        this.retryTimer = null;
        this.currentTargetUrl = '';
        this.fallbackUrl = '';
      }

      load(targetUrl, fallbackUrl) {
        if (this.retryTimer) {
          clearTimeout(this.retryTimer);
          this.retryTimer = null;
        }
        this.currentTargetUrl = targetUrl;
        this.fallbackUrl = fallbackUrl;
        this.currentAttempt = 0;

        this.hideFallbackOverlay();
        this.executeLoad(targetUrl);
      }

      executeLoad(url) {
        const img = DOM.mascotImg;
        if (!img) return;

        const testImg = new Image();
        testImg.decoding = 'async';
        testImg.onload = () => {
          img.src = url;
          img.classList.remove('opacity-30');
          this.hideFallbackOverlay();
        };

        testImg.onerror = () => {
          this.currentAttempt++;
          if (this.currentAttempt <= this.maxRetries) {
            const backoff = Math.min(3000, 500 * Math.pow(1.8, this.currentAttempt));
            img.classList.add('opacity-30');
            this.retryTimer = setTimeout(() => this.executeLoad(url), backoff);
          } else if (this.fallbackUrl && url !== this.fallbackUrl) {
            // Tentative sur le format statique PNG
            this.executeLoad(this.fallbackUrl);
          } else {
            this.showFallbackOverlay();
          }
        };

        testImg.src = url;
      }

      retry() {
        if (this.currentTargetUrl) {
          this.load(this.currentTargetUrl, this.fallbackUrl);
        }
      }

      showFallbackOverlay() {
        if (DOM.fallbackOverlay) DOM.fallbackOverlay.classList.remove('hidden');
        if (DOM.mascotImg) DOM.mascotImg.classList.add('opacity-10');
      }

      hideFallbackOverlay() {
        if (DOM.fallbackOverlay) DOM.fallbackOverlay.classList.add('hidden');
        if (DOM.mascotImg) DOM.mascotImg.classList.remove('opacity-10');
      }
    }

    const mascotLoader = new MascotImageLoaderController();

    // ==========================================================================
    // 3. SENTINELLE TOAST JAPANDI & DÉTECTION HORS LIGNE (toastSentinel)
    // ==========================================================================
    const toastSentinel = {
      activeToastId: null,
      toastTimeout: null,

      show({ message, type = 'info', duration = 3500, id = null }) {
        const container = DOM.toastContainer;
        if (!container) return;

        if (this.activeToastId && this.activeToastId === id) {
          const existing = document.getElementById(this.activeToastId);
          if (existing) {
            const textEl = existing.querySelector('.toast-msg');
            if (textEl) textEl.textContent = message;
            return;
          }
        }

        this.dismiss();

        const toast = document.createElement('div');
        const toastId = id || `toast-${Date.now()}`;
        this.activeToastId = toastId;
        toast.id = toastId;

        let bgClass = 'bg-[var(--japandi-surface)] border-[var(--japandi-border)] text-[var(--japandi-text)]';
        let iconSvg = '<span class="w-2 h-2 rounded-full bg-[var(--japandi-moss)] shrink-0"></span>';

        if (type === 'offline') {
          bgClass = 'bg-[var(--japandi-surface)] border-[var(--japandi-ochre)] text-[var(--japandi-text)]';
          iconSvg = '<span class="w-2.5 h-2.5 rounded-full bg-[var(--japandi-ochre)] animate-pulse shrink-0"></span>';
        } else if (type === 'online') {
          bgClass = 'bg-[var(--japandi-surface)] border-[var(--japandi-moss)] text-[var(--japandi-text)]';
          iconSvg = '<svg class="w-3.5 h-3.5 text-[var(--japandi-moss)] shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>';
        } else if (type === 'warning') {
          bgClass = 'bg-[var(--japandi-surface)] border-[var(--japandi-ochre)] text-[var(--japandi-text)]';
          iconSvg = '<svg class="w-3.5 h-3.5 text-[var(--japandi-ochre)] shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>';
        }

        toast.className = `pointer-events-auto flex items-center justify-between gap-3 px-3.5 py-2.5 rounded-xl border shadow-modal transition-all duration-300 transform opacity-0 translate-y-[-8px] scale-98 ${bgClass}`;
        toast.innerHTML = `
          <div class="flex items-center gap-2.5 min-w-0">
            ${iconSvg}
            <span class="toast-msg text-xs font-medium tracking-tight truncate">${sanitizePlainText(message)}</span>
          </div>
          <button onclick="toastSentinel.dismiss()" aria-label="Fermer" class="text-[var(--japandi-text-muted)] hover:text-[var(--japandi-text)] p-0.5 rounded cursor-pointer transition">
            <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
          </button>
        `;

        container.appendChild(toast);

        requestAnimationFrame(() => {
          toast.classList.remove('opacity-0', 'translate-y-[-8px]', 'scale-98');
          toast.classList.add('opacity-100', 'translate-y-0', 'scale-100');
        });

        if (duration > 0) {
          this.toastTimeout = setTimeout(() => this.dismiss(), duration);
        }
      },

      dismiss() {
        if (this.toastTimeout) {
          clearTimeout(this.toastTimeout);
          this.toastTimeout = null;
        }
        if (this.activeToastId) {
          const el = document.getElementById(this.activeToastId);
          if (el) {
            el.classList.remove('opacity-100', 'translate-y-0', 'scale-100');
            el.classList.add('opacity-0', 'translate-y-[-8px]', 'scale-98');
            setTimeout(() => el.remove(), 250);
          }
          this.activeToastId = null;
        }
      }
    };

    window.addEventListener('online', () => {
      toastSentinel.show({
        message: window.i18n.get('resilience.onlineStatus') || "Connexion rétablie ✨",
        type: 'online',
        duration: 3500,
        id: 'net-status'
      });
      mascotLoader.retry();
    });

    window.addEventListener('offline', () => {
      toastSentinel.show({
        message: window.i18n.get('resilience.offlineStatus') || "Mode hors ligne actif — Studio 100% fonctionnel",
        type: 'offline',
        duration: 0,
        id: 'net-status'
      });
    });

    // ==========================================================================
    // 4. LIMITATION DE DÉBIT PAR FENÊTRE GLISSANTE & ANTI-BOT (RateLimiter)
    // ==========================================================================
    class SlidingWindowRateLimiter {
      constructor({ maxRequests, windowMs }) {
        this.maxRequests = maxRequests;
        this.windowMs = windowMs;
        this.timestamps = [];
      }

      tryAcquire() {
        const now = Date.now();
        this.timestamps = this.timestamps.filter(t => now - t < this.windowMs);

        if (this.timestamps.length < this.maxRequests) {
          this.timestamps.push(now);
          return { allowed: true, remaining: this.maxRequests - this.timestamps.length, retryAfterSec: 0 };
        }

        const oldest = this.timestamps[0];
        const retryAfterMs = Math.max(0, this.windowMs - (now - oldest));
        return {
          allowed: false,
          remaining: 0,
          retryAfterSec: Math.max(1, Math.ceil(retryAfterMs / 1000))
        };
      }
    }

    const voteLimiter = new SlidingWindowRateLimiter({ maxRequests: 6, windowMs: 8000 });
    const suggestLimiter = new SlidingWindowRateLimiter({ maxRequests: 2, windowMs: 20000 });
    const modalLimiter = new SlidingWindowRateLimiter({ maxRequests: 4, windowMs: 8000 });
    const payLimiter = new SlidingWindowRateLimiter({ maxRequests: 2, windowMs: 10000 });

    // ==========================================================================
    // 4.5 MOTEUR DE GESTES TACTILES DU STUDIO (StageTouchGestureEngine)
    // ==========================================================================
    class StageTouchGestureEngine {
      constructor(stageElement, wrapperElement) {
        if (!stageElement || !wrapperElement) return;
        this.stage = stageElement;
        this.wrapper = wrapperElement;
        this.mascotOrder = ['aituko', 'owluko', 'luneko', 'inuko', 'hatoko', 'usako'];
        
        this.startX = 0;
        this.startY = 0;
        this.currentX = 0;
        this.currentY = 0;
        this.startTime = 0;
        this.isTracking = false;
        this.directionLocked = null; // 'horizontal' | 'vertical' | null
        this.slopThreshold = 8;
        this.minSwipeDist = 36;
        this.minVelocity = 0.28; // px/ms

        this.cueLeft = document.getElementById('swipeCueLeft');
        this.cueRight = document.getElementById('swipeCueRight');

        this.init();
      }

      init() {
        this.stage.addEventListener('touchstart', (e) => this.onTouchStart(e), { passive: true });
        this.stage.addEventListener('touchmove', (e) => this.onTouchMove(e), { passive: false });
        this.stage.addEventListener('touchend', (e) => this.onTouchEnd(e), { passive: true });
        this.stage.addEventListener('touchcancel', () => this.reset(), { passive: true });
      }

      onTouchStart(e) {
        if (e.touches.length !== 1) return;
        const touch = e.touches[0];
        this.startX = touch.clientX;
        this.startY = touch.clientY;
        this.currentX = touch.clientX;
        this.currentY = touch.clientY;
        this.startTime = Date.now();
        this.isTracking = true;
        this.directionLocked = null;
      }

      onTouchMove(e) {
        if (!this.isTracking || e.touches.length !== 1) return;
        const touch = e.touches[0];
        this.currentX = touch.clientX;
        this.currentY = touch.clientY;

        const deltaX = this.currentX - this.startX;
        const deltaY = this.currentY - this.startY;
        const absX = Math.abs(deltaX);
        const absY = Math.abs(deltaY);

        if (!this.directionLocked) {
          if (absX > this.slopThreshold || absY > this.slopThreshold) {
            this.directionLocked = absX >= absY ? 'horizontal' : 'vertical';
          }
        }

        if (this.directionLocked === 'horizontal') {
          if (e.cancelable) e.preventDefault();
          // Effet de résistance élastique Japandi (Rubber Band)
          const rubberX = Math.sign(deltaX) * Math.min(absX * 0.4, 48);
          this.wrapper.style.transform = `translateX(${rubberX}px)`;

          // Indicateurs visuels directionnels
          if (deltaX > 15 && this.cueLeft) {
            this.cueLeft.classList.remove('opacity-0');
            this.cueLeft.classList.add('opacity-100');
          } else if (this.cueLeft) {
            this.cueLeft.classList.remove('opacity-100');
            this.cueLeft.classList.add('opacity-0');
          }

          if (deltaX < -15 && this.cueRight) {
            this.cueRight.classList.remove('opacity-0');
            this.cueRight.classList.add('opacity-100');
          } else if (this.cueRight) {
            this.cueRight.classList.remove('opacity-100');
            this.cueRight.classList.add('opacity-0');
          }
        }
      }

      onTouchEnd(e) {
        if (!this.isTracking) return;
        const deltaX = this.currentX - this.startX;
        const deltaY = this.currentY - this.startY;
        const duration = Math.max(1, Date.now() - this.startTime);
        const velocityX = deltaX / duration;
        const velocityY = deltaY / duration;
        const absX = Math.abs(deltaX);
        const absY = Math.abs(deltaY);

        this.resetVisuals();

        // 1. Détection Tap Direct (Micro-rebond et avance à la pose suivante)
        if (absX < 12 && absY < 12 && duration < 320) {
          this.triggerTapSpring();
          nextPose();
          this.reset();
          return;
        }

        // 2. Swipe Horizontal -> Changement de Pose (← / →)
        if (this.directionLocked === 'horizontal' || (absX > absY && absX > 20)) {
          if (deltaX < -this.minSwipeDist || velocityX < -this.minVelocity) {
            nextPose();
          } else if (deltaX > this.minSwipeDist || velocityX > this.minVelocity) {
            prevPose();
          }
        }
        // 3. Swipe Vertical Direct sur le Canvas -> Changement de Mascotte (Cycle)
        else if (this.directionLocked === 'vertical') {
          if (deltaY < -55 || velocityY < -0.45) {
            this.cycleMascot(1);
          } else if (deltaY > 55 || velocityY > 0.45) {
            this.cycleMascot(-1);
          }
        }

        this.reset();
      }

      triggerTapSpring() {
        this.wrapper.classList.remove('mascot-tap-spring');
        void this.wrapper.offsetWidth;
        this.wrapper.classList.add('mascot-tap-spring');
        setTimeout(() => {
          if (this.wrapper) this.wrapper.classList.remove('mascot-tap-spring');
        }, 400);
      }

      cycleMascot(direction) {
        const curIdx = this.mascotOrder.indexOf(currentMascot);
        const nextIdx = (curIdx + direction + this.mascotOrder.length) % this.mascotOrder.length;
        const targetMascot = this.mascotOrder[nextIdx];
        switchMascot(targetMascot);

        toastSentinel.show({
          message: `Mascotte active : ${MASCOTS[targetMascot].name} ✨`,
          type: 'online',
          duration: 1800,
          id: 'mascot-switch'
        });
      }

      resetVisuals() {
        this.wrapper.style.transition = 'transform 0.25s cubic-bezier(0.16, 1, 0.3, 1)';
        this.wrapper.style.transform = 'translateX(0px)';
        setTimeout(() => {
          if (this.wrapper) this.wrapper.style.transition = '';
        }, 260);

        if (this.cueLeft) {
          this.cueLeft.classList.remove('opacity-100');
          this.cueLeft.classList.add('opacity-0');
        }
        if (this.cueRight) {
          this.cueRight.classList.remove('opacity-100');
          this.cueRight.classList.add('opacity-0');
        }
      }

      reset() {
        this.isTracking = false;
        this.directionLocked = null;
      }
    }

    // ==========================================================================
    // 5. CONTRÔLEURS DE L'APPLICATION & GESTION DES ÉTATS
    // ==========================================================================
    function toggleLangMenu(e) {
      if (e) e.stopPropagation();
      const menu = DOM.langMenu;
      const chevron = DOM.langChevron;
      const btn = DOM.langBtn;
      if (!menu) return;
      const isHidden = menu.classList.contains('hidden');
      
      if (isHidden) {
        menu.classList.remove('hidden');
        if (btn) btn.setAttribute('aria-expanded', 'true');
        if (chevron) chevron.classList.add('rotate-180');
      } else {
        closeLangMenu();
      }
    }

    function closeLangMenu() {
      const menu = DOM.langMenu;
      const chevron = DOM.langChevron;
      const btn = DOM.langBtn;
      if (menu) menu.classList.add('hidden');
      if (btn) btn.setAttribute('aria-expanded', 'false');
      if (chevron) chevron.classList.remove('rotate-180');
    }

    function selectLanguage(lang) {
      if (window.i18n && typeof window.i18n.setLanguage === 'function') {
        window.i18n.setLanguage(lang);
      }
      closeLangMenu();
    }

    document.addEventListener('click', (e) => {
      const container = document.getElementById('langDropdownContainer');
      if (container && !container.contains(e.target)) {
        closeLangMenu();
      }
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        closeLangMenu();
        closeModal();
      }
    });

    function onLanguageChanged(lang) {
      updateMascotMessage();
      updateUI();

      if (DOM.bubbleQuickTxt) {
        DOM.bubbleQuickTxt.textContent = window.i18n.get(isBubbleVisible ? 'studio.bubbleOn' : 'studio.bubbleOff');
      }
      if (DOM.formatBtn) {
        DOM.formatBtn.textContent = window.i18n.get(isAnimated ? 'studio.formatWebp' : 'studio.formatPng');
      }
      if (DOM.catalogueVoteCount) {
        DOM.catalogueVoteCount.textContent = `${totalVotes} ${window.i18n.get('catalogue.voteCountSuffix')}`;
      }

      const barText = document.getElementById('studioQuickBarText');
      if (barText && MASCOTS[currentMascot]) {
        barText.textContent = window.i18n.get('studio.quickBarStatus', { name: MASCOTS[currentMascot].name });
      }

      const headerBtnTxt = document.getElementById('studioHeaderDownloadTxt');
      if (headerBtnTxt && MASCOTS[currentMascot]) {
        headerBtnTxt.textContent = window.i18n.get('studio.downloadPackBtn', { name: MASCOTS[currentMascot].name });
      }
    }

    function updateMascotMessage() {
      const pKey = poseKeys[activeIdx];
      let msg = window.i18n ? window.i18n.get(`messages.${currentMascot}.${pKey}`) : '';
      if (!msg || msg.startsWith('messages.')) {
        msg = "Bienvenue sur votre espace !";
      }
      if (DOM.bubbleInput) DOM.bubbleInput.value = msg;
      if (DOM.bubbleDisplay) DOM.bubbleDisplay.textContent = msg;
    }

    function switchMascot(mKey) {
      if (!MASCOTS[mKey]) return;
      currentMascot = mKey;
      Object.keys(MASCOTS).forEach(k => {
        const tab = document.getElementById(`mascot-tab-${k}`);
        if (tab) {
          if (k === mKey) {
            tab.className = "snap-center shrink-0 px-3.5 sm:px-4 py-2 sm:py-2.5 rounded-xl bg-[var(--japandi-surface)] text-[var(--japandi-text)] text-xs sm:text-sm font-semibold transition flex items-center gap-2 sm:gap-2.5 cursor-pointer shadow-soft min-h-[44px] border border-[var(--japandi-border)]/40";
          } else {
            tab.className = "snap-center shrink-0 px-3.5 sm:px-4 py-2 sm:py-2.5 rounded-xl text-[var(--japandi-text-secondary)] hover:text-[var(--japandi-text)] text-xs sm:text-sm font-medium transition flex items-center gap-2 sm:gap-2.5 cursor-pointer min-h-[44px]";
          }
        }
      });

      updateMascotMessage();
      updateUI();

      const barText = document.getElementById('studioQuickBarText');
      if (barText && MASCOTS[mKey]) {
        barText.textContent = window.i18n.get('studio.quickBarStatus', { name: MASCOTS[mKey].name });
      }

      const headerBtnTxt = document.getElementById('studioHeaderDownloadTxt');
      if (headerBtnTxt && MASCOTS[mKey]) {
        headerBtnTxt.textContent = window.i18n.get('studio.downloadPackBtn', { name: MASCOTS[mKey].name });
      }
    }

    function selectMascotFromCard(mKey) {
      switchMascot(mKey);
      const studio = document.getElementById('studio');
      if (studio) studio.scrollIntoView({ behavior: 'smooth' });
    }

    function setPoseIndex(idx) {
      const parsed = parseInt(idx, 10);
      if (!Number.isInteger(parsed) || parsed < 0 || parsed >= poseKeys.length) return;
      activeIdx = parsed;
      updateMascotMessage();
      updateUI();
    }

    function prevPose() {
      activeIdx = (activeIdx - 1 + poseKeys.length) % poseKeys.length;
      updateMascotMessage();
      updateUI();
    }

    function nextPose() {
      activeIdx = (activeIdx + 1) % poseKeys.length;
      updateMascotMessage();
      updateUI();
    }

    function getAssetPrefix() {
      return getAssetPrefixFor(currentMascot);
    }

    function getAssetPrefixFor(mascotKey) {
      const path = window.location.pathname;
      const inPreview = path.includes('/preview/') || path.endsWith('/preview');
      const base = inPreview ? '../' : '';
      return base + MASCOTS[mascotKey].folderPrefix;
    }

    const ACTIVE_PILL_CLASS = "pose-pill active min-h-[44px] py-2.5 px-2.5 rounded-xl border border-[var(--japandi-border)] bg-[var(--japandi-surface)] text-[var(--japandi-text)] text-xs sm:text-sm font-bold flex items-center justify-center text-center transition truncate cursor-pointer shadow-soft";
    const INACTIVE_PILL_CLASS = "pose-pill min-h-[44px] py-2.5 px-2.5 rounded-xl border border-[var(--japandi-border-subtle)] bg-[var(--japandi-surface-muted)] text-[var(--japandi-text-secondary)] hover:text-[var(--japandi-text)] text-xs sm:text-sm font-medium flex items-center justify-center text-center transition truncate cursor-pointer";

    function updateUI() {
      const pFolder = poseFolders[activeIdx];
      if (DOM.counterTxt) DOM.counterTxt.textContent = `${activeIdx + 1} / ${poseKeys.length}`;
      
      if (DOM.mascotVideo) {
        DOM.mascotVideo.classList.add('hidden');
        DOM.mascotVideo.pause();
      }
      if (DOM.mascotImg) DOM.mascotImg.classList.remove('hidden');
      
      const filename = isAnimated ? "animated.webp?v=chroma-green-20260830-v14" : "static.png?v=chroma-green-20260830-v14";
      const staticFallback = "static.png?v=chroma-green-20260830-v14";
      const prefix = getAssetPrefix();
      
      const targetUrl = `${prefix}${pFolder}/${filename}`;
      const fallbackUrl = `${prefix}${pFolder}/${staticFallback}`;

      // Chargement sécurisé avec retry exponentiel
      mascotLoader.load(targetUrl, fallbackUrl);

      // Préchargement prédictif de l'anneau des poses suivantes
      preloader.preloadRing(currentMascot, activeIdx, isAnimated);

      // Mise à jour différentielle O(1) des pilules
      if (DOM.pills) {
        if (DOM.pills[lastActiveIdx]) DOM.pills[lastActiveIdx].className = INACTIVE_PILL_CLASS;
        if (DOM.pills[activeIdx]) DOM.pills[activeIdx].className = ACTIVE_PILL_CLASS;
        lastActiveIdx = activeIdx;
      }

      renderSnippet();
    }

    function toggleBubbleQuick() {
      toggleBubble(!isBubbleVisible);
    }

    function toggleBubble(val) {
      isBubbleVisible = Boolean(val);
      const b = DOM.bubbleBox;
      const chk = DOM.bubbleToggle;
      const eyeOpen = DOM.eyeOpen;
      const eyeClosed = DOM.eyeClosed;
      const txt = DOM.bubbleQuickTxt;
      
      if (chk) chk.checked = isBubbleVisible;

      if (isBubbleVisible) {
        if (b) b.classList.remove('hidden');
        if (eyeOpen) eyeOpen.classList.remove('hidden');
        if (eyeClosed) eyeClosed.classList.add('hidden');
        if (txt) txt.textContent = window.i18n.get('studio.bubbleOn');
      } else {
        if (b) b.classList.add('hidden');
        if (eyeOpen) eyeOpen.classList.add('hidden');
        if (eyeClosed) eyeClosed.classList.remove('hidden');
        if (txt) txt.textContent = window.i18n.get('studio.bubbleOff');
      }
      renderSnippet();
    }

    function updateBubbleText(val) {
      if (DOM.bubbleDisplay) DOM.bubbleDisplay.textContent = val;
      renderSnippet();
    }

    window.addEventListener('keydown', (e) => {
      if (e.target.matches('input, textarea')) return;
      if (DOM.buyModal && !DOM.buyModal.classList.contains('hidden')) return;

      if (e.key === 'ArrowLeft') prevPose();
      if (e.key === 'ArrowRight') nextPose();
    });

    function zoomIn() {
      setSize(currentSize + 20);
    }

    function zoomOut() {
      setSize(currentSize - 20);
    }

    function setSize(v) {
      scheduledSize = clampSize(v);
      if (!sizeRafId) {
        sizeRafId = requestAnimationFrame(flushSizeTransform);
      }
    }

    function flushSizeTransform() {
      sizeRafId = null;
      currentSize = scheduledSize;
      
      if (DOM.sizeTxt) DOM.sizeTxt.textContent = `${currentSize}px`;
      if (DOM.mascotStageWrapper) {
        DOM.mascotStageWrapper.style.width = `${currentSize}px`;
        DOM.mascotStageWrapper.style.height = `${currentSize}px`;
      }

      if (snippetDebounceTimer) clearTimeout(snippetDebounceTimer);
      snippetDebounceTimer = setTimeout(renderSnippet, 30);
    }

    function toggleFormat() {
      isAnimated = !isAnimated;
      if (DOM.formatBtn) {
        DOM.formatBtn.textContent = isAnimated ? "WebP" : "PNG";
      }
      updateUI();
    }

    function setBg(t) {
      const b = DOM.stageBox;
      if (!b) return;
      b.className = "relative rounded-3xl border border-[var(--japandi-border)] min-h-[340px] sm:min-h-[380px] flex flex-col items-center justify-center p-4 sm:p-6 transition-all duration-300 shadow-card select-none";
      if (t === 'default') b.classList.add('bg-[var(--japandi-surface-stage)]');
      if (t === 'dark') b.classList.add('bg-[#141416]');
      if (t === 'stone') b.classList.add('bg-[#F3F1EC]');
      if (t === 'checker') b.classList.add('bg-checker');
    }

    function setFw(f) {
      if (!ALLOWED_FRAMEWORKS.includes(f)) return;
      currentFw = f;
      ALLOWED_FRAMEWORKS.forEach(item => {
        const btn = DOM.fwBtns[item];
        if (btn) {
          btn.className = item === f 
            ? "text-[var(--japandi-text)] font-semibold cursor-pointer py-1 px-1.5" 
            : "text-[var(--japandi-text-secondary)] hover:text-[var(--japandi-text)] font-medium cursor-pointer transition py-1 px-1.5";
        }
      });
      renderSnippet();
    }

    function renderSnippet() {
      const pKey = poseKeys[activeIdx];
      const m = MASCOTS[currentMascot];
      const animProp = isAnimated ? ' animated' : '';
      const inputEl = DOM.bubbleInput;
      const rawMsg = inputEl ? inputEl.value : (DOM.bubbleDisplay ? DOM.bubbleDisplay.textContent : '');
      const c = DOM.codeBlock;
      if (!c || !m) return;

      if (currentFw === 'react') {
        const escaped = sanitizeForJsx(rawMsg);
        const msgProp = isBubbleVisible ? ` message="${escaped}"` : '';
        c.textContent = `<${m.component} state="${pKey}" size={${currentSize}}${msgProp}${animProp} />`;
      } else if (currentFw === 'vue') {
        const escaped = sanitizeForJsx(rawMsg);
        const msgProp = isBubbleVisible ? ` message="${escaped}"` : '';
        c.textContent = `<${m.component} state="${pKey}" :size="${currentSize}"${msgProp}${animProp} />`;
      } else if (currentFw === 'flutter') {
        const camel = pKey.replace(/_([a-z])/g, g => g[1].toUpperCase());
        const escaped = sanitizeForDart(rawMsg);
        const flutterMsg = isBubbleVisible ? `, message: '${escaped}'` : '';
        c.textContent = `${m.flutter}(state: ${m.component}State.${camel}, size: ${currentSize}.0${flutterMsg})`;
      } else if (currentFw === 'html') {
        const folder = poseFolders[activeIdx];
        const file = isAnimated ? `${m.folderPrefix}${folder}/animated.webp` : `${m.folderPrefix}${folder}/static.png`;
        c.textContent = `<img src="${file}" width="${currentSize}" height="${currentSize}" alt="${sanitizeForJsx(m.name)}" />`;
      }
    }

    function copyCode() {
      const codeBlock = DOM.codeBlock;
      if (!codeBlock) return;
      navigator.clipboard.writeText(codeBlock.textContent).then(() => {
        const copyTxt = DOM.copyTxt;
        if (copyTxt) {
          copyTxt.textContent = window.i18n.get('studio.copied');
          setTimeout(() => { copyTxt.textContent = window.i18n.get('studio.copyCode'); }, 2000);
        }
      });
    }

    // Gestion du Thème (Dark & Light)
    function initTheme() {
      const savedTheme = safeStorage.get('uko_theme');
      if (ALLOWED_THEMES.includes(savedTheme)) {
        setTheme(savedTheme);
      } else {
        const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
        setTheme(prefersDark ? 'dark' : 'light');
      }
    }

    function toggleTheme() {
      const isDark = document.documentElement.classList.contains('dark');
      setTheme(isDark ? 'light' : 'dark');
    }

    function setTheme(mode) {
      if (!ALLOWED_THEMES.includes(mode)) return;
      const sun = document.getElementById('themeIconSun');
      const moon = document.getElementById('themeIconMoon');
      
      if (mode === 'dark') {
        document.documentElement.classList.add('dark');
        safeStorage.set('uko_theme', 'dark');
        if (sun) sun.classList.remove('hidden');
        if (moon) moon.classList.add('hidden');
      } else {
        document.documentElement.classList.remove('dark');
        safeStorage.set('uko_theme', 'light');
        if (sun) sun.classList.add('hidden');
        if (moon) moon.classList.remove('hidden');
      }
    }

    // Téléchargement Direct 1-Clic du Pack Gratuit (Zéro friction, zéro formulaire inutile)
    function downloadFreeSample() {
      const m = MASCOTS[currentMascot] || MASCOTS.aituko;
      const zipPath = m.zips.free;
      
      const a = document.createElement('a');
      a.href = zipPath;
      a.download = zipPath.split('/').pop();
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);

      toastSentinel.show({
        message: window.i18n.get('pricing.freeDownloadStarted', { name: m.name }),
        type: 'info',
        duration: 3500
      });
    }

    let currentModalMascot = 'aituko';

    function setModalMascot(mKey) {
      if (!MASCOTS[mKey]) return;
      currentModalMascot = mKey;

      Object.keys(MASCOTS).forEach(k => {
        const tab = document.getElementById(`modal-tab-${k}`);
        if (tab) {
          if (k === mKey) {
            tab.className = "py-2 px-1.5 rounded-xl bg-[var(--japandi-surface)] text-[var(--japandi-text)] shadow-soft font-semibold transition flex items-center justify-center gap-1.5 cursor-pointer min-h-[44px]";
          } else {
            tab.className = "py-2 px-1.5 rounded-xl text-[var(--japandi-text-secondary)] hover:text-[var(--japandi-text)] font-medium transition flex items-center justify-center gap-1.5 cursor-pointer min-h-[44px]";
          }
        }
      });

      updateModalSummary();
    }

    function updateModalSummary() {
      const m = MASCOTS[currentModalMascot];
      if (!m) return;
      const name = DOM.modalTierName;
      const price = DOM.modalPrice;
      const dl = DOM.downloadLink;
      const btn = DOM.paySubmitBtn;

      if (currentModalTier === 'free') {
        if (name) name.textContent = `${m.name} — ${window.i18n.get('pricing.freeTierTitle')}`;
        if (price) price.textContent = window.i18n.get('pricing.freeTierPrice');
        if (dl) dl.href = m.zips.free;
        if (btn) btn.textContent = window.i18n.get('modal.submitBtn');
      } else if (currentModalTier === 'starter') {
        if (name) name.textContent = `${m.name} — ${window.i18n.get('pricing.starterTierTitle')}`;
        if (price) price.textContent = window.i18n.get('pricing.starterTierPrice');
        if (dl) dl.href = m.zips.starter;
        if (btn) {
          const val = window.i18n.get('modal.payBtn');
          btn.textContent = (val && val !== 'modal.payBtn') ? val : "Procéder au Paiement Sécurisé";
        }
      } else {
        if (name) name.textContent = `${m.name} — ${window.i18n.get('pricing.proTierTitle')}`;
        if (price) price.textContent = window.i18n.get('pricing.proTierPrice');
        if (dl) dl.href = m.zips.pro;
        if (btn) {
          const val = window.i18n.get('modal.payBtn');
          btn.textContent = (val && val !== 'modal.payBtn') ? val : "Procéder au Paiement Sécurisé";
        }
      }
    }

    // Modal Achat & Téléchargement Sécurisé (Protégé par Rate Limiter & Honeypot)
    function openModal(tier = 'pro') {
      const limitCheck = modalLimiter.tryAcquire();
      if (!limitCheck.allowed) {
        toastSentinel.show({
          message: window.i18n.get('resilience.rateLimitModal') || "Trop de requêtes rapides.",
          type: 'warning',
          duration: 2500
        });
        return;
      }

      if (!ALLOWED_TIERS.includes(tier)) tier = 'pro';
      currentModalTier = tier;
      currentModalMascot = currentMascot;

      const m = DOM.buyModal;
      const btn = DOM.paySubmitBtn;
      const successBox = DOM.paySuccess;

      if (btn) {
        btn.textContent = tier === 'free' 
          ? window.i18n.get('modal.submitBtn') 
          : (window.i18n.get('modal.payBtn') || "Procéder au Paiement Sécurisé");
        btn.disabled = false;
        btn.classList.remove('hidden');
      }
      if (successBox) {
        successBox.classList.add('hidden');
      }

      setModalMascot(currentModalMascot);

      if (m) {
        m.classList.remove('hidden');
        m.classList.add('flex');
      }

      setTimeout(() => {
        const input = document.querySelector('#buyModal input[type="email"]');
        if (input) input.focus();
      }, 50);
    }

    
    // Gestion de la Modale de Licence Commerciale
    function openLicenseModal() {
      const modal = document.getElementById('licenseModal');
      if (modal) {
        modal.classList.remove('hidden');
        modal.classList.add('flex');
      }
    }

    function closeLicenseModal() {
      const modal = document.getElementById('licenseModal');
      if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
      }
    }

    function closeModal() {
      const m = DOM.buyModal;
      if (m) {
        m.classList.add('hidden');
        m.classList.remove('flex');
      }
    }

    function handlePay(e) {
      e.preventDefault();

      // Piège Honeypot Bot Modal
      const hp = document.getElementById('modal_hp_website');
      if (hp && hp.value.trim().length > 0) {
        console.warn('[Anti-Bot] Honeypot déclenché sur le modal checkout.');
        const btn = DOM.paySubmitBtn;
        if (btn) {
          btn.textContent = window.i18n.get('modal.preparing');
          btn.disabled = true;
        }
        setTimeout(() => {
          if (btn) btn.classList.add('hidden');
          if (DOM.paySuccess) DOM.paySuccess.classList.remove('hidden');
        }, 500);
        return;
      }

      // Limitation de débit
      const limitCheck = payLimiter.tryAcquire();
      if (!limitCheck.allowed) {
        toastSentinel.show({
          message: window.i18n.get('resilience.rateLimitModal') || "Trop de requêtes rapides.",
          type: 'warning',
          duration: 2500
        });
        return;
      }

      const emailInput = document.querySelector('#buyModal input[type="email"]');
      const email = emailInput ? emailInput.value.trim() : '';
      if (!email) return;

      const btn = DOM.paySubmitBtn;
      if (btn) {
        btn.textContent = window.i18n.get('modal.preparing');
        btn.disabled = true;
      }

      // Pack Gratuit → Téléchargement direct immédiat
      if (currentModalTier === 'free') {
        setTimeout(() => {
          if (btn) btn.classList.add('hidden');
          const dl = DOM.downloadLink;
          if (dl) dl.href = MASCOTS[currentModalMascot].zips.free;
          if (DOM.paySuccess) DOM.paySuccess.classList.remove('hidden');
        }, 400);
        return;
      }

      // Pack Payant → Redirection Stripe Checkout
      fetch('/api/create-checkout-session', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tier: currentModalTier,
          mascot: currentModalMascot,
          email: email,
          origin: window.location.origin,
        }),
      })
      .then(r => r.json())
      .then(data => {
        if (data.url) {
          window.location.href = data.url;
        } else {
          throw new Error(data.error || 'Stripe session creation failed');
        }
      })
      .catch(err => {
        console.error('[Stripe]', err);
        if (btn) {
          btn.textContent = window.i18n.get('modal.payBtn', {}, 'Réessayer');
          btn.disabled = false;
        }
        toastSentinel.show({ message: 'Erreur de paiement. Veuillez réessayer.', type: 'error', duration: 3000 });
      });
    }

    // Système de Vote Communautaire Sécurisé (Rate Limité)
    let voteCounts = {
      kumako: 128,
      kitsuko: 94,
      duckuko: 71,
      panduko: 49
    };
    let totalVotes = 342;
    let userVotedKey = null;
    let feedbackTimer = null;

    function formatCandidateName(key) {
      return key.charAt(0).toUpperCase() + key.slice(1);
    }

    function toggleCandidateVote(candidate) {
      const limitCheck = voteLimiter.tryAcquire();
      if (!limitCheck.allowed) {
        showInlineFeedback(window.i18n.get('resilience.rateLimitVote') || "Ralentissez un instant avant de revoter.");
        return;
      }

      if (!Object.prototype.hasOwnProperty.call(voteCounts, candidate)) return;
      const displayName = formatCandidateName(candidate);
      const isCancelling = (userVotedKey === candidate);

      if (isCancelling) {
        voteCounts[candidate]--;
        totalVotes--;
        userVotedKey = null;

        updateInlineVoteUI(candidate, false);
        showInlineFeedback(window.i18n.get('catalogue.voteCancelMsg', { name: displayName }));
      } else {
        if (userVotedKey) {
          voteCounts[userVotedKey]--;
          updateInlineVoteUI(userVotedKey, false);
        } else {
          totalVotes++;
        }

        voteCounts[candidate]++;
        userVotedKey = candidate;

        updateInlineVoteUI(candidate, true);
        showInlineFeedback(window.i18n.get('catalogue.voteSuccessMsg', { name: displayName }));
      }

      if (DOM.catalogueVoteCount) DOM.catalogueVoteCount.textContent = `${totalVotes} ${window.i18n.get('catalogue.voteCountSuffix')}`;
    }

    function updateInlineVoteUI(candidate, isActive) {
      const card = document.getElementById(`vote-card-${candidate}`);
      const badge = document.getElementById(`badge-${candidate}`);

      if (card && badge) {
        if (isActive) {
          card.classList.add('border-[var(--japandi-ochre)]', 'bg-[var(--japandi-ochre-subtle)]');
          badge.classList.remove('hidden');
        } else {
          card.classList.remove('border-[var(--japandi-ochre)]', 'bg-[var(--japandi-ochre-subtle)]');
          badge.classList.add('hidden');
        }
      }
    }

    function submitCustomSuggestion(e) {
      e.preventDefault();

      // Piège Honeypot
      const hp = document.getElementById('suggestion_hp_field');
      if (hp && hp.value.trim().length > 0) {
        console.warn('[Anti-Bot] Honeypot déclenché sur suggestion.');
        const input = document.getElementById('inlineCustomInput');
        if (input) input.value = '';
        showInlineFeedback(window.i18n.get('catalogue.suggestSuccessMsg', { val: "..." }));
        return;
      }

      // Limitation de débit
      const limitCheck = suggestLimiter.tryAcquire();
      if (!limitCheck.allowed) {
        showInlineFeedback(window.i18n.get('resilience.rateLimitSuggest', { sec: limitCheck.retryAfterSec }));
        return;
      }

      const input = document.getElementById('inlineCustomInput');
      if (!input) return;
      const val = sanitizePlainText(input.value).slice(0, 60);
      if (!val) return;

      totalVotes++;
      if (DOM.catalogueVoteCount) DOM.catalogueVoteCount.textContent = `${totalVotes} ${window.i18n.get('catalogue.voteCountSuffix')}`;

      input.value = '';
      showInlineFeedback(window.i18n.get('catalogue.suggestSuccessMsg', { val: val }));
    }

    function showInlineFeedback(msg) {
      const fb = document.getElementById('inlineVoteFeedback');
      if (!fb) return;
      if (feedbackTimer) {
        clearTimeout(feedbackTimer);
      }
      fb.textContent = msg;
      fb.classList.remove('hidden');
      feedbackTimer = setTimeout(() => {
        fb.classList.add('hidden');
        feedbackTimer = null;
      }, 3500);
    }

    // ==========================================================================
    // 6. SUITE DE BENCHMARK & STRESS-TEST AUTOMATISÉE (window.UkoPerformanceBenchmark)
    // ==========================================================================
    window.UkoPerformanceBenchmark = {
      async runAll() {
        console.log('%c[Uko Performance Suite] Démarrage du stress-test complet...', 'color: #2E5844; font-weight: bold;');
        const results = {};
        results.poseTransitions = await this.benchmarkPoseTransitions(100);
        results.sliderScrubbing = await this.benchmarkSliderScrubbing(100);
        results.i18nBatchUpdates = await this.benchmarkI18nUpdates(14);
        results.preloaderStatus = this.inspectPreloader();
        console.table(results);
        return results;
      },

      async benchmarkPoseTransitions(iterations = 100) {
        const t0 = performance.now();
        for (let i = 0; i < iterations; i++) {
          setPoseIndex(i % 12);
          await new Promise(r => requestAnimationFrame(r));
        }
        const totalTime = performance.now() - t0;
        const avgPerFrame = (totalTime / iterations).toFixed(2);
        return { iterations, totalTimeMs: totalTime.toFixed(1), avgPerFrameMs: avgPerFrame, fps: (1000 / avgPerFrame).toFixed(1) };
      },

      async benchmarkSliderScrubbing(iterations = 100) {
        const t0 = performance.now();
        for (let i = 0; i < iterations; i++) {
          const size = 120 + ((i * 3) % 160);
          setSize(size);
          await new Promise(r => requestAnimationFrame(r));
        }
        const totalTime = performance.now() - t0;
        const avgPerFrame = (totalTime / iterations).toFixed(2);
        return { iterations, totalTimeMs: totalTime.toFixed(1), avgPerFrameMs: avgPerFrame, targetFps: 60 };
      },

      async benchmarkI18nUpdates(iterations = 14) {
        const langs = ['en', 'fr', 'es', 'de', 'ja', 'pt', 'zh'];
        const t0 = performance.now();
        for (let i = 0; i < iterations; i++) {
          window.i18n.setLanguage(langs[i % langs.length]);
          await new Promise(r => requestAnimationFrame(r));
        }
        const totalTime = performance.now() - t0;
        return { iterations, totalTimeMs: totalTime.toFixed(1), avgPerSwitchMs: (totalTime / iterations).toFixed(2) };
      },

      inspectPreloader() {
        return {
          cachedAssetsCount: preloader.cache.size,
          queuedIdleCount: preloader.idleQueue.length
        };
      }
    };

    // Initialisation au chargement du DOM
    window.addEventListener('DOMContentLoaded', () => {
      initDOMRegistry();
      initTheme();
      if (window.i18n && typeof window.i18n.updateDOM === 'function') {
        window.i18n.updateDOM();
      }
      updateMascotMessage();
      updateUI();

      // Initialisation du Moteur de Gestes Tactiles du Stage
      const stageBox = document.getElementById('stageBox');
      const mascotStageWrapper = document.getElementById('mascotStageWrapper');
      if (stageBox && mascotStageWrapper) {
        window.stageGestureEngine = new StageTouchGestureEngine(stageBox, mascotStageWrapper);
      }

      // Deep linking via URL Parameters (?mascot=inuko&pose=7&dark=1&scroll=studio)
      try {
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.has('mascot')) {
          switchMascot(urlParams.get('mascot'));
        }
        if (urlParams.has('pose')) {
          selectPose(parseInt(urlParams.get('pose'), 10));
        }
        if (urlParams.get('dark') === '1') {
          setTheme('dark');
        }
        if (urlParams.has('scroll')) {
          const targetId = urlParams.get('scroll');
          const targetEl = document.getElementById(targetId);
          if (targetEl) {
            targetEl.scrollIntoView({ behavior: 'instant', block: 'start' });
          }
        }
      } catch (err) {
        console.warn('URL params parsing failed:', err);
      }
    });
  