import js from '@eslint/js';
import globals from 'globals';

import pluginCypress from 'eslint-plugin-cypress/flat';
import cgds from './eslint-config-cgds.js';


export default [
  {
    ignores: [
      'node_modules/**',
    ],
  },
  js.configs.recommended,
  ...cgds,
  pluginCypress.configs.recommended,
  pluginCypress.configs.globals,
  {
    languageOptions: {
      sourceType: 'module',
      ecmaVersion: 2022,
      globals: {
        ...globals.node,
        ...globals.browser,
      },
    },
  },
];
