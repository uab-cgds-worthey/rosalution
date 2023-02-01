const {defineConfig} = require('cypress');

module.exports = defineConfig({
  e2e: {
    video: false,
    baseUrl: 'http://local.rosalution.cgds/rosalution',
    fixturesFolder: './fixtures',
    screenshotsFolder: 'cypress/screenshots',
    videosFolder: 'cypress/videos',
    specPattern: './e2e/**/*.cy.js',
    supportFile: './support/e2e.js',
    setupNodeEvents(on, config) {
    },
  },
});
