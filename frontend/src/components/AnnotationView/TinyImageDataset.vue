<template>
    <div>
        <img class="section-image" :src="imageSrc"/>
        <button class="edit-icon" @click="$emit('edit-image')" data-test="edit-icon">
          <font-awesome-icon :icon="['fa', 'pencil']" size="xl" />
        </button>
    </div>
</template>

<script>
import fileRequests from '@/fileRequests.js'

export default {
    name: "tiny-image-dataset",
    props: {
        image: {
            type: String,
        }
    },
    data() {
        return {
            imageSrc: "/src/assets/rosalution-logo.svg"
        }
    },
    created() {
        console.log(this.image);
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