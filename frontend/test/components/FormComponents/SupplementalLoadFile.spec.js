import {test, expect, describe} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import SupplementalLoadFile from '../../../src/components/FormComponents/SupplementalLoadFile.vue';

describe('SupplementalLoadFile.vue', () => {
    let wrapper;

    beforeEach(() => {
        wrapper = shallowMount(SupplementalLoadFile);
      });

    it('Vue instance exists and it is an object', () => {
        expect(typeof wrapper).toBe('object');
    });

    it('should emit "fileadded" when file is inputted', async () => {
        const actualFile = 'fakeFile.ext';
        wrapper.vm.$refs.file.files = actualFile;

        const input = wrapper.find('[data-test=attach-file-button]');
        await input.trigger('change');

        expect(wrapper.emitted().fileadded).to.not.be.undefined;
        expect(wrapper.emitted().fileadded[0]).deep.to.equal([actualFile]);
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

