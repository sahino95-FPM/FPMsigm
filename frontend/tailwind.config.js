/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#e6f5e6',
          100: '#c2e6c2',
          200: '#9dd69d',
          300: '#78c678',
          400: '#53b653',
          500: '#2ea62e',
          600: '#006b01',
          700: '#005501',
          800: '#004001',
          900: '#002a01',
        },
      },
      fontFamily: {
        sans: ['Tahoma', 'Arial', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
