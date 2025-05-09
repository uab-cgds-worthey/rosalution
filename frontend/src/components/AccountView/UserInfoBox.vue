<template>
  <div class="rosalution-section-container">
    <div class="rosalution-section-header">
        <h2 class="rosalution-section-header-text">{{ header }}</h2>
    </div>
    <div class="rosalution-section-seperator"></div>
    <div class="section-row">
      <div class="section-field">Username</div><div class="section-content" data-test="username">{{ username }}</div>
    </div>
    <div class="section-row">
      <div class="section-field">Full Name</div><div class="section-content" data-test="full-name">{{ fullName }}</div>
    </div>
    <div class="section-row">
      <div class="section-field">Full Name</div><div class="section-content" data-test="email">{{ email }}</div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  header: {
    type: String,
  },
  username: {
    type: String,
  },
  fullName: {
    type: String,
  },
  email: {
    type: String,
  },
},
);
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
  flex-direction: column;
  flex: 1 0 0;
}

</style>
