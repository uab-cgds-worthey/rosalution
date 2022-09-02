<template>
  <table class="supplemental-container">
    <tbody>
        <tr class="supplemental-header">
            <td>
                <h2 class="supplemental-header-name">Supplemental Attachments</h2>
            </td>
            <td>
                <button class="add-attachment-button" @click="showAttachDocumentModal()" data-test="add-button">
                    <font-awesome-icon icon="circle-plus" size="xl"/>
                </button>
            </td>
            <td class="collapse-box">
                <font-awesome-icon icon="chevron-down" size="lg"/>
            </td>
        </tr>
        <div class="seperator"></div>
        <ModalDialog v-if="showModal"
                    v-on:cancelmodal="this.showAttachDocumentModal"
                    v-on:addattachment="this.onAttachmentChange"
                    data-test="modal-dialog"/>
        <div class="attachment-list" v-for="attachment in attachments" v-bind:key="attachment.id">
            <tr class="attachment-row">
                <td class="attachment-logo">
                    <font-awesome-icon :icon="['far', 'file']" size="lg" v-if="attachment.type==='file'"/>
                    <font-awesome-icon icon="link" size="lg" v-else-if="attachment.type==='link'"/>
                </td>
                <td class="attachment-name">
                    {{ attachment.name }}
                </td>
                <td class="comment-button">
                    <button v-on:click="comment(attachment)">
                        <font-awesome-icon :icon="['far', 'comment']" size="xl"/>
                    </button>
                </td>
                <td class="edit-button">
                    <button  v-on:click="edit(attachment)">
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
    height: 1.75rem;
    display: flex;
    flex-direction: row;
  }

  .supplemental-header-name {
    height: 1.75rem;
    margin: .125rem .125rem 0 .125rem;
  }
  .add-attachment-button {
    border: none;
    background: none;
    height: 1.75rem;
    padding: 0;
  }

  .collapse-box {
    color: var(--rosalution-grey-200);
    float: right;
    right: 3%;
    position: absolute;
  }

  .seperator {
    height: .125rem;
    background-color: var(--rosalution-grey-100);
    border: solid .0469rem var(--rosalution-grey-100);
  }

  .attachment-list:nth-child(even) {
    background-color: var(--rosalution-grey-100);
  }

  .attachment-list:nth-child(odd) {
    background-color: var(--rosalution-grey-50);
  }

  .attachment-list {
    width: 100%;
    vertical-align: middle;
    align-items: center;
  }

  .attachment-row {
    height: 1.75rem;
    width: 100%;
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
    right: 3%;
    position: absolute;
    padding: 0.5rem 0 0.5rem 0;
  }

  .comment-button {
    border: none;
    background: none;
    float: right;
    right: 6%;
    position: absolute;
    padding: 0.5rem 0 0.5rem 0;
  }

  button {
    border: inherit;
    background-color: inherit;
    color: inherit;
  }

  .attachment-logo {
    border: none;
    background: none;
    float: left;
    padding: 0.5rem 0.75rem 0.5rem 0.75rem;
  }

</style>
