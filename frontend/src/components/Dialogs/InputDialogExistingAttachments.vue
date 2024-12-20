<template>
  <div class="input-dialog-existing-evidence">
    Existiing evidence list
    <!-- <div class="existing-evidences" v-for="evidence in existingEvidence" v-bind:key="evidence.attachment_id">
      Evidence here
      <tr class="evidence-row">
        <td class="evidence-logo">
          <font-awesome-icon :icon="['far', 'file']" size="lg" v-if="evidence.type==='file'"/>
          <font-awesome-icon icon="link" size="lg" v-else-if="evidence.type==='link'"/>
        </td>
        <td class="evidence-data">
          {{ evidence.name }}
        </td>
      </tr>
    </div> -->
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
  existingEvidence: {
    type: Array,
    default: () => {
      return [];
    },
  },
});

console.log(props.existingEvidence);

onMounted(async () => {
  console.log('awhyyyyyyyyyyyy');
});
</script>

<!-- <style scoped>

.attach-existing-evidence {
  width: 3rem;
}

</style> -->
