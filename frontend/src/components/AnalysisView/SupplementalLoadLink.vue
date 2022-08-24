<template>
    <div>
        <div>
            <input placeholder="Text to display" id="textBox" @change="onTextChange"
            v-model="linkNameUploaded"
            data-test="link-name-input"/>
        </div>
        <div>
            <input placeholder="Paste a link" id="linkBox" @change="onLinkChange" v-model="linkUploaded"
            data-test="link-input"/>
        </div>
        <div>
            <textarea placeholder="Comments" id="commentsBox" @change="onCommentChange" v-model="comments"
            data-test="comments-text-area">
            </textarea>
        </div>
    </div>
</template>

<script>
export default {
  name: 'supplemental-load-file',
  data() {
    return {
      linkNameUploaded: '',
      linkUploaded: '',
      comments: '',
    };
  },
  methods: {
    onTextChange() {
      this.$emit('linknameadded', this.linkNameUploaded);
    },
    onLinkChange() {
      this.$emit('linkadded', this.linkUploaded);
    },
    onCommentChange() {
      this.$emit('commentadded', this.comments);
    },
    remove(i) {
      this.linkUploaded = '';
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

h2 {
    float: left;
    margin: 0%;
    text-align: left;
    display: block;
}

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

span {
  display: block;
  overflow: hidden;
  padding: 0px 4px 0px 6px;
}

input[type=file]::file-selector-button {
  border: none;
}

#browseBtn {
  display: inline-block;
  background-color: white;
  color: #19A3CF;
  border-bottom: 2px solid #19A3CF;
  font-family: sans-serif;
  cursor: pointer;
  margin-top: 1rem;
}

[v-cloak] {
  display: none;
}

#fileName {
  display: inline-block;
  text-align: center;
  vertical-align: middle;
  padding: 1rem;
  margin: 0%;
}

#removeBtn {
  border-radius: 9999px;
  border-color: black;
  border-width: thin;
  background-color: #e7e7e7;
  display: inline-block;
  font-weight: 500;
  text-align: center;
}

</style>
