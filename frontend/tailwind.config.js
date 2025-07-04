/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Videoflix colors based on Figma design
        'videoflix-black': '#000000',
        'videoflix-dark': '#141414', 
        'videoflix-gray': '#2f2f2f',
        'videoflix-light-gray': '#564d4d',
        'videoflix-red': '#e50914',
        'videoflix-red-hover': '#f40612',
      },
      fontFamily: {
        'sans': ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
