import {test, expect} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import ModalDialog from '../../../src/components/AnalysisView/ModalDialog.vue';
// import SupplementalLoadLink from '../../../src/components/AnalysisView/SupplementalLoadLink.vue';

test('Vue instance exists and it is an object', () => {
  const wrapper = shallowMount(ModalDialog);
  expect(typeof wrapper).toBe('object');
});

test('Should close the modal when clicking on the close button.', async () => {
  const wrapper = shallowMount(ModalDialog);
  wrapper.find('[data-test=cancel-modal]').trigger('click');
  expect(wrapper.emitted().cancelmodal).to.not.be.undefined;
});

test('Should emit "addfile" when clicking on the add button', async () => {
  const wrapper = shallowMount(ModalDialog);
  wrapper.find('[data-test=add-button]').trigger('click');
  expect(wrapper.emitted().addattachment).to.not.be.undefined;
});

test('Should close the modal after clicking on the add button', async () => {
  const wrapper = shallowMount(ModalDialog);
  wrapper.find('[data-test=add-button]').trigger('click');
  expect(wrapper.emitted().cancelmodal).to.not.be.undefined;
});

test('Should show the supplemental load link when clicking on the link tab', async () => {
  const wrapper = shallowMount(ModalDialog);
  await wrapper.find('[data-test=link-tab-button]').trigger('click');
  const supplementalLoadLink = wrapper.find('[data-test=supplemental-load-link]');

  expect(supplementalLoadLink.exists()).toBe(true);
});

test('Should show the supplemental load file when clicking on the file tab', async () => {
  const wrapper = shallowMount(ModalDialog);
  await wrapper.find('[data-test=file-tab-button]').trigger('click');
  const supplementalLoadFile = wrapper.find('[data-test=supplemental-load-file]');

  expect(supplementalLoadFile.exists()).toBe(true);
});

test('Should clear the supplemental load link when clicking on the clear button', async () => {
  const wrapper = shallowMount(ModalDialog);
  await wrapper.find('[data-test=link-tab-button]').trigger('click');
  await wrapper.vm.$nextTick();
  // const supplementalLoadLink = wrapper.find('[data-test=supplemental-load-link]');
  const actualLinkName = 'it-is-a-link-name';
  const actualLink = 'it-is-a-link';
  const actualComments = 'it-is-a-comment';

  const linkNameInput = wrapper.find('[data-test=link-name-input]');
  expect(linkNameInput.exists()).toBe(true);
  linkNameInput.setValue(actualLinkName);

  const linkInput = wrapper.find('[data-test=link-input]');
  linkInput.setValue(actualLink);

  const commentsInput = wrapper.find('[data-test=comments-text-area]');
  commentsInput.setValue(actualComments);

  await wrapper.find('[data-test=clear-modal]').trigger('click');

  expect(linkNameInput.getValue()).toBe('');
});

test.skip('Should clear the supplemental load file when clicking on the clear button', async () => {
  const wrapper = shallowMount(ModalDialog);
  await wrapper.find('[data-test=file-tab-button]').trigger('click');
  const supplementalLoadFile = wrapper.find('[data-test=supplemental-load-file]');

  expect(supplementalLoadFile.exists()).toBe(true);
});
