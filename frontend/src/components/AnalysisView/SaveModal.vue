<template>
  <table class="save-modal-container">
    <tbody>
      <tr class="save-modal-btn-row">
        <td class="cancel-btn-container">
          <button class="cancel-btn" @click="$emit('cancelEdit')">
            Cancel
          </button>
        </td>
        <td class="save-btn-container">
          <button class="save-btn" @click="this.saveAnalysis()">
            Save
          </button>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: 'save-modal',
  components: {
  },
  methods: {
    saveAnalysis() {
      console.log('Analysis is Saved!');
    },
  },
};
</script>

<style>

div {
  font-family: "Proxima Nova", sans-serif;
  padding: var(--p-0);
}

.save-modal-container {
  display: flex;
  flex-direction: column;
  padding: var(--p-1);
  margin: 0.625rem;
  width: 100%;
  height: fit-content;
  border-radius: 1.25rem;
  background-color: var(--rosalution-white);
  justify-content: center;
}

.save-modal-btn-row {
  display: flex;
  flex-direction: row;
}

.save-btn-container {
  padding-top: var(--p-1);
  padding-bottom: var(--p-1);
  padding-left: var(--p-1);
  padding-right: 45%;
  line-height: 1.75rem;
  text-align: center;
  vertical-align: middle;
}

.save-btn {
  background-color: var(--rosalution-purple-100);
  border: none;
  border-radius: .625rem;
  text-decoration: none;
  font-size: 1rem;
  font-weight: bold;
  line-height: 1.625rem;
  height: 2rem;
  width: 5rem;
  text-align: center;
  justify-self: stretch;
  cursor: pointer;
  vertical-align: middle;
}

.cancel-btn-container {
  padding-top: var(--p-1);
  padding-bottom: var(--p-1);
  padding-left: 45%;
  padding-right: var(--p-1);
  height: 1.75rem;
  text-align: center;
  vertical-align: middle;
}

.cancel-btn {
  background-color: var(--rosalution-purple-100);
  border: none;
  border-radius: .625rem;
  text-decoration: none;
  font-size: 1rem;
  line-height: 1.625rem;
  height: 2rem;
  width: 5rem;
  text-align: center;
  justify-self: stretch;
  cursor: pointer;
  vertical-align: middle;
}

</style>
