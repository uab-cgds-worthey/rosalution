<template>
  <div v-if="dialog.state.active" class="modal-background">
      <div class="modal-container modal-remove-file-container">
          <h2 v-if="dialog.state.title"> {{ dialog.state.title }}</h2>
          <span>{{ dialog.state.message }}</span>

          <div class="cancel-button-column">
            <a
                v-if="dialog.state.type !== 'alert'"
                title="Cancel"
                class="cancel-button-item"
                @click="dialog.cancel()"
                data-test="cancel-button">
                    {{ dialog.state.cancelText }}
            </a>
          </div>
          <div class="confirm-button-column">
            <a
                title="Confirm"
                class="confirm-button-item"
                @click="dialog.confirmation(userInput)"
                data-test="confirm-button">
                {{ dialog.state.confirmText }}
            </a>
          </div>
      </div>
  </div>
</template>

<script>
import dialog from '@/dialog.js';

export default {
  name: 'the-dialog',
  data() {
    return {
      userInput: '',
      dialog,
    };
  },
};
</script>

<style scoped>
  .modal-remove-file-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    width: 400px;
    height: 170px;
    padding: 20px 35px 15px 35px;
  }

  h2 {
    display: flex;
    grid-column: 1 / 3;
    grid-row: 1;
    margin: 0px;
    align-items: center;
  }

  span {
    font-family: "Proxima Nova", sans-serif;
    font-size: 14px;
    grid-column: span 2 / 3;
    grid-row: 2;
  }

  .cancel-button-item {
    display: flex;
    grid-row: 3;
    text-decoration: none;
    font-size: 100%;
    font-weight: bold;
    line-height: 1.625rem;
    text-align: center;
    border-radius: 2rem;
    border-color: black;
    border-style: solid;
    justify-content: center;
    align-items: center;
    height: 25px;
    width: 100px;
    cursor: pointer;
  }

  .cancel-button-column {
    display: flex;
    justify-content: left;
    align-items: center;
  }

  .confirm-button-column {
    display: flex;
    justify-content: right;
    align-items: center;
    cursor: pointer;
  }

  .confirm-button-column {
    display: flex;
    justify-content: left;
    align-items: center;
  }

  .confirm-button-item {
    display: flex;
    grid-row: 3;
    background-color: var(--rosalution-purple-100);
    border-radius: 2rem;
    text-decoration: none;
    font-size: 100%;
    font-weight: bold;
    line-height: 1.625rem;
    text-align: center;
    justify-content: center;
    align-items: center;
    height: 30px;
    width: 100px;
  }

</style>
