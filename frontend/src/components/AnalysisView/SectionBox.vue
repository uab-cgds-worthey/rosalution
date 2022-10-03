<template>
  <table class="section-box-container">
    <tbody>
      <input type="checkbox" v-bind:id="section_toggle"/>
      <tr class="section-header">
        <td>
          <h2 class="section-name">
            {{header}}
          </h2>
        </td>
        <label class="logo-dropdown-edit" v-bind:for="section_toggle">
          <font-awesome-icon icon="chevron-down" size="lg"/>
        </label>
      </tr>
      <div class="seperator"></div>
      <tr class="field-value-row" v-for="content in contentList" :key="content">
        <td>
          <label class="field">
            {{content.field}}
          </label>
        </td>
        <td class="value">
          <tr v-for="value in content.value" :key="value">
              {{value}}
          </tr>
        </td>
      </tr>

    </tbody>
  </table>
</template>

<script>
export default {
  name: 'section-box',
  components: {
  },
  props: {
    analysis_name: {
      type: String,
    },
    header: {
      type: String,
    },
    contentList: {
      type: Array,
    },
  },
  data() {
    return {
      section_toggle: this.header.toLowerCase() + '_collapse',
    };
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
  cursor: pointer;
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

input[type="checkbox"] {
  display: none;
}


.section-box-container input[type="checkbox"]:checked ~ .field-value-row {
  display: none;
}

input[type="checkbox"]:checked ~ tr > .logo-dropdown-edit {
  transform: scaleY(-1);
}

</style>
