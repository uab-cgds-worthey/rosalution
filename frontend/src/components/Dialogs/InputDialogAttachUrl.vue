<template>
 <input v-if="'name' in userInput"
    placeholder="Text to display (required)"
    v-model="name"
    data-test="name-input"
  />
  <input
    placeholder="Paste a link (required)"
    v-model="url"
    data-test="link-input"
  />
  <textarea v-if="'comments' in userInput"
    class="comments"
    placeholder="Comments"
    v-model="comments"
    data-test="comments-text-area"
  >
  </textarea>
</template>

<script>
export default {
  name: 'input-dialog-attach-url',
  emits: ['update:userInput'],
  props: {
    userInput: {
      type: Object,
      required: true,
    },
  },
  computed: {
    name: {
      get() {
        return this.userInput.name;
      },
      set(value) {
        const input = this.userInput;
        input['name'] = value;
        this.$emit('update:userInput', input);
      },
    },
    url: {
      get() {
        return this.userInput.data;
      },
      set(value) {
        const input = this.userInput;
        input['data'] = value;
        this.$emit('update:userInput', input);
      },
    },
    comments: {
      get() {
        return this.userInput['comments'];
      },
      set(value) {
        const input = this.userInput;
        input['comments'] = value;
        this.$emit('update:userInput', input);
      },
    },
  },
};
</script>

<style>

.comments {
  flex: 3 0 auto;
  height: 8rem;
}

</style>
