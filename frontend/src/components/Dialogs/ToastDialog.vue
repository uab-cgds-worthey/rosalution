<template>
  <transition @after-enter="onAfterEnter()">
    <div v-if="state.active" class="toast-container" :class="state.type" data-test="toast-container">
      <span class="toast-message">
        <font-awesome-icon :icon="icon" size="lg"/>
        <span class="toast-type" data-test="toast-title-type">
          {{title}}
        </span>
        <span>
          {{ state.message }}
        </span>
      </span>
      <font-awesome-icon
        class="close-icon"
        icon="xmark"
        size="xs"
        @click="cancel()"
        data-test="toast-close-button"
      />
    </div>
  </transition>
</template>

<script setup>
import {computed, reactive} from 'vue';

const state = reactive({
  type: 'info',
  active: false,
  message: '',
});

// -----------------------------------
// Private Methods
// -----------------------------------
let close;

const dialogPromise = () => new Promise((resolve) => (close = resolve));

const open = (message) => {
  state.message = message;
  state.active = true;

  return dialogPromise();
};

const reset = () => {
  state.active = false;
  state.message = '';
  state.type = 'info';
};

// -----------------------------------
// Public Methods
// -----------------------------------

/**
 * Opens a 'success' toast with a message
 * @param {String} message text content of the toast
 * @return {Promise} returns a Promise that resolves when the toast closes
 */
function success(message) {
  state.type = 'success';
  return open(message);
}

/**
 * Opens an 'information' toast with a message
 * @param {String} message text content of the toast
 * @return {Promise} returns a Promise that resolves when the toast closes
 */
function info(message) {
  state.type = 'info';
  return open(message);
}

/**
 * Opens an 'error' toast with a message
 * @param {String} message text content of the toast
 * @return {Promise} returns a Promise that resolves when the toast closes
 */
function error(message) {
  state.type = 'error';
  return open(message);
}

/**
 * Closes the toast and resets the content
 */
function cancel() {
  close();
  reset();
}

defineExpose({
  success,
  info,
  error,
  cancel,
});

const icon = computed(() => {
  if (state.type == 'info') {
    return ['far', 'circle-question'];
  } else if (state.type == 'success') {
    return ['far', 'circle-check'];
  } else if (state.type == 'error') {
    return ['far', 'circle-xmark'];
  }
  return ['far', 'circle-question'];
});

const title = computed(() => {
  if (state.type == 'info') {
    return 'Info';
  } else if (state.type == 'success') {
    return 'Success';
  } else if (state.type == 'error') {
    return 'Error';
  }

  return 'Info';
});

/**
 * A JavaScript transition hook to progamatically close the toast after 3 seconds.
 */
function onAfterEnter() {
  const closeAfterMiliseconds = 3000;
  setTimeout(() => {
    cancel();
  }, closeAfterMiliseconds);
}

</script>

<style scoped>
  .toast-container {
    border-radius: var(--button-border-radius);
    padding: var(--p-5) var(--p-10) var(--p-5) var(--p-10);

    position: fixed;
    top: 5%;
    left: 50%;
    width: 90%;
    transform: translate(-50%, -50%);
    z-index: var(--modal-container-z-index);

    display: flex;
    justify-content: space-between;
    align-items: center;

    font-size: 1rem; /* 16px */
  }

  .toast-message {
    display: flex;
    gap: var(--p-16);
    align-items: center;
  }

  .toast-type {
    font-weight: 700;
  }

  .info {
    border: 1px solid var(--rosalution-orange-300);
    background-color: var(--cgds-yellow-100);
    color: var(--rosalution-orange-300);
  }

  .success {
    border: 1px solid var(--rosalution-purple-300);
    background-color: var(--rosalution-purple-100);
    color: var(--rosalution-purple-300);
  }

  .error {
    border: 1px solid var(--rosalution-red-300);
    background-color: var(--cgds-red-100);
    color: var(--rosalution-red-300);
  }

  .close-icon {
    cursor: pointer;
    padding: var(--p-5);
  }

  .v-enter-active,
  .v-leave-active {
    transition: all 0.25s ease;
  }

  .v-enter-from {
    top: 0;
    opacity: 0;
  }

  .v-leave-to {
    opacity: 0;
  }
</style>
