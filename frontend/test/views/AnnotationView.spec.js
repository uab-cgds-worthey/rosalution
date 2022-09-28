import {expect, describe, it, beforeAll, afterAll} from 'vitest';
import {config, shallowMount} from '@vue/test-utils';
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

    wrapper = shallowMount(AnnotationView, {
      props: {...defaultProps},
      global: {
        components: {
          'font-awesome-icon': FontAwesomeIcon,
        },
        mocks: {
          $route: mockRoute,
          $router: mockRouter,
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
});
