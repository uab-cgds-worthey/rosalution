<template>
    <dt>
      <a :href="linkout"
        class="dataset-label"
        :class="isLinkoutAvailable ? 'dataset-label-available' : 'dataset-label-unavailable'"
        data-test="text-label"
        target="_blank" rel="noreferrer noopener"
        style="font-size: 1.25rem;"
      >
        {{ label }}
      </a>
      <font-awesome-icon v-if="isLinkoutAvailable" icon="up-right-from-square" size="2xs"/>
    </dt>
    <dd></dd>
</template>

<script>
export default {
  name: 'clinvar-dataset',
  props: {
    label: {
      type: String,
    },
    linkout: {
      type: String,
      required: false,
    },
    value: {
      type: [String, Array],
      default: () => {
        return [];
      },
    },
  },
  computed: {
    isDataAvailable: function() {
      return !(this.value == '.' || this.value == 'null' || this.value == null || typeof(this.value) != 'undefined');
    },
    isLinkoutAvailable() {
      return typeof(this.linkout) !== 'undefined';
    },
  },
};
</script>
