<template>
    <div>
        <img class="section-image" :src="imageSrc" data-test="annotation-image"/>
        <button
          class="edit-icon"
          @click="$emit('update-annotation-image', imageId, dataSet, genomicType)"
          data-test="annotation-edit-icon"
        >
          <font-awesome-icon :icon="['fa', 'pencil']" size="xl" />
        </button>
    </div>
</template>

<script>
import FileRequests from '@/fileRequests.js';

export default {
  name: 'tiny-image-dataset',
  emits: ['update-annotation-image'],
  props: {
    imageId: {
      type: String,
    },
    dataSet: {
      type: String,
      default: '',
    },
    genomicType: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      imageSrc: '/src/assets/rosalution-logo.svg',
    };
  },
  created() {
    this.sectionImageUpdate();
  },
  methods: {
    async sectionImageUpdate() {
      const loadingImage = await FileRequests.getImage(this.imageId);
      this.imageSrc = loadingImage;
    },
  },
};
</script>

<style>
.edit-icon {
  color: var(--rosalution-purple-300);
  background: none;
  border: none;
  float: right;
  cursor: pointer;
  margin-top: var(--p-5);
  margin-right: var(--p-5);
}
</style>
