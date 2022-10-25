<template>
  <div class="dataset-container">
    <span class="dataset-label" :style="{'color': labelTextColor}">{{ label }}:</span>
    <span class="highlight-text" :style="highlightStyle">{{ value }}</span>
  </div>
</template>

<script>
export default {
  name: 'text-highlight-dataset',
  props: {
    label: {
      type: String,
    },
    value: {
      type: String,
    },
    highlight: {
      type: Object,
      required: true,
    },
  },
  computed: {
    isDataUnavailable: function() {
      return this.value == '.' || this.value == 'null' || this.value == null;
    },
    labelTextColor: function() {
      return this.isDataUnavailable ? 'var(--rosalution-grey-300)' : 'var(--rosalution-black)';
    },
    highlightStyle() {
      const style = {
        'background-color': 'var(--rosalution-grey-300)',
      };

      if ( !(this.value in this.highlight) ) {
        return style;
      }

      const highlightColour = this.highlight[this.value];
      if (highlightColour === 'Red') {
        style['background-color'] = 'var(--rosalution-red-200)';
      } else if (highlightColour === 'Blue') {
        style['background-color'] = 'var(--rosalution-blue-200)';
      } else if (highlightColour === 'Yellow') {
        style['background-color'] = 'var(--rosalution-yellow-200)';
      } else if (highlightColour === 'Green') {
        style['background-color'] = 'var(--rosalution-green-200)';
      }
      return style;
    },
  },
};
</script>


<style scoped>
.dataset-container {
  display: flex;
  gap: var(--p-5);
  align-items: center;
}

.dataset-label {
  flex: 0 0 content;
  font-weight: 600;
}

.highlight-text {
  padding: 0 var(--p-8) 0 var(--p-8);
  border-radius: 9999px;
}

</style>
