<template>
  <div v-if="dialog.state.active" class="modal-background">
    <div :class="['modal-container', dialog.state.warningText ? 'limit-width' : '']">
      <div class="tab-header">
        <button
          v-for="(tab, index) in dialog.state.tabs"
          :key="`button-${tab.name}-${index}`"
          :class="tab.name == dialog.state.activeTabName ? 'tab-button-active' : ''"
          class="tab-button"
          @click="dialog.state.activeTabName = tab.name"
          :data-test="`button-${tab.name}`"
        >
          <img
            v-if="tab.icon == 'phenotips'"
            src="@/assets/phenotips-favicon-96x96.png"
          />
          <font-awesome-icon v-else
            :icon="'file' == tab.icon ? ['far', 'file'] : tab.icon"
            size="2xl">
          </font-awesome-icon>
        </button>
      </div>
      <div v-if="dialog.state.warningText"
        class="warning-message"
        v-html="dialog.state.warningText"
        data-test="warning-message">
      </div>
        <component v-bind:is="dialog.state.activeTabName"
          :userInput = "dialog.activeTab().input"
          v-bind="dialog.activeTab().props"
          @update:userInput="dialog.updateActiveTabInput"
        />
      <div class="button-row">
        <button class="secondary-button" @click="dialog.cancel()" data-test="cancel">
          {{ dialog.state.cancelText }}
        </button>
        <button class="secondary-button" v-if="dialog.state.deleteText!=''" @click="dialog.delete()" data-test="delete">
          {{ dialog.state.deleteText }}
        </button>
        <button class="primary-button" @click="dialog.confirmation(dialog.activeTab().input)" data-test="confirm">
          {{ dialog.state.confirmText }}
        </button>
      </div>
  </div>
  </div>
</template>

<script>
import InputDialogAttachUrl from '@/components/Dialogs/InputDialogAttachUrl.vue';
import InputDialogUploadFile from '@/components/Dialogs/InputDialogUploadFile.vue';

import dialog from '@/inputDialog.js';

export default {
  name: 'input-dialog',
  components: {
    InputDialogAttachUrl,
    InputDialogUploadFile,
  },
  data: function() {
    return {
      dialog,
    };
  },
};
</script>

<style scoped>

.modal-container {
  padding: var(--p-16);
  display: flex;
  flex-direction: column;
  min-width: 25rem;
  min-height: auto;
  gap: var(--p-16);
  align-items: stretch;
}

.tab-header {
  margin: auto;
  border: 2px var(--rosalution-grey-100) solid;
  border-radius: var(--input-border-radius);

  width: 160px;
  display: flex;
  justify-content: center;
}

.tab-button {
  width: 2.5rem;
  background-color: var(--rosalution-white);
  border: none;
  padding-top: var(--p-10);
  padding-bottom: var(--p-10);
}

.tab-header .tab-button:not(:first-child) {
  border-left: 2px var(--rosalution-grey-100) solid;
  padding-left: var(--p-8);
}

.tab-button-active {
  color: var(--rosalution-blue-200) !important;
}

.button-row {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: var(--p-16);
}

.warning-message{
  font-size: var(--font-size-16);
  font-weight: var(--font-weight-regular);
  line-height: var(--line-height-24);
  text-align: center;
}

.limit-width {
  max-width: 25rem;
}

</style>
