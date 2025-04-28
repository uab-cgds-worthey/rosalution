import {expect, describe, it} from 'vitest';
import {shallowMount} from '@vue/test-utils';
import CredentialsBox from '@/components/AccountView/CredentialsBox.vue';

/**
 * helper function that shallow mounts and returns the rendered component
 * @param {props} props props for testing to overwrite default props
 * @return {VueWrapper} returns a shallow mounted using props
 */
function getMountedComponent(props) {
  const defaultProps = {
    header: '',
    clientId: '',
    clientSecret: '',
    content: [],
  };

  return shallowMount(CredentialsBox, {
    props: {...defaultProps, ...props},
  });
}

describe('CredentialsBox.vue', () => {
  it('renders the clientId prop', () => {
    const clientId = 'test-client-id';
    const wrapper = getMountedComponent({clientId});

    expect(wrapper.find('[data-test="client-id-value-row"]').text()).to.contain(clientId);
  });

  it('emits display-secret event when clientSecret is clicked', async () => {
    const clientSecret = 'test-client-secret';
    const wrapper = getMountedComponent({clientSecret});

    await wrapper.find('.clickable-text').trigger('click');
    expect(wrapper.emitted()).to.have.property('display-secret');
    expect(wrapper.emitted()['display-secret']).to.have.length(1);
  });

  it('emits generateSecret event when Generate Secret button is clicked', async () => {
    const wrapper = getMountedComponent();

    await wrapper.find('.generate-button').trigger('click');
    expect(wrapper.emitted()).to.have.property('generate-secret');
    expect(wrapper.emitted()['generate-secret']).to.have.length(1);
  });
});
