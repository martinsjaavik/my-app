/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // NYT Connections color scheme
        'connections': {
          'yellow': '#f9df6d',
          'green': '#a0c35a',
          'blue': '#b0c4ef',
          'purple': '#ba81c5',
          'tile': '#efefe6',
          'tile-selected': '#5a594e',
          'bg': '#ffffff',
          'bg-dark': '#121213',
        }
      },
      animation: {
        'shake': 'shake 0.5s ease-in-out',
        'bounce-in': 'bounceIn 0.3s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
      },
      keyframes: {
        shake: {
          '0%, 100%': { transform: 'translateX(0)' },
          '25%': { transform: 'translateX(-5px)' },
          '75%': { transform: 'translateX(5px)' },
        },
        bounceIn: {
          '0%': { transform: 'scale(0.9)', opacity: '0' },
          '50%': { transform: 'scale(1.05)' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}
