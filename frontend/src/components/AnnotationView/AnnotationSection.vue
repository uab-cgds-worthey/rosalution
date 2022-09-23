<template>
  <table class="section-box-container">
    <tbody>
      <tr class="section-header">
        <td>
          <h2 class="section-name">
            {{header}}
          </h2>
        </td>
        <td class="logo-dropdown-edit">
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

div {
  font-family: "Proxima Nova", sans-serif;
  padding: var(--p-0);
}

.section-box-container {
  display: flex;
  flex-direction: column;
  padding: var(--p-10);
  margin: 0.625rem;
  width: 100%;
  gap: .625rem;
  border-radius: 1.25rem;
  background-color: var(--rosalution-white);
}

.section-header {
  height: 1.75rem;
  display: flex;
  flex-direction: row;
}

.section-name {
  height: 1.75rem;
  margin: .125rem .125rem 0 .125rem;
}

.logo-dropdown-edit {
  color: var(--rosalution-grey-200);
  float: right;
  right: 3%;
  position: absolute;
}

.seperator {
  height: .125rem;
  background-color: var(--rosalution-grey-100);
  border: solid .0469rem var(--rosalution-grey-100);
}

.field-value-row {
  display: flex;
  flex-direction: row;
  gap: .625rem;
  margin: 0.625rem 0.250rem 0.625rem 0.250rem;
}

.field {
  display: inline-block;
  width: 11.25rem;
  height: 1.375rem;
  margin: 0 1.1875rem .0063rem 0;
  font-size: 1.125rem;
  font-weight: 600;
  text-align: left;
  color: var(--rosalution-black);
}

.value {
  font-size: 1.125rem;
  text-align: left;
  color: var(--rosalution-black);
}

</style>
