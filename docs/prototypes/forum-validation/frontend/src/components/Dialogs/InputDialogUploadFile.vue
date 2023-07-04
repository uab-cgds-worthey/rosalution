<template>
  <div class="drop-file-box" @dragover="dragover"  @drop="drop">
    <div v-if="!fileUploaded" class="drop-file-box-content">
        Drag & drop or
        <input
          type="file"
          id="attach-file-button"
          @change="onChanged"
          ref="file"
          :accept="fileTypeAccept"
          hidden
        />
        <label for="attach-file-button" class="browse-button"> browse </label>
    </div>
    <div v-else class="drop-file-box-content" v-cloak>
      <span class="file-name">
        {{ fileUploaded.name }}
        <button v-if="!userInput.attachment_id" type="button" @click="remove(fileUploaded)" title="Remove file">
          remove
        </button>
      </span>
    </div>
  </div>
  <textarea v-if="'comments' in userInput"
    class="comments"
    placeholder="Comments"
    v-model="comments"
  ></textarea>
</template>

<script>
export default {
  name: 'input-dialog-upload-file',
  emits: ['update:userInput', 'update:allRequiredFieldsFilled', 'validationDone'],
  props: {
    userInput: {
      type: Object,
      required: true,
    },
    fileTypeAccept: {
      type: String,
      default: '.json',
    },
    runValidation: {
      type: Boolean,
    },
  },
  data() {
    return {
      highlight: {},
    };
  },
  computed: {
    requiredFields() {
      return this.userInput.requiredFields || [];
    },
    fileUploaded: {
      get() {
        return this.userInput.data;
      },
    },
    comments: {
      get() {
        return this.userInput['comments'] || '';
      },
      set(value) {
        this.updateUserInput('comments', value);
      },
    },
    allRequiredFieldsFilled() {
      return Boolean(this.fileUploaded && this.fileUploaded !== '');
    },
  },
  watch: {
    runValidation(currentValidationState, previousValidationState) {
      if (currentValidationState !== previousValidationState && currentValidationState === true) {
        this.validateAndHighlightFields();
        this.$emit('validationDone'); // Emit event after validation
      }
    },
    fileUploaded: {
      handler(newFile) {
        this.validateAndHighlightFields();
      },
      deep: true,
    },
  },
  methods: {
    updateUserInput(field, value) {
      const input = this.userInput;
      input[field] = value;
      this.$emit('update:userInput', input);
    },
    onChanged() {
      this.updateUserInput('data', this.$refs.file.files[0]);
    },
    remove(i) {
      this.updateUserInput('data', '');
    },
    dragover(event) {
      event.preventDefault();
    },
    dragleave(event) {
      // event.preventDefault();
    },
    drop(event) {
      event.preventDefault();
      if (!this.fileUploaded) {
        this.$refs.file.files = event.dataTransfer.files;
        this.onChanged();
      }
    },
    validateAndHighlightFields() {
      this.$emit('update:allRequiredFieldsFilled', this.allRequiredFieldsFilled);
    },
  },
};
</script>


<style scoped>

input[type=file]::file-selector-button {
  border: none;
}

.browse-button {
  color: var(--rosalution-blue-200);
  border-bottom: 2px solid var(--rosalution-blue-200);
  font-family: sans-serif;
  cursor: pointer;
  margin-top: 4px;
}

[v-cloak] {
  display: none;
}

.file-name {
  display: inline-block;
  text-align: center;
  vertical-align: middle;
  padding: 1rem;
  margin: 0%;
}

.drop-file-box-content {
  display: flex;
  height: 12rem; /* This is not accepting the var(--p-10) variable. reason unknown*/
  justify-content: center ;
  align-items: center;
  gap: var(--p-1);
}

.drop-file-box {
  flex: 7 0 auto;
  border-radius: 20px;
  background-image: url("data:image/svg+xml,%3csvg width='100%25' height='100%25'\
    xmlns='http://www.w3.org/2000/svg'%3e%3crect width='100%25' height='100%25'\
    fill='none' rx='20' ry='20' stroke='%23E7E6E6FF' stroke-width='4'\
    stroke-dasharray='6%2c 14' stroke-dashoffset='0'\
    stroke-linecap='round'/%3e%3c/svg%3e");
}

.comments {
  flex: 3 0 auto;
  height: 8rem;
}

</style>
