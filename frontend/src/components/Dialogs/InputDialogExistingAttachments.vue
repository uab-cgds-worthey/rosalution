<template>
  <div class="attach-existing-evidence">
    Existiing evidence list
    <div class="existing-evidences" v-for="evidence in existingEvidence" v-bind:key="evidence.attachment_id">
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
    </div>
  </div>
</template>

<script>
export default {
  name: 'input-dialog-existing-attachments',
  emits: ['update:userInput'],
  props: {
    userInput: {
      type: Object,
      required: true,
    },
    existingEvidence: {
      type: Array,
      default: () => {
        return [];
      },
    },
  },
  computed: {
  },
  methods: {
  },
};
</script>

<style scoped>

.attach-existing-evidence {
  width: 3rem;
}

</style>
