// / <reference types="vitest" />
import {defineConfig} from 'vite';
import vue from '@vitejs/plugin-vue';
import strip from '@rollup/plugin-strip';
const path = require('path');

// https://vitejs.dev/config/
export default defineConfig({
  test: {
    global: true,
    environment: 'happy-dom',
    coverage: {
      exclude: ['test', 'src/requests.js', 'src/cookie.js'],
      lines: 80,
      functions: 80,
      branches: 80,
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
    {
      ...strip({
        include: ['**/*.js','**/*.vue'],
        labels: ['label']
      }),
      apply: 'build'
    }
  ],
});
