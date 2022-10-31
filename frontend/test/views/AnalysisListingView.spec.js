import {describe, it, expect, beforeEach, afterEach} from 'vitest';
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
  let mockedLogout;
  let wrapper;
  let sandbox;

  beforeEach(() => {
    sandbox = sinon.createSandbox();
    mockedData = sandbox.stub(Analyses, 'all');
    mockedData.returns(fixtureData());

    mockedImport = sandbox.stub(Analyses, 'importPhenotipsAnalysis');

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

  afterEach(() => {
    sandbox.restore();
  });

  it('Analysis Listing contains a header and content', () => {
    const appHeader = wrapper.find('app-header');
    expect(appHeader.exists()).to.be.true;

    const appContent = wrapper.find('app-content');
    expect(appContent.exists()).to.be.true;
  });

  it('Contains an analysis create card', () => {
    const createCard = wrapper.findComponent(AnalysisCreateCard);
    expect(createCard.exists()).to.be.true;
  });

  it('Contains listing of Analyses', () => {
    const cards = wrapper.findAllComponents(AnalysisCard);
    expect(cards.length).to.equal(3);
  });

  it('Filters analyses when text from the search bar in header is updated', async () => {
    const searchBarWrapper = wrapper.findComponent(AnalysisListingHeader);
    searchBarWrapper.vm.$emit('update:searchText', 'ON');

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
    name: 'CPAM0046',
    genomic_units: [{
      gene: 'LMNA',
      transcripts: ['NM_170707.3'],
      variants: [],
    }],
    nominated_by: 'Dr. Person Two',
    latest_status: 'Approved',
    created_date: '2021-09-30',
    last_modified_date: '2021-10-01',
  },
  {
    name: 'CPAM0047',
    genomic_units: [{
      gene: 'SBF1ON',
      transcripts: ['NM_002972.2'],
      variants: [],
    }],
    nominated_by: 'CMT4B3 Foundation',
    latest_status: 'Declined',
    created_date: '2020-12-03',
    last_modified_date: '2021-12-12',
  },
  {
    name: 'CPAM0053',
    genomic_units: [{
      gene: 'PEX10',
      transcripts: ['NM_153818.2'],
    }],
    nominated_by: 'N/A',
    latest_status: 'Ready',
    created_date: '2021-11-02',
    last_modified_date: '2021-11-23',
  },
  ];
}
