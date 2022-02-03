import {describe, it, test, expect} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import TextInput from '../../../src/components/FormComponents/TextInput.vue';

test('Vue instance exists and it is an object', () => {
  const wrapper = shallowMount(TextInput);
  expect(typeof wrapper).toBe('object');
});

/**
 * Creates a wrapper with a shallow mount with the default props data or a custom wrapper with the passed in propsData.
 * @param {Object} propsData Custom props data for creating a wrapper
 * @return {Object} vue test utils wrapper for TextInput.vue component
 */
function getMountedComponent(propsData) {
  const defaultPropsData = {
    label: 'Case',
    placeholderText: 'Enter Case Number',
  };

  return shallowMount(TextInput, {
    propsData: {...defaultPropsData, ...propsData},
  });
}

describe('TextInput.vue', () => {
  let wrapper;

  it('renders a vue instance', () => {
    wrapper = getMountedComponent();
    expect(typeof wrapper).toBe('object');
  });

  it('renders a placeholder text', () => {
    wrapper = getMountedComponent();

    const textWrapper = wrapper.find('[placeholder="Enter Case Number"]');
    expect(textWrapper.html()).to.contains('Enter Case Number');
  });

  it('renders a text input box', () => {
    wrapper = getMountedComponent();

    const textWrapper = wrapper.find('[type="text"]');
    expect(textWrapper.attributes().class).to.contains('border-gray-200');
  });
});
