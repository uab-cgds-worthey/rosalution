<template>
  <div class="legend">
    <div v-for="status in statuses" :key="status.name" class="status" @click="toggleFilter(status.name)">
      <font-awesome-icon :icon="status.icon" size="lg" :style="{
        color: isFiltered(status.name)
          ? `var(--rosalution-status-${status.name})`
          : 'var(--rosalution-grey-300)',
      }" />
      <p :style="{
        color: isFiltered(status.name)
          ? ''
          : 'var(--rosalution-grey-300)',
      }">
        {{ status.displayName }}
      </p>
    </div>
  </div>
</template>

<script>
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

export default {
  name: 'analysis-listing-legend',
  emits: ['filtered-changed'],
  components: {
    'font-awesome-icon': FontAwesomeIcon,
  },
  data() {
    return {
      activeFilters: [],
      statuses: [
        {name: 'annotation', displayName: 'Preparation', icon: 'asterisk'},
        {name: 'ready', displayName: 'Ready', icon: 'clipboard-check'},
        {name: 'active', displayName: 'Active', icon: 'book-open'},
        {name: 'on-hold', displayName: 'On Hold', icon: 'pause'},
        {name: 'approved', displayName: 'Approved', icon: 'check'},
        {name: 'declined', displayName: 'Declined', icon: 'times'},
      ],
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

      if (this.activeFilters.length === this.statuses.length) {
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
}

.legend p {
  line-height: .245rem;
  padding-left: var(--p-10);
}
</style>
