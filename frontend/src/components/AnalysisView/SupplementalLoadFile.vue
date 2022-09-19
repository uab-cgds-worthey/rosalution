<template>
    <div class="supplemental-load-file-container">
        <div class="drop-file-box" @dragover="dragover"  @drop="drop">
          <div v-if="!fileUploaded || !fileUploaded.length">
            Drag & drop or
            <input type="file" id="attachFileBtn" @change="onFileChange" ref="file" accept=".pdf, .jpg, .jpeg, .png"
            data-test="attach-file-button" hidden/>
            <label for="attachFileBtn" id="browseBtn">
              browse
            </label>
          </div>
          <div>
            <tbody v-if="this.fileUploaded.length" v-cloak>
              <tr v-for="file in fileUploaded" v-bind:key="file.name" id="fileName">
                {{ file.name }}
                <button type="button" @click="remove(fileUploaded)" title="Remove file" id="removeBtn">
                  remove
                </button>
              </tr>
            </tbody>
          </div>
        </div>
        <div>
            <textarea placeholder="Comments" id="commentsBox" @change="onCommentChange" v-model="comments"
            data-test="comments-text-area">
            </textarea>
        </div>
    </div>
</template>

<script>
export default {
  name: 'supplemental-load-file',
  data() {
    return {
      fileUploaded: '',
      comments: '',
    };
  },
  methods: {
    onFileChange() {
      this.fileUploaded = this.$refs.file.files;
      this.$emit('fileadded', this.fileUploaded);
    },
    onCommentChange() {
      this.$emit('commentadded', this.comments);
    },
    remove(i) {
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
  },
};
</script>

<style scoped>

@import url("https://use.typekit.net/rgh1osc.css");

div {
    font-family: "Proxima Nova", sans-serif;
    padding: 0%;
}

.supplemental-load-file-container {
  width: fit-content;
  height: fit-content;
}

h2 {
    float: left;
    margin: 0%;
    text-align: left;
    display: block;
}

.drop-file-box {
  display: inline-block;
  padding-left: 1rem;
  padding-right: 1rem;
  padding-top: 2rem;
  margin: 1rem 1rem .5rem 1rem;
  border: 0.120rem dashed var(--rosalution-grey-100);
  border-radius: .4375rem;
  width: 24rem;
  height: 6.5rem;
  text-align: center;
  vertical-align: middle;
  align-items: center;
  font-size: 1.125rem;
}

#commentsBox {
  display: block;
  padding: 1rem;
  margin: 1rem 1rem .5rem 1rem;
  border-style: solid;
  border-color: var(--rosalution-grey-100);
  border-radius: 7px;
  width: 24rem;
  height: 6.5rem;
  outline: none;
  resize: none;
  font-family: "Proxima Nova", sans-serif;
  text-align: left;
  font-size: 1.125rem;
  color: var(--rosalution-grey-200);
}

span {
  display: block;
  overflow: hidden;
  padding: 0px 4px 0px 6px;
}

input[type=file]::file-selector-button {
  border: none;
}

textarea::placeholder {
  color: var(--rosalution-grey-200);
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
