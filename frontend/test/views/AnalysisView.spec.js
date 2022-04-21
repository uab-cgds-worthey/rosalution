import {expect, describe, it, beforeAll, afterAll} from 'vitest';
import {shallowMount} from '@vue/test-utils';
import sinon from 'sinon';

import Analyses from '@/models/analyses.js';
import AnalysisView from '@/views/AnalysisView.vue';

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

describe('AnalysisView', () => {
  let mockedData;
  let wrapper;

  const mockRoute = {
    params: {
      id: 1,
    },
  };

  const mockRouter = {
    push: sinon.spy(),
  };

  beforeAll( () => {
    mockedData = sinon.stub(Analyses, 'getAnalysis');
    mockedData.returns(fixtureData());

    const defaultProps = {analysis_name: 'CPAM0046'};

    wrapper = shallowMount(AnalysisView, {
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
    mockedData.restore();
  });

  it('Vue instance exists and it is an object', () => {
    expect(typeof wrapper).toBe('object');
  });

  it('Analysis Listing contains a header and content', () => {
    const appHeader = wrapper.find('app-header');
    expect(appHeader.exists()).toBe(true);

    const appContent = wrapper.find('app-content');
    expect(appContent.exists()).toBe(true);
  });

  it('Contains Analysis Name', () => {
    const analysisName = wrapper.find('[data-test=analysis-name]');
    expect(analysisName.text()).to.contain('CPAM0046');
  });
});

/**
 * Returns fixture data
 * @return {Object} containing analysis data for CPAM0046.
 */
function fixtureData() {
  return {
    id: '10f7aa04-6adf-4538-a700-ebe2f519473f',
    name: 'CPAM0046',
    description: 'LMNA-related congenital muscular dystropy',
  };
}
