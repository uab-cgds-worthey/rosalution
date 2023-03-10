<template>
  <table class="credentials-box-container">
    <tbody>
      <tr class="credentials-header">
        <td class="credentials-header-content">
          <h2 class="credentials-name">
            {{header}}
          </h2>
        </td>
      </tr>
      <div class="separator"></div>
      <tr class="field-value-row" v-for="content in contentList" :key="content">
        <td>
          <lable class="field"
          v-bind:style="[content.value.length === 0 && !this.edit ? 'color: var(--rosalution-grey-300);'
          : 'color: var(--rosalution-black);']">
            {{content.field}}
          </lable>
        </td>
        <td class="values">
          <tr v-for="value in content.value" :key="value" class="value-row" data-test="value-row">
            <a v-if="content.clickable" @click="toggle()">{{value}}</a>
            <span v-else>
              {{value}}
            </span>
          </tr>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: 'credentials-box',
  emits: ['toggle'],
  props: {
    header: {
      type: String,
    },
    content: {
      type: Array,
    },
  },
  data() {
    return {
      contentList: this.content,
    };
  },
  methods: {
    toggle() {
      this.$emit('toggle');
    },
  },
};
</script>

<style scoped>
div {
  font-family: "Proxima Nova", sans-serif;
  padding: var(--p-0);
}
.credentials-box-container {
  display: flex;
  flex-direction: column;
  padding: var(--p-10);
  margin: var(--p-10);
  width: 100%;
  gap: var(--p-10);
  border-radius: 1.25rem;
  background-color: var(--rosalution-white);
}

.credentials-header {
  height: 1.75rem;
  display: flex;
}

.credentials-header-content {
  display: flex;
  align-items: center;
  flex: 1 0 auto;
}

.separator {
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
}

.values {
  font-size: 1.125rem;
  text-align: left;
  color: var(--rosalution-black);
  width: 100%;
  display: block;
}
</style>
