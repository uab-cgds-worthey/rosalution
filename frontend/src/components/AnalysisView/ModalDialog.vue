<template>
  <div>
    <div class="modal-background" @click="closeModal()"></div>
    <div class="modal-container">
      <a title="Clear" class="clear-item" @click="clearModal()" data-test="clear-modal">Clear</a>
      <a title="Cancel" class="cancel-item" @click="cancelModal()" data-test="cancel-modal">Cancel</a>
      <a title="Add" class="addbutton-item" @click="addAttachment()" data-test="add-button">Add</a>
      <div class="content-item">
        <br>
        <!-- Leaving here for tabbed in the future -->
        <div class="tab-container">
          <div class="tab-buttons">
            <span class="link-tab-container">
              <button class="link-tab-button" @click="showSupplementalLoadLink()"
                v-bind:class="{'link-tab-button_focused': showLink}"
                data-test="link-tab-button"
              >
                <font-awesome-icon icon="link" size="xl"/>
              </button>
            </span>
            <span class="file-tab-container">
              <button class="file-tab-button" @click="showSupplementalLoadFile()"
                v-bind:class="{'file-tab-button_focused': showFile}"
                data-test="file-tab-button"
              >
                <font-awesome-icon :icon="['far', 'file']" size="xl"/>
              </button>
            </span>
          </div>
        </div>
        <form ref="modal">
          <SupplementalLoadFile v-if="showFile"
            v-on:fileadded="this.getFile"
            v-on:commentadded="this.getComments"
            data-test="supplemental-load-file"
          />
          <SupplementalLoadLink v-if="showLink"
            v-on:linknameadded="this.getLinkName"
            v-on:linkadded="this.getLink"
            v-on:commentadded="this.getComments"
            data-test="supplemental-load-link"
          />
        </form>
      </div>
    </div>
  </div>
</template>

<script>
// Unsure how tabbed will handle this, but leaving here for now
import SupplementalLoadFile from '@/components/AnalysisView/SupplementalLoadFile.vue';
import SupplementalLoadLink from '@/components/AnalysisView/SupplementalLoadLink.vue';

export default {
  name: 'modal-dialog',
  components: {
    SupplementalLoadFile,
    SupplementalLoadLink,
  },
  data: function() {
    return {
      name: '',
      type: '',
      data: null,
      comments: '',
      showFile: true,
      showLink: false,
    };
  },
  created() {
  },
  methods: {
    showSupplementalLoadFile() {
      this.showFile = true;
      this.showLink = false;
    },
    showSupplementalLoadLink() {
      this.showLink = true;
      this.showFile = false;
    },
    clearModal() {
      this.$refs.modal.reset();
      if (this.showFile) {
        document.getElementById('removeBtn').click();
      }
    },
    cancelModal() {
      this.$emit('cancelmodal');
    },
    addAttachment() {
      const attachment = {
        name: this.name,
        type: this.type,
        data: this.data,
        comment: this.comments,
      };
      this.$emit('addattachment', attachment);
      this.cancelModal();
    },
    getFile(fileUploaded) {
      this.data = fileUploaded[0];
      this.name = fileUploaded[0].name;
      this.type = 'file';
    },
    getLink(link) {
      this.data = link;
      this.type = 'link';
    },
    getLinkName(name) {
      this.name = name;
    },
    getComments(comments) {
      this.comments = comments;
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
    "clear cancel addbutton";
  background-color: white;
  font-weight: 600;
  font-size: 18px;
  /* line-height: 1.4; */
  /* color: black; */
  position: absolute;
  border-radius: 1rem;
  justify-items: center;
  top: 110%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: fit-content;
  height: fit-content;
}

.header-item {
  grid-area: header;
  font-size: 150%;
  margin: 25px;
}

.content-item {
  grid-area: main;
  /* text-align: left; */
  /* margin: 25px; */
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

.clear-item {
  grid-area: clear;
  background-color: var(--cgds-red-200);
  text-decoration: none;
  font-size: 100%;
  font-weight: bold;
  line-height: 1.625rem;
  text-align: center;
  justify-self: stretch;
  border-radius: 2rem;
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
  color: lightslategrey;
}

.tab-container {
  text-align: center;
  vertical-align: middle;
  align-items: center;
  grid-area: header;
  /* display: inline;
  border: 1px red solid; */
  /* width: 154px; */
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

.file-tab-button_focused {
  color: var(--rosalution-blue-150) !important;
}

</style>
