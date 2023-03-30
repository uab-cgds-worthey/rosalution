<template>
    <div class="section-image">
        <TinyImageDataset
            v-for="(sectionImage, index) in this.sectionImages"
            :key="sectionImage.id"
            :image="sectionImage.id"
            :genomicUnitType="genomicUnitType"
            :sectionLabel="sectionLabel"
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
            type: Array,
            default: []
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
    created() {
        console.log(this.label)
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

<style>

</style>