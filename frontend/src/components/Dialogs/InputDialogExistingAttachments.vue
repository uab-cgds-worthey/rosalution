<template>
  <div class="existing-attachments-list">
    <div 
      class="existing-attachments-list-row"
      v-for="existingAttachment in existingAttachments" 
      v-bind:key="existingAttachment.attachment_id"
      data-test="existing-attachments-list"
    >
      <span class="existing-attachment-logo">
        <font-awesome-icon :icon="['far', 'file']" size="lg" v-if="existingAttachment.type==='file'"/>
        <font-awesome-icon icon="link" size="lg" v-else-if="existingAttachment.type==='link'"/>
      </span>
      <label for="existing-attachment-row" class="existing-attachment-name">{{ existingAttachment.name }}</label>
      <input type="checkbox" class="existing-attachment-checkbox" name="existing-attachment-row"/>
    </div>
  </div>
</template>

<script setup>
console.log('SETUPPING THE THING');
import {computed, onMounted, reactive} from 'vue';

const emit = defineEmits(['update:userInput']);

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

console.log(props.existingAttachments);

onMounted(async () => {
  console.log('awhyyyyyyyyyyyy');
});
</script>

<style scoped>

.existing-attachments-list {
  background-color: var(--rosalution-white);
  margin: auto;
  border: 3px var(--rosalution-grey-100) solid;
  border-radius: var(--input-border-radius);
  padding: var(--p-8);
}

.existing-attachments-list-row {
  background-color: var(--rosalution-grey-50);
  padding: var(--p-8);
  margin: auto;
  border: 5px var(--rosalution-white) solid;
  border-radius: var(--input-border-radius);
}

.existing-attachment-logo {
  padding: var(--p-8);
  color: var(--rosalution-black);
}

.existing-attachment-name {
  color: var(--rosalution-purple-300);
  font-weight: bold;
  cursor: pointer;
  display:inline-block;
  vertical-align: middle;
}

/* .existing-attachment-checkbox input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
} */

.existing-attachment-checkbox {
  float: right;
}
</style>
