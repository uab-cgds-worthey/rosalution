import {defineConfig} from 'cypress';

export default defineConfig({
  e2e: {
    video: false,
    baseUrl: 'https://local.rosalution.cgds/rosalution',
    fixturesFolder: './fixtures',
    downloadsFolder: 'cypress/downloads',
    screenshotsFolder: 'cypress/screenshots',
    videosFolder: 'cypress/videos',
    specPattern: './e2e/**/*.cy.js',
    supportFile: './support/e2e.js',
    trashAssetsBeforeRuns: true,
    setupNodeEvents(on, config) {
    },
  },
});
