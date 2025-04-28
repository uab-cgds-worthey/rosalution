<template>
  <div class="rosalution-section-container">
    <div class="rosalution-section-header">
      <h2 class="rosalution-section-header-text">{{ header }}</h2>
    </div>
    <div class="rosalution-section-seperator"></div>
    <div class="section-row">
      <div class="section-field">Client ID</div>
      <div class="section-content" data-test="client-id-value-row">{{clientId}}</div>
    </div>
    <div class="section-row">
      <div class="section-field">Client Secret</div>
      <div class="section-content">
        <a class="clickable-text section-text" @click="$emit('display-secret')" data-test="client-secret-value-row">
          {{ clientSecret }}
        </a>
        <button class="generate-button rosalution-button" @click="$emit('generate-secret')" type="submit">
          Generate Secret
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import {defineEmits} from 'vue';

defineProps({
  header: {
    type: String,
  },
  clientId: {
    type: String,
  },
  clientSecret: {
    type: String,
  },
  secretExists: {
    type: Boolean,
    default: false,
  },
});

defineEmits(['display-secret', 'generate-secret']);
</script>

<style scoped>
.section-row {
  display: flex;
  flex-direction: row;
  gap: var(--p-10);
  padding: var(--p-1);
}

.section-field {
  flex: 0 0 11.25rem;
  font-weight: 600;
}

.section-content {
  display: flex;
  flex-direction: row;
  flex: 1 0 0;
}

.section-text {
  flex: 1 0 0;
}

.generate-button {
  flex: 0 1 auto;
  font-size: 1rem;
  font-weight: bold;
  padding-top: var(--p-5);
  padding-bottom: var(--p-5);
}

.clickable-text {
  color: var(--rosalution-purple-300);
  cursor: pointer;
}
</style>
