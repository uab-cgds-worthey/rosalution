module.exports = {
    env: {
      node: true,
    },
    extends: [
      'eslint:recommended',
      'plugin:vue/vue3-essential',
      'google'
    ],
    rules: {
        'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'off',
        'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
        'max-len': [2, 120, 4],
        'no-invalid-this': 0,
        'vue/multi-word-component-names': 'off'
    },
    ignorePatterns: [
        'node_modules/*',
        'dist/*',
      ],
  }