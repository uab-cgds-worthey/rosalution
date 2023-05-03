import {reactive} from 'vue';

const state = reactive({
  type: 'info',
  active: false,
  message: '',
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
  state.type = 'info';
};

// -----------------------------------
// Public interface
// -----------------------------------

export default {
  get state() {
    return state;
  },
  success(message) {
    state.type = 'success';
    return open(message);
  },
  info(message) {
    state.type = 'info';
    return open(message);
  },
  error(message) {
    state.type = 'error';
    return open(message);
  },
  cancel() {
    close();
    reset();
  },
};

