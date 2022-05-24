<template>
  <table class="section-box-container" @wheel.prevent @touchmove.prevent @scroll.prevent>
    <tbody>
      <tr class="section-header">
        <th colspan="2">
          <tr>
            <td>
              <h2 class="section-name">
                {{header}}
              </h2>
            </td>
            <td>
              <span class="logo-dropdown-edit" >
                <font-awesome-icon icon="chevron-down" size="lg"/>
              </span>
            </td>
            <div class="seperator"></div>
          </tr>
        </th>
      </tr>
      <div class="fields">
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
      </div>
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
  data: function() {
    return {
      fieldsList: [],
    };
  },
  created() {
  },
  methods: {
    dropDown() {
    },
  },
};
</script>

<style scoped>

div {
  font-family: "Proxima Nova", sans-serif;
  padding: 0%;
  display: inline-block;
}

.section-box-container {
  display: flex;
  flex-wrap: wrap;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  padding: 0.625rem;
  margin: 0.625rem;
  height: auto;
  width: 100%;
  gap: .625rem;
  border-radius: 1.25rem;
  background-color: var(--divergen-white);
}

.section-header {
  height: 1.75rem;
  /* gap: 66.5rem; */
  align-self: stretch;
  flex-grow: 0;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: flex-start;
}

.section-name {
  display: inline-block;
  white-space: nowrap;
  min-width: 3.4375rem;
  height: 1.75rem;
  margin: .125rem .125rem 0 .125rem;
}

.logo-dropdown-edit {
  width: 1.875rem;
  height: 1.875rem;
  flex-grow: 0;
  object-fit: contain;
  color: var(--divergen-grey-200);
  float: right;
}

.seperator {
  height: .125rem;
  align-self: stretch;
  flex-grow: 0;
  background-color: var(--divergen-grey-100);
  border: solid .0469rem var(--divergen-grey-100);
  width: 100%;
}

.field-value-row {
  height: auto;
  align-self: stretch;
  flex-grow: 1;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: flex-start;
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
  letter-spacing: .0112rem;
  text-align: left;
  color: var(--divergen-black);
}

.value {
  white-space:nowrap;
  height: auto;
  flex-grow: 1;
  font-size: 1.125rem;
  text-align: left;
  color: var(--divergen-black);
}

</style>
