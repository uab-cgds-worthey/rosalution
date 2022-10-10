import {it, expect, describe, beforeEach} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import SectionImportModal from '../../../src/components/AnalysisView/SectionImportModal.vue';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

describe('SectionImportModal.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallowMount(SectionImportModal, {
      global: {
        components: {
          'font-awesome-icon': FontAwesomeIcon,
        },
      },
    });
  });

  it('Vue instance exists and it is an object', () => {
    expect(typeof wrapper).toBe('object');
  });

  it('Should close the modal when clicking on the close button.', async () => {
    wrapper.find('[data-test=cancel-button]').trigger('click');
    expect(wrapper.emitted().close).to.not.be.undefined;
  });

  it('Should emit "addfile" when clicking on the add button', async () => {
    wrapper.find('[data-test=add-button]').trigger('click');
    expect(wrapper.emitted().add).to.not.be.undefined;
  });

  it('should display the file dropped in the component', async () => {
    const eventObject = {
      dataTransfer: {
        files: [{name: 'fakeFile.ext'}],
      },
    };

    const fileInput = wrapper.find('[class=drop-file-box]');
    await fileInput.trigger('drop', eventObject);

    const fileNameText = wrapper.find('[class=file-name]');

    expect(fileNameText.text()).to.be.equal('fakeFile.ext  remove');
  });
});

