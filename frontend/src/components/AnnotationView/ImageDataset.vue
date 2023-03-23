<template>
    <div>
        <img class="section-image" :src="this.sectionImage"/>
    </div>
</template>

<script>
import Annotations from '@/models/annotations.js';

export default {
    name: 'image-dataset',
    props: {
        value: {
            type: String
        }
    },
    updated() {
        this.fetchImage(this.value);
    },
    data() {
        return {
            sectionImage: ''
        }
    },
    methods: {
        async fetchImage(imageId) {
            if (imageId == '')
                return;
            const image = await Annotations.getAnnotationImage(imageId);
            console.log(image);
            this.sectionImage = image;
        },
    }
}
</script>

<style>
.section-image {
  max-height: 31.25rem;
}
</style>