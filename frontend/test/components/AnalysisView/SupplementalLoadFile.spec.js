import {describe, it, beforeEach, expect} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import SupplementalLoadFile from '../../../src/components/AnalysisView/SupplementalLoadFile.vue';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

describe('SupplementalLoadFile.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallowMount(SupplementalLoadFile, {
      global: {
        components: {
          'font-awesome-icon': FontAwesomeIcon,
        },
      },
    });
  });

  it('Vue instance exists and it is an object', () => {
    expect(typeof wrapper).toBe('object');
  });

  it('should emit "changed" when file is input', async () => {
    const actualFile = 'fakeFile.ext';
    wrapper.vm.$refs.file.files = [actualFile];

    const input = wrapper.find('[data-test=attach-file-button]');
    await input.trigger('change');

    expect(wrapper.emitted().changed).to.not.be.undefined;
    expect(wrapper.emitted().changed[0][0]).to.equal(actualFile);
  });

  it('should emit "changed" when comment is input', async () => {
    const actualComments = 'it-is-a-comment';

    const input = wrapper.find('[data-test=comments-text-area]');
    input.setValue(actualComments);

    await input.trigger('change');

    expect(wrapper.emitted().changed).to.not.be.undefined;
    expect(wrapper.emitted().changed[0][1]).to.equal(actualComments);
  });

  it('should display the file dropped in the component', async () => {
    const eventObject = {
      dataTransfer: {
        files: [{name: 'fakeFile.ext'}],
      },
    };

    const fileInput = wrapper.find('[class=drop-file-box]');
    await fileInput.trigger('drop', eventObject);

    const fileNameText = wrapper.find('[id=fileName]');

    expect(fileNameText.text()).to.be.equal('fakeFile.ext  remove');
  });

  it('should remove the file chosen to upload remove button clicked', async () => {
    const eventObject = {
      dataTransfer: {
        files: [{name: 'fakeFile.ext'}],
      },
    };

    const fileInput = wrapper.find('[id=attachFileBtn]');
    await fileInput.trigger('drop', eventObject);

    const fileListedComponent = wrapper.find('tr');
    const removeButton = fileListedComponent.get('[id=removeBtn]');
    await removeButton.trigger('click');

    const tableBody = wrapper.find('tbody');
    expect(tableBody.exists()).to.be.false;
  });
});

