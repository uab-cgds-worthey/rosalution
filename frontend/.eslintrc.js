module.exports = {
  root: true,
  env: {
    browser: true,
    node: true,
    es6: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:vue/vue3-essential',
    'google',
  ],
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'no-unused-labels': 'off',
    'max-len': [2, 120, 4],
    'no-invalid-this': 0,
  },
  ignorePatterns: [
    'node_modules/*',
    'dist/*',
  ],
  parserOptions: {
    'ecmaVersion': 2018,
    'sourceType': 'module',
  },
};
