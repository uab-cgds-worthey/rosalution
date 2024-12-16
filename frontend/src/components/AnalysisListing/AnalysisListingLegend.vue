<template>
  <div class="legend">
    <div v-for="status in workflow" :key="status" :data-test="status" class="status" @click="toggleFilter(status)">
      <font-awesome-icon :icon="StatusType[status].icon" size="lg"
        :style="{
          color: isFiltered(status)
            ? `var(${StatusType[status].color})`
            : 'var(--rosalution-grey-300)',
        }"
      />
      <p :style="{
        color: isFiltered(status)
          ? 'var(--rosalution-black)'
          : 'var(--rosalution-grey-300)',
      }" :data-test="status" >
        {{ status }}
      </p>
    </div>
  </div>
</template>

<script>
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';
import {StatusType} from '@/config.js';

export default {
  name: 'analysis-listing-legend',
  emits: ['filtered-changed'],
  components: {
    'font-awesome-icon': FontAwesomeIcon,
  },
  computed: {
    workflow: function() {
      return Object.keys(StatusType);
    },
  },
  data() {
    return {
      activeFilters: [],
      StatusType,
    };
  },
  methods: {
    toggleFilter(status) {
      const index = this.activeFilters.indexOf(status);

      if (index !== -1) {
        this.activeFilters.splice(index, 1);
      } else {
        this.activeFilters.push(status);
      }

      if (this.activeFilters.length === this.workflow.length) {
        this.activeFilters = [];
      }

      this.$emit('filtered-changed', this.activeFilters);
    },
    isFiltered(status) {
      return this.activeFilters.includes(status) || this.activeFilters.length === 0;
    },
  },
};
</script>

<style scoped>
.legend {
  display: flex;
  flex-grow: 0;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  gap: var(--p-10);
  border-radius: var(--content-border-radius);
  padding: var(--p-8);
  background-color: var(--secondary-background-color);
}

.status {
  display: flex;
  align-items: center;
  user-select: none;
  border-radius: var(--input-border-radius);
  padding: var(--p-05);
}

.status:hover {
  background-color: var(--primary-background-color);
}

.legend p {
  line-height: .245rem;
  padding-left: var(--p-10);
}
</style>
