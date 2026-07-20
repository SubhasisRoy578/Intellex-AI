// Premium Dark Gold Theme for Intellex AI
// A luxury design system with sophisticated colors, typography, and animations

export const colors = {
  // Primary dark background colors
  background: '#0A0A0A',
  surface: '#141414',
  card: '#1B1B1B',
  border: '#2D2D2D',
  
  // Premium gold accent colors
  gold: '#D4AF37',
  goldLight: '#E8C547',
  goldDim: '#B8860B',
  
  // Complementary colors
  amber: '#F59E0B',
  orange: '#FB923C',
  
  // Text colors
  textPrimary: '#FFFFFF',
  textSecondary: '#A3A3A3',
  textTertiary: '#707070',
  
  // Status colors
  success: '#10B981',
  error: '#EF4444',
  warning: '#F59E0B',
  info: '#3B82F6',
  
  // Interactive states
  hover: '#242424',
  active: '#2D2D2D',
  disabled: '#404040',
};

export const typography = {
  fontFamily: {
    sans: 'ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
    serif: 'ui-serif, Georgia, serif',
    mono: 'ui-monospace, "SF Mono", Monaco, monospace',
  },
  
  // Font sizes in rem
  fontSize: {
    xs: '0.75rem',      // 12px
    sm: '0.875rem',     // 14px
    base: '1rem',       // 16px
    lg: '1.125rem',     // 18px
    xl: '1.25rem',      // 20px
    '2xl': '1.5rem',    // 24px
    '3xl': '1.875rem',  // 30px
    '4xl': '2.25rem',   // 36px
    '5xl': '3rem',      // 48px
  },
  
  // Line heights
  lineHeight: {
    tight: 1.2,
    normal: 1.5,
    relaxed: 1.6,
    loose: 1.8,
  },
  
  // Font weights
  fontWeight: {
    light: 300,
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
    extrabold: 800,
  },
};

export const spacing = {
  '0': '0',
  '1': '0.25rem',   // 4px
  '2': '0.5rem',    // 8px
  '3': '0.75rem',   // 12px
  '4': '1rem',      // 16px
  '5': '1.25rem',   // 20px
  '6': '1.5rem',    // 24px
  '8': '2rem',      // 32px
  '10': '2.5rem',   // 40px
  '12': '3rem',     // 48px
  '16': '4rem',     // 64px
  '20': '5rem',     // 80px
  '24': '6rem',     // 96px
};

export const shadows = {
  sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
  base: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1)',
  md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1)',
  lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1)',
  xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1)',
  
  // Premium shadows with gold accent
  goldGlow: '0 0 20px rgba(212, 175, 55, 0.15)',
  goldGlowLarge: '0 0 40px rgba(212, 175, 55, 0.2)',
};

export const transitions = {
  fast: 'all 150ms ease-out',
  base: 'all 250ms ease-out',
  slow: 'all 350ms ease-out',
  
  // Specific transitions
  color: 'color 250ms ease-out',
  transform: 'transform 250ms ease-out',
  opacity: 'opacity 250ms ease-out',
};

export const borderRadius = {
  none: '0',
  sm: '0.25rem',    // 4px
  base: '0.5rem',   // 8px
  md: '0.75rem',    // 12px
  lg: '1rem',       // 16px
  xl: '1.5rem',     // 24px
  '2xl': '2rem',    // 32px
  full: '9999px',
};

export const animation = {
  // Duration in milliseconds
  duration: {
    instant: 0,
    fast: 150,
    base: 250,
    slow: 350,
    slower: 500,
  },
  
  // Easing functions
  easing: {
    linear: 'linear',
    easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
    easeOut: 'cubic-bezier(0, 0, 0.2, 1)',
    easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
    easeQuad: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)',
  },
};
