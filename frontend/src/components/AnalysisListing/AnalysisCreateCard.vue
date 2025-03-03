<template>
  <button class="analysis-card card-content"  data-test="create-analysis-button">
    <span>Create New Analysis</span>
    <div class="icon-section">
      <font-awesome-icon icon="plus" size="8x"></font-awesome-icon>
    </div>
  </button>
</template>

<script>

export default {
  name: 'analysis-create-card',
};
</script>

<style scoped>

.icon-section {
  flex-grow: 1;

  display: flex;
  align-items: center;
  justify-content: center;
}

.analysis-card.card-content {
  display: flex;
  flex-direction: column;

  border-color: var(--rosalution-grey-300);
}

.analysis-card.card-content > * {
  color: var(--rosalution-grey-300);
}
</style>
