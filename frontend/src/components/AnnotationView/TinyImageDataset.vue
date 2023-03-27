<template>
    <div>
        <!-- <img class="section-image" :src="this.sectionImage"/> -->
        <img class="section-image" :src="image"/>
        <!-- <div v-if="areImagesLoaded"></div> -->
    </div>
</template>

<script>
export default {
    name: "tiny-image-dataset",
    props: {
        image: {
            type: String,
        }
    },
    computed: {
        imageSrc() {
            if(!this.image) {
                return "/src/assets/rosalution-logo.svg"
            }
            return this.image
        }
    }
    // data() {
    //     return {
    //         sectionImage: this.image
    //     }
    // },
    // updated() {
    //     sectionImageUpdate()
    // },
    // methods: {
    //     sectionImageUpdate() {
    //         this.sectionImage = this.image
    //     }
    // }
}
</script>