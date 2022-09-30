import {expect, describe, it, beforeAll, afterAll} from 'vitest';
import {config, mount} from '@vue/test-utils';
import sinon from 'sinon';

import Auth from '@/models/authentication.js';

import AnnotationView from '@/views/AnnotationView.vue';
import AnnotationSection from '@/components/AnnotationView/AnnotationSection.vue';
import AnnotationViewHeader from '@/components/AnnotationView/AnnotationViewHeader.vue';
import TextDataset from '@/components/AnnotationView/TextDataset.vue';

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

describe('AnnotationView', () => {
  let wrapper;
  // Future Mock Analyis Annotation Rendering Configuration
  // Future Mock Annotations for Active Gene and Variant being analyzed
  let mockedUser;

  const mockRoute = {
    params: {
      id: 1,
    },
  };

  const mockRouter = {
    push: sinon.spy(),
  };
  let sandbox;

  beforeAll(() => {
    config.renderStubDefaultSlot = true;
    sandbox = sinon.createSandbox();

    const defaultProps = {
      analysis_name: 'CPAM0046',
    };

    mockedUser = sandbox.stub(Auth, 'getUser');
    mockedUser.returns('');

    wrapper = mount(AnnotationView, {
      props: {...defaultProps},
      global: {
        components: {
          'font-awesome-icon': FontAwesomeIcon,
        },
        mocks: {
          $route: mockRoute,
          $router: mockRouter,
        },
        stubs: {
          AnnotationViewHeader: true,
          FontAwesomeIcon: true,
        },
      },
    });
  });

  afterAll(() => {
    config.renderStubDefaultSlot = false;
    // mockedData.restore();
  });

  it('contains a header with the analysis name', () => {
    const headerComponent = wrapper.findComponent(AnnotationViewHeader);
    expect(headerComponent.props('titleText')).to.equal('CPAM0046');
  });

  it('renders expected number of sections ', () => {
    const sections = wrapper.findAllComponents(AnnotationSection);
    expect(sections.length).to.equal(7);
  });

  it('renders each section with an Id to be used for an achor', () => {
    const sections = wrapper.findAllComponents(AnnotationSection);
    sections.forEach((section) => {
      expect(section.attributes('id')).to.not.be.empty;
    });
  });

  it('renders text datasets according to configuration', () => {
    const textDatasets = wrapper.findAllComponents(TextDataset);
    expect(textDatasets.length).to.equal(3);
  });

  describe('Section headers ought to render datasets according to configuration', () => {
    let geneSection;
    let geneSectionHeader;
    let linkoutElements;

    beforeAll(() => {
      geneSection = wrapper.find('#Gene');
      geneSectionHeader = geneSection.get('.annotations');
      linkoutElements = geneSectionHeader.findAll('a');
    });

    it('should render each header dataset', () => {
      expect(linkoutElements.length).to.equal(3);
    });

    it('should not render any linkouts if none provided', () => {
      const variantSection = wrapper.find('#Variant');
      const variantSectionHeader = variantSection.get('.annotations');
      const noLinkouteElements = variantSectionHeader.findAll('a');
      expect(noLinkouteElements.length).to.equal(0);
    });

    it('should render each linkout to open in a new tab', () => {
      linkoutElements.forEach((linkDomElement) => {
        expect(linkDomElement.attributes('target')).to.equal('_blank');
      });
    });

    it('should render each linkout with an href', () => {
      linkoutElements.forEach((linkDomElement) => {
        expect(
            ['https://search.clinicalgenome.org/kb/genes/HGNC:22082',
              'https://www.ncbi.nlm.nih.gov/gene?Db=gene&Cmd=DetailsSearch&Term=203547',
              'https://gnomad.broadinstitute.org/gene/ENSG00000160131?dataset=gnomad_r2_1',
            ]).to.include(linkDomElement.attributes('href'));
      });
    });
  });
});
