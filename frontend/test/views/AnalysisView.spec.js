import {expect, describe, it, beforeAll, afterAll} from 'vitest';
import {shallowMount} from '@vue/test-utils';
import sinon from 'sinon';

import Analyses from '@/models/analyses.js';

import AnalysisView from '@/views/AnalysisView.vue';

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

describe('AnalysisView', () => {
  let mockedData;
  let mockedUser;
  let wrapper;

  const mockRoute = {
    params: {
      id: 1,
    },
  };

  const mockRouter = {
    push: sinon.spy(),
  };

  beforeAll(() => {
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

  it('Analysis view contains a header and content', () => {
    const appHeader = wrapper.find('app-header');
    expect(appHeader.exists()).toBe(true);

    const appContent = wrapper.find('app-content');
    expect(appContent.exists()).toBe(true);
  });

  it('Analysis view provides the expected headings of sections to be used as anchors to header', () => {
    const headerComponent = wrapper.get('[data-test="analysis-view-header"]');
    expect(headerComponent.attributes('sectionanchors'))
        .to.equal('Brief,Medical Summary,Case Information,Supplemental Attachments');
  });
});

/**
 * Returns fixture data
 * @return {Object} containing analysis data for CPAM0046.
 */
function fixtureData() {
  return {
    name: 'CPAM0046',
    description: ': LMNA-related congenital muscular dystropy',
    nominated_by: 'Dr. Person Two',
    latest_status: 'Approved',
    created_date: '2021-09-30',
    last_modified_date: '2021-10-01',
    genomic_units: [{
      gene: 'LMNA',
      transcripts: [{transcript: 'NM_170707.3'}],
      variants: [{
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
      }],
    }],
    sections: [{
      header: 'Brief',
      content: [
        {
          field: 'Nominated',
          value: [
            'Dr. Person Two (Local) - working with Dr. Person Three in Person Four Lab',
          ],
        },
        {
          field: 'Reason',
          value: [
            'Contribute a dominant negative patient-variant model to the existing zebrafish model (LOF; in-progress)',
            'Will be used in NBL 240: a research-based undergraduate course at UAB',
          ],
        },
        {
          field: 'Desired Outcomes',
          value: ['Functional impact confirmation (animal/cell modeling)'],
        },
      ],
    }, {
      header: 'Medical Summary',
      content: [
        {
          field: 'Clinical Diagnosis',
          value: ['LMNA-related congenital muscular dystropy'],
        },
        {
          field: 'Affected Individuals Identified',
          value: ['Male, YOB: 2019'],
        },
      ],
    }, {
      header: 'Case Information',
      content: [{
        field: 'Systems',
        value: ['Growth Parameters; Craniofacial; Musculoskeletal; Gastrointestinal; Behavior, Cognition;'],
      }, {
        field: 'HPO Terms',
        value: ['HP:0001508; HP:0001357; HP:0000473; HP:0003560; HP:0003701; HP:0009062; HP:0012389; HP: 0003236;'],
      }, {
        field: 'Additional Details',
        value: [
          'Review of VUSes (Why not considered)',
          'NEB (NM_001164508.1)  | c.7385C>G (p.A2462G) (Pat.) and c.16625A>G (p.H5542R) (Mat.). ',
          'LYZL6 (NM_020426.2)  | c.228G>C (p.Q76H) (Mat./Pat.) - Lysozyme Like 6. - No currently known disease',
          'NOL6 (NM_022917.4)  | c.518G>A (p.R173Q) (Pat.) and c.91G>A (p.G31R) (Mat.). - Nucleolar protein 6. -',
        ],
      }, {
        field: 'Experimental Design',
        value: [],
      }, {
        field: 'Prior Testing',
        value: ['WES - February  2020;'],
      }],
    }],
  };
}
