import {it, expect, describe, beforeEach} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import InputDialog from '@/components/Dialogs/InputDialog.vue';
import InputDialogAttachUrl from '@/components/Dialogs/InputDialogAttachUrl.vue';
import InputDialogUploadFile from '@/components/Dialogs/InputDialogUploadFile.vue';

import inputDialog from '@/inputDialog.js';

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

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
          .file(includeComments, 'file', '.pdf, .jpg, .jpeg, .png')
          .url(includeComments, includeName)
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
  });
});

