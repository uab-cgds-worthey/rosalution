<template>
    <div class="analysis-create-card">
        <button @click="createAnalysisClicked" data-test="create-analysis-button">
          <div class="analysis-base" :style="cardBorderColorStyle">
              <span style="margin-top: 1rem">Create New Analysis</span>
              <font-awesome-icon icon="plus" size="8x" class="create-card-icon"></font-awesome-icon>
          </div>
        </button>
    </div>
  </template>

<script>

export default {
  name: 'analysis-create-card',
  computed: {
    cardBorderColorStyle: function() {
      return {
        'border-color': `var(--rosalution-grey-300)`,
        'color': `var(--rosalution-grey-300)`,
      };
    },
  },
  methods: {
    createAnalysisClicked() {
      // This is where we'll open a modal for uploading a file to create a analysis
      console.log('Opening create analysis modal...');
    },
  },
};
</script>

  <style scoped>

  div {
    font-family: "Proxima Nova", sans-serif;
    font-size: 0.75rem; /* 12 px */
    font-weight: bold;
    color: var(--rosalution-black)
  }

  button {
    border:none;
    background: none;
  }

  .analysis-create-card {
    position: relative;
    text-decoration: none;
  }

  .analysis-base:hover {
    box-shadow: 0 0.5em 0.5em -0.4em;
    transform: translateY(-0.4em);
  }

  .analysis-base:active {
    transform: translateY(0em);
    transition: all .1s ease-in-out;
  }

  .analysis-base {
    width: 11.25rem;
    height: 18.125rem;
    padding: var(--p-8) var(--p-5) var(--p-8) var(--p-5);
    border-radius: 1.25rem;
    border: solid 0.625rem;
    background-color: var(--rosalution-white);
    display: block;
    box-sizing: border-box;
    color: inherit;
    transition: all .2s ease-in-out;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .create-card-icon {
    position: relative;
    top: 20%;
  }
  </style>
