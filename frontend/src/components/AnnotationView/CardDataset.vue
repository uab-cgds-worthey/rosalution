<template>
  <div class="model-cards">
    <!-- TODO: This is intended to become a <slot> to allow any card type to be used here -->
    <AllianceGenomeCard
      v-for="(model) in this.models"
      :key="model.id"
      :model="model"
    />
  </div>
</template>

<script>
import AllianceGenomeCard from '@/components/AnnotationView/AllianceGenomeCard.vue';

export default {
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
  },
  computed: {
    models() {
      return this.value;
    },
  },
};
</script>

<style>

.model-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

</style>
