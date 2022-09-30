<template>
  <table class="section-box-container">
    <tbody>
      <tr class="section-header">
        <td>
          <h2 class="section-name">
            {{header}}
          </h2>
        </td>
        <td class="annotations">
          <slot name="headerDatasets"></slot>
        </td>
        <td class="collapsable-icon">
          <font-awesome-icon icon="chevron-down" size="lg"/>
        </td>
      </tr>
      <div class="seperator"></div>
      <slot></slot>
    </tbody>
  </table>
</template>

<script>
export default {
  name: 'annotation-section',
  components: {
  },
  props: {
    header: {
      type: String,
    },
  },
};
</script>

<style scoped>
table {
  width:100%;
}

.section-box-container {
  display: flex;
  flex-direction: column;
  padding: var(--p-10);
  margin: var(--p-10);
  gap: var(--p-10);
  border-radius: var(--content-border-radius);
  background-color: var(--rosalution-white);
}

.section-header {
  height: 2rem;
  display: flex;
}

.section-name {
  margin: var(--p-1) var(--p-1) 0 var(--p-1);
}

.annotations {
  flex-grow: 2;
  justify-content: flex-start;
}

.collapsable-icon {
  color: var(--rosalution-grey-200);
}

.seperator {
  height: .125rem;
  background-color: var(--rosalution-grey-100);
  border: solid .0469rem var(--rosalution-grey-100);
}


</style>
