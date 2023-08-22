import {expect, describe, it, beforeAll, afterAll} from 'vitest';
import {config, shallowMount} from '@vue/test-utils';

import FileRequests from '@/fileRequests.js';

import SectionImage from '@/components/SectionImage.vue';

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';
import {RouterLink} from 'vue-router';

import sinon from 'sinon';

/**
    * Creates a shallow mount for the vue component.
    * @param {Object} propsData Mocked props data
    * @return {Object} shallowMount to be used
*/
function getMountedComponent(propsData) {
  const defaultPropsData = {
    imageId: 'fake-image-id-1',
    dataSet: 'Fake Dataset Section',
    writePermissions: true,
  };

  return shallowMount(SectionImage, {
    props: {...defaultPropsData, ...propsData},
    global: {
      components: {
        'font-awesome-icon': FontAwesomeIcon,
        'router-link': RouterLink,
      },
    },
  });
}


beforeAll(() => {
  config.global.renderStubDefaultSlot = true;
});

afterAll(() => {
  config.global.renderStubDefaultSlot = false;
});

describe('SectionImage.vue', () => {
  let sandbox;
  let getImageMock;

  beforeAll(() => {
    sandbox = sinon.createSandbox();
    getImageMock = sandbox.stub(FileRequests, 'getImage');
    getImageMock.returns('fake-image-data-from-mongo');
  });

  afterAll(() => {
    sandbox.restore();
  });

  it('Should display a placeholder image if image has not been fetched from mongo', () => {
    const imagePlaceholderPath = '/src/assets/rosalution-logo.svg';

    const wrapper = getMountedComponent();
    const annotationImage = wrapper.find('[data-test=annotation-image]');

    expect(annotationImage.html()).toContain(imagePlaceholderPath);
  });

  it('Should display image data that has been retrieved from mongo', async () => {
    const wrapper = getMountedComponent();
    const annotationImage = wrapper.find('[data-test=annotation-image]');

    await wrapper.vm.$nextTick();

    expect(annotationImage.html()).toContain('fake-image-data-from-mongo');
  });

  it('Should emit an update-annotation-image event when the edit icon is clicked', async () => {
    const wrapper = getMountedComponent();
    const editAnnotationImageButton = wrapper.find('[data-test=annotation-edit-icon]');

    await editAnnotationImageButton.trigger('click');

    const emittedObjects = wrapper.emitted()['update-annotation-image'][0];

    expect(emittedObjects[0]).to.equal('fake-image-id-1');
    expect(emittedObjects[1]).to.equal('Fake Dataset Section');
  });
});
