<template>
  <div class="dataset-container">
    <span class="dataset-label" :style="{'color': labelTextColor}">{{ label }}</span>
    <div class="set-section">
      <div v-if="!value || availableData"
        class="set-background set-fill-unavailable set-fill"
        data-test="set-unavailable">
      </div>
      <div v-else class="set-background set-text set-fill" data-test="set-fill">
        <span v-for="(item, index) in set"
          :key="`${item.value}-${index}`"
          :style="this.setItemStyle(item)"
        >
          {{ classificationText(item) }}
        </span>
    </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'set-dataset',
  props: {
    label: {
      type: String,
    },
    value: {
      type: String,
    },
    set: {
      type: Array,
      default: () => {
        return [];
      },
    },
    ticker: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    availableData: function() {
      return this.value == '.' || this.value == 'null' || this.value == null;
    },
    labelTextColor: function() {
      return this.availableData ? 'var(--rosalution-grey-300)' : 'var(--rosalution-black)';
    },
  },
  methods: {
    setItemStyle(item) {
      const style = {
        'background-color': 'var(--rosalution-grey-300)',
        'opacity': 1,
      };


      if (item.colour == 'Red') {
        style['background-color'] = 'var(--rosalution-red-200)';
      } else if (item.colour == 'Blue') {
        style['background-color'] = 'var(--rosalution-blue-200)';
      } else if (item.colour == 'Yellow') {
        style['background-color'] = 'var(--rosalution-yellow-200)';
      } else if (item.colour == 'Green') {
        style['background-color'] = 'var(--rosalution-green-200)';
      }

      style['width'] = this.calculateWidth(item.value);

      return (item.value == this.value) ? style : {...style, 'opacity': 0.5};
    },

    calculateWidth(value) {
      const width = 100;

      if (value == this.value) {
        return `${width * .75}%`;
      }
      return `${ (width / this.set.length) / 2}%`;
    },
    classificationText(setItem) {
      return (setItem.value == this.value) ? setItem.classification : '';
    },
  },
};
</script>


<style scoped>
.dataset-container {
  flex: 4 1 auto;
  display: flex;
  align-items: center;
}

.dataset-label {
  flex: 0 0 110px;
  font-weight: 600;
}

.set-section {
  flex: 1 0 content;
}

.set-background {
  overflow: hidden;
  width: 12.5rem;
  border-radius: 9999px;
}

.set-fill-unavailable {
  background-color: var(--rosalution-grey-100);
  height: 1rem;
}

.set-fill {
  display:flex
}

.set-text {
  font-size: 0.75rem; /* 12px */
  line-height: 1rem; /* 16px */
  white-space: nowrap;
  text-align: center;
  color: var(--rosalution-white);
}

</style>
