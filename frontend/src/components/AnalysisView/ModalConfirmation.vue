<template>
    <div class="modal-background">
        <div class="modal-container">
            <h2>Delete File?</h2>
            <span>Deleting this file will remove it from the supporting evidence list.</span>
            <div class="cancel-button-column">
              <a
                  title="Cancel"
                  class="cancel-button-item"
                  @click="cancelModal()"
                  data-test="cancel-modal">
                      Cancel
              </a>
            </div>
            <div class="delete-button-column">
              <a
                  title="Delete"
                  class="delete-button-item"
                  @click="deleteAttachment()"
                  data-test="delete-button">
                      Delete
              </a>
            </div>
        </div>
    </div>
  </template>

<script>

export default {
  name: 'modal-confirmation',
  methods: {
    deleteAttachment() {
      this.$emit('deleteattachment');
      this.cancelModal();
    },
    cancelModal() {
      this.$emit('cancelconfirmation');
    },
  },
};
</script>

<style scoped>
  .modal-background {
    position: fixed;
    z-index: 1;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    z-index: 1;
    background-color: rgba(192, 192, 192, 0.45);
  }

  .modal-container {
    background-color: white;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    background-color: var(--rosalution-white);
    width: 385px;
    height: 170px;
    border-radius: 10px;
    box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
    padding: 20px 35px 15px 35px;
    z-index: 999;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }

  h2 {
    display: flex;
    grid-column: 1 / 3;
    grid-row: 1;
    margin: 0px;
    align-items: center;
  }

  span {
    font-family: "Proxima Nova", sans-serif;
    font-size: 14px;
    grid-column: span 2 / 3;
    grid-row: 2;
  }

  .cancel-button-item {
    display: flex;
    grid-row: 3;
    text-decoration: none;
    font-size: 100%;
    font-weight: bold;
    line-height: 1.625rem;
    text-align: center;
    border-radius: 2rem;
    border-color: black;
    border-style: solid;
    justify-content: center;
    align-items: center;
    height: 25px;
    width: 100px;
    cursor: pointer;
  }

  .delete-button-column {
    display: flex;
    justify-content: right;
    align-items: center;
    cursor: pointer;
  }

  .cancel-button-column {
    display: flex;
    justify-content: left;
    align-items: center;
  }

  .delete-button-item {
    display: flex;
    grid-row: 3;
    background-color: var(--rosalution-purple-100);
    border-radius: 2rem;
    text-decoration: none;
    font-size: 100%;
    font-weight: bold;
    line-height: 1.625rem;
    text-align: center;
    justify-content: center;
    align-items: center;
    height: 30px;
    width: 100px;
  }

</style>
