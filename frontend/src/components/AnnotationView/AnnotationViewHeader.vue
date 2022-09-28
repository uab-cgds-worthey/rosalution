<template>
  <Header :username="this.username" :titleText="this.titleText">
    <div>
      <h2>
        {{ genes[0] }}
      </h2>
      <font-awesome-icon v-if="variants.length > 0" icon="chevron-right" size="xl"/>
      <h2 v-if="variants.length > 0">
        {{ variants[0] }}
      </h2>
    </div>
  </Header>
</template>

<script>
import Header from '@/components/Header.vue';

export default {
  name: 'annotation-view-header-component',
  components: {
    Header,
  },
  props: {
    username: {
      type: String,
      default: undefined,
      required: false,
    },
    titleText: {
      type: String,
      required: true,
    },
    genes: {
      type: Array,
      required: true,
    },
    variants: {
      type: Array,
      required: false,
    },
  },
};
</script>

<style scoped>
div {
  flex: 1 1 auto;
  display: inline-flex;
  justify-content: space-between;
  margin-left: var(--p-8)
}

div h2 {
  margin: 0;
  flex: 2 1 auto;
}

svg {
  color: var(--rosalution-black);
  flex: 1 1 auto;
}
</style>
