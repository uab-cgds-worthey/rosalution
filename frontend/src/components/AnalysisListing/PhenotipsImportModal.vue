<template>
  <div>
    <div class="modal-background" @click="closeModal()"></div>
    <div class="modal-container">
      <a title="Cancel" class="cancel-item" @click="cancelModal()" data-test="cancel-modal" >
        Cancel
      </a>
      <a title="Add" class="addbutton-item" @click="addAttachment()" data-test="add-button" >
        Add
      </a >
      <div class="content-item">
        <br />
        <!-- Leaving here for tabbed in the future -->
        <div class="tab-container">
          <div class="tab-buttons">
            <span class="link-tab-container">
              <button class="file-upload" data-test="file-upload-button">
                <img src="@/assets/phenotips-favicon-96x96.svg" />
              </button>
            </span>
          </div>
        </div>
        <form ref="modal">
          <div class="supplemental-load-file-container">
            <div class="drop-file-box" @dragover="dragover" @drop="drop">
              <div v-if="!fileUploaded || !fileUploaded.length">
                Drag & drop or
                <input
                  type="file"
                  id="attachFileBtn"
                  @change="onFileChange"
                  ref="file"
                  accept=".pdf, .jpg, .jpeg, .png"
                  data-test="attach-file-button"
                  hidden
                />
                <label for="attachFileBtn" id="browseBtn"> browse </label>
              </div>
              <div>
                <tbody v-if="this.fileUploaded.length" v-cloak>
                  <tr v-for="file in fileUploaded" v-bind:key="file.name" id="fileName">
                    {{
                      file.name
                    }}
                    <button
                      type="button"
                      @click="remove(fileUploaded)"
                      title="Remove file"
                      id="removeBtn"
                    >
                      remove
                    </button>
                  </tr>
                </tbody>
              </div>
            </div>
            <div>
              <textarea
                placeholder="Comments"
                id="commentsBox"
                @change="onCommentChange"
                v-model="comments"
                data-test="comments-text-area"
              >
              </textarea>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "modal-dialog",
  components: {},
  data: function () {
    return {
      name: "",
      type: "",
      data: null,
      comments: "",
      showFile: true,
      showLink: false,
    };
  },
  created() {},
  methods: {
    cancelModal() {
      this.$emit("cancelmodal");
    },
    getFile(fileUploaded) {
      this.data = fileUploaded[0];
      this.name = fileUploaded[0].name;
      this.type = "file";
    },
  },
};
</script>

<style scoped>
.modal-background {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 1;
  background-color: rgba(192, 192, 192, 0.45);
}

.modal-container {
  vertical-align: middle;
  display: grid;
  z-index: 999;
  grid-template-columns: 200px 200px 200px;
  grid-template-rows: auto;
  grid-template-areas:
    "header header header"
    "main main main"
    "remove cancel addbutton";
  background-color: var(--rosalution-white);
  font-weight: 600;
  font-size: 1rem;
  position: absolute;
  border-radius: 1rem;
  justify-items: center;
  top: 100%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.header-item {
  grid-area: header;
  font-size: 150%;
  margin: 25px;
}

.content-item {
  grid-area: main;
}

.addbutton-item {
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
}

.cancel-item {
  grid-area: cancel;
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
}

a {
  color: inherit;
}

small {
  color: var(--rosalution-grey-200);
}

.supplemental-load-file-container {
  width: fit-content;
  height: fit-content;
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

.link-tab-button {
  background-color: var(--rosalution-white);
  border: none;
  border-right: 1px var(--rosalution-grey-100) solid;
  text-align: center;
  vertical-align: middle;
  align-items: center;
  width: 73px;
  height: 36px;
  color: var(--rosalution-grey-300);
}

.link-tab-button_focused {
  color: var(--rosalution-blue-150) !important;
}

.file-tab-button {
  background-color: white;
  border: none;
  border-left: 1px var(--rosalution-grey-100) solid;
  text-align: center;
  vertical-align: middle;
  align-items: center;
  width: 73px;
  height: 36px;
  padding: 0%;
  color: var(--rosalution-grey-300);
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

#browseBtn {
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

#fileName {
  display: inline-block;
  text-align: center;
  vertical-align: middle;
  padding: 1rem;
  margin: 0%;
}

#removeBtn {
  border-radius: 9999px;
  border-color: black;
  border-width: thin;
  background-color: #e7e7e7;
  display: inline-block;
  font-weight: 500;
  text-align: center;
}
</style>
