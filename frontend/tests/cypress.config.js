const { defineConfig } = require('cypress');

module.exports = defineConfig({
  reporter: 'cypress-mochawesome-reporter',
  videoCompression: false,
  reporterOptions: {
    charts: true,
    reportsPageTitle: 'Cypress Report',
    embededScreenshots: true,
    inlineAssets: true,
  },

  e2e: {
    setupNodeEvents(on, config) {
      require('cypress-mochawesome-reporter/plugin')(on);
    },
  },
});
