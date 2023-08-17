import {expect, describe, it} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import AnnotationSection from '@/components/AnnotationView/AnnotationSection.vue';

import {FontAwesomeIcon, FontAwesomeLayers} from '@fortawesome/vue-fontawesome';

/**
 * Helper that shallow mounts and returns the rendered component
 * @param {props} props props for testing to overwrite default props
 * @return {VueWrapper} returns a shallow mounted using props
 */
function getMountedComponent(props) {
  const defaultProps = {
    header: 'fake_header',
  };

  return shallowMount(AnnotationSection, {
    props: {...defaultProps, ...props},
    global: {
      components: {
        'font-awesome-icon': FontAwesomeIcon,
        'font-awesome-layers': FontAwesomeLayers,
      },
    },
  });
}

describe('AnnotationSidebar.vue', () => {
  it('should render the header text', () => {
    const wrapper = getMountedComponent();
    expect(wrapper.html()).to.include('fake_header');
  });
});
