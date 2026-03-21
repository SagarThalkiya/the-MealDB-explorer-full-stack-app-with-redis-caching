import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'https://the-meal-db-explorer-full-stack-app-with-redis-cachi-ni51ikyxm.vercel.app',
        changeOrigin: true,
      },
    },
  },
});

