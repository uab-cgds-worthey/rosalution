<template>
  <div class="section-row">
    <label class="section-field" v-bind:style="[
      value.length === 0 && !this.editable
        ? 'color: var(--rosalution-grey-300);'
        : 'color: var(--rosalution-black);',
    ]">
      {{ field }}
    </label>
    <div class="section-content" :data-test="`supporting-evidence-${field}`">
      <div class="supporting-evidence-content">
        <span v-if="isDataUnavailable && this.editable" role="textbox" @input="onContentChanged($event)">
          Attach
        </span>
        <span class="status-icon attachment-logo">
          <font-awesome-icon :icon="typeIcon" size="lg" />
        </span>
        <div v-if="content.type == 'file'" @click="$emit('download', content)" target="_blank" rel="noreferrer noopener" class="attachment-data attachment-name">
          {{ content.name }}
        </div>
        <a v-if="content.type == 'link'" :href="content.data" target="_blank" rel="noreferrer noopener" class="attachment-data attachment-name">
          {{ content.name }}
        </a>
      </div>
      <div class="action-items">
        <button @click="$emit('edit', content)" data-test="edit-button">
          <font-awesome-icon icon="pencil" size="xl" />
        </button>
        <button v-if="writePermissions" @click="$emit('delete', content)" data-test="delete-button">
          <font-awesome-icon icon="xmark" size="xl" />
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'supporting-evidence',
  emits: ['update:evidence'],
  props: {
    field: {
      type: String,
    },
    value: {
      type: Array,
      required: false,
    },
    editable: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    isDataUnavailable: function () {
      return this.value == '.' || this.value == 'null' || this.value == null || this.value.length == 0;
    },
    dataAvailabilityColour: function () {
      return this.isDataUnavailable ? 'var(--rosalution-grey-300)' : 'var(--rosalution-black)';
    },
    typeIcon: function () {
      if (this.isDataUnavailable) {
        return undefined;
      } else if (this.content.type === 'file') {
        return ['far', 'file'];
      }

      return 'link';
    },
    content: function () {
      if (this.isDataUnavailable) {
        return {};
      }

      return this.value[0];
    },
  },
  methods: {
    onContentChanged(event) {
      const contentRow = {
        field: this.field,
        value: event.target.innerText.split('\n'),
      };
      this.$emit('update:sectionText', contentRow);
    },
  },
};
</script>

<style scoped>
.section-row {
  display: flex;
  flex-direction: row;
  gap: var(--p-10);
  padding: var(--p-1);
}

.section-field {
  flex: 0 0 11.25rem;
  font-weight: 600;
}

.section-content {
  display: flex;
  flex-direction: row;
  flex: 1 0 0;
  justify-content: space-between;
  align-items: center;
  background-color: var(--rosalution-grey-50);
  border-radius: var(--content-border-radius);
  padding: var(--p-10);
}

.attachment-name {
  color: var(--rosalution-purple-300);
  font-weight: bold;
  cursor: pointer;
}

.supporting-evidence-content {
  display: flex;
  align-items: center;
  gap: var(--p-10);
}

.action-items svg{
  color: var(--rosalution-black);
}

.action-items > button {
  border: none;
  background: none;
}

</style>
