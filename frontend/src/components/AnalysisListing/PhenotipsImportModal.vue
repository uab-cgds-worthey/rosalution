<template>
    <div class="modal-background">
      <div class="modal-container modal-phenotips-import-container">
        <button title="Cancel" class="cancelbutton" @click="$emit('close')" data-test="cancel-button">Cancel</button>
        <button title="Add" class="addbutton" @click="onAddFile" data-test="add-button">Add</button>
        <div class="content-item">
          <br />
          <div class="tab-container">
            <div class="tab-buttons">
                <img class="phenotips-icon" src="@/assets/phenotips-favicon-96x96.png">
            </div>
          </div>
          <form ref="modal">
            <div class="drop-file-box" @dragover="dragover" @drop="drop">
              <div v-if="!fileUploaded || !fileUploaded.length">
                Drag & drop or
                <input
                  type="file"
                  id="attach-file-button"
                  @change="onFileChange"
                  ref="file"
                  accept=".json"
                  hidden
                />
                <label for="attach-file-button" class="browse-file-button"> browse </label>
              </div>
              <tbody v-if="this.fileUploaded.length" v-cloak>
                <tr v-for="file in this.fileUploaded" v-bind:key="file.name" class="file-name">
                  {{ file.name }}
                  <button type="button" @click="remove(fileUploaded)" title="Remove file" class="remove-button">
                    remove
                  </button>
                </tr>
              </tbody>
            </div>
          </form>
        </div>
      </div>
  </div>
</template>

<script>
export default {
  name: 'phenotips-modal-dialog',
  components: {},
  data: function() {
    return {
      fileUploaded: '',
    };
  },
  created() {},
  methods: {
    onFileChange() {
      this.fileUploaded = this.$refs.file.files;
    },
    remove() {
      this.fileUploaded = '';
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
        this.onFileChange();
      }
    },
    onAddFile() {
      this.$emit('upload', this.fileUploaded);
    },
  },
};
</script>

<style scoped>

button {
  border: none;
  background: none;
}

.phenotips-icon {
  height:24px
}

.modal-phenotips-import-container {
  display: grid;
  grid-template-columns: 200px 200px 200px;
  grid-template-rows: auto;
  grid-template-areas:
    "header header header"
    "main main main"
    "remove cancelbutton addbutton";
  background-color: var(--rosalution-white);
  font-weight: 600;
  font-size: 1rem;
  justify-items: center;
}

.content-item {
  grid-area: main;
}

.addbutton {
  grid-area: addbutton;
  background-color: var(--rosalution-purple-100);
  border-radius: 2rem;
  text-decoration: none;
  font-size: 100%;
  font-weight: bold;
  line-height: 1.625rem;
  text-align: center;
  justify-self: stretch;
  margin: 1.5rem;
  cursor: pointer;
}

.cancelbutton {
  grid-area: cancelbutton;
  text-decoration: none;
  font-size: 100%;
  font-weight: bold;
  line-height: 1.625rem;
  text-align: center;
  justify-self: stretch;
  border-radius: 2rem;
  border-color: black;
  border-style: solid;
  margin: 1.5rem;
  cursor: pointer;
}

a {
  color: inherit;
}

small {
  color: var(--rosalution-grey-200);
}

.tab-container {
  text-align: center;
  vertical-align: middle;
  align-items: center;
  grid-area: header;
}

.tab-buttons {
  text-align: center;
  vertical-align: middle;
  align-items: center;
  grid-area: header;
  display: inline-block;
  border: 2px var(--rosalution-grey-100) solid;
  width: 154px;
  border-radius: 7px;
  height: 36px;
}

.drop-file-box {
  display: inline-block;
  padding-left: 1rem;
  padding-right: 1rem;
  padding-top: 2rem;
  margin: 1rem 1rem 0.5rem 1rem;
  border: 0.12rem dashed var(--rosalution-grey-100);
  border-radius: 0.4375rem;
  width: 24rem;
  height: 6.5rem;
  text-align: center;
  vertical-align: middle;
  align-items: center;
  font-size: 1.125rem;
}

span {
  display: block;
  overflow: hidden;
  padding: 0px 4px 0px 6px;
}

input[type="file"]::file-selector-button {
  border: none;
}

.browse-file-button {
  display: inline-block;
  background-color: white;
  color: var(--rosalution-blue-150);
  border-bottom: 2px solid var(--rosalution-blue-150);
  font-family: sans-serif;
  cursor: pointer;
  margin-top: 1rem;
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

.remove-button {
  border-radius: 9999px;
  border-color: black;
  border-width: thin;
  background-color: #e7e7e7;
  display: inline-block;
  font-weight: 500;
  text-align: center;
}
</style>
