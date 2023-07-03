import {expect, describe, it, beforeAll, afterAll, vi} from 'vitest';
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
  config.global.renderStubDefaultSlot = true;
});

afterAll(() => {
  config.global.renderStubDefaultSlot = false;
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

    // const build = wrapper.vm.getBuild('hg19');
    expect(wrapper.vm.getBuild('hg19')).toBe('grch37');
    expect(wrapper.vm.getBuild('hg38')).toBe('grch38');
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

  /*
  this test will need to be modified when the copy functionality is added
  copy method needs to be changed to navigator.clipboard.writeText(textToCopy);
  */
  it('should log text to console when copy button is clicked', async () => {
    const wrapper = getMountedComponent();

    const copyButton = wrapper.find('[data-test=copy-button]');
    vi.spyOn(console, 'log');
    await copyButton.trigger('click');
    expect(console.log).toHaveBeenCalled();
  });

  it('should route to annotations for a gene', async () => {
    const wrapper = getMountedComponent();
    const gene = wrapper.findComponent('[data-test=gene-route]');

    expect(gene.props('to').name).to.equal('annotation');
    expect(gene.props('to').props.analysis_name).to.equal('CPAM0046');
    expect(gene.props('to').props.gene).to.equal('LMNA');
  });

  it('should route to annotations for a variant in the anlaysis', async () => {
    const wrapper = getMountedComponent();
    const variant = wrapper.findComponent('[data-test=variant-route]');

    expect(variant.props('to').name).to.equal('annotation');
    expect(variant.props('to').props.analysis_name).to.equal('CPAM0046');
    expect(variant.props('to').props.gene).to.equal('LMNA');
    expect(variant.props('to').props.variant).to.equal('NM_170707.3:c.745C>T(p.R249W)');
  });
});
