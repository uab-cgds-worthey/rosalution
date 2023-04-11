import {expect, describe, it, beforeAll, afterAll} from 'vitest';
import {config, shallowMount} from '@vue/test-utils';

import AnnotationViewHeader from '@/components/AnnotationView/AnnotationViewHeader.vue';

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';
import {RouterLink} from 'vue-router';

/**
 * Shallow mounts and returns the rendered component
 * @param {props} props props for testing to overwrite default props
 * @return {VueWrapper} returns a shallow mounted using props
 */
function getMountedComponent(props) {
  const defaultProps = {
    username: '',
    analysisName: 'CPAM0004',
    genes: {
      'PEX10': ['NM_153818.2:c.28dup(p.Glu10fs)', 'NM_153818.2:c.928C>G(p.His310Asp)'],
      'LMNA': ['NM_170707.3:c.745C>T(p.R249W)'],
    },
    variants: ['NM_153818.2:c.28dup(p.Glu10fs)', 'NM_153818.2:c.928C>G(p.His310Asp)', 'NM_170707.3:c.745C>T(p.R249W)'],
    activeGenomicUnits: {
      'gene': 'PEX10',
      'variant': 'NM_153818.2:c.28dup(p.Glu10fs)',
    },
    mondayLink: 'https://monday.com',
    phenotipsLink: 'https://phenotips.org',
  };

  return shallowMount(AnnotationViewHeader, {
    props: {...defaultProps, ...props},
    global: {
      components: {
        'font-awesome-icon': FontAwesomeIcon,
        'router-link': RouterLink,
      },
      stubs: {
        RouterLink: true,
        FontAwesomeIcon: true,
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

describe('AnnotationViewHeader.vue', () => {
  it('should provide no actions to display', () => {
    const wrapper = getMountedComponent();
    expect(wrapper.attributes('actions')).to.be.empty;
  });

  it('should emit changed event when a new variant is selected in the same gene', () => {
    const wrapper = getMountedComponent();

    const variantSelectComponent = wrapper.getComponent('[class="variant-unit-select"]');
    variantSelectComponent.vm.$emit('update:selected', 'NM_153818.2:c.928C>G(p.His310Asp)');

    const changedEvent = wrapper.emitted('changed');
    expect(changedEvent.length).to.equal(1);
    const changedActiveGenomicUnits = changedEvent[0][0];
    expect(changedActiveGenomicUnits.gene).to.equal('PEX10');
    expect(changedActiveGenomicUnits.variant).to.equal('NM_153818.2:c.928C>G(p.His310Asp)');
  });

  it('should emit changed event when a new variant is selected in a different gene', () => {
    const wrapper = getMountedComponent();

    const variantSelectComponent = wrapper.getComponent('[class="variant-unit-select"]');
    variantSelectComponent.vm.$emit('update:selected', 'NM_170707.3:c.745C>T(p.R249W)');

    const changedEvent = wrapper.emitted('changed');
    expect(changedEvent.length).to.equal(1);
    const changedActiveGenomicUnits = changedEvent[0][0];
    expect(changedActiveGenomicUnits.gene).to.equal('LMNA');
    expect(changedActiveGenomicUnits.variant).to.equal('NM_170707.3:c.745C>T(p.R249W)');
  });

  it('should emit changed event when a new gene is selected', () => {
    const wrapper = getMountedComponent();

    const geneSelectComponent = wrapper.getComponent('[class="gene-unit-select"]');
    geneSelectComponent.vm.$emit('update:selected', 'LMNA');

    const changedEvent = wrapper.emitted('changed');
    expect(changedEvent.length).to.equal(1);
    const changedActiveGenomicUnits = changedEvent[0][0];
    expect(changedActiveGenomicUnits.gene).to.equal('LMNA');
    expect(changedActiveGenomicUnits.variant).to.equal('NM_170707.3:c.745C>T(p.R249W)');
  });

  it('should not emit changed event when the same variant', () => {
    const wrapper = getMountedComponent();

    const variantSelectComponent = wrapper.getComponent('[class="variant-unit-select"]');
    variantSelectComponent.vm.$emit('update:selected', 'NM_153818.2:c.28dup(p.Glu10fs)');

    expect(wrapper.emitted('changed'), 'the "changed" event happened').to.be.undefined;
  });

  it('should not emit changed event when the same gene is selected', () => {
    const wrapper = getMountedComponent();

    const geneSelectComponent = wrapper.getComponent('[class="gene-unit-select"]');
    geneSelectComponent.vm.$emit('update:selected', 'PEX10');

    expect(wrapper.emitted('changed'), 'the "changed" event happened').to.be.undefined;
  });

  it('should render third party links', () => {
    const wrapper = getMountedComponent();

    const mondayLink = wrapper.get('[data-test="monday-link"]');
    expect(mondayLink.attributes('href')).to.equal('https://monday.com');
    expect(mondayLink.attributes('target')).to.equal('_blank');

    const phenotipsLink = wrapper.get('[data-test="phenotips-link"]');
    expect(phenotipsLink.attributes('href')).to.equal('https://phenotips.org');
    expect(phenotipsLink.attributes('target')).to.equal('_blank');
  });

  it('should not render third party links if null or empty string', () => {
    const wrapper = getMountedComponent({
      mondayLink: null,
      phenotipsLink: '',
    });

    const mondayLink = wrapper.find('[data-test="monday-link"]');
    expect(mondayLink.exists()).to.be.false;

    const phenotipsLink = wrapper.find('[data-test="phenotips-link"]');
    expect(phenotipsLink.exists()).to.be.false;
  });
});
