import {it, expect, describe, beforeEach} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import PhenotipsImportModal from '@/components/AnalysisListing/PhenotipsImportModal.vue';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

describe('PhenotipsImportModal.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallowMount(PhenotipsImportModal, {
      global: {
        components: {
          'font-awesome-icon': FontAwesomeIcon,
        },
      },
    });
  });

  it('should close the modal when clicking on the close button.', async () => {
    wrapper.find('[data-test=cancel-button]').trigger('click');
    expect(wrapper.emitted().close).to.not.be.undefined;
  });

  it('should emit "addfile" when clicking on the add button', async () => {
    wrapper.find('[data-test=add-button]').trigger('click');
    expect(wrapper.emitted().upload).to.not.be.undefined;
  });

  it('should display the file uploaded when file is inputted', async () => {
    wrapper.vm.$refs.file.files = [{name: 'fakeFile.ext'}];

    const fileInput = wrapper.find('[id=attach-file-button]');
    await fileInput.trigger('change');

    const fileNameText = wrapper.find('[class=file-name]');

    expect(fileNameText.text()).to.be.equal('fakeFile.ext  remove');
  });

  it('should display the file dropped in the component', async () => {
    const eventObject = {
      dataTransfer: {
        files: [{name: 'fakeFile.ext'}],
      },
    };

    const fileInput = wrapper.find('[id=attach-file-button]');
    await fileInput.trigger('drop', eventObject);

    const fileNameText = wrapper.find('[class=file-name]');

    expect(fileNameText.text()).to.be.equal('fakeFile.ext  remove');
  });

  it('should remove the file chosen to upload remove button clicked', async () => {
    const eventObject = {
      dataTransfer: {
        files: [{name: 'fakeFile.ext'}],
      },
    };

    const fileInput = wrapper.find('[id=attach-file-button]');
    await fileInput.trigger('drop', eventObject);

    const fileListedComponent = wrapper.find('tr');
    const removeButton = fileListedComponent.get('[class=remove-button]');
    await removeButton.trigger('click');

    const tableBody = wrapper.find('tbody');
    expect(tableBody.exists()).to.be.false;
  });
});

