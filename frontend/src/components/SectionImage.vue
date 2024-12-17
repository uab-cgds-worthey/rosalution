<template>
    <div class="image-row">
      <router-link :to="{
          name: 'file',
          params: {
            file_id: imageId,
          },
        }"
        target="_blank" rel="noreferrer noopener"
      >
        <img class="section-image" :src="imageSrc" data-test="annotation-image" :id="imageId"/>
      </router-link>
      <!-- TODO: Since both AnalysisView and AnnotationView are using this component,
        change the emit to be update-image -->
        <button v-if="this.writePermissions"
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
  name: 'section-image',
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
    writePermissions: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      imageSrc: new URL('/src/assets/rosalution-logo.svg', import.meta.url),
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

.image-row {
  display: flex;
  justify-content: space-between;
  flex-wrap: nowrap;
  align-items: start;
}

.section-image {
  width:100%;
}

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
