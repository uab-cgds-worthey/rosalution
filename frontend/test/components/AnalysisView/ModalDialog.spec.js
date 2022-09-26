import {it, expect, describe, beforeEach} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import ModalDialog from '../../../src/components/AnalysisView/ModalDialog.vue';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

describe('ModalDialog.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallowMount(ModalDialog, {
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

  it('Should show the supplemental load link when clicking on the link tab', async () => {
    await wrapper.find('[data-test=link-tab-button]').trigger('click');
    const supplementalLoadLink = wrapper.find('[data-test=supplemental-load-link]');
    expect(supplementalLoadLink.exists()).toBe(true);
  });

  it('Should show the supplemental load file when clicking on the file tab', async () => {
    await wrapper.find('[data-test=file-tab-button]').trigger('click');
    const supplementalLoadFile = wrapper.find('[data-test=supplemental-load-file]');
    expect(supplementalLoadFile.exists()).toBe(true);
  });
});

