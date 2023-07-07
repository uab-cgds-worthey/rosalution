<template>
  <div class="section-row">
    <label
      class="section-field"
      v-bind:style="[
        value.length === 0 && !this.editable
          ? 'color: var(--rosalution-grey-300);'
          : 'color: var(--rosalution-black);',
      ]"
    >
      {{ field }}
    </label>
    <span class="section-content">
      <span v-if="this.editable" role="textbox" class="editable-section-content-values" contenteditable
        data-test="editable-value" @input="onContentChanged($event)"
      >
        {{ value.join("\r\n") }}
      </span>
      <span v-else v-for="(rowValue, index) in value" :key="index" data-test="value-row">
        {{ rowValue }}
      </span>
    </span>
  </div>
</template>

<script>
export default {
  name: 'section-text',
  emits: ['update:sectionText'],
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
    isDataUnavailable: function() {
      return this.value == '.' || this.value == 'null' || this.value == null;
    },
    dataAvailabilityColour: function() {
      return this.isDataUnavailable ?
        'var(--rosalution-grey-300)' : this.linkout ? 'var(--rosalution-purple-300)' : 'var(--rosalution-black)';
    },
    content: function() {
      if (typeof this.value == 'object') {
        return this.value.join(this.delimeter);
      }

      return this.value;
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
  flex-direction: column;
  flex: 1 0 0;
}

.editable-section-content-values {
  overflow: hidden;
  resize: both;
  border-top: none;
  border-right: none;
  border-left: none;
  border-bottom: 2px solid var(--rosalution-purple-200);
}

span:focus {
  color: var(--rosalution-purple-300);
  outline: none;
  box-shadow: 0px 5px 5px var(--rosalution-grey-200);
}
</style>
