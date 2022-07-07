const { defineConfig } = require("cypress");

module.exports = defineConfig({
  e2e: {
    video: false,
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
});
