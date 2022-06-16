import {describe, it, expect, beforeAll, afterAll} from 'vitest';
import {shallowMount} from '@vue/test-utils';
import {nextTick} from 'vue';
import sinon from 'sinon';

import Analyses from '@/models/analyses.js';
import User from '@/models/user.js';
import AnalysisCard from '@/components/AnalysisListing/AnalysisCard.vue';
import AnalysisListingHeader from '@/components/AnalysisListing/AnalysisListingHeader.vue';
import AnalysisListingView from '@/views/AnalysisListingView.vue';


import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

describe('AnalysisListingView', () => {
  let mockedData;
  let mockedUser;
  let wrapper;

  beforeAll(() => {
    mockedData = sinon.stub(Analyses, 'all');
    mockedData.returns(fixtureData());

    mockedUser = sinon.stub(User, 'getUser');
    mockedUser.returns('');

    wrapper = shallowMount(AnalysisListingView, {
      global: {
        components: {
          'font-awesome-icon': FontAwesomeIcon,
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

  it('Contains listing of Analyses', async () => {
    await nextTick();
    const cards = wrapper.findAllComponents(AnalysisCard);
    expect(cards).to.have.lengthOf(4);
  });

  it('Filters analyses by search event from search bar', async () => {
    const searchBarWrapper = wrapper.findComponent(AnalysisListingHeader);
    searchBarWrapper.vm.$emit('search', 'NM_1');

    await nextTick();

    const cards = wrapper.findAllComponents(AnalysisCard);
    expect(cards).to.have.lengthOf(2);
  });
});

/**
 * Generates an array of analyses of rosalution projects to test with
 * @return {Object[]} A listing of anlayses for rosalution
 */
function fixtureData() {
  return [{
    id: '10f7aa04-6adf-4538-a700-ebe2f519473f',
    name: 'CPAM0046',
    description: ': LMNA-related congenital muscular dystropy',
    genomic_units: [
      {gene: 'LMNA'},
      {transcript: 'NM_170707.3'},
      {chromosome: '1', position: '156134885', reference: 'C', alternate: 'T'},
    ],
    nominated_by: 'Dr. Person Two',
    latest_status: 'Approved',
    created_date: '2021-09-30',
    last_modified_date: '2021-10-01',
  },
  {
    id: 'e99def4b-cdb3-4a6b-82f1-e3ab4df37f9f',
    name: 'CPAM0047',
    description: 'Congenital variant of Rett syndrome',
    genomic_units: [
      {gene: 'SBF1'},
      {transcript: 'NM_002972.2'},
      {chromosome: '1', position: '5474', reference: 'T', alternate: 'G'},
    ],
    nominated_by: 'CMT4B3 Foundation',
    latest_status: 'Declined',
    created_date: '2020-12-03',
    last_modified_date: '2021-12-12',
  },
  {
    id: '10342gs4-6adf-4538-a700-ebef319473f',
    name: 'CPAM0053',
    description:
        'Mild Zellweger Spectrum Disorder, a Peroxisome Biogenesis Disorder',
    genomic_units: [
      {gene: 'PEX10'},
      {transcript: 'NM_153818.2'},
      {chromosome: '1', position: '2406528', reference: 'C', alternate: 'G'},
    ],
    nominated_by: 'N/A',
    latest_status: 'Ready',
    created_date: '2021-11-02',
    last_modified_date: '2021-11-23',
  },
  {
    id: '1aeg4-6d32f-4348-a700-ebef334gfsf',
    name: 'CPAM0065',
    description: 'Congenital variant of Rett syndrome',
    genomic_units: [
      {gene: 'FOXG1'},
      {transcript: 'NM_005249.5'},
      {chromosome: '1', position: '924', reference: 'G', alternate: 'A'},
    ],
    nominated_by: 'Believe in a Cure Foundation',
    latest_status: 'Declined',
    created_date: '2020-12-03',
    last_modified_date: '2021-12-12',
  },
  ];
}
