<template>
    <div>
        <div>
            <input placeholder="Text to display" id="textBox" @change="onChanged" v-model="linkNameUploaded"
            data-test="link-name-input"/>
        </div>
        <div>
            <input placeholder="Paste a link" id="linkBox" @change="onChanged" v-model="linkUploaded"
            data-test="link-input"/>
        </div>
        <div>
            <textarea placeholder="Comments" id="commentsBox" @change="onChanged" v-model="comments"
            data-test="comments-text-area">
            </textarea>
        </div>
    </div>
</template>

<script>
export default {
  name: 'supplemental-load-link',
  data() {
    return {
      linkNameUploaded: '',
      linkUploaded: '',
      comments: '',
    };
  },
  methods: {
    onChanged() {
      const changedLink = {
        name: this.linkNameUploaded,
        link: this.linkUploaded,
        comment: this.comments,
      };
      this.$emit('changed', changedLink);
    },
  },
};
</script>

<style scoped>
#textBox {
    display: inline-block;
    padding: 1rem;
    margin: 1rem 1rem .5rem 1rem;
    border-style: solid;
    border-color: var(--rosalution-grey-100);
    border-radius: 7px;
    border-width: 1px;
    width: 24rem;
    height: .75rem;
    outline: none;
    resize: none;
    font-family: "Proxima Nova", sans-serif;
    text-align: left;
    font-size: 1.125rem;
}

#linkBox {
    display: inline-block;
    padding: 1rem;
    margin: .5rem 1rem 1rem 1rem;
    border-style: solid;
    border-color: var(--rosalution-grey-100);
    border-radius: 7px;
    border-width: 1px;
    width: 24rem;
    height: .75rem;
    outline: none;
    resize: none;
    font-family: "Proxima Nova", sans-serif;
    text-align: left;
    font-size: 1.125rem;
}

#commentsBox {
  display: block;
  padding: 1rem;
  margin: 1rem;
  border-style: solid;
  border-color: var(--rosalution-grey-100);
  border-radius: 7px;
  width: 24rem;
  height: 6.5rem;
  outline: none;
  resize: none;
  font-family: "Proxima Nova", sans-serif;
  text-align: left;
  font-size: 1.125rem;
}

input::placeholder {
  color: var(--rosalution-grey-200);
}

textarea::placeholder {
  color: var(--rosalution-grey-200);
}
</style>
