// frontend/vite.config.js
import { defineConfig } from 'vite'

export default defineConfig({
  server: {
    origin: 'http://localhost:5173',
    cors: true,
    strictPort: true,
  }
})