<template>
  <transition @after-enter="this.onAfterEnter">
    <div v-if="toast.state.active" class="toast-container" :class="toast.state.type" data-test="toast-container">
        <span class="toast-message">
          <font-awesome-icon :icon="icon" size="lg"/>
          <span class="toast-type" data-test="toast-title-type">
            {{title}}
          </span>
          <span>
            {{ toast.state.message }}
          </span>
        </span>
        <font-awesome-icon
          class="close-icon"
          icon="xmark"
          size="xs"
          @click="toast.cancel()"
          data-test="toast-close-button"
        />
    </div>
  </transition>
</template>

<script>
import toast from '@/toast.js';

export default {
  name: 'toast-dialog',
  data() {
    return {
      toast,
    };
  },
  computed: {
    icon() {
      if (this.toast.state.type == 'info') {
        return ['far', 'circle-question'];
      } else if (this.toast.state.type == 'success') {
        return ['far', 'circle-check'];
      } else if (this.toast.state.type == 'error') {
        return ['far', 'circle-xmark'];
      }

      return ['far', 'circle-question'];
    },
    title() {
      if (this.toast.state.type == 'info') {
        return 'Info';
      } else if (this.toast.state.type == 'success') {
        return 'Success';
      } else if (this.toast.state.type == 'error') {
        return 'Error';
      }

      console.log("IS IT GETTING TO THE TITLE THAT DIDN'T PLASS?")
      return 'Info';
    },
  },
  methods: {
    onAfterEnter() {
      const closeAfterMiliseconds = 3000;
      setTimeout(() => {
        this.toast.cancel();
      }, closeAfterMiliseconds);
    },
  },
};
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
