import {expect, describe, it} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import AnnotationSidebar from '@/components/AnnotationView/AnnotationSidebar.vue';

/**
 * Helper that shallow mounts and returns the rendered component
 * @param {props} props props for testing to overwrite default props
 * @return {VueWrapper} returns a shallow mounted using props
 */
function getMountedComponent(props) {
  const defaultProps = {
    sectionAnchors: [
      'Gene',
      'Variant',
      'Gene_Homology',
      'Protein_Expression',
      'Modelability',
      'Model_Systems',
      'Druggability',
    ],
  };

  return shallowMount(AnnotationSidebar, {
    props: {...defaultProps, ...props},
  });
}

describe('AnnotationSidebar.vue', () => {
  it('should render a hyperlink per section anchor', () => {
    const wrapper = getMountedComponent();
    expect(wrapper.findAll('a').length).to.equal(7);
  });

  it('should render a a valid anchor hyperlink per link', () => {
    const wrapper = getMountedComponent();
    const anchorLinks = wrapper.findAll('a');
    anchorLinks.forEach((linkDomElement) => {
      expect(linkDomElement.attributes('href')).to.be.a('string').and.satisfy((href) => href.startsWith('#'));
    });
  });
});
