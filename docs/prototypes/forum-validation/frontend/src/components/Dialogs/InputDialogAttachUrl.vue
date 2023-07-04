<template>
  <input v-if="'name' in userInput" placeholder="Text to display (required)" v-model="name" data-test="name-input"
    :class="{ 'invalid-input-highlight': highlight && !name }" />
  <div v-if="'name' in userInput && highlight && !name" class="required-message" data-test="required">
    *required
  </div>
  <input placeholder="Paste a link (required)" v-model="url" data-test="link-input"
    :class="{ 'invalid-input-highlight': highlight && !url }" />
  <div v-if="highlight && !url" class="required-message" data-test="required">
    *required
  </div>
  <textarea v-if="'comments' in userInput" class="comments" placeholder="Comments" v-model="comments"
    data-test="comments-text-area">
  </textarea>
</template>


<script>
export default {
  name: 'input-dialog-attach-url',
  emits: ['update:userInput', 'update:allRequiredFieldsFilled', 'validationDone'],
  props: {
    userInput: {
      type: Object,
      required: true,
    },
    runValidation: {
      type: Boolean,
    },
  },
  data() {
    return {
      highlight: false,
    };
  },
  computed: {
    requiredFields() {
      return this.userInput.requiredFields || [];
    },
    name: {
      get() {
        return this.userInput.name;
      },
      set(value) {
        this.updateUserInput('name', value);
      },
    },
    url: {
      get() {
        return this.userInput.data;
      },
      set(value) {
        this.updateUserInput('data', value);
      },
    },
    comments: {
      get() {
        return this.userInput['comments'];
      },
      set(value) {
        this.updateUserInput('comments', value);
      },
    },
    allRequiredFieldsFilled() {
      return this.requiredFields.every((field) => !!this[field] && this[field].length > 0);
    },
  },
  watch: {
    runValidation(currentValidationState, previousValidationState) {
      if (currentValidationState !== previousValidationState && currentValidationState === true) {
        this.validateRequiredFields();
        this.$emit('validationDone');
      }
    },
  },
  methods: {
    confirmClicked() {
      this.validateRequiredFields();
    },
    updateUserInput(field, value) {
      const input = this.userInput;
      input[field] = value;
      this.$emit('update:userInput', input);
    },
    validateRequiredFields() {
      const allFieldsFilled = this.requiredFields.every((field) => !!this[field] && this[field].length > 0);
      if (!allFieldsFilled) {
        this.highlightRequiredFields();
      } else {
        this.$emit('update:allRequiredFieldsFilled', allFieldsFilled);
      }
    },
    highlightRequiredFields() {
      this.highlight = true;
    },
  },
};
</script>


<style>

.comments {
  flex: 3 0 auto;
  height: 8rem;
}

.required-message {
  color: var(--rosalution-red-100);
  transform: translateY(-1rem);
}

</style>
