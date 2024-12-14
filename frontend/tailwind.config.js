/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          light: '#E8F5FE',
          dark: '#343541',
        },
        secondary: {
          light: '#F7F7F8',
          dark: '#444654',
        },
        accent: {
          light: '#0EA5E9',
          dark: '#2563EB',
        }
      }
    },
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: ["light", "dark"],
  },
}