import {it, expect, describe, beforeEach} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import SaveModal from '../../../src/components/AnalysisView/SaveModal.vue';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

describe('SaveModal.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallowMount(SaveModal, {
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

  it('Should emit "canceledit" when clicking on the cancel button', async () => {
    wrapper.find('[data-test=cancel-edit-button]').trigger('click');
    expect(wrapper.emitted().canceledit).to.not.be.undefined;
  });
});
