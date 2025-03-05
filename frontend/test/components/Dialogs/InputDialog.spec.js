import {it, expect, describe, beforeEach} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import InputDialog from '@/components/Dialogs/InputDialog.vue';
import InputDialogAttachUrl from '@/components/Dialogs/InputDialogAttachUrl.vue';
import InputDialogUploadFile from '@/components/Dialogs/InputDialogUploadFile.vue';

import inputDialog from '@/inputDialog.js';

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';
import InputDialogExistingAttachments from '../../../src/components/Dialogs/InputDialogExistingAttachments.vue';

describe('InputDialog.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallowMount(InputDialog, {
      global: {
        components: {
          'font-awesome-icon': FontAwesomeIcon,
        },
      },
    });
  });

  describe('when prompting to input a URL and File', () => {
    beforeEach(() => {
      const includeComments = true;
      const includeName = true;

      inputDialog
          .confirmText('Add')
          .cancelText('Cancel')
          .file(includeComments, 'file', '.pdf, .jpg, .jpeg, .png, .gb')
          .url(includeComments, includeName)
          .existing()
          .message('Warning message')
          .prompt();
    });

    it('Should render the dialog', async () => {
      await wrapper.vm.$nextTick();

      const modalsBackgroundElement = wrapper.find('.modal-background');
      expect(modalsBackgroundElement.exists()).to.be.true;
    });

    it('Should close the modal when clicking on the close button.', async () => {
      await wrapper.vm.$nextTick();

      wrapper.find('[data-test=cancel]').trigger('click');
      await wrapper.vm.$nextTick();

      const modalsBackgroundElement = wrapper.find('.modal-background');
      expect(modalsBackgroundElement.exists()).to.be.false;
    });

    it('Should prompt adding adding when clicking on the add button', async () => {
      inputDialog.prompt().then((confirmed) => {
        expect(confirmed).to.be.exist;
      });
      await wrapper.vm.$nextTick();

      const confirmButton = wrapper.find('[data-test=confirm]');
      expect(confirmButton.text()).to.equal('Add');
      confirmButton.trigger('click');
    });

    it('Should show the attach url tab when clicking on the link tab', async () => {
      await wrapper.find('[data-test=button-input-dialog-attach-url]').trigger('click');
      const attachUrlComponent = wrapper.findComponent(InputDialogAttachUrl);
      expect(attachUrlComponent.exists()).to.be.true;
    });

    it('Should show the upload file tab when clicking the file tab', async () => {
      await wrapper.find('[data-test=button-input-dialog-upload-file]').trigger('click');
      const uploadFileComponent = wrapper.findComponent(InputDialogUploadFile);
      expect(uploadFileComponent.exists()).to.be.true;
    });

    it('Should show the rosalution existing evidence tab when clicking the Rosalution tab', async () => {
      const inputDialogRosalutionTab = wrapper.find('[data-test=button-input-dialog-existing-attachments]');
      await inputDialogRosalutionTab.trigger('click');
      const existingAttachmentsComponent = wrapper.findComponent(InputDialogExistingAttachments);
      expect(existingAttachmentsComponent.exists()).to.be.true;
    });

    it('Should show the warning message when one is set', async () => {
      const warningMessageElement = wrapper.find('[data-test=warning-message]');
      expect(warningMessageElement.exists()).to.be.true;
      expect(warningMessageElement.text()).to.equal('Warning message');
    });

    it('Should not show the warning message when one is not set', async () => {
      inputDialog.message('');
      await wrapper.vm.$nextTick();

      const warningMessageElement = wrapper.find('[data-test=warning-message]');
      expect(warningMessageElement.exists()).to.be.false;
    });

    it('Should render raw html in the warning message', async () => {
      inputDialog.message('<b>Bolded Text</b>');
      await wrapper.vm.$nextTick();

      const warningMessageElement = wrapper.find('[data-test=warning-message]');
      expect(warningMessageElement.exists()).to.be.true;
      expect(warningMessageElement.text()).to.equal('Bolded Text');
      expect(warningMessageElement.html()).to.contain('<b>Bolded Text</b>');
    });
  });
});

