<template>
    <div class="pt-3 pb-2 pl-2 bg-white rounded-xl" style="box-shadow: 0px 2px 5px 0 rgb(0 0 0 / 16%);">
        <div data-test="primary-content"
             style="display: grid; grid-template-columns: 85% 15%; margin-bottom: 0.50rem;">
            <span class="text-xl font-bold">{{ header }}</span>
            <slot></slot>
        </div>
    </div>
</template>

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
