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
      <tr class="field-value-row">
        <td>
          <label class="field">
            Client ID
          </label>
        </td>
        <td class="values">
          <tr class="value-row" data-test="client-id-value-row">
            {{clientId}}
          </tr>
        </td>
      </tr>
      <tr class="field-value-row">
        <td>
          <label class="field">
            Client Secret
          </label>
        </td>
        <td class="values">
          <tr class="value-row" data-test="client-secret-value-row">
            <a class="clickable-text" @click="displaySecret()">{{clientSecret}}</a>
          </tr>
        </td>
        <td>
          <button class="button" @click="generateSecret" type="submit">
            Generate Secret
          </button>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: 'credentials-box',
  emits: ['display-secret', 'generate-secret'],
  props: {
    header: {
      type: String,
    },
    clientId: {
      type: String,
    },
    clientSecret: {
      type: String,
    },
    secretExists: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      contentList: this.content,
    };
  },
  methods: {
    displaySecret() {
      this.$emit('display-secret');
    },
    generateSecret() {
      this.$emit('generate-secret');
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

.value-row {
  font-size: 1.125rem;
  color: var(--rosalution-black);
  display: block;
  width: 100%;
}

.button {
  background-color: var(--rosalution-purple-100);
  color: var(--rosalution-purple-300);
  border: none;
  border-radius: .625rem;
  text-decoration: none;
  font-size: 1rem;
  font-weight: bold;
  line-height: 1.625rem;
  height: 2rem;
  width: 9rem;
  text-align: center;
  justify-self: stretch;
  cursor: pointer;
  vertical-align: middle;
}

.clickable-text {
  color: var(--rosalution-purple-300);
  cursor: pointer;
}
</style>
