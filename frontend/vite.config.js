// / <reference types="vitest" />
import {defineConfig} from 'vite';
import vue from '@vitejs/plugin-vue';
const path = require('path');

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    hmr: {
      clientPort: 3001,
    },
    proxy: {
      // proxying websockets or socket.io
      '/socket.io': {
        target: 'ws://localhost:3001',
        ws: true,
      },
    },
  },
  test: {
    global: true,
    environment: 'happy-dom',
    coverage: {
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  plugins: [
    vue({
      template: {
        compilerOptions: {
          isCustomElement: (tag) => {
            return tag.startsWith('app-');
          },
        },
      },
    }),
  ],
});
