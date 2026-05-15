/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#166534',
        secondary: '#15803D',
        accent: '#22C55E',
        darktext: '#4B5563',
        lightbg: '#F3F4F6',
        cardbg: '#F8FAFC',
      },
      fontFamily: {
        pacifico: ['Pacifico', 'cursive'],
        roboto: ['Roboto', 'sans-serif'],
      },
    },
  },
  plugins: [],
}