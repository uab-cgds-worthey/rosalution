import {test, expect} from 'vitest';
import {shallowMount, mount} from '@vue/test-utils';

import ModalDialog from '../../../src/components/AnalysisView/ModalDialog.vue';
import SupplementalLoadLink from '../../../src/components/AnalysisView/SupplementalLoadLink.vue';

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

test.only('Should clear the supplemental load link when clicking on the clear button', async () => {
  const wrapper = mount(ModalDialog);
  await wrapper.find('[data-test=link-tab-button]').trigger('click');
  await wrapper.vm.$nextTick();
  // const supplementalLoadLinkWrapper = mount(wrapper.find('[data-test=supplemental-load-link]'));
  const supplementalLoadLinkWrapper = wrapper.findComponent(SupplementalLoadLink);
  // console.log('LOAD LINK MOUNTED!!!!!!!!!!!!!!!!!!!!!!!!');
  // console.log(supplementalLoadLinkWrapper);
  // expect(supplementalLoadLink.exists()).toBe(true);
  // console.log(supplementalLoadLinkWrapper);
  // console.log('link loads is true');
  const actualLinkName = 'it-is-a-link-name';
  // const actualLink = 'it-is-a-link';
  // const actualComments = 'it-is-a-comment';

  // const linkNameInput = supplementalLoadLinkWrapper.find('[data-test=link-name-input]');
  // expect(linkNameInput.exists()).toBe(true);
  // console.log('HERE!!!!!!!!!!!!!!!!!!!');
  // console.log(linkNameInput);
  await supplementalLoadLinkWrapper.setData({linkNameUploaded: actualLinkName});
  expect(supplementalLoadLinkWrapper.vm.linkNameUploaded).to.equal(actualLinkName);
  // linkNameInput.setValue(actualLinkName);
  // await linkNameInput.trigger('change');
  // const linkInput = wrapper.find('[data-test=link-input]');
  // linkInput.setValue(actualLink);

  // const commentsInput = wrapper.find('[data-test=comments-text-area]');
  // commentsInput.setValue(actualComments);

  const clearBtn = wrapper.find('[data-test=clear-modal]');
  // console.log(clearBtn);
  await clearBtn.trigger('click');
  console.log('CLEAR IS CLICKEd');
  // await supplementalLoadLinkWrapper.vm.$nextTick();
  expect(supplementalLoadLinkWrapper.vm.linkNameUploaded).toBe('');
});

test.skip('Should clear the supplemental load file when clicking on the clear button', async () => {
  const wrapper = shallowMount(ModalDialog);
  await wrapper.find('[data-test=file-tab-button]').trigger('click');
  const supplementalLoadFile = wrapper.find('[data-test=supplemental-load-file]');

  expect(supplementalLoadFile.exists()).toBe(true);

  const actualComments = 'it-is-a-comment';

  const input = wrapper.find('[data-test=comments-text-area]');
  expect(input.exists()).toBe(true);
  input.setValue(actualComments);

  await wrapper.find('[data-test=clear-modal]').trigger('click');

  expect(input.html()).toBe('');
});
