import {expect, describe, it, beforeAll, afterAll} from 'vitest';
import {config, shallowMount} from '@vue/test-utils';

import Header from '@/components/Header.vue';

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';
import {RouterLink} from 'vue-router';

/**
 * helper function that shadllow mounts and returns the rendered component
 * @param {props} props props for testing to overwrite default props
 * @return {VueWrapper} returns a shallow mounted using props
 */
function getMountedComponent(props) {
  const defaultProps = {
    username: '',
  };

  return shallowMount(Header, {
    props: {...defaultProps, ...props},
    global: {
      components: {
        'font-awesome-icon': FontAwesomeIcon,
        'router-link': RouterLink,
      },
    },
  });
}

beforeAll(() => {
  config.renderStubDefaultSlot = true;
});

afterAll(() => {
  config.renderStubDefaultSlot = false;
});

describe('HeaderComponent.vue', () => {
  it('should display application title by default', () => {
    const wrapper = getMountedComponent();
    const headerTextLink = wrapper.find('[data-test="header-title-text"]');
    expect(headerTextLink.html()).to.contains('rosalution');
  });

  it('should display the title route the the analysis listing by default', () => {
    const wrapper = getMountedComponent();
    const headerTextLink = wrapper.get('[data-test="header-title-text"]');
    // console.log(JSON.stringify(headerTextLink.attributes().to, null, 4));
    // Object.keys(headerTextLink.attributes().to).forEach((prop)=> console.log(prop));
    // console.log(headerTextLink.attributes('to')['path'])
    // const toProp = headerTextLink.attributes('to');
    // Object.values(toProp).forEach((prop)=> console.log(prop));
    console.log(headerTextLink.html());
    console.log(headerTextLink.vm);

    // expect(headerTextLink.attribute('to')).to.contain('rosalution');
  });

  it('should display "Login" in the upper right hand corner if username is a blank string', async () => {
    const wrapper = getMountedComponent();

    const userMenuWrapper = wrapper.find('[data-test=user-menu]');

    expect(userMenuWrapper.text()).to.contain('LOGIN');
  });

  it('should properly display the username in the upper right hand corner', async () => {
    const wrapper = getMountedComponent({
      username: 'UABProvider',
    });
    const userMenuWrapper = wrapper.find('[data-test=user-text]');

    expect(userMenuWrapper.text()).to.contain('UABProvider');
  });
});
