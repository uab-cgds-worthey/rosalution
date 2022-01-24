<template>
  <div class="py-1.5">
    <span class="text-lg text-left">{{ label }} </span>
    <input
      type="text"
      :placeholder="placeholderText"
      class="text-lg border border-solid border-gray-200 placeholder-gray-300 w-60 rounded-md text-center"
      >
  </div>
</template>

<script>
export default {
  name: 'text-input',
  props: {
    label: {
      default: '',
      type: String,
    },
    placeholderText: {
      default: '',
      type: String,
    },
  },
};
</script>


<style scoped>
@tailwind base;
@tailwind components;
@tailwind utilities;
@import url("https://use.typekit.net/rgh1osc.css");

div {
  font-family: "Proxima Nova", sans-serif;
  padding: 0%;
}


</style>
