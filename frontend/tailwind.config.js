/** @type {import('tailwindcss').Config} */
import colors from 'tailwindcss/colors';

export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        pixel: ['"VT323"', 'monospace'],
      },
      colors: {
        primary: '#3b82f6', // Keep blue but maybe we can tweak later
        'primary-dark': '#1d4ed8',
        surface: '#4a4a4a',
        background: '#2f2f2f',
        'text-main': '#ffffff',
        'pixel-border': '#000000',
      },
      boxShadow: {
        'pixel': '4px 4px 0px 0px #000000',
        'pixel-sm': '2px 2px 0px 0px #000000',
        'pixel-lg': '6px 6px 0px 0px #000000',
      },
    },
  },
  plugins: [],
}
