import {expect, describe, it, beforeAll, afterAll} from 'vitest';
import {config, shallowMount} from '@vue/test-utils';

import GeneBox from '@/components/AnalysisView/GeneBox.vue';

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';
import {RouterLink} from 'vue-router';

/**
 * helper function that shallow mounts and returns the rendered component
 * @param {props} props props for testing to overwrite default props
 * @return {VueWrapper} returns a shallow mounted using props
 */
function getMountedComponent(props) {
  const defaultProps = {
    name: 'CPAM0046',
    gene: 'LMNA',
    transcripts: [
      {
        transcript: 'NM_170707.3',
      },
    ],
    variants: [
      {
        hgvs_variant: 'NM_170707.3:c.745C>T',
        c_dot: 'c.745C>T',
        p_dot: 'p.R249W',
        build: 'hg19',
        case: [
          {
            field: 'Evidence',
            value: ['PS2', 'PS3', 'PM2', 'PP3', 'PP5'],
          },
          {
            field: 'Interpretation',
            value: ['Pathogenic'],
          },
          {
            field: 'Inheritance',
            value: ['De Novo'],
          },
        ],
      },
    ],
  };

  return shallowMount(GeneBox, {
    props: {...defaultProps, ...props},
    global: {
      components: {
        'font-awesome-icon': FontAwesomeIcon,
        'router-link': RouterLink,
      },
    },
  });
}

beforeAll(() => {
  config.renderStubDefaultSlot = true;
});

afterAll(() => {
  config.renderStubDefaultSlot = false;
});

describe('GeneBox.vue', () => {
  it('should show Gene name', () => {
    const wrapper = getMountedComponent();
    expect(wrapper.text()).to.contains('LMNA');
  });

  it('should show Transcript', () => {
    const wrapper = getMountedComponent();
    expect(wrapper.text()).to.contains('NM_170707.3');
  });

  it('should show c-dot notation', () => {
    const wrapper = getMountedComponent();
    expect(wrapper.text()).to.contains('c.745C>T');
  });

  it('should show p-dot notation', () => {
    const wrapper = getMountedComponent();
    expect(wrapper.text()).to.contains('p.R249W');
  });

  it('should show correct build', () => {
    const wrapper = getMountedComponent();

    const build = wrapper.vm.getBuild('hg19');
    expect(build).toBe('grch37');
    expect(wrapper.text()).to.contains('grch37');
  });

  it('should show field names', () => {
    const wrapper = getMountedComponent();
    expect(wrapper.text()).to.contains('Evidence');
    expect(wrapper.text()).to.contains('Interpretation');
    expect(wrapper.text()).to.contains('Inheritance');
  });

  it('should show values', () => {
    const wrapper = getMountedComponent();
    expect(wrapper.text()).to.contains('PS2, PS3, PM2, PP3, PP5');
  });

  // These two tests need to mock a router in order to be tested
  it.skip('should show annotations view when Gene is clicked', async () => {
    const wrapper = getMountedComponent();
    const gene = wrapper.find('[data-test=gene-name]');

    await gene.trigger('click');
    const annotations = wrapper.find('[data-test=annotations]');
    console.log(annotations);

    expect(annotations.exists()).toBe(true);
  });

  it.skip('should show annotations view when c-dot notation is clicked', async () => {
    const wrapper = getMountedComponent();
    const cDot = wrapper.find('[data-test=c-dot]');

    await cDot.trigger('click');
    const annotations = wrapper.find('[data-test=annotations]');

    expect(annotations.exists()).toBe(true);
  });

  it.skip('should redirect to Genome browser when clicked', async () => {
    const wrapper = getMountedComponent();
    const genomeBrowserButton = wrapper.find('[data-test=genome-browser-button]');

    await genomeBrowserButton.trigger('click');
    /* this needs to change to read webpage */
    // const annotations = wrapper.find('[data-test=annotations]');

    // expect(annotations.exists()).to.equal(true);
  });
});
