import {test, expect} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import ModalDialog from '../../../src/components/FormComponents/ModalDialog.vue';

test('Vue instance exists and it is an object', () => {
    const wrapper = shallowMount(ModalDialog);
    expect(typeof wrapper).toBe('object');
});

test('Should close the modal when clicking on the close button.', async () => {
    const wrapper = shallowMount(ModalDialog);
    wrapper.find('[data-test=close-modal]').trigger('click');
    expect(wrapper.emitted().closemodal).to.not.be.undefined;
})

test('Should emit "addfile" when clicking on the add button', async () => {
    const wrapper = shallowMount(ModalDialog);
    wrapper.find('[data-test=add-button]').trigger('click');
    expect(wrapper.emitted().addattachment).to.not.be.undefined;
})

test('Should close the modal after clicking on the add button', async () => {
    const wrapper = shallowMount(ModalDialog);
    wrapper.find('[data-test=add-button]').trigger('click');
    expect(wrapper.emitted().closemodal).to.not.be.undefined;
})