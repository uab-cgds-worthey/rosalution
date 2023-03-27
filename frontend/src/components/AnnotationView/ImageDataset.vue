<template>
    <div>
        <!-- <img class="section-image" :src="this.sectionImage"/> -->
        <!-- <img
            v-for="(sectionImage, index) in sectionImages"
            class="section-image"
            :src="sectionImage.image_src"
            :key="sectionImage.id"
        /> -->
        <!-- <div v-if="areImagesLoaded"></div> -->

        <TinyImageDataset
            v-for="(sectionImage, index) in this.sectionImages"
            :key="sectionImage.id + sectionImage.image_src ? '_found': '_notFound'"
            :image="sectionImage.image_src"
        />
    </div>
</template>

<script>
import Annotations from '@/models/annotations.js';
import TinyImageDataset from '@/components/AnnotationView/TinyImageDataset.vue';

export default {
    name: 'image-dataset',
    components: {
        TinyImageDataset,
    },
    props: {
        value: {
            type: Array,
            default: []
        },
    },
    computed: {
        // areImagesLoaded() {
        //     let images = this.sectionImages;
        //     const notLoadedImages = images.filter(image => image.image_src == "/src/assets/rosalution-logo.svg")
        //     return notLoadedImages.length > 0
        // },
        sectionImages() {
            console.log('computed section images is called!')
            let images = [];

            this.value.forEach(async incoming_image => {
                const imageToLoad = {
                    id: incoming_image.file_id,
                    onLoad: async function(component, loadingImage) {
                        console.log('sit!')
                        loadingImage.image_src = await Annotations.getAnnotationImage(incoming_image.file_id)
                        console.log('osuwari!')
                        console.log(component);
                    }
                }
                images.push(imageToLoad);
                imageToLoad.onLoad(this, imageToLoad);
            });
            return images;
        }
        //     // images
        //     // this.value.forEach( async incoming_image => {
        //     //     const loaded_image = ;
        //     //     this.sectionImages.filter(section_image => section_image.id === incoming_image.file_id).forEach(matched_image => matched_image.image_src = loaded_image )
        //     // })

        //     // return 
        // }
    },
    // created() {
    //     this.value.forEach(async incoming_image => {
    //         Annotations.getAnnotationImage(incoming_image.file_id)
    //             images.push(imageToLoad);
    //             imageToLoad.onLoad(this, imageToLoad);
    //         });
    // },
    // data() {
    //     return {
    //         sectionImages: []
    //     }
    // },
    // methods: {
    //     imageDatasetOnLoad(imageSrc) {
    //         this.sectionImages.push(imageSrc)
    //     }
    // }
}
    // created() {
    //     console.log('updated is called!')
    //     console.log(this.value);
    //     let images = [];

    //     this.value.forEach(async incoming_image => {
    //         images.push({
    //             id: incoming_image.file_id,
    //             image_src: "@/assets/rosalution-logo.svg"
    //         });
    //     });

    //     this.sectionImages.length = 0;
    //     this.sectionImages = [...images];
    //     console.log("loaded empty images first")
    //     this.value.forEach( async incoming_image => {
    //         console.log(incoming_image);
    //         console.log('atempting to load')
    //         const loaded_image = await Annotations.getAnnotationImage(incoming_image.file_id);
    //         this.sectionImages.filter(section_image => section_image.id === incoming_image.file_id).forEach(matched_image => matched_image.image_src = loaded_image )
    //         console.log('replaced image' + incoming_image.file_id)
    //     })
    //     console.log('finished the mo0unted function')
    // }
    // },
    // methods: {
    //     async fetchImage(imageIds) {
    //         if (imageIds == [])
    //             return;
            
    //         let images = [];

    //         // for(let imageId in imageIds) {
    //         //     console.log(imageId)
    //         // }

    //         imageIds.forEach(async imageId => {
    //             const image = await Annotations.getAnnotationImage(imageId);
    //             images.push(image);
    //         });

    //         this.sectionImages = images;
    //     },
    // }

</script>

<style>
.section-image {
  max-height: 31.25rem;
}
</style>