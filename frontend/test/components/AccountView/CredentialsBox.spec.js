import {expect, describe, it, beforeEach, afterEach} from 'vitest';
import {shallowMount} from '@vue/test-utils';
import CredentialsBox from '@/components/AccountView/CredentialsBox.vue';
import sinon from 'sinon';

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
  let displaySecretSpy;
  let generateSecretSpy;

  beforeEach(() => {
    displaySecretSpy = sinon.spy(CredentialsBox.methods, 'displaySecret');
    generateSecretSpy = sinon.spy(CredentialsBox.methods, 'generateSecret');
  });

  afterEach(() => {
    displaySecretSpy.restore();
    generateSecretSpy.restore();
  });

  it('renders the header prop', () => {
    const header = 'Test Header';
    const wrapper = getMountedComponent({header});

    expect(wrapper.find('.credentials-name').text()).toContain(header);
  });

  it('renders the clientId prop', () => {
    const clientId = 'test-client-id';
    const wrapper = getMountedComponent({clientId});

    expect(wrapper.find('[data-test="client-id-value-row"]').text()).toContain(clientId);
  });

  it('emits display-secret event when clientSecret is clicked', async () => {
    const clientSecret = 'test-client-secret';
    const wrapper = getMountedComponent({clientSecret});

    await wrapper.find('.clickable-text').trigger('click');
    expect(displaySecretSpy.calledOnce).toBe(true);
  });

  it('emits generateSecret event when Generate Secret button is clicked', async () => {
    const wrapper = getMountedComponent();

    await wrapper.find('.button').trigger('click');
    expect(generateSecretSpy.calledOnce).toBe(true);
  });
});
