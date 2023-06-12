<template>
  <div class="legend">
    <!-- Annotating -->
    <div class="status" @click="toggleFilter('annotating')">
      <font-awesome-icon icon="asterisk" size="lg" :style="{
        color: isFiltered('annotating')
          ? 'var(--rosalution-grey-300)'
          : 'var(--rosalution-status-annotation)'
      }" />
      <p :style="{ color: isFiltered('annotating') ? 'var(--rosalution-grey-300)' : '' }">Annotating</p>
    </div>

    <!-- Ready -->
    <div class="status" @click="toggleFilter('ready')">
      <font-awesome-icon icon="clipboard-check" size="lg" :style="{
        color: isFiltered('ready')
          ? 'var(--rosalution-grey-300)'
          : 'var(--rosalution-status-ready)'
      }" />
      <p :style="{ color: isFiltered('ready') ? 'var(--rosalution-grey-300)' : '' }">Ready</p>
    </div>

    <!-- Active -->
    <div class="status" @click="toggleFilter('active')">
      <font-awesome-icon icon="book-open" size="lg" :style="{
        color: isFiltered('active')
          ? 'var(--rosalution-grey-300)'
          : 'var(--rosalution-status-active)'
      }" />
      <p :style="{ color: isFiltered('active') ? 'var(--rosalution-grey-300)' : '' }">Active</p>
    </div>

    <!-- On Hold -->
    <div class="status" @click="toggleFilter('onHold')">
      <font-awesome-icon icon="pause" size="lg" :style="{
        color: isFiltered('onHold')
          ? 'var(--rosalution-grey-300)'
          : 'var(--rosalution-status-on-hold)'
      }" />
      <p :style="{ color: isFiltered('onHold') ? 'var(--rosalution-grey-300)' : '' }">On Hold</p>
    </div>

    <!-- Approved -->
    <div class="status" @click="toggleFilter('approved')">
      <font-awesome-icon icon="check" size="lg" :style="{
        color: isFiltered('approved')
          ? 'var(--rosalution-grey-300)'
          : 'var(--rosalution-status-approved)'
      }" />
      <p :style="{ color: isFiltered('approved') ? 'var(--rosalution-grey-300)' : '' }">Approved</p>
    </div>

    <!-- Declined -->
    <div class="status" @click="toggleFilter('declined')">
      <font-awesome-icon icon="x" size="lg" :style="{
        color: isFiltered('declined')
          ? 'var(--rosalution-grey-300)'
          : 'var(--rosalution-status-declined)'
      }" />
      <p :style="{ color: isFiltered('declined') ? 'var(--rosalution-grey-300)' : '' }">Declined</p>
    </div>
  </div>
</template>

<script>
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

export default {
  name: 'analysis-listing-legend',
  emits: ['filtered-statuses'],
  components: {
    'font-awesome-icon': FontAwesomeIcon,
  },
  data() {
    return {
      filteredStatuses: [],
    };
  },
  methods: {
    toggleFilter(status) {
      if (this.isFiltered(status)) {
        // If the status is already filtered, remove it from the array
        const index = this.filteredStatuses.indexOf(status);
        if (index !== -1) {
          this.filteredStatuses.splice(index, 1);
        }
      } else {
        // If the status is not filtered, add it to the array
        this.filteredStatuses.push(status);
      }
      // Emit the filtered statuses
      this.$emit('filtered-statuses', this.filteredStatuses);
    },
    isFiltered(status) {
      // A status is filtered if it's in the array
      return this.filteredStatuses.includes(status);
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
