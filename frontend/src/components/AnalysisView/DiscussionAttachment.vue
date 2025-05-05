<template>
<span :class="accessAttachment" class="attachment" :title="name">
  <font-awesome-icon :icon="attachmentIcon" size="lg" class="attachment-icon"/>
  <a v-if="type=='file'"
     @click="downloadAttachment(attachment)"
     :class="accessAttachment"
     class="attachment-text content"
  >
    {{ name }}
  </a>
  <a v-if="type=='link'"
    :href="attachment.data"
    target="_blank"
    rel="noreferrer noopener"
    class="attachment-text content"
    :class="accessAttachment"
  >
    {{ name }}
  </a>
  <font-awesome-icon v-if="removeable"
    icon="xmark"
    size="sm"
    @click="$emit('remove')"
    class="attachment-icon remove-attachment-icon"
  />
</span>
</template>

<script setup>

import {inject} from 'vue';

const props = defineProps({
  postId: {
    type: String,
  },
  type: {
    type: String,
    default: '',
  },
  name: {
    type: String,
  },
  removeable: {
    type: Boolean,
    default: false,
  },
  attachment: {
    type: Object,
  },
});

const downloadAttachment = inject('downloadFile');

const iconMapping = {
  'file': ['far', 'file'],
  'link': 'link',
};

const attachmentIcon =  props.type in iconMapping ? iconMapping[props.type] : 'question';
const accessAttachment = !props.removeable ? 'available' : '';

</script>

<style scoped>

.attachment {
  background-color: var(--rosalution-white);
  color: var(--rosalution-black);
  border-radius: var(--content-border-radius);
  border: 1px solid var(--rosalution-black);
  box-sizing: border-box;

  display: flex;
  gap: var(--p-1);
  align-items: center;
  cursor: pointer;
  padding: var(--p-05);
}

.attachment-icon {
  padding: var(--p-05);
}

.remove-attachment-icon {
  padding-left: var(--p-1);
}

.remove-attachment-icon:hover {
  color: var(--rosalution-grey-300)
}

.attachment-text {
  cursor: pointer;
  font-size: 1rem;

  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.content {
  flex-grow: 1;
}

.available.attachment:hover {
  border-color: var(--rosalution-grey-200);
  color: var(--rosalution-grey-300);
}

.available.attachment-text:hovor {
  color: var(--rosalution-grey-200)
}

.available.attachment-text:active,
.available.attachment-text:focus {
  color: var(--rosalution-grey-300)
}

</style>
