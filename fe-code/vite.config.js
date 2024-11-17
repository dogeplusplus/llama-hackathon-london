import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/upload": "http://localhost:8000",
    },
  },
  "/pdfs": {
    target: "http://localhost:8000",
    changeOrigin: true,
    secure: false,
  },
})



