<template>
  <button class="analysis-base card-content"  data-test="create-analysis-button">
    <span>Create New Analysis</span>
    <div class="create-card-content">
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

.create-card-content {
  flex-grow: 1;

  display: flex;
  align-items: center;
  justify-content: center;
}

.analysis-base.card-content {
  display: flex;
  flex-direction: column;

  border-color: var(--rosalution-grey-300);
}

.analysis-base.card-content > * {
  color: var(--rosalution-grey-300);
}
</style>
