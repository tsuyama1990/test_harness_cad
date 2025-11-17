/// <reference types="vitest" />
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/setupTests.ts',
    coverage: {
      enabled: false,
    },
  },
  server: {
    proxy: process.env.DISABLE_PROXY === 'true' 
      ? undefined 
      : {
          '/api': {
            target: 'http://127.0.0.1:8000',
            changeOrigin: true,
          },
        },
  },
})
