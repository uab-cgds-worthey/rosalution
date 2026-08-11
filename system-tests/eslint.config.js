import {defineConfig} from 'eslint/config';

import js from '@eslint/js';

import pluginCypress from 'eslint-plugin-cypress';
import cgds from './eslint-config-cgds.js';


export default defineConfig([
  {
    name: 'system-test-project',
    files: ['**/*.js'],
    plugins: {js},
    extends: [
      'js/recommended',
      cgds,
      pluginCypress.configs.recommended,
    ],
    languageOptions: {
      sourceType: 'module',
      ecmaVersion: 2022,
    },
  },
]);
