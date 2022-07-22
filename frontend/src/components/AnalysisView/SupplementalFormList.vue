<template>
  <table class="supplemental-container">
    <tbody>
        <tr class="supplemental-header">
            <td>
                <h2>Supplemental Attachments</h2>
            </td>
            <td>
                <button class="add-attachment-button" @click="showAttachDocumentModal()" data-test="add-button">
                    <font-awesome-icon icon="circle-plus" size="2xl"/>
                </button>
            </td>
            <td class="collapse-box">
                <font-awesome-icon icon="chevron-down" size="lg"/>
            </td>
        </tr>
        <ModalDialog v-if="showModal"
                    v-on:closemodal="this.showAttachDocumentModal"
                    v-on:addattachment="this.onAttachmentChange"
                    data-test="modal-dialog"/>
        <div class="attachment-list" v-for="attachment in attachments" v-bind:key="attachment.id">
            <tr class="attachment-row">
                <td class="attachment-logo">
                    <font-awesome-icon :icon="['far', 'file']" size="lg"/>
                </td>
                <td class="attachment-name">
                    <span> {{ attachment.name }}</span>
                </td>
                <td>
                    <button class="comment-button" v-on:click="comment(attachment.comment)">
                        <font-awesome-icon :icon="['far', 'comment']" size="xl"/>
                    </button>
                </td>
                <td>
                    <button class="edit-button" v-on:click="edit(attachment)">
                        <font-awesome-icon icon="pencil" size="xl"/>
                    </button>
                </td>
            </tr>
        </div>
    </tbody>
  </table>
</template>

<script>
import ModalDialog from '@/components/AnalysisView/ModalDialog.vue';

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

    .supplemental-container {
        display: flex;
        flex-direction: column;
        padding: var(--p-10);
        margin: 0.625rem;
        width: 100%;
        gap: .625rem;
        border-radius: 1.25rem;
        background-color: var(--rosalution-white);
    }

    .supplemental-header {
        line-height: 1.75rem;
        height: 1.75rem;
        margin: .125rem .125rem 0 .125rem;
    }

    .collapse-box {
        color: var(--rosalution-grey-200);
        right: 3%;
        position: absolute;
        vertical-align: middle;
        height: 1.75rem;
    }

    .attachment-list:nth-child(even) {
        background-color: var(--rosalution-grey-100);
    }

    .attachment-list:nth-child(odd) {
        background-color: var(--rosalution-grey-50);
    }

    .add-attachment-button {
        border: none;
        background: none;
    }

    .attachment-list {
        height: 4rem;
        width: 100%;
        vertical-align: middle;
        align-items: center;
    }

    .attachment-row {
        height: 1.75remrem;
        width: 55rem;
        vertical-align: middle;
        font-size: 1.125rem;
        line-height: 1.75rem;
    }

    .attachment-name {
        padding-left: 1rem;
        color: var(--rosalution-purple-300);
        vertical-align: middle;
        font-weight: bold;
    }

    .edit-button {
        border: none;
        background: none;
        float: right;
        right: 6%;
        position: absolute;
        vertical-align: middle;
    }

    .comment-button {
        border: none;
        background: none;
        float: right;
        right: 9%;
        position: absolute;
        vertical-align: middle;
    }

    .attachment-logo {
        border: none;
        background: none;
        float: left;
        margin: auto;
        align-content: center;
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
        padding-right: 0.75rem;
        padding-left: 0.75rem;
        vertical-align: middle;
    }

</style>
