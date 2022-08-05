<template>
  <div>
    <div class="modal-background" @click="closeModal()"></div>
    <div class="modal-container">
      <a title="Close" class="close-item" @click="closeModal()" data-test="close-modal">Close</a>
      <a title="Add" class="addbutton-item" @click="addAttachment()" data-test="add-button">Add</a>
      <div class="content-item">
        <br>
        <!-- Leaving here for tabbed in the future -->
        <!-- <SupplementalLoadFile v-on:fileadded="this.getFile" v-on:commentadded="this.getComments"/> -->
        <SupplementalLoadLink
          v-on:linknameadded="this.getLinkName"
          v-on:linkadded="this.getLink"
          v-on:commentadded="this.getComments"
        />
      </div>
    </div>
  </div>
</template>

<script>
// Unsure how tabbed will handle this, but leaving here for now
// import SupplementalLoadFile from '@/components/AnalysisView/SupplementalLoadFile.vue';
import SupplementalLoadLink from '@/components/AnalysisView/SupplementalLoadLink.vue';

export default {
  name: 'modal-dialog',
  components: {
    // SupplementalLoadFile,
    SupplementalLoadLink,
  },
  data: function() {
    return {
      name: '',
      type: '',
      data: null,
      comments: '',
    };
  },
  created() {
  },
  methods: {
    closeModal() {
      this.$emit('closemodal');
    },
    addAttachment() {
      const attachment = {
        name: this.name,
        type: this.type,
        data: this.data,
        comment: this.comments,
      };
      this.$emit('addattachment', attachment);
      this.closeModal();
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

.header-item {
  grid-area: header;
  font-size: 150%;
  margin: 25px;
}
.content-item {
  grid-area: main;
  text-align: left;
  margin: 25px;
}
.addbutton-item {
  grid-area: addbutton;
  background-color: green;
  border-radius: 2rem;
  text-decoration: none;
  font-size: 80%;
  line-height: 50px;
  text-align: center;
  justify-self: stretch;
  margin: 25px;
}
.addbutton-item:hover{
  background-color: rgba(0, 128, 0, 0.74);
}
.close-item {
  grid-area: close;
  color: #aaa;
  text-decoration: none;
  font-size: 80%;
  line-height: 50px;
  text-align: center;
  justify-self: stretch;
  border-radius: 2rem;
  border-color: black;
  border-style: solid;
  margin: 25px;
}
.close-item:hover{
  color:black;
  background-color: red;
}
.modal-container {
  vertical-align: middle;
  display: grid;
  z-index: 999;
  grid-template-columns: 450px 270px 270px 110px;
  grid-template-rows: auto;
  grid-template-areas:
    "header header header header"
    "main main main main"
    ". close addbutton  .";
  background-color: white;
  font-weight: 600;
  font-size: 18px;
  line-height: 1.4;
  color: black;
  position: absolute;
  border-radius: 1rem;
  justify-items: center;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

a {
  color: inherit;
}

small {
  color: lightslategrey;
}


</style>
