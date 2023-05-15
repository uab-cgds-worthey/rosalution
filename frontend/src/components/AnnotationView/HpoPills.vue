<template>
  <div class="pills-container">
    <div class="pill" v-for="(item, index) in items" :key="index">
      {{ item }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'hpo-pills',
  props: {
    values: {
      type: String,
      required: true
    },
  },
  computed: {
    items() {
      return this.values.split('; ');
    }
  }
}
</script>

<style scoped>
.pills-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.pill {
  padding: 10px 15px;
  background-color: var(--rosalution-grey-100);
  color: var(--rosalution-white);
  border-radius: 20px;
}
</style>
