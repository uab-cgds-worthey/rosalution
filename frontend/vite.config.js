// / <reference types="vitest" />
import {defineConfig} from 'vite';
import vue from '@vitejs/plugin-vue';
import strip from '@rollup/plugin-strip';

import * as path from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  test: {
    environment: 'happy-dom',
    coverage: {
      exclude: [
        'test', 'src/requests.js', 'eslint.config.js', 'eslint-config-cgds.js', 'src/main.js', 'vite.config.js', 'dist',
      ],
      lines: 80,
      functions: 80,
      branches: 80,
      provider: 'v8',
    },
    sequence: {
      hooks: 'parallel',
    },
    include: ['test/**/*.spec.js'],
    deps: {
      moduleDirectories: ['node_modules', path.resolve('./test/__mocks__')],
    },
    setupFiles: ['./test/setup-tests.js'],
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
        include: ['**/*.js', '**/*.vue'],
        labels: ['development'],
      }),
      apply: 'build',
    },
  ],
});
