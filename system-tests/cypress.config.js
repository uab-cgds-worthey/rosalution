const {defineConfig} = require('cypress');

module.exports = defineConfig({
  e2e: {
    video: false,
    baseUrl: 'http://local.rosalution.cgds/rosalution',
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
});
