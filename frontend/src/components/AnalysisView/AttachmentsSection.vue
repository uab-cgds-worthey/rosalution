<template>
  <div class="rosalution-section-container">
    <input type="checkbox" id="attachments_toggle"/>
    <div class="rosalution-section-header">
      <h2 class="rosalution-section-header-text">Attachments</h2>
      <button class="icon-button" @click="$emit('openModal')" data-test="add-button">
        <font-awesome-icon icon="circle-plus" size="xl"/>
      </button>
      <span class="rosalution-section-center"></span>
      <label class="collapsable-icon" for="attachments_toggle">
        <font-awesome-icon icon="chevron-down" size="lg"/>
      </label>
    </div>
    <div class="rosalution-section-seperator"></div>
    <div class="attachment-list" v-for="attachment in attachments" v-bind:key="attachment.attachment_id">
      <div class="attachment-icon">
        <font-awesome-icon :icon="['far', 'file']" size="lg" v-if="attachment.type==='file'"/>
        <font-awesome-icon icon="link" size="lg" v-else-if="attachment.type==='link'"/>
      </div>
      <div class="attachment-content">
        <div class="attachment-name">
          <div v-if="attachment.type=='file'" @click="$emit('download', attachment)"
            target="_blank" rel="noreferrer noopener">
            {{ attachment.name }}
        </div>
          <a v-if="attachment.type=='link'" :href="attachment.data" target="_blank" rel="noreferrer noopener">
            {{ attachment.name }}
          </a>
        </div>
        <div class="attachment-comments">
          {{ attachment.comments }}
        </div>
      </div>
      <div>
        <button @click="$emit('edit', attachment)" class="icon-button attachment-action" data-test="edit-button">
          <font-awesome-icon icon="pencil" size="xl"/>
        </button>
        <button v-if="writePermissions" @click="$emit('delete', attachment)" class="icon-button attachment-action" data-test="delete-button">
          <font-awesome-icon icon="xmark" size="xl"/>
        </button>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'attachment-section',
  props: {
    attachments: {
      type: Array,
      default: () => {
        return [];
      },
    },
    writePermissions: {
      type: Boolean,
      default: false,
    },
  },
};
</script>

<style scoped>

input[type="checkbox"] {
  display: none;
}

.attachment-list {
  display: flex;
  align-items: center;
  gap: var(--p-5);
  padding: var(--p-5);
}

.attachment-list:nth-child(even) {
  background-color: var(--rosalution-grey-50);
}

.attachment-list:nth-child(odd) {
  background-color: var(--rosalution-grey-100);
}

.attachment-icon {
  width: 3rem;
}

.attachment-content {
  flex-grow: 1;
}

.attachment-name {
  font-weight: bold;
}

.attachment-comments {
  font-size: var(--p-14);
  max-width: 120ch;
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
}

.attachment-action{
  padding-left: var(--p-14);
}

</style>
