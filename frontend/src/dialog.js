import {reactive} from 'vue';

const state = reactive({
  type: 'alert',
  active: false,
  message: '',
  confirmText: 'Ok',
  cancelText: 'Cancel',
  inputType: 'text',
});


// -----------------------------------
// Private Methods
// -----------------------------------
let close;

const dialogPromise = () => new Promise((resolve) => (close = resolve));

const open = (message) => {
  state.message = message;
  state.active = true;
  return dialogPromise();
};

const reset = () => {
  state.active = false;
  state.message = '';
  state.confirmText = 'Ok';
  state.cancelText = 'Cancel';
  state.title = '';
  state.type = 'alert';
};

// -----------------------------------
// Public interface
// -----------------------------------

export default {
  get state() {
    return state;
  },
  title(title) {
    state.title = title;
    return this;
  },
  confirmText(text) {
    state.confirmText = text;
    return this;
  },
  cancelText(text) {
    state.cancelText = text;
    return this;
  },
  inputType(type) {
    state.inputType = type;
    return this;
  },
  alert(message) {
    state.type = 'alert';
    return open(message);
  },
  confirm(message) {
    state.type = 'confirm';
    return open(message);
  },
  cancel() {
    close(false);
    reset();
  },
  confirmation(input = true) {
    input = state.type === 'prompt' ? input : true;
    close(input);
    reset();
  },
};

