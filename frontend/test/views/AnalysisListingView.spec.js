import {describe, it, expect, beforeAll, afterAll} from 'vitest';
import {shallowMount} from '@vue/test-utils';
import sinon from 'sinon';

import Analyses from '@/models/analyses.js';
import AnalysisCard from '@/components/AnalysisListing/AnalysisCard.vue';
import AnalysisCreateCard from '@/components/AnalysisListing/AnalysisCreateCard.vue';
import AnalysisListingHeader from '@/components/AnalysisListing/AnalysisListingHeader.vue';
import AnalysisListingView from '@/views/AnalysisListingView.vue';

import NotificationDialog from '@/components/Dialogs/NotificationDialog.vue';

import inputDialog from '@/inputDialog.js';
import notificationDialog from '@/notificationDialog.js';

import {authStore} from '@/stores/authStore.js';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

describe('AnalysisListingView', () => {
  let mockedData;
  let mockedImport;
  let mockedUser;
  let mockedLogout;
  let wrapper;
  let sandbox;

  beforeAll(() => {
    sandbox = sinon.createSandbox();
    mockedData = sandbox.stub(Analyses, 'all');
    mockedData.returns(fixtureData());

    mockedImport = sandbox.stub(Analyses, 'importPhenotipsAnalysis');

    mockedUser = sandbox.stub(authStore, 'fetchUser');
    mockedUser.returns('');

    mockedLogout = sandbox.stub(authStore, 'logout');

    wrapper = shallowMount(AnalysisListingView, {
      global: {
        components: {
          'font-awesome-icon': FontAwesomeIcon,
        },
        mocks: {
          $route: {
            push: sandbox.spy(),
          },
          $router: {
            push: sandbox.spy(),
          },
        },
      },
    });
  });

  afterAll(() => {
    sandbox.restore();
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

  it('Contains an analysis create card', async () => {
    const createCard = wrapper.findComponent(AnalysisCreateCard);
    expect(createCard.exists()).to.be.true;
  });

  it('Contains listing of Analyses', async () => {
    const cards = wrapper.findAllComponents(AnalysisCard);
    expect(cards).to.have.lengthOf(4);
  });

  it('Filters analyses by search event from search bar', async () => {
    const searchBarWrapper = wrapper.findComponent(AnalysisListingHeader);
    searchBarWrapper.vm.$emit('search', 'NM_1');

    await wrapper.vm.$nextTick();

    const cards = wrapper.findAllComponents(AnalysisCard);
    expect(cards).to.have.lengthOf(2);
  });

  it('should allow file upload to import a phenotips json on prompt', async ()=> {
    const createCard = wrapper.findComponent(AnalysisCreateCard);
    await createCard.trigger('click');

    const attachmentData = {
      data: {
        name: 'fake-import-phenotips.json',
      },
    };
    inputDialog.confirmation(attachmentData);
    await wrapper.vm.$nextTick();

    expect(mockedImport.called).to.be.true;
  });

  it('should render notification with a sucessful upload', async () => {
    const createCard = wrapper.findComponent(AnalysisCreateCard);
    await createCard.trigger('click');

    const attachmentData = {
      data: {
        name: 'fake-import-phenotips.json',
      },
    };
    inputDialog.confirmation(attachmentData);
    await wrapper.vm.$nextTick();

    const dialogComponent = wrapper.findComponent(NotificationDialog);
    expect(dialogComponent.exists()).to.be.true;
  });

  it('should render notification for a failed upload', async () => {
    mockedImport.throws('broken import sad face');
    const createCard = wrapper.findComponent(AnalysisCreateCard);
    await createCard.trigger('click');

    const attachmentData = {
      data: {
        name: 'fake-import-phenotips.json',
      },
    };
    inputDialog.confirmation(attachmentData);
    await wrapper.vm.$nextTick();

    const dialogComponent = wrapper.findComponent(NotificationDialog);
    expect(dialogComponent.exists()).to.be.true;
    expect(notificationDialog.state.title).to.equal('Failed to import phenotips analysis');
    expect(notificationDialog.state.message.toString()).to.equal('broken import sad face');
  });

  it('should logout when the analysis listing header emits the logout event', async () => {
    const header = wrapper.findComponent(AnalysisListingHeader);
    header.vm.$emit('logout');
    await header.vm.$nextTick();

    expect(mockedLogout.called).to.be.true;
    expect(wrapper.vm.$router.push.called).to.be.true;
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
