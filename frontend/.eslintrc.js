module.exports = {
    env: {
      node: true,
    },
    extends: [
      'eslint:recommended',
      'plugin:vue/vue3-recommended',
    ],
    rules: {
        'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'off',
        'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
        'max-len': [2, 120, 4],
        'babel/no-invalid-this': 1,
        'no-invalid-this': 0,
    },
    ignorePatterns: [
        'node_modules/*',
        'dist/*',
      ],
  }