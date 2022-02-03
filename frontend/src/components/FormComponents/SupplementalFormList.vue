<template>
  <div>
      <div id="supplementalBlock">
        <h2>Supplemental</h2>
        <div>
            <button class="addAttachmentButton" @click="showAttachDocumentModal()" data-test="add-button">
                <img style="height: 25px; width: 25px;" src="../../assets/plus-logo.svg"/>
            </button>
        </div>
        <ModalDialog v-if="showModal"
                     v-on:closemodal="this.showAttachDocumentModal"
                     v-on:addattachment="this.onAttachmentChange"
                     data-test="modal-dialog"/>
        <div class="attachmentList" >
            <table>
            <tbody v-for="attachment in attachments" v-bind:key="attachment.id">
                <tr id="attachmentRow">
                    <td class="attachmentLogo">
                        <!-- This is broken at the moment and we're missing the icons for link and file -->
                        <!-- <img :src="'/src/assets/' + listIcon(attachment.type)" style="height: 40px; width: 32px; vertical-align: middle;"/> -->
                    </td>
                    <td id="attachmentName">
                        <span style="vertical-align: middle;"> {{ attachment.name }}</span>
                    </td>
                    <td>
                        <button id="commentButton" v-on:click="comment(attachment.comment)">
                            <img style="height: 32px; width: 32px; vertical-align: middle;"
                            src="../../assets/comment.png"/>
                        </button>
                    </td>
                    <td>
                        <button id="editButton" v-on:click="edit(attachment)">
                            <img style="height: 30px; width: 30px; vertical-align: middle;"
                            src="../../assets/edit.png"/>
                        </button>
                    </td>
                    <td id="removeAttachmentRow">
                        <button id="removeAttachmentButton" v-on:click="deleteRow(attachment)">
                            <img style="height: 30px; width: 30px;" src="../../assets/minus-button.png"/>
                        </button>
                    </td>
                </tr>
            </tbody>
            </table>
        </div>
      </div>
  </div>
</template>

<script>
import ModalDialog from '@/components/FormComponents/ModalDialog.vue';

export default {
  name: 'supplemental-form',
  data() {
    return {
      attachments: [
      ],
      showModal: false,
    };
  },
  components: {
    ModalDialog,
  },
  methods: {
    onAttachmentChange(attachment) {
    //   const fileData = file[0];
      this.attachments.push(attachment);
    },
    deleteRow(elem) {
      this.attachments.splice(elem, 1);
    },
    comment(attachment) {
      // This method will handle the commenting modal/feature
      console.log('Skeleton method for Commenting ' + attachment.name);
    },
    edit(attachment) {
      // This method will handle the edit modal/feature
      console.log('Skeleton method for Editing ' + attachment.name);
    },
    showAttachDocumentModal() {
      this.showModal = !this.showModal;
    },
    listIcon(type) {
      if (type === 'file') {
        return 'file.svg';
      } else if (type === 'link') {
        return 'link.svg';
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

    tbody:nth-child(even) {
        background-color: #DFDADA;
    }

    tbody:nth-child(odd) {
        background-color: #F6F6F6;
    }

    h2 {
        float: left;
        margin: 0;
        text-align: left;
    }

    .addAttachmentButton {
        border: none;
        background: none;
        float: right;
        text-align: center;
        margin: auto;
        align-content: center;
    }

    .addAttachmentInput {
        display:none;
    }

    #supplementalBlock {
        display: inline-block;
        width: 200px;
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
    }

    input[type="file"]  {
        height:0;
        display:none
    }

    .attachmentList {
        float: left;
        /* display: block; */
        height: 4rem;
        width: 50rem;
        vertical-align: middle;
        align-items: center;
    }

    tr {
        padding: none;
        font-size: 1.25rem;
        text-align: left;
        height: 4rem;
        width: 55rem;
        line-height: 4rem;
        vertical-align: middle;
    }

    th {
        font-weight: normal;
    }

    .attachmentRow {
        height: 4rem;
        width: 55rem;
    }

    #attachmentName {
        padding-left: 1rem;
        height: 4rem;
        width: 50rem;
    }

    #removeAttachmentButton {
        border: none;
        background: none;
        float: right;
        text-align: center;
        margin: auto;
        align-content: center;
    }

    #editButton {
        border: none;
        background: none;
        float: right;
        text-align: center;
        margin: auto;
        align-content: center;
    }

    #commentButton {
        border: none;
        background: none;
        float: right;
        text-align: center;
        margin: auto;
        align-content: center;
    }

    .attachmentLogo {
        border: none;
        background: none;
        float: left;
        text-align: center;
        margin: auto;
        align-content: center;
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
        padding-right: 0.75rem;
        padding-left: 0.75rem;
    }

    #removeAttachmentRow {
        border-left-width: 1rem;
        border-left-style: solid;
        border-left-color: white;
    }

</style>
