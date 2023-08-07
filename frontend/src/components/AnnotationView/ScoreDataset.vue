<template>
  <div class="dataset-container">
    <span class="dataset-label dataset-label-position" :style="{ color: dataAvailabilityColour }">
      {{ label }}
    </span>
    <span
      class="score-background"
      :style="{
        'background-color': scoreStyling.backgroundColour,
        'border-color': `2px solid ${scoreStyling.borderColour}`,
      }"
      data-test="score-background"
    >
      <span
        v-if="value"
        class="score-fill"
        :style="{
          'background-color': scoreStyling.fillColour,
          width: scoreFillWidthPercentage,
        }"
        data-test="score-fill"
      >
      </span>
    </span>
    <span class="score-text" :style="{ color: scoreStyling.textColour }" data-test="score-text">
      {{ value }}
    </span>
  </div>
</template>

<script>
export default {
  name: 'score-dataset',
  props: {
    label: {
      type: String,
    },
    value: {
      type: [Number, String],
    },
    minimum: {
      type: Number,
    },
    maximum: {
      type: Number,
    },
    bounds: {
      type: Object,
    },
    cutoff: {
      type: Number,
    },
  },
  data: function() {
    return {
      unavailableColours: {
        fillColour: '',
        backgroundColour: 'var(--rosalution-grey-100)',
        borderColour: '',
        textColour: 'var(--rosalution-grey-300)',
      },
      nominalColours: {
        fillColour: 'var(--rosalution-blue-200)',
        backgroundColour: 'var(--rosalution-blue-300)',
        borderColour: 'var(--rosalution-blue-100)',
        textColour: 'var(--rosalution-blue-300)',
      },
      closeToThresholdColours: {
        fillColour: 'var(--rosalution-yellow-200)',
        backgroundColour: 'var(--rosalution-yellow-300)',
        borderColour: 'var(--rosalution-yellow-100)',
        textColour: 'var(--rosalution-yellow-300)',
      },
      outOfThresholdColours: {
        fillColour: 'var(--rosalution-red-200)',
        backgroundColour: 'var(--rosalution-red-300)',
        borderColour: 'var(--rosalution-red-100)',
        textColour: 'var(--rosalution-red-300)',
      },
    };
  },
  computed: {
    unavailableData: function() {
      return this.value == '.' || this.value == 'null' || this.value == null;
    },
    scoreFillValue: function() {
      return (
        parseFloat(Math.abs(this.minimum) + this.value) /
        (Math.abs(this.minimum) + Math.abs(this.maximum))
      );
    },
    scoreFillWidthPercentage: function() {
      return Math.floor(Math.abs(this.scoreFillValue) * 100) + '%';
    },
    scoreStyling: function() {
      if (this.unavailableData) {
        return this.unavailableColours;
      }

      let score = 0;

      if (this.cutoff) {
        score = this.value / this.cutoff;
        if (this.withinBounds(score)) {
          return this.closeToThresholdColours;
        }
        if (this.belowBounds(score)) {
          return this.outOfThresholdColours;
        }
      }

      return this.nominalColours;
    },
    dataAvailabilityColour: function() {
      return this.unavailableData ?
        'var(--rosalution-grey-300)' :
        'var(--rosalution-black)';
    },
  },
  methods: {
    withinBounds: function(score) {
      return score > this.bounds.lowerBound && score < this.bounds.upperBound;
    },
    belowBounds: function(score) {
      return score > this.bounds.upperBound;
    },
  },
};
</script>

<style scoped>
.dataset-container {
  display: flex;
  padding: var(--p-1);
  align-items: center;
}

.dataset-label {
  flex: 0 0 110px;
  font-weight: 600;
}

.score-background {
  overflow: hidden;
  width: 10.75rem;
  height: 1rem;
  border-radius: 9999px;
  display: flex;
}

.score-fill {
  box-shadow: 0 0 #0000;
  border-radius: 9999px;
}

.score-text {
  padding-left: var(--p-1);
  font-size: 1rem;
  /* margin:auto; */
}
</style>
