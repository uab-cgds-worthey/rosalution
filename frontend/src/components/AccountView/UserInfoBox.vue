<template>
  <table class="user-info-box-container">
    <tbody>
      <tr class="user-info-header">
        <td class="user-info-header-content">
          <h2 class="user-info-name">
            {{ header }}
          </h2>
        </td>
      </tr>
      <div class="separator"></div>
      <tr class="field-value-row">
        <td>
          <label class="field">
            Username
          </label>
        </td>
        <td class="values">
          <tr class="value-row" data-test="username">
            {{ username }}
          </tr>
        </td>
      </tr>
      <tr class="field-value-row">
          <td>
            <label class="field">
              Full Name
            </label>
          </td>
          <td class="values">
            <tr class="value-row" data-test="full-name">
              {{ fullName }}
            </tr>
          </td>
        </tr>
      <tr class="field-value-row">
          <td>
            <label class="field">
              Email
            </label>
          </td>
          <td class="values">
            <tr class="value-row" data-test="email">
              {{ email }}
            </tr>
          </td>
        </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: 'user-info-box',
  props: {
    header: {
      type: String,
    },
    username: {
      type: String,
    },
    fullName: {
      type: String,
    },
    email: {
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

.user-info-box-container {
  display: flex;
  flex-direction: column;
  padding: var(--p-10);
  margin: var(--p-10);
  width: 100%;
  gap: var(--p-10);
  border-radius: 1.25rem;
  background-color: var(--rosalution-white);
}

.user-info-header {
  height: 1.75rem;
  display: flex;
}

.user-info-header-content {
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

</style>
