<template>
    <div>
        <TinyImageDataset
            v-for="(sectionImage, index) in this.sectionImages"
            :key="sectionImage.id"
            :image="sectionImage.id"
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
            type: Array,
            default: []
        },
        genomic_unit_type: {
            type: String,
        }
    },
    computed: {
        sectionImages() {
            let images = [];

            this.value.forEach(async incoming_image => {
                const imageToLoad = { id: incoming_image.file_id }
                images.push(imageToLoad);
            });

            return images;
        }
    }
}
</script>
