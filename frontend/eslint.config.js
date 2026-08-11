import globals from 'globals';
import {defineConfig} from 'eslint/config';
import js from '@eslint/js';
import pluginVue from 'eslint-plugin-vue';
import cgds from './eslint-config-cgds.js';


export default defineConfig([
  {
    name: 'rosalution-frontend',
    plugins: {js},
    extends: [
      'js/recommended',
      cgds,
    ],
    ignores: [
      'node_modules/**',
      'dist/**',
      'test/__mocks__/**',
    ],
    languageOptions: {
      sourceType: 'module',
      ecmaVersion: 2022,
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
  },
  {
    name: 'rosalution-frontend/vue',
    extends: [
      pluginVue.configs['flat/essential'],
    ],
    rules: {
      'no-useless-assignment': 'off',
      'vue/prop-name-casing': 'off',
      'vue/require-default-prop': 'off',
      'vue/max-attributes-per-line': ['error', {
        'singleline': {
          'max': 6,
        },
        'multiline': {
          'max': 2,
        },
      }],
      // Disabling error temporarilly until team can reconvence and make a decision on us moving forward regarding
      // this configuration.
      'vue/html-self-closing': ['off', {
        'html': {
          'void': 'never',
          'normal': 'always',
          'component': 'always',
        },
        'svg': 'always',
        'math': 'always',
      }],
      // We inconsistently 2 space tab in SFC template section at the template base.
      // Will update in future update to set rule and make consistent in seperate PR
      // after team discussion.
      'vue/html-indent': ['off'],
      // 'vue/singleline-html-element-content-newline': ['error', {
      //   'ignoreWhenNoAttributes': true,
      //   'ignoreWhenEmpty': true,
      //   'ignores': ['pre', 'textarea', ...INLINE_ELEMENTS],
      //   'externalIgnores': []
      // }],
      //     'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'off',
      //     'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
      //   },
    },
  },
]);
