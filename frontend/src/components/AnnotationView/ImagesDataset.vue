<template>
    <div>
        <SectionImage
            v-for="(sectionImage) in this.sectionImages"
            :key="sectionImage.id"
            :imageId="sectionImage.id"
            :dataSet="dataSet"
            :genomicType="genomicType"
            v-bind="$attrs"
        />
    </div>
</template>

<script>
import SectionImage from '@/components/SectionImage.vue';

export default {
  name: 'images-dataset',
  components: {
    SectionImage,
  },
  props: {
    value: {
      type: Array,
      default() {
        return [];
      },
    },
    dataSet: {
      type: String,
    },
    genomicType: {
      type: String,
    },
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
