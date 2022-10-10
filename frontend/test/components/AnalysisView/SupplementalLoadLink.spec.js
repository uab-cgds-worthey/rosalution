import {describe, it, beforeEach, expect} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import SupplementalLoadLink from '../../../src/components/AnalysisView/SupplementalLoadLink.vue';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

describe('SupplementalLoadLink.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallowMount(SupplementalLoadLink, {
      global: {
        components: {
          'font-awesome-icon': FontAwesomeIcon,
        },
      },
    });
  });

  it('renders a vue instance', () => {
    expect(typeof wrapper).toBe('object');
  });

  it('should emit "changed" when link name is inputted', async () => {
    const actualLinkName = 'it-is-a-link-name';

    const input = wrapper.find('[data-test=link-name-input]');
    input.setValue(actualLinkName);

    await input.trigger('change');

    expect(wrapper.emitted().changed).to.not.be.undefined;
    expect(wrapper.emitted().changed[0][0].name).to.equal('it-is-a-link-name');
  });

  it('should emit "changed" when link is inputted', async () => {
    const actualLink = 'it-is-a-link';

    const input = wrapper.find('[data-test=link-input]');
    input.setValue(actualLink);

    await input.trigger('change');

    expect(wrapper.emitted().changed).to.not.be.undefined;
    expect(wrapper.emitted().changed[0][0].link).to.equal('it-is-a-link');
  });

  it('should emit "changed" when comment is inputted', async () => {
    const actualComments = 'it-is-a-comment';

    const input = wrapper.find('[data-test=comments-text-area]');
    input.setValue(actualComments);

    await input.trigger('change');

    expect(wrapper.emitted().changed).to.not.be.undefined;
    expect(wrapper.emitted().changed[0][0].comment).to.equal('it-is-a-comment');
  });
});
