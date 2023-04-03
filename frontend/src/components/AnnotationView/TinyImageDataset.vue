<template>
    <div>
        <img class="section-image" :src="imageSrc"/>
        <button class="edit-icon" @click="$emit('update-annotation-image', image, sectionLabel, genomicUnitType)" data-test="edit-icon">
          <font-awesome-icon :icon="['fa', 'pencil']" size="xl" />
        </button>
    </div>
</template>

<script>
import fileRequests from '@/fileRequests.js'

export default {
    name: "tiny-image-dataset",
    emits: ['update-annotation-image'],
    props: {
        image: {
            type: String,
        },
        sectionLabel: {
            type: String,
            default: ''
        },
        genomicUnitType: {
            type: String,
            default: ''
        }
    },
    data() {
        return {
            imageSrc: "/src/assets/rosalution-logo.svg"
        }
    },
    created() {
        this.sectionImageUpdate();
    },
    methods: {
        async sectionImageUpdate() {
            const loadingImage = await fileRequests.getImage(this.image)
            this.imageSrc = loadingImage;
        }
    }
}
</script>

<style>
.edit-icon {
  color: var(--rosalution-purple-300);
  background: none;
  border: none;
  float: right;
  cursor: pointer;
  margin-top: 5px;
  margin-right: 5px;
}
</style>