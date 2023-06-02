<template>
<div class="section-row">
  <label class="section-field"
    v-bind:style="[value.length === 0 && !this.editable ? 'color: var(--rosalution-grey-300);' : 'color: var(--rosalution-black);']" >
    {{ field }}
  </label>
  <span class="section-content">
    <span v-if="this.editable" role="textbox" class="editable-section-content-values" contenteditable data-test="editable-value" @input="onContentChanged($event)">
      {{ value.join('\r\n') }}
    </span>
    <span v-else v-for="rowValue, index in value" :key="index" class="section-content-values" data-test="value-row">
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
        'var(--rosalution-grey-300)' :
          this.linkout ? 'var(--rosalution-purple-300)' :
          'var(--rosalution-black)';
    },
    content: function() {
      if (typeof(this.value) == 'object') {
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
      console.log(contentRow);
      console.log('section text');
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
  /* margin: var(--p-10) var(--p-1) var(--p-10) var(--p-1); */
  background-color: hotpink;
}

.section-field {
  width: 11.25rem;
  font-weight: 600;
  text-align: left;
  background-color: gold;
}

.section-content {
  text-align: left;
  color: var(--rosalution-black);
  display: block;
}

.section-content-values {
  font-size: 1.125rem;
  color: var(--rosalution-black);
  display: block;
  width: 100%;
}

.editable-section-content-values {
  display: block;
  width: 100%;
  overflow: hidden;
  resize: both;
  border-top: none;
  border-right: none;
  border-left: none;
  border-bottom: 2px solid var(--rosalution-purple-200);
  font-family: inherit;
  font-size: inherit;
}

span:focus {
  color: var(--rosalution-purple-300);
  outline: none;
  box-shadow: 0px 5px 5px var(--rosalution-grey-200);
}
</style>
