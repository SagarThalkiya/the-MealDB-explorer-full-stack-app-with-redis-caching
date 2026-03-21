import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  // We removed the proxy entirely because it doesn't work on Vercel anyway
});