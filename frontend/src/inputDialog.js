import {reactive} from 'vue';

const state = reactive({
  tabs: [],
  active: false,
  activeTabName: '',
  confirmText: 'Ok',
  cancelText: 'Cancel',
  deleteText: '',
  warningText: '',
});

// -----------------------------------
// Private Methods
// -----------------------------------
let close;

const dialogPromise = () => new Promise((resolve) => (close = resolve));

const open = () => {
  state.active = true;
  return dialogPromise();
};

const reset = () => {
  state.tabs.splice(0),
  state.active = false;
  state.activeTabName = '';
  state.confirmText = 'Ok';
  state.cancelText = 'Cancel';
  state.deleteText = '';
  state.warningText = '';
};

// -----------------------------------
// Public interface
// -----------------------------------

export default {
  get state() {
    return state;
  },
  confirmText(text) {
    state.confirmText = text;
    return this;
  },
  cancelText(text) {
    state.cancelText = text;
    return this;
  },
  deleteText(text) {
    state.deleteText = text;
    return this;
  },
  warningText(text) {
    state.warningText = text;
    return this;
  },
  file(includeComments=false, includeIcon='file', fileTypesAccept='.json') {
    const fileInput = {
      name: 'input-dialog-upload-file',
      icon: includeIcon,
      input: {
        data: '',
        ...(includeComments) && {comments: ''},
        type: 'file',
      },
      props: {
        fileTypeAccept: fileTypesAccept,
      },
    };

    state.tabs.push(fileInput);
    state.activeTabName = fileInput.name;
    return this;
  },
  url(includeComments=false, includeName=false) {
    const attachUrlInput = {
      name: 'input-dialog-attach-url',
      icon: 'link',
      input: {
        ...(includeName) && {name: ''},
        data: '',
        ...(includeComments) && {comments: ''},
        type: 'link',
      },
      props: {
      },
    };
    state.tabs.push(attachUrlInput);
    state.activeTabName = attachUrlInput.name;
    return this;
  },
  edit(attachmentInput) {
    const attachUrlInput = {
      name: attachmentInput.type == 'link' ? 'input-dialog-attach-url' : 'input-dialog-upload-file',
      icon: attachmentInput.type == 'link' ? 'link' : 'file',
      input: {
        ...attachmentInput,
        data: attachmentInput.type == 'file' ? {name: attachmentInput.name} : attachmentInput.data,
      },
    };
    state.tabs.push(attachUrlInput);
    state.activeTabName = attachUrlInput.name;
    return this;
  },
  prompt() {
    if (0 == state.tabs.length) {
      throw Error('InputDialog requires either a file or url to be configured for render');
    }
    return open();
  },
  cancel() {
    close(false);
    reset();
  },
  confirmation(userInput) {
    close(userInput);
    reset();
  },
  delete() {
    close('DELETE');
    reset();
  },
  activeTab() {
    if ('' == state.activeTabName) {
      return undefined;
    }
    return state.tabs.find((tab) => tab.name === state.activeTabName);
  },
  updateActiveTabInput(updatedUserInput) {
    const tab = state.tabs.find((tab) => tab.name === state.activeTabName);
    tab.input = updatedUserInput;
  },
};

