import React, { useState } from 'react';

export type MascotState = 'idle' | 'waving' | 'celebrating' | 'ai_thinking' | 'error_404' | 'thumbs_up' | 'sleeping';

export interface MascotProps {
  /** État de la mascotte */
  state?: MascotState;
  /** Taille en pixels (carré) */
  size?: number;
  /** Utiliser la version animée continue (WebP 60fps) au lieu du PNG statique */
  animated?: boolean;
  /** Classe CSS personnalisée */
  className?: string;
  /** Action au clic */
  onClick?: () => void;
  /** Active l'effet de lueur néon adaptatif */
  glow?: boolean;
}

const STATIC_ASSETS: Record<MascotState, string> = {
  idle: '/assets/processed/waving_transparent.webp',
  waving: '/assets/processed/waving_transparent.webp',
  celebrating: '/assets/processed/celebrating_transparent.webp',
  ai_thinking: '/assets/processed/ai_thinking_transparent.webp',
  error_404: '/assets/processed/error_404_transparent.webp',
  thumbs_up: '/assets/processed/thumbs_up_transparent.webp',
  sleeping: '/assets/processed/sleeping_transparent.webp',
};

const ANIMATED_ASSETS: Record<MascotState, string> = {
  idle: '/assets/processed/waving_animated.webp',
  waving: '/assets/processed/waving_animated.webp',
  celebrating: '/assets/processed/celebrating_animated.webp',
  ai_thinking: '/assets/processed/ai_thinking_animated.webp',
  error_404: '/assets/processed/error_404_animated.webp',
  thumbs_up: '/assets/processed/thumbs_up_animated.webp',
  sleeping: '/assets/processed/sleeping_animated.webp',
};

const GLOW_COLORS: Record<MascotState, string> = {
  idle: '#06B6D4',
  waving: '#06B6D4',
  celebrating: '#F59E0B',
  ai_thinking: '#3B82F6',
  error_404: '#EF4444',
  thumbs_up: '#10B981',
  sleeping: '#8B5CF6',
};

export const Mascot: React.FC<MascotProps> = ({
  state = 'idle',
  size = 180,
  animated = true,
  className = '',
  onClick,
  glow = true,
}) => {
  const [isHovered, setIsHovered] = useState(false);
  const assetUrl = animated ? ANIMATED_ASSETS[state] : STATIC_ASSETS[state];

  return (
    <div
      role="img"
      aria-label={`ByteBot ${state}`}
      onClick={onClick}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      className={`relative inline-flex items-center justify-center select-none cursor-pointer transition-all duration-300 ${
        isHovered ? 'scale-105 -translate-y-1' : ''
      } ${className}`}
      style={{ width: size, height: size }}
    >
      {glow && (
        <div
          className="absolute inset-0 rounded-full blur-2xl opacity-40 transition-opacity duration-300 pointer-events-none"
          style={{
            backgroundColor: GLOW_COLORS[state],
            transform: isHovered ? 'scale(1.2)' : 'scale(0.85)',
          }}
        />
      )}
      <img
        src={assetUrl}
        alt={`ByteBot in state ${state}`}
        className="w-full h-full object-contain drop-shadow-xl z-10"
        loading="eager"
      />
    </div>
  );
};

export default Mascot;
