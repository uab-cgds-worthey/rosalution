import {expect, describe, it, beforeAll, afterAll} from 'vitest';
import {config, shallowMount} from '@vue/test-utils';

import AnalysisViewHeader from '@/components/AnalysisView/AnalysisViewHeader.vue';

/**
 * helper function that shadllow mounts and returns the rendered component
 * @param {props} props props for testing to overwrite default props
 * @return {VueWrapper} returns a shallow mounted using props
 */
function getMountedComponent(props) {
  const defaultProps = {
    username: '',
    titleText: 'CPAM0002',
    sectionAnchors: ['Brief', 'Summary', 'Medical'],
    actions: ['Action1', 'Action2', 'Action3'],
    third_party_links: [{'type': 'monday_com', 'link': 'https://monday.com'}],
  };

  return shallowMount(AnalysisViewHeader, {
    props: {...defaultProps, ...props},
  });
}

beforeAll(() => {
  config.global.renderStubDefaultSlot = true;
});

afterAll(() => {
  config.global.renderStubDefaultSlot = false;
});

describe('AnalysisViewHeader.vue', () => {
  it('should provide actions to display', () => {
    const wrapper = getMountedComponent();
    expect(wrapper.attributes('actions')).to.equal('Action1,Action2,Action3');
  });

  it('should render an anchor link for each anchor', async () => {
    const wrapper = getMountedComponent();
    const contentWrapper = wrapper.get('div');
    const anchorLinksWrapper = contentWrapper.findAll('a');
    expect(anchorLinksWrapper.length).to.equal(3);
  });

  it('should render an anchor link using the # character for in page anchors', async () => {
    const wrapper = getMountedComponent();
    const anchorLinksWrapper = wrapper.findAll('a');
    const expected = ['#Brief', '#Summary', '#Medical'];

    const actualHrefs = anchorLinksWrapper.map((anchorLink) => {
      return anchorLink.attributes('href');
    });

    for (const expectedAnchorHref of expected) {
      expect(actualHrefs).to.include(expectedAnchorHref);
    }
  });

  it('should render third party links', () => {
    const wrapper = getMountedComponent();

    const mondayLink = wrapper.get('[data-test="monday-link"]');
    expect(mondayLink.attributes('href')).to.equal('https://monday.com');
    expect(mondayLink.attributes('target')).to.equal('_blank');
  });

  it('should not render third party links if null or empty string', () => {
    const wrapper = getMountedComponent({
      third_party_links: [],
    });

    const mondayLink = wrapper.find('[data-test="monday-link"]');
    expect(mondayLink.exists()).to.be.false;
  });
});
