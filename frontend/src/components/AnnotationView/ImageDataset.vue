<template>
    <div class="section-image">
        <TinyImageDataset
            v-for="(sectionImage) in this.sectionImages"
            :key="sectionImage.id"
            :imageId="sectionImage.id"
            :dataSet="dataSet"
            v-bind="$attrs"
        />
    </div>
</template>

<script>
import TinyImageDataset from '@/components/AnnotationView/TinyImageDataset.vue';

export default {
  name: 'image-dataset',
  components: {
    TinyImageDataset,
  },
  props: {
    value: {
      type: Object,
      default: [],
    },
    dataSet: {
      type:String,
    }
  },
  computed: {
    sectionImages() {
      const images = [];

      this.value.forEach(async (incomingImage) => {
        const imageToLoad = {id: incomingImage.file_id};
        images.push(imageToLoad);
      });

      return images;
    },
  },
};
</script>

<style>

</style>
