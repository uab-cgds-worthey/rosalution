import {expect, describe, it} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import ImageDataset from '@/components/AnnotationView/ImageDataset.vue';
import TinyImageDataset from '@/components/AnnotationView/TinyImageDataset.vue';

/**
    * Creates a shallow mount for the vue component.
    * @param {Object} propsData Mocked props data
    * @return {Object} shallowMount to be used
*/
function getMountedComponent(propsData) {
    const defaultPropsData = {
        value: [
            {file_id: 'fake-file-id-1', created_date: '1979-01-01 00:00:00.029728'},
            {file_id: 'fake-file-id-2', created_date: '1979-01-01 00:00:00.627261'},
            {file_id: 'fake-file-id-3', created_date: '1979-01-01 00:00:00.653973'},
            {file_id: 'fake-file-id-4', created_date: '1979-01-01 00:00:00.901430'},
        ],
        dataSet: 'Fake Dataset Section',
    }

    return shallowMount(ImageDataset, {
        propsData: {...defaultPropsData, ...propsData}
    })
};

describe('ImageDataset.vue', () => {
    let wrapper;

    it('Should render TinyImageDatasets with the given props data', () => {
        wrapper = getMountedComponent();

        const sections = wrapper.findAllComponents(TinyImageDataset);
        expect(sections.length).to.equal(4);
    });

    it('Should not render TinyImageDatasets if the props are empty', () => {
        wrapper = getMountedComponent({value: []});

        const sections = wrapper.findAllComponents(TinyImageDataset);
        expect(sections.length).to.equal(0);
    });
});