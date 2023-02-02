<template>
  <RosalutionHeader
    :username="this.username"
    :titleText="this.analysisName"
    :titleToRoute="{ name: 'analysis', params: { analysis_name: this.analysisName } }"
  >
    <div class="annotations-select">
        <AnnotationViewHeaderFormSelect
          v-model:selected="selectedGene"
          :options="Object.keys(this.genes)"
          class="gene-unit-select"
        >
        </AnnotationViewHeaderFormSelect>
      <font-awesome-icon icon="chevron-right" size="lg"/>
        <AnnotationViewHeaderFormSelect
          v-model:selected="selectedVariant"
          :options="this.variants"
          class="variant-unit-select"
        >
        </AnnotationViewHeaderFormSelect>
    </div>
  </RosalutionHeader>
</template>

<script>
import RosalutionHeader from '@/components/RosalutionHeader.vue';
import AnnotationViewHeaderFormSelect from '@/components/AnnotationView/AnnotationViewHeaderFormSelect.vue';

export default {
  name: 'annotation-view-header-component',
  emits: ['changed'],
  components: {
    RosalutionHeader,
    AnnotationViewHeaderFormSelect,
  },
  props: {
    username: {
      type: String,
      default: undefined,
      required: false,
    },
    analysisName: {
      type: String,
      required: true,
    },
    genes: {
      type: Object,
      required: true,
    },
    variants: {
      type: Array,
      required: false,
    },
    activeGenomicUnits: {
      type: Object,
      required: true,
    },
  },
  computed: {
    selectedGene: {
      get() {
        return this.activeGenomicUnits['gene'];
      },
      set(newValue) {
        if (this.activeGenomicUnits.gene == newValue) {
          return;
        }

        const newActive = this.activeGenomicUnits;
        newActive.gene = newValue;

        if (this.genes[newActive.gene].length > 0) {
          newActive.variant = this.genes[newActive.gene][0];
        }

        this.$emit('changed', newActive);
      },
    },
    selectedVariant: {
      get() {
        return this.activeGenomicUnits['variant'];
      },
      set(newValue) {
        if (this.activeGenomicUnits.variant == newValue) {
          return;
        }

        const newActive = this.activeGenomicUnits;
        newActive.variant = newValue;

        if (!this.genes[this.activeGenomicUnits.gene].includes(newActive.variant)) {
          newActive.gene = Object.keys(this.genes).find((gene) => this.genes[gene].includes(newActive.variant));
        }

        this.$emit('changed', newActive);
      },
    },
  },
};
</script>

<style scoped>
.annotations-select {
  flex: 1 1 auto;
  display: inline-flex;
  align-items: center;
  margin-left: var(--p-8);
  gap: var(--p-10);
}

.gene-unit-select {
  flex: 1 1 auto;
}

.variant-unit-select {
  flex: 2 1 auto;
}

svg {
  color: var(--rosalution-black);
  flex: 0 1 auto;
}
</style>
