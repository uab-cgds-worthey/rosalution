import {describe, it, beforeEach, expect} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import InputDialogUploadFile from '@/components/Dialogs/InputDialogUploadFile.vue';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

describe('InputDialogUploadFile.vue', () => {
  let wrapper;
  describe('basic upload file dialog', () => {
    beforeEach(() => {
      const defaultProps = {
        userInput: {
          'data': '',
          'comments': '',
        },
      };
      wrapper = shallowMount(InputDialogUploadFile, {
        props: {
          ...defaultProps,
        },
        global: {
          components: {
            'font-awesome-icon': FontAwesomeIcon,
          },
        },
      });
    });

    it('should emit "changed" when file is input', async () => {
      const actualFile = 'fakeFile.ext';
      wrapper.vm.$refs.file.files = [actualFile];

      const input = wrapper.find('[id=attach-file-button]');
      await input.trigger('change');

      expect(wrapper.emitted()['update:userInput']).to.not.be.undefined;
      expect(wrapper.emitted()['update:userInput'][0][0]['data']).to.equal(actualFile);
    });

    it('should emit "changed" when comment is input', async () => {
      const actualComments = 'it-is-a-comment';

      const input = wrapper.find('.comments');
      input.setValue(actualComments);

      await input.trigger('change');

      expect(wrapper.emitted()['update:userInput']).to.not.be.undefined;
      expect(wrapper.emitted()['update:userInput'][0][0]['comments']).to.equal(actualComments);
    });

    it('should display the file dropped in the component', async () => {
      const eventObject = {
        dataTransfer: {
          files: [{name: 'fakeFile.ext'}],
        },
      };

      const fileInput = wrapper.find('.drop-file-box');
      await fileInput.trigger('drop', eventObject);

      const fileNameText = wrapper.find('.file-name');

      expect(fileNameText.text()).to.be.equal('fakeFile.ext  remove');
    });

    it('should remove the file chosen to upload remove button clicked', async () => {
      const eventObject = {
        dataTransfer: {
          files: [{name: 'fakeFile.ext'}],
        },
      };

      const fileInput = wrapper.find('#attach-file-button');
      await fileInput.trigger('drop', eventObject);

      const fileNameElement = wrapper.find('.file-name');
      const removeButton = fileNameElement.get('button');
      await removeButton.trigger('click');

      const fileNameContent = wrapper.find('span');
      expect(fileNameContent.exists()).to.be.false;
    });
  });

  describe('basic upload file dialog with form', () => {
    beforeEach(() => {
      const defaultProps = {
        userInput: {
          'data': '',
          'comments': '',
          'projectSelect': {
            'selected': '695d5b157709ebcd1c7325c0',
            'options': [
              {
                'value': '695d5b157709ebcd1c7325c0',
                'text': 'Ciliopathies',
              },
              {
                'value': '695d5b157709ebcd1c7325c1',
                'text': 'CPAM',
              },
              {
                'value': '695d5b157709ebcd1c7325c4',
                'text': 'LW',
              },
            ],
          },
        },
      };
      wrapper = shallowMount(InputDialogUploadFile, {
        props: {
          ...defaultProps,
        },
        global: {
          components: {
            'font-awesome-icon': FontAwesomeIcon,
          },
        },
      });
    });

    it('should render select input for form', async () => {
      const input = wrapper.find('[id=project-select]');
      expect(input.exists()).toBe(true);
    });

    it('should emit update:userInput when item is selected', async () => {
      const input = wrapper.find('[id=project-select]');
      await input.setValue('695d5b157709ebcd1c7325c1');
      expect(wrapper.emitted()['update:userInput'][0][0]['projectSelect']['selected'])
          .to.equal('695d5b157709ebcd1c7325c1');
    });
  });
});

