/** @type {import('tailwindcss').Config} */
import colors from 'tailwindcss/colors';

export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: colors.blue[600],
        surface: colors.white,
        background: colors.gray[50],
        'text-main': colors.gray[900],
      }
    },
  },
  plugins: [],
}
