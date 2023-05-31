<template>
    <div class="model-cards">
      <AllianceGenomeCard
        v-for="(model) in this.models"
        :key="model.id"
        :model="model"
      />
    </div>
</template>

<script>
import AllianceGenomeCard from '@/components/AnnotationView/AllianceGenomeCard.vue';

export default ({
  name: 'CardDataset',
  components: {
    AllianceGenomeCard,
  },
  props: {
    value: {
      type: Array,
      default() {
        return [];
      },
    },
    dataSet: {
      type: String,
    },
  },
  computed: {
    models() {
      return this.value;
    },
  },
});
</script>

<style>

.model-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  padding: 1rem;
  height: 100%;
}

</style>
