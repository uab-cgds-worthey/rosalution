<template>
  <div v-if="dialog.state.active" class="modal-background">
    <div class="modal-container modal-notification-content">
      <h2 class="header" v-if="dialog.state.title"> {{ dialog.state.title }}</h2>
      <span class="message-content message">{{ dialog.state.message }}</span>
      <a
        v-if="dialog.state.type !== 'alert'"
        title="Cancel"
        class="actions cancel-content secondary-button cancel-button-sizing"
        @click="dialog.cancel()"
        data-test="cancel-button">
            {{ dialog.state.cancelText }}
      </a>
      <a
        title="Confirm"
        class="actions confirm-content primary-button confirm-button-sizing"
        @click="dialog.confirmation(userInput)"
        data-test="confirm-button">
        {{ dialog.state.confirmText }}
      </a>
    </div>
  </div>
</template>

<script>
import dialog from '@/notificationDialog.js';

export default {
  name: 'notification-dialog',
  data() {
    return {
      userInput: '',
      dialog,
    };
  },
};
</script>

<style scoped>
  .modal-container {
    padding: var(--p-16);
    min-width: 25rem;
    max-width: 35rem;
    min-height: auto;
  }

  .modal-notification-content {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: repeat(3, auto);
    justify-items: start;
    gap: var(--p-16);
    white-space: pre-wrap;
  }

  .header {
    grid-column: 1 / 3;
    grid-row: 1 / 2;
  }

  .message-content {
    grid-column: 1 / 3;
    grid-row: 2 / 3;
    min-height: 3rem;
  }

  .message {
    font-size: var(--p-16);
  }

  .actions {
    grid-row: 3 / 4;
    height: var(--p-28);
  }

  .cancel-content {
    grid-column: 1 / 2;
  }

  .confirm-content {
    grid-column: 2 / 3;
    justify-self: end;
    align-self: center;
  }

  .cancel-button-sizing {
    padding-top: 0;
    padding-bottom: 0;
  }

  /* TODO - Return to this when buttons in design system are revised */
  .confirm-button-sizing {
    border-color: var(--rosalution-black);
    box-sizing: border-box;
    border-radius: var(--button-border-radius);
    border-style: solid;
    border-color: var(--rosalution-purple-100);
    padding-top: 0;
    padding-bottom: 0;
  }


</style>
