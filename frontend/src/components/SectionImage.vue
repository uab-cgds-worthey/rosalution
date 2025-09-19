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
        <img class="section-image" :src="imageSrc" data-test="annotation-image" :id="imageId" @click="getDimensions"/>
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

<script setup>
import {reactive, ref} from 'vue';
import FileRequests from '@/fileRequests.js';

defineEmits(['update-annotation-image']);

const props = defineProps({
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
});

const img = new Image();

img.src = ref(new URL('/src/assets/rosalution-logo.svg', import.meta.url));

img.onload = () => {
  console.log(`the image dimensions are ${img.width}x${img.height}`);
};

const imageSrc = ref(new URL('/src/assets/rosalution-logo.svg', import.meta.url));

const screenWidth = ref(window.innerWidth);
const screenHeight = ref(window.height);

const maxScreenResolution = Math.min(screenWidth, screenHeight);

const styledImage = reactive({
  width: 100% * maxScreenResolution,
  height: 100% * maxScreenResolution,
});

// functions

function getDimensions() {
  console.log('This is the image');
  console.log(img);
  console.log(`the image dimensions are ${img.width}x${img.height}`);
}

async function sectionImageUpdate() {
  const loadingImage = await FileRequests.getImage(props.imageId);
  imageSrc.value = loadingImage;
}

function calculateAspectRatioFit(imgWidth, imgHeight, maxWidth, maxHeight) {
  const ratio = Math.min(maxWidth/imgWidth, maxHeight/imgHeight);
  // return {width: imgWidth*ratio, height: imgHeight*ratio};
  return ratio;
}

sectionImageUpdate();

</script>

<style>

/* html {
  --img-width: .section-image.width;
  --img-height: .section-image.height
  --max-width: 12.5rem;
  --max-height: 12.5rem;
  --ratio: min(var(--img-width)/var(--max-width), var(--img-height)/var(--max-height));
} */

/* img {
  width:
  --org-width: this.imageSrc.naturalWidth
} */

.image-row {
  display: flex;
  justify-content: space-between;
  flex-wrap: nowrap;
  align-items: start;
}

/* .section-image {
  width: calc(100%*calculateAspectRatioFit());
  height: calc(100%*calculateAspectRatioFit());
} */

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
