import {describe, it, beforeEach, expect} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import SupplementalFormList from '../../../src/components/AnalysisView/SupplementalFormList.vue';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

/**
 * Helper mounts and returns the rendered component
 * @param {props} props props for testing to overwrite default props
 * @return {VueWrapper} returns a shallow mounted using props
 */
function getMountedComponent(props) {
  return shallowMount(SupplementalFormList, {
    props: {...props},
    attachTo: document.body,
    global: {
      components: {
        'font-awesome-icon': FontAwesomeIcon,
      },
    },
  });
}

describe('SupplementalFormList.vue', () => {
  let wrapper;
  const defaultAttachment = {
    data: 'fakeFiledData',
    name: '/path/to/fakeFile.ext',
    type: 'file',
  };

  beforeEach(() => {
    wrapper = getMountedComponent({
      attachments: [defaultAttachment],
    });
  });

  it('plus icon emits open modal event', async () => {
    const button = wrapper.find('[data-test=add-button]');

    await button.trigger('click');

    expect(wrapper.emitted().openModal).to.not.be.undefined;
  });

  it('should render each attachemnt', async () => {
    const attachmentRow = wrapper.get('.attachment-row');
    expect(attachmentRow.text()).to.equal('/path/to/fakeFile.ext');
  });

  it('should emit remove for the designated attachment', async () => {
    const attachmentRow = wrapper.get('.attachment-row');
    await attachmentRow.get('[data-test=delete-button]').trigger('click');

    const attachmentToDelete = wrapper.emitted().delete[0][0];
    expect(attachmentToDelete.data).to.equal('fakeFiledData');
    expect(attachmentToDelete.name).to.equal('/path/to/fakeFile.ext');
    expect(attachmentToDelete.type).to.equal('file');
  });

  it('should emit edit for the designated attachment', async () => {
    const attachmentRow = wrapper.get('.attachment-row');
    await attachmentRow.get('[data-test=edit-button]').trigger('click');

    const attachmentToEdit = wrapper.emitted().edit[0][0];
    expect(attachmentToEdit.data).to.equal('fakeFiledData');
    expect(attachmentToEdit.name).to.equal('/path/to/fakeFile.ext');
    expect(attachmentToEdit.type).to.equal('file');
  });
});
