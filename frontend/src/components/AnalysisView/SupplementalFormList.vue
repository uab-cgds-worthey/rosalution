<template>
  <table class="supplemental-container">
    <input type="checkbox" id="supporting_toggle"/>
    <tbody>
      <tr class="supplemental-header">
        <td class="supplemental-header-content">
          <span>
            <h2 class="supplemental-header-name">Supporting Evidence</h2>
            <button class="add-attachment-button" @click="$emit('openModal')" data-test="add-button">
              <font-awesome-icon icon="circle-plus" size="xl"/>
            </button>
          </span>
          <label class="collapse-box" for="supporting_toggle">
            <font-awesome-icon icon="chevron-down" size="lg"/>
          </label>
        </td>
      </tr>
      <div class="seperator"></div>
      <div class="attachment-list" v-for="attachment in attachments" v-bind:key="attachment.attachment_id">
        <tr class="attachment-row">
          <td class="attachment-logo">
            <font-awesome-icon :icon="['far', 'file']" size="lg" v-if="attachment.type==='file'"/>
            <font-awesome-icon icon="link" size="lg" v-else-if="attachment.type==='link'"/>
          </td>
          <td class="attachment-data" rowspan="2">
            <div class="attachment-name">
              <div v-if="attachment.type=='file'" @click="$emit('download', attachment)"
                target="_blank" rel="noreferrer noopener">
                {{ attachment.name }}
            </div>
              <a v-if="attachment.type=='link'" :href="attachment.data" target="_blank" rel="noreferrer noopener">
                {{ attachment.name }}
              </a>
            </div>
            <div class="attachment-comments">
              {{ attachment.comments }}
            </div>
          </td>
          <td class="edit-button">
            <button @click="$emit('edit', attachment)" data-test="edit-button">
              <font-awesome-icon icon="pencil" size="xl"/>
            </button>
          </td>
          <td class="delete-button">
            <button @click="$emit('delete', attachment)" data-test="delete-button">
              <font-awesome-icon icon="xmark" size="xl"/>
            </button>
          </td>
        </tr>
      </div>
    </tbody>
  </table>
</template>

<script>

export default {
  name: 'supplemental-form',
  props: {
    attachments: {
      type: Array,
      default: () => {
        return [];
      },
    },
  },
};
</script>

<style scoped>
  div {
    font-family: "Proxima Nova", sans-serif;
    padding: var(--p-0);
  }

  .supplemental-container {
    display: flex;
    flex-direction: column;
    padding: var(--p-10);
    margin: var(--p-10);
    width: 100%;
    gap: var(--p-10);
    border-radius: 1.25rem;
    background-color: var(--rosalution-white);
  }

  .supplemental-header {
    height: 1.75rem;
    display: flex;
  }

  .supplemental-header-content {
    display: flex;
    flex: 1 0 auto;
  }

  .supplemental-header-content > span {
    display: inline-flex;
    flex: 1 0 auto;
    align-items: flex-end;
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
    color: var(--rosalution-black);
  }

  .collapse-box {
    color: var(--rosalution-grey-200);
    align-self: center;
    cursor: pointer;
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

  .attachment-data {
    padding-left: 1rem;
    vertical-align: middle;
  }

  .attachment-name {
    color: var(--rosalution-purple-300);
    font-weight: bold;
    cursor: pointer;
  }
  .attachment-comments {
    color: var(--rosalution-black);
    font-weight: normal;
    font-size: .875rem;
    max-width: 120ch;
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
  }

  .edit-button {
    border: none;
    background: none;
    float: right;
    right: 6%;
    position: absolute;
    padding: 0.5rem 0 0.5rem 0;
    color: var(--rosalution-black);
  }

  .delete-button {
    border: none;
    background: none;
    float: right;
    right: 3%;
    position: absolute;
    padding: 0.5rem 0 0.5rem 0;
    color: var(--rosalution-black);
  }

  button {
    border: inherit;
    background-color: inherit;
    color: inherit;
    cursor: pointer;
  }

  .attachment-logo {
    border: none;
    background: none;
    float: left;
    padding: 0.5rem 0.75rem 0.5rem 0.75rem;
    color: var(--rosalution-black);
  }

  input[type="checkbox"] {
    display: none;
  }

  .supplemental-container input[type="checkbox"]:checked ~ tbody > .attachment-list {
    display: none;
  }

  input[type="checkbox"]:checked ~ tbody > tr > td > .collapse-box {
    transform: scaleY(-1);
  }

  a {
    color: inherit;
  }

</style>
