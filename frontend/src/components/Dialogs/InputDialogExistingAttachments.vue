<template>
  <div class="existing-attachments-list">
    <div
      v-if="existingAttachments.length == 0"
      class="no-existing-attachments-content"
    >
      No existing attachments.
    </div>
    <div
      class="existing-attachments-list-row"
      v-for="existingAttachment in props.existingAttachments"
      v-bind:key="existingAttachment.attachment_id"
      data-test="existing-attachments-list"
    >
      <span class="existing-attachment-logo">
        <font-awesome-icon :icon="['far', 'file']" size="lg" v-if="existingAttachment.type==='file'"/>
        <font-awesome-icon icon="link" size="lg" v-else-if="existingAttachment.type==='link'"/>
      </span>
      <label :for="existingAttachment.attachment_id" class="existing-attachment-name">
        {{ existingAttachment.name }}
        <input type="checkbox"
        :id="existingAttachment.attachment_id"
        class="existing-attachment-checkbox"
        :value="existingAttachment"
        v-model="checkedAttachments"
        @change="onChanged($event)"
        />
      </label>
    </div>
  </div>
</template>

<script setup>
// console.log('Setting up the Input Dialog Existing Attachments');
import {onMounted, ref, toRaw} from 'vue';

const emit = defineEmits(['update:userInput']);
const checkedAttachments = ref([]);

defineOptions({
  name: 'input-dialog-existing-attachments',
});

const props = defineProps({
  userInput: {
    type: Object,
    required: false,
  },
  existingAttachments: {
    type: Array,
    default: () => {
      return [];
    },
  },
});

onMounted(async () => {
});

function onChanged() {
  const unwrappedAttachments = checkedAttachments.value.map(function(attachment) {
    return toRaw(attachment);
  });
  emit('update:userInput', unwrappedAttachments);
}
</script>

<style scoped>

.no-existing-attachments-content {
  height: 12rem;
  text-align: center;
  align-content: center;
}

.existing-attachments-list {
  background-color: var(--rosalution-white);
  border: 3px var(--rosalution-grey-100) solid;
  border-radius: var(--input-border-radius);
}

.existing-attachments-list-row {
  background-color: var(--rosalution-grey-50);
  padding: var(--p-8);
  border: 5px var(--rosalution-white) solid;
  border-radius: var(--input-border-radius);

  display: flex;
  align-items: center;
  gap: var(--p-8)
}

.existing-attachment-logo {
  color: var(--rosalution-black);
}

.existing-attachment-name {
  color: var(--rosalution-purple-300);
  font-weight: bold;
  cursor: pointer;

  flex-grow: 1;

  display: flex;
  justify-content: space-between;
  align-items: center;
}

.existing-attachment-checkbox {
  transform: unset;
}
</style>
