/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        navy: { 900: '#0a0f1a', 800: '#111827', 700: '#1e293b' },
        aero: { blue: '#3b82f6', green: '#10b981', amber: '#f59e0b', red: '#ef4444' },
      },
    },
  },
  plugins: [],
}
