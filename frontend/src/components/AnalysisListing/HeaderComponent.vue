<template>
    <header class="header">
        <div data-test="primary-content"
             style="display: grid; grid-template-columns: 85% 15%; margin-bottom: 0.50rem;">
            <span class="text-xl font-bold">{{ header }}</span>
        </div>
    </header>
</template>

<style>

header {
  flex-grow: 0;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  gap: 15px;
  padding: 0;
}
</style>

<script>
export default {
  name: 'header-component',
  props: {
    header: {
      type: String,
    },
  },
};
</script>
