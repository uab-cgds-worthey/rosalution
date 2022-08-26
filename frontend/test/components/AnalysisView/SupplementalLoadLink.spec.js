import {describe, it, beforeEach, expect} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import SupplementalLoadLink from '../../../src/components/AnalysisView/SupplementalLoadLink.vue';

describe('SupplementalLoadLink.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallowMount(SupplementalLoadLink);
  });

  it('renders a vue instance', () => {
    expect(typeof wrapper).toBe('object');
  });

  it('should emit "linknameadded" when link name is inputted', async () => {
    const actualLinkName = 'it-is-a-link-name';

    const input = wrapper.find('[data-test=link-name-input]');
    input.setValue(actualLinkName);

    await input.trigger('change');

    expect(wrapper.emitted().linknameadded).to.not.be.undefined;
    expect(wrapper.emitted().linknameadded[0]).deep.to.equal([actualLinkName]);
  });

  it('should emit "linkadded" when link is inputted', async () => {
    const actualLink = 'it-is-a-link';

    const input = wrapper.find('[data-test=link-input]');
    input.setValue(actualLink);

    await input.trigger('change');

    expect(wrapper.emitted().linkadded).to.not.be.undefined;
    expect(wrapper.emitted().linkadded[0]).deep.to.equal([actualLink]);
  });

  it('should emit "commentadded" when comment is inputted', async () => {
    const actualComments = 'it-is-a-comment';

    const input = wrapper.find('[data-test=comments-text-area]');
    input.setValue(actualComments);

    await input.trigger('change');

    expect(wrapper.emitted().commentadded).to.not.be.undefined;
    expect(wrapper.emitted().commentadded[0]).deep.to.equal([actualComments]);
  });
});
