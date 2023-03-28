<template>
    <div>
        <img class="section-image" :src="imageSrc"/>
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